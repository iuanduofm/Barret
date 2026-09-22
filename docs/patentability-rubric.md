# Patentability Rubric (1–10) and Scrap-Metal Patent Concepts

> This is a structured way to screen ideas. It is not a legal opinion. Any concept
> that scores 5 or higher should go to a registered patent attorney or agent for a
> professional prior-art search before money is spent on filing.

---

## Part 1 — The Rubric

### How scoring works

The rubric is a **ladder of nine pass/fail gates**. You evaluate them in order,
and you stop at the first gate that fails.

```
Score = 1 + (number of consecutive gates passed, starting from G1)
```

- Fail G1 → score 1. Pass G1, fail G2 → score 2. ... Pass all nine → score 10.
- **A gate you can't answer confidently counts as a fail.** Scores are conservative
  on purpose. You raise a score by producing evidence, not by arguing.
- Each gate is a yes/no question with a stated evidence standard, so two reviewers
  working from the same facts should reach the same score.

Gates G1–G4 are the legal floor: a concept has to clear all four to be patentable
at all. Gates G5–G9 measure how much the patent would be **worth**: whether it can
be enforced, whether competitors can avoid it, and how much of the market it covers.

### The gates

| Gate | Question (must be "yes" to pass) | Evidence standard |
|---|---|---|
| **G1 — Eligible subject matter** (35 U.S.C. §101) | Is the independent claim a process, machine, article of manufacture, or composition, **and** if it involves an abstract idea (math, a business practice, organizing information), does it recite a specific technical implementation that improves how a machine or physical process works? | The claim can be written without reading as "do [business practice] on a computer." Test: remove the generic computer parts. If what is left is a human activity or a formula, the gate fails. |
| **G2 — Novel** (§102) | Is there **no single** prior-art reference that discloses every element of the independent claim? | Minimum search: Google Patents / USPTO full text, Google Scholar, and the product literature and manuals of the 5 largest vendors in the field. Any reference (a patent, paper, product, public use, or sale) dated before the filing date that contains every element fails the gate. Your own public disclosure also fails it if it was made more than 1 year before filing. |
| **G3 — Non-obvious** (§103) | Is it true that **no combination of two references**, plus a documented reason to combine them, produces the claim with predictable results? | The gate fails if any KSR-style rationale fits: combining known elements with predictable results, simple substitution of a known equivalent, automating a manual process, "obvious to try" among a small number of options, or optimizing a result-effective variable. It passes if at least one claim element has no counterpart in the best two-reference combination, **or** if there is documented unexpected results or teaching away. |
| **G4 — Enabled and described** (§112) | Could an engineer in the field build a working version from the written disclosure without undue experimentation? | A specification exists, or could be written today, that names the components, the data flow, and the control logic, and gives at least one worked embodiment. "Use AI to figure out X" with no stated inputs, outputs, or training approach fails. A prototype or test data is strong evidence but is not required. |
| **G5 — Non-trivial design-around** | Would the cheapest non-infringing alternative cost a competitor something real? | The gate passes if the best alternative requires at least one of: **(a)** more than 3 engineer-months of redesign, **(b)** a loss of 15% or more on the metric the invention improves, or **(c)** a unit or operating cost increase of 15% or more. It fails if an engineer could step outside the claims in about a week with no loss, for example by moving a numeric range or swapping one standard part. |
| **G6 — Detectable infringement** | Could the patent owner show that a competitor infringes using **only publicly available evidence**? | Acceptable evidence: buying and inspecting the product, observing its output, public documentation or spec sheets, marketing claims, regulatory filings, or published certificates. The gate fails if proof would require litigation discovery or entry to the competitor's plant, as with a hidden back-end process that leaves no trace in its output. |
| **G7 — No viable design-around** | Do the independent claims cover **every commercially practical way** of getting the benefit? | The gate fails if any known alternative delivers 85% or more of the benefit at comparable cost, even if that alternative is worse. It passes only if every alternative falls short on performance or cost by more than those margins. |
| **G8 — Pioneering / genus-level** | Does the concept solve a **documented long-felt need**, and do the claims apply **across industries**? | Two conditions, both required. **(a)** The problem has been publicly recognized for 5 years or more (trade press, standards bodies, papers), and there are documented failed or partial attempts by others. **(b)** The independent claim works without modification in at least 2 distinct industries or markets, which supports genus claims and a continuation family. |
| **G9 — Indispensable** | Is the invention, or will it foreseeably become, something the industry **cannot operate without**? | At least one of: it is written into, or required by, an industry standard or regulation; it is used in 50% or more of the target market; or there is objective evidence such as copying by competitors, licensing demand, or commercial success traced to the claimed feature. This gate is rarely scoreable before launch. If there is no evidence yet, it fails. |

### What each score means

| Score | Last gate passed | Plain meaning | Recommended action |
|---|---|---|---|
| **1** | none | Not patentable subject matter: an abstract idea, business method, or law of nature. | Drop it, or keep it as a trade secret or know-how. |
| **2** | G1 | Eligible, but a single existing reference already discloses it. | Drop it. Keep the search results. |
| **3** | G2 | New, but an obvious combination of known things. | Drop it, unless you can find an unexpected result to document. |
| **4** | G3 | New and non-obvious, but still only an idea. Nobody could build it from what exists. | Do engineering work (a prototype or detailed design), then re-score. |
| **5** | G4 | Patentable, but competitors could cheaply avoid it. | File only if it's inexpensive to do or needed defensively. A provisional application is usually enough. |
| **6** | G5 | Patentable and costly to avoid, but you would never know if someone infringed. | Usually better kept as a **trade secret** than disclosed in a patent. |
| **7** | G6 | Patentable, costly to avoid, and infringement is visible. A worse but workable alternative still exists. | **File.** This is a solid commercial patent that gives real leverage for licensing and competitive position. |
| **8** | G7 | Covers every practical way to get the benefit in the target market. | File with a continuation strategy and international (PCT) coverage. |
| **9** | G8 | Pioneering: it solves a long-standing problem and supports genus claims across industries. | Build a patent family and plan for licensing outside your own industry. |
| **10** | G9 | Indispensable: standard-essential or de facto required. | Plan for licensing on standards (FRAND) terms and budget for enforcement. |

### Calibration examples (scrap-metal context)

These are illustrative, not searched.

| Score | Example | Why it stops there |
|---|---|---|
| 1 | Paying scrap sellers with a loyalty-points scheme based on tonnage | Business method (fails G1) |
| 2 | An electromagnet on a crane for lifting ferrous scrap | Anticipated by decades of use (fails G2) |
| 3 | A handheld XRF gun that sends each reading over Bluetooth to scale-ticket software | Known gun + known software + an obvious reason to combine (fails G3) |
| 4 | "A camera system that predicts the exact platinum-group-metal value of a catalytic converter from a photo," with no stated method | No enabling detail (fails G4) |
| 5 | A shear blade with teeth at a specific 37–42° rake angle | Easy to design around by using 35° (fails G5) |
| 6 | A proprietary control scheme for an eddy-current separator inside the yard | Hard to copy, but invisible from outside (fails G6) |
| **7** | **The concept in Part 2** | Detectable and costly to avoid, but a workable alternative exists (fails G7) |
| **8** | **The concept in Part 3** | Covers every practical approach, but applies only to vehicle shredding (fails G8) |
| 9 | The first practical method for removing copper from molten steel, usable in steel, foundry, and recycling | Long-felt need, cross-industry, but not yet a standard (fails G9) |
| 10 | A composition-measurement method written into an ISRI/ASTM scrap specification that every mill requires | Indispensable |

---

## Part 2 — A Concept That Scores 7

### Title

**Spec-Targeted Scrap Lot Assembly with Closed-Loop Mass Calibration and a
Bound Composition Record**

### The problem

Mills and secondary smelters buy scrap by **grade**, then do their own sampling
and blending to reach a chemistry target. Residual elements are a well-known,
costly problem, for example copper and tin in steel for EAF flat products, or iron
and zinc in secondary aluminum. A mill cannot remove them in the melt, so it
dilutes them with expensive prime material or pig iron. Existing sensor-based
sorters (LIBS or XRF plus air-jet or flap diverters) sort scrap into **fixed alloy
classes**. They do not assemble each outgoing lot toward a **specific buyer's
chemistry window**, and they do not give the buyer a per-lot chemistry
prediction that has been verified against a physical measurement.

### The invention

A sorting line that:

1. **Measures each piece.** It singulates pieces on a conveyor, measures each
   one's elemental composition (LIBS or XRF), and estimates its **mass** from a 3D
   profile (laser triangulation or stereo imaging) multiplied by a density looked
   up from the measured alloy class.
2. **Keeps N lots open at once.** It maintains N open lots (bales, bins, or boxes),
   each tied to a buyer's spec window, for example Cu ≤ 0.15%, Sn ≤ 0.02%, or an
   aluminum-alloy-family range. For each lot it keeps a **running mass-weighted
   composition estimate and a confidence interval**.
3. **Assigns each piece.** For each incoming piece, it computes the lot assignment
   that **minimizes the expected deviation of all open lots from their targets**,
   under hard ceilings on tramp elements. It then actuates the diverter.
   Low-confidence pieces go to a re-scan loop or to a general-grade lot.
4. **Closes a lot only when the math says so.** A lot is closed when its predicted
   composition **and its full confidence interval** fall inside the buyer's window.
5. **Calibrates itself.** When a closed lot is weighed on a certified scale, the
   difference between the scale weight and the summed per-piece mass estimates is
   used to **update the mass-estimation model** (density table and volume
   correction factors) for later pieces. This is the key technical hook.
6. **Ships a record with the lot.** It writes a **machine-readable composition
   record** (predicted chemistry, interval, piece count, calibration version) and
   binds it to a physical identifier on the lot, such as an RFID tag or a QR code
   under the bale strap. The receiving mill scans it at the gate.

### Draft claim structure

- **Independent method claim:** steps 1–4 plus step 6. This covers the commercial
  product: a spec-targeted lot with a bound record.
- **Independent system claim:** sensor, mass estimator, allocator, diverter, lot
  identifier writer.
- **Dependent claims:**
  - (a) the scale-weight feedback that recalibrates the mass model (step 5);
  - (b) the re-scan loop for low-confidence pieces;
  - (c) spec windows ingested automatically from a buyer's purchase order;
  - (d) hard tramp-element ceilings treated as constraints rather than
    optimization terms;
  - (e) the mill-side receiving step that reads the record and adjusts the
    furnace charge plan.

### Gate-by-gate scoring

| Gate | Result | Reasoning |
|---|---|---|
| G1 Eligible | ✅ Pass | The claims recite physical sensing, physical diversion, and physical lot formation. The calibration loop improves the accuracy of a measuring machine, which is a technical improvement rather than an abstract idea on a computer. |
| G2 Novel | ✅ Pass *(to be confirmed by search)* | Known references sort pieces into **fixed classes**, and furnace **charge optimization** software blends at the mill. The combination of per-piece allocation across multiple open lots toward buyer-specific windows, confidence-interval-gated lot closure, and a bound record is not expected to appear in any single reference. |
| G3 Non-obvious | ✅ Pass *(the weakest gate; see risk below)* | Examiners will argue that "LIBS sorter + charge optimizer" is an obvious combination. The rebuttal is that neither reference teaches **(i)** closing a lot on a *confidence interval* rather than a point estimate, or **(ii)** using the *final lot scale weight* to recalibrate a *per-piece* mass model. Charge optimizers work on lots with known weights, and sorters don't track lots. Claim elements (i) and (ii) have no counterpart in the best two-reference combination. |
| G4 Enabled | ✅ Pass | Every component is off-the-shelf (LIBS or XRF heads, 3D line scanners, air-jet diverters, RFID). The allocator is a constrained online assignment problem with a standard formulation. An engineer could build it from a detailed specification. |
| G5 Non-trivial design-around | ✅ Pass | The obvious alternative is to sort into fixed classes and then **certify each lot by drill or melt sampling**. That adds lab cost and turnaround per lot, and sampling a heterogeneous bale gives a much wider chemistry uncertainty. The loss on the metric the invention improves (lot chemistry confidence) is expected to exceed 15%. |
| G6 Detectable | ✅ Pass | The product is the evidence. A competitor selling lots with a per-lot predicted chemistry, a confidence interval, and a tag readable at the mill gate is visible in the tag itself, in the documents that ship with the lot, and in marketing claims such as "spec-guaranteed bales." Buying one bale is enough to check. |
| G7 No viable design-around | ❌ **Fail** | Sort into fixed classes, then certify by sampling. This is worse, but it is **commercially workable** and delivers most of the value (the premium for a certified lot), probably 85% or more for buyers with loose windows. A competitor could also skip the bound record and send chemistry by email, which avoids the independent claim if the tag is a required element. |

**Score: 1 + 6 gates passed = 7.**

### Why it's not a 6

Invisible yard-process patents score 6. This one ships its evidence **inside the
product**. The bound composition record is the feature buyers pay for, and it is
also what exposes an infringer.

### Why it's not an 8

The sampling-based alternative is inferior but commercially viable. The claims
don't cover **every** practical way to deliver certified low-residual lots.

### What would move it to 8

- Test data showing that post-hoc sampling of a heterogeneous bale **cannot** meet
  tight windows (for example Cu ≤ 0.10%) at a confidence buyers will accept. That
  would make the design-around fall short of 85% of the benefit for the premium
  segment.
- Redrafting the independent claim so the record can be **any** per-lot chemistry
  representation derived from per-piece measurements, not only a physical tag. That
  closes the "send it by email" gap.

### What would drop it to 6 or lower

- The search turns up a sorter vendor's patent or white paper describing
  multi-lot, spec-targeted allocation. That would reduce the novelty to the
  calibration loop only, and the likely score would fall to about 5, because a
  competitor could simply recalibrate manually.
- Buyers don't care about the record and competitors sell the lots without one.
  Infringement would then be hidden inside the plant (score 6).

### Main risk and next steps

1. **G3 is the gate most likely to flip.** Put the confidence-interval lot
   closure and the scale-feedback calibration in the independent claim, not only
   in dependent claims.
2. Commission a professional search focused on: sensor-based scrap sorting
   (LIBS/XRF), furnace charge optimization, online bin-packing and blending, and
   material traceability tags in metals supply chains.
3. Run a pilot on one line and record: the per-piece mass error before and after
   calibration, and predicted versus lab-measured lot chemistry. That data
   strengthens G3 (unexpected results) and G7 (the size of the design-around gap).
4. File a provisional application **before** any customer pilot or marketing,
   because public use or an offer for sale starts the 1-year clock.

---

## Part 3 — A Concept That Scores 8

### Title

**Pre-Shred Thermal Neutralization of Pyrotechnic Devices in End-of-Life
Vehicle Hulks**

### The problem

Auto shredders process flattened end-of-life vehicle (ELV) hulks. Undeployed
airbag inflators and seat-belt pretensioners are supposed to be removed or
deployed during dismantling. Many hulks still arrive with live devices,
because the supplier skipped the step, missed a curtain or knee airbag, or
flattened the car first.

Once a car is flattened, the wiring is crushed, so the devices can no longer be
fired electrically. They are also hard to find and hard to pull out. When they
reach the hammer mill they go off unpredictably, contributing to deflagrations,
fires, damage to the shredder, and injuries. The shredding yard gets the hulk
but has no control over, and no practical way to verify, what the supplier did
upstream.

### The key insight

Pyrotechnic inflators are **designed to function safely when heated from
outside**. For transport classification and fire safety, inflators and airbag
modules are tested under external fire exposure (for example, the UN bonfire
test). Most contain an **auto-ignition material** that sets off the device in a
controlled way at a set temperature, so that it doesn't rupture violently in a
vehicle fire.

This means heat neutralizes every device in a hulk, **whether or not anyone
knows where the devices are**. You don't have to find them first.

### The invention

A containment tunnel installed in line before the shredder infeed:

1. **Contain the hulk.** A flattened hulk enters a blast-rated tunnel, either as
   a batch chamber or a continuous conveyor tunnel.
2. **Heat it until the devices fire.** The whole hulk is heated (hot gas,
   infrared, or induction) until thermocouple or model-verified core
   temperatures reach or exceed the activation temperature of the auto-ignition
   material. The setpoint comes from inflator manufacturer data, commonly in the
   low-to-mid hundreds of °C, and is held for a verified residence time.
3. **Control fire risk.** The tunnel atmosphere is oxygen-reduced (nitrogen or
   flue-gas recirculation, with O₂ monitored below a set limit). Volatilized
   fuel and fluid residues are extracted to a condenser or thermal oxidizer.
4. **Count the deployments.** Acoustic and pressure-transient sensors count the
   deployment events in each hulk. Together with the temperature log, this
   produces a **per-hulk neutralization record**.
5. **Release to the shredder.** Hulks are released to the shredder only after
   the temperature and time criteria have been met.

### Draft claim structure

- **Independent method claim (deliberately broad):** before size reduction in a
  shredder, raise an ELV hulk, within a containment enclosure, to a temperature
  at or above the activation temperature of the auto-ignition material of its
  pyrotechnic safety devices, **by any heating means**; then feed the hulk to
  the shredder.
- **Independent system claim:** a containment enclosure upstream of the shredder
  infeed, a heater, temperature verification, and an interlock that blocks
  release until the temperature and time criteria are met.
- **Dependent claims:**
  - (a) an oxygen-reduced atmosphere with O₂ monitoring;
  - (b) vapor extraction and recovery of fuel and fluid residues;
  - (c) acoustic or pressure event counting and a per-hulk record;
  - (d) a setpoint selected from a database of inflator auto-ignition data;
  - (e) induction heating;
  - (f) a continuous conveyor tunnel sized to the shredder's feed rate.

### Gate-by-gate scoring

| Gate | Result | Reasoning |
|---|---|---|
| G1 Eligible | ✅ Pass | A physical process performed on physical objects, using physical equipment. There is no abstract-idea issue. |
| G2 Novel | ✅ Pass *(to be confirmed by search)* | Known references cover bulk thermal destruction of **loose, already-removed** inflators (for example, recall disposal), thermal de-coating of aluminum scrap, and shredder explosion venting and suppression. Whole-hulk, in-line thermal neutralization **before shredding** is not expected in any single reference. |
| G3 Non-obvious | ✅ Pass *(the weakest gate; see risk below)* | An examiner will combine "inflators can be destroyed by heat" with "hulks contain inflators." The rebuttal is **teaching away**. Standard industry practice treats hulks as fuel- and oil-contaminated fire hazards to be kept *away* from heat, so deliberately heating whole hulks is counterintuitive. The technical problems this raises (fuel vapor, fire, throughput) are solved by the claimed containment and atmosphere control, and neither reference addresses them. |
| G4 Enabled | ✅ Pass | Every component exists in industrial practice: blast-rated enclosures, industrial ovens and induction heaters, inerting systems, vapor recovery, and acoustic event detection. A rough energy estimate puts heating roughly a tonne of steel to about 200 °C at a few tens of kWh, a small cost per hulk. A detailed specification is feasible today. |
| G5 Non-trivial design-around | ✅ Pass | Follows from G7 below. |
| G6 Detectable | ✅ Pass | A heated, blast-rated tunnel in front of a shredder is a large, visible installation. It will almost certainly need an **air permit**, since it emits volatilized hydrocarbons. Air permits are public filings that describe the process, and equipment vendors will market it. No discovery is needed. |
| G7 No viable design-around | ✅ Pass | Because the claim covers heating **by any means**, the remaining alternatives all fall short. The four realistic ones are: **(1) Supplier certification or manual removal.** This is today's practice. It is the source of the problem and adds nothing new. **(2) X-ray imaging plus manual extraction from flattened hulks.** Finding small canisters in crushed steel is unreliable, and extracting them is slow manual work that can't keep pace with a shredder fed many hulks an hour. The cost penalty is far above 15%. **(3) Electrical firing.** It is impossible once the wiring has been crushed. **(4) Tougher shredders or explosion venting and suppression.** These lessen the damage after a device fires in the mill rather than preventing it, deliver well under 85% of the benefit, and complement the invention rather than replacing it. |
| G8 Pioneering / genus-level | ❌ **Fail** | Part (a) probably passes: undeployed pyrotechnics in shredder feed have been a recognized hazard for well over 5 years, and compliance regimes have not solved it. Part (b) fails. The claims are tied to ELV hulks going into a shredder, and they don't carry over **without modification** to a second distinct industry. Bulk disposal of loose inflators is already prior art, so that market isn't open to these claims. |

**Score: 1 + 7 gates passed = 8.**

### Why it's not a 7

The Part 2 concept had a worse but commercially workable alternative (sampling).
This concept has none. Its insight is that heat is the **one** mechanism that
reaches every device regardless of location or wiring, and the independent claim
covers that mechanism at the genus level ("by any heating means"), not one type
of heater.

### Why it's not a 9

It is a single-industry patent. Every other context where live pyrotechnic
devices matter (munitions demilitarization, loose inflator disposal) either
already uses thermal treatment or needs a different claim.

### What would move it to 9

This would take a claim that generalizes cleanly beyond vehicles. For example, it
could be reframed as "thermal neutralization of **any** heat-activated embedded
energetic device in a mixed metal stream before size reduction." That would also
cover appliance and e-waste shredding, where lithium cells and pressurized
components behave differently. The reframing works only if test data shows the
same process reliably neutralizes those hazards too, which is far from certain.

### What would drop it to 7 or lower

- The search finds a reference that heats whole hulks before shredding, for
  another reason such as de-oiling or pre-pyrolysis. Novelty would then rest on
  the pyrotechnic setpoint and the interlock. That is narrower and easier to
  design around, so the score would drop to about 5 or 6.
- The independent claim has to be narrowed to the oxygen-reduced atmosphere to
  get past G3. A competitor could then heat in air with fire suppression
  instead, which would fail G7 and give a 7.

### Main risk and next steps

1. **The main risk is G3, and it pulls against G7.** A broader independent claim
   helps G7 but hurts G3. Draft a ladder of fallback claims (heat only →
   heat + containment → + reduced-O₂ atmosphere → + record and interlock) so
   prosecution can retreat one step at a time without losing enforceability.
2. **Check safety first.** Test the premise on removed inflators across
   manufacturers and generations, including ammonium-nitrate designs and hybrid
   stored-gas inflators. Hybrid inflators respond to heat differently, and
   their behavior determines both enablement and whether the claims cover
   "all devices."
3. **Commission a professional search** focused on: thermal pretreatment of
   ELVs, inflator disposal by heating, shredder infeed safety, and
   thermal de-oiling or de-coating of scrap.
4. **File a provisional application before any pilot, vendor RFQ, or permit
   application.** An air permit filing is itself a public disclosure.

---

## Part 4 — The Flagship Concept (scores 9 on paper)

### Title

**Conductivity-Sensing Lifting Magnet: Detecting Copper in Ferrous Scrap While
It Hangs From the Magnet**

### The pitch

Every ton of ferrous scrap in a yard, and every charge bucket at a mill, hangs
from a lifting magnet at least once. **This invention makes the magnet report
what it's holding.** It needs no sorting line, no conveyor, no extra floor space,
and no change to how operators work.

### The problem it solves

Copper is the most costly contaminant in ferrous scrap, and it has been for
decades:

- **Copper can't be removed once it's in the melt.** Mills cap residual copper
  and dilute it with costly low-residual material. They downgrade or reject
  scrap that runs high.
- **Much of it arrives inside things the magnet picks up.** Electric motors
  ("meatballs"), alternators, starters, and transformer cores have steel bodies
  that the magnet grabs, with copper windings inside. The magnet can't tell a
  motor from a piece of plate.
- **Motors are worth far more than ferrous scrap.** When they ride along in a
  ferrous load, the yard sells copper at the steel price **and** hurts the load's
  quality. That's a loss both ways.
- **Today's fixes don't reach most of the tonnage.** Hand-pickers and
  sensor-sorting lines work only on shredded material that travels on a
  conveyor. Heavy melting, plate and structural, unprepared scrap, and mill
  charge buckets never pass a sorting line. The magnet is the only
  piece of equipment that handles all of it.

### The key insight

A lifting magnet's large DC field **magnetically saturates the steel it holds**.
Saturated steel has a very low incremental permeability. To a small, fast AC or
pulsed field added on top, the steel largely stops acting like a magnet and acts
like an ordinary, fairly poor conductor.

Copper is a much better conductor and isn't magnetic at all. It produces a
strong, slowly decaying eddy-current response that stands out against the
saturated steel. The magnet's own lifting field therefore **suppresses the
background that would normally swamp a metal detector sitting on a pile of
steel**. That is an unexpected result, and it anchors the non-obviousness
argument (G3).

### The invention

1. **Sense.** A pulse-induction or multi-frequency eddy-current sensor array is
   embedded in the magnet face, or sold as a retrofit ring or puck. It runs
   while the magnet is energized and holding a load. It uses its own small
   transmit/receive coils rather than the magnet's main coil, whose inductance
   is too large to modulate quickly.
2. **Classify.** Signal features are matched against a library of reference
   signatures to classify each lift. The features are decay time constant,
   response amplitude versus frequency, and spatial distribution across the
   array. The classes are clean ferrous, copper-bearing item (motor,
   alternator, wound part), aluminum-bearing item, and unknown.
3. **Act.** The operator gets an alert in the cab, or the controller routes the
   lift automatically: drop to the reject or recovery zone, or tap-release
   (briefly drop the magnet current to shed loosely attached pieces).
4. **Record.** Each lift is logged with its time, location, the magnet's
   current-derived or load-cell mass, and its classification.
5. **Roll up per load.** Per-lift results are added into a **load-level copper
   estimate**. This supports a **certified low-copper shipment** document (it
   connects to the Part 2 concept) and gives the yard evidence against mill
   downgrade claims.

### Draft claim structure

- **Independent method claim (the genus):** while a lifting electromagnet holds
  ferrous material, measure an electromagnetic response of the held material
  that indicates the presence of a non-ferromagnetic conductor, and generate a
  control or data output from it.
- **Independent apparatus claim:** a lifting magnet, or a retrofit kit for one,
  with a sensing coil array at the working face and a processor that
  discriminates non-ferromagnetic conductive material while the magnet is
  energized.
- **Dependent claims:**
  - (a) sensing timed to occur while the DC field saturates the held ferrous
    material;
  - (b) pulse-induction decay-time discrimination;
  - (c) automatic routing or tap-release;
  - (d) a per-load copper roll-up and certificate;
  - (e) mill charge-bucket use, with the charge plan adjusted from the result;
  - (f) estimating the lifted ferrous mass from the magnet's electrical
    signature.

### Gate-by-gate scoring

| Gate | Result | Reasoning |
|---|---|---|
| G1 Eligible | ✅ Pass | A physical apparatus that senses physical material and changes what physically happens to it. |
| G2 Novel | ✅ Pass *(to be confirmed by search)* | Known references include lifting magnets and magnet controllers, crane scales, eddy-current separators on conveyors, and hand-held and walk-through metal detectors. Sensing a **non-ferrous conductor in material held on an energized lifting magnet** is not expected in any single reference. |
| G3 Non-obvious | ✅ Pass *(depends on the bench test)* | "Put a metal detector on the magnet" looks obvious, but the obvious version doesn't work. A metal detector next to tonnes of steel is swamped by the ferrous response. A skilled engineer would expect that and not try it, which is **teaching away**. The unexpected result is that the magnet's own saturating field suppresses the ferrous background. That is documentable, and it is what makes the combination work. |
| G4 Enabled | ✅ Pass *(the gate to verify first)* | Pulse-induction and multi-frequency eddy-current electronics, ruggedized coils, and magnet controllers are all off-the-shelf. A specification with coil geometry, timing relative to the DC field, and the discrimination logic can be written today. A bench test with a motor, plate, and shred on an energized magnet turns "plausible" into "demonstrated." |
| G5 Non-trivial design-around | ✅ Pass | Follows from G7 below. |
| G6 Detectable | ✅ Pass | Magnets are visible equipment sold by a small number of vendors. A "copper-detecting magnet" or retrofit kit would be marketed, and its brochure is the evidence. The certified low-copper shipments are public claims too. |
| G7 No viable design-around | ✅ Pass | The genus claim covers **any** electromagnetic sensing of the held load while it is lifted. The remaining alternatives: **(1) Hand-picking or sorting lines.** Shredded material only, a separate capital project, and they miss the large share of tonnage that never reaches a conveyor. **(2) Cameras on the crane.** Copper windings sit inside steel housings, so a camera sees a steel lump and can't tell a motor from a gear case with any reliability. **(3) X-ray.** Can't be done safely or practically on a swinging crane in an open yard. **(4) Sense the pile before lifting.** A detector on top of a steel pile runs into the same ferrous background problem this invention solves. No alternative delivers 85% or more of the benefit across all grades at comparable cost. |
| G8 Pioneering / genus-level | ✅ Pass | **(a) Long-felt need:** copper in steel scrap has been a recognized industry problem for decades, and pickers, sensor sorters, cryogenic processing, and melt-stage research have only partly solved it. **(b) Cross-industry:** the same claim works unchanged in scrap recycling, **steelmaking** (mill charge buckets), **waste-to-energy** (magnets recovering ferrous from incinerator ash), and **demolition** (magnets on excavators). |
| G9 Indispensable | ❌ **Fail** | There is no standard adoption, market share, or copying yet. By the rubric's rule this can't be scored before launch. |

**Score: 1 + 8 gates passed = 9.**

### Path to 10

The score reaches 10 if magnet-verified copper data becomes what buyers **require**:
- mills write "magnet-verified Cu" into purchase specifications;
- a scrap specification body references the method; or
- the major magnet vendors license it because customers won't buy magnets
  without it.

### Why this one is different from Parts 2 and 3

| | Part 2 (score 7) | Part 3 (score 8) | **Part 4 (score 9)** |
|---|---|---|---|
| New equipment | A sorting line | A heated tunnel | **A sensor on the magnet the yard already owns** |
| Tonnage it touches | What goes through the line | Car hulks only | **Nearly every ferrous ton, at yards and mills** |
| How it makes money | A premium on certified lots | Avoided damage and downtime (a cost center) | **Recovered motor value, a low-copper premium, fewer mill claims, and licensing** |
| Who licenses it | Sorter builders | Shredder operators | **Magnet vendors, every EAF mill, every yard, and waste-to-energy plants** |

### Risks and next steps

1. **Bench test first. This determines G3 and G4.** Put a commercial pulse-induction
   coil on an energized lifting magnet and lift three loads: clean plate, a
   motor, and shred with and without motors. Measure the signal separation with
   the DC field on versus off. If the saturation effect shows up, it is both the
   invention and the unexpected result to put on record.
2. **Search** magnet-vendor patents, magnet-controller patents, crane-scale
   patents, and metal detection in bulk-handling equipment.
3. **Draft for the genus.** The independent claim should cover "sensing a
   non-ferromagnetic conductor in material held by an energized lifting
   magnet," not just one sensor type, so that multi-frequency, pulse, and
   other approaches all fall inside it.
4. **Keep it confidential until a provisional is filed.** That includes the
   bench test with any outside vendor, which should happen under an NDA.
5. **Size the economics** with the company's own data: tons handled by magnet,
   the motor-versus-ferrous price spread, the frequency of motors in ferrous
   loads, and annual mill downgrade claims.
