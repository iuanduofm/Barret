# Inventor 3 - Constellation Coordination Candidate

## Title

**Constellation-shared, advected three-dimensional cloud field for per-target line-of-sight and sunlit-ground selection of view geometry by a trailing agile imaging satellite**

(Short name: "3D Cloud Gap Threading")

---

## Brainstorm (5+ raw concepts considered)

| # | Concept | Verdict |
|---|---------|---------|
| 1 | A leader satellite sends a 2D cloud mask over ISL so a trailing optical satellite skips cloudy targets. | Rejected. Anticipated by IAI IL276014 (leading/trailing cloud mitigation), UrtheCast OptiSAR "CloudCam", JPL Dynamic Targeting. |
| 2 | A leader measures the radiance histogram or BRDF of each target and sends it ahead, so the follower pre-sets TDI stages, gain and exposure to avoid saturation over glint, snow or night lights. | Workable but weak: a small, obvious extension of on-board auto-exposure. |
| 3 | Inter-satellite predictive compression. A follower in the same plane, minutes behind, receives a compact reference from the leader and downlinks only the tiles that changed. | Interesting, but ISL bandwidth for the reference is heavy, and on-board change detection against a stored reference is already known. |
| 4 | A SAR leader detects ships and sends a kinematic track, and the optical follower images the predicted intercept. | Rejected. SAR-to-optical tip-and-cue is widely published (BlackSky, ICEYE partnerships, OptiSAR). |
| 5 | Several small satellites in formation image one scene at once from different angles, and the images are fused into a super-resolved product. | Known (multi-angle SR, distributed aperture). Also hard to phase. |
| **6** | **The leader builds a 3D cloud field (cloud-top/base height plus motion vectors) from multi-look stereo and advects it to the follower's future pass time. The follower ray-traces each candidate view vector, and the sun vector, through that field per target pixel. It then picks the look time, azimuth and zenith (or a complementary set of partial looks) that give the most ground that is both visible and sunlit.** | **Selected.** It uses the ISL to change how the imaging is performed (the view geometry), not just whether to image. It also fixes a real physical error in 2D-mask-based cloud avoidance. |
| 7 | A trailing SAR uses an optical leader's soil-moisture or vegetation map to choose polarization and incidence angle. | Plausible but niche. |

**Why #6 wins:** everyone doing cloud avoidance today (on one satellite or several) uses a **2D, nadir-projected** cloud mask and a yes/no decision. Broken cumulus has tops at 1-3 km. A very-high-resolution (VHR) imager looking 30 deg off nadir sees each ground point through the air column 0.6-1.7 km sideways, and the clouds cast shadows another 1-2 km away in the anti-solar direction. The 2D mask is therefore wrong for exactly the off-nadir, agile looks that make up most commercial collections. The error cannot be fixed on one satellite (a look-ahead camera on the same bus gives only about 60-90 s of lead and no second baseline). It needs a constellation partner whose own along-track multi-look gives both cloud height and cloud motion, delivered over an ISL before the follower's access window opens.

---

## One-paragraph abstract

A leading satellite and a trailing agile imaging satellite share, or nearly share, an orbital plane and are separated by a lead time of about 1-10 minutes. A cloud-sensing payload on the leader takes at least three along-track looks (fore, near-nadir, aft) of a corridor that includes the follower's upcoming targets. From the parallax between these looks, optionally constrained by thermal-IR brightness temperature, the leader works out a gridded three-dimensional cloud field: cloud-top height, cloud-base or thickness estimate, cloud motion vector, and a confidence value for each cell. The leader sends a compact, target-local form of this field to the follower over an inter-satellite link. For each queued target, the follower advects the field to each candidate acquisition time in its access window. It then traces two rays from each target ground cell through the field: one toward the follower's predicted position (line-of-sight occlusion) and one toward the sun (cloud-shadow occlusion). This gives a predicted *visible-and-sunlit fraction* for every candidate view geometry. An agility-constrained scheduler on board chooses the acquisition time, and therefore the view azimuth and zenith, that maximizes the value of the target weighted by that fraction. If no single look is good enough, the scheduler chooses two or more partial looks whose clear footprints complement each other. The follower's own images can then refine the field for satellites further back in the chain.

---

## Problem addressed

1. **Cloud avoidance uses the wrong geometry.** Existing leader-follower and look-ahead systems classify a target as clear or cloudy from a 2D, nadir-projected cloud mask. An agile VHR imager seldom looks at nadir; typical looks are 15-45 deg off nadir. A cloud whose top is at height *h* hides the ground point that lies *h*·tan(VZA) away along the view azimuth, not the point directly beneath it. At VZA 30 deg and *h* = 2 km, that offset is about 1.15 km, which is larger than typical fair-weather cumulus gaps (0.3-2 km). A target labelled "clear" in the 2D mask can be hidden at the chosen look angle, and a target labelled "cloudy" can often be seen by looking *through* a gap from the right direction.
2. **Cloud shadows are ignored.** Even where the line of sight is clear, ground in cloud shadow is 5-20x darker. That hurts SNR, analytics (change detection, object detection) and radiometric products. The shadow falls *h*·tan(SZA) away in the anti-solar direction. The view geometry decides whether the imager sees the shadows or whether they are hidden behind the clouds that cast them.
3. **Clouds move during the lead time.** At a lead time of 120 s and a steering-level wind of 10 m/s, clouds move 1.2 km. That shift is comparable to the gap sizes. A static leader mask is stale by the time the follower arrives.
4. **One-satellite look-ahead is limited.** A satellite that pitches forward to look ahead (e.g., JPL Dynamic Targeting on CogniSAT-6) gets about 60-90 s of lead from one extra look. That is not enough baseline or temporal diversity to separate cloud height from along-track cloud motion, and it costs the primary imager's time.
5. **Result:** commercial VHR operators routinely lose about 30-60% of optical collects in partly cloudy regimes to clouds or cloud shadow, even with weather-forecast-based tasking. Much of that loss happens in *broken* cloud, where usable views exist from some directions.

---

## Detailed description

### System block list

**A. Leading satellite ("scout")**
- A1. Cloud-sensing imager: a wide-swath VNIR camera (e.g., 3 bands: 0.49, 0.67, 0.86 um), 30-60 m GSD, cross-track swath ≥ the follower's field of regard (e.g., 800 km). Implemented as three fixed along-track-tilted pushbroom or framing heads at about +26 deg, 0 deg and -26 deg, as in MISR, or as a single framing camera taking repeated frames.
- A2. Optional LWIR microbolometer (8-12 um, about 100-200 m GSD). It gives cloud-top brightness temperature, which provides an independent height prior through a lapse-rate or NWP profile and is also used at night.
- A3. On-board processor (e.g., a radiation-tolerant FPGA/SoC or edge AI accelerator) running:
  - A3a. a cloud detection and optical-thickness classifier;
  - A3b. multi-look stereo matching that jointly solves for cloud-top height *h* and cloud motion vector **v** from three or more looks (the three-look solution separates along-track wind from height, as in the MISR stereo approach);
  - A3c. a cloud-base or thickness estimator (from shadow-to-cloud distance, a lifting-condensation-level prior, or the minimum top height in a local cluster);
  - A3d. a target-local field extractor, which extracts only the cells within a radius *R* of the follower's queued targets (the queue is sent up via ISL or ground).
- A4. Inter-satellite link terminal (optical ISL or S/X-band crosslink, ≥ 2 Mbps). A relay through a GEO/LEO data-relay network also works.

**B. Trailing satellite ("imager")**
- B1. Agile VHR imager (e.g., 0.3-0.8 m GSD, 10-15 km swath, field of regard ±45 deg).
- B2. Attitude control with control moment gyros (slew about 1-3 deg/s).
- B3. On-board processor running:
  - B3a. a **field advection module**, which moves each cell by **v**·(t − t_obs) and inflates the uncertainty with lead time (σ_pos² = σ_v²·Δt² + κ·Δt for cumulus growth/decay);
  - B3b. a **dual-ray occlusion tracer**. For each candidate time *t* in the access window it computes the satellite position, hence VZA(t) and VAZ(t), and the sun vector (SZA, SAZ). For each ground cell of the target it marches along both rays through altitude slabs [h_base, h_top] and gives the probability P_vis that the ray is not blocked and the probability P_sun that the ground is not shadowed;
  - B3c. a **utility evaluator**: U(target, t) = Σ_cells w_cell·P_vis·P_sun, plus optional penalties for GSD growth and atmospheric path length at high VZA;
  - B3d. an **agility-constrained scheduler**, which picks a sequence of (target, t) pairs, allowing several partial looks per target, to maximize Σ value·U within slew and settle limits;
  - B3e. a **feedback generator**, which compares the follower's own cloud detections with the prediction, updates **v** and *h* (e.g., with a Kalman update), and forwards the refined field to the next trailing satellite.
- B4. ISL terminal (receive, plus onward relay).

**C. Ground segment (optional)** - It uploads target queues and NWP wind/lapse-rate priors, and it receives prediction-vs-actual statistics for model tuning. It is not in the real-time loop.

### Step-by-step method

1. **Queue sharing.** The follower's current target queue (target IDs, centroids, polygons, value) is known to the leader, either uploaded from the ground or sent by the follower over ISL.
2. **Multi-look sensing.** At time t_L the leader passes over the corridor that the follower will see about Δt_lead later. Its fore, nadir and aft heads image each ground cell at three times separated by about 33 s (for 500 km altitude and ±26 deg tilt).
3. **3D retrieval.** For each cell with cloud, the leader solves the parallax equations of the three looks for (h, v_along, v_cross). The disparity between look *i* and look *j* equals h·(tanθ_i − tanθ_j) + v·(t_i − t_j). Three looks give two independent disparities in the along-track direction, and the cross-track displacement gives v_cross directly. The LWIR brightness temperature, when present, provides a prior or tie-breaker. Cloud base comes from the shadow offset or the LCL prior.
4. **Field packaging.** Only cells within R (e.g., 5 km) of each queued target are kept. Per 250 m cell the leader packs h_top (8 bit, 50 m steps), h_base (8 bit), an optical-thickness class (3 bit), v_x and v_y (6 bit each, 0.5 m/s steps), and confidence (3 bit): 34 bits per cell. A field-wide mean wind and a time stamp go in the header.
5. **Crosslink.** The package is sent over ISL, and the follower receives it at least T_plan (e.g., 20 s) before the access window of the first affected target.
6. **Advection.** For each target and each candidate time t_k (e.g., every 5 s across the access window), the follower shifts the field by **v**·(t_k − t_L) and inflates the uncertainty.
7. **Dual-ray tracing.** For each target ground cell g (e.g., a 50 m grid) and candidate t_k, the follower:
   - builds the view ray from g toward the follower's position at t_k, samples altitudes h in [h_base_min, h_top_max] in 100 m steps, and accumulates occlusion probability from the advected cells at horizontal offset h·tan(VZA) along VAZ;
   - builds the sun ray from g toward the sun and accumulates shadow probability at offset h·tan(SZA) along SAZ.
8. **Utility.** U(target, t_k) = mean over g of P_vis·P_sun. The best achievable union over multiple looks is also recorded: U_union({t_a, t_b}) = mean of [1 − (1 − p_a)(1 − p_b)] per cell.
9. **Scheduling.** A dynamic-programming or greedy-with-repair scheduler over all queued targets chooses (target, t_k, look count), subject to slew time between consecutive looks, dwell time, power and data volume. Targets whose best U is below a threshold (e.g., 0.15) are deferred to later passes and their slot is released.
10. **Execution.** The follower slews and collects. If it has a small context camera, a last-second check at the chosen t_k can confirm or veto the look.
11. **Feedback and relay.** The follower's collected images, or its low-resolution context frames, give an observed clear/shadow mask at a *different* view geometry from the leader's. This is a fourth look, and it refines h and v. The refined field is forwarded to the next trailing satellite in the chain (a daisy-chain), and the prediction residuals go to the ground for tuning.

---

## Worked numerical example

**Orbit and geometry.**
- Altitude 500 km, ground speed about 7.06 km/s.
- Leader lead time Δt_lead = 120 s, which is about 850 km along-track separation in the same plane.
- Leader heads at ±26 deg along-track tilt: the fore-to-nadir ground offset is 500·tan26 ≈ 244 km, so the look-to-look time is about 35 s and the three-look span is about 70 s.

**Height and wind retrieval accuracy.**
- VNIR GSD 30 m, stereo matching precision 0.3 px, so disparity precision is about 9 m.
- For the fore-minus-nadir pair (tan26 = 0.488), σ_h ≈ 9/0.488 ≈ 18 m from geometry alone.
- Once v_along is solved jointly from three looks, the combined σ_h is about 100-200 m and σ_v about 0.5-1 m/s (in line with MISR-class stereo retrievals, which have coarser pixels).
- Over Δt = 120-180 s, a wind error of 0.75 m/s gives a position error of about 90-135 m, plus a cumulus-evolution term. This is well below typical gap widths (0.3-2 km).

**ISL payload.**
- 40 queued targets × (10 km × 10 km neighbourhood) = 4,000 km², which is 64,000 cells at 250 m.
- At 34 bits per cell that is 2.2 Mbit (about 0.27 MB). Over a 10 Mbps optical ISL or relay this takes 0.22 s. Over a 2 Mbps S-band crosslink it takes 1.1 s.
- Leader processing latency is budgeted at 30 s (after the last look), and the follower has about 50 s of planning margin before the first access window.

**Follower access.**
- Target is 150 km cross-track from the follower's ground track. Candidate looks at t = −60, −30, 0, +30, +60 s relative to closest approach give off-nadir angles of 41.9, 27.4, 16.7, 27.4 and 41.9 deg (VZA at ground ≈ 45.7, 29.9, 18.2, 29.9, 45.7 deg). The view azimuths sweep from about 29 deg to 171 deg.
- Sun: SZA 40 deg, SAZ 150 deg.

**Scene and simulation.**
- Scene: broken fair-weather cumulus. 360 cells with radius 0.3-0.9 km in a 30 km × 30 km domain, base 1.0 km, tops 1.4-2.5 km, wind (8, −5) m/s.
- AOI: 3 km × 3 km, evaluated on a 25 m grid.
- Toy Monte-Carlo ray-trace by the inventor (Python, geometric slabs in 100 m steps). Results:

| Look t (s) | Off-nadir | VZA | View az | 2D-mask prediction (advected, nadir-projected) | 3D line of sight only | **3D visible AND sunlit** |
|---|---|---|---|---|---|---|
| −60 | 41.9° | 45.7° | 29° | 0.49 | 0.41 | **0.11** |
| −30 | 27.4° | 29.9° | 45° | 0.46 | 0.44 | **0.18** |
| 0 | 16.7° | 18.2° | 100° | 0.43 | 0.38 | **0.23** |
| **+30** | 27.4° | 29.9° | **155°** | 0.42 | 0.36 | **0.29** |
| +60 | 41.9° | 45.7° | 171° | 0.42 | 0.44 | **0.26** |

(The leader-time, un-advected 2D mask predicted 0.53 clear.)

**Interpretation.**
- The 2D approach overestimates the usable fraction by about 2-5x and ranks the looks wrongly. It favours t = −60 s (0.49 predicted), which in fact delivers only 0.11 sunlit, visible ground. A conventional "closest to nadir" rule picks t = 0 s and gets 0.23.
- The invention picks t = +30 s and gets 0.29: **+26% relative to the nadir rule and 2.6x relative to the 2D-mask-best choice.**
- The t = +30 s look has its view azimuth (155°) within 5° of the solar azimuth (150°). The follower looks from the sun side, so **cloud shadows lie behind the clouds that cast them**, and the occluded and shadowed areas overlap instead of adding together. This effect is invisible to any 2D mask, and the dual-ray tracer finds it automatically.
- Two complementary looks {+30 s, +60 s} give a union of **0.33**. That is a 45% gain over the single nadir-rule look, at a cost of one extra 30 s dwell-plus-slew.

**Throughput impact (illustrative).**
- Assume a 25% share of partly cloudy targets and a delivery threshold of "≥ 25% usable AOI or a customer-specified clear fraction".
- Converting about a quarter of the marginal cases from fail to pass adds roughly 5-8% effective collection capacity per follower.
- For a fleet of 20 VHR satellites at about $3-5k per delivered scene, that is several $M per year of recovered capacity. The added hardware is only a small scout satellite (or a hosted payload) per plane.

(Simulation code is inventor-internal. The numbers are illustrative of the geometry, not a validated performance claim.)

---

## Closest prior art found and distinguishing features

1. **IL276014A / IL276014B2 - "Satellite imaging system with reduced cloud obstruction" / "Cloud reduction in satellite imagery", Israel Aerospace Industries (inventor Eran Rosenthal).** https://patents.google.com/patent/IL276014B2/en , https://patents.google.com/patent/IL276014A/en
   - *Teaches:* a smaller leading satellite with an imaging subsystem detects clouds ahead of a larger trailing imaging satellite to mitigate cloud obstruction. **This is the closest prior art.**
   - *Differs:* from the available abstract, there is no disclosure of (a) retrieving cloud *height* and *motion* from multiple leader looks, (b) advecting the field to the follower's time, (c) per-candidate-view-vector ray tracing so that the *view geometry* (time, azimuth, zenith) of the follower is chosen, (d) sun-ray shadow tracing, or (e) complementary multi-look unions. *The full text could not be retrieved (patents.google.com blocked from this environment). A full-text review is needed before filing, and the family (possible US/WO equivalents) must be checked.*
2. **UrtheCast OptiSAR constellation - "CloudCam" on the leading SAR satellites streams cloud maps to trailing optical satellites for cloud avoidance.** https://www.eoportal.org/satellite-missions/optisar
   - *Differs:* it streams 2D cloud maps and avoids clouds by skipping or selecting targets. It has no 3D field, no advection, no view-geometry optimization and no shadow handling.
3. **JPL Dynamic Targeting (Chien, Candela et al.), flown on CogniSAT-6 in 2025.** https://arxiv.org/abs/2509.05304 ; Candela et al., "Dynamic Targeting for Cloud Avoidance to Improve Science of Space Missions", ASTRA 2022, https://ai.jpl.nasa.gov/public/documents/papers/Candela-DT-ASTRA-2022.pdf ; GEO-supplemented DT, https://arxiv.org/abs/2603.06719
   - *Teaches:* single-spacecraft look-ahead (pitch 40-50 deg forward), on-board cloud detection, and re-pointing of the primary instrument to avoid clouds, with 60-90 s of lead. The GEO variant uses GEO data for up to about 35 min of lead. JAXA's GOSAT-2 TANSO-FTS-2 uses a similar method operationally.
   - *Differs:* it is single-platform or GEO-sourced 2D cloud masks with no LEO partner stereo. Cloud height, parallax of the *follower's* line of sight, and shadow-ray tracing are not used to pick view azimuth and zenith. GEO pixels (2 km) cannot resolve cumulus gaps.
4. **US9001311B2 - "Using parallax in remote sensing to determine cloud feature height".** https://patents.google.com/patent/US9001311B2/en
   - *Teaches:* using parallax between detector portions to find cloud height.
   - *Differs:* it is a retrieval technique only. It does not use a constellation, crosslink to a second satellite or view-geometry selection. It is useful as a supporting reference for the leader's retrieval step (the invention does not claim the retrieval itself).
5. **US11010606B1 - "Cloud detection from satellite imagery"** (cloud detection from the temporal offset between two sensor arrays). https://patents.google.com/patent/US11010606
   - *Differs:* it concerns detection within one image product, not tasking a second satellite.
6. **MISR multi-angle stereo cloud-top height and cloud-motion retrieval** (Moroney, Mueller, Seiz et al.). https://misr.jpl.nasa.gov/mission/misr-instrument/viewing-angles/ , https://amt.copernicus.org/articles/12/1841/2019/
   - *Teaches:* joint height and wind from multi-angle views.
   - *Differs:* it is a science retrieval with no tasking use. It is prior art for step 3 alone.
7. **Agile-satellite scheduling under cloud uncertainty** (e.g., simulated annealing for multiple agile satellites under cloud coverage uncertainty, https://arxiv.org/pdf/2003.08363 ; CN103983254A agile imaging, https://patents.google.com/patent/CN103983254A/en).
   - *Differs:* these treat cloud as a per-target probability that does not depend on view geometry.
8. **Cloud-free line-of-sight (CFLOS) modelling for optical ground-to-satellite comms** (IEEE 7875453, https://ieeexplore.ieee.org/document/7875453/ ; all-sky-imager CFLOS, https://doi.org/10.3390/photonics13060515).
   - *Teaches:* a directional clear line-of-sight from a *ground station* looking up.
   - *Differs:* it is a different domain (communications, not ground imaging). There is no shadow term, no space-borne 3D field and no constellation relay. It is still an obviousness risk as a source of the "directional LOS" idea.

**Combined distinguishing features (the claim hook):** (i) the 3D field (height plus motion) comes from a *separate* leading LEO satellite's multi-look observations; (ii) it is advected to *each candidate acquisition time* of the follower; (iii) dual-ray (view plus sun) occlusion is traced *per target ground cell* for each candidate view vector; (iv) the result sets the follower's acquisition time, and therefore view azimuth and zenith, rather than a yes/no on the target; (v) optionally, complementary multi-look sets are selected by a per-cell union metric; (vi) optionally, the follower's own look is fed back and relayed down a daisy-chain.

---

## Why non-obvious

- **The field thinks in 2D masks.** Leader-follower cloud avoidance (IAI, UrtheCast) and look-ahead DT (JPL, JAXA) have existed for more than 5 years. All of them treat cloud as a 2D, nadir-projected yes/no attribute of a *target*. None treats it as an attribute of a *(target, view vector, sun vector, time)* tuple. Going from "is the target clear?" to "which direction through the 3D cloud field is clear and sunlit?" changes the decision variable.
- **The results are counter-intuitive.** The worked example shows that the 2D approach ranks looks in the *wrong order*, and that a steeper, more off-nadir look can beat the closest-to-nadir look. Operators normally penalize off-nadir angle, so a skilled person would not be expected to *prefer* it. The "sun-side view hides the shadows" effect (VAZ ≈ SAZ) does not arise from any single reference.
- **It needs a constellation.** A single satellite cannot get the multi-look baseline and lead time needed to separate height from wind without taking time from its primary mission. GEO cannot resolve sub-km cumulus gaps. The benefit only appears when a LEO scout's along-track stereo is paired with a follower's agile access window, and no reference suggests that pairing.
- **The pieces are scattered.** Joint height-wind stereo sits in atmospheric-science literature (MISR). Agile scheduling sits in operations research. CFLOS ray models sit in optical communications. Combining them needs the specific insight that a VHR follower's view-azimuth freedom is the control variable that exploits a 3D cloud field. That is a teaching-away pattern: in the scheduling literature, off-nadir angle is penalized, not optimized for occlusion.

---

## Draft claims

**Independent method claim**

1. A method of acquiring imagery of Earth from low Earth orbit using a plurality of satellites, comprising:
   (a) acquiring, by a cloud-sensing payload on a first satellite, at least two observations of a region containing a target at different along-track viewing angles and different times;
   (b) determining, from parallax between the at least two observations, a three-dimensional cloud field comprising, for each of a plurality of horizontal cells, at least a cloud-top height and a cloud motion vector;
   (c) transmitting data representing at least a target-local portion of the three-dimensional cloud field from the first satellite to a second satellite over an inter-satellite communication path, the second satellite having an imaging payload and an attitude-agile pointing capability and being scheduled to access the target after the first satellite;
   (d) for each of a plurality of candidate acquisition times within an access window of the second satellite to the target, each candidate acquisition time corresponding to a respective view zenith angle and view azimuth angle at the target: (i) advecting the three-dimensional cloud field to that candidate acquisition time using the cloud motion vectors, and (ii) computing, for each of a plurality of ground cells of the target, a probability that a ray from the ground cell toward the predicted position of the second satellite at that time is unobstructed by the advected cloud field;
   (e) computing, for each candidate acquisition time, an imaging utility from the probabilities of the ground cells; and
   (f) commanding the second satellite to point the imaging payload at the target and acquire imagery at at least one acquisition time selected, based at least in part on the imaging utility, from the plurality of candidate acquisition times.

**Independent system claim**

2. A satellite imaging system comprising:
   a first satellite in low Earth orbit comprising a cloud-sensing imager configured to observe a ground region at a plurality of along-track viewing angles, a first processor configured to derive from the observations a three-dimensional cloud field including cloud-top heights and cloud motion vectors, and a first inter-satellite communication terminal;
   a second satellite in low Earth orbit trailing the first satellite, comprising an agile imaging payload having a field of regard of at least ±20 degrees off nadir, a second inter-satellite communication terminal configured to receive the three-dimensional cloud field, and a second processor configured to:
   advect the received three-dimensional cloud field to each of a plurality of candidate acquisition times for a target;
   trace, for each candidate acquisition time and for each of a plurality of ground cells of the target, a view ray toward the second satellite's predicted position through the advected three-dimensional cloud field to obtain a visibility estimate;
   select, based on an aggregate of the visibility estimates, an acquisition time and corresponding pointing attitude; and
   command the agile imaging payload to acquire the target at the selected acquisition time and attitude.

**Dependent claims**

3. The method of claim 1, further comprising computing, for each ground cell and each candidate acquisition time, a probability that a ray from the ground cell toward the sun is unobstructed by the advected cloud field, wherein the imaging utility is based on a product of the view-ray probability and the sun-ray probability, such that ground cells in cloud shadow are penalized.

4. The method of claim 3, wherein, among candidate acquisition times having comparable view zenith angles, the selecting favours a candidate acquisition time whose view azimuth angle is within a threshold of the solar azimuth angle, such that cloud shadows are at least partly hidden behind the clouds casting them from the viewpoint of the second satellite.

5. The method of claim 1, wherein the at least two observations comprise at least three observations at a fore, a near-nadir and an aft viewing angle, and step (b) comprises jointly solving for the cloud-top height and an along-track component of the cloud motion vector for each cell.

6. The method of claim 1, wherein the three-dimensional cloud field further comprises a cloud-base height or a cloud geometric thickness for each cell, and computing the view-ray probability comprises sampling the ray at a plurality of altitudes between the cloud-base height and the cloud-top height.

7. The method of claim 1, wherein step (f) comprises selecting a set of two or more acquisition times for the same target whose predicted per-ground-cell visibilities are complementary, based on a union metric of the per-cell probabilities, and acquiring partial images at each acquisition time of the set for subsequent mosaicking into a composite image with a higher cloud-free and sunlit fraction than any single acquisition.

8. The method of claim 1, wherein the transmitting of step (c) comprises selecting, by the first satellite, only cells within a predetermined radius of targets in a target queue of the second satellite, the target queue having been received by the first satellite before step (a).

9. The method of claim 1, wherein advecting in step (d)(i) comprises inflating a positional uncertainty of each cell as a function of the elapsed time between the observations of step (a) and the candidate acquisition time, and the probability of step (d)(ii) is computed using the inflated positional uncertainty.

10. The method of claim 1, further comprising: detecting, from imagery acquired by the second satellite at the selected acquisition time, an observed occlusion pattern; updating the cloud-top heights and cloud motion vectors of the three-dimensional cloud field using the observed occlusion pattern as an additional viewing geometry; and transmitting the updated three-dimensional cloud field over an inter-satellite communication path to a third satellite trailing the second satellite.

11. The method of claim 1, wherein the imaging utility further includes a penalty that is an increasing function of view zenith angle representing ground-sample-distance growth and atmospheric path length, and the selecting of step (f) is performed jointly for a plurality of targets subject to slew-time constraints of the second satellite.

12. The method of claim 1, wherein step (b) further uses a thermal-infrared brightness temperature of cloud tops observed by the first satellite, together with a temperature-altitude profile, as a prior for the cloud-top height.

13. The method of claim 1, further comprising deferring the target to a later access opportunity, and releasing its time slot to another target, when the maximum imaging utility over the plurality of candidate acquisition times is below a threshold.

14. The system of claim 2, wherein the first satellite is a smaller satellite than the second satellite, is in substantially the same orbital plane, and leads the second satellite by a time between 60 seconds and 15 minutes.

15. The system of claim 2, wherein the second processor is further configured to trace a sun ray from each ground cell and to combine the visibility estimate with a sunlit estimate, and the selection maximizes an aggregate of combined visible-and-sunlit estimates.

16. The system of claim 2, wherein the inter-satellite communication terminals relay the three-dimensional cloud field through at least one intermediate relay satellite.

---

## Commercial use cases

- **Commercial VHR constellations** (e.g., Maxar WorldView Legion, Planet Pelican, BlackSky Gen-3, Airbus Pléiades Neo, Satellogic): recover partly cloudy collections, which adds several percent of fleet capacity and shortens time-to-first-clear-image for tropical and monsoon AOIs.
- **Defence and intelligence tip-and-cue:** higher probability of a usable look on the first pass over time-critical targets under broken cloud, where a second pass may be hours away.
- **Disaster response** (flood, wildfire aftermath under post-frontal cumulus): the first clear image arrives sooner.
- **Agriculture and insurance analytics:** fewer shadow-corrupted pixels in NDVI and change-detection time series. The shadow term matters as much as occlusion here.
- **Hosted "scout" service:** a small-satellite or hosted-payload operator sells 3D cloud-field streams over optical relay networks (e.g., SDA-style or commercial optical ISL relays) to other operators' VHR fleets. This is a heterogeneous, multi-operator business model.
- **Tasking marketplaces:** a view-geometry-aware clear-probability becomes a pricing input for "guaranteed clear" SLAs.

---

## Known weaknesses / risks to patentability

1. **IAI IL276014 family.** The full text has not been reviewed. If it discloses cloud height or re-pointing the trailing imager to an alternative angle, claims 1-2 narrow to the advection and per-ground-cell ray-tracing combination, and claims 3/4 (sun-ray shadow, and VAZ ≈ SAZ) become the key novelty. A search for US/EP/WO equivalents is needed.
2. **Obviousness combination.** An examiner could combine IAI/OptiSAR (leader → follower cloud info) + MISR (height and wind from multi-angle stereo) + textbook parallax geometry (offset = h·tanθ) + standard agile scheduling. The counter-argument rests on the change of decision variable to view geometry, the teaching-away (off-nadir penalized), and the unexpected results (2D ranking inverted, shadow-hiding azimuth). Strong claim drafting should lead with the per-cell dual-ray utility that drives time/azimuth selection.
3. **Alice/§101 risk.** Much of the method is computation. It is mitigated by claiming concrete acts: satellite attitude commands, acquisition, ISL transmission, and multi-look physical sensing.
4. **Physical performance uncertainty.** Cumulus cells evolve on 5-15 min timescales. At long lead times (> 5 min) the benefit falls off quickly. Thin cirrus is poorly handled by VNIR stereo. The worked example is a toy geometric simulation, not validated against real data. Enablement is fine, but the claimed advantage needs real-data evidence (e.g., simulation on MISR plus WorldView pairs) before relying on it in prosecution.
5. **Operational constraints.** It requires near-co-planar phasing (or a relay) and an on-board scheduler that can re-plan within about 30-60 s. Many operators still plan on the ground, and a ground-in-the-loop variant (relay to ground, replan, uplink) may be what is actually practised. A dependent claim, or a separate claim set, should cover ground-computed selection to avoid easy design-around.
6. **Design-around.** A competitor could compute an equivalent result from a single GEO/LEO NWP-assimilated 3D cloud product instead of a partner satellite's stereo. A broader continuation should cover "a three-dimensional cloud field derived from observations by at least one other space-borne sensor" without requiring stereo by the first satellite.

**Self-assessed patentability: 6/10.** Novelty over the known references looks solid for the combination. The main risks are a full-text surprise in the IAI family and a §103 combination attack. The sun-ray/azimuth dependent claims are the strongest fallback.
