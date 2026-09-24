#!/usr/bin/env python3
"""
Monte-Carlo simulation of the Chronometric Cooperative Ground Beacon (refined).

Recovers the GNSS-referenced mid-exposure time of the image line in which a
surveyed array of phase-stepped emitters was integrated by an orbital imager,
and from it the time-tag error and (separately) the pitch/alignment error.

Error sources modelled (truth side):
  * photon (Poisson) shot noise of emitter + daylight background, read noise
  * atmospheric scintillation per head (log-normal, independent between heads,
    sigma_I from the Hufnagel-Valley 5/7 profile and the emitting-aperture size,
    via reciprocity with large-telescope stellar scintillation)
  * emitter layout errors: survey error, ground-velocity error, heading(yaw) error
  * TDI: window = boxcar(N_stages * T_line) convolved with the along-track LSF
    expressed in time; stage-count recovery from visibility with/without LSF
    (temporal-MTF) correction
  * GNSS timebase + driver latency residuals, waveform harmonic distortion,
    PSF-fit photometry error, PRNU/flat-field residual, residual nonlinearity,
    per-head amplitude spread (known to 0.1 % from monitor photodiodes),
    light-time and slant-range error, centroid error for line-tag interpolation

Also: waveform-family comparison (sinusoid / PN / chirp / on-off edge),
single-pass time-vs-pitch decomposition, and the multi-pitch-GCP design-around.

Only numpy is required.  Run:  python3 beacon_sim.py  (about 1-2 min)
"""
import numpy as np

RNG = np.random.default_rng(20260924)
C = 299_792_458.0
H_PLANCK = 6.62607015e-34

# --------------------------------------------------------------------------
# Numerics helpers
# --------------------------------------------------------------------------
def erf(x):
    """Abramowitz & Stegun 7.1.26, |err| < 1.5e-7."""
    s = np.sign(x)
    x = np.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * np.exp(-x * x)
    return s * y


def window_weights(tau, sig_lsf_t, dt=1.0e-6):
    """Temporal weighting of a point source's total collected energy.
    boxcar(tau) (N TDI rows crossed at 1 row / T_line, or a global shutter)
    convolved with the along-track LSF (optics+atmosphere+jitter) in time."""
    half = tau / 2 + 5 * max(sig_lsf_t, 1e-9)
    u = np.arange(-half, half + dt / 2, dt)
    if sig_lsf_t <= 0:
        w = ((u >= -tau / 2) & (u < tau / 2)).astype(float)
    else:
        s = np.sqrt(2) * sig_lsf_t
        w = 0.5 * (erf((u + tau / 2) / s) - erf((u - tau / 2) / s))
    w *= tau / (w.sum() * dt)          # normalise: integral(w) = tau
    return u, w * dt / tau             # weights sum to 1


# --------------------------------------------------------------------------
# Turbulence / scintillation (HV 5/7)
# --------------------------------------------------------------------------
def hv57_integrals():
    h = np.linspace(0, 40000, 400001)
    cn2 = (0.00594 * (21 / 27) ** 2 * (1e-5 * h) ** 10 * np.exp(-h / 1000)
           + 2.7e-16 * np.exp(-h / 1500) + 1.7e-14 * np.exp(-h / 100))
    return (np.trapezoid(cn2 * h ** 2, h), np.trapezoid(cn2 * h ** (5 / 6), h),
            np.trapezoid(cn2, h))


I_H2, I_H56, I_H0 = hv57_integrals()


def sigma_scint(D_src, lam=850e-9, zen_deg=0.0):
    """Short-exposure scintillation index (sigma_I) of an incoherent emitting
    aperture of diameter D_src seen from orbit.  By reciprocity this equals the
    aperture-averaged scintillation of a star seen by a ground telescope of
    diameter D_src (Osborn et al. 2015, large-aperture short-exposure form),
    capped by the weak-fluctuation point-aperture value."""
    X = 1 / np.cos(np.radians(zen_deg))
    large = np.sqrt(17.34 * D_src ** (-7 / 3) * X ** 3 * I_H2)
    point = np.sqrt(19.2 * lam ** (-7 / 6) * X ** (11 / 6) * I_H56)
    return float(min(large, point))


# --------------------------------------------------------------------------
# Photon budget
# --------------------------------------------------------------------------
def electrons(I_wsr, T_atm, R, D_ap, eta_opt, QE, tau, lam=850e-9):
    A = np.pi * (D_ap / 2) ** 2
    P = I_wsr * T_atm / R ** 2 * A * eta_opt
    return P / (H_PLANCK * C / lam) * QE * tau


# --------------------------------------------------------------------------
# Scenario definition
# --------------------------------------------------------------------------
BASE = dict(
    name="base",
    H=500e3, v_g=7060.0, gsd=0.75, n_tdi=8, lsf_px=0.70,  # LSF sigma (px) optics+atm+jitter
    D_ap=0.35, eta=0.7, QE=0.6, I_peak=30.0, T_atm=0.8,     # 30 W/sr in-band peak per head
    bg_px=260.0, read_e=30.0, n_eff_px=6.2,                 # PSF-fit noise-equivalent pixels
    periods=(2e-3, 32e-3, 0.512, 8.192), J=4, M_fine=1, n_ref=1,
    D_src=None,            # emitting-aperture diameter [m]; None -> no scintillation
    zen=0.0,
    spacing=4.0, heading_deg=12.0,
    survey_sig=0.0, vg_rel_err=0.0, yaw_err=0.0,
    t_gnss_common=0.0, t_head_jit=0.0,
    h2=0.0, h3=0.0, phot_err=0.0, prnu=0.0, nonlin=0.0,
    amp_spread=0.05, amp_known=0.0,
    range_err=0.0, cent_px=0.0,
    layout_correction=True,
    precomp=True,           # pass-specific drive-phase pre-compensation of along-track offsets
    lsf_corr=True, lsf_knowledge=0.10,
    prior_sig=0.5,          # a-priori (onboard) time uncertainty, s  (uniform +/- 1 s used)
    tag_err_true=350e-6,
    framing=False, tau_frame=None,
)


def derive(s):
    s = dict(s)
    s["T_L"] = s["gsd"] / s["v_g"]
    s["tau"] = s["tau_frame"] if s["framing"] else s["n_tdi"] * s["T_L"]
    s["sig_lsf_t"] = 0.0 if s["framing"] else s["lsf_px"] * s["T_L"]
    R = s["H"] / np.cos(np.radians(s["zen"]))
    s["R"] = R
    s["T_atm_eff"] = s["T_atm"] ** (1 / np.cos(np.radians(s["zen"])))
    s["S_peak"] = electrons(s["I_peak"], s["T_atm_eff"], R, s["D_ap"], s["eta"],
                            s["QE"], s["tau"])
    s["bg"] = s["bg_px"] * s["n_eff_px"]
    s["rn2"] = s["read_e"] ** 2 * s["n_eff_px"]
    s["sig_I"] = 0.0 if s["D_src"] is None else sigma_scint(s["D_src"], zen_deg=s["zen"])
    return s


def build_layout(s):
    """Heads: for each period group k, J phase steps; fine group repeated M times
    with cyclically permuted grid positions; plus n_ref constant references.
    Returns arrays: group idx (-1 = ref), step delay, x, y."""
    grp, dly = [], []
    for k, P in enumerate(s["periods"]):
        reps = s["M_fine"] if k == 0 else 1
        for _ in range(reps):
            for j in range(s["J"]):
                grp.append(k)
                dly.append(j * P / s["J"])
    for _ in range(s["n_ref"]):
        grp.append(-1)
        dly.append(0.0)
    n = len(grp)
    ncol = int(np.ceil(np.sqrt(n)))
    xs, ys = np.meshgrid(np.arange(ncol), np.arange(int(np.ceil(n / ncol))))
    pos = np.c_[xs.ravel(), ys.ravel()][:n].astype(float) * s["spacing"]
    pos -= pos.mean(0)
    perm = np.random.default_rng(7).permutation(n)       # interleave groups spatially
    pos = pos[perm]
    return np.array(grp), np.array(dly), pos[:, 0], pos[:, 1]


def waveform_sin(t, P, d, h2=0.0, h3=0.0):
    x = 2 * np.pi * (t - d) / P
    return 0.5 * (1 + np.cos(x) + h2 * np.cos(2 * x + 0.7) + h3 * np.cos(3 * x + 1.9)) / (1 + h2 + h3)


def invert_tau(Vc, P):
    """Solve sinc(pi*tau/P) = Vc for tau in (0, P) by bisection."""
    lo, hi = np.zeros_like(Vc), np.full_like(Vc, P * 0.999)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        x = np.pi * mid / P
        f = np.sin(x) / x - Vc
        lo = np.where(f > 0, mid, lo)
        hi = np.where(f > 0, hi, mid)
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------
# Main ladder simulation (sinusoidal phase-stepped groups)
# --------------------------------------------------------------------------
def simulate_ladder(scn, n_trials=4000, chunk=400):
    s = derive(scn)
    grp, dly, x, y = build_layout(s)
    nh = len(grp)
    u, w = window_weights(s["tau"], s["sig_lsf_t"])
    psi = np.radians(s["heading_deg"])
    s_along = x * np.cos(psi) + y * np.sin(psi)            # true along-track offsets
    if s["precomp"]:
        # scheduler predicts heading (0.1 deg) and ground speed (0.1 %) from TLE/ephemeris and
        # advances each head's drive delay so the *effective* phase steps seen by the imager are
        # uniform; the delays actually applied are logged (monitor photodiodes) and used below.
        rp = np.random.default_rng(11)
        psi_p = psi + rp.normal(0, np.radians(0.1))
        s_pred = x * np.cos(psi_p) + y * np.sin(psi_p)
        Ps = np.array([s["periods"][g] if g >= 0 else 1.0 for g in grp])
        dly = (dly + s_pred / (s["v_g"] * (1 + rp.normal(0, 1e-3)))) % Ps
    out = dict(err=[], tau_est=[], tau_est_nocorr=[], tau_est_self=[], decomp_pitch_err=[])
    for c0 in range(0, n_trials, chunk):
        n = min(chunk, n_trials - c0)
        # ---------------- truth ----------------
        t_c = 1000.0 + RNG.uniform(0, 8.192, n)              # true GNSS mid-exposure (origin)
        dt_true = s_along / (s["v_g"])                         # (nh,)
        t_gn = RNG.normal(0, s["t_gnss_common"], n)[:, None]
        t_hd = RNG.normal(0, s["t_head_jit"], (n, nh))
        t_emit_centre = (t_c[:, None] + dt_true[None, :] - s["R"] / C) + t_gn + t_hd
        amp = 1 + RNG.normal(0, s["amp_spread"], nh)          # fixed per site
        E = np.empty((n, nh))
        for i in range(nh):
            tt = t_emit_centre[:, i][:, None] + u[None, :]
            if grp[i] < 0:
                m = np.ones_like(tt)
            else:
                m = waveform_sin(tt, s["periods"][grp[i]], dly[i], s["h2"], s["h3"])
            E[:, i] = (m * w[None, :]).sum(1)
        S = s["S_peak"] * amp[None, :] * E
        if s["sig_I"] > 0:
            sl = np.sqrt(np.log(1 + s["sig_I"] ** 2))
            S = S * np.exp(RNG.normal(-sl ** 2 / 2, sl, (n, nh)))
        S = S * (1 + RNG.normal(0, s["phot_err"], (n, nh))) * (1 + RNG.normal(0, s["prnu"], (n, nh)))
        S = S * (1 - s["nonlin"] * S / s["S_peak"])
        meas = RNG.poisson(np.maximum(S + s["bg"], 0)) - s["bg"] + RNG.normal(0, np.sqrt(s["rn2"]), (n, nh))
        # ---------------- processing ----------------
        amp_est = amp * (1 + RNG.normal(0, s["amp_known"], nh))
        # survey + heading + velocity knowledge
        xe = x[None, :] + RNG.normal(0, s["survey_sig"], (n, nh))
        ye = y[None, :] + RNG.normal(0, s["survey_sig"], (n, nh))
        psie = psi + RNG.normal(0, s["yaw_err"], (n, 1))
        vge = s["v_g"] * (1 + RNG.normal(0, s["vg_rel_err"], (n, 1)))
        dt_est = (xe * np.cos(psie) + ye * np.sin(psie)) / vge
        if not s["layout_correction"]:
            dt_est = np.zeros_like(dt_est)
        R_est = s["R"] + RNG.normal(0, s["range_err"], (n, 1))
        refm = (meas[:, grp < 0] / amp_est[grp < 0]).mean(1, keepdims=True)
        r = meas / amp_est[None, :] / refm                     # reference-normalised ratios
        # a-priori time from onboard tag (bias + big uncertainty)
        t_prior = t_c + s["tag_err_true"] + RNG.uniform(-1.0, 1.0, n) * s["prior_sig"] * 2
        t_est = t_prior.copy()
        tau_fine = tau_nc = tau_self = None
        for k in range(len(s["periods"]) - 1, -1, -1):
            P = s["periods"][k]
            sel = grp == k
            th = 2 * np.pi * (dly[sel][None, :] - dt_est[:, sel]) / P      # (n, J*)
            rr = r[:, sel]
            # per-trial linear LSQ: rr = A + X cos th + Y sin th
            G = np.stack([np.ones_like(th), np.cos(th), np.sin(th)], -1)    # (n, m, 3)
            GtG = np.einsum("nmi,nmj->nij", G, G)
            Gtr = np.einsum("nmi,nm->ni", G, rr)
            A_, X_, Y_ = np.linalg.solve(GtG, Gtr[..., None])[..., 0].T
            phi = np.arctan2(Y_, X_)
            t_mod = phi / (2 * np.pi) * P                      # emission-time centre mod P
            t_ref = t_est - R_est[:, 0] / C                    # current best estimate (emit time)
            nwrap = np.round((t_ref - t_mod) / P)
            t_e = t_mod + nwrap * P
            t_est = t_e + R_est[:, 0] / C
            if k == 0:
                amp_ = np.hypot(X_, Y_)
                V_ref = amp_ / 0.5                              # reference-normalised visibility
                V_self = amp_ / A_                              # self-referenced (set mean)
                mtf_true = np.exp(-2 * np.pi ** 2 * s["sig_lsf_t"] ** 2 / P ** 2)
                sig_lsf_est = s["sig_lsf_t"] * (1 + RNG.normal(0, s["lsf_knowledge"], n))
                mtf_est = np.exp(-2 * np.pi ** 2 * sig_lsf_est ** 2 / P ** 2)
                h_att = 1.0  # harmonic normalisation already in waveform
                tau_fine = invert_tau(np.clip(V_ref / mtf_est, 1e-3, 0.9999), P)
                tau_nc = invert_tau(np.clip(V_ref, 1e-3, 0.9999), P)
                tau_self = invert_tau(np.clip(V_self / mtf_est, 1e-3, 0.9999), P)
        out["err"].append(t_est - t_c)
        out["tau_est"].append(tau_fine)
        out["tau_est_nocorr"].append(tau_nc)
        out["tau_est_self"].append(tau_self)
    for kk in list(out):
        if out[kk]:
            out[kk] = np.concatenate(out[kk]) if out[kk][0] is not None else None
    out["s"] = s
    out["nh"] = nh
    return out


def robust_stats(e, fail_thr=50e-6):
    ok = np.abs(e) < fail_thr
    eo = e[ok]
    return dict(rms=np.sqrt(np.mean(eo ** 2)), bias=np.mean(eo), p95=np.percentile(np.abs(eo), 95),
                fail=1 - ok.mean())


# --------------------------------------------------------------------------
# Waveform-family comparison (fine timing, locally unwrapped)
# --------------------------------------------------------------------------
def mseq(n=15):
    reg = [1, 0, 0, 0]
    out = []
    for _ in range(n):
        out.append(reg[-1])
        fb = reg[-1] ^ reg[0]          # x^4 + x + 1
        reg = [fb] + reg[:-1]
    return np.array(out, float)


PN = mseq(15)


def wf_family(name, t, d):
    if name == "sinusoid":
        return waveform_sin(t, 2e-3, d)
    if name == "pn":           # 15-chip m-sequence, chip 0.4 ms, period 6 ms
        Tc = 0.4e-3
        idx = np.floor(((t - d) / Tc)) % 15
        return PN[idx.astype(int)]
    if name == "chirp":        # linear chirp 250->750 Hz over 20 ms, repeating
        Tp = 20e-3
        tl = (t - d) % Tp
        f0, f1 = 250.0, 750.0
        ph = 2 * np.pi * (f0 * tl + 0.5 * (f1 - f0) / Tp * tl ** 2)
        return 0.5 * (1 + np.cos(ph))
    if name == "edge":         # on/off square wave, period 2 ms, 50 % duty
        return (((t - d) % 2e-3) < 1e-3).astype(float)
    raise ValueError(name)


FAMILY_DELAYS = {
    "sinusoid": [0, 0.5e-3, 1.0e-3, 1.5e-3],
    "pn": [0, 1.6e-3, 3.2e-3, 4.4e-3],
    "chirp": [0, 5e-3, 10e-3, 15e-3],
    "edge": [0, 0.5e-3, 1.0e-3, 1.5e-3],
}


def simulate_family(name, scn, n_trials=1500, search=0.4e-3):
    s = derive(scn)
    u, w = window_weights(s["tau"], s["sig_lsf_t"])
    M = s["M_fine"]
    delays = np.tile(FAMILY_DELAYS[name], M)
    nh = len(delays)
    rng_pos = np.random.default_rng(3)
    s_along = rng_pos.uniform(-10, 10, nh)                    # m
    dt_true = s_along / s["v_g"]
    # model grid F_i(tc) on fine grid
    tg = np.arange(-search - 2e-3, search + 2e-3, 0.25e-6)
    def integ(i, centres):
        tt = centres[:, None] + u[None, :]
        return (wf_family(name, tt, delays[i]) * w[None, :]).sum(1)
    T0 = 0.0137  # arbitrary epoch inside code period
    errs = []
    sl = np.sqrt(np.log(1 + s["sig_I"] ** 2)) if s["sig_I"] > 0 else 0.0
    # precompute model tables per head at shifted grid
    tables = [integ(i, T0 + tg + dt_true[i]) for i in range(nh)]   # processor knows layout
    for _ in range(n_trials):
        dtc = RNG.uniform(-search, search)
        E = np.array([integ(i, np.array([T0 + dtc + dt_true[i]]))[0] for i in range(nh)])
        Sig = s["S_peak"] * E
        if sl > 0:
            Sig = Sig * np.exp(RNG.normal(-sl ** 2 / 2, sl, nh))
        Sig = Sig * (1 + RNG.normal(0, s["phot_err"], nh))
        meas = RNG.poisson(Sig + s["bg"]) - s["bg"] + RNG.normal(0, np.sqrt(s["rn2"]), nh)
        # grid search over tc with free common scale (self-referenced), residual chi2
        cand = np.arange(-search, search, 1e-6)
        idx = np.searchsorted(tg, cand)
        Mdl = np.stack([np.interp(cand, tg, tables[i]) for i in range(nh)], 1)   # (nc, nh)
        var = np.maximum(meas, 1) + s["bg"] + s["rn2"] + (sl * np.maximum(meas, 1)) ** 2
        wts = 1 / var
        a = (Mdl * meas * wts).sum(1) / (Mdl ** 2 * wts).sum(1)
        chi = (((meas - a[:, None] * Mdl) ** 2) * wts).sum(1)
        j = np.argmin(chi)
        if 0 < j < len(cand) - 1:   # parabolic refinement
            y0, y1, y2 = chi[j - 1], chi[j], chi[j + 1]
            den = y0 - 2 * y1 + y2
            off = 0.5 * (y0 - y2) / den if den > 0 else 0.0
        else:
            off = 0.0
        est = cand[j] + off * 1e-6
        errs.append(est - dtc)
    e = np.array(errs)
    return robust_stats(e, 100e-6)


# --------------------------------------------------------------------------
# TDI stage-count verification
# --------------------------------------------------------------------------
def tdi_stage_test(res):
    s = res["s"]
    out = {}
    for key in ["tau_est", "tau_est_nocorr", "tau_est_self"]:
        te = res[key]
        N_est = te / s["T_L"]
        out[key] = dict(bias_us=1e6 * (te.mean() - s["tau"]), sig_us=1e6 * te.std(),
                        sig_stage=te.std() / s["T_L"],
                        correct=(np.nan if s["framing"] else np.mean(np.round(N_est) == s["n_tdi"])))
    return out


# --------------------------------------------------------------------------
# Time-vs-pitch decomposition (single pass)
# --------------------------------------------------------------------------
def decomposition(res, n_heads, true_dt=350e-6, true_dth=4e-6, eph_sig=0.05,
                  cent_px=0.05, jitter_urad=0.0, n_trials=4000):
    s = res["s"]
    e_t = RNG.choice(res["err"], n_trials)
    y_obs = s["v_g"] * true_dt + s["H"] * true_dth + RNG.normal(0, eph_sig, n_trials) \
        + RNG.normal(0, cent_px * s["gsd"] / np.sqrt(n_heads), n_trials) \
        + RNG.normal(0, 0.02 / np.sqrt(n_heads), n_trials) \
        + s["H"] * RNG.normal(0, jitter_urad * 1e-6, n_trials)
    # the line-tag interpolation (centroid of origin, averaged over heads) adds to dt error
    tag_interp = RNG.normal(0, cent_px * s["T_L"] / np.sqrt(n_heads), n_trials)
    dt_est = true_dt + e_t + tag_interp
    dth_est = (y_obs - s["v_g"] * dt_est) / s["H"]
    return dict(dt_rms_us=1e6 * np.std(dt_est - true_dt), dth_rms_urad=1e6 * np.std(dth_est - true_dth),
                dt_mean_us=1e6 * dt_est.mean(), dth_mean_urad=1e6 * dth_est.mean())


# --------------------------------------------------------------------------
# Design-around: multi-pitch GCP collects
# --------------------------------------------------------------------------
def multipitch_gcp(n_collects, pitches_deg=(-30, 0, 30), sig_y=1.0, drift_urad=1.0,
                   H=500e3, v_g=7060.0, true_dt=350e-6, true_dth=4e-6, n_trials=4000):
    p = np.radians(np.resize(np.array(pitches_deg, float), n_collects))
    errs = []
    for _ in range(n_trials):
        dth_k = true_dth + RNG.normal(0, drift_urad * 1e-6, n_collects)   # alignment drifts between collects
        y = v_g * true_dt + H * dth_k / np.cos(p) ** 2 + RNG.normal(0, sig_y, n_collects)
        G = np.c_[np.full(n_collects, v_g), H / np.cos(p) ** 2]
        sol, *_ = np.linalg.lstsq(G, y, rcond=None)
        errs.append(sol - [true_dt, true_dth])
    e = np.array(errs)
    return 1e6 * e[:, 0].std(), 1e6 * e[:, 1].std()


# --------------------------------------------------------------------------
# Run everything
# --------------------------------------------------------------------------
def fmt(x):
    return f"{x:8.2f}"


def main():
    print("=" * 78)
    print("Chronometric beacon Monte-Carlo  (numpy", np.__version__, ")")
    print("HV5/7: int Cn2 h^2 dh = %.3e,  r0(500nm) = %.1f cm" %
          (I_H2, 100 * (0.423 * (2 * np.pi / 0.5e-6) ** 2 * I_H0) ** (-3 / 5)))
    print("sigma_I (850 nm, zenith) vs emitting aperture:")
    for D in [0.02, 0.05, 0.1, 0.25, 0.5, 1.0]:
        print(f"   D_src = {D:5.2f} m : sigma_I = {sigma_scint(D):.3f}   (30 deg: {sigma_scint(D, zen_deg=30):.3f})")
    s0 = derive(BASE)
    print(f"T_L = {s0['T_L']*1e6:.1f} us, tau = {s0['tau']*1e6:.1f} us, S_peak = {s0['S_peak']:.0f} e-,"
          f" LSF sigma_t = {s0['sig_lsf_t']*1e6:.1f} us")

    systematics = dict(survey_sig=0.02, vg_rel_err=1e-3, yaw_err=1e-3, t_gnss_common=30e-9,
                       t_head_jit=50e-9, h2=0.005, h3=0.002, phot_err=0.003, prnu=0.002,
                       nonlin=0.001, amp_known=0.001, range_err=1.0)
    scen = [
        ("S0 photon-only, day, J=4, 1 ref (inventor model)", dict()),
        ("S0b S0 without drive-phase pre-compensation", dict(precomp=False)),
        ("S1 + all systematics, no scintillation", dict(**systematics)),
        ("S2 + scint, compact emitter D_src=5 cm", dict(**systematics, D_src=0.05)),
        ("S3 + scint, diffuse panel D_src=0.5 m", dict(**systematics, D_src=0.5)),
        ("S4 MITIGATED: D_src=1.0 m, M=3 fine copies, 3 refs", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3)),
        ("S5 S4 at night (no background)", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3, bg_px=0.0)),
        ("S4b S4 without drive-phase pre-compensation", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3, precomp=False)),
        ("S6 S4 but NO layout correction", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3, layout_correction=False)),
        ("S7 S4 at 30 deg off-nadir (pre-aimed heads)", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3, zen=30.0)),
        ("S8 S4 but 16-stage TDI (tau=1.7 ms), P1=4 ms", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3, n_tdi=16,
                                                           periods=(4e-3, 64e-3, 1.024, 16.384))),
        ("S9 cubesat framing D_ap=9 cm, GSD 3.7 m, tau=1 ms", dict(**systematics, D_src=1.0, M_fine=3, n_ref=3,
                                                              D_ap=0.09, gsd=3.7, framing=True, tau_frame=1e-3,
                                                              bg_px=490.0, read_e=10.0, spacing=12.0)),
        ("S9b S9 with x8 ladder (5 groups) + M=4 fine copies", dict(**systematics, D_src=1.0, M_fine=4, n_ref=3,
                                                              D_ap=0.09, gsd=3.7, framing=True, tau_frame=1e-3,
                                                              bg_px=490.0, read_e=10.0, spacing=12.0,
                                                              periods=(2e-3, 16e-3, 0.128, 1.024, 8.192))),
    ]
    results = {}
    print("\n--- Absolute mid-exposure time recovery (single band, single pass) ---")
    print(f"{'scenario':55s} {'heads':>5s} {'S_pk e-':>8s} {'sigI':>6s} {'rms us':>8s} {'bias us':>8s} {'p95 us':>8s} {'unwrapFail':>10s}")
    for name, over in scen:
        sc = dict(BASE, **over)
        res = simulate_ladder(sc, n_trials=3000)
        st = robust_stats(res["err"])
        results[name] = (res, st)
        print(f"{name:55s} {res['nh']:5d} {res['s']['S_peak']:8.0f} {res['s']['sig_I']:6.3f} "
              f"{st['rms']*1e6:8.2f} {st['bias']*1e6:8.2f} {st['p95']*1e6:8.2f} {st['fail']*100:9.2f}%")

    print("\n--- TDI stage-count / exposure verification (P1 visibility) ---")
    for name in [scen[2][0], scen[4][0], scen[5][0], scen[6][0], scen[11][0]]:
        t = tdi_stage_test(results[name][0])
        print(name)
        for k, lab in [("tau_est", "ref-normalised + LSF(temporal-MTF) corr"),
                       ("tau_est_nocorr", "ref-normalised, NO LSF correction   "),
                       ("tau_est_self", "self-referenced + LSF corr          ")]:
            v = t[k]
            print(f"   {lab}: bias {v['bias_us']:7.1f} us, sigma {v['sig_us']:6.1f} us "
                  f"({v['sig_stage']:.2f} stage), correct N: {v['correct']*100:5.1f}%")

    print("\n--- Waveform families (fine timing, 4 phase steps x M=3, locally unwrapped) ---")
    for cond, over in [("photon+phot 0.3% (no scint)", dict(phot_err=0.003, M_fine=3)),
                       ("+ scint D_src=1.0 m", dict(phot_err=0.003, M_fine=3, D_src=1.0))]:
        for fam in ["sinusoid", "pn", "chirp", "edge"]:
            st = simulate_family(fam, dict(BASE, **over), n_trials=1200)
            print(f"   {cond:28s} {fam:9s}: rms {st['rms']*1e6:6.2f} us, bias {st['bias']*1e6:6.2f} us,"
                  f" outliers {st['fail']*100:.2f}%")

    print("\n--- Single-pass time vs pitch decomposition (truth dt=350 us, dtheta=4 urad) ---")
    for name in [scen[2][0], scen[5][0]]:
        res, _ = results[name]
        d = decomposition(res, res["nh"])
        dj = decomposition(res, res["nh"], jitter_urad=0.5)
        print(f"   {name}")
        print(f"      dt = {d['dt_mean_us']:.1f} +/- {d['dt_rms_us']:.2f} us ; "
              f"dtheta = {d['dth_mean_urad']:.3f} +/- {d['dth_rms_urad']:.3f} urad "
              f"(with 0.5 urad instantaneous jitter: +/- {dj['dth_rms_urad']:.3f} urad)")

    print("\n--- Design-around: multi-pitch GCP collects (pitch -30/0/+30 deg) ---")
    for sig_y in [0.5, 1.0, 2.0]:
        for n in [3, 6, 12, 30]:
            sdt, sdth = multipitch_gcp(n, sig_y=sig_y)
            print(f"   sigma_y={sig_y:.1f} m/collect, {n:3d} collects: sigma_dt = {sdt:7.1f} us, sigma_dtheta = {sdth:5.2f} urad")
    for sig_y in [1.0]:
        sdt, _ = multipitch_gcp(3, sig_y=sig_y, drift_urad=0.0)
        print(f"   (no alignment drift, sigma_y=1 m, 3 collects: sigma_dt = {sdt:.1f} us)")


if __name__ == "__main__":
    main()
