#!/usr/bin/env python3
"""
cc_tdi_sim.py -- Monte-Carlo simulation of Complementary-Coded TDI (CC-TDI) jitter sensing.

What is simulated (all in the digital-TDI-CMOS embodiment, N = 64 stages, 14.12 kHz line rate):
  * A textured, optics-blurred, band-limited scene on a 2x oversampled grid (three texture classes:
    "urban", "agri", "low"), sampled by each TDI stage at its jittered position with a 16-tap Keys
    cubic interpolator (i.e. the non-linear imaging model, not the linearised one).
  * Line-of-sight jitter: 4 reaction wheels (fundamental + harmonics + bearing tones), a cryocooler
    (49 Hz drive + 20 harmonics; 9th and 18th harmonics deliberately coincide with the split-half
    code nulls at 441.25 Hz and 882.5 Hz), three structural resonances, broadband floor, and a
    large low-frequency attitude wobble. A separate "comb probe" scenario puts equal-amplitude tones
    on 64 log-spaced frequencies + every split-half null up to 3 kHz.
  * Per-pixel gain non-uniformity (0.5 % row + 1.0 % pixel, raw) and a calibrated pipeline with a
    0.1 % residual; Gaussian-approximated shot noise, 3 e- read noise per stage sample.
  * Four stage-code layouts accumulated from the same photo-samples:
       split : contiguous two-block split (+1 x32, -1 x32) on all 1024 sensing columns (e2v-style)
       rand1 : one optimised balanced pseudo-random code on all columns
       multi4: four optimised balanced codes interleaved over column groups (c mod 4)  <- invention
       seg8  : 8 contiguous segments of 8 stages, zero-sum +/-1 segment coefficients, 4 patterns
               interleaved (charge-domain-compatible "K>=3 partial sums" variant)
  * Estimator: per-line, per-code-group gradient-weighted least squares (gradients from the noisy
    science image S itself), then a sliding-window deconvolution to one displacement sample per
    line period, solved as a Tikhonov-regularised weighted LS by conjugate gradients with FFT
    operators (equivalent to the fixed-lag Kalman/Wiener smoother at steady state).
  * Image-quality part: per-line intra-window OTF computed from the true and estimated trajectories
    for (none | integer-address | bilinear fractional | Lanczos-3 fractional accumulation) using a
    causal harmonic predictor, and post-hoc per-line Wiener restoration from the smoothed estimate;
    restored MTF and noise gain reported at Nyquist.

Usage:  python3 cc_tdi_sim.py [--quick]      (full run ~5-8 min on 4 cores; prints a results report)
"""
import sys, time, json
import numpy as np

# ----------------------------------------------------------------------------- parameters
N = 64                     # TDI stages
FL = 14120.0               # line rate [Hz]
DT = 1.0 / FL
L = 4096                   # lines per record (0.29 s); jitter synthesised periodic in L
C_SENS = 1024              # sensing columns
GUARD = 2
C_TOT = C_SENS + 2 * GUARD
SBAR = 200.0               # mean e- per stage per pixel (judges: 150-290)
SIG_R = 3.0                # read noise e- per stage sample (digital TDI CMOS)
ROW_PRNU, PIX_PRNU, CAL_RES = 0.005, 0.010, 0.001
QUICK = "--quick" in sys.argv

# ----------------------------------------------------------------------------- code design
def sign_changes(w):
    return int(np.sum(np.sign(w[1:]) != np.sign(w[:-1])))

def design_codes(rng):
    f = np.r_[np.linspace(20, 300, 60), np.linspace(300, FL / 2, 500)]
    E = np.exp(-2j * np.pi * np.outer(f, np.arange(N)) * DT)
    split = np.r_[np.ones(32), -np.ones(32)]
    cands = []
    for _ in range(6000):
        w = split.copy(); rng.shuffle(w); cands.append(w)
    for k in range(2, 14):                      # high-first-moment candidates (good low-f)
        for _ in range(1000):
            w = split.copy()
            w[rng.choice(32, k, replace=False)] = -1
            w[32 + rng.choice(32, k, replace=False)] = 1
            cands.append(w)
    Cc = np.array([c for c in cands if sign_changes(c) >= 4])
    P = np.abs(Cc @ E.T) ** 2
    best_single = int(np.argmax(P.min(1)))
    best = None
    for _ in range(8):
        sel = list(rng.choice(len(Cc), 4, replace=False)); acc = P[sel].sum(0)
        for _ in range(5):
            for m in range(4):
                rest = acc - P[sel[m]]
                j = int(np.argmax(np.min((rest + P) / 4, axis=1)))
                acc = rest + P[j]; sel[m] = j
        v = np.sqrt(np.min(acc / 4))
        if best is None or v > best[0]:
            best = (v, sel.copy())
    multi = Cc[best[1]]
    # segmented (8 x 8 stages) zero-sum coefficient patterns, 4 interleaved, band 20-1600 Hz
    import itertools
    pats = []
    for pos in itertools.combinations(range(8), 4):
        c = -np.ones(8); c[list(pos)] = 1; pats.append(np.repeat(c, 8))
    pats = np.array([p for p in pats if sign_changes(p) >= 4])
    fs = np.linspace(20, 1600, 400)
    Es = np.exp(-2j * np.pi * np.outer(fs, np.arange(N)) * DT)
    Ps = np.abs(pats @ Es.T) ** 2
    bests = None
    for combo in itertools.combinations(range(len(pats)), 4):
        v = np.min(Ps[list(combo)].mean(0))
        if bests is None or v > bests[0]:
            bests = (v, combo)
    seg = pats[list(bests[1])]
    return dict(split=split[None, :], rand1=Cc[best_single][None, :], multi4=multi, seg8=seg)

def code_spectrum_table(codes, freqs):
    E = np.exp(-2j * np.pi * np.outer(freqs, np.arange(N)) * DT)
    out = {}
    for k, W in codes.items():
        out[k] = np.sqrt((np.abs(W @ E.T) ** 2).mean(0))   # effective |W| (rms over interleaved codes)
    return out

# ----------------------------------------------------------------------------- scene
def diffraction_mtf(nu, nu_c):
    x = np.clip(nu / nu_c, 0, 1)
    return (2 / np.pi) * (np.arccos(x) - x * np.sqrt(1 - x * x))

def make_scene(rows, cols, cls, rng):
    """Scene on a 2x oversampled grid (rows*2, cols*2); units e-/stage. Returns fine grid."""
    R, Cn = 2 * rows, 2 * cols
    fy = np.fft.fftfreq(R, d=0.5)[:, None]; fx = np.fft.rfftfreq(Cn, d=0.5)[None, :]   # cy / native px
    rho = np.sqrt(fx ** 2 + fy ** 2)
    def fractal(beta, f0=0.01):
        ph = rng.standard_normal((R, Cn))
        F = np.fft.rfft2(ph) / (rho + f0) ** beta
        x = np.fft.irfft2(F, s=(R, Cn)); return (x - x.mean()) / x.std()
    def parcels(smin, smax, spread):
        # rectangular parcels (fields / blocks) with sharp edges
        def cuts(n):
            b = [0]
            while b[-1] < n:
                b.append(b[-1] + int(rng.uniform(smin, smax) * 2))
            return np.array(b)
        rb, cb = cuts(R), cuts(Cn)
        lev = rng.standard_normal((len(rb), len(cb))) * spread
        ri = np.searchsorted(rb, np.arange(R), side="right") - 1
        ci = np.searchsorted(cb, np.arange(Cn), side="right") - 1
        # offset every other band to avoid a pure checkerboard
        return lev[ri][:, ci]
    if cls == "urban":
        s = 0.22 * fractal(1.0) + parcels(8, 40, 0.25) + 0.10 * parcels(3, 12, 1.0)
        # roads: bright lines
        for _ in range(int(Cn / 60)):
            c0 = rng.integers(0, Cn - 8); s[:, c0:c0 + int(rng.integers(4, 12))] += 0.35
        for _ in range(int(R / 60)):
            r0 = rng.integers(0, R - 8); s[r0:r0 + int(rng.integers(4, 12)), :] += 0.35
    elif cls == "agri":
        s = parcels(60, 300, 0.18) + 0.14 * fractal(0.8) + 0.03 * fractal(0.6)
    elif cls == "low":
        s = 0.05 * fractal(0.8) + 0.01 * fractal(0.5)
    else:
        raise ValueError(cls)
    s = SBAR * np.clip(1 + s, 0.08, None)
    # optics (f/11, 0.6 um, 5.5 um pixel -> cutoff 0.833 cy/px), pixel aperture, TDI step smear (along-track)
    fyf = np.fft.fftfreq(R, d=0.5)[:, None]; fxf = np.fft.rfftfreq(Cn, d=0.5)[None, :]
    H = diffraction_mtf(np.sqrt(fxf ** 2 + fyf ** 2), 0.833) * np.sinc(fxf) * np.sinc(fyf) * np.sinc(fyf)
    s = np.fft.irfft2(np.fft.rfft2(s) * H, s=(R, Cn))
    return s.astype(np.float64)

def gradient_stats(fine):
    nat = fine[::2, ::2]
    gy = (nat[2:, 1:-1] - nat[:-2, 1:-1]) / 2; gx = (nat[1:-1, 2:] - nat[1:-1, :-2]) / 2
    g = np.sqrt(gx ** 2 + gy ** 2) / nat.mean()
    return float(np.median(g)), float(np.sqrt(np.mean(gx ** 2 + gy ** 2)) / nat.mean())

# ----------------------------------------------------------------------------- jitter
def bin_of(f):
    return int(round(f * L / FL))

def synth_tones(tones, rng):
    """tones: list of (freq, amp_px, axis_weights(2,)) -> periodic (L,2) signal on exact bins."""
    d = np.zeros((L, 2))
    n = np.arange(L)
    for f, a, ax in tones:
        k = bin_of(f)
        if k <= 0 or k >= L // 2:
            continue
        ph = rng.uniform(0, 2 * np.pi, 2)
        for j in range(2):
            d[:, j] += a * ax[j] * np.cos(2 * np.pi * k * n / L + ph[j])
    return d

def make_jitter(kind, rng):
    tones = []
    freqs_known = []           # frequencies known to the spacecraft (wheel tach, cryo drive)
    if kind == "realistic":
        wheel_f = [36.7, 48.2, 57.9, 63.3]
        harm = [(1, 1.0), (2, 0.45), (3, 0.25), (4.63, 0.3), (5.31, 0.2), (8.12, 0.15)]
        for wf in wheel_f:
            dirv = rng.standard_normal(2); dirv /= np.linalg.norm(dirv)
            for h, a in harm:
                f = wf * h
                amp = 0.05 * a * (1 + 2.5 / (1 + ((f - 380) / 25) ** 2) + 1.5 / (1 + ((f - 120) / 10) ** 2))
                tones.append((f, amp, np.abs(dirv) + 0.2)); freqs_known.append(f)
        # cryocooler 49.0 Hz drive, 20 harmonics; 9th -> 441 Hz, 18th -> 882 Hz (split-half nulls)
        for h in range(1, 21):
            amp = 0.06 / h ** 0.6
            if h in (9, 18):
                amp = 0.07
            tones.append((49.0 * h, amp, np.array([0.8, 1.0]))); freqs_known.append(49.0 * h)
        d = synth_tones(tones, rng)
        # broadband structural response: resonances at 120, 380, 1150 Hz + 1/f floor, 20 Hz-3 kHz
        fk = np.fft.rfftfreq(L, DT)
        for j in range(2):
            spec = np.zeros_like(fk)
            band = (fk >= 20) & (fk <= 3000)
            spec[band] = 1 / fk[band]
            for f0, Q, g in [(120, 15, 3.0), (380, 25, 4.0), (1150, 30, 2.0)]:
                spec += g / fk.clip(1) * 1 / (1 + (Q * (fk / f0 - f0 / fk.clip(1))) ** 2)
            X = np.sqrt(spec) * (rng.standard_normal(len(fk)) + 1j * rng.standard_normal(len(fk)))
            X[0] = 0
            x = np.fft.irfft(X, n=L); x = x / x.std() * 0.12
            d[:, j] += x
        # scale >20 Hz content to 0.30 px (along-track, y=axis 1) and 0.25 px (cross-track, x=axis 0)
        for j, target in [(0, 0.25), (1, 0.30)]:
            d[:, j] *= target / band_rms(d[:, j], 20, FL / 2)
        # large low-frequency attitude motion (unobservable by design; comes from gyro/ST fusion)
        n = np.arange(L)
        d[:, 0] += 0.6 * np.cos(2 * np.pi * bin_of(1.7) * n / L + 0.3)
        d[:, 1] += 0.5 * np.cos(2 * np.pi * bin_of(5.2) * n / L + 1.1)
    elif kind == "tonal-large":
        # realistic + a strongly imbalanced wheel (57.9 Hz, 1.0 px along) and a large cryocooler line (49 Hz, 0.6 px cross)
        d, freqs_known = make_jitter("realistic", rng)
        n = np.arange(L)
        d[:, 1] += 1.0 * np.cos(2 * np.pi * bin_of(57.9) * n / L + 0.4)
        d[:, 0] += 0.6 * np.cos(2 * np.pi * bin_of(49.0) * n / L + 2.0)
    elif kind == "zero":
        d = np.zeros((L, 2))
    elif kind == "comb":
        fs = list(np.geomspace(25, 5000, 64))
        nulls = [FL / 32 * m for m in range(1, 7)]      # 441.25 ... 2647.5 Hz (split-half nulls)
        allf = sorted(set([bin_of(f) for f in fs] + [bin_of(f) for f in nulls]))
        tones = [(k * FL / L, 0.025, np.array([1.0, 1.0])) for k in allf]
        d = synth_tones(tones, rng)
        freqs_known = [k * FL / L for k in allf]
    else:
        raise ValueError(kind)
    return d, freqs_known

def band_mask(f1, f2):
    fk = np.fft.rfftfreq(L, DT)
    return (fk >= f1) & (fk <= f2)

def band_rms(x, f1, f2):
    X = np.fft.rfft(x); m = band_mask(f1, f2)
    return float(np.sqrt(2 * np.sum(np.abs(X[m]) ** 2)) / L)

def band_filter(x, f1, f2):
    X = np.fft.rfft(x, axis=0); m = band_mask(f1, f2)
    X[~m] = 0
    return np.fft.irfft(X, n=L, axis=0)

# ----------------------------------------------------------------------------- TDI imaging + accumulation
def keys(t):
    a = -0.5
    x = np.array([1 + t, t, 1 - t, 2 - t])
    w = np.where(x <= 1, (a + 2) * x ** 3 - (a + 3) * x ** 2 + 1,
                 a * x ** 3 - 5 * a * x ** 2 + 8 * a * x - 4 * a)
    return w

def run_tdi(fine, d, codes, rng, noise=True):
    """Simulate stage samples frame-by-frame and accumulate S and coded sums for every layout.
    d: (L,2) periodic jitter [x (cross-track), y (along-track)] in native px.
    Returns dict pipeline -> {'S': (L,C_TOT), layout: D (L,C_TOT)}."""
    yoff, xoff = N + 16, 4
    gains_raw = 1 + ROW_PRNU * rng.standard_normal((N, 1)) + PIX_PRNU * rng.standard_normal((N, C_TOT))
    gains_hat = gains_raw - CAL_RES * rng.standard_normal((N, C_TOT))     # calibration estimate
    eq = 1.0 / gains_hat
    # weight matrices per layout, (N, C_TOT)
    Wl = {}
    for name, W in codes.items():
        M = W.shape[0]
        Wl[name] = W[np.arange(C_TOT) % M].T.copy()
    pipes = ("eq", "raw")
    acc = {p: {"S": np.zeros((L + 2 * N, C_TOT)), **{k: np.zeros((L + 2 * N, C_TOT)) for k in Wl}} for p in pipes}
    cols_fine = 2 * (np.arange(C_TOT) + xoff)
    for n in range(L + N - 1):
        dx, dy = d[n % L]
        # fine-grid coordinates
        Y0 = 2 * (n + yoff) + 2 * dy; X0 = 2 * xoff + 2 * dx
        fy0 = int(np.floor(Y0)); ty = Y0 - fy0
        fx0 = int(np.floor(X0)); tx = X0 - fx0
        wy = keys(ty); wx = keys(tx)
        # rows for stages i = 0..N-1 are fy0 - 2i (+a-1)
        tmp = 0.0
        for a in range(4):
            start = fy0 + a - 1
            rows = fine[start - 2 * (N - 1): start + 1: 2][::-1]          # (N, cols_fine_total), i ascending
            tmp = tmp + wy[a] * rows
        frame = 0.0
        for b in range(4):
            frame = frame + wx[b] * tmp[:, fx0 + b - 1: fx0 + b - 1 + 2 * C_TOT: 2]
        lam = np.clip(frame, 0, None)
        e_raw = gains_raw * lam
        if noise:
            e_raw = e_raw + np.sqrt(e_raw + SIG_R ** 2) * rng.standard_normal(e_raw.shape)
        samples = {"raw": e_raw, "eq": e_raw * eq}
        r0 = n - (N - 1) + N; r1 = n + 1 + N            # rows for k = n-63 .. n  (i = 63 .. 0)
        for p in pipes:
            smp = samples[p][::-1]                        # i = 63..0 to match ascending k
            acc[p]["S"][r0:r1] += smp
            for name, W in Wl.items():
                acc[p][name][r0:r1] += W[::-1] * smp
    out = {}
    for p in pipes:
        out[p] = {k: v[N:N + L] for k, v in acc[p].items()}
    return out

# ----------------------------------------------------------------------------- estimator
def deriv5(A, axis):
    return (-np.roll(A, -2, axis) + 8 * np.roll(A, -1, axis) - 8 * np.roll(A, 1, axis) + np.roll(A, 2, axis)) / 12.0

def estimate(S, D, W):
    """Gradient-weighted LS per line/code-group, then sliding-window deconvolution (CG, FFT operators).
    Returns d_hat (L,2) [x, y]."""
    M = W.shape[0]
    gx = deriv5(S, 1) / N; gy = deriv5(S, 0) / N
    var = np.clip(S, 1, None) + N * SIG_R ** 2
    sl = slice(GUARD, GUARD + C_SENS)
    gx, gy, Dd, var = gx[:, sl], gy[:, sl], D[:, sl], var[:, sl]
    grp = (np.arange(C_TOT) % M)[sl]
    valid = np.ones(L); valid[:2] = 0; valid[-2:] = 0    # 5-pt along-track derivative edges
    I = np.zeros((M, L, 2, 2)); b = np.zeros((M, L, 2))
    for m in range(M):
        c = grp == m
        wgt = 1 / var[:, c]
        X, Y, Z = gx[:, c], gy[:, c], Dd[:, c]
        I[m, :, 0, 0] = (wgt * X * X).sum(1); I[m, :, 0, 1] = I[m, :, 1, 0] = (wgt * X * Y).sum(1)
        I[m, :, 1, 1] = (wgt * Y * Y).sum(1)
        b[m, :, 0] = (wgt * X * Z).sum(1); b[m, :, 1] = (wgt * Y * Z).sum(1)
    I *= valid[None, :, None, None]; b *= valid[None, :, None]
    Wf = np.array([np.fft.fft(np.r_[W[m], np.zeros(L - N)]) for m in range(M)])   # (M,L)
    def A(dv, m):      # z_k = sum_i w_i d_{k+i}
        return np.real(np.fft.ifft(np.conj(Wf[m])[:, None] * np.fft.fft(dv, axis=0), axis=0))
    def At(y, m):
        return np.real(np.fft.ifft(Wf[m][:, None] * np.fft.fft(y, axis=0), axis=0))
    # generic microvibration-envelope prior (same for every code): flat to 300 Hz, -40 dB/dec above
    fk = np.abs(np.fft.fftfreq(L, DT))
    lam_f = (1 / 0.3 ** 2) * np.maximum(1.0, (fk / 300.0) ** 2)
    def reg(dv):
        return np.real(np.fft.ifft(lam_f[:, None] * np.fft.fft(dv, axis=0), axis=0))
    def op(dv):
        out = reg(dv)
        for m in range(M):
            z = A(dv, m)
            out = out + At(np.einsum("kij,kj->ki", I[m], z), m)
        return out
    rhs = sum(At(b[m], m) for m in range(M))
    x = np.zeros((L, 2)); r = rhs - op(x); p = r.copy(); rs = np.sum(r * r)
    for it in range(400):
        Ap = op(p); alpha = rs / np.sum(p * Ap)
        x += alpha * p; r -= alpha * Ap; rsn = np.sum(r * r)
        if np.sqrt(rsn) < 1e-7 * np.sqrt(np.sum(rhs * rhs)):
            break
        p = r + (rsn / rs) * p; rs = rsn
    return x

# ----------------------------------------------------------------------------- metrics (sensing)
def sensing_metrics(d_true, d_hat):
    res = {}
    for name, (f1, f2) in {"20Hz-7kHz": (20, FL / 2), "20Hz-1kHz": (20, 1000), "300Hz-3kHz": (300, 3000)}.items():
        t = band_filter(d_true, f1, f2); e = band_filter(d_hat, f1, f2) - t
        res[name] = {ax: dict(truth=float(np.sqrt(np.mean(t[:, j] ** 2))), err=float(np.sqrt(np.mean(e[:, j] ** 2))))
                     for j, ax in enumerate(("x", "y"))}
    return res

def tone_errors(d_true, d_hat, freqs):
    T = np.fft.rfft(d_true, axis=0); Hh = np.fft.rfft(d_hat, axis=0)
    out = []
    for f in freqs:
        k = bin_of(f)
        rel = np.abs(Hh[k] - T[k]) / np.abs(T[k])
        out.append((k * FL / L, float(rel[0]), float(rel[1])))
    return out

def noise_floor(d_hat, tone_freqs, f1, f2):
    """rms of the estimate on non-tone bins (truth = 0 there), scaled to the full band -> per-sample noise."""
    H = np.fft.rfft(d_hat, axis=0); m = band_mask(f1, f2).copy()
    for f in tone_freqs:
        k = bin_of(f); m[max(k - 1, 0):k + 2] = False
    nb = band_mask(f1, f2).sum()
    p = 2 * np.mean(np.abs(H[m]) ** 2, axis=0) / L ** 2 * nb
    return np.sqrt(p)

# ----------------------------------------------------------------------------- image-quality part
def lanczos3(x):
    return np.where(np.abs(x) < 3, np.sinc(x) * np.sinc(x / 3), 0.0)

def splat_transfer(d, c, f, kind):
    """Complex transfer of one stage sample that truly sits at d but is accumulated as if at c.
    Arrays d, c same shape; returns complex array."""
    if kind == "none":
        return np.exp(2j * np.pi * f * d)
    if kind == "integer":
        return np.exp(2j * np.pi * f * (d - np.round(c)))
    base = np.floor(c)
    if kind == "bilinear":
        taps = np.arange(0, 2)
        h = lambda x: np.clip(1 - np.abs(x), 0, None)
    elif kind == "lanczos3":
        taps = np.arange(-2, 4)
        h = lanczos3
    tot = 0; norm = 0
    for t in taps:
        m = base + t
        wv = h(m - c); norm = norm + wv
        tot = tot + wv * np.exp(-2j * np.pi * f * (m - d))
    return tot / norm

def stage_view(x):
    """(L,) -> (L, N) values at times k+i for line k (periodic)."""
    idx = (np.arange(L)[:, None] + np.arange(N)[None, :]) % L
    return x[idx]

def causal_harmonic_predict(d_hat, d_lowfused, freqs, block=64, win=2048, ridge=1e-2):
    """Causal prediction: fit known-frequency harmonics (wheel tach / cryo drive) to the smoothed
    estimate that is final (older than N lines), extrapolate N..N+block lines ahead."""
    pred = np.zeros_like(d_hat)
    n = np.arange(L)
    fk = np.array(sorted(set(bin_of(f) for f in freqs if 20 <= f <= 3000))) * FL / L
    for s in range(0, L, block):
        t_hist = np.arange(s - N - win, s - N)
        idx = t_hist % L
        Xh = np.concatenate([np.cos(2 * np.pi * fk[None, :] * t_hist[:, None] * DT),
                             np.sin(2 * np.pi * fk[None, :] * t_hist[:, None] * DT)], 1)
        coef = np.linalg.solve(Xh.T @ Xh + ridge * len(t_hist) * np.eye(Xh.shape[1]), Xh.T @ d_hat[idx])
        t_new = np.arange(s, s + block)
        Xn = np.concatenate([np.cos(2 * np.pi * fk[None, :] * t_new[:, None] * DT),
                             np.sin(2 * np.pi * fk[None, :] * t_new[:, None] * DT)], 1)
        pred[s:s + block] = Xn @ coef
    return pred + d_lowfused

def mtf_study(d_true, d_hat, freqs_known, rng, alpha=0.02, gmax=2.5):
    lowband = band_filter(d_true, 0, 20)                                # from gyro/star-tracker fusion
    d_low_fused = lowband + 0.01 * rng.standard_normal(lowband.shape)   # 0.01 px fusion error (assumed)
    d_smooth = band_filter(d_hat, 20, FL / 2) + d_low_fused
    d_causal = causal_harmonic_predict(band_filter(d_hat, 20, FL / 2), d_low_fused, freqs_known)
    out = {}
    lines = np.arange(1200, L - N)        # skip predictor warm-up and wrap-around
    for j, ax in enumerate(("x_cross", "y_along")):
        Dt = stage_view(d_true[:, j])[lines]; Ds = stage_view(d_smooth[:, j])[lines]
        Dc = stage_view(d_causal[:, j])[lines]
        res = {}
        for f in (0.25, 0.45, 0.5):
            row = {}
            variants = [("none", "none", Dt * 0), ("integer_causal", "integer", Dc), ("bilinear_causal", "bilinear", Dc),
                        ("lanczos3_causal", "lanczos3", Dc), ("bilinear_oracle", "bilinear", Dt),
                        ("lanczos3_oracle", "lanczos3", Dt), ("lanczos3_buffered", "lanczos3", Ds)]
            for label, kind, Cm in variants:
                Hk = splat_transfer(Dt, Cm, f, kind).mean(1)
                row[label] = float(np.mean(np.abs(Hk)))
                if label in ("none", "lanczos3_causal", "lanczos3_buffered"):
                    # post-hoc restoration with per-line OTF predicted from the smoothed estimate
                    Hhat = splat_transfer(Ds, Cm, f, kind).mean(1)
                    G = np.conj(Hhat) / (np.abs(Hhat) ** 2 + alpha) * (1 + alpha)
                    G = G * np.minimum(1, gmax / np.maximum(np.abs(G), 1e-9))
                    row[label + "+restore"] = float(np.mean(np.real(G * Hk)))
                    row[label + "+restore_err"] = float(np.sqrt(np.mean(np.abs(G * Hk - 1) ** 2)))
                    row[label + "+restore_noisegain_dB"] = float(10 * np.log10(np.mean(np.abs(G) ** 2)))
                    Go = np.conj(Hk) / (np.abs(Hk) ** 2 + alpha) * (1 + alpha)
                    Go = Go * np.minimum(1, gmax / np.maximum(np.abs(Go), 1e-9))
                    row[label + "+oracle"] = float(np.mean(np.real(Go * Hk)))
            # noise power of fractional splats relative to plain accumulation (white noise)
            res[f] = row
        # noise variance ratio of fractional accumulation (per output pixel, white noise)
        for kind, h, taps in (("bilinear", lambda x: np.clip(1 - np.abs(x), 0, None), np.arange(0, 2)),
                              ("lanczos3", lanczos3, np.arange(-2, 4))):
            base = np.floor(Dc); w2 = 0; ws = 0
            for t in taps:
                wv = h(base + t - Dc); w2 = w2 + wv ** 2; ws = ws + wv
            res["noise_var_ratio_" + kind] = float(np.mean(w2 / ws ** 2))
        # inter-line registration residual after resampling with smoothed estimate
        cent_t = Dt.mean(1); cent_s = Ds.mean(1)
        res["line_centroid_resid_px"] = float(np.std(cent_t - cent_s))
        res["uncorr_within_window_rms_px"] = float(np.sqrt(np.mean((Dt - Dt.mean(1, keepdims=True)) ** 2)))
        res["causal_pred_err_rms_px"] = float(np.sqrt(np.mean(band_filter(d_causal[:, [j]] - d_true[:, [j]], 20, FL / 2)[lines] ** 2)))
        out[ax] = res
    return out

# ----------------------------------------------------------------------------- driver
def main():
    t0 = time.time()
    rng = np.random.default_rng(20260924)
    codes = design_codes(np.random.default_rng(2))
    fr = np.array([20, 50, 100, 200, 441.25, 882.5, 1000, 1323.75, 2000, 3000, 7000])
    spec = code_spectrum_table(codes, fr)
    fgrid = np.linspace(20, FL / 2, 3000)
    specg = code_spectrum_table(codes, fgrid)
    report = {"code_effective_|W|": {k: dict(zip([float(x) for x in fr], np.round(v, 2).tolist())) for k, v in spec.items()},
              "code_min_|W|_20Hz-7kHz": {k: float(v.min()) for k, v in specg.items()},
              "code_min_|W|_20Hz-1.6kHz": {k: float(v[fgrid <= 1600].min()) for k, v in specg.items()},
              "sign_changes": {k: [sign_changes(w) for w in W] for k, W in codes.items()},
              "codes": {k: [''.join('+' if x > 0 else '-' for x in w) for w in W] for k, W in codes.items()}}
    runs = []
    if QUICK:
        plan = [("tonal-large", "urban", 1)]
    else:
        plan = [("comb", "agri", 1), ("comb", "urban", 1), ("floor-zero-jitter-noiseless", "urban", 1),
                ("floor-realistic-noiseless", "urban", 1)] + \
               [("realistic", cls, s) for cls in ("urban", "agri", "low") for s in (1, 2, 3)] + [("tonal-large", "urban", 1)]
    for kind, cls, seed in plan:
        r = np.random.default_rng(1000 * seed + {'comb': 1, 'realistic': 2, 'tonal-large': 4}.get(kind, 3) * 10 + {'urban': 1, 'agri': 2, 'low': 3}[cls])
        jkind = {"floor-zero-jitter-noiseless": "zero", "floor-realistic-noiseless": "realistic"}.get(kind, kind)
        noisy = not kind.startswith("floor")
        fine = make_scene(L + 2 * N + 60, C_TOT + 10, cls, r)
        gmed, grms = gradient_stats(fine)
        d, fk = make_jitter(jkind, r) if jkind != "zero" else (np.zeros((L, 2)), [])
        acc = run_tdi(fine, d, codes, r, noise=noisy)
        entry = {"kind": kind, "scene": cls, "seed": seed, "grad_median_frac_per_px": gmed, "grad_rms_frac_per_px": grms,
                 "jitter_rms_20Hz+": [band_rms(d[:, 0], 20, FL / 2), band_rms(d[:, 1], 20, FL / 2)]}
        for pipe in ("eq", "raw"):
            for lay, W in codes.items():
                if kind == "floor-zero-jitter-noiseless":
                    dh = estimate(acc[pipe]["S"], acc[pipe][lay], W)
                    entry[f"{lay}/{pipe}"] = {"false_jitter_rms_20Hz-7kHz": [band_rms(dh[:, j], 20, FL / 2) for j in range(2)],
                                              "false_jitter_rms_20Hz-1kHz": [band_rms(dh[:, j], 20, 1000) for j in range(2)]}
                    continue
                if pipe == "raw" and lay not in ("multi4",):
                    continue
                dh = estimate(acc[pipe]["S"], acc[pipe][lay], W)
                key = f"{lay}/{pipe}"
                ent = {"metrics": sensing_metrics(d, dh)}
                # regression slope (scale bias) in band 20 Hz-3 kHz
                t = band_filter(d, 20, 3000); e = band_filter(dh, 20, 3000)
                ent["slope"] = [float(np.sum(t[:, j] * e[:, j]) / np.sum(t[:, j] ** 2)) for j in range(2)]
                if kind == "comb":
                    ent["tones"] = tone_errors(d, dh, fk)
                    ent["noise_floor_fullband"] = noise_floor(dh, fk, 20, FL / 2).tolist()
                    ent["noise_floor_1kHz"] = noise_floor(dh, fk, 20, 1000).tolist()
                if jkind in ("realistic", "tonal-large") and noisy and pipe == "eq" and lay in ("multi4", "split"):
                    ent["mtf"] = mtf_study(d, dh, fk, r)
                entry[key] = ent
        runs.append(entry)
        print(f"[{time.time() - t0:6.1f}s] done {kind}/{cls}/seed{seed}  grad median {gmed:.3f}", flush=True)
    report["runs"] = runs
    with open(__file__.replace(".py", "_results.json"), "w") as fh:
        json.dump(report, fh, indent=1, default=float)
    summarize(report)

def summarize(rep):
    print("\n=== CODE SPECTRA (effective |W|, rms over interleaved codes; N=64, 14.12 kHz) ===")
    for k, v in rep["code_effective_|W|"].items():
        print(f"{k:7s}", " ".join(f"{f:>7.0f}:{w:5.2f}" for f, w in v.items()))
    print("min |W| 20Hz-7kHz:", {k: round(v, 3) for k, v in rep["code_min_|W|_20Hz-7kHz"].items()})
    print("min |W| 20Hz-1.6kHz:", {k: round(v, 3) for k, v in rep["code_min_|W|_20Hz-1.6kHz"].items()})
    print("sign changes:", rep["sign_changes"])
    for r in rep["runs"]:
        print(f"\n=== {r['kind']} / {r['scene']} / seed {r['seed']}: grad median {r['grad_median_frac_per_px']:.3f}/px, "
              f"rms {r['grad_rms_frac_per_px']:.3f}/px; jitter >20Hz rms x={r['jitter_rms_20Hz+'][0]:.3f} y={r['jitter_rms_20Hz+'][1]:.3f} px")
        for key in [k for k in r if "/" in k]:
            e = r[key]
            if "false_jitter_rms_20Hz-7kHz" in e:
                print(f"  {key:12s} FALSE jitter (no motion, no noise) 20Hz-7kHz x/y = {e['false_jitter_rms_20Hz-7kHz'][0]:.5f}/{e['false_jitter_rms_20Hz-7kHz'][1]:.5f} px;"
                      f" 20Hz-1kHz = {e['false_jitter_rms_20Hz-1kHz'][0]:.5f}/{e['false_jitter_rms_20Hz-1kHz'][1]:.5f} px")
                continue
            m = e["metrics"]
            s = "  ".join(f"{b}: err x={m[b]['x']['err']:.4f} y={m[b]['y']['err']:.4f} (truth {m[b]['x']['truth']:.3f}/{m[b]['y']['truth']:.3f})"
                          for b in m)
            print(f"  {key:12s} slope={e['slope'][0]:.3f}/{e['slope'][1]:.3f}  {s}")
            if "tones" in e:
                nt = [t for t in e["tones"] if abs((t[0] / (FL / 32)) - round(t[0] / (FL / 32))) < 1e-6]
                print(f"     noise floor per 70.8us sample full-band x/y = {e['noise_floor_fullband'][0]:.4f}/{e['noise_floor_fullband'][1]:.4f} px;"
                      f" 20Hz-1kHz = {e['noise_floor_1kHz'][0]:.4f}/{e['noise_floor_1kHz'][1]:.4f} px")
                print("     split-null tones rel.err (x,y):", [(round(f, 1), round(a, 2), round(b, 2)) for f, a, b in nt])
                oth = np.array([[a, b] for f, a, b in e["tones"] if 20 < f < 3000])
                print(f"     median rel.err all tones 20Hz-3kHz: {np.median(oth):.3f}; worst: {oth.max():.2f}")
            if "mtf" in e:
                for ax, res in e["mtf"].items():
                    for fq in (0.5, 0.45, 0.25):
                        r5 = res[fq]
                        print(f"     MTF@{fq} {ax}: none {r5['none']:.3f} | int-causal {r5['integer_causal']:.3f} | bilin-causal {r5['bilinear_causal']:.3f} | "
                              f"lanc3-causal {r5['lanczos3_causal']:.3f} | bilin-oracle {r5['bilinear_oracle']:.3f} | lanc3-oracle {r5['lanczos3_oracle']:.3f} | "
                              f"lanc3-buffered {r5['lanczos3_buffered']:.3f}")
                        print(f"        restore-only {r5['none+restore']:.3f} (err {r5['none+restore_err']:.3f}, noise {r5['none+restore_noisegain_dB']:+.1f} dB, oracle {r5['none+oracle']:.3f}) | "
                              f"lanc3-causal+restore {r5['lanczos3_causal+restore']:.3f} ({r5['lanczos3_causal+restore_noisegain_dB']:+.1f} dB) | "
                              f"lanc3-buffered+restore {r5['lanczos3_buffered+restore']:.3f} ({r5['lanczos3_buffered+restore_noisegain_dB']:+.1f} dB)")
                    print(f"        win-rms {res['uncorr_within_window_rms_px']:.3f} px, causal-pred err {res['causal_pred_err_rms_px']:.3f} px, "
                          f"line-centroid resid {res['line_centroid_resid_px']:.4f} px, splat noise-var ratio bilin {res['noise_var_ratio_bilinear']:.2f} lanc3 {res['noise_var_ratio_lanczos3']:.2f}")

if __name__ == "__main__":
    main()
