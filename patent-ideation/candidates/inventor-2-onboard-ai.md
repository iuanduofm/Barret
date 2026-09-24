# Inventor 2 - Onboard AI / Autonomous Tasking Candidate

## Title

**Parallax-Aware Line-of-Sight Threading: Onboard 3D Cloud Reconstruction and Time-of-View Selection So an Agile LEO Imager Looks Through Gaps in Broken Cloud**

## Abstract

An agile low-Earth-orbit (LEO) imaging satellite carries a low-resolution, forward-tilted look-ahead camera and an edge-AI processor. Successive overlapping look-ahead frames see each upcoming ground region from three or more along-track view angles. Onboard, the processor segments cloud and jointly solves for cloud-top height, cloud base (or thickness) and cloud-level wind by multi-angle parallax. The result is a short-lived, advected 3D cloud-slab model. For each candidate target, the processor treats clouds as volumes at altitude, not as a 2D ground mask. It computes the target's *cloud-layer transit locus*: the path along which the line of sight (LOS) from target to spacecraft crosses the cloud slab as the spacecraft moves through the access window. To first order, this locus is the sub-satellite ground track scaled by h/H about the target. The processor then finds the sub-intervals of the access window in which the whole slab-crossing segment of the LOS lies inside predicted clear air. It schedules and steers the primary high-resolution acquisition into those intervals. For area targets, it picks a small set of view times whose clear-pixel footprints together cover the area of interest (AOI), and fuses them onboard. The result is a clear image of a target whose nadir-projected cloud mask says "cloudy", in broken low-cloud conditions where 2D look-ahead cloud avoidance fails.

## Problem Addressed

1. **Broken low cloud (cumulus, stratocumulus) is the dominant loss mode for very-high-resolution (VHR) tasking.** In these conditions scene-level cloud fraction is 20-60%, but gaps of 0.3-3 km exist. Industry figures say roughly 50-80% of acquired VHR images are rejected for cloud (see US 9,126,700 and US 11,037,011 background).
2. **Today's onboard cloud avoidance is 2D.** ESA Phi-Sat-1/2, KP Labs, Satellogic, Planet Pelican and JPL Dynamic Targeting (DT) on CogniSAT-6 all label cloud pixels on a ground-projected grid. They then either discard the image or retarget to ground cells labelled clear. JPL DT scores cloud-avoidance utility per ground pixel of a cloud mask.
3. **At look-ahead angles, a 2D mask is geometrically wrong at the scale of the gaps.** A 45 deg look-ahead is typical (CogniSAT-6 uses 40-50 deg). At that angle a cloud top at 1.8 km appears shifted about 2.1 km (h·tanθ, θ≈49.7 deg view zenith) from where it actually blocks a nadir view. That shift is larger than a typical cumulus cell or gap. A 2D mask georeferenced to terrain therefore gives almost random advice at sub-2-km scale.
4. **Whether a cloud blocks the view depends on the viewing geometry.** The same target can be blocked from one along-track angle and clear from another a few seconds later, because the LOS crosses the cloud layer at a different place. No fielded onboard system uses this degree of freedom. Agile platforms have ±30-45 deg pitch access, which gives a free choice of *when* in a roughly 120 s window to image. That freedom is currently spent only on scheduling convenience.
5. **Cloud advection over the 30-120 s look-ahead latency is about 0.3-1.2 km** at 10 m/s wind. This is comparable to gap size, and 2D look-ahead schemes do not model it.

## Detailed Description

### System blocks

| # | Block | Example implementation |
|---|---|---|
| B1 | **Primary imager**: VHR pushbroom (TDI) or framing camera | 0.5 m GSD at 500 km, 10 km swath |
| B2 | **Look-ahead multi-angle camera (LMC)**: one forward-tilted wide-field framing camera, boresight +38 deg pitch, along-track FOV ±10 deg, cross-track FOV ±12 deg, RGB+NIR (or a single broad VIS band plus a 1.38 µm cirrus band as an option) | 2k×2k CMOS, 20 m GSD after 2×2 binning, 1 frame every 2.5 s. Each ground point then appears in about 12-15 frames spanning view zenith ≈ 30-50 deg. A single-imager variant uses B1 itself in a look-ahead mode (as on CogniSAT-6), at a cost in duty cycle. |
| B3 | **Edge processor** | Jetson Orin NX / Myriad X / Versal class, 10-25 W |
| B4 | **Cloud segmentation network** (per LMC frame) | Lightweight U-Net, about 1-2 M parameters, INT8. Outputs P(cloud) and P(cloud-edge/side). |
| B5 | **Multi-angle 3D cloud solver** | Semi-global or learned stereo matching on cloud pixels across ≥3 LMC frames. Joint least-squares for cloud-top height h_t(x,y), along- and cross-track cloud-level wind (u,v), and cloud base h_b (or thickness) per cloud object. |
| B6 | **Advected cloud-slab model (ACSM)** | A 2.5D raster at 50 m cells over the next ~500 km of track. Each cell holds [h_b, h_t], P(cloud), (u,v) and a covariance. |
| B7 | **LOS transit-locus engine** | Per target and per candidate time t, it intersects the target-to-spacecraft LOS with the altitude band [h_b, h_t] and tests that segment against the ACSM advected to time t. |
| B8 | **Clear-window scheduler** | Picks acquisition start times, attitude profiles and (for area targets) a covering set of view times, subject to slew and settle limits, the maximum off-nadir angle, sun glint and a GSD penalty. |
| B9 | **Attitude control interface** | Sends quaternion or rate profiles to the ADCS. The profile is refreshed each time the ACSM updates. |
| B10 | **Onboard multi-view fusion (optional)** | Parallax-correct orthorectification of partial-clear strips using an onboard DEM, then per-pixel selection of the clear view. |
| B11 | **Ground uplink priors (optional)** | NWP fields for lifted-condensation level (LCL), cloud-base height and wind at 850/700 hPa. These act as Bayesian priors in B5. |

### Key geometric relation (core of the invention)

Let T be the target, S(t) the spacecraft position, and u(t) = (S(t) - T)/|S(t) - T| the LOS unit vector. The LOS reaches altitude h at the horizontal point

P_h(t) = T + h · tanθ(t) · â(t)

where θ is the view zenith angle at the target and â is the horizontal azimuth unit vector toward the spacecraft. In a flat-Earth approximation, P_h(t) ≈ T + (h/H)·(G(t) - T), with G(t) the sub-satellite point and H the orbit altitude. In words, **the cloud-layer transit locus is the ground track scaled down by h/H about the target**. For H = 500 km and h = 1.8 km the scale is 1/278. An 870 km access arc therefore maps to about 3.1 km of cloud layer that the LOS sweeps across. The LOS is clear at time t if and only if the segment {P_h(t) : h_b ≤ h ≤ h_t} does not intersect cloud in the ACSM advected to time t. The flight code uses the exact spherical-Earth θ(t).

### Method (step-by-step)

1. **Acquire the look-ahead stack.** The LMC images the upcoming track continuously. Each frame is tagged with time, attitude and ephemeris.
2. **Segment.** B4 produces cloud probability and cloud-edge maps for each frame (about 40 ms per frame on the NPU).
3. **Build multi-angle correspondences.** For every cloud object, B5 matches it across N ≥ 3 frames with different view zenith angles θ_1..θ_N at times t_1..t_N.
4. **Solve height and wind jointly.** The apparent along-track shift between frames i and j is Δx_ij = h·(tanθ_i - tanθ_j) + u·(t_i - t_j). tanθ is nonlinear in t, so with N ≥ 3 frames h and u separate. The cross-track shift gives v directly. B11 priors regularise the solve when conditioning is poor.
5. **Estimate cloud base / thickness.** Per object, the processor uses the best available of: (a) the LCL prior; (b) the side-wall extent seen in the most oblique frame (the vertical extent of the cloud edge in the P(edge) channel, divided by the sinθ scale); (c) the cloud-to-shadow offset under the known sun vector, which constrains the base of thin clouds; (d) a conservative default h_b = 0.5·h_t for convective cloud.
6. **Build the ACSM.** Clouds are rasterised as slabs [h_b, h_t]. Each is dilated by a 3σ margin that combines height, wind and matching error, and each carries (u,v).
7. **Compute the transit locus for each target.** For every target in the next access horizon (about 60-600 s), B7 samples t at 0.5 s steps. At each step it forms the LOS slab segment, advects the ACSM to t, and computes P_clear(t) as the product of (1 - P(cloud)) over the cells the segment crosses. Cells are treated as correlated within one cloud object.
8. **Extract clear windows.** Contiguous intervals where P_clear(t) ≥ τ (for example 0.8) and the duration is at least the dwell needed are recorded as candidate windows.
9. **Schedule.** B8 solves a small time-window selection problem (greedy or dynamic programming over targets) that maximises Σ value·P_clear·GSD-penalty(θ), subject to agility limits.
10. **Cover area targets.** If the AOI is larger than the gaps, B8 computes a per-AOI-pixel clear mask for each candidate view time and picks the minimum set of 2-3 view times whose union maximises clear AOI coverage (a greedy set cover).
11. **Close the loop.** Until the acquisition starts, newer LMC frames keep refining the ACSM. The window can shift by a few seconds, and the attitude profile is updated in time.
12. **Verify after capture.** A segmentation network runs on the primary image. The observed clear fraction is compared with the predicted P_clear and logged to calibrate τ and the margins. Where the product is still cloudy, the target is re-queued on the next pass or on a crosslinked follower satellite.
13. **Fuse and downlink.** For multi-view AOIs, B10 orthorectifies each strip with the DEM, selects clear pixels per location and downlinks the fused product plus a 3D cloud-occlusion quality layer.
14. **Hand off within the constellation (optional).** The ACSM (compact: about 10-50 kB per 100 km of track) is crosslinked to a trailing satellite on a different ground track. That satellite has a different transit locus and can image targets the leader could not see through.

## Worked Numerical Example

**Platform.** H = 500 km, ground-track speed 7.06 km/s, agile to ±40 deg off-nadir (view zenith up to about 43.9 deg). The along-track access half-width is about 434 km, so the window per target is about 123 s. Slew capacity is 2 deg/s with 1.5 deg/s² acceleration and 3 s settle time.

**Scene.** A 1 km × 1 km port facility sits 100 km cross-track from the ground track (roll about 11 deg). It is under trade-wind cumulus: 40% cover, cells 0.6-1.5 km across, gaps 0.3-1.0 km, cloud top 1.8 km, base 0.9 km, wind 8 m/s from the east.

**Look-ahead geometry.** The LMC sees the port at view zenith 50 → 30 deg, from about 80 s to about 41 s before the port's nadir time. That gives 15 frames at 2.5 s spacing. Two numbers bound what the solver has to recover:
- Parallax difference between the extreme frames: h·(tan49.7 - tan32.6) = 1.8 km × 0.54 ≈ 0.97 km. That is 49 pixels at 20 m.
- Wind displacement over 37 s: about 0.30 km.

Using 15 frames and matching accuracy of 0.3 px (6 m), the least-squares solve gives σ_h ≈ 60 m and σ_u ≈ 1 m/s (conservative, allowing for the conditioning of the h-u separation). Processing takes about 3 s on Orin NX: 15 frames × 40 ms segmentation plus about 1.5 s stereo on a 20 × 60 km cloud crop.

**Transit locus.** The LOS crosses the slab over horizontal offsets from P_0.9 to P_1.8:
- At t = -61 s (40 deg ahead): the slab crossing lies about 0.84-1.67 km north of the port and 0.18-0.36 km east of it.
- At nadir time: 0.18-0.36 km east (pure cross-track).
- At t = +61 s: 0.84-1.67 km south.

The LOS therefore sweeps a band of cloud layer about 3.3 km long and 0.2 km wide. At the upper slab boundary the crossing point moves at about 25 m/s near nadir, rising to about 35 m/s at the window edges. The slab-crossing segment is about 0.9 km × tanθ long along track: roughly 0.2 km near nadir and up to 0.87 km at the edges.

**Clear windows.** Take a 700 m gap about 0.2-0.9 km south of the port. Advected at 8 m/s, it lies under the LOS from about t = +8 s to t = +27 s, a window of roughly 19 s. Imaging a 1 km AOI takes about 0.15 s, plus about 5 s for pitch slew and settle. **This window is easy to hit.** The nadir-projected (2D) mask shows a cloud cell over the port at every time in the window. A 2D-DT scheduler would skip the port or take a cloudy image.

**Statistical benefit.** The cloud field decorrelates over about 1 km. The swept 3.3 km band therefore offers about 3 roughly independent LOS samples.
- Account for oblique views seeing cloud sides: effective cover rises from 0.40 at nadir to about 0.55 at θ = 40 deg. Averaged over the window, P(a given look is clear) ≈ 0.5.
- Blind or 2D-scheduled single look: P(clear) ≈ 0.5.
- With threading: P(at least one clear window exists and is found) ≈ 1 - 0.5³ ≈ 0.875. After a detection and prediction efficiency of about 0.85, that is about 0.74.
- **Yield gain for point targets under broken cumulus: about 1.5×.** For a 3 × 3 km AOI, two-view set cover raises the expected clear-pixel fraction from about 0.50 to about 0.80.

**Resources.**
- LMC: about 3 W, 0.4 kg.
- Processing: about 8 W average during look-ahead.
- ACSM memory: under 20 MB for a 600 km track band.
- No added downlink except the optional occlusion layer (under 1% of product size).

## Closest Prior Art Found and Distinguishing Features

| Prior art | What it discloses | Difference from this invention |
|---|---|---|
| **US 9,126,700 B2 / WO2011089477A1 / JP2013518246A** - Ozkul & Aldhafri, "Autonomous decision system for selecting target in observation satellites" ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9126700), [Google Patents](https://patents.google.com/patent/US9126700), [WO](https://patents.google.com/patent/WO2011089477A1/en)) | Several gimballed forward-looking preview cameras at different nadir angles (for example -15 to -45 deg) detect cloud cover over upcoming targets by radiance thresholding. A fuzzy-logic engine then picks which targets to image and in what order. | **Closest art.** It decides *which* targets to image from a 2D cloudy/clear verdict per target. It does not estimate cloud height, base or wind. It does not model the view-dependent LOS through a cloud slab. It does not choose the *time/angle within one target's access window* so the LOS passes through a gap. It does not compute a transit locus, predict advection, or cover an AOI with multiple views. |
| **JPL Dynamic Targeting (DT)** - Candela et al., "Dynamic Targeting for Cloud Avoidance...", ASTRA 2022 ([PDF](https://ai.jpl.nasa.gov/public/documents/papers/Candela-DT-ASTRA-2022.pdf)); "Flight of Dynamic Targeting on the CogniSAT-6 Spacecraft", arXiv:2509.05304 ([arXiv](https://arxiv.org/abs/2509.05304)); DT-Update ASTRA 2023 ([PDF](https://ai.jpl.nasa.gov/public/documents/papers/DT-Update-ASTRA-2023.pdf)); [JPL news 2025](https://www.jpl.nasa.gov/news/how-nasa-is-testing-ai-to-make-earth-observing-satellites-smarter/) | A 40-50 deg look-ahead image is analysed onboard (Myriad X CNN) in under 90 s, and a pointable primary instrument is steered toward clear ground pixels. Utility is set per pixel of a 2D cloud mask (for example 10 for clear, 1 for cloudy). | DT picks *which ground location* to observe from a ground-projected mask. The invention picks *from which viewpoint (time) to observe a fixed target*, using a 3D slab model. DT, as published, does not correct look-ahead parallax, estimate cloud height or wind from multiple look-ahead angles, or test LOS-slab intersection. Its gain comes from redirecting to other ground; ours comes from seeing the *same* ground past clouds. |
| **US 11,037,011 / EP 3571468 B1** - "Method for observing the surface of the earth and device for implementing same" ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11037011), [EPO](https://data.epo.org/gpi/EP3571468B1)) | A first system images a zone and splits it into mesh units. Units with no cloud or shadow are then imaged by a second (high-resolution) system. | Selection is per ground mesh unit on a 2D basis. There is no height or parallax model and no view-time optimisation. Cloudy mesh units are simply not imaged, whereas the invention images them through gaps. |
| **ESA Φ-Sat-1/-2** (KP Labs cloud app), [eoPortal](https://www.eoportal.org/satellite-missions/phisat-1), [ESA Φsat-2](https://www.esa.int/Applications/Observing_the_Earth/Phsat-2); **Satellogic/Palantir** onboard cloud models, [Palantir blog](https://blog.palantir.com/edge-ai-in-space-93d793433a1e); **Planet Pelican** Jetson onboard inference, [Via Satellite 2026](https://www.satellitetoday.com/imagery-and-sensing/2026/04/07/planet-details-ai-driven-object-detection-onboard-pelican-4-satellite/); **US 11,915,476** onboard AI cloud detection using PUS ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11915476)) | Onboard 2D cloud segmentation used to filter or prioritise downlink or to trigger re-tasking. | All run after capture or on a 2D mask. None drives pointing time from 3D cloud geometry. |
| **Multi-angle cloud-height science** - MISR stereo cloud-top height and wind ([NASA MISR](https://misr.jpl.nasa.gov/mission/misr-instrument/viewing-angles/)); cloud base from multi-angle data ([AMT 2019](https://amt.copernicus.org/articles/12/1841/2019/)); DIWATA-1 3D cloud reconstruction ([PMC7200711](https://pmc.ncbi.nlm.nih.gov/articles/PMC7200711/)); **US 11,657,597** cloud and shadow positions from cloud height and off-nadir angle ([USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11657597)) | Ground-processed retrieval of cloud height and wind from several angles, and parallax or shadow correction of *already-acquired* imagery. | These are retrieval or correction methods. None uses the 3D reconstruction *onboard, in real time, to drive the acquisition time or attitude of a separate high-resolution imager*. |
| **Agile-EOS scheduling literature** (for example [CN103983254A](https://patents.google.com/patent/CN103983254A/en); constraint-programming super-agile scheduling [arXiv:2601.11967](https://arxiv.org/pdf/2601.11967)) | Selecting imaging time windows under agility constraints, sometimes with cloud-forecast probability per target. | Cloud is treated as a per-target scalar probability. Within a pass it does not vary with view time. |

**Distinguishing features, summarised.**
- (i) Onboard multi-angle estimation of cloud height, base and wind from a look-ahead stack.
- (ii) A LOS/cloud-slab intersection test as a function of view time for a fixed target (the h/H-scaled transit locus).
- (iii) Scheduling the primary acquisition inside a sub-window where the LOS is clear, even though the target is cloud-covered in the nadir projection.
- (iv) Advecting the cloud model to the predicted acquisition time.
- (v) A multi-view set cover for area targets with onboard fusion.
- (vi) Crosslink of the 3D cloud model to satellites on other ground tracks.

## Why Non-Obvious

- **The field has framed the problem in 2D.** From US 9,126,700 (2011) through JPL DT (2022-2025) and Φ-Sat-2 (2024-2025), everyone asks "which ground location is clear?". The invention reframes it as "from which of my own future viewpoints is this particular ground location visible?". That reframing needs a 3D cloud model, which none of the art builds onboard.
- **A skilled person would expect parallax to be a nuisance to correct, not a resource.** Cloud-height parallax is treated in the literature as a geolocation *error* to remove from products. Deliberately exploiting the view-dependent LOS through a cloud layer as a scheduling variable goes against that teaching.
- **The key insight is not intuitive at first glance.** It is that the LOS transit locus is the ground track scaled by h/H about the target. That scale is tiny (about 1/280), yet at LEO speeds and 120 s windows the swept 3 km is exactly the scale of cumulus gaps. For very low cloud (under 0.3 km) or deep cloud (over 5 km), the feature is either useless or needs other margins. The designed operating regime is a specific, non-trivial result.
- **Combining MISR-style stereo with DT is not a simple bolt-on.** It needs:
  - separating height and wind from a single forward camera, via the nonlinear tanθ(t) across successive frames;
  - a base/thickness estimate, because top height alone gives the wrong clear test at oblique angles;
  - advection over the specific look-ahead latency;
  - a transit-locus scheduler.
  None of these is taught in the combination.

## Draft Claims

**Independent method claim**

1. A method of acquiring an image of a ground target from an agile imaging satellite in low Earth orbit, comprising:
 (a) capturing, with a look-ahead sensor of the satellite, a plurality of look-ahead images of a region containing the target at a plurality of different view angles before the target enters an access window of a primary imager of the satellite;
 (b) processing the look-ahead images onboard the satellite with a trained segmentation model to identify cloud features, and determining onboard, from apparent displacements of said cloud features among the look-ahead images at the different view angles, at least a cloud-top altitude for each of the cloud features;
 (c) generating onboard a three-dimensional cloud model comprising, for each cloud feature, a horizontal extent and an altitude interval bounded by said cloud-top altitude and a cloud-base altitude;
 (d) for each of a plurality of candidate acquisition times within the access window, computing onboard the segment of the line of sight between the target and the predicted satellite position at that candidate time which lies within the altitude interval, and determining a clear-line-of-sight metric from the intersection of said segment with the three-dimensional cloud model;
 (e) selecting an acquisition time for which the clear-line-of-sight metric meets a criterion, including when a nadir projection of the three-dimensional cloud model covers the target; and
 (f) commanding the attitude of the satellite so that the primary imager acquires the target at the selected acquisition time.

**Independent system claim**

2. An Earth-observation satellite system comprising:
 a primary imager;
 an attitude control system configured to point the primary imager at a ground target over a range of along-track view angles during an access window;
 a look-ahead sensor oriented to image the ground ahead of the satellite such that successive look-ahead frames observe a common ground region at different view angles; and
 an onboard processor configured to:
 (i) detect cloud features in the look-ahead frames with a neural network;
 (ii) estimate a cloud-top altitude and a cloud-base altitude of the cloud features from multi-angle parallax among the look-ahead frames;
 (iii) maintain a three-dimensional cloud model;
 (iv) for a ground target, evaluate as a function of time within the access window whether the line of sight from the target to the satellite, between the cloud-base and cloud-top altitudes, intersects the three-dimensional cloud model; and
 (v) issue to the attitude control system an attitude profile that places the acquisition of the target by the primary imager within a time interval in which said line of sight is predicted not to intersect the cloud model.

**Dependent claims**

3. The method of claim 1, wherein step (b) further comprises jointly estimating the cloud-top altitude and a horizontal cloud-motion vector from at least three look-ahead images. This uses the non-proportional variation of the tangent of the view zenith angle and of the capture time across said images. The method further comprises advecting the three-dimensional cloud model by the cloud-motion vector to each candidate acquisition time before step (d).

4. The method of claim 1, wherein step (d) computes the horizontal location at which the line of sight crosses an altitude h as the target position plus h·tan(θ(t)) along the view-azimuth direction. The set of such locations over the access window thus forms a transit locus corresponding to the satellite ground track scaled by approximately h/H about the target, where H is the orbit altitude.

5. The method of claim 1, wherein the cloud-base altitude is estimated onboard from at least one of: (i) the apparent vertical extent of cloud side-walls in the most oblique look-ahead image; (ii) the displacement between a cloud feature and its shadow under a known solar vector; (iii) an uplinked lifted-condensation-level or numerical-weather-prediction prior; and (iv) a predetermined fraction of the cloud-top altitude.

6. The method of claim 1, wherein the ground target is an area of interest larger than a characteristic cloud gap. The method further comprises: computing, for each candidate acquisition time, a per-location clear mask over the area of interest; selecting a set of two or more acquisition times whose clear masks together maximise clear coverage of the area of interest subject to agility constraints; acquiring the area of interest at each selected time; and fusing the acquisitions onboard into a composite image by parallax-corrected orthorectification and per-location selection of clear pixels.

7. The method of claim 1, further comprising repeating steps (a) through (e) with newer look-ahead images after an initial selection and before the acquisition, and updating the selected acquisition time and the commanded attitude profile accordingly.

8. The method of claim 1, wherein the look-ahead sensor is a single framing camera tilted forward in pitch whose along-track field of view is such that each ground point appears in at least three successive frames spanning a view-zenith range of at least 15 degrees.

9. The method of claim 1, wherein the clear-line-of-sight metric is a probability computed from per-cell cloud probabilities of the three-dimensional cloud model along the segment, with cells dilated by a margin derived from the estimated uncertainties of cloud altitude, cloud motion and image registration. The criterion is that the probability exceeds a threshold which is adaptively recalibrated onboard by comparing predicted clear probability with clear fraction measured in images subsequently acquired by the primary imager.

10. The method of claim 1, further comprising transmitting a compressed representation of the three-dimensional cloud model over an inter-satellite link to a second satellite with a different ground track, the second satellite performing steps (d) through (f) for targets not acquired clear by the first satellite.

11. The method of claim 1, wherein step (e) selects among multiple targets and acquisition times by maximising a sum of target value multiplied by clear-line-of-sight metric and by a view-angle-dependent resolution penalty, subject to slew-and-settle constraints of the attitude control system.

12. The system of claim 2, wherein the onboard processor is further configured to generate, with each image product, an occlusion-quality layer indicating for each pixel the predicted line-of-sight clearance and the estimated cloud-top altitude of any occluding cloud feature, and to prioritise downlink of products according to the measured clear fraction.

13. The system of claim 2, wherein the look-ahead sensor includes a spectral band at approximately 1.38 µm, and the processor assigns cirrus features a separate high-altitude slab in the three-dimensional cloud model.

## Commercial Use Cases

- **Commercial VHR tasking** (Maxar, Planet Pelican, Airbus Pléiades Neo, Satellogic): higher first-pass success under trade-wind and continental fair-weather cumulus. Fair-weather cumulus is one of the most common sky states over populated tropics and summer mid-latitudes.
- **Defence and intelligence point-target revisit**: port, airfield and facility monitoring where fixed-time collections are often lost to scattered cloud.
- **Disaster response**: after a tropical cyclone passes, broken convective cloud persists for days. The method images damaged infrastructure through gaps.
- **Agricultural and insurance field-level collection** in the monsoon season.
- **Constellation-as-a-service**: a leader satellite builds the 3D cloud model and followers use it (claim 10), creating licensing value across multi-operator constellations.
- **Retrofit on existing agile satellites** that already carry a look-ahead or star-tracker-class wide-field camera and an edge GPU, via a software upgrade plus pointing profile.

## Known Weaknesses / Risks to Patentability

1. **Obviousness combination.** An examiner could combine US 9,126,700 (multi-angle forward preview cameras), JPL DT (onboard look-ahead steering) and MISR (multi-angle cloud height and wind). The response rests on:
   - the specific LOS/slab intersection versus view time for a *fixed* target;
   - the base estimate and advection needed for it to work;
   - the explicit teaching in the art that parallax is an error to remove.
   Claim 1 should keep "including when a nadir projection covers the target" and the altitude-interval segment test.
2. **Unpublished military or classified art.** "Cloud-free line of sight" (CFLOS) probability modelling exists in defence literature and could include view-angle selection. That literature mostly concerns statistical planning on the ground, not onboard 3D reconstruction, but it should be searched in depth (DTIC, AFRL).
3. **Analogy to urban-canyon view-angle selection.** Choosing an off-nadir angle to see around buildings or into canyons is known. An examiner may treat clouds as "just another occluder". Clouds, however, move, must be reconstructed onboard in real time, and have an unknown base.
4. **Where it works.** The benefit is largest for low broken cloud (h about 0.5-3 km) and small gaps. It is minimal for overcast skies or very high thin cirrus. This narrows the commercial claim but not validity.
5. **Hard parts of the estimation.**
   - Cloud-base estimation is the weakest technical link. A wrong base gives wrong answers at oblique angles, which is mitigated by conservative dilation.
   - Separating height from along-track wind with a single forward camera is poorly conditioned when the view-angle spread is small.
6. **Enablement details a competitor could design around.** Examples: using only cloud-top height with a column assumption (base = 0), or using a ground-uplinked 3D cloud field from geostationary stereo. Dependent claims should cover the base = 0 variant and the case where the 3D model comes from any source, provided the time-selection step runs onboard.
7. **Crowded adjacent space.** Onboard cloud AI is heavily filed, especially in China (CN). A professional search of CNIPA full text for 云高 / 视线 / 成像时刻 (cloud height / line of sight / imaging time) combinations is recommended before filing.

## Sources consulted

- [US 9,126,700 (USPTO)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9126700) · [Google Patents](https://patents.google.com/patent/US9126700) · [WO2011089477A1](https://patents.google.com/patent/WO2011089477A1/en)
- [Candela et al., DT for Cloud Avoidance, ASTRA 2022](https://ai.jpl.nasa.gov/public/documents/papers/Candela-DT-ASTRA-2022.pdf)
- [Flight of Dynamic Targeting on CogniSAT-6, arXiv:2509.05304](https://arxiv.org/abs/2509.05304) · [ISAIRAS 2024 PDF](https://ai.jpl.nasa.gov/public/documents/papers/dt-isairas-2024.pdf)
- [JPL news: testing AI to make EO satellites smarter](https://www.jpl.nasa.gov/news/how-nasa-is-testing-ai-to-make-earth-observing-satellites-smarter/)
- [US 11,037,011 (USPTO)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11037011) · [EP 3571468 B1](https://data.epo.org/gpi/EP3571468B1)
- [US 11,915,476 onboard AI cloud detection (USPTO)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11915476)
- [US 11,657,597 cloud detection with height/off-nadir (USPTO)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11657597)
- [PhiSat-1/-2 eoPortal](https://www.eoportal.org/satellite-missions/phisat-1) · [ESA Φsat-2](https://www.esa.int/Applications/Observing_the_Earth/Phsat-2)
- [Palantir/Satellogic Edge AI](https://blog.palantir.com/edge-ai-in-space-93d793433a1e) · [Planet Pelican-4 onboard AI](https://www.satellitetoday.com/imagery-and-sensing/2026/04/07/planet-details-ai-driven-object-detection-onboard-pelican-4-satellite/)
- [MISR viewing angles](https://misr.jpl.nasa.gov/mission/misr-instrument/viewing-angles/) · [AMT 2019 cloud base from multi-angle](https://amt.copernicus.org/articles/12/1841/2019/) · [DIWATA-1 3D cloud reconstruction](https://pmc.ncbi.nlm.nih.gov/articles/PMC7200711/)
- [CN103983254A agile imaging](https://patents.google.com/patent/CN103983254A/en) · [Super-agile EOS scheduling, arXiv:2601.11967](https://arxiv.org/pdf/2601.11967)

Note: the full texts of the JPL DT papers and Google Patents pages could not be fetched (network egress blocked). The characterisations above come from search-result abstracts and excerpts, and should be confirmed against the full texts before filing.
