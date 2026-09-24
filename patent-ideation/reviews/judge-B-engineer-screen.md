# Judge B: Engineering and Patentability Screen of Six Candidates

Reviewer role: chief systems engineer (LEO/VLEO EO: payload, ADCS, propulsion, mission ops) and registered patent agent.
Scope: inventor-1 to inventor-6 in `candidates/`. The other judge's work in `reviews/` was not read.
Method: I recomputed every headline number (Python scripts; the arithmetic is shown below). I ran 2-3 prior-art web searches per candidate. Google Patents and USPTO full text were blocked by the egress proxy, so patent characterisations come from abstracts and snippets.

Scoring is 1-10, where higher is better. For "Lifetime/Sustainability", 10 means no negative effect on vehicle life, propellant or deorbit compliance. For "Impl. cost/risk", 10 means cheap and low risk.

---

## 1. Score table

| # | Candidate | Novelty | Non-obvious | Tech. feasibility | Lifetime / sustainability | Impl. cost / risk | Commercial value & design-around resistance | **Total /60** |
|---|---|---|---|---|---|---|---|---|
| 6 | Chronometric ground beacon (time-tag vs pitch) | 7 | 5 | 8 | 10 | 9 | 4 | **43** |
| 1 | CC-TDI: complementary-coded TDI jitter sensing | 7 | 6 | 6 | 7 | 5 | 7 | **38** |
| 5 | TIR kinematic pre-look → motion-matched SAR | 7 | 6 | 4 | 5 | 3 | 6 | **31** |
| 2 | Onboard 3D cloud / LOS gap threading (single sat) | 5 | 4 | 4 | 6 | 7 | 5 | **31** |
| 3 | Leader→follower 3D cloud field + dual-ray tracing | 5 | 4 | 3 | 4 | 3 | 5 | **24** |
| 4 | VLEO torque-balanced ram visor + drag steering | 4 | 3 | 5 | 2 | 3 | 3 | **20** |

Headline findings:
- **Inventors 2 and 3 describe the same invention**, one on a single satellite and one on a pair. Both rely on a height/along-track-wind separation that the physics does not support as described (§3). Treat them as one filing.
- **Inventor 4's central premise is wrong.** A forward-only-thrust satellite *can* already shift phase in both directions: thruster off gives the early/east shift, extra thrust gives the late/west shift. The visor only buys the lead time that about 6 more hours of planning buys for free. It also carries a clear lifetime penalty.

---

## 2. Per-candidate findings

### Candidate 1: CC-TDI (Optics)

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| Focal length | 5.5 m | 5.5 µm × 500 km / 0.5 m = 5.5 m | OK |
| IFOV | 1.0 µrad | 1.0 µrad | OK |
| Ground speed v_g at 500 km | 7.06 km/s | 7.613 × 6378/6878 = 7.06 km/s | OK |
| Line rate | 14.12 kHz | 14.12 kHz | OK |
| Integration window T | 4.53 ms | 64 × 70.8 µs = 4.53 ms | OK |
| Signal per stage | 150 e⁻ | Photon budget (L ≈ 30-100 W m⁻² sr⁻¹ µm⁻¹, 0.4 µm pan, 0.5 m aperture, QE·τ ≈ 0.5) gives roughly 250-800 e⁻ per 70.8 µs | Conservative, OK |
| σ_D | ≈100 e⁻ | √(9600 + 64·25) = 106 e⁻; var(2A − S) = var(A) + var(B) = var(S) | OK |
| Per-column σ_d | 0.83 px | 100 / (30 × 4) = 0.83 px | OK |
| MTF, uncorrected | 0.64 | exp(−2π²·0.09·0.25) = exp(−0.444) = 0.641 | OK |
| MTF, residual | 0.99 | exp(−0.0123) = 0.988 | OK |
| Extra SRAM | 1.3 Mbit | 1024 × 64 × 20 bit = 1.31 Mbit | OK |
| Jitter telemetry | 0.45 Mbit/s | 2 × 14.12k × 16 = 0.45 Mbit/s | OK |

**Physics and logic corrections**

1. **The averaging count is double-counted.** "K_eff = 2,400 from 1,024 columns × 2 gradient axes" is wrong. Each sensing column gives *one* scalar equation D = g·(w⋆d) in two unknowns. With random gradient orientation, the information per axis is about Σg_x² ≈ K·g²/2. Also, "rotating column selection" adds no samples within a given line. Corrected precision:
   - full band: 0.83/√512 ≈ **0.037 px worst case, about 0.018 px typical** (2.2× worse than claimed);
   - in a 1 kHz band: × √(1000/7060) → **about 0.014 / 0.007 px**.
   These are still excellent and still beat any gyro in this band, so the headline survives, but the numbers need correcting. The 4-code interleave is fine: per-frequency information is Σ_m 256·|W_m|² = 1024·mean|W|², which is equivalent to K = 1024 at |W_eff| = 4.
2. **The closed loop cannot correct sub-pixel jitter.** Claim 10 shifts accumulation addresses by integer pixels, which does nothing for 0.3 px rms jitter. The "0.05 px residual → MTF 0.99" result is mislabelled. Known-PSF deconvolution does not remove the displacement. It restores MTF and pays for it in noise: at Nyquist the noise gain is about 1/0.64, roughly −3.9 dB of SNR at that frequency. Either claim **fractional-pixel (interpolated or weighted) accumulation**, or state the restored MTF together with the noise penalty.
3. **Feasibility depends on the TDI architecture.** Per-stage access exists only in digital-domain TDI CMOS. That costs 64 × 12,000 × 14.12 kHz ≈ **10.8 Gsample/s per band** of internal ADC traffic, plus √N read-noise growth. This is the reason high-end space TDI is charge-domain (CCD or CCD-in-CMOS). There, the only embodiment is claim 13 (dual charge registers with a steering gate), which is unproven and at enablement risk. That embodiment is also where the licensing value sits.
4. **Linearisation and fixed-pattern noise.** Second-order terms (½s''d²) and row PRNU mismatch produce a false D proportional to s itself, not to ∇s. Per-row equalisation is essential and belongs in an independent claim, not a dependent one.

**Mission / lifetime.** Lifetime impact is essentially neutral to positive. The method adds no consumables. Line-rate LOS telemetry is a wheel-health and bearing-degradation monitor, which is a real on-orbit ageing diagnostic. Caution: removing the passive isolator, as the inventor suggests, makes image quality depend on scene texture. Over ocean the method falls back to the gyro, so the isolator should not be deleted outright.

**Prior art (my searches)**
- Teledyne e2v US 9,967,490 / EP 2 954 671 B1, sub-matrix comparison for travelling-error detection. This is the closest art. It is a contiguous split with best-match shift and extra offset columns. https://patents.google.com/patent/US9967490 , https://patents.google.com/patent/EP2954671B1/en
- Wuhan Univ. US 11,210,766 (ground jitter detection for TDI CCD), and the IEEE continuous dynamic shooting model, which subdivides TDI integration intervals to detect jitter (ground processing). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11210766 , https://ieeexplore.ieee.org/document/9247296/
- Digital-domain TDI-CMOS with jitter estimation and alignment (frame registration). https://pmc.ncbi.nlm.nih.gov/articles/PMC12158263/
- Complementary / two-bucket coded exposure in computational imaging (SPAD "generalized event cameras"; sign-coded exposure). These are the closest to "complementary partition, no light loss", but they are not TDI and not motion sensing. https://arxiv.org/pdf/2407.02683 , https://arxiv.org/pdf/2305.03226
- TDI random-exposure super-resolution (charge-transfer coding in TDI CCD). https://www.sciencedirect.com/science/article/abs/pii/S0030401818304279

**Assessment.** This is a real invention. The sliding-window convolution inversion with spectrally designed, interleaved balanced codes is not taught by e2v. The two-bucket computational-imaging art weakens the "no light loss" argument as a standalone point. Claims must lead with steps (d) and (e) plus the no-null code design. Main risk: a §103 rejection over e2v plus two-bucket coded exposure.

---

### Candidate 2: Onboard 3D cloud / LOS gap threading (single satellite)

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| Parallax shift | 2.1 km | 1.8 × tan 49.7° = 2.12 km | OK |
| h/H scale | 1/278 | 1.8/500 = 1/278 | OK |
| Swept band | 3.1 km | 870 km × 1/278 = 3.13 km | OK |
| ±40° off-nadir: VZA | 43.9° | asin(1.0784·sin40°) = 43.9° | OK |
| ±40° off-nadir: access half-width | 434 km | 3.9° central angle ≈ 434 km | OK |
| ±40° off-nadir: window | 123 s | 868 / 7.06 = 123 s | OK |
| LMC boresight 38° ± 10° | VZA 30-50° | VZA 30.4-53.3°; about 18 frames at 2.5 s | Minor error |
| tan 49.7° − tan 32.6° | 0.54 | 1.179 − 0.640 = 0.539; × 1.8 km = 0.97 km | OK |
| Crossing-point speed near nadir | 25 m/s | 1.8/500 × 7060 = 25.4 m/s | OK |
| Clear window | +8 to +27 s | For the stated gap, requiring the whole [0.9, 1.8] km segment inside it gives roughly +16 to +35 s, before E-W advection | Same order |

**Physics error (critical, shared with Candidate 3): height and along-track wind are nearly degenerate for a single platform.**
In flat-Earth geometry with constant ground speed, a fixed ground point is seen at tanθ(t) = (x − v_g t)/H, which is *linear* in t. The along-track disparity is then Δx_ij = h(tanθ_i − tanθ_j) + u(t_i − t_j) = (u − h·v_g/H)(t_i − t_j). Only the combination u − h·v_g/H is observable. The inventor's statement that "tanθ is nonlinear in t, so h and u separate" is false to first order. Only Earth curvature, which is weak at these angles, breaks the degeneracy.

I computed the full spherical-geometry Fisher information for the inventor's own geometry: 18 frames at off-nadir 28-48°, 6 m (0.3 px) matching noise, and unknowns (h, u, s₀). Result: **σ_h ≈ 380 m and σ_u ≈ 6.3 m/s**, against the claimed 60 m and 1 m/s. At σ_u = 6.3 m/s, 60 s of advection gives a 380 m position error. That is the same size as the 0.3-1 km gaps, so the threading prediction becomes close to a coin toss. This matches MISR's published performance of about 400 m height and 3 m/s wind, which it reaches only with looks out to 70.5°. See the [NASA MISR note](https://science.nasa.gov/earth/earth-observatory/cloud-height-and-wind-speed-1698/).

**Fixes:**
- (a) Take height from the cloud-to-shadow offset under the known sun vector. The shadow moves with the cloud, so this measurement is wind-free.
- (b) Take along-track wind from an uplinked NWP or GEO atmospheric-motion-vector prior.
- (c) Or tilt the look-ahead camera to ≥ 60° VZA. With views at 0/45.6/60°, I get σ_h ≈ 62 m and σ_u ≈ 1.1 m/s.

Cloud-base estimation remains the weakest link. The "base = 0 (column)" conservative variant should be claimed.

**Other issues**
- The yield model 1 − 0.5³ treats three samples as independent. At the window edges the slab segment is 0.87 km long, so the samples are correlated, and a whole segment is less likely to be clear than a single point. The ×1.5 gain is optimistic. I would expect ×1.2-1.4 and would want a real-data simulation.
- The approach competes with multi-target scheduling. Holding a specific sub-window for one target costs other targets.

**Mission / lifetime.** Impact is small. It adds more CMG slews (actuator cycles), a 0.4 kg / 3 W camera, and 8 W of processing. Longer oblique slant paths do not affect lifetime.

**Prior art (my searches)**
- US 9,126,700 / WO2011089477A1: forward preview cameras at several nadir angles, autonomous target selection. https://patents.google.com/patent/WO2011089477A1/en
- JPL Dynamic Targeting on CogniSAT-6: https://arxiv.org/abs/2509.05304
- US 9,001,311, cloud height from parallax: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9001311
- Cloud/shadow-location patents that use cloud height and sun angle (e.g., US 11,256,916 / 11,769,232 / 12,136,201): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11769232
- Canon-type "information processing apparatus" patents (US 11,074,446 and US 11,450,100) came up in the off-nadir / cloud search. Full text could not be fetched; they must be reviewed. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11074446

**Assessment.** The reframing from "which ground is clear" to "from which of my future viewpoints is this target clear" has some novelty. However, a skilled person holding DT plus textbook parallax (offset = h·tanθ) plus urban-canyon view selection is not far away. The estimation method as described does not work; the fixes above are required.

---

### Candidate 3: Leader→follower 3D cloud field (Constellation)

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| Separation for 120 s lead | 850 km | 7.06 × 120 = 847 km | OK |
| ±26° head ground offset | 244 km, 35 s | 246 km (spherical), 34.9 s | OK |
| σ_h from geometry alone | 18 m | 9 m / 0.488 = 18 m | OK, but misleading (see below) |
| ISL payload | 2.2 Mbit | 64,000 cells × 34 bit = 2.18 Mbit | OK |
| Off-nadir angles | 41.9°, 27.4°, 16.7° | 41.1°, 27.2°, 16.6°; VZA ≈ 45.1° at the edge | Minor |

**Physics error (critical):** the fore / nadir / aft ±26° triplet is *exactly* degenerate for (h, u_along). By symmetry the disparities are ±(a·h + b·u), and my Jacobian columns for h and u are exactly proportional: 0.5398 : −35.02 in both rows, which makes the Fisher matrix singular. **Along-track wind and height cannot be separated with this camera set at any SNR.** The claimed σ_h of 100-200 m and σ_v of 0.5-1 m/s are unsupported.

A MISR-style asymmetric 0 / 45.6 / 60° set gives σ_h ≈ 62 m and σ_u ≈ 1.1 m/s. Alternatively, derive height from the shadow offset, or give the leader a cross-track (different-plane) baseline.

**Other issues**
- **Claim 4 ("VAZ ≈ SAZ hides shadows")** is the well-known BRDF hot-spot / shadow-hiding effect (Hapke, Kuusk). It is weak as a novelty hook, although it is a useful dependent claim inside the scheduling context.
- **The toy Monte-Carlo cannot be verified.** Inventor-internal code at a single scene is not evidence of "2D ranking inverted".
- **Lead-time decay.** Cumulus lifetimes are 5-15 min, and the inventor concedes the benefit falls off beyond about 5 min.

**Mission / lifetime / sustainability (the user's concern)**
- A **scout satellite per orbital plane** adds tracked objects and brings its own deorbit-compliance obligation (the 5-year FCC rule at LEO).
- The scout needs formation-keeping propellant (differential drag or EP) to hold a 1-10 min phase lag. With about 1 km of along-track tolerance and differential ballistic coefficients, this is a continuous Δv consumer.
- The follower's gain comes at larger off-nadir angles: more slews, more CMG cycles, and more ISL terminal wear.
- The business case must fund a whole spacecraft per plane.

**Prior art (my searches)**
- IAI IL276014B2 "Cloud reduction in satellite imagery" (leading/trailing). Full text blocked; the family must be read. https://patents.google.com/patent/IL276014B2/en
- UrtheCast OptiSAR CloudCam: https://www.eoportal.org/satellite-missions/optisar
- JPL DT and GEO-supplemented DT: https://arxiv.org/abs/2509.05304
- MISR joint height and wind (400 m / 3 m/s): https://science.nasa.gov/earth/earth-observatory/cloud-height-and-wind-speed-1698/
- US 9,001,311: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9001311

**Assessment.** Candidate 3 is Candidate 2 plus an ISL and a sun ray. Filed separately, the two would largely overlap each other. **Recommendation: merge into one application.** The independent claim should cover the core step "select the acquisition time of a fixed target from LOS-segment / 3D cloud intersection, where the 3D field comes from any source". Dependent claims then cover the onboard look-ahead source, the constellation leader source, the sun ray, and multi-view union.

---

### Candidate 4: VLEO ram visor + drag steering

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| v / period / n | 7.755 km/s, 89.5 min, 1.170e-3 rad/s | Same | OK |
| Baseline drag f₀ | 9.3e-6 m/s² (1.39 mN) | ½·7e-11·7755²·2.2·0.3/150 = 9.26e-6 m/s² | OK |
| Visor Δf | 1.23e-5 m/s² (1.85 mN) | 1.235e-5 m/s² | OK |
| Option A, 48 h thruster off | s = 416 km, Δt = 53.7 s, shift 20.5 km, Δa = 2.75 km | Same | OK |
| Option B, visor out | s = 967 km, Δt = 124.8 s, shift 47.5 km, Δa = 6.38 km | Same | OK |
| Wheel saturation | 270 s | 0.5 / 1.85e-3 = 270 s | OK |
| Along-track formula | s ≈ 3/2·f·τ² | Correct secular term | OK |

**Physics and engineering corrections**
1. **False premise that forward-only thrust gives one-directional phasing.** Thruster-off drag already gives the early/east direction and extra thrust gives the late/west direction, so bidirectional authority exists today. The visor only accelerates the east direction, by 2.3×. Because s ∝ τ², the same 26 km shift is available with the thruster off alone given **54.1 h** of lead instead of 48 h. **The whole hardware invention is worth about 6 h of planning lead time.** That fact destroys both the commercial case and the non-obviousness argument.
2. **The counter-flap doubles the added drag.** A 0.4 m² counter-flap at 1 m, sized for torque balance, adds another 1.85 mN. The frontal area therefore goes from 0.30 to 1.10 m², not 0.70 m². Authority rises to about 75 km per 48 h, but so does the cost: **4.3 m/s per targeting event, not 2.1 m/s**. A simpler design-around avoids the counter-flap altogether: put the drag surfaces symmetric about the CoM plane, as with aircraft speed brakes, instead of at the aperture.
3. **Aerodynamic stability.** A large panel ahead of the CoM moves the centre of pressure forward and reduces passive weathervane (yaw/pitch) stability. That needs analysis and is not addressed.
4. **The AO "shield state" is expensive.** At δ = 25°, projected area is 0.4·sin25° = 0.17 m², plus the matching counter-flap, which is about +0.34 m² on a 0.30 m² baseline. That **more than doubles lifetime drag-makeup propellant and thruster power**. The shielding benefit is small: ram AO strikes a nadir aperture at grazing incidence (thermal spread about ±7°), and a fixed lip baffle does the same job at zero cost.
5. The claim that "ρ at 500 km is 50× lower" is conservative. The true ratio is about 70-140×. Harmless.

**Lifetime and propellant (the user's specific concern), 150 kg at 250 km, Isp 1500 s**

| Condition | ρ (kg/m³) | Drag | Makeup Δv/yr | EP power (30 mN/kW) |
|---|---|---|---|---|
| Solar min | 2.5e-11 | 0.50 mN | 104 m/s | about 17 W |
| Moderate | 7e-11 | 1.39 mN | 292 m/s | about 46 W |
| Solar max | 1.6e-10 | 3.18 mN | 668 m/s | about 106 W |

- **5-year mix** (1.5 yr max, 2 yr moderate, 1.5 yr min) with no visor use: **Δv ≈ 1,740 m/s, about 16.8 kg of Xe**. That already exceeds the inventor's "typical 5-15 kg" load.
- Each targeting event costs 2.1 m/s (visor only) or 4.3 m/s (with counter-flap). At 50-100 events per year, that is **+100-430 m/s per year**, which is 30-150% of the baseline makeup.
- The shield state doubles the baseline to about 35 kg over 5 years. **The visor is a propellant-life consumer, not "small".**
- **Stuck-deployed failure** (visor plus counter-flap, A = 1.1 m²): makeup thrust needed at solar max is 3.18 × 1.1/0.3 ≈ **11.6 mN**. That is beyond a typical small-sat EP thruster, so a stuck visor ends the mission during solar max.
- **No-thrust decay from 250 km** (simple exponential-atmosphere integration): about 29 days nominal versus about 8 days with the visor stuck at moderate density; about 13 versus 3.5 days at solar max. Deorbit compliance is trivially met, which is the only sustainability positive. There is essentially no safe-mode survival margin.
- A fail-safe spring-to-stow mechanism, a burn-wire jettison, or both are mandatory.
- There is also jitter risk: a visor mechanism next to the TDI aperture in a flow of about 10⁻³ N.

**Prior art (my searches)**
- Omar & Bevilacqua, *Drag De-Orbit Device (D3)*. A retractable, modulated drag device explicitly used to target any longitude/latitude by varying the ballistic coefficient, given enough lead time. This anticipates much of method claim 1, which recites only a "variable-drag surface". https://arc.aiaa.org/doi/10.2514/1.A34218
- Planet differential drag (attitude-mode based): https://arxiv.org/pdf/1509.03270 , https://arxiv.org/pdf/1806.01218
- Ground-track control with differential drag: https://arc.aiaa.org/doi/10.2514/1.A35256
- Optimal aerodynamic orbit control in VLEO (2026): https://www.sciencedirect.com/science/article/pii/S0094576526001372
- Differential lift/drag satellite design (SOAR lineage): https://arxiv.org/pdf/2303.16612
- Stingray VLEO: https://www.eoportal.org/satellite-missions/stingray

**Assessment.** Claim 1 is obvious over D3 plus ground-track drag control plus Planet. Claim 2's hardware combination is narrow, easily designed around (symmetric CoM-plane drag panels, or simply longer lead time), and costly in lifetime. **Not recommended.**

---

### Candidate 5: TIR kinematic pre-look → motion-matched SAR

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| Look angle (550 km, 35° incidence) | 31.5° | 31.87° | Minor |
| Ground range | 337 km | 348 km | Minor |
| Slant range | 645 km | 659 km | Minor |
| F1 / F2 offsets | 185 / 68 km | 645·tan16° = 185 km, 645·tan6° = 68 km | OK |
| Δt, F1 to F2 | 16.7 s | 16.7 s | OK |
| Broadside v_r | 1.78 m/s | 3.11·sin35° = 1.78 m/s | OK |
| Azimuth displacement | about 157 m | about 157 m | OK |
| Doppler offset | 115 Hz | 115 Hz | OK |
| Range walk over 1.5 s | about 5 cells | 2.7 m ≈ 5 cells | OK |
| Squint | 8.0° | y = 337·tan15° = 90.3 km, ψ = 7.97° | OK |
| K_a | 5,281 Hz/s | 5,281 Hz/s | OK |

**Physics and system errors**
1. **Timing conflict (critical).** A forward squint of 8° puts aperture centre at about 90 km ahead of zero-Doppler. But F2 looks only 68 km ahead. The SAR aperture would therefore occur *between* F1 and F2, before the velocity is known. Roughly half of all ship headings need a forward squint, and for those the stated field layout fails. **Fix:** place both TIR fields beyond the maximum forward squint (e.g., +20° and +30° along-track, or ψ_max + margin). Or restrict to aft squint and claim "TIR fields ahead of the forward-most aperture-centre position".
2. **The FM-rate sensitivity is a factor of 2 low.** K_a ∝ V_rel², so ΔK_a/K_a ≈ 2·v_∥/V (not 1×).
   - Deterministic ΔK_a ≈ 17.5 Hz/s (not 8.7).
   - σ_ΔKa ≈ 0.45 Hz/s (1σ).
   - Dwell T = 1/√(2σ) = **1.05 s**, giving ρ_a ≈ **1.26 m**, not 0.87 m.
   - Without the prior, T = 0.24 s and ρ_a ≈ 5.5 m.
   The **improvement ratio of about 4.4× survives** because it is independent of the factor, but the "sub-metre" marketing number does not.
3. **The velocity accuracy is optimistic.**
   - 20 µrad of relative pointing error equals 12.9 m at 645 km, i.e. **about 1.1 m/s** of velocity error across F1-F2, not 0.1 m/s.
   - Over open ocean there are no static features to register F1 against F2. The error budget therefore rests on gyro/star-tracker stability over 16.7 s (it needs ≤ 3 µrad), which typical SAR-smallsat ADCS does not reach.
   - Plume drift biases the centroid.
   Realistic σ_v is about 0.5-1 m/s, which shrinks the gain to about 2-3×.
4. **Body-steered SARs** (Capella, Umbra) re-slew the bus for every squint change, which also swings the TIR fields off the incoming ship queue. The "15-25 ships per 60 s" figure then falls to roughly 8-12 with 3 s slew and settle times. The TIR needs its own pointing or a wide field.
5. **Ship motion dominates sub-metre ship focus anyway.** Pitch, roll and yaw over 1 s cannot be addressed by a constant-velocity prior, and autofocus on bright ships usually works. That weakens the claimed "blind autofocus unreliable" problem.

**Mission / lifetime.** A 0.3 m-class cooled LWIR/MWIR payload of 30-60 kg and 30-80 W on a 100-150 kg SAR smallsat has several costs:
- a **cryocooler is a lifetime-limiting, microvibration-producing item** (typical MTTF 5-10 years with degradation);
- it competes with the SAR for power in eclipse;
- the added mass raises the ballistic coefficient, which slightly lengthens natural decay, so a deorbit plan at 550 km needs propulsion or a drag device to meet the 5-year rule.
A smaller uncooled microbolometer (60-100 m GSD) is the cheaper fallback, but it degrades σ_v further.

**Prior art (my searches)**
- GF-3NG moving-ship image improvement using simultaneous AIS, i.e. an external velocity prior applied in processing. https://doi.org/10.3390/rs13101951
- Hybrid SAR/ISAR refocusing: https://pmc.ncbi.nlm.nih.gov/articles/PMC7180630/
- Squint staring / sliding spotlight attitude and beam-steering frameworks: https://link.springer.com/article/10.1007/s42423-026-00212-x , https://www.mdpi.com/2226-4310/8/10/277
- Multi-satellite Doppler-rate velocity estimation with squinted geometry (EUCASS): https://www.eucass.eu/component/docindexer/?task=download&id=7237
- OptiSAR tip-and-cue: https://www.eoportal.org/satellite-missions/optisar
- US 4,546,355: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4546355

**Assessment.** Novel as a same-bus, seconds-latency, velocity-to-aperture-geometry control law. Claim 1 as drafted, "at least one of … Doppler-centroid setting / range-gate offset", is too broad: AIS-prior compensation plus tip-and-cue gets close. The independent claim should be limited to squint-nulling from the on-bus measured velocity vector, plus covariance-sized dwell. Hardware cost and the cryocooler limit its commercial reach.

---

### Candidate 6: Chronometric cooperative ground beacon

**Recomputed numbers**

| Quantity | Inventor | My check | Verdict |
|---|---|---|---|
| Line period at 0.75 m GSD | 106 µs | 0.75 / 7060 = 106 µs | OK |
| τ (8-stage TDI) | 850 µs | 850 µs | OK |
| Emitter intensity | 67 W/sr | 40 W over 2π(1 − cos25°) = 0.589 sr → 68 W/sr | OK |
| Irradiance at aperture | 9.6e-11 W/m² | 30·0.8/(5e5)² = 9.6e-11 W/m² | OK |
| Collected power | 6.5e-12 W | × 0.0962 m² × 0.7 = 6.47e-12 W | OK |
| Photon rate | 2.8e7 ph/s | 6.47e-12 / 2.34e-19 J = 2.77e7 ph/s | OK |
| Electrons per emitter | 14,100 e⁻ | × 0.6 × 850 µs = 14,100 e⁻ | OK |
| Daylight background | about 260 e⁻/px | about 195 e⁻/px (ρ = 0.1, SZA 40°, 40 nm at 850 nm) | Conservative |
| Emitter SNR | 103 | 14100/√(14100 + 1040 + 3600) = 103 | OK |
| V₁ (P = 2 ms) | 0.728 | sinc(0.425π) = 0.9723/1.335 = 0.728 | OK |
| σ_φ | 0.0133 rad | For a J-step estimator σ_φ = √(2/J)/(SNR·V) = 0.8165/(103·0.728) = 0.0109 rad. Reference noise is common-mode across the J ratios and drops out of the phase | Conservative |
| σ_t | 4.2 µs | 2 ms × 0.0109/2π = 3.5 µs | Conservative |
| Unwrap margins | 10σ, 5.2σ | 10σ, 5.2σ | OK |
| Decomposition example | 2.47 m + 2.0 m | 350 µs × 7.06 km/s = 2.47 m; 4 µrad × 500 km = 2.0 m | OK |

**Physics check of the key assumption.** In TDI, a point source's total collected energy (summed over all output lines it lands in) is integrated over [t_y, t_y + τ], where t_y varies continuously with the emitter's ground position. Sub-pixel phase therefore enters only through position, which the P3 layout correction handles. A symmetric along-track PSF does not bias the window centroid. **The core physics is sound.**

**Corrections**
1. **The claim that passive GCPs "cannot split" time from pitch is overstated.** An agile satellite can separate them using GCP collects at different pitch angles:
   - a pitch bias maps as H·δθ/cos²(pitch);
   - a time bias maps as v_g·δt, independent of pitch;
   - a time-tag error in attitude interpolation shows up as a residual proportional to angular rate during slews.
   ZY-3 and similar programmes calibrate time-sync error as a separate term (search results below). This is the main **design-around** and weakens the "problem nobody can solve" narrative. The beacon's real advantage is a *single pass, absolute, no-manoeuvre* measurement, plus exposure/TDI-stage verification.
2. **Electrical power.** 40 W of optical output at 850 nm needs about 100 W electrical per head at about 40% wall-plug efficiency, not 60 W. This is minor.
3. **Off-nadir passes** need tracking mounts. At ±25° beams, SNR falls off quickly beyond about 20° off-nadir.
4. **Night operation** needs laser/LED eye-safety analysis and light-pollution management. At 67 W/sr, the NIR hazard distance is non-trivial.

**Mission / lifetime.** No flight hardware. Zero impact on propellant, drag or deorbit, and the method helps recover timing after safe-mode resets. Best in class on this criterion.

**Prior art (my searches)**
- US 9,955,047, GNSS-controlled modulated LED for frame time-stamping. This is the closest art. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9955047
- Stellar-occultation timing: a GPS-driven LED flashed at each UTC second and **timing parameters recovered by modelling count levels** within an exposure. This is close to the "integrated energy encodes window timing" idea (single LED, not phase-stepped). https://arxiv.org/pdf/1005.3569
- QHY174-GPS built-in LED pulse calibration of exposure start/end to 1 µs: https://www.qhyccd.com/qhy174gps-imx174-scientific-cooled-camera/
- RE45452 / US 7,705,879, GPS-synchronized pulsed-source acquisition: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/RE45452
- ZY-3 time-sync and attitude constant-error calibration (evidence for the design-around): https://doi.org/10.3390/rs14051157 , https://www.tandfonline.com/doi/abs/10.1080/01431161.2017.1372858
- Point-source array geometric calibration: https://www.mdpi.com/2072-4292/15/16/4028

**Assessment.** The strongest technical robustness and the lowest risk of the six. It is a clean invention: phase-stepped, reference-normalised spatial emitters that make one integration window reveal its centre and its duration. The occultation LED art plus US 9,955,047 plus phase-shifting interferometry is a credible §103 combination, so non-obviousness is only moderate. The market is niche (cal/val service, geolocation certification) and enforcement is hard. Commercial value is the weak score.

---

## 3. Consolidated physics corrections

| Cand. | Inventor claim | Correction | Impact |
|---|---|---|---|
| 1 | K_eff = 2,400; σ = 0.017 / 0.009 px | K ≤ 1,024, about 512 per axis → σ ≈ 0.037 / 0.018 px (full band) | Moderate; still beats gyros |
| 1 | Closed loop plus deconvolution → 0.05 px residual, MTF 0.99 | Integer shifts cannot fix sub-pixel jitter; deconvolution restores MTF only with a noise penalty | Claims/spec need fractional accumulation |
| 1 | Digital TDI assumed | 10.8 Gsample/s per band and √N read noise; the charge-domain variant is unproven | Feasibility / enablement |
| 2 | 15 frames → σ_h 60 m, σ_u 1 m/s | Single-platform h-u degeneracy: σ_h ≈ 380 m, σ_u ≈ 6.3 m/s | **Critical** |
| 3 | ±26° triplet → σ_h 100-200 m, σ_v 0.5-1 m/s | Symmetric triplet is **exactly singular** for (h, u_along) | **Critical** |
| 3 | "Sun-side view hides shadows" is inventive | Known BRDF hot-spot effect | Weakens claim 4 |
| 4 | Forward-only thrust gives one-way phasing | Thruster-off already gives the other direction; visor = about 6 h of lead time | **Premise fails** |
| 4 | Recovery 0.022 kg Xe, "small" | Counter-flap doubles it (4.3 m/s per event); shield state doubles lifetime drag; 5-yr baseline is already 16.8 kg | **Lifetime hit** |
| 4 | Stuck visor needs fail-safe | Needs 11.6 mN at solar max, beyond typical EP; loss of mission | **Critical failure mode** |
| 5 | Forward squint 8° after F2 (6°) | Aperture centre (90 km ahead) comes before F2 (68 km ahead) | **Critical timing** |
| 5 | ΔK_a = K_a·v/V_g | ΔK_a ≈ 2K_a·v/V → T = 1.05 s, ρ_a = 1.26 m | Numbers; ratio kept |
| 5 | σ_v 0.3 m/s | 20 µrad relative pointing alone gives about 1.1 m/s; no static features at sea | Gain about 2-3×, not 4.4× |
| 6 | σ_t 4.2 µs | 3.5 µs (inventor conservative) | Positive |
| 6 | GCPs cannot split time and pitch | Multi-pitch or slew-rate GCP collects can | Design-around exists |

---

## 4. Final ranking and recommendation

| Rank | Candidate | Total | One-line verdict |
|---|---|---|---|
| 1 | **6: Chronometric beacon** | 43 | Sound physics, zero flight risk, clean claimable construct. Niche market and moderate §103 risk. |
| 2 | **1: CC-TDI** | 38 | Most valuable IP (sensor-ASIC licensing, hard to replicate). Numbers need correcting. Charge-domain enablement is the key gap. |
| 3 | 5: TIR→SAR | 31 | Novel control law, but a field-timing flaw and heavy SWaP. Keep as a second-tier filing after the redesign. |
| 4 | 2 (+3 merged): 3D cloud LOS threading | 31 / 24 | One invention. Estimation physics broken as described. Refile as one merged application after the shadow/NWP fix. |
| 6 | 4: VLEO visor | 20 | Premise fails; lifetime-negative; anticipated by D3. Drop. |

### Top 2 recommended for refinement

**A. Candidate 1 (CC-TDI), recommended for commercial value**

Engineering fixes:
1. Correct the noise budget to K = 1,024 with per-axis information (0.037 / 0.018 px full band; 0.014 / 0.007 px in 1 kHz). Add a Monte-Carlo with real Pleiades/WorldView texture statistics and row PRNU of 0.1-0.5%.
2. Replace integer-address closed loop with **fractional-pixel weighted accumulation** (bilinear split of each stage sample between neighbouring accumulators). This is the only way the loop helps sub-pixel jitter. Report restored MTF *with* the noise penalty.
3. Enable the charge-domain embodiment: a CCD-in-CMOS dual-register gate layout, charge-transfer-efficiency and dark-current budget, and a sensing-column-only implementation. Alternatively, commit to hybrid digital TDI with a sensing-row readout and state its power cost (about 10.8 GS/s per band at 64 stages).
4. Define the gyro fusion crossover and fallback over low-texture scenes. Keep the isolator requirement relaxed but not deleted.

Claim fixes:
- Independent claim: keep (c) balanced code + (d) sliding-window convolution model + (e) inversion to a sub-window trajectory. **Add "the code having no spectral null in a predetermined jitter band"** to distinguish e2v's split-half. Move per-stage gain equalisation into claim 1 or claim 2.
- Broaden "binary ±1" to "weights of a multi-level balanced code". Add a claim on **fractional-pixel accumulation driven by the estimate**.
- Add an apparatus claim directed at the **sensor chip itself**: code register + coded accumulator + D output. This is the licensable unit and makes infringement detectable from datasheets.
- Add a claim covering the D stream being output off-chip, so FPGA-side implementations are captured.
- Read the e2v US 9,967,490 claims in full before filing.

**B. Candidate 6 (Chronometric beacon), recommended for technical soundness and zero mission risk**

Engineering fixes:
1. Recompute σ_φ with the J-step formula (3.5 µs). Show that reference-emitter noise is common-mode for phase.
2. Budget 100 W electrical per head. Add a tracking-mount or multi-beam option for off-nadir passes up to 30°, and an eye-safety/NOHD analysis.
3. Add a detector linearity and saturation plan (intensity scheduling from predicted range and gain).
4. Quantify the advantage over multi-pitch GCP separation (single pass, no manoeuvre, absolute time, TDI stage count) to pre-empt the design-around.

Claim fixes:
- Merge claim 1(e) with claim 7 (time-versus-pitch decomposition) as the fallback independent claim, as the inventor suggests.
- Keep "phase-stepped **spatially separate** emitters, **normalised by a co-imaged reference**, **within a single integration window**" in claim 1. That is the distinction over the occultation-LED art and US 9,955,047.
- Broaden the waveform to "periodic, pseudo-random or chirp codes with known integrated response" to close the PN-code design-around.
- Add claims for: TDI stage-count/exposure verification from visibility (claim 3, promoted); the rolling-shutter row-skew variant; and **onboard clock disciplining** from the result, which gives a satellite-side infringement hook.
- Cite arXiv:1005.3569 (occultation LED count-level timing) to the examiner proactively.

**Honourable mention.** The merged Candidate 2+3 is worth a provisional *only after* the estimation fix:
- height from the cloud-shadow offset (wind-free), along-track wind from an NWP or GEO-AMV prior, or ≥ 60° look-ahead;
- an independent claim on "selecting the acquisition time of a fixed target from LOS-segment/3D-cloud intersection with a 3D field from any source".

**Drop Candidate 4.** Its premise fails, its sole benefit equals about 6 h of lead time, D3 anticipates the method claim, and it has a mission-ending stuck-deployed failure mode at solar max.
