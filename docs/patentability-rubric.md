# Patentability Rubric (1–10) and a Scrap-Metal Concept Scored at 7

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
| 8 | A shredder-infeed system that detects lithium batteries and **every** practical way of stopping them before shredding falls within the claims | Covers every practical approach, but not pioneering across industries (fails G8) |
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
