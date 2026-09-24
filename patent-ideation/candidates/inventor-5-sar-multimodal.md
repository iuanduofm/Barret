# Inventor 5 - SAR / Thermal IR Multi-Modal Acquisition-Time Fusion

## Title

**Thermal-Infrared Kinematic Pre-Look for Motion-Matched Synthetic Aperture Radar Acquisition of Moving Targets from a Single LEO Spacecraft**

---

## Abstract

A LEO spacecraft carries a synthetic aperture radar (SAR) and a thermal-infrared (TIR) imager on the same bus. The TIR focal plane has two detector fields, separated along-track and both pointed ahead of the SAR's zero-Doppler plane into the SAR's cross-track access region. Each moving target, for example a ship's hot exhaust stack or hull, is therefore imaged twice by the TIR, about 10–20 s apart, before it enters the SAR beam. An onboard processor detects hot-spot targets in both TIR fields, associates them, and computes each target's ground velocity vector from the displacement between the two looks. It also estimates the velocity's uncertainty. A SAR mode controller then turns each target's velocity vector into acquisition parameters for the SAR aperture that follows seconds later on the same pass: (i) an azimuth squint angle that brings the target's line-of-sight (radial) velocity to zero, (ii) a time-varying beam-center trajectory that follows the target's predicted position, (iii) a coherent dwell time sized to the residual phase error allowed by the velocity uncertainty, and (iv) offsets to the range-gate and Doppler-centroid settings. The measured velocity prior is written into the SAR raw-data header for motion-compensated focusing. The result is well-focused, correctly positioned SAR images of moving vessels at resolutions that would otherwise need blind autofocus or would be lost to defocus, azimuth displacement and range walk. No second satellite, AIS data or ground loop is needed.

---

## Problem Addressed

1. **Moving targets break SAR focusing.** A ship moving at 10–15 kn has a line-of-sight (radial) velocity v_r that shifts it in azimuth by Δx ≈ R·v_r/V (often 100–500 m from LEO, which leaves the ship "off its wake"). It also causes range walk across several resolution cells during a multi-second aperture. The along-track velocity v_a changes the azimuth FM rate, which smears the target in azimuth. At sub-meter resolution these effects are severe.
2. **Current fixes are post-hoc and blind.** Ship refocusing today uses autofocus methods such as minimum-entropy, phase-gradient or time-frequency analysis, applied after acquisition to data collected with parameters chosen for a static scene. These methods break down at low SNR, with several ships per spot, or when the target has already migrated out of range cells or out of the processed Doppler band. They cannot recover data that was never collected, such as a spotlight scene pointed at where the ship was rather than where it will be.
3. **Tip-and-cue works across satellites, not within an aperture.** Operational tip-and-cue (AIS or RF to SAR, or SAR to optical) passes a *position* to a *different* satellite with a latency of minutes to hours. None of these systems measures a target's *velocity vector* seconds before a SAR aperture on the same bus and uses it to shape the aperture's geometry and timing.
4. **Dark vessels at night.** Optical pre-looks fail at night. AIS is missing for "dark" vessels by definition. TIR sees engine exhaust and hull heat day and night, so it is the only passive modality that can supply kinematics for every vessel at every local time.

---

## Detailed Description

### System blocks

| # | Block | Description / example spec |
|---|-------|---------------------------|
| B1 | **SAR payload** | X-band (λ = 3.1 cm), phased array or reflector with electronic or body-slew azimuth steering of about ±15° squint. Supports sliding-spotlight and staring-spotlight modes. Programmable PRF, range-gate delay (data-window position, DWP) and beam-steering table per burst. |
| B2 | **Dual-field TIR imager** | LWIR (8–12 µm) or MWIR (3–5 µm) telescope, D ≈ 0.30 m, cooled or high-grade microbolometer focal plane. Carries two along-track-separated **field windows** (TIR-F1 "far-fore" and TIR-F2 "near-fore"). Both are boresighted to the SAR's cross-track look angle and both sit ahead of the SAR's zero-Doppler plane (e.g., +16° and +6° along-track). The windows may be on one focal plane with a field-splitting mirror, or on two small co-mounted telescopes. |
| B3 | **Common metrology frame** | Both instruments mount to one thermally stable optical bench with a shared star tracker and IMU. The inter-field angle is calibrated on orbit using static coastline and platform features, so that relative TIR-SAR pointing is known to better than 20 µrad. |
| B4 | **Onboard TIR detection & kinematics processor** | FPGA or SoC. Runs hot-spot/CFAR detection over a sea-surface background, associates detections between F1 and F2 (gated by physical speed limits of 0–40 kn), estimates sub-pixel centroids and computes the velocity vector with its covariance. Optionally extracts the heading of the thermal wake. |
| B5 | **Kinematic SAR mode controller** | Takes (position, velocity, covariance, thermal class) per target and solves for squint angle, beam-center trajectory, dwell time, PRF/DWP and Doppler-centroid offset under agility, power and duty-cycle limits. Produces a per-target command block within 2 s. |
| B6 | **Multi-target scheduler** | Ranks targets by priority (thermal class, speed, user area of interest) and sequences apertures, trading dwell (resolution) against the number of ships imaged per pass. |
| B7 | **Metadata packer** | Writes the TIR velocity prior, its covariance and the TIR chip into the SAR raw-data header. This lets ground or onboard focusing use a known-parameter motion model and gives a SAR-TIR tie point. |
| B8 | **Optional feedback path** | SAR-measured Doppler-centroid anomaly or along-track-interferometry (ATI) phase refines the velocity estimate, which is used for the next aperture on the same target (a Kalman update). |

### Method (step by step)

1. **Pre-look 1 (TIR-F1).** As the spacecraft advances, TIR-F1 images a strip in the SAR access region at along-track angle θ_F1 ahead of zero-Doppler, at time t₁.
2. **Detection.** B4 detects compact thermal anomalies. For LWIR, detections are pixels with brightness temperature at least 1.5 K above the local sea background and a spatial extent consistent with a vessel. Each detection gets a thermal class: *hot-stack / underway*, *warm hull / idle*, or *ambient / platform-iceberg*.
3. **Pre-look 2 (TIR-F2).** The same targets are imaged again at time t₂ = t₁ + Δt, where Δt = R·(tan θ_F1 − tan θ_F2)/V_g.
4. **Association and velocity.** B4 matches detections across the two looks within a gate of r ≤ v_max·Δt + 3σ_pos. It computes **v** = (**p**₂ − **p**₁)/Δt in a local ground frame, corrected for the known platform motion, and the covariance **Σ_v** from the centroid SNR and the pointing knowledge. The thermal-wake axis, if detected, is fused as a heading constraint.
5. **Prediction.** B5 propagates each target to the planned aperture-center time t_c, using constant velocity: **p**(t) = **p**₂ + **v**(t − t₂).
6. **Squint selection.** B5 chooses the aperture-center along-track position (and hence squint ψ) so that the ground-projected line-of-sight unit vector **û** is orthogonal to **v**, making v_r = **v**·**û** ≈ 0. If the needed |ψ| exceeds the agility or ambiguity limit ψ_max, it clips to ψ_max and records the residual v_r.
7. **Beam-center trajectory.** The spotlight steering table follows **p**(t) over the aperture instead of a fixed ground point. The spot can then be made smaller, which cuts data volume and range/azimuth ambiguities.
8. **Dwell sizing.** B5 computes the along-LOS-orthogonal velocity component v_⊥ and the deterministic FM-rate offset ΔK_a ≈ K_a·v_∥/V_g, where v_∥ is the target velocity component parallel to the spacecraft ground track. From the 2σ uncertainty σ_ΔKa it sets T = 1/√(2σ_ΔKa) for a residual quadratic phase error of at most π/4. This T sets the achievable azimuth resolution. The scheduler (B6) decides whether to spend that dwell.
9. **Range / Doppler settings.** The DWP is offset by the predicted range change and the Doppler centroid by 2·v_r,residual/λ. The PRF is checked against the target's shifted Doppler band to avoid folding it into an azimuth ambiguity.
10. **Acquisition.** The SAR collects the aperture with the per-target command block.
11. **Tagging.** B7 attaches the velocity prior, the TIR chip and the timestamps to the raw SAR data. Focusing applies the known FM-rate correction first and then a narrow-band autofocus over the residual.
12. **Refinement (optional).** A Doppler-centroid anomaly measured by SAR, or an ATI phase, updates **v**, and the update is used when the scheduler revisits the same target or a nearby follower.

---

## Worked Numerical Example

**Orbit / geometry.** h = 550 km, V_s ≈ 7.6 km/s, ground-track speed V_g ≈ 7.0 km/s, effective velocity V_eff ≈ 7.3 km/s. SAR X-band, λ = 0.031 m, incidence 35° (look angle ≈ 31.5°). Ground range g ≈ 337 km, broadside slant range R ≈ 645 km.

**TIR pre-look timing.** The TIR fields are at +16° and +6° along-track at slant range R:
- F1 ground offset ≈ 645·tan16° ≈ 185 km ahead; F2 ≈ 645·tan6° ≈ 68 km ahead.
- **Δt (F1 to F2) ≈ (185 − 68)/7.0 ≈ 16.7 s**; **lead time (F2 to broadside) ≈ 9.7 s**. That leaves over 5 s of margin for detection, kinematics and command upload.

**TIR resolution and velocity accuracy.** LWIR at 10 µm with D = 0.30 m gives a diffraction spot ≈ 40 µrad, or ≈ 26 m GSD at 645 km. A 12 m vessel with its exhaust plume is a sub-pixel hot spot with high contrast (stack 350–450 K against 290 K sea). Centroiding to 0.1 px gives about 2.6 m per look, so σ_v ≈ √2·2.6/16.7 ≈ **0.22 m/s**. Adding about 0.1 m/s of inter-field pointing knowledge error gives a budget of **σ_v ≈ 0.3 m/s**.

**Target.** A ship at 12 m/s (23 kn), heading 15° off the satellite ground-track direction, with a component toward the radar.
- Cross-track ground component = 12·sin15° = 3.11 m/s; along-track component v_∥ = 11.6 m/s.
- **Conventional broadside acquisition:** v_r = 3.11·sin35° = 1.78 m/s.
  - Azimuth displacement ≈ R·v_r/V_eff = 645 km × 1.78/7300 ≈ **157 m** (the ship is displaced from its wake).
  - Range walk over a 1.5 s aperture = 2.7 m, which is **about 5 range cells at 0.5 m range resolution**.
  - Doppler centroid offset = 2v_r/λ ≈ 115 Hz.
- **Invention: velocity-nulling squint.** Rotate the ground LOS by 15° so that it is orthogonal to **v**. The along-track offset is y = g·tan15° ≈ 90 km, the slant range becomes R' ≈ 651 km and the **squint is ψ ≈ 8.0°**, which is within typical small-SAR agility of ±15°. Residual v_r = 0 ± 0.3 m/s, so displacement ≤ 27 m (1σ) and range walk ≤ 0.45 m (under 1 cell).
- **Dwell sizing.**
  - Azimuth FM rate: K_a = 2V_eff²/(λR') ≈ 5280 Hz/s.
  - Deterministic offset: ΔK_a ≈ K_a·v_∥/V_g ≈ 8.7 Hz/s. This is known from the TIR measurement, so it is removed in focusing.
  - Uncertainty: σ_ΔKa ≈ K_a·0.3/7000 ≈ 0.23 Hz/s. Using 2σ (0.45 Hz/s) and QPE ≤ π/4 gives **T ≈ 1.49 s**, so azimuth resolution ρ_a ≈ λR'/(2V_eff·T)·(V_g/V_eff) ≈ **0.87 m**.
  - **Without the prior** (speed unknown over 0–12 m/s), |ΔK_a| can be up to 8.7 Hz/s and T_max ≈ 0.34 s, so **ρ_a ≈ 3.8 m**, unless blind autofocus works, which is unreliable for small, low-RCS or multiple targets.
- **Net effect:** about a **4.4× finer azimuth resolution** that can be guaranteed on the moving target, at the correct geolocation, with no range-cell migration from target motion. The per-ship aperture costs about 1.5 s of radar-on time. In a 60 s access window the scheduler can therefore interleave about 15–25 ships (with slew overhead) instead of committing to one staring spot.

---

## Closest Prior Art Found and Distinguishing Features

| Prior art | What it discloses | How this invention differs |
|-----------|-------------------|---------------------------|
| **UrtheCast OptiSAR / SAR-XL** (eoPortal: https://www.eoportal.org/satellite-missions/optisar ; IEEE 7944492: https://ieeexplore.ieee.org/document/7944492/) | Tandem pairs of *separate* SAR and optical satellites. The leading SAR detects targets and passes positions to the trailing optical satellite about 2 min later. The SAR satellite also carries a cloud camera for cloud avoidance by the optical satellite. | The cue direction is reversed (a passive TIR sensor cues the SAR), everything is on one bus, the latency is seconds and the cue lies inside the SAR access window. Most importantly, the transferred quantity is a **velocity vector with covariance**, and it is used to set **squint, beam trajectory, dwell and Doppler/range-gate** parameters. OptiSAR transfers position only, for re-tasking. |
| **ICEYE tip-and-cue** (https://www.iceye.com/blog/tip-and-cue-technique-for-efficient-near-real-time-satellite-monitoring-of-moving-objects) ; **Synspective multi-sensor tip & cue** (https://synspective.com/blogs/2025/kumar_blog2/) ; Wikipedia overview (https://en.wikipedia.org/wiki/Tip_and_cue) | Ground-in-the-loop cueing of SAR from AIS, RF or other sensors, with a latency of minutes to hours, to *locate* objects. | No on-bus TIR kinematics and no aperture-geometry optimization. Cueing gives a location for a later collection, not the motion parameters of the current aperture. |
| **Sentinel-2 inter-band parallax velocity** (Heiselberg, *Sensors* 2019, 19(13):2873, https://www.mdpi.com/1424-8220/19/13/2873 ; Binet et al., ISPRS Annals V-1-2022, https://isprs-annals.copernicus.org/articles/V-1-2022/57/2022/) | Estimates ship and aircraft velocity from the time lag between staggered optical bands (up to about 2.6 s), in ground post-processing. | This invention deliberately enlarges the along-track field separation to 10–20 s so that velocity is accurate enough for SAR focusing. It works in TIR for day and night, runs onboard in real time and **feeds the result forward to control a different instrument's acquisition**. |
| **US 8,094,886 B1 - Thermal wake/vessel detection technique** (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8094886) | Detects vessels, and their location and motion from thermal wakes, in IR imagery. | Detection and characterization only. There is no SAR, and no use of the result to set radar acquisition parameters. This invention uses wake heading only as an optional fusion input (a dependent claim). |
| **SAR moving-ship refocusing literature** (e.g., minimum-entropy refocusing, *Sensors* 2019, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6427439/ ; time-frequency velocity estimation, *Sensors* 2026, 26(3):832, https://doi.org/10.3390/s26030832 ; Gaofen-3 dual-channel GMTI, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5713135/) | Estimates target motion *from the SAR data itself* after collection and compensates it in processing. | This invention obtains motion *before* collection from an independent passive sensor and changes the *collection itself*: squint that nulls v_r, a moving beam center and uncertainty-sized dwell. The post-hoc methods can still be used as a narrow residual step. |
| **US 4,546,355 - Range/azimuth/elevation ship imaging for ordnance control** (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4546355) ; **US 7,589,662 B1 - SAR systems and methods (Optimal SAR Receiver Path)** (https://patents.google.com/patent/US7589662) | Airborne SAR imaging of translating ships, and trajectory planning of an airborne SAR platform for good imaging of a target. | Airborne platforms can manoeuvre freely and have no orbital TIR pre-look. The prior art has no second-modality velocity prior, no squint-nulling within the constraints of a fixed Keplerian pass and no covariance-driven dwell sizing. |
| **Patsnap SAR patent landscape 2026** (https://www.patsnap.com/resources/blog/articles/sar-technology-landscape-2026-74-patent-analysis/), including Chinese target-trajectory-based SAR task planning (CETC 54, GEO SAR) | Mission-level planning of SAR tasks using target trajectories, generally from AIS or tracks. | That work is task scheduling across passes and orbits. This invention sets aperture-level radar parameters from an on-bus TIR velocity measured seconds earlier, in LEO. |

**Distinguishing combination (core novelty):** (a) a passive TIR sensor on the *same bus* with (b) two deliberately separated along-track pre-look fields that yield (c) a per-target velocity vector *and covariance* seconds before (d) the SAR aperture, which (e) is converted into a squint that nulls radial velocity, a moving beam-center trajectory and a dwell time sized to the velocity covariance.

---

## Why Non-Obvious

- **The default design direction is the opposite.** The industry treats SAR as the all-weather *cuer* and optical or IR as the *cued* sensor (OptiSAR, dark-vessel workflows). Using a lower-resolution, weather-limited passive sensor to steer an all-weather radar runs against that practice.
- **Squinting to null radial velocity is counter-intuitive.** SAR designers avoid squint because of range-cell-migration coupling, ambiguities and resolution loss. Choosing a squint *per target*, with the target's own velocity as the cost function, needs knowledge that no SAR normally has before collection.
- **The TIR field separation is set by what SAR focusing needs.** The along-track angular separation (10–20 s baseline) comes from the FM-rate error budget of the downstream SAR aperture, not from any TIR imaging need. A TIR designer would not create this separation, and a SAR designer would not expect to receive the information.
- **Dwell sized to covariance.** Tying coherent integration time to the covariance of an independent sensor's velocity estimate (T = 1/√(2σ_ΔKa)) is a new control law. Conventional systems fix dwell by product tier (resolution) regardless of whether the target is moving.
- **The effect is synergistic.** The TIR adds no resolution on its own. The SAR's resolution on moving targets improves by about 4× in the example only because of the combination.

---

## Draft Claims

### Independent method claim

**1.** A method of acquiring synthetic aperture radar (SAR) imagery of a moving surface target from a spacecraft in low Earth orbit, the spacecraft carrying a SAR instrument and a thermal-infrared (TIR) imager, the method comprising:
(a) acquiring, with the TIR imager at a first time, a first thermal image of a region within an access region of the SAR instrument and ahead of a zero-Doppler plane of the SAR instrument;
(b) acquiring, with the TIR imager at a second time later than the first time by a time baseline, a second thermal image of at least part of the region, also ahead of the zero-Doppler plane;
(c) detecting, by an onboard processor, a thermal signature of the target in each of the first and second thermal images, and computing from the displacement of the thermal signature between them a ground velocity vector of the target and an uncertainty of the ground velocity vector;
(d) determining, by the onboard processor and from the ground velocity vector and its uncertainty, at least one SAR acquisition parameter for a synthetic aperture that includes the target and is collected during the same orbital pass, the at least one SAR acquisition parameter being selected from an azimuth squint angle, a time-varying beam-center trajectory, a coherent dwell time, a range-gate timing offset, and a Doppler-centroid setting; and
(e) acquiring the synthetic aperture with the SAR instrument using the at least one SAR acquisition parameter.

### Independent system claim

**2.** A spacecraft Earth-observation system comprising:
a spacecraft bus configured for low Earth orbit;
a SAR instrument mounted on the bus and having electronically or mechanically controllable azimuth steering and programmable timing;
a TIR imager mounted on the bus and having at least a first field and a second field, the first and second fields being separated in the along-track direction and both pointed into the SAR instrument's access region ahead of its zero-Doppler plane, such that a surface point is imaged by the first field and then by the second field after a time baseline of at least 5 seconds;
an onboard processor configured to detect a moving target in imagery from both fields and to compute a ground velocity vector of the target and its covariance; and
a SAR mode controller configured to compute, from the ground velocity vector and its covariance, a command set for the SAR instrument comprising at least an azimuth squint angle and a coherent dwell time for a synthetic aperture that includes the target, and to issue the command set to the SAR instrument before the target enters the SAR beam on the same orbital pass.

### Dependent claims

**3.** The method of claim 1, wherein the azimuth squint angle is chosen to make the ground-projected radar line-of-sight vector at aperture center substantially orthogonal to the ground velocity vector, so that the target's radial velocity is substantially zero, subject to a maximum squint limit of the SAR instrument.

**4.** The method of claim 1, wherein the coherent dwell time T is selected such that the residual quadratic phase error from the uncertainty of the target's velocity component parallel to the spacecraft ground track stays below a threshold. The dwell time satisfies approximately T ≤ 1/√(k·σ_ΔKa), where σ_ΔKa is the azimuth FM-rate uncertainty derived from the velocity uncertainty and k is a confidence factor.

**5.** The method of claim 1, wherein the time-varying beam-center trajectory follows a predicted position of the target obtained by propagating the ground velocity vector from the second time through the synthetic aperture.

**6.** The method of claim 1, wherein the thermal signature is classified by brightness temperature into at least an underway class, indicating engine exhaust, and a non-underway class, and wherein the SAR acquisition parameters of claim 1(d) are computed only for targets in the underway class, with non-underway targets acquired with static-scene parameters.

**7.** The method of claim 1, further comprising detecting in at least one thermal image a thermal wake associated with the target, and fusing an axis orientation of the thermal wake with the displacement-derived ground velocity vector to reduce the uncertainty of the target's heading.

**8.** The method of claim 1, further comprising writing the ground velocity vector and its uncertainty into metadata of the SAR raw data, and focusing the SAR raw data by first applying a deterministic azimuth FM-rate correction computed from the ground velocity vector and then applying an autofocus limited to a search interval derived from the uncertainty.

**9.** The method of claim 1, wherein a plurality of moving targets are detected in the first and second thermal images, and an onboard scheduler allocates sequential synthetic apertures of individually determined squint angles and dwell times among the targets within the SAR access window of the pass, trading the dwell time of each target against the number of targets imaged.

**10.** The method of claim 1, further comprising measuring, from the acquired synthetic aperture, a Doppler-centroid anomaly or an along-track interferometric phase of the target, updating the ground velocity vector with that measurement by a recursive estimator, and using the updated vector to set acquisition parameters for a subsequent synthetic aperture of the same target or of a target in convoy with it.

**11.** The system of claim 2, wherein the first and second fields are two windows on a common TIR focal plane behind a single telescope, their angular separation is at least 5° along-track, and it is calibrated on orbit against static surface features.

**12.** The system of claim 2, wherein the SAR mode controller further sets a pulse-repetition frequency and a data-window position such that the Doppler band of the target, shifted by its predicted residual radial velocity, lies within the unambiguous azimuth band and the target's range history lies within the recorded range window.

**13.** The method of claim 1, wherein the time baseline is at least 10 seconds and the ground velocity vector uncertainty is at most 0.5 m/s (1σ) for targets with thermal contrast of at least 1.5 K above the surrounding surface.

---

## Commercial Use Cases

- **Maritime domain awareness and dark-vessel characterization.** Sub-meter SAR "fingerprint" imagery of moving, non-AIS vessels day and night. Superstructure, length, beam and deck cargo are focused and correctly geolocated for identification.
- **Illegal, unreported and unregulated (IUU) fishing enforcement.** Tells actively steaming or trawling vessels (hot stack, speed profile) from drifting ones, with well-focused SAR for vessel-type classification.
- **Sanctions and ship-to-ship transfer monitoring.** Slow-moving pairs at 1–4 kn are measured accurately enough to tell transfer operations from anchoring.
- **Port and strait throughput analytics.** Per-vessel speed and heading from TIR plus high-resolution SAR, sold as an analytics product.
- **Land extension.** Trains, convoys and aircraft on taxiways, all of which have strong thermal signatures from engines and brakes.
- **Hardware differentiator for SAR+TIR smallsats** (combining Umbra/Capella/ICEYE-class SAR with Hydrosat/SatVu/OroraTech-class TIR), with defensible IP on the fused acquisition mode.

---

## Known Weaknesses / Risks to Patentability

1. **Obviousness combination risk.** An examiner may combine OptiSAR (on-orbit cross-cueing), Sentinel-2 parallax velocity estimation and SAR moving-target compensation literature. Mitigations: claim the *squint-nulling from the velocity vector* and the *covariance-sized dwell*, which none of these references teaches, and argue the teaching-away of the SAR-cues-optical norm.
2. **Clouds block TIR.** The pre-look fails under cloud (about 60–70% global ocean cloud fraction). The invention helps only in clear or partly clear conditions and falls back to static-scene parameters otherwise. The value claim must be presented as opportunistic.
3. **Ship motion beyond constant velocity.** Pitch, roll, yaw and manoeuvring during the 10–25 s from pre-look to aperture limit focus regardless of the prior. A residual narrow autofocus is still needed.
4. **Agility limits.** Nulling v_r for ships heading close to cross-track needs very large squints (over 30°), which are impractical. The claim should allow partial nulling up to the squint limit, as claim 3 does.
5. **Hot-spot centroid bias.** Exhaust plumes drift with the wind, which biases the centroid. Wake fusion (claim 7) and a plume model help but add complexity.
6. **SWaP and cost.** Adding a 0.3 m-class TIR telescope with a cooled or high-grade focal plane to a SAR smallsat is significant. The claims do not depend on a specific aperture size, so a smaller MWIR aperture with coarser GSD and a longer baseline is a fallback.
7. **Military prior art.** Classified or unpublished airborne EO/IR-cued SAR/ISAR ship-imaging practice may exist. Published airborne references such as US 4,546,355 are distinguishable on the orbital pre-look geometry and the squint/dwell control law.
8. **Divided infringement.** Detection runs onboard and focusing (claim 8) may run on the ground. Keep independent claims limited to onboard steps.

---

## Sources

- https://www.eoportal.org/satellite-missions/optisar
- https://ieeexplore.ieee.org/document/7944492/
- https://www.iceye.com/blog/tip-and-cue-technique-for-efficient-near-real-time-satellite-monitoring-of-moving-objects
- https://synspective.com/blogs/2025/kumar_blog2/
- https://en.wikipedia.org/wiki/Tip_and_cue
- https://www.mdpi.com/1424-8220/19/13/2873
- https://isprs-annals.copernicus.org/articles/V-1-2022/57/2022/
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8094886
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6427439/
- https://doi.org/10.3390/s26030832
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5713135/
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4546355
- https://patents.google.com/patent/US7589662
- https://www.patsnap.com/resources/blog/articles/sar-technology-landscape-2026-74-patent-analysis/
- https://science.nasa.gov/earth-science/csda/vendor-hydrosat/
- https://www.satellitevu.com/
