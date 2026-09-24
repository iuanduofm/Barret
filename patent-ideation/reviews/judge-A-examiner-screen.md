# Judge A: Examiner Screen of Six Candidate Inventions

Reviewer role: primary examiner (AU 3661/3663 spacecraft, 2400-series imaging), with a physics PhD in remote sensing.
Date: 2026-09-24
Scope: inventor-1 to inventor-6 in `patent-ideation/candidates/`. Inventors 2 and 3 are assessed together.

**Search caveat.** I ran my own web searches for each candidate (about 45 queries in total). This environment blocks full-text access to patents.google.com, USPTO ppubs, arxiv.org, freepatentsonline and ai.jpl.nasa.gov. The characterisations of patents below therefore rest on search-engine abstracts and snippets. Before any filing, someone must read the full text of every reference marked **[FT]**.

---

## 1. Score table

Scores run from 1 to 10, where 10 is best for the applicant. "Lifetime" is mission/orbital lifetime and operational sustainability. The weighted score uses N 0.20, O 0.25, 101/112 0.10, F 0.15, L 0.15, C 0.15.

| # | Candidate | Novelty (102) | Non-obvious (103) | 101 / 112 | Feasibility | Lifetime | Commercial / breadth | **Weighted** | Rank |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Complementary-Coded TDI (CC-TDI) jitter sensing | 7 | 6 | 8 | 6 | 9 | 7 | **7.0** | **1** |
| 6 | Chronometric ground beacon (time-tag vs pitch) | 6 | 4 (5 once amended) | 7 | 7 | 9 | 4 | **5.9** | **2** |
| 5 | TIR kinematic pre-look for motion-matched SAR | 6 | 4 | 8 | 6 | 6 | 6 | **5.7** | 3 |
| 2 | Onboard 3D cloud gap threading (single satellite) | 5 | 3 | 7 | 5 | 7 | 6 | **5.2** | 4 |
| 4 | VLEO ram visor plus target-driven drag steering | 6 | 4 | 7 | 6 | 3 | 4 | **4.9** | 5 |
| 3 | Constellation-shared 3D cloud field (leader to follower) | 5 | 4 | 7 | 4 | 5 | 5 | **4.8** | 6 |
| 2+3 | *Merged 2+3 application (recommended if pursued)* | 5 | 4 | 7 | 6 | 6 | 6 | *~5.5* | (alt.) |

**Summary.** CC-TDI is the only candidate I would expect to reach allowance with claims of commercially meaningful breadth. The beacon (6) and the TIR-cued SAR (5) are close for second place. I pick 6 because its §103 position can be repaired by claim amendment, whereas 5's §103 problem comes from decades of airborne same-platform cross-cueing. If the business weights commercial value above allowance odds, swap 5 in for 6.

---

## 2. Inventors 2 and 3 converged on the same idea. Does that signal obviousness?

**Yes. It is a warning sign, but weak evidence in the legal sense.**

- **The case law.** Independent, near-simultaneous invention by others can be evidence of the level of ordinary skill and can support a conclusion of obviousness. See *Concrete Appliances v. Gomery*, 269 U.S. 177 (1925); *Ecolochem v. S. Cal. Edison*, 227 F.3d 1361 (Fed. Cir. 2000); *Geo. M. Martin Co. v. Alliance Mach.*, 618 F.3d 1294 (Fed. Cir. 2010). Two members of one ideation program reached "use h·tanθ parallax to choose *when/from where* to look through broken cloud" within hours of each other. That tells me the key insight is reachable from public art (MISR stereo, h·tanθ parallax, preview cameras, agile scheduling) with ordinary skill.
- **Why the evidence is weak.** Both inventors worked from the same brief, in the same session, from overlapping public sources. They are not independent members of the art, and their convergence is not prior art. An examiner would not see it. A litigation defendant could discover the internal ideation records, however, so it should be assumed to be discoverable.
- **The substantive problem is separate from the convergence.** The conceptual step, that whether a line of sight is cloud-free depends on view angle, is itself old art:
  - RAND's CFLOS calculations: https://www.rand.org/pubs/papers/P4883.html
  - AFRL/EUMETSAT PCFLOS, tabulated at nine 10° view-angle increments and 20 altitude levels: https://www-cdn.eumetsat.int/files/2020-04/pdf_conf_p59_s2_06_reinke_v.pdf
  - CALIPSO-derived PCFLOS (2025): https://www.spiedigitallibrary.org/journals/journal-of-applied-remote-sensing/volume-19/issue-02/028503/Global-probability-of-a-cloud-free-line-of-sight-and/10.1117/1.JRS.19.028503.full
  - US 9,126,700 already uses preview cameras at several nadir angles to decide "which target images should be acquired in which particular sequence **and when the target image acquisition should start**" (search abstract of WO2011089477A1: https://patents.google.com/patent/WO2011089477A1/en) **[FT]**.
- **Recommendation.** If the concept is pursued at all, file **one** application naming both inventors. Embodiment A is the single-satellite look-ahead (inventor 2). Embodiment B is the leader-follower crosslink (inventor 3). Two separate same-day filings on overlapping subject matter would invite obviousness-type double-patenting rejections and terminal disclaimers for no gain.

---

## 3. Per-candidate findings

### Candidate 1: CC-TDI (complementary-coded stage accumulation)

**My prior-art search**

- **EP 2 954 671 B1 / US 9,967,490 (Teledyne e2v)** [FT]. https://patents.google.com/patent/EP2954671B1/en
  - The pixel matrix is split *along the columns* into sub-matrices Ma and Mb, each partially summed.
  - Offset column groups are compared, and "the group pair that provides the signals nearest to each other determines the probable shift".
  - The partial sums add up to the full N-row sum.
  - This teaches the *N=2 contiguous-code* special case of CC-TDI, including "no light lost". It is the principal §103 reference.
- **US 9,374,540**, multi-register-bank digital TDI (several accumulation registers per row). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9374540
  - This makes the dual-accumulator hardware of claim 2 a known element.
- **Applied Optics 61(16):4655 (2022)**, "Dynamic PSF-based jitter compensation … considering terrain relief and the TDI effect". https://opg.optica.org/ao/abstract.cfm?uri=ao-61-16-4655
  - It builds a per-line dynamic PSF from estimated jitter *including the TDI multistage effect*.
  - This **anticipates dependent claim 11** in substance. Claim 11 adds no patentable weight.
- **ISPRS 2022 TDICCD jitter paper** (a jitter inversion model with the TDI effect): https://isprs-archives.copernicus.org/articles/XLIII-B1-2022/79/2022/
- **ZY-3 tri-band relative residuals**: https://www.sciencedirect.com/science/article/abs/pii/S0924271619302497
- **Complementary (Golay-pair) flutter sequences for motion deblurring** (Optics & Laser Technology, 2019): https://www.sciencedirect.com/science/article/abs/pii/S0030399219321978
  - This teaches *complementary* temporal codes.
  - It weakens the "complementary is non-obvious" argument, although it still blocks light in each frame and aims to deblur, not to measure.
- **US 7,164,810 / US 7,668,406**: real-time, image-based velocity and jitter estimation in FPGA hardware feeding line-scan compensation. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7164810 , https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7668406
  - Industrial line-scan, not satellite, but it covers the "onboard closed-loop from image data" element.
- **Not found:** balanced pseudo-random ±1 stage weighting, a sliding-window deconvolution of the code to a line-rate trajectory, or multi-code interleaving with a spectral-null-free design. Searches for Hadamard/coded TDI and coded-exposure TDI returned nothing on point.

**§102.** Not anticipated as claimed. e2v lacks non-contiguous balanced codes, the sliding-window convolution inversion and multi-code interleaving. **7.**

**§103.** The likely rejection is **e2v (EP 2 954 671) in view of Raskar (coded exposure, ACM TOG 2006) and the Golay complementary flutter art**. The rationale would be: "replacing a contiguous 2-segment partition with a pseudo-random partition to improve the frequency response is a known technique to improve a similar device (*KSR*, rationale C/D)". Dependent claims 8, 9 and 11 fall to the addition of the AO 2022 dynamic PSF and standard gyro complementary filtering.

The applicant's best rebuttals are:
- The e2v split-half code has hard spectral nulls (441 Hz in the example). Reaction-wheel and cryocooler lines routinely fall there. Showing this would be an *unexpected result*, but only if backed by data.
- Tendero/Morel/Rougé teach away from temporal coding for satellites.
- The sliding-window *convolution* structure, which yields a trajectory rather than a single shift, is not suggested by e2v.

**6.**

**§101/§112.** The claims are eligible: they are a specific sensor architecture operating on physical signals, a practical application (*McRO*; *Thales v. US*). Enablement is good for digital-domain TDI. Claim 13 (charge-domain dual register) has an enablement/written-description weakness because no pixel or transfer-gate design is disclosed. "Balanced", "substantially zero" and "sensing columns" need definitions in the specification. **8.**

**Feasibility (recomputed).**
- **Signal level.** Pan radiance of about 20 W m⁻² sr⁻¹ (ρ≈0.2) at f/11 with optics transmission 0.7 gives focal-plane irradiance of about π·20·0.7/(4·121) ≈ 0.091 W m⁻². On a 5.5 µm pixel that is 2.75 pW, or about 4×10⁶ e⁻/s at QE 0.5. Over 70.8 µs that is **~290 e⁻/stage**. The inventor's 150 e⁻ is conservative. **OK.**
- **Jitter MTF.** exp(−2π²·0.09·0.25) = **0.64**. **OK.**
- **Averaging count is inflated.** The inventor's K_eff = 2,400 double-counts columns: "2 gradient axes" means 2 unknowns, not 2 measurements. The maximum is K ≤ 1,024.
  - Worst case: 0.83/√1024 = **0.026 px** per 70.8 µs sample (inventor: 0.017).
  - With a realistic *median* gradient of 5–10 %/px instead of 20 %, g ≈ 8–15 e⁻, which is 2–4× worse. That gives **~0.05–0.1 px** at full bandwidth, or **~0.02–0.04 px** in a 1 kHz band.
  - This is still useful (it beats gyros above about 50 Hz), but the "6 nrad" headline is not supportable.
- **Low-frequency observability.** Σw = 0 forces W(0) = 0. Near DC, |W| ≈ 2πfΔt·|Σ i·w_i|. For a random balanced 64-code, |Σ i·w_i| ≈ 150, so |W(20 Hz)| ≈ 1.3, consistent with the inventor's ≥1.6. **OK**, but gyro fusion is mandatory below about 20 Hz.
- **Row PRNU.** Row PRNU mismatch of about 0.1 % creates a scene-proportional false D. This needs quantification against real TDI row-gain maps.
- **Linearisation.** The first-order model needs residual motion well below 0.5 px inside the window. The closed loop is therefore a *precondition*, not an option.

**6.**

**Lifetime.** There is no propellant, drag or orbit impact. The added load is under 1 W and about 1.3 Mbit of SRAM. It is mildly positive: it may let a 2–5 kg microvibration isolator be deleted, which lowers mass. At VLEO, lower mass means a higher ballistic coefficient and longer decay life. A secondary benefit is wheel-health telemetry for predicting wheel failures, which are the most common life-limiting ADCS failures. The only failure mode is a code-memory SEU corrupting D, which is benign because S is unaffected. **9.**

**Commercial value and breadth.** There is a licensing path to detector vendors (e2v, Gpixel, ams). Design-arounds a competitor could try:
- (a) Read out K ≈ 4–8 contiguous partial sums and combine them off-chip with zero-sum weights. This is not literally a "coded accumulator" per stage, so the claims must cover it.
- (b) Use ternary weights {+1, 0, −1}.
- (c) Use the e2v contiguous split with several offsets.

(a) and (b) are closable by drafting. (c) stays free to use. **7.**

---

### Candidate 6: Chronometric cooperative ground beacon

**My prior-art search**

- **Image Engineering LED-Panel / ISO 15781 camera timing** ("running light" LED arrays that show exposure time and shutter lag in a *single* frame). https://www.image-engineering.de/products/equipment/measurement-devices/900-led-panel ; https://www.image-engineering.de/en/resources/blog/timing-measurements/ ; https://www.imatest.com/product/camera-timing-system-led-panel/
  - This is **new and important art the inventor missed**. It measures exposure start and duration from one image of time-coded LEDs.
  - It damages the novelty of dependent claim 3 (exposure duration from the image) and supplies the "single-window timing" concept for §103.
- **CN103676453A**: pulse sequences light a high-speed LED array at set intervals to measure camera shutter delay. https://patents.google.com/patent/CN103676453A/en [FT]
- **US 9,955,047** (GNSS-controlled modulated LED gives image time stamps; the inventor's #1) and **US 7,705,879 / RE44604** (GPS-synchronised pulsed beacons): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7705879
- **GF-7 laser-footprint camera**: time-synchronous imaging of laser spots, used for on-orbit geometric calibration. https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ipr2.12306 ; IR-detector and CCR ground arrays for laser altimeter calibration: https://www.tandfonline.com/doi/full/10.1080/17538947.2023.2220617
- **LAPAN-A3** (arXiv:1901.09189) documents the time-error/pitch-misalignment confound. https://arxiv.org/pdf/1901.09189
  - This is *motivation to combine*, which cuts against the applicant: the problem was known, so an examiner will say a skilled person had reason to look for a timing reference.
- **Continuous-wave time-of-flight 4-phase demodulation** (for example Lange & Seitz, IEEE JQE 2001) is textbook J-step phase recovery from integrated, phase-stepped windows. It is the analogous-art source for the atan2 estimator.

**§102.** Not anticipated. No reference combines phase-stepped, reference-normalised point emitters imaged from orbit with a GNSS-absolute mid-exposure time and a time-tag/pitch split. **6.**

**§103.** As drafted, claim 1 is **likely rejected** over **US 9,955,047 (GNSS-disciplined modulated LED gives absolute image time) in view of the ISO 15781 LED-Panel (single-frame exposure timing from time-coded emitters) and SPARC/point-source arrays (US 8,158,929; Remote Sens. 15(16):4028) for orbital point-source geometry**, with CW-ToF phase-stepping as the known phase estimator. The claim is currently drafted as generic "time-tag error determination", and that is what the combination reaches.

The strongest non-obvious hook is **claim 7**: splitting the along-track residual into a time-tag part and a pitch part from one pass, using the absolute mid-exposure time. It is not in the independent claim yet. **4 as drafted, about 5–6 if amended.**

**§101/§112.** Claim 1 recites physical emitters, orbital acquisition and a measurement, which is eligible as a measurement technique. A processing-only "service" claim, where a customer supplies images, would face *Electric Power Group* risk. Two §112 issues:
- Claim 3 (TDI stage count from visibility) is confounded by the along-track system MTF, so the specification must disclose the correction.
- "Mutually separable" is indefinite without a spacing or PSF criterion.

**7.**

**Feasibility (recomputed).**
- **Photon budget.** 30 W/sr × 0.8 / (5×10⁵ m)² = 9.6×10⁻¹¹ W/m². Multiplying by 0.096 m² and 0.7 gives 6.45×10⁻¹² W, or 2.76×10⁷ photons/s at 850 nm. With QE 0.6 over 850 µs that is **≈14,050 e⁻**, which matches the inventor's 14,100.
- **Timing precision.** SNR ≈ 100 gives σ_t ≈ 4 µs, which is plausible for photon noise alone.
- **Missing error term: atmospheric scintillation.** Emitters 4 m apart look through *decorrelated* near-ground turbulence. Over one 0.85 ms window the intensity fluctuations are not common-mode, so the ratio does not cancel them. At the few-percent level they exceed the 1 % photon noise and could degrade σ_t to about 5–15 µs. That is still far below millisecond-class time-tag errors, so the concept survives, but the "cancels atmosphere" statement is wrong as written.
- **Visibility.** V is the system along-track temporal MTF, not just sinc(πτ/P). For P = 2 ms at 0.75 m GSD the extra factor is about 0.99, so this matters only for the τ/stage-count dependent claim.
- **Beam geometry.** A ±25° beam supports only near-overhead passes unless a tracking mount is added. Daylight SNR is adequate. Small-aperture cubesats are about 15× worse, which is still usable.

**7.**

**Lifetime.** Ground segment only, with no vehicle impact. It is mildly positive for fleet sustainment, because it detects clock/PPS faults after safe-mode events without flight hardware. **9.**

**Commercial value and breadth.** The market is niche: calibration service providers, cal/val agencies and high-accuracy geolocation certification. Easy design-arounds:
- A single emitter with a GNSS-timed on/off *edge* plus a constant reference (not a "phase-stepped group").
- PN codes.
- The running-light approach.

The claims must be broadened to "known time-varying waveforms" or they will be designed around the same day. **4.**

---

### Candidate 5: TIR kinematic pre-look for motion-matched SAR

**My prior-art search**

- **GA-ASI Lynx multi-mode SAR/GMTI.** An operator selects a GMTI target and **automatically cross-cues** to an EO/IR sensor on the *same airframe*. Spotlight SAR runs on the same platform. https://www.ga-asi.com/radars/lynx-multi-mode-radar ; NATO Unified Vision 2012 trial: https://www.osti.gov/servlets/purl/1115669
  - Same-platform, seconds-latency cross-cueing between SAR and EO/IR is old in the airborne art. The inventor's "cue direction reversed" argument is weak, because cross-cueing runs in both directions in these systems.
- **SAR plus AIS onboard one microsatellite constellation** (SPIE 8537, 2012). https://ui.adsabs.harvard.edu/abs/2012SPIE.8537E..10P/abstract
  - An on-bus kinematic sensor paired with SAR. Its fusion is post-hoc, not used for acquisition control.
- **CN111474545A**: AIS-based ship position calculation **and refocusing** in SAR images, i.e. an external velocity prior used for moving-ship focusing. https://patents.google.com/patent/CN111474545A/en [FT]
  - This squarely hits dependent claim 8.
- **High-squint SAR imaging of maritime ship targets** (IEEE TGRS 2020) and BIT high-squint noncooperative ship imaging: https://www.researchgate.net/publication/347178371_High-Squint_SAR_Imaging_of_Maritime_Ship_Targets ; https://pure.bit.edu.cn/en/publications/high-squint-sar-imaging-for-noncooperative-moving-ship-target-bas/
- **US 7,106,243**: enhanced 2D imaging of ground moving targets. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7106243
- **SDGSAT-1** coordinated multi-payload TIR observation on one bus: https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2532781
- **ICEYE tip-and-cue** (moving-object velocity and trajectory uncertainty explicitly considered in cueing): https://www.iceye.com/blog/tip-and-cue-technique-for-efficient-near-real-time-satellite-monitoring-of-moving-objects
- **Not found:** a squint *chosen to null the target's radial velocity* from an a-priori velocity, or dwell sized to velocity covariance.

**§102.** Not anticipated. **6.**

**§103.** The likely rejection is **Lynx (same-platform EO/IR↔SAR cross-cue) in view of the SAR+AIS microsat (SPIE 2012; orbital on-bus kinematic sensor) and Heiselberg 2019 (velocity from along-track time-lagged looks), with CN111474545A for velocity-prior focusing**. Claim 1 as drafted lets the SAR parameter be any of five items, including "Doppler-centroid setting" and "range-gate timing offset". An examiner would call those routine uses of known velocity. Claims 3 (radial-velocity-nulling squint) and 4 (covariance-sized dwell) are the only hooks. **4.**

**§101/§112.** Strong: this is physical radar control. The §112 issue: the dwell law as written (T = 1/√(kσ)) uses the wrong FM-rate sensitivity (see below). An error in the specification's core formula invites a written-description and enablement challenge to the numerical dependent claims. **8.**

**Feasibility (recomputed).**
- **Geometry checks.**
  - Δt = (645·tan16° − 645·tan6°)/7.0 = (185 − 68)/7.0 = **16.7 s**. OK.
  - TIR spot: 1.22·10 µm/0.3 m = 40.7 µrad, or **26 m** at 645 km. OK.
  - Azimuth displacement: 645 km × 1.78/7300 = **157 m**. OK.
  - Squint ≈ atan(90/645) = **7.9°**. OK.
- **Physics error.** The inventor uses ΔK_a ≈ K_a·v_∥/V_g. For a target moving along track, the relative velocity term gives ΔK_a/K_a ≈ −v_a(1/V_s + 1/V_g) ≈ **−2v_a/V_eff**, which is about 2× the inventor's value.
  - Corrected: ΔK_a ≈ 17 Hz/s and σ_ΔKa ≈ 0.45 Hz/s (1σ).
  - At 2σ with QPE ≤ π/4: T ≈ 1/√0.9 ≈ **1.05 s**, giving ρ_a ≈ **1.3 m** (inventor: 0.87 m).
  - Without the prior, T ≈ 0.24 s and ρ_a ≈ 5.4 m. The ~4× *ratio* survives, but the absolute sub-metre claim does not.
- **Strawman baseline.** Ships are usually bright, point-like scatterer clusters. PGA and minimum-entropy autofocus routinely recover the quadratic phase post hoc from a *long* aperture that was collected anyway. The real, unrecoverable losses are narrower:
  - Doppler folding outside the PRF band.
  - A target leaving a *small* staring spot. A 12 m/s ship moves about 310 m in 26 s, which matters only for sub-km staring spots.
- **Other limits.**
  - TIR sees nothing under cloud (60–70 % of the ocean).
  - Small-vessel pixel contrast is about 0.5–1 K at 26 m GSD, not ≥1.5 K.
  - Plume offset cancels in the displacement if it is steady, which is a point in the inventor's favour.

**6.**

**Lifetime.** A cooled MWIR/LWIR focal plane needs a **cryocooler**, typically rated 5–10 years, which is often the life-limiting unit. The cooler also adds microvibration to the SAR bus. Per-target squint slews (body-steered on many smallsat SARs) add CMG/wheel cycles. At 550 km the drag life is fine, but the added TIR mass and area slightly shortens natural decay life. FCC 5-year deorbit compliance still needs propulsion or a drag device for a heavier bus. **6.**

**Commercial value and breadth.** There is a real defence and maritime-domain-awareness market. Design-arounds: use AIS (the independent claim is TIR-limited) or daytime optical for the pre-look; use ground-computed parameters. Broaden to "passive pre-look sensor on the same spacecraft". **6.**

---

### Candidate 2: Onboard 3D cloud gap threading (single satellite)

**My prior-art search**

- **US 9,126,700 / WO2011089477A1**. Several forward preview cameras at different nadir angles; the system decides which targets, in what sequence, **and when acquisition should start**. https://patents.google.com/patent/WO2011089477A1/en [FT]
  - The inventor's characterisation ("only which targets") understates it.
- **JPL Dynamic Targeting, flown on CogniSAT-6 (2025)**: https://arxiv.org/abs/2509.05304 ; DT ASTRA-2025 extended abstract: https://ai.jpl.nasa.gov/public/documents/papers/DT-Astra-2025-Extended-Abstract.pdf [FT]
  - Also GEO-supplemented DT with hierarchical planning (35 min of lead): https://arxiv.org/abs/2603.06719
  - Also "Improving Cloud Observations by Autonomously Pointing Satellites": https://www.researchgate.net/publication/397978996_Improving_Cloud_Observations_by_Autonomously_Pointing_Satellites
- **Autonomous mission planning based on onboard cloud detection** (Adv. Space Res. 2022): https://www.sciencedirect.com/science/article/abs/pii/S0273117722005816
- **PCFLOS by view angle and altitude** (Reinke/EUMETSAT; RAND P-4883; CALIPSO 2025), as cited in §2.
- **Multi-view 3D cloud geometry**: RSE 2005 https://www.sciencedirect.com/science/article/abs/pii/S0034425705003081 ; MISR 3D cloud volume https://airbornescience.nasa.gov/content/Three-Dimensional_Cloud_Volume_Reconstruction_from_the_Multi-angle_Imaging_SpectroRadiometer ; US 9,001,311 (parallax cloud height).

**§102.** Probably novel in the specific LOS-slab-segment test plus onboard time selection. It is at risk if the full text of US 9,126,700 discusses view-angle-dependent occlusion. **5.**

**§103.** The likely rejection is **US 9,126,700 (multi-nadir-angle preview; choose acquisition start) in view of MISR/US 9,001,311 (cloud height from parallax) and Reinke PCFLOS (occlusion depends on view angle and cloud altitude), with CogniSAT-6 DT for onboard NN look-ahead re-pointing**. The skilled person had the motivation (cloud loss), the tools, and a reasonable expectation of success (*KSR*, predictable use of prior-art elements according to their established functions). The convergence of inventors 2 and 3 reinforces this. **3.**

**§101/§112.** The claims survive Step 2A prong 2 because they command attitude and acquisition. The §112 problem is cloud-base altitude: the specification offers four heuristics and no validated method. Claim 1 *requires* a base altitude, which invites an enablement attack on the "including when a nadir projection covers the target" limitation. **7.**

**Feasibility (recomputed; this is the key finding).**
- **Height and wind are not separable from one forward camera.** In flat-Earth geometry, tanθ(t) = D(t)/H is *linear* in time. The disparity model h·tanθ + u·t is therefore degenerate in (h, u). Only Earth curvature (a few percent at 30–50° VZA) breaks the degeneracy.
- I computed the least-squares covariance for the inventor's own case: 15 frames over 37 s, VZA 50→30°, σ = 6 m, spherical Earth. The result is **σ_h ≈ 580–590 m and σ_u ≈ 9.5 m/s**, against the inventor's claimed 60 m and 1 m/s. The condition number is about 1.3×10⁴. Dependent claim 3's premise ("non-proportional variation of tanθ") is physically weak at these angles.
- **This is not fatal for inventor 2, and the reason is worth a claim.** The same satellite later views the same target along the *same* tanθ(t) law, so the degenerate combination cancels in the prediction. The predicted along-track LOS crossing of the cloud-top layer comes out at **σ ≈ 2 m (t = −61 s), 26 m (nadir) and 54 m (+61 s)**. With a 1.5 m/s NWP or GEO-AMV wind prior this drops to 2, 8 and 17 m, and σ_h falls to about 90 m.
  - Absolute h is still needed for the slab-thickness term and for cross-track offsets.
  - Cloud-shadow offset gives h *independently of wind*, because cloud and shadow advect together. That is the correct fix.
- **Other points.**
  - Cumulus lifetimes of 5–15 min and side-wall occlusion at 40° make the "3 independent looks gives P = 0.875" estimate optimistic. Expect about 1.2–1.4× yield, not 1.5×.
  - The resource figures (3 W camera, 8 W processing) are plausible.

**5.**

**Lifetime.** More off-nadir and late-retargeted collections mean more slew/settle cycles, which increases CMG and wheel wear (their bearings are life-limiting). The always-on look-ahead camera plus 8–11 W of processing increases battery depth of discharge. There is no drag or propellant impact at 500 km. **7.**

**Commercial value and breadth.** The technique could be retrofitted by software. Design-arounds:
- A ground-computed schedule.
- A GEO/NWP 3D cloud field instead of look-ahead stereo.
- Cloud-top only with base = 0.

The independent claims must not require "trained segmentation model" or "cloud-base altitude". **6.**

---

### Candidate 3: Constellation-shared advected 3D cloud field

The prior art is as for candidate 2, plus:
- UrtheCast OptiSAR CloudCam (leader streams 2D cloud maps to a trailing optical satellite): https://www.eoportal.org/satellite-missions/optisar
- The IAI IL276014 family. I could not retrieve it: Google Patents and the Israeli register are blocked here, and web search returned no US/WO equivalent. **[FT], mandatory.**
- For the shadow claims: cloud-shadow projection from view and sun geometry is standard. See Sentinel-Hub "Projecting cloud shadows from clouds" (https://medium.com/sentinel-hub/projecting-cloud-shadows-from-clouds-c2fd2263139d), Remote Sens. 16(21):3950 (https://doi.org/10.3390/rs16213950), cloud base from shadows Remote Sens. 18(1):147 (https://doi.org/10.3390/rs18010147), and Sentinel-3 stereo CTH for shadow detection (https://www.sciencedirect.com/science/article/pii/S0924271621002458).

**§102.** Probably novel as a combination. The IAI full text is an unquantified risk. **5.**

**§103.** The likely rejection is **IAI IL276014 or OptiSAR (leader cloud data → follower over a link) in view of US 9,126,700 (select acquisition start from multi-angle preview), MISR (height plus motion from fore/nadir/aft) and Reinke PCFLOS (view-angle-dependent CFLOS)**, with the shadow projection art for claims 3 and 15. The one element I found no art for is **choosing view azimuth ≈ solar azimuth so that shadows hide behind the clouds that cast them (claim 4)**. That is the best hook of the 2/3 family. **4.**

**§101/§112.** As for candidate 2. Divided infringement across two satellites plus ground is a real enforcement issue. **7.**

**Feasibility (recomputed).**
- **The symmetric three-look design cannot separate height from wind.** For fore, nadir and aft heads at ±26° off-nadir, the along-track parallax term is an odd function of time. With three looks, the (x₀, h, u) system is **exactly singular**: I computed it numerically.
- The inventor's "σ_h 100–200 m, σ_v 0.5–1 m/s" is therefore unsupported by the geometry.
- **The 120 s leader-follower lag makes it worse.** Unlike the single-satellite case, the degenerate direction does *not* cancel, because the follower's tanθ(t) is time-shifted. The advection error is about σ_u·Δt_lead, which exceeds 1 km without an independent wind or height source. Viable fixes:
  - shadow-based height;
  - MISR-like wide asymmetric angles (up to 60–70°);
  - an NWP/AMV wind prior.
- **The simulated benefit is small.** Visible-and-sunlit fraction is 0.29 against 0.23 for the nadir rule, from a toy model, and it is sensitive to the errors above.

**4.**

**Lifetime (the main weakness).** The concept needs a scout in the same plane with a 1–10 min lead.
- A small scout has a different ballistic coefficient from the follower. At 500 km a differential acceleration of about 3×10⁻⁷ m/s² produces an along-track drift of about 1.5·Δf·τ² ≈ **2,000 km per month**, so the 425–4,200 km slot is lost within weeks without propulsion or differential-drag management.
- The scout needs propellant for phasing and deorbit, and its own solar-maximum decay budget.
- Each extra spacecraft is another failure point: loss of the scout degrades the whole chain.

**5.**

**Commercial value and breadth.** A design-around is to use a GEO- or NWP-assimilated 3D cloud product with no partner stereo (the inventor admits this). The value depends on building scout infrastructure. **5.**

---

### Candidate 4: VLEO ram visor plus target-driven drag steering

**My prior-art search**

- **"Drag-based orbit phasing through attitude and articulation control"** (Acta Astronautica, 2021). It uses articulating solar arrays so that "array pointing can be decoupled from the main payload pointing", i.e. **drag modulation while the payload keeps operating**. https://www.sciencedirect.com/science/article/abs/pii/S0094576521004069
  - This directly undercuts the inventor's main distinction from Planet ("existing methods leave the imaging attitude").
- **Omar and Bevilacqua et al., "Atmospheric Interface Reentry Point Targeting Using Aerodynamic Drag Control"** (JGCD). Drag modulation to hit a chosen *ground-track point*, which is the target-absolute use of drag timing. https://arc.aiaa.org/doi/10.2514/1.G000884
- **Ground-track control using differential drag** (JSR, doi:10.2514/1.A35256): https://arc.aiaa.org/doi/10.2514/1.A35256
- **Planet differential drag**: https://arxiv.org/pdf/1806.01218 ; https://arc.aiaa.org/doi/abs/10.2514/1.A33927
- **VLEO aerodynamic control surfaces** (DISCOVERER; anti-saturation logic for aero actuators): https://discovery.ucl.ac.uk/id/eprint/10120598/ ; https://deimos-space.com/discoverer-aerodynamic-control-earth-observation/ ; differential lift/drag design optimisation: https://arxiv.org/pdf/2303.16612
- **Exo-Brake, an actively modulated drag device targeting a location**: https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/

**§102.** No single reference shows a ram-side aperture visor plus a pitch-balancing counter-flap plus a per-target timing planner. **6.**

**§103.** The likely rejection is **Omar/Bevilacqua (drag timing to reach a ground point) in view of the Acta Astronautica 2021 decoupled articulating drag surfaces (payload keeps pointing) and DISCOVERER/SOAR aero surfaces, with telescope doors and baffles for the AO/stray-light function**.
- Balancing pitch moment by adding a surface on the other side of the CoM is routine aerodynamic trim design and would be treated as an obvious design choice.
- The "forward-only thruster" limitation is a statement of the problem, not a technical feature.

**4.**

**§101/§112.** Method claim 1 is physical, and eligible. The inventor's plan to license "the planner separately" (claims 1 and 3–7 in software form) runs into *Alice*: converting a timing offset through ω⊕R⊕cosφ is a mathematical relationship. §112: "field-of-regard limit" and "substantially only in the direction of orbital motion" are OK. The FOV keep-out needs a geometric definition. **7.**

**Feasibility (recomputed).**
- **Drag.** f₀ = ½·7×10⁻¹¹·7755²·2.2·0.30/150 = **9.3×10⁻⁶ m/s²** (1.39 mN). With the visor, Δf adds 1.85 mN. **OK.**
- **Along-track shift, thruster off 48 h.** s = 1.5·9.3×10⁻⁶·(172,800)² = **417 km**, so Δt = 53.7 s. Ground-track shift = 7.292×10⁻⁵·6.378×10⁶·cos35°·53.7 = **20.5 km**. **OK.**
- **Altitude loss.** Δa = 2fτ/n = **6.4 km**. **OK.**
- **Omission.** The counter-flap's own drag is left out. At the same area it roughly *doubles* ΔA (0.4 → 0.8 m²). That helps authority but doubles makeup propellant and failure exposure.
- **Density uncertainty is understated.** Storm-time density at 250 km can rise by a factor of 2–3 within hours (Solar Cycle 25 lessons: https://arxiv.org/pdf/2406.08342 ; https://amostech.com/TechnicalPapers/2022/Atmospherics_Space-Weather/Ray.pdf), not ±40 %.
- **Authority collapses at solar minimum.** Density falls about 3–5×, so the 48 h shift drops to about 5–10 km.
- **The problem is partly self-inflicted.** The target at 117 km needs about 25° of roll at 250 km. Many VLEO designs accept ±30°.

**6.**

**Lifetime (the user's concern; this is the weakest candidate on it).**
- **Baseline makeup propellant** at Isp 1500 s, 150 kg, 0.30 m²:
  - moderate activity (ρ ≈ 7×10⁻¹¹): impulse 1.39 mN × 3.15×10⁷ s ≈ 4.4×10⁴ N·s per year, or **≈3.0 kg/yr**;
  - solar maximum (ρ ≈ 2×10⁻¹⁰ at 250 km): **≈8.5 kg/yr**.
  - A 5-year mission spanning a maximum needs about **25–30 kg**. The inventor's "typical 5–15 kg load" is already inadequate *before* the invention is used.
- **Cost per targeting event** is about 318 N·s, or **0.022 kg** (0.043 kg if the counter-flap drag is included). At commercial tempo of 100–300 events per year that is **2–13 kg/yr**, which is 70–400 % of the moderate-activity baseline. That is not "negligible".
- **Recovery time and thruster wear.** Recovering 6.4 km with a 10 mN thruster takes about 18–20 h per event, adding thruster on-time and grid erosion (ion thruster life is usually throughput-limited) and power.
- **Stuck-deployed visor.** Total drag becomes 1.4 + 1.85 (+1.85 counter-flap) ≈ 5.1 mN at moderate activity, and about 15 mN at solar maximum. That exceeds most 150 kg-class ion thrusters, and the decay rate is about 3 km/day with the thruster off, so **re-entry comes in about 2–3 weeks**.
- **Fail-safe dilemma.** "Spring-to-stow" preserves mission life. "Spring-to-deploy" helps deorbit compliance. Only one can be chosen, and the specification must pick one.
- **Atomic oxygen.** AO fluence on the ram visor is about 10¹⁵ cm⁻² s⁻¹, or about 3×10²² cm⁻² per year. Coating erosion products and diffuse re-emission upstream of the aperture need contamination analysis.
- **Deorbit compliance.** Trivially met at VLEO; the visor could double as a deorbit brake.

**3.**

**Commercial value and breadth.** Few VLEO operators exist. Design-arounds:
- Symmetric port/starboard flaps at CoM height (torque-free by placement, with no counter-flap and no ram-side visor).
- Articulated solar arrays, as in the 2021 art.
- A wider roll envelope.

**4.**

---

## 4. Claim amendments I would require for allowance

### Candidate 1 (CC-TDI)
1. **Claim 1(c):** replace "balanced code" with: "*a zero-sum weight sequence w₁…w_N that is non-monotonic in stage index, having at least four sign changes, such that the coded sum is not a difference of two contiguous stage blocks*". This distinguishes e2v's contiguous sub-matrices.
2. **Fold claim 4 into claim 1**, or into a second independent claim: "*at least two different weight sequences assigned to interleaved column groups, the sequences selected such that the sum of their squared spectral magnitudes has no zero over a predetermined band of at least 20 Hz to 1 kHz*".
3. **Claim 1(e):** recite "*deconvolving the weight sequence from a time series of coded residuals of successive ground lines, each ground line contributing one measurement, to obtain displacement samples at intervals equal to the TDI line period*". This is the trajectory limitation, and it separates the claim from e2v's single best-match shift.
4. **Add** "*wherein individual stage signals are not transferred off the focal-plane electronics*", to distinguish digital-TDI frame registration (IEEE 8796436; Sensors 25:3490).
5. **Design-around coverage:** add a dependent (or parallel independent) claim reading "*the coded sum is formed as a linear combination of K ≥ 3 partial sums of stage subsets with zero-sum coefficients*", plus ternary weights {−1, 0, +1}.
6. **Cancel claim 11 or demote it to a sub-dependent.** It is anticipated in substance by AO 61(16):4655 (2022).
7. **Claim 13:** either add a transfer-gate/pixel embodiment in the specification (for enablement) or drop it.

### Candidate 6 (Chronometric beacon)
1. **Merge claims 5 and 7 into claim 1.** Step (f) becomes "*determining an along-track geolocation residual of the emitters in the same image, subtracting the product of the time-tag error and the ground velocity, and outputting a pitch/alignment error of the sensor separately from the time-tag error*". This is the only element no reference suggests.
2. **Broaden "periodic waveform of period P"** to "*known time-varying intensity waveforms whose integrals over an exposure window differ from one another as a known, invertible function of the window-centre time*", with the phase-stepped sinusoid as a dependent claim. This closes the PN, edge and running-light design-arounds.
3. **Require** "*from a single image acquired in one pass by a sensor in orbit, the emitters being separated along-track by at least three ground-sample distances and the relative integration-time offsets corrected from surveyed layout and ground velocity*". This distinguishes the ISO 15781 bench panels and the multi-frame US 9,955,047.
4. **Cancel "exposure duration" as an independent result** (it is anticipated or obvious over the LED-Panel/ISO 15781). Keep claim 3 only as dependent on an MTF-corrected visibility, with the correction method written into the specification.
5. **Add a scintillation-mitigation dependent claim:** spatially incoherent emitter apertures larger than r₀, repeated phase-step groups, and ratios formed between co-located heads.
6. **Draft a second independent claim for the processing service** that recites the physical measurement inputs (surveyed emitter coordinates plus GNSS drive logs plus image) and the output of a corrected geolocation model *applied to image products*. This supports §101 Step 2A prong 2.

### Candidate 5 (TIR-cued SAR)
1. **Limit claim 1(d)** to "*an azimuth squint angle selected such that the ground-projected radar line-of-sight at aperture centre is substantially orthogonal to the measured ground velocity, subject to a squint limit*". This is claim 3 promoted. Delete "range-gate timing offset" and "Doppler-centroid setting" from the Markush group, because they are routine.
2. **Add** "*and a coherent dwell time determined from the covariance of the ground velocity vector via the azimuth FM-rate sensitivity ∂K_a/∂v_a ≈ −2K_a/V_eff*". Correct the formula across the specification.
3. **Broaden "TIR imager"** to "*a passive imaging sensor on the same spacecraft*", with TIR as a dependent claim. This blocks the AIS and optical design-arounds without reaching the AIS-cue art, provided claim 1 keeps the along-track dual-field displacement.
4. **Cancel claim 8 or narrow it.** It is obvious over CN111474545A.

### Candidates 2 and 3 (merged application)
1. **Independent claim:** "*selecting, from a plurality of candidate acquisition times of the same target, a time at which (i) a nadir-projected cloud mask indicates the target is occluded and (ii) a predicted line-of-sight segment through a cloud altitude interval is unoccluded*". Both embodiments (single-satellite look-ahead, and cloud field received from another spacecraft) should be claimed.
2. **Replace inventor 2's claim 3 premise** (separating h and u from tanθ non-proportionality) with "*predicting the apparent cloud position along the imaging satellite's own future view geometry from look-ahead image displacements, without separately resolving cloud height and along-track cloud motion*". This matches the physics shown above. Add shadow-offset height as a dependent claim.
3. **Promote the sun-ray/shadow utility and azimuth ≈ solar-azimuth selection (inventor 3, claims 3–4)** to a second independent claim. It is the least-anticipated element.
4. Do not require "trained segmentation model" or "cloud-base altitude" in the independent claims.

### Candidate 4 (VLEO visor)
1. **Claim 2:** require "*the visor and counter-flap being actuated such that the net aerodynamic pitch moment is substantially zero **and** the visor in its minimum-deployment state geometrically shadows the aperture from ram-direction flux*". The dual function is the only non-routine element.
2. **Claim 1:** add "*while acquiring imagery in a nadir imaging attitude, the variable-drag surface being distinct from solar arrays*". This addresses the Acta Astronautica 2021 art, and even then it is weak.
3. **Add a fail-safe dependent claim** (spring-to-stow with a separate end-of-life deploy mode) and a propellant-budget-constrained planner claim.

---

## 5. Final ranking and recommendation

| Rank | Candidate | Weighted | Allowance odds (my estimate, after amendment) | Notes |
|---|---|---|---|---|
| **1** | **CC-TDI (inventor 1)** | 7.0 | ~60–65 % | The only candidate with good breadth and a clean hardware hook. No lifetime penalty. |
| **2** | **Chronometric beacon (inventor 6)** | 5.9 | ~50–55 % (narrow) | The time/pitch decomposition is the hook. Low commercial breadth. |
| 3 | TIR-cued SAR (inventor 5) | 5.7 | ~35–40 % | Airborne cross-cue art is strong. Physics formula error. Cryocooler life limit. Alternate for slot 2 if commercial weight dominates. |
| 4 | 3D gap threading, merged 2+3 | ~5.5 | ~30 % | Obviousness is serious (convergence plus PCFLOS plus US 9,126,700). The shadow-azimuth claim is the best fallback. |
| 5 | VLEO visor (inventor 4) | 4.9 | ~30 % | Worst lifetime and propellant profile. Undercut by 2021 decoupled drag-articulation art. |
| 6 | Constellation 3D field (inventor 3, alone) | 4.8 | ~25 % | Singular three-look geometry. Scout phasing and propellant burden. |

### Top 2 for refinement: what the refiner must fix

**#1 CC-TDI (inventor 1)**
1. **Get and read the full text and claims of US 9,967,490 / EP 2 954 671.** Map exactly where "contiguous sub-matrix" appears in their claims. Draft claim 1 to require a non-contiguous weight sequence with at least four sign changes (amendments 1 to 3 above).
2. **Correct the noise budget.** K_eff ≤ 1,024, not 2,400. Use a realistic gradient distribution (median 5–10 %/px, not 20 %). Restate precision as about 0.02–0.04 px in a 1 kHz band and drop "6 nrad".
3. **Produce unexpected-results evidence.** Simulate on real TDI raw data (or realistic scene statistics) with injected wheel and cryocooler harmonics. Show split-half (e2v-equivalent) failing at its nulls where multi-code interleaving recovers the signal. Quantify the PRNU residual floor from real row-gain maps.
4. **Add design-around claims:** off-chip zero-sum combination of K ≥ 3 partial sums, and ternary weights. Drop or demote claim 11 (anticipated by AO 2022). Either give claim 13 an enabling pixel design or delete it.
5. **Search CN art specifically:** 编码 TDI 颤振 探测 (coded TDI jitter detection), 级 加权 (stage weighting). Also Golay/Hadamard-coded TDI in inspection tools (KLA/Hamamatsu) as a possible anticipation.

**#2 Chronometric beacon (inventor 6)**
1. **Move the time-tag/pitch decomposition (claim 7) and layout correction (claim 5) into claim 1.** Without them, claim 1 falls under §103 over US 9,955,047 + ISO 15781 LED-Panel + SPARC.
2. **Address the ISO 15781 / Image Engineering LED-Panel and CN103676453A art explicitly** in the background and distinguishing sections. Cancel "exposure duration" as a standalone contribution.
3. **Broaden the waveform language** to any known time-varying code with an invertible integral (PN, chirp, edge). Keep the phase-stepped sinusoid as a dependent claim.
4. **Add atmospheric scintillation to the error budget** (decorrelated between emitters about 4 m apart). Specify mitigation: extended incoherent apertures larger than r₀, repeated groups, co-located multi-wavelength heads. Restate the expected σ_t as about 5–15 µs rather than 4 µs.
5. **Specify the along-track temporal-MTF correction** of visibility for the TDI/τ claim (§112). Add a service-processing independent claim with concrete physical inputs and outputs for §101.
6. **Search non-patent literature** (SPIE, IGARSS, CALCON) for commissioning-phase ground laser or LED timing checks by satellite primes. Check for public-use and on-sale events.

### Lifetime note for the portfolio
- Inventor 4 has the only material risk to vehicle life, and it is severe: 25–30 kg of makeup propellant over a 5-year VLEO mission spanning solar maximum before any drag-steering use, 2–13 kg/yr added by steering, and a stuck-visor failure mode that means re-entry within weeks. It should not advance unless the program is VLEO-specific and accepts an approximately 2× propellant allocation.
- Inventor 3 needs propulsion on the scout for phasing (about 2,000 km/month natural drift from ballistic-coefficient mismatch).
- Inventor 5 is life-limited by its cryocooler.
- Inventors 1 and 6 are neutral to positive for vehicle life.

---

*Every reference marked [FT] is characterised from search abstracts only, because full-text sources are blocked in this environment. Confirm each before relying on it in prosecution.*
