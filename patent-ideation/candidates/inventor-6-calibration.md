# Inventor 6 — Calibration / Geolocation / Space-Ground Interaction

## Title

**Chronometric Cooperative Ground Beacon: Phase-Stepped, GNSS-Disciplined Emitter Constellation for Recovering the True Mid-Exposure Time of an Orbital Imager's Line from a Single Image, and Separating Time-Tag Error from Pitch-Attitude Error in Along-Track Geolocation**

---

## Brainstorm (raw concepts considered)

1. **Chronometric beacon (selected).** A surveyed cluster of GNSS-time-disciplined emitters driven with phase-stepped periodic waveforms. The imager's own pixels integrate them over the exposure window, so a single overpass image yields the absolute GNSS time of the line's mid-exposure (sub-10 µs) and the exposure duration. This breaks the long-standing along-track ambiguity between clock/time-tag bias and pitch bias.
2. **Laser-comm terminal as a radiometer.** Reuse the satellite's optical downlink telescope and its quad-cell tracking sensor to image a ground optical-ground-station beacon for absolute radiometric transfer. Heavily explored in the optical-comms literature, and gains are modest.
3. **Retro-reflector "barcode" GCPs.** Arrays of corner cubes tilted to form a sun-angle-dependent code that identifies the GCP in imagery. Close to SPARC-style mirror arrays, so novelty is weak.
4. **Lunar-limb band-to-band registration.** Use the Moon's limb during a pitch maneuver for push-broom band-to-band timing. Lunar calibration is crowded (ROLO, GIRO), and limb timing has been done.
5. **Polarization-modulated ground target for polarimetric calibration.** A liquid-crystal panel that flips polarization synchronized to the overpass. Niche, and the SNR is poor.
6. **Wavelength-hopping LED target for spectral response function (SRF) recovery.** Tunable narrow-band emitters that step across a band edge during the overpass to measure the SRF on orbit. Interesting, but a point source is seen for only ~3 lines, which limits how many steps it can capture.

Concept 1 was selected. It turns on a subtle physical fact. For a point source, a push-broom or framing pixel does not sample the source at one instant: it integrates over a window [t0, t0+τ]. If several co-imaged emitters carry the same known periodic waveform with deliberately stepped phases, the ratios of their integrated energies give the **phase of the window centre** directly. The ratio also cancels PSF, atmosphere, sub-pixel phase, and the absolute radiance of the emitters. No existing calibration site or patent found uses this to measure the image's *true absolute time*.

---

## Abstract

A ground calibration installation comprises a surveyed constellation of optical emitters. Their drive waveforms are disciplined to GNSS time and grouped into "phase-stepped groups": within a group, each emitter's radiant intensity follows the same periodic waveform of period P_k, offset by a known phase step (e.g., 0°, 120°, 240°). An unmodulated reference emitter is also included. The groups use a geometric ladder of periods (e.g., 2 ms, 64 ms, 4 s). The emitters are spaced several ground-sample distances apart, so each appears as a separable point source in a single image from a LEO push-broom (including TDI) or framing imager. Within each group the integrated energies are normalized by the reference emitter. From these ratios a processor computes the phase of the window centre and the modulation visibility. Phase gives the true mid-exposure time modulo P_k; visibility gives the exposure (TDI) duration. The processor corrects for the known relative layout of the emitters and for the light-travel time, then unwraps phase across the period ladder to get the absolute GNSS time at which the imaged line was integrated. Comparing it with the time tag the satellite gave that line yields the time-tag bias directly. The along-track geolocation residual of the beacon's surveyed position can then be split, from one pass, into a time-tag part and a pitch/ephemeris part. Doing the same for each spectral band gives inter-band timing, and the reference emitter doubles as an absolute point-source radiometric standard.

---

## Problem addressed

1. **Time-tag bias and pitch bias cannot be told apart in along-track geolocation.** For a nadir LEO imager, an image time-tag error δt shifts the product along-track by v_g·δt (v_g ≈ 7.06 km/s at 500 km, so 1 ms gives 7 m). A pitch error δθ shifts it by H·δθ (1 µrad gives 0.5 m at 500 km). With passive ground control points (GCPs), both show up as the same along-track offset. Operators fit a lumped "along-track bias", which then fails when conditions change: pitch-steered or off-nadir imaging, a different altitude, a clock re-sync after safe mode, or thermal drift of the star-tracker-to-camera alignment. The LAPAN-A3 processing paper (arXiv:1901.09189) documents exactly this confound: along-track error came jointly from system time error and imager/star-tracker misalignment.
2. **Timing is poorly observed on small satellites.** Cubesat and smallsat constellations often have time-tag chains (PPS distribution, FPGA line-counter latching, bus-to-payload offsets) with 0.1–10 ms uncertainty. That uncertainty drifts after resets, and today nothing on the ground can observe it independently.
3. **TDI stage count, exposure time and line-rate errors** are verified today only indirectly, through radiometric gain (confounded with degradation) or MTF.
4. **Band-to-band registration** in multi-line push-brooms depends on the inter-band time offsets. Those offsets are currently inferred from image correlation, which is confounded by terrain parallax and attitude jitter.

---

## Detailed description

### System blocks

**Ground segment ("Chronometric Beacon Site", CBS)**

- **B1. GNSS-disciplined timebase.** A multi-constellation timing receiver with an OCXO or CSAC holdover gives <30 ns RMS to UTC(GPS) and a 10 MHz reference plus PPS.
- **B2. Waveform synthesizer.** An FPGA with a DDS per emitter channel, phase-locked to B1. It produces a precomputed intensity waveform m_{k,j}(t) = 1 + cos(2π t/P_k − 2πj/J) for group k, phase step j (J = 3 or 4). A PPS-referenced epoch t = 0 is defined at each GNSS second (with integer-second bookkeeping for P ≥ 1 s).
- **B3. Emitter array.** High-power LED or laser-diode emitter heads, each a current-mode linear driver (bandwidth >1 MHz, so the waveform fidelity error is <0.1% for P ≥ 1 ms). Each head has a homogenizing diffuser and a ±25° to ±30° beam pointed at the zenith or on a two-axis tracking mount. Wavelengths are chosen to fall inside the target imager's bands (e.g., 490, 560, 665, 850 nm heads co-mounted). Head spacing is ≥4 GSD of the finest target imager (e.g., 3–4 m for 0.75 m GSD). One head per site is the **reference emitter R**, held at constant intensity during the pass window.
- **B4. Closed-loop monitor photodiodes.** A fast Si photodiode at each head, digitized against B1, measures the actual emitted waveform: its phase delay (driver latency, typically 0.2–2 µs), its amplitude and its harmonic distortion. The measured values, not the nominal ones, are logged per pass.
- **B5. Survey and metadata.** RTK- or PPP-surveyed coordinates (<2 cm) of every head, the site heading of the emitter layout, and the calibrated radiant intensity of R (traceable to a lab standard). An on-site sun photometer (optional) supplies aerosol optical depth.
- **B6. Pass scheduler.** Ingests public TLEs or operator ephemerides and energizes the array only during predicted overpass windows (±30 s). This saves power and reduces light pollution. It can also select wavelength heads matching the passing satellite.

**Space segment (unmodified)**

- **S1.** Any LEO push-broom (single-line or TDI), multi-line multispectral, or framing (global or rolling shutter) imager. No hardware change is needed. The method uses only the raw or L1A pixel data and the per-line time tags that already exist.

**Processing segment ("Chronometric Solver")**

- **P1.** Point-source detection and separable photometry per emitter, per band. Energy is summed within a PSF-sized aperture (e.g., 5×5 pixels) after local background subtraction.
- **P2.** Emitter identification from the known layout, matched to the detected point pattern with a similarity transform.
- **P3.** Relative-timing correction. Emitters at different along-track positions are integrated at slightly different instants. The expected offset Δt_i = (Δs_i · û_track)/v_g is computed from the surveyed relative layout and the ephemeris ground velocity. This is a *relative* correction and needs no absolute geolocation knowledge; the error from a 0.05% v_g error over a 5 m offset is 0.35 ns.
- **P4.** Phase-stepped demodulation per group, giving phase φ_k, visibility V_k and exposure τ.
- **P5.** Light-time correction: t_line = t_emit + R_slant/c. The slant range comes from the ephemeris; a 1 m range error gives 3.3 ns.
- **P6.** Hierarchical phase unwrapping across the period ladder, giving the absolute GNSS time of mid-exposure, t_c, for the image line or TDI row that recorded the beacon.
- **P7.** Error decomposition: time-tag bias δt = t_tag − t_c. The along-track residual of the beacon centroid, with v_g·δt removed, gives pitch bias plus along-track ephemeris error. Cross-track residual gives roll. Per-band t_c differences give inter-band delays.
- **P8.** Radiometric by-product: the reference emitter R's integrated DN divided by its known in-band intensity (after atmospheric transmission) gives an absolute point-source gain, cross-checked against exposure τ from P4.

### Step-by-step method

1. The pass scheduler predicts the overpass and selects the wavelength heads and the period ladder {P_1 < P_2 < P_3}. Ladder rules: P_1 ≈ 2–3 × expected exposure τ (sensitivity is maximal near there); each P_{k+1}/P_k ≤ π·σ-margin (typically 16–64); and the final P_K exceeds the worst-case a-priori time uncertainty.
2. The synthesizer drives each group k with J phase-stepped copies of the waveform, and the reference R constant, all disciplined to GNSS. The monitor photodiodes log the actual emitted phase and amplitude.
3. The satellite images the site normally.
4. For each band b and each emitter i, the solver extracts the integrated energy E_i. For a window centred at t_c with duration τ, and a sinusoidal waveform:
   E_{k,j} / E_R = a · [1 + V_k cos(2π t_c/P_k − 2πj/J)], where V_k = sinc(π τ/P_k) = sin(πτ/P_k)/(πτ/P_k).
   The PSF, sub-pixel phase, atmospheric transmission and view-angle factors are common to all heads of one wavelength, so they cancel in the ratio. The emitter-to-reference intensity ratio a is known from the monitors.
5. The J-step estimator gives φ_k = atan2(−Σ_j r_j sin(2πj/J), Σ_j r_j cos(2πj/J)) and V_k from the magnitude. Then τ = inverse-sinc of V_k, using the shortest-period group (the most sensitive to τ).
6. The P3 relative-timing correction is applied to each emitter, and the P5 light-time correction to the whole solution.
7. Phase is unwrapped from the longest period down: t_c^(K) = φ_K P_K/2π + n_K P_K, with n_K fixed by the a-priori onboard time (±P_K/2). Then, for each shorter period, n_k = round((t_c^(k+1) − φ_k P_k/2π)/P_k).
8. The time-tag bias δt_b = t_tag,b(line) − t_c,b is computed per band.
9. Along-track decomposition: Δy_obs = y_image − y_predicted(survey, ephemeris, attitude, t_tag). Then pitch-equivalent residual = Δy_obs − v_g·δt, and δθ ≈ residual/H (with an off-nadir geometry factor).
10. Repeating over several passes, sites and look angles fits a timing model (bias, drift, line-period scale) and an alignment model (pitch/roll bias, thermal terms) as *separate* parameter sets. These are delivered to the operator as calibration updates, or used onboard to discipline the payload clock.

---

## Worked numerical example

**Satellite:** 500 km, v_g = 7.06 km/s, GSD 0.75 m, line period T_L = 106 µs, 8-stage TDI, so τ = 850 µs. Aperture D = 0.35 m (A = 0.096 m²), optics×filter throughput 0.7, QE 0.6, NIR band 830–870 nm, read noise 30 e⁻.

**Emitter:** a 40 W optical 850 nm LED array into ±25° gives ≈ 67 W/sr on axis. Budget uses I = 30 W/sr in-band (derated for band overlap and off-axis) with atmospheric transmittance 0.8.

- Irradiance at the aperture: 30 × 0.8 / (5×10⁵ m)² = 9.6×10⁻¹¹ W/m², giving 6.5×10⁻¹² W collected.
- That is 2.8×10⁷ photons/s, or **≈ 14,100 e⁻** per emitter over τ.
- Daylight background (ρ = 0.1, 40° sun zenith, 40 nm band): ≈ 260 e⁻ per pixel. The 4-pixel PSF core gives ≈ 1,040 e⁻.
- **Emitter SNR ≈ 14,100 / √(14,100 + 1,040 + 4·900) ≈ 103.**

**Ladder:** P_1 = 2 ms, P_2 = 64 ms, P_3 = 4 s, each group with J = 3 phases.

| Group | P_k | V_k = sinc(πτ/P) | σ_φ ≈ 1/(SNR·V) | σ_t = P·σ_φ/2π | Unwrap margin (P_{k-1}/2 ÷ σ_t) |
|---|---|---|---|---|---|
| 1 | 2 ms | 0.728 | 0.0133 rad | **4.2 µs** | — |
| 2 | 64 ms | 0.9997 | 0.0097 rad | 99 µs | 1 ms / 99 µs = **10σ** |
| 3 | 4 s | 1.000 | 0.0097 rad | 6.2 ms | 32 ms / 6.2 ms = **5.2σ** |

The final 4 s ambiguity is resolved by the onboard clock, which is always good to ≪ 2 s.

**Results from one band on one pass:**

- **Absolute mid-exposure time σ ≈ 4.2 µs**, equal to **3.0 cm** along-track. Three bands averaged give ≈ 2.4 µs.
- **Exposure / TDI:** dV/dτ at τ/P = 0.425 is ≈ −0.93 per unit τ/P. σ_V ≈ 1/SNR ≈ 0.0097 gives σ_τ ≈ 21 µs, about 0.2 of a TDI stage. This is enough to detect a wrong stage count (±106 µs) at 5σ.
- **Decomposition:** suppose the satellite's time tag is 350 µs late (a plausible FPGA-latching error) and there is a 4 µrad pitch bias. Passive GCPs see a lumped 2.47 m + 2.0 m = 4.47 m along-track error and cannot split it. The beacon measures δt = 350 ± 4 µs, so it removes 2.47 m ± 0.03 m of the error. The remaining 2.00 m is attributed to pitch: 4.0 ± 0.1 µrad, with σ limited by centroid precision of ~0.05 px ≈ 3.8 cm.
- **Emitter count:** 3 groups × 3 phases + 1 reference = 10 heads per wavelength. At 4 m spacing in a 4×3 grid the footprint is 16 m × 12 m, installable on one rooftop or pad. Electrical power is ≈ 10 × 60 W for ~60 s per pass.
- **Timebase error budget:** GNSS 30 ns, driver latency after monitor correction 50 ns, light-time 3 ns, relative layout 1 ns. The total of ≪ 1 µs is negligible compared with the 4 µs photon-noise term.

---

## Closest prior art found and distinguishing features

| # | Reference | What it discloses | How this invention differs |
|---|---|---|---|
| 1 | **US 9,955,047 B2**, "Method and device for acquiring stream of the precisely time-stamped images" ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9955047)) | A GNSS-time-controlled modulated LED placed in a scene. The camera decodes the modulation over the frame sequence to assign absolute time stamps to frames. Multi-element sources are mentioned for richer coding. | **This is the closest prior art.** It decodes a code over *many frames* in a terrestrial video stream. It does not disclose (a) *phase-stepped groups normalized by a co-imaged reference* to recover sub-exposure timing from a *single* integration window; (b) visibility-based recovery of exposure/TDI duration; (c) correcting for relative emitter layout and ground velocity; (d) orbital light-time correction; (e) using the recovered time to *split time-tag bias from pitch-attitude bias* in geolocation; (f) per-band inter-band delay calibration. A point source seen by a LEO push-broom appears in only ~1–3 lines, so frame-sequence decoding is physically unavailable. |
| 2 | **WO2015173001A1 / EP3143759A1**, "Verification of images captured using a timestamp decoded from illumination from a modulated light source" ([Google Patents](https://patents.google.com/patent/EP3143759A1/en)) | Timestamps are decoded from modulated ambient illumination to authenticate images. | Its purpose is authentication and it works at frame-level resolution. It has no sub-exposure phase retrieval, no orbital geometry, and no geolocation-error decomposition. |
| 3 | **US 8,767,210 B1 / US 9,052,236**, NASA "Method for ground-to-space laser calibration system" ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8767210)) | A ground laser tracks a satellite at night to radiometrically calibrate reflected-solar sensors. | Radiometric only. It has no time-coded, phase-stepped waveform and no measurement of timing or exposure. |
| 4 | **SPARC**, Schiller et al., **US 8,158,929** (referenced in search results); Zhongwei point-source array (Li et al., "Improved On-Orbit MTF Measurement Method Based on Point Source Arrays", *Remote Sens.* 2023, 15(16):4028, [MDPI](https://www.mdpi.com/2072-4292/15/16/4028)) | Passive convex-mirror point sources reflecting sunlight, for radiometric, MTF and geometric calibration. | These are passive and time-invariant, so they carry no time information. The present invention's core signal is the *temporal* waveform. |
| 5 | **T2L2 on Jason-2** (Samain et al., [OCA](https://www.oca.eu/en/r-d-geoazur/2312-t2l2-geoazur-en); [Metrologia 2014](https://iopscience.iop.org/article/10.1088/0026-1394/51/5/503)) | Ground laser pulses are timed by a *dedicated onboard photodetector and event timer* for clock comparison. | That approach needs dedicated flight hardware and measures the clock, not the *imaging pixel's integration window*. The present invention needs no flight hardware and measures the quantity geolocation actually needs: when the pixel that saw the ground was exposed. |
| 6 | **DMSP OLS "Aladdin's Magic Lamp"** active target (Elvidge et al., [ResearchGate](https://www.researchgate.net/publication/277675188_Aladdin's_Magic_Lamp_Active_Target_Calibration_of_the_DMSP_OLS)) | A steady high-power lamp used as a night-time radiometric target. | It is unmodulated and carries no timing. |
| 7 | **LAPAN-A3/IPB processing** ([arXiv:1901.09189](https://arxiv.org/pdf/1901.09189)) | Identifies system time error and pitch misalignment as the joint causes of along-track error, estimated together from GCPs. | This is evidence of the *problem*. It uses no active beacon and so cannot separate the two terms in one pass. |
| 8 | US 7,705,879 / RE44604, "synchronous acquisition of pulsed source light" ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7705879)) | GPS-synchronized pulsed beacons with a gated camera; the *camera* is synchronized to the beacon. | Here the camera is *not* synchronized and its timing is the unknown being measured. Phase-stepped ratiometric demodulation is absent. |

---

## Why non-obvious

- **The inversion is counterintuitive.** Conventional point-source calibration treats pixel integration as a nuisance that smears a source; GNSS beacon art treats the camera as a sampler of a code over many frames. The invention instead treats *the integration window itself as a matched filter*. With phase-stepped, reference-normalized emitters, one window yields both its centre time (phase) and its duration (visibility). That is the natural move for phase-shifting interferometry, not for remote-sensing geometric calibration, which is not known to have borrowed the technique.
- **The ratiometric design is what makes it work from orbit.** Absolute photometry of a point source through the atmosphere is uncertain at the 5–10% level, which is useless for timing. Normalizing by co-imaged phase-stepped siblings and a reference cancels the PSF, sub-pixel phase, atmosphere and view angle. This is a specific, non-trivial enabling feature.
- **Relative-layout timing correction** lets the emitters sit in an arbitrary surveyed 2-D layout rather than exactly along a line of constant image time. A naive design would require perfect alignment with the ground track, which is impossible across different orbits and headings.
- **The motivation to separate time-tag bias from pitch bias with a ground device is not suggested by the art.** Practitioners accept a lumped along-track bias or rely on onboard PPS design reviews.
- The combination of a period ladder, light-time correction, and multi-band per-line timing forms a coherent system with no single reference teaching it.

---

## Draft claims

**Independent method claim**

1. A method of calibrating the timing of an orbital Earth-imaging sensor, comprising:
   (a) providing, at surveyed ground locations, a plurality of optical emitters, including at least one reference emitter and at least one phase-stepped group of emitters, wherein the emitters of the group are driven to emit radiant intensities following a common periodic waveform of period P, each offset by a distinct known phase, and are driven synchronously to a global navigation satellite system (GNSS) timebase;
   (b) acquiring, by the orbital sensor, an image in which the emitters appear as mutually separable point-source responses produced by pixel integration over an exposure window;
   (c) determining, for each emitter of the group, an integrated response and normalizing it by the integrated response of the reference emitter to form normalized ratios;
   (d) computing, from the normalized ratios, a phase of the exposure window's centre relative to the periodic waveform, and computing therefrom a GNSS-referenced mid-exposure time of the image line or row that recorded the emitters; and
   (e) comparing the GNSS-referenced mid-exposure time with a time tag assigned by the orbital sensor to that line or row, to determine a time-tag error of the sensor.

**Independent system claim**

2. A system for timing calibration of an orbital Earth-imaging sensor, comprising:
   a GNSS-disciplined timebase;
   a waveform generator phase-locked to the timebase and configured to generate, for each of one or more phase-stepped groups, a plurality of periodic drive waveforms of common period and mutually offset known phases;
   an array of optical emitters driven by the waveform generator and including a reference emitter, the emitters being spaced apart on the ground by at least three ground-sample distances of the sensor so as to be separately resolved; and
   a processor configured to receive an image of the array acquired by the sensor, extract integrated point-source responses, form ratios normalized to the reference emitter, compute from the ratios the phase of the exposure-window centre, and output a GNSS-referenced mid-exposure time and a time-tag error for the sensor.

**Dependent claims**

3. The method of claim 1, further comprising computing from the normalized ratios a modulation visibility and determining therefrom the exposure-window duration, including a time-delay-integration stage count of the sensor.
4. The method of claim 1, wherein a plurality of phase-stepped groups are driven with a ladder of different periods, and the mid-exposure time is determined unambiguously by hierarchical phase unwrapping from the longest period to the shortest.
5. The method of claim 1, further comprising, before computing the phase, correcting each emitter's integrated response for a predicted relative integration-time offset computed from the surveyed along-track separation of that emitter relative to the other emitters and from the sensor's ground velocity.
6. The method of claim 1, further comprising correcting the mid-exposure time for the optical light-travel time over the slant range between the emitters and the sensor, computed from sensor ephemeris.
7. The method of claim 1, further comprising determining an along-track geolocation residual of the emitters' surveyed position in the image, subtracting the product of the time-tag error and the ground velocity, and attributing the remainder to a pitch-attitude or camera-alignment error of the sensor.
8. The method of claim 1, wherein the sensor is a multi-band push-broom sensor, the emitters include heads emitting within each of a plurality of spectral bands, and a mid-exposure time is determined separately for each band to yield inter-band timing offsets used for band-to-band registration.
9. The system of claim 2, further comprising a monitor photodetector at each emitter, time-stamped against the timebase, wherein the processor uses measured, rather than nominal, emitted phase and amplitude.
10. The system of claim 2, wherein the reference emitter has a calibrated in-band radiant intensity and the processor further derives an absolute radiometric gain of the sensor, using the exposure duration derived from the phase-stepped group.
11. The system of claim 2, further comprising a pass scheduler that energizes the emitters only during a predicted overpass window of the sensor and selects emitter wavelengths matching the sensor's spectral bands.
12. The method of claim 1, repeated over multiple passes and ground sites to estimate separately a timing model (bias, drift and line-period scale) and a geometric alignment model of the sensor, and uploading at least one of them to the sensor or to its ground processing chain.
13. The method of claim 1, wherein the sensor is a rolling-shutter framing sensor and the mid-exposure times determined for emitters at different image rows are used to calibrate the row readout skew.

---

## Commercial use cases

- **Smallsat constellation operators** (sub-meter optical fleets): fleet-wide time-tag verification after launch, software updates or safe-mode recovery, with no flight hardware. Timing and pitch biases are reported as separate calibration products. Sold as a calibration-as-a-service site network, alongside RadCalNet- or SPARC-style offerings.
- **Geolocation-accuracy certification** for defence and insurance customers that need traceable GCP-free error budgets: an "absolute time traceability" line item.
- **Band-to-band registration QA** for hyperspectral push-brooms, whose inter-band delays can be large.
- **TDI health monitoring:** detects a stuck or wrong TDI stage setting before it is misread as radiometric degradation.
- **Stereo and video-from-orbit:** absolute timing is critical for moving-target velocity estimation (ships, vehicles), where a 1 ms error gives about 1 cm/s velocity bias per metre.
- **Cal/val agencies** (USGS, ESA, NIST-traceable sites) can add chronometric heads to existing SPARC or RadCalNet sites.

---

## Known weaknesses / risks to patentability

- **US 9,955,047 is the key §103 risk.** An examiner could combine it (GNSS-modulated LED gives image time stamps) with the phase-shifting interferometry literature (J-step demodulation) and SPARC (point-source sites). The rebuttal rests on the single-window ratiometric construction, the layout correction, orbital light-time, and above all the claimed time-versus-pitch decomposition. Claims 1(e) and 7 should probably be merged into the independent claim for a stronger fallback.
- **Undisclosed operator practice:** satellite primes may already do private timing checks with pulsed lasers during commissioning. A non-patent-literature search (SPIE/IGARSS proceedings on "LED beacon" or "laser beacon" plus "time tag") beyond the one performed here is needed.
- **Practical constraints:** it needs clear sky and a beam pointed at the satellite (off-nadir passes need a tracking mount or wide beams, which cost SNR). Daytime SNR is adequate at 0.75 m GSD, but degrades for small-aperture cubesats (D = 9 cm cuts the signal about 15×, to σ_t ≈ 20–40 µs, which is still ≪ typical time-tag errors). Laser-safety and light-pollution rules apply at night. Pixel saturation must be avoided through gain or pass-specific intensity scheduling.
- **Nonlinearity:** detector nonlinearity or charge blooming at high emitter signal would bias the ratios. This is mitigated by keeping intensities in the linear range and by the reference ratio, but a claim limitation may be needed.
- **Enforcement:** infringement happens on the ground and in data processing, so it is detectable through site operators and calibration-service offerings. Satellite operators processing their own images could be hard to police.
- **Claim scope:** "periodic waveform" should be broadened to include pseudo-random and chirp codes with a known integrated response. Otherwise a design-around using PN-coded integrations with least-squares timing is available.

---

**Self-assessed patentability: 7/10.** Novelty is fairly strong in the combination and application. Obviousness is the main battleground, because of US 9,955,047 combined with phase-shifting demodulation.
