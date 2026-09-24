# Inventor 1 (Optics / Focal Plane): Complementary-Coded Stage Accumulation in Digital TDI for Loss-Free, In-Band Sensing of Jitter Within the Integration Window

## Title

**Complementary-Coded Time-Delay-Integration Focal Plane That Measures Line-of-Sight Jitter Inside the Integration Window Without Losing Any Signal, and Corrects It On Board**

(Short name: CC-TDI)

## Abstract

A push-broom time-delay-integration (TDI) focal plane for a LEO Earth-observation satellite gives each of its N TDI stages a binary code bit from a balanced code (equal numbers of +1 and -1 stages). For a subset of "sensing columns", the photo-signal from each stage goes into the normal full-sum accumulator and, only for +1 stages, into a second "coded" accumulator. The full sum is the ordinary TDI image, so no light is lost. The coded difference D = 2*A - (A+B) is exactly zero for a scene that moves in perfect sync with the stages. When the line of sight moves during the integration window, D becomes a linear projection of the within-window displacement trajectory, weighted by the local scene gradient. Each output line gives one new projection, and the window slides by one stage per line. The sequence of D values is therefore the jitter trajectory convolved with the code. Codes are chosen so that their spectrum has no nulls across the microvibration band, and several codes are interleaved across column groups. That makes the convolution invertible, so an onboard estimator recovers the two-axis jitter trajectory at the TDI line rate (about 14 kHz) with a precision of about 0.01 pixel. It uses the imaging band itself: no extra detector, no second spectral band, and no frame readout. The estimate (a) drives the digital-TDI accumulation addresses in closed loop, (b) defines a known per-line point-spread function for residual deconvolution, and (c) is downlinked as a high-rate line-of-sight telemetry product.

## Problem addressed

1. **Microvibration sets the resolution limit for small LEO and VLEO imagers.** Reaction wheels, cryocoolers, solar-array drive mechanisms and thermal snap produce line-of-sight jitter from about 10 Hz to a few kHz. For a 0.5 m GSD camera at 500 km, one pixel is only about 1 µrad. A jitter of 0.3 px rms (0.3 µrad) inside the 4-5 ms TDI integration window lowers the Nyquist MTF to about 0.64. At 10-30 cm GSD (VLEO, Albedo-class systems) the tolerance is tighter still.
2. **Gyros and star trackers do not cover the band.** Their useful bandwidth is at most about 10-100 Hz, and their noise floor (about 0.1-1 µrad) is comparable to the jitter being corrected. Angular-rate sensors on the optical bench (for example MHD sensors) add mass, cost and alignment error, and they measure the bench, not the image.
3. **Existing image-based jitter detection runs on the ground, is band-limited, and misses frequencies.** The multispectral-parallax method (ZY-3, GF-9, Pleiades-class) uses the fixed time lag Δt between two spectral bands. Its transfer function is |2 sin(π f Δt)|, which has hard nulls at f = k/Δt. It needs two bands with co-registered content, and it only produces a correction after the ground processing.
4. **Frame-registration digital TDI needs high SNR in each frame.** Reading out and registering each short sub-frame before summation (digital-domain TDI-CMOS self-registration) fails in exactly the conditions where TDI is needed (low light, low contrast), because each sub-frame has only 1/N of the signal. It also multiplies readout bandwidth.
5. **Coded exposure (flutter shutter) costs light.** Raskar-style flutter shutters make motion blur invertible by closing the shutter about 50% of the time. That loses about 3 dB of signal, which is unacceptable for a photon-starved high-resolution imager.

The unmet need is a way to measure within-integration jitter at kHz bandwidth, on board, from the science band itself, with no signal loss and no added sensors.

## Detailed description

### Principle

Consider a digital-domain (or dual-register charge-domain) TDI array with N stages (rows) along track. The ground line k is seen by stage i at time t_k + iΔt, where Δt is the line period. With a line-of-sight displacement d(t) (a 2-vector, in pixels) and scene radiance s(x), stage i records approximately

 p_i = s(x_k + d(t_k + iΔt)) + noise.

Assign each stage a code value w_i ∈ {+1, -1}, balanced so that Σ w_i = 0. The standard TDI output is S_k = Σ_i p_i. The coded output is D_k = Σ_i w_i p_i. In hardware this is implemented as D = 2A - S, where A is an extra accumulator that adds only the stages with w_i = +1.

Linearising for small residual displacement:

 D_k ≈ ∇s(x_k) · Σ_i w_i d(t_k + iΔt)  (the Σ w_i s(x_k) term vanishes because the code is balanced)

So D_k / ∇s is a sample of the trajectory d **correlated with the code**: D = g · (w ⋆ d). The window slides by one Δt per output line, so the sequence {D_k} is a discrete convolution of the jitter with the time-reversed code. The standard image S_k is unchanged, because every photon still goes into S.

Key properties:
- **No light loss.** Unlike a flutter shutter, the code only partitions the stages. It never blocks them.
- **Self-nulling.** A static scene, or perfect TDI synchronisation, gives D = 0. The scene content cancels to first order, leaving only motion (plus calibrated fixed-pattern residue).
- **Trajectory, not a single shift.** Because the window slides, each new line contributes one new equation while one new unknown sample of d(t) enters the window. The trajectory is therefore recoverable at the line rate (about 14 kHz), not at the frame or integration-window rate.
- **No spectral nulls.** Balanced pseudo-random codes, optimised for minimum |W(f)| over the jitter band and interleaved across column groups, avoid the k/Δt nulls of two-band parallax and of the split-half comparison.
- **Two axes.** Along-track and cross-track displacement are separated by using the two components of ∇s over many columns with different gradient orientations (a weighted least-squares problem similar to optical flow).
- **Unobservable DC is handled by fusion.** Because Σ w_i = 0, a constant offset within the window is unobservable. The method measures relative motion within the window, which is exactly what causes smear. The low-frequency and absolute line of sight come from the gyro and star tracker and are fused in a complementary filter. The crossover is about 10-20 Hz.

### System block list

1. **Telescope** (for example a 0.5 m aperture, f = 5.5 m, f/11 TMA) forming the image on the focal plane.
2. **TDI focal plane array**: CMOS area or TDI sensor, N = 64 stages × 12,000 columns, 5.5 µm pitch, column-parallel ADCs (digital TDI). Or a CCD-in-CMOS charge-domain TDI with two parallel charge registers per column in the sensing columns (see claim 13).
3. **Code memory and stage-to-accumulator router**: stores M balanced codes w^(m) of length N (M = 4 in the example). It assigns code m to sensing-column group m, and in each line period it routes stage i's sample into accumulator A only if w_i^(m) = +1. The code may be changed per scene by command.
4. **Dual accumulator bank**:
   - the full-sum accumulator S (all columns; the existing TDI partial-sum memory);
   - the coded accumulator A (sensing columns only, for example 1,024 columns, which adds about 1.3 Mbit of SRAM).
5. **Per-stage gain and offset equaliser**: a digital PRNU/DSNU correction per row, applied before accumulation, so that the +1 and -1 stage groups are photometrically matched. It is calibrated from D over uniform scenes or from dark and flat frames.
6. **Scene-gradient estimator**: computes ∇s from the (already corrected) S image in a local window. It also selects the columns with the highest gradient information (texture-adaptive column selection, re-chosen every few hundred lines).
7. **Jitter trajectory estimator** (FPGA/SoC):
   - weighted least squares across sensing columns per line, giving the two-axis projections z_k = (w ⋆ d)_k;
   - a Kalman or Wiener deconvolution of the code, giving d̂(t) at line rate;
   - complementary fusion with gyro and star-tracker rates below the crossover frequency.
8. **Closed-loop accumulation-address controller**: uses the predicted d̂ to re-index which accumulator and which column each stage's sample is added to (integer part), and to trim the line-rate clock (along-track rate mismatch).
9. **Residual PSF generator and deconvolver**: for each output line, builds the known intra-window PSF h_k = Σ_i δ(x - d̂_res(t_k + iΔt)) and applies a local deconvolution or MTF restoration (on board or on the ground).
10. **Telemetry formatter**: downlinks S (the science image), d̂(t) (line-of-sight jitter at about 14 kHz on 2 axes, about 0.45 Mbit/s), a per-line quality flag, and optionally decimated D for ground re-estimation.

### Step-by-step method

1. **Configure.** Load M balanced codes w^(m) chosen to maximise min_f Σ_m |W^(m)(f)|² over the mission jitter band (for example 20 Hz to f_line/2). Assign them to interleaved sensing-column groups.
2. **Integrate.** At each line period Δt, read all N stages. Apply the per-row gain and offset correction. Add every stage sample to S. For sensing columns, also add stage i's sample to A if w_i = +1.
3. **Form the coded residual.** When ground line k completes its N stages, output S_k and compute D_k = 2A_k - S_k for the sensing columns.
4. **Build per-line measurement equations.** For each sensing column c with sufficient gradient: D_{k,c} = ∇s_{k,c} · (w^(m(c)) ⋆ d)_k + n. Solve in weighted least squares across columns for the two-axis projection vector z_k^(m) for each code group m.
5. **Deconvolve the code.** Run a Kalman smoother (state: d at line rate, plus a band-limited jitter model with optional known wheel harmonics) on the z_k^(m) streams. This gives d̂(t) with a fixed lag of about N lines, plus a causal prediction.
6. **Fuse** with gyro and star-tracker line-of-sight below about 15 Hz to obtain the absolute line of sight.
7. **Close the loop.** Use the causal prediction to shift the accumulation address of each incoming stage sample (integer pixels, both axes) and to trim the TDI line clock. This keeps the residual small, which also keeps step 4 in its linear regime.
8. **Restore.** For each output line, compute the residual intra-window PSF from the smoothed d̂ and apply space-variant deconvolution. Resample geometry for inter-line jitter.
9. **Monitor and downlink.** Downlink d̂(t) as a microvibration product. Flag lines where the gradient information is too low (water, cloud) so they use the gyro-only fallback.
10. **Recalibrate.** Use long-term statistics of D over uniform scenes to refresh the per-row gains (step 2). Optionally rotate codes between scenes to decorrelate fixed-pattern residue.

## Worked numerical example

**Orbit and optics**
- Altitude 500 km. Orbital speed 7.61 km/s, giving a ground-track speed v_g ≈ 7.06 km/s.
- GSD 0.5 m, pixel pitch 5.5 µm, so focal length f = 5.5 µm × 500 km / 0.5 m = **5.5 m**. IFOV = 1.0 µrad.
- 12,000 columns, giving a **6 km swath**.
- Line rate f_line = 7,060 / 0.5 = **14.12 kHz** (Δt = 70.8 µs).
- N = 64 stages, so the integration window T = 4.53 ms.

**Signal**
- Assume about 150 e⁻ per stage per pixel (typical radiance at f/11, 0.5 m). S = 9,600 e⁻, shot noise about 98 e⁻, read noise 64 × (5 e⁻)² folded in, giving σ_D ≈ **100 e⁻**. D = 2A - S has the same variance as S.
- Textured land: a local gradient of about 20% of signal per pixel gives g ≈ 30 e⁻ per pixel per stage.

**Code design** (computed numerically for this example)
- The best single balanced random 64-bit code found in a 3,000-code search has |W(f)| ≥ 1.6 from 20 Hz to 7 kHz, and an rms of 8.0 (= √N, as expected).
- **Four codes interleaved** over column groups give an effective per-column √(mean|W|²) ≥ **4.0 everywhere from 20 Hz to 7 kHz** (16.8 at 100 Hz).
- By contrast, a split-half code (the within-band analogue of two-band parallax) has an **exact null at 441 Hz** (= 1/(T/2)) and |W| = 1.1 at 3 kHz.

**Estimation noise**
- Per column per line: σ_d ≈ σ_D / (g · |W_eff|) = 100 / (30 × 4) = 0.83 px worst case (0.42 px typical).
- Averaging over K = 2,400 usable gradient-bearing columns (from 1,024 sensing columns × 2 gradient axes, plus rotation of column selection; conservatively K_eff ≈ 2,400) gives **0.017 px worst case** and **0.009 px typical** per 70.8 µs sample (full 7 kHz bandwidth).
- Restricted to a 1 kHz jitter band, this becomes about **0.006 px ≈ 6 nrad**, which is 1-2 orders of magnitude better than a spacecraft gyro in this band.

**Image-quality impact**
- Uncorrected jitter of 0.3 px rms inside the window: MTF_jitter(Nyquist) = exp(-2π²σ²f²) = exp(-2π² × 0.09 × 0.25) = **0.64**.
- Residual after closed loop plus deconvolution of about 0.05 px: MTF = **0.99**.
- This recovers about 35% of system MTF at Nyquist. The margin could instead be spent on 2× more TDI stages (+3 dB SNR) or on removing a passive microvibration isolator (about 2-5 kg on a 100-200 kg smallsat).

**Implementation budget**
- Extra accumulator memory: 1,024 columns × 64 partial sums × 20 bit ≈ **1.3 Mbit**.
- Internal D stream: 1,024 × 14.12 kHz × 16 bit ≈ 231 Mbit/s. This stays inside the FPGA and is not downlinked.
- Estimator compute: about 10 MAC per column per line, so about 150 MMAC/s plus a small Kalman filter. That is **< 1 W** on a radiation-tolerant FPGA or SoC.
- Science data rate is unchanged (12,000 × 14.12 kHz × 12 bit ≈ 2.0 Gbit/s before compression).
- Jitter telemetry: 2 axes × 14.12 kHz × 16 bit ≈ **0.45 Mbit/s** (or 0.06 Mbit/s decimated to 2 kHz).

**Degraded scenes**
- Over open ocean (g ≈ 3 e⁻/px/stage) the precision drops about 10× to about 0.1 px. The estimator flags these lines and blends to gyro-only or to the jitter model propagated from the last textured scene. Periodic wheel harmonics identified over land keep their phase through short low-texture gaps.

## Closest prior art found (with links) and distinguishing features

| # | Prior art | What it does | How CC-TDI differs |
|---|---|---|---|
| 1 | **US 9,967,490 B2 / EP 2 954 671 B1**, Teledyne e2v (Mayer, de Monte), "TDI image sensor with detection of travelling errors" / "Moving image sensor and summation having movement error detection". [US9967490](https://patents.google.com/patent/US9967490), [EP2954671B1](https://patents.google.com/patent/EP2954671B1/en) | Splits the pixel matrix along the columns into two sub-matrices (Ma, Mb), with extra laterally offset column groups. It compares their summed signals and picks the group pair that matches best, giving a *probable shift* (lateral or speed error). | (a) It uses a contiguous split, which is equivalent to our split-half code, and that has spectral nulls. CC-TDI uses balanced **pseudo-random, spectrally optimised, interleaved multi-code** stage partitions. (b) It gives a discrete best-match shift per readout. CC-TDI **inverts the code convolution along the sliding window** to recover a **continuous two-axis trajectory at line rate inside the integration window**. (c) It needs extra offset column groups. CC-TDI uses the ordinary columns and only one extra accumulator. (d) It does not teach PSF construction or deconvolution from the recovered intra-window trajectory, nor gyro fusion. |
| 2 | **US 11,210,766 B2** (Wuhan Univ.), jitter detection and image restoration for TDI-CCD satellite images; ZY-3 / GF-9 multispectral parallax papers. [US11210766B2](https://patents.google.com/patent/US11210766B2/en), [ZY-3 parallax](https://www.researchgate.net/publication/272390925_Attitude_Oscillation_Detection_of_the_ZY-3_Satellite_by_Using_Multispectral_Parallax_Images), [GF-9](https://www.researchgate.net/publication/325305274_High-frequency_attitude_jitter_correction_for_the_Gaofen-9_satellite), [ISPRS 2022](https://isprs-archives.copernicus.org/articles/XLIII-B1-2022/79/2022/isprs-archives-XLIII-B1-2022-79-2022.pdf) | Estimates jitter on the ground from the parallax between two spectral bands (or CCD overlap) with a fixed time lag. | Needs two bands and a fixed lag, so its transfer function |2 sin(πfΔt)| has nulls. It runs on the ground after the fact and cannot resolve motion *within* the TDI window. CC-TDI works in **one band, on board, in real time**, with **no nulls**, and at **intra-integration resolution**. |
| 3 | Digital-domain TDI-CMOS self-registration: "Realize the Image Motion Self-Registration Based on TDI in Digital Domain" (IEEE, 2019), and Sensors 2025, 25(11):3490 "Digital Domain TDI-CMOS Imaging Based on Minimum Search Domain Alignment". [IEEE 8796436](https://ieeexplore.ieee.org/document/8796436/), [MDPI](https://www.mdpi.com/1424-8220/25/11/3490) | Reads out area-sensor sub-frames, registers them by feature matching or correlation, then accumulates. | Registration works on *individual low-SNR frames* (1/N signal) and multiplies readout bandwidth. CC-TDI never reads out individual frames. It measures motion from **coded partial sums that already carry about N/2 stages of signal**, and it self-nulls scene content. |
| 4 | **Coded exposure / flutter shutter**: Raskar, Agrawal, Tumblin, SIGGRAPH 2006, and the associated MERL patents (e.g. US 7,580,620, "deblurring images using optimized temporal coding patterns"; number to be verified); Tendero, Morel, Rougé, "The Flutter Shutter Paradox", SIAM J. Imaging Sci. 2013 (applied to SPOT-5 / Pleiades simulations). [ACM](https://dl.acm.org/doi/10.1145/1141911.1141957), [SIAM](https://epubs.siam.org/doi/10.1137/120880665) | Blocks light with a binary temporal code, so the blur PSF is broadband and invertible *given a known or estimated velocity*. | The flutter shutter **discards about 50% of photons**, and Tendero et al. show it cannot beat a short exposure in SNR. CC-TDI **discards nothing**: the code *partitions* stages into complementary accumulators whose sum is the full TDI image. Also, flutter shutter uses the code to *deblur given the motion*. CC-TDI uses the complementary difference to *measure the motion* (the self-nulling scene cancellation has no counterpart in flutter shutter). |
| 5 | **US 2011/0115793 A1**, super-resolution digital TDI with Kalman-filtered motion estimates. [US20110115793A1](https://patents.google.com/patent/US20110115793A1/en) | Estimates frame-to-frame motion from full frames for digital-TDI super-resolution. | Frame-based, with no coded stage partition and no intra-window trajectory. |
| 6 | Charge-steering / multi-tap TDI and lock-in pixels (e.g. "Charge demultiplexing high-speed CMOS TDI", US 12,413,875; two-tap lock-in ToF pixels). | Demultiplexes charge for readout speed, or demodulates a modulated illumination. | None uses a *balanced pseudo-random stage code* to sense passive platform motion in Earth-imaging TDI. This is relevant only to the charge-domain dependent claim. |
| 7 | Event-based vision in space (Falcon Neuro on the ISS; arXiv 2606.01280 survey). [arXiv](https://arxiv.org/pdf/2606.01280) | Separate neuromorphic sensors, used among other things for jitter-robust star tracking. | Needs an extra sensor and optics path. CC-TDI uses the science focal plane itself. |

Commercial systems (Planet SkySat and Pelican, Maxar WorldView Legion, Satellogic NewSat/Mark V, Albedo, Pixxel, Jilin-1) are publicly described as using analog or digital TDI and/or frame-based super-resolution, plus mechanical isolation and gyros. No public disclosure was found of coded complementary stage accumulation for jitter sensing. The search was limited to public web and patent-search snippets. Full-text access to Google Patents and USPTO was blocked from this environment, so the full claim sets of #1 and #4 must be read before filing.

## Why non-obvious

1. **It uses the TDI stage stack as a coded temporal aperture for sensing, not for imaging.** TDI designers treat stage summation as something that should be *uniform* (for SNR) and *synchronous* (for MTF). Deliberately applying a ±1 pseudo-random weighting to the stages, even in a parallel channel, cuts against the design intuition of the field.
2. **Coded-exposure practitioners pursue the opposite goal.** Flutter-shutter work codes the exposure to *deblur a known motion*, accepts light loss, and has been analytically argued (Tendero-Morel-Rouge) to be SNR-inferior for satellites. That result steers a skilled person *away* from temporal coding in satellite TDI. The inventive step is to notice that (i) a complementary partition wastes no light, and (ii) the complementary difference cancels the scene and becomes a *motion sensor*, which reverses the purpose of the code.
3. **The sliding-window convolution structure is not apparent from either field alone.** The e2v travelling-error sensors compare two contiguous halves and pick a best-match shift. Nothing in them suggests that, because the TDI window slides one stage per line, the per-line coded residuals form a *convolution* of the trajectory with the code. Nor do they suggest that the code's *spectrum* then governs which jitter frequencies are observable. That is what motivates spectrally optimised, multi-code interleaving. The parallax literature treats its frequency nulls as an intrinsic limitation of band geometry, not as a design variable.
4. **The combination crosses three communities**: detector ASIC and TDI design (e2v, CMOSIS/ams), computational photography (Raskar, Morel), and satellite attitude-jitter geodesy (ZY-3 and GF-9 groups). None cites the others on this problem. A skilled person would also expect first-order scene cancellation to fail because of row PRNU. The per-row digital equalisation and on-orbit recalibration from D itself are what make it practical.

## Draft claims

**Independent method claim**

1. A method of imaging the Earth from a satellite in low Earth orbit, comprising:
 (a) forming an optical image of the Earth on a time-delay-integration (TDI) detector array having N stages arranged along a scan direction, such that a given ground line is observed successively by the N stages during an integration window;
 (b) accumulating, for each ground line and each of a plurality of detector columns, a full sum of the signals from all N stages to form a science image line;
 (c) for at least a subset of sensing columns, concurrently accumulating a coded sum in which the signal from each stage i contributes with a weight determined by a code value w_i of a balanced code having substantially equal total positive and negative weight, such that a coded residual derived from the coded sum and the full sum is substantially zero when the image is stationary relative to the stages;
 (d) computing, for a sequence of ground lines, coded residuals and forming measurement equations that relate each coded residual to a local scene gradient and to a correlation of the code with a line-of-sight displacement trajectory sampled at the TDI line period within the integration window;
 (e) estimating, by inverting said correlation over the sequence of successively overlapping integration windows, the line-of-sight displacement trajectory at a temporal resolution finer than the integration window duration; and
 (f) using the estimated trajectory to at least one of: (i) adjust, in closed loop, the accumulation of subsequent stage signals; (ii) restore the science image using a point-spread function derived from the estimated trajectory; or (iii) transmit the estimated trajectory as line-of-sight telemetry;
 wherein every stage signal contributes to the full sum, such that the coding introduces no loss of collected signal in the science image.

**Independent system claim**

2. An Earth-observation satellite imaging system, comprising:
 a telescope configured to form an image of the Earth on a focal plane;
 a TDI detector array at the focal plane having N stages along a scan direction and a plurality of columns;
 a code memory storing at least one balanced binary code of length N;
 a stage-to-accumulator router and a dual accumulator bank comprising, for each of a plurality of columns, a full-sum accumulator receiving all N stage signals, and, for a subset of sensing columns, a coded accumulator receiving stage signals selected or weighted according to the code;
 a jitter estimator configured to compute coded residuals from the coded and full-sum accumulators, to weight them by local scene gradients derived from the science image, and to deconvolve the code across successive ground lines to produce a two-axis line-of-sight displacement trajectory at the TDI line rate; and
 at least one of an accumulation-address controller, an image-restoration processor, and a telemetry formatter that consumes the displacement trajectory.

**Dependent claims**

3. The method of claim 1, wherein the coded sum is formed by an accumulator that adds only stages with code value +1, and the coded residual is computed as twice the coded sum minus the full sum.
4. The method of claim 1, wherein a plurality of different balanced codes are assigned to interleaved groups of sensing columns, the codes being selected to maximise the minimum over frequency of the summed squared code-spectrum magnitudes over a predetermined jitter frequency band, such that the combined measurement has no spectral null in that band.
5. The method of claim 4, wherein the predetermined jitter band extends from at most 20 Hz to at least 1 kHz and the TDI line rate exceeds 5 kHz.
6. The method of claim 1, wherein the subset of sensing columns is re-selected during imaging according to a scene-gradient information metric computed from the science image.
7. The method of claim 1, wherein step (d) comprises solving, per ground line, a weighted least-squares problem across sensing columns using both along-scan and cross-scan components of the local scene gradient, to separate along-track and cross-track displacement.
8. The method of claim 1, wherein step (e) comprises a Kalman smoother or Wiener deconvolution with a jitter model including at least one harmonic at a known or estimated rotation frequency of an onboard reaction wheel or cryocooler.
9. The method of claim 1, further comprising fusing the estimated trajectory with a gyroscope or star-tracker measurement in a complementary filter having a crossover frequency, the code-derived estimate being used above the crossover frequency.
10. The method of claim 1, wherein the closed-loop adjustment comprises shifting, for each stage signal, the accumulator row address and column address into which it is added by an integer number of pixels according to a predicted displacement, and trimming the TDI line clock according to an estimated along-track rate mismatch.
11. The method of claim 1, wherein restoring comprises constructing, for each science image line, a residual point-spread function as the sum of displacements at the N stage times, and applying a space-variant deconvolution.
12. The method of claim 1, further comprising applying a per-stage gain and offset correction to each stage signal before accumulation, and updating said correction from statistics of the coded residual accumulated over low-gradient scene regions.
13. The system of claim 2, wherein the TDI detector array is a charge-domain TDI array in which, for the sensing columns, photocharge from each stage is steered by a transfer gate into one of two parallel charge registers according to the code, and the full sum is formed as the sum of the two registers after readout.
14. The system of claim 2, wherein the code memory is reprogrammable by ground command and the code is changed between imaging scenes or rotated periodically to decorrelate fixed-pattern residuals.
15. The system of claim 2, wherein the telemetry formatter downlinks the displacement trajectory at a rate of at least 1 kHz per axis together with a per-line quality flag indicating scene-gradient sufficiency.
16. The system of claim 2, wherein a plurality of spectral bands each have their own TDI section with coded accumulation, and the jitter estimator jointly estimates a common line-of-sight trajectory from the coded residuals of all bands.

## Commercial use cases

1. **Removing mass and cost from high-resolution smallsats.** Passive or active microvibration isolators and high-bandwidth angular-rate sensors could be replaced, or their requirements relaxed. This targets 0.3-0.8 m class constellations (Satellogic, Planet Pelican, Pixxel hyperspectral TDI, BlackSky Gen-3, Jilin-1).
2. **VLEO ultra-high resolution** (Albedo-class, 10-30 cm GSD at about 250-350 km). Here 1 px ≈ 0.4-1 µrad, and wheel jitter is the dominant limit on MTF.
3. **Agile imaging while slewing.** Settle-time requirements after slews can be relaxed, because residual oscillation is measured and corrected, which increases collection capacity per orbit.
4. **Microvibration diagnostics as a product.** Line-rate line-of-sight telemetry supports on-orbit wheel health monitoring, in-orbit verification of the pointing budget, and automatic tuning of wheel speed zones.
5. **Hyperspectral and multispectral TDI band-to-band registration.** A common trajectory from claim 16 removes jitter-induced band misregistration without ground parallax processing.
6. **Licensing to detector ASIC vendors** (Teledyne e2v, Gpixel, ams-CMOSIS, Sony) as an on-chip feature. The extra silicon is one accumulator per sensing column plus a code register.

## Known weaknesses / risks to patentability

1. **Teledyne e2v's travelling-error patents (US 9,967,490 / EP 2 954 671) are the biggest risk.** If their claims read broadly on "two partial TDI sums from different stage subsets compared to detect motion", an examiner may argue that CC-TDI is an obvious generalisation (split-half → interleaved). The defence rests on: balanced pseudo-random spectrally-designed codes; sliding-window deconvolution to a line-rate trajectory; no light loss with the full sum preserved; and gradient-weighted two-axis least squares. The independent claims should keep limitations (d) and (e) (convolution inversion, sub-window resolution). Their full text has **not** been read (blocked from this environment) and must be reviewed.
2. **Flutter shutter plus e2v as a two-reference obviousness rejection.** An examiner could combine "temporal binary codes improve invertibility" (Raskar) with e2v's partial sums. The counter-argument is that Raskar teaches light-blocking codes for deblurring with known motion (a different purpose and a different result), and Tendero et al. teach away for satellites.
3. **Scene dependence.** Performance collapses over water, snow, cloud and uniform desert. This is mitigated by fusion and harmonic models, but prior art on gradient-weighted image-based motion estimation (optical flow) is extensive. Claims must not rely on the gradient-weighting step alone.
4. **Linearisation limits.** The method requires residual displacement well below 1 px inside the window, so it depends on the closed loop and on a reasonably quiet platform. Large-amplitude low-frequency motion must come from attitude control.
5. **Fixed-pattern noise.** Row-to-row PRNU mismatch between the +1 and -1 groups produces a scene-proportional false residual. It is corrected by calibration, but a critic could argue the residual floor (about 0.1% PRNU gives about a 0.01 px bias on high-contrast edges) limits the headline precision.
6. **Charge-domain variant maturity.** Dual-register steering in TDI CCD-in-CMOS is plausible but unproven. Claim 13 may attract enablement questions.
7. **Undisclosed internal practice.** Large primes (Maxar, Airbus) may already use similar in-house techniques without publishing them. That would not be prior art unless it was published or commercially disclosed, but it could surface as a public-use or on-sale issue.
