# Inventor 4 (VLEO / orbital dynamics): Ram visor that brakes while the satellite keeps imaging, and target-driven drag steering

## Title

**Torque-Balanced, Aperture-Forward Variable-Drag Visor and Target-Driven Drag-Steering Method for Continuously Imaging Very-Low-Earth-Orbit Satellites**

## Abstract

A VLEO Earth-imaging satellite carries a deployable visor on the ram side of its nadir-facing telescope aperture. The visor hangs toward nadir, ahead of the aperture and outside the imaging field of view. A zenith-side counter-flap moves with the visor so that the two drag forces produce no net pitch torque. By changing how far the visor is deployed, the spacecraft changes its ballistic coefficient continuously while it stays in its nominal nadir imaging attitude. The same visor also shields the aperture region from ram atomic-oxygen flux and blocks forward stray light. An onboard planner turns the tasking queue into a drag schedule. For each tasked target it works out the along-track timing offset that would bring the target inside the sensor's low-obliquity field of regard on a chosen future pass. The offset comes from Earth rotation: a timing offset Δt moves the ground track by about ω⊕·R⊕·cos φ·Δt. The planner then solves for a schedule that combines visor deployment and throttling of the aft, forward-only electric thruster. That schedule reaches the required offset, and the thruster later makes up the altitude lost. Existing differential-drag methods change drag by leaving the imaging attitude, and their goal is spacing between satellites in a constellation. This invention changes drag while imaging continues, balances the torque, and aims the drag at individual imaging targets. It also lets a satellite whose thruster can only push forward move its ground track in both directions without a 180° yaw flip.

## Problem addressed

1. **VLEO shrinks the field of regard.** At 250 km, a ±20° agility limit covers only about ±91 km of ground. At 500 km the same limit covers about ±182 km. Many VLEO designs are streamlined bodies with body-mounted arrays and high-inertia telescopes, such as Albedo Clarity-1 (3 m tall). Designers often limit roll further to hold drag area and aerodynamic torque down. As a result, a target that falls between adjacent ground tracks can wait days for a pass within reach. Revisit then depends on luck in the ground-track geometry, not on how many satellites are flying.
2. **VLEO EO satellites usually have one aft-facing, forward-only electric thruster** (for example, ion or Hall thrusters making up drag). They can raise the orbit or hold it, but they cannot produce a retrograde impulse without a 180° yaw flip. At VLEO that flip would put the optics, star trackers and any air intake into the ram flow of atomic oxygen, and it would stop imaging. So they can move phase in only one direction, and slowly: the fastest backward phasing available is to switch the thruster off and let natural drag work.
3. **Existing drag-modulation methods take time away from imaging.** Planet-style differential drag, for example, uses attitude modes, so the satellite spends orbit fractions in a high-drag attitude that is not an imaging attitude. At VLEO, where each satellite is expensive and pixels are valuable, that costs revenue.
4. **The optics are exposed to atomic oxygen.** Near 250 km, ram AO flux is about 10^15 atoms cm^-2 s^-1 at about 5 eV. Grazing and scattered flux reaches the aperture rim, the baffle interior and the front optics. Forward stray light from the sunlit limb and airglow near the terminator is also a problem.
5. **Drag surfaces placed away from the center of mass create a pitch torque that saturates the wheels.** For example, 1.85 mN at a 1 m arm fills a 0.5 N·m·s wheel in about 4.5 minutes. This is why nobody bolts a large drag flap to an imaging satellite and keeps imaging.

## Detailed description

### System blocks

| # | Block | Function |
|---|---|---|
| B1 | Nadir-pointing imaging telescope (push-broom or push-frame TDI) with a nadir aperture at the lower end of a streamlined bus whose long axis lies along the velocity vector | Primary payload |
| B2 | **Ram visor**: a flat or slightly curved panel hinged at the forward (ram) edge of the aperture baffle. A single-axis actuator swings it from stowed (flush with the bus, about 0 m² added frontal area) to fully deployed (hanging toward nadir, normal to the flow, frontal area ΔA_max). Its angle is continuously variable, δ ∈ [0°, 90°]. Its trailing edge stays outside the telescope's field-of-view cone, with a keep-out margin | Variable-drag actuator, AO shadow, forward stray-light baffle |
| B3 | **Zenith counter-flap**: a panel above the center of mass (CoM), sized and driven so that its drag moment cancels the visor's pitch moment: F_v·z_v = F_c·z_c. It may be split port/starboard so it can also trim yaw | Pitch-torque balance, so drag changes as a pure force |
| B4 | Flap mixer (software) | Maps the commanded Δ(C_D·A) to (δ_v, δ_c) so that the net pitch moment stays at zero. It uses an onboard free-molecular-flow panel model, updated with the aerodynamic-torque residual measured from wheel momentum |
| B5 | Aft electric thruster, throttleable, forward thrust only | Drag makeup and forward (west-shifting) phasing |
| B6 | GNSS receiver plus accelerometer or POD filter | Estimates atmospheric density and C_D·A online (drag nowcast) |
| B7 | **Target-to-timing converter** | For each target k and each candidate pass p, computes the required along-track timing offset Δt_k,p = Δλ_k,p / ω⊕, where Δλ is the longitude shift that brings the target within the chosen obliquity limit (or to nadir) at latitude φ_k |
| B8 | **Drag-steering planner** (receding-horizon MPC or MILP) | Chooses the visor deployment fraction u_v(t) ∈ [0,1] and thruster throttle u_T(t) ∈ [0,1] over the horizon. It maximizes the value of tasked targets captured, weighted by a predicted image-quality metric (GSD from altitude and obliquity, plus atmospheric path). Constraints: altitude corridor, propellant, power, wheel momentum, AO fluence on the visor, and robustness to density uncertainty |
| B9 | Late-stage agility reserve | Keeps a roll or pitch budget to absorb residual timing error. The planner solves for the timing offset only within ±X s of the target and leaves the rest to slewing |
| B10 | Imaging scheduler | Runs unchanged. The visor is outside the FOV, so imaging goes on in every visor state |

### Method

1. **Ingest tasking.** Each target k has a latitude and longitude, a value w_k, a deadline, and an obliquity limit θ_max,k (for example, 10° for mapping-grade products).
2. **Propagate the reference trajectory.** Use the nominal control law (EP holding altitude, visor stowed). Find the pass on which each target comes closest, and its cross-track miss distance d_k,p.
3. **Convert the miss to time.** For each (k, p), compute the ground-track shift needed, Δx_k,p = d_k,p − h·tan θ_max,k, if positive. Convert it to a timing offset: Δt_k,p ≈ Δx / (ω⊕·R⊕·cos φ_k·sin ψ_k), where ψ is the track azimuth. The sign tells the planner what to do. **Early arrival** means the ground track shifts east, which needs extra drag: visor out, thruster throttled down. **Late arrival** means the track shifts west, which needs extra thrust.
4. **Map timing to along-track displacement.** Use s = v·Δt. For a constant differential tangential acceleration f held for time τ, the secular along-track displacement is s ≈ (3/2)·f·τ², and the altitude change is Δa ≈ 2·f·τ/n.
5. **Solve the schedule.** The planner picks u_v(t) and u_T(t) to hit the chosen set of Δt_k,p. Targets that conflict, needing opposite shifts at the same time, are handled by value-weighted selection. Robust constraints use density-scenario bounds from B6, such as ±40% during geomagnetic activity. The objective also rewards the GSD gain from being lower on the target pass, because drag steering in the "early" direction lowers the orbit.
6. **Execute while imaging.** The flap mixer B4 applies visor and counter-flap angles with net pitch moment set to zero. Imaging, downlink and pointing go on in the nominal attitude.
7. **Close the loop.** Every orbit, re-estimate density and C_D·A from GNSS and the accelerometer, re-propagate, and re-solve. A dependent option also uses the imaging payload's own along-track geolocation residuals (image timing against a reference orthobase) as a direct measurement of timing error relative to the ground.
8. **Hand over near the target.** Inside T_handover (for example, 6 h), freeze drag steering and let B9 absorb any residual cross-track miss with a small roll.
9. **Recover.** After the capture, the thruster restores the altitude corridor. The propellant cost equals the extra drag impulse applied.
10. **Protect the optics with the same hardware.** When no steering is needed, the visor sits at a minimum "shield" angle δ_s (for example, 20–30°). That angle shadows the aperture from grazing ram AO and blocks forward stray light for a small drag penalty. Near-terminator or airglow-sensitive collections can use a larger baffle angle.

### Optional features (become dependent claims)

- The visor is canted about the yaw axis to make a cross-track aerodynamic side force, which gives direct (small) cross-track and inclination/RAAN authority.
- The visor face carries a reference target of known spectral reflectance. The telescope sees it only in a special calibration configuration: the visor partially intrudes into the field of view while the satellite is in eclipse or pointed at the terminator.
- The visor faces the ram direction, so it takes nearly all of the AO fluence. It has an AO-resistant coating (SiO₂ or Al₂O₃ over polyimide, or a low-accommodation specular coating that lowers C_D in the stowed state). The planner tracks cumulative fluence on it as a constraint.
- Several satellites in a constellation run the planner jointly, so tasked targets go to whichever satellite needs the smallest timing offset.
- The visor is fully stowed during eclipse or when power is short, so it does not raise the drag the thruster must make up.

## Worked numerical example

**Spacecraft:** 150 kg, 250 km altitude, circular, SSO (i ≈ 96.6°). v = 7.755 km/s, period 89.5 min, n = 1.170×10⁻³ rad/s. Baseline frontal area A₀ = 0.30 m², C_D = 2.2. The visor is a 0.80 m × 0.50 m panel, so ΔA_max = 0.40 m². Moderate solar activity gives ρ ≈ 7×10⁻¹¹ kg/m³. Aft ion thruster with I_sp = 1500 s.

**Accelerations:**
- Baseline drag: f₀ = ½ρv²C_D·A₀/m = 9.3×10⁻⁶ m/s² (drag force 1.4 mN)
- Extra drag with the visor fully out: Δf = 1.23×10⁻⁵ m/s² (1.85 mN)

**Tasking case:** a target at φ = 35° N lies 117 km cross-track from its nearest pass in 48 h. The roll limit of ±20° gives a field of regard of ±91 km, so the target is out of reach by about 26 km. It needs an eastward shift, which means arriving early.

**Option A (prior-art style for a forward-only-thrust satellite): switch the thruster off for 48 h.**
- f = 9.3×10⁻⁶ → s = 1.5·f·τ² = 415 km → Δt = 53.5 s
- Ground-track shift = R⊕·cos35°·ω⊕·Δt = **20.4 km**. That falls short of 26 km.

**Option B (invention): thruster off and visor fully out for 48 h, with imaging uninterrupted.**
- f = 2.16×10⁻⁵ → s = 968 km → Δt = 124.8 s → shift = **47.6 km**.
- That is 2.3× the authority of Option A. Only about 26 km is needed, so the planner runs the visor at about 45% average deployment, or fully out for about 26 h. The rest of the time is margin against density error.
- **Altitude effect:** the orbit drops by up to about 6.4 km in the full case (about 3.5 km as planned). The target is imaged from about 246.5 km instead of 250 km, so GSD improves by about 1.4%. Obliquity falls from out of reach to at most 20°. With B9 absorbing residual error, it typically ends near 15–18°.
- **Recovery cost:** the extra impulse is at most Δf·τ ≈ 2.1 m/s. That takes 150 × 2.1 / (1500 × 9.81) ≈ **0.022 kg of xenon**, and at most about 0.038 kg if the entire drag impulse must be made up. That is small next to a typical 5–15 kg load.
- **Torque balance:** 1.85 mN acting 1.0 m below the CoM makes a pitch torque of 1.85 mN·m. Unbalanced, that saturates a 0.5 N·m·s wheel in about 270 s. A counter-flap of about 0.4 m² at 1.0 m above the CoM, or 0.27 m² at 1.5 m, cancels it. The wheels are left for imaging agility.
- **Robustness:** with a ±40% density error, the full-visor authority ranges from 28.6 to 66.6 km over 48 h. Both ends cover the 26 km need. The planner shortens deployment in closed loop as it re-estimates density every orbit. Residual timing error at handover is under about 5 s, or about 2 km, which a 0.5° roll absorbs.

**Comparison with 500 km LEO:** at 500 km, ρ is about 50× lower. The same visor would give less than 1 km of shift in 48 h, which is useless. The invention is specific to VLEO: the drag that VLEO operators pay to fight becomes an imaging-targeting actuator.

## Closest prior art found and distinguishing features

| Prior art | What it discloses | How this invention differs |
|---|---|---|
| Foster et al., "Orbit Determination and Differential-Drag Control of Planet Labs CubeSat Constellations," AAS 15-524, arXiv:1509.03270 (https://arxiv.org/abs/1509.03270) | Changes the ballistic coefficient by switching between attitude modes (roughly 5:1 area ratio) *when not imaging*, to set up and keep along-track slots in a constellation | (a) Drag changes through a dedicated torque-balanced visor, with no attitude change, so imaging continues. (b) The goal is capturing individual targets at a bounded obliquity through Earth-rotation timing conversion, not spacing between satellites. (c) Designed for forward-only-thrust VLEO satellites |
| "Ground Track Control Using Differential Drag for Small Earth Observation Satellite Constellations," J. Spacecraft & Rockets, doi:10.2514/1.A35256 (https://arc.aiaa.org/doi/10.2514/1.A35256) | Controls *relative* equatorial ground-track spacing of a constellation with differential drag, for coverage patterns | Controls absolute ground-track position at a *target's latitude* for a *specific pass*, with objectives weighted by value and image quality. Uses a variable-geometry visor that works during imaging. Adds combined thruster-throttle and drag control plus a late handover to agility |
| Falcone, Willis, Manchester, "Propulsion-Free Cross-Track Control of a LEO Small-Satellite Constellation with Differential Drag," IEEE CDC 2023, arXiv:2306.13844 (https://arxiv.org/abs/2306.13844) | Cross-track and along-track relative formation control through differential drag and J2 | Formation-relative and propulsion-free. This invention is target-absolute, works with a forward-only thruster, and uses a torque-balanced visor that runs during imaging |
| SOAR / DISCOVERER steerable fins (Crisp, Roberts et al.; https://research.manchester.ac.uk/en/publications/experimental-results-from-the-satellite-for-orbital-aerodynamics-/; arXiv:2303.16612) | Steerable aft fins for aerostability, attitude control, and differential lift and drag in VLEO | The fins are aft stabilizers that are not tied to the optics. This invention's actuator is a forward visor next to the aperture that doubles as AO shield and baffle. A zenith counter-flap cancels its pitch moment, and a target-driven planner schedules it |
| "Responsive Maneuver Planning for Sun-Synchronous Repeating Ground Track Orbits," J. Spacecraft & Rockets, doi:10.2514/1.A35944 (https://arc.aiaa.org/doi/10.2514/1.A35944); Aerospace 12(2):143 (https://doi.org/10.3390/aerospace12020143) | Impulsive (chemical) maneuvers that adjust the ground track so it overflies targets | Uses propellant-free braking from atmospheric drag, which is only practical at VLEO density, instead of retrograde impulses. Imaging continues throughout |
| US6288670B1, combined roll-yaw steering (https://patents.google.com/patent/US6288670B1/en) | Changes attitude to follow targets or compensate ground motion | Attitude only. No orbit or ground-track change, and no drag |
| Albedo Clarity-1 (https://www.eoportal.org/satellite-missions/clarity) | VLEO satellite at about 250 km with body-mounted arrays and ion-thruster drag makeup | Minimizes drag and does not use it as an actuator. No variable-drag hardware is disclosed |
| Telescope doors and baffles (e.g., ULTRASAT trap door, arXiv:2208.00159); VLEO AO risk (arXiv:2607.25525) | Doors for contamination and launch protection. AO concentrates on ram surfaces | No prior door or baffle is operated as a continuously variable, torque-balanced drag actuator during imaging |

No reference found combines (i) a ram-side aperture visor that keeps the field of view clear, (ii) pitch-moment cancellation by a counter-flap, and (iii) planning that converts per-target timing to ground-track shift and runs drag and throttle together on a forward-only-thrust VLEO imager.

## Why non-obvious

- **Conventional thinking points the other way.** All VLEO design effort goes into *reducing* drag (Albedo, SOAR geometry optimization, arXiv:2202.11779). Adding a large drag panel *in front of the optics* looks self-defeating until you notice two things. First, the cost of the extra drag is small, about 0.02 kg of xenon per targeting event. Second, a forward-only-thrust VLEO satellite has no other way to make a retrograde force without leaving its imaging attitude.
- **The prior drag-control community relies on attitude modes.** The Planet lineage assumes drag authority comes from rotating the whole spacecraft, which excludes imaging during control. Separating drag control from attitude needs the torque-balancing insight. Without it, a forward, off-CoM drag surface saturates the wheels in minutes (see the worked example). This is not a routine design choice.
- **The objective function is different.** Differential-drag literature optimizes *relative* slots and coverage spacing. Turning a *single target's* cross-track miss into an along-track timing offset through ω⊕·R⊕·cos φ, and then into a drag schedule, is a different problem. The fixed geometry is the target on Earth, not a neighboring satellite.
- **The hardware does three jobs at once:** drag actuator, AO shadow and baffle. Each would normally be a separate component. It takes a VLEO-specific insight to see that a ram-side nadir visor is the right place for all three.
- **Authority exists only in VLEO.** At about 500 km the same hardware gives less than 1 km per 48 h, so a LEO practitioner would dismiss the idea.

## Draft claims

**Independent method claim**

1. A method of acquiring imagery of a ground target from a satellite in low Earth orbit at an altitude below 450 km, the satellite comprising a nadir-pointing imaging sensor, a variable-drag surface, and an electric thruster configured to produce thrust substantially only in the direction of orbital motion, the method comprising:
 (a) determining, from a predicted trajectory of the satellite, a pass on which the ground target lies at a cross-track distance exceeding a field-of-regard limit of the imaging sensor;
 (b) computing an along-track timing offset for the satellite at the latitude of the ground target such that the ground-track shift produced by Earth rotation over said timing offset brings the ground target within the field-of-regard limit on said pass;
 (c) computing a control schedule comprising a deployment state of the variable-drag surface and a throttle state of the electric thruster over a planning horizon preceding said pass, such that the resulting differential tangential acceleration produces said along-track timing offset;
 (d) executing the control schedule while holding the satellite in a nadir imaging attitude and while continuing to acquire imagery with the imaging sensor during at least part of the planning horizon; and
 (e) acquiring imagery of the ground target on said pass.

**Independent system claim**

2. An Earth-observation satellite for operation below 450 km altitude, comprising:
 a bus having a nadir-facing telescope aperture;
 a visor hinged adjacent to a ram-side edge of the telescope aperture and actuated among a plurality of deployment angles, the visor in at least one deployed angle projecting frontal area into the incident atmospheric flow and lying outside the field-of-view cone of the telescope;
 a counter-flap located on the opposite side of the satellite's center of mass from the visor along the nadir-zenith axis, actuated in coordination with the visor;
 a flap mixer configured to command the visor and counter-flap such that the net aerodynamic pitch moment about the center of mass is substantially zero while the net drag force varies with a commanded value; and
 a drag-steering controller configured to compute the commanded value from a set of tasked ground targets by converting, for each target, a required ground-track shift into an along-track timing offset, and to command the flap mixer accordingly while the telescope continues imaging.

**Dependent claims**

3. The method of claim 1, wherein the timing offset Δt is computed as Δt ≈ Δx / (ω⊕·R⊕·cos φ·sin ψ), where Δx is the required ground-track shift, φ the target latitude, and ψ the ground-track azimuth. A negative (early-arrival) offset is achieved by increasing deployment of the variable-drag surface and reducing thruster throttle, and a positive (late-arrival) offset by increasing thruster throttle.
4. The method of claim 1, wherein the control schedule is computed by receding-horizon optimization, re-solved at least once per orbit, using an atmospheric density estimate updated from GNSS-derived orbit determination or accelerometer data, subject to a robust constraint covering a density-uncertainty band.
5. The method of claim 1, further comprising freezing the control schedule at a handover time before said pass and absorbing residual cross-track error by a spacecraft roll or pitch slew drawn from a reserved agility budget.
6. The method of claim 1, wherein the objective of step (c) comprises a predicted image-quality metric for the ground target that is a function of both the satellite altitude on said pass, lowered by the drag schedule, and the viewing obliquity.
7. The method of claim 1, further comprising measuring the along-track timing error of the satellite relative to the ground by registering acquired imagery to a reference orthoimage, and using said timing error as a feedback measurement in recomputing the control schedule.
8. The satellite of claim 2, wherein the visor, in a minimum-deployment shield state, geometrically shadows the telescope aperture from ram-direction atomic-oxygen flux and forward stray light, and the drag-steering controller keeps the visor at or above the shield state during imaging.
9. The satellite of claim 2, wherein the counter-flap comprises port and starboard segments independently actuated, and the flap mixer additionally commands a differential deflection that trims aerodynamic yaw moment.
10. The satellite of claim 2, wherein the visor is further rotatable about an axis parallel to the nadir direction to produce a cross-track aerodynamic side force, and the drag-steering controller uses said side force to additionally shift the ground track in the cross-track direction.
11. The satellite of claim 2, wherein the ram-facing surface of the visor carries an atomic-oxygen-resistant coating, and the drag-steering controller tracks cumulative atomic-oxygen fluence on the visor as a constraint.
12. The satellite of claim 2, wherein the flap mixer estimates the aerodynamic moment residual from reaction-wheel momentum history and updates a free-molecular-flow panel model used to compute the coordinated visor and counter-flap angles.
13. The method of claim 1, performed jointly for a plurality of satellites, wherein each tasked ground target is assigned to the satellite requiring the smallest magnitude of along-track timing offset.

## Commercial use cases

- **Assured tasking for defense and intelligence customers on VLEO fleets.** A target that falls in a ground-track gap becomes reachable in 1–3 days with no need to add satellites. This can be sold as a premium "guaranteed-access" SLA.
- **Low-obliquity mapping-grade collects** (orthophoto and cadastral work, 3D reconstruction baselines) from agility-limited streamlined VLEO buses.
- **Disaster and emergency response** where the next natural pass is off-nadir or out of reach. The planner moves the ground track toward the event over the next day or two.
- **Longer optics life** from the AO shield, which lowers mirror and baffle degradation over 3–5 years at 220–280 km.
- **Constellation retasking** without extra propellant sized for retrograde maneuvers or yaw flips, for Albedo-, Skeyeon- or EOI-class VLEO fleets.
- **Licensing** the drag-steering planner (claims 1 and 3–7) separately from the hardware, to any VLEO operator with a controllable drag surface.

## Known weaknesses and risks to patentability

- **Obviousness combination.** An examiner could combine Planet differential drag (1509.03270) or ground-track drag control (A35256) with SOAR steerable fins and a telescope door. Counter-arguments: continuous imaging during control, the torque-balance element (claim 2), the per-target timing conversion, and the forward-only-thrust framing. The dependent claims (AO-shield state, image-registration feedback, altitude- and obliquity-aware objective) add fallback positions.
- **Claim 1 may be read broadly** as "use drag to shift the ground track toward a target," which is arguably in the literature on responsive-orbit and drag reentry targeting (arXiv:2407.18762). It may need to be narrowed to include "while imaging" and the forward-only-thrust limitation.
- **Physics limits.** Authority depends strongly on density. In solar minimum at about 300 km, ρ can be 5–10× lower and authority falls to a few km per day. The concept is strongest at 200–280 km. Lead times of 1–3 days rule out true minute-scale responsiveness.
- **Only drag and thrust are available.** Conflicting targets that need opposite shifts cannot both be served. Value-weighted selection is required.
- **Engineering risk.** Visor structural dynamics could inject jitter into TDI imaging, so the actuator must hold still or move slowly during collects. Deploying the visor raises power demand on the thruster for later makeup. The visor adds a failure mode: if it sticks deployed, lifetime at VLEO shrinks sharply. That needs a fail-safe spring-to-stowed design.
- **The prior-art search was limited** to web searches of Google Patents, arXiv and AIAA. Classified or defense-program art (for example, low-perigee reconnaissance programs) and Chinese CN utility models on "drag plates" for VLEO could be closer than anything found. A professional search in CPC B64G1/242 and B64G1/62 and G01C11 is recommended before filing.
