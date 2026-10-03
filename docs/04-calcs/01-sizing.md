---
doc_id: CLD-CAL-001
title: CollarDrive sizing calculations
project: CollarDrive
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First TRL 3 sizing of the drive, rope pump, blower and duct, exhaust, frame, shafts, mass and cost
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Rerun on the constructable design (CLD-DDR-002); two-belt pump stage, two-module frame on sleepers; results against every requirement
---

# CollarDrive sizing calculations

On paper the constructable design meets every requirement. One 4.8 kW class engine kept on the surface lifts about 76 L/min from 20 m and 19 L/min from 60 m, and delivers 0.19 m³/s of air at the end of 30 m of 200 mm duct, using less than 0.8 kW of shaft power. The exhaust outlet stands 7.05 m from the edge of a 1.5 m collar and 6.46 m from the blower intake. The tightest margin is the pump belt stage at the 30 m design depth, loaded to 92 % of what two A-section belts carry on a 90 mm pulley. All figures are first-principles estimates for a proof of concept on paper; none has been measured.

> **Safety:** CollarDrive puts a running engine, belts and an open shaft side by side. These calculations size the machine; they do not make a shaft safe. Carbon monoxide, low oxygen and other gases must be checked with a gas detector before and during any work below ground, whatever the blower delivers. The frame is not a working platform: nobody stands on it, and the collar is fenced. Stop the engine before touching the drive.

## Scope and method

The script `docs/04-calcs/sizing.py` computes every figure below and writes `docs/04-calcs/results.csv`; each figure carries its tag (for example [B20]). Geometry comes from the parametric model `cad/src/model.py` (shaft heights, pulley diameters, belt centres, exhaust layout, frame sections), prices from `bom/bom.csv`, and the value-engineering target from `project.yaml`. Section L compares the results with every requirement in CLD-REQ-001.

## Assumptions

*Table 1. Assumptions.*

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| 1 | Engine running speed (governor set) | 2,800 rpm | Small 4-stroke engines rated 4.8 kW at 3,600 rpm run quieter and longer slower |
| 2 | Continuous power at 2,800 rpm | 3.0 kW | About 60 % of the rating, a conservative continuous figure |
| 3 | Fuel use at part load | 0.55 kg/kWh petrol, 0.74 kg/L | Lightly loaded small engines are thirsty |
| 4 | V-belt stage efficiency | 95 % | Classical A section |
| 5 | Rope wheel and bearing efficiency | 90 % | Rope pump practice |
| 6 | Rope pull | Water column weight x 1.15 | Pistons rub in the pipe |
| 7 | Volumetric efficiency | 0.90 minus 0.006 per metre of head | Leakage past the pistons grows with head |
| 8 | Allowable belt pull | 150 N per A belt on a 90 mm pulley at low speed | Conservative reading of belt makers' power tables |
| 9 | Blower at 2,000 rpm | 700 Pa shut-off, 0.25 m³/s free delivery, 45 % efficient, parabolic curve | Typical small belt-driven centrifugal blower; to confirm with the blower bought |
| 10 | Lay-flat duct | Friction factor 0.035; entry, bend and exit losses 2.5 velocity heads; 10 % of the air lost through couplings per 30 m | Ventilation duct practice |
| 11 | Air per person at the face | 0.05 m³/s | Planning figure only, not a regulation |
| 12 | Exhaust gas temperature | 500 °C | Small petrol engine at part load |
| 13 | Design shaft for the priced kit | 30 m deep, 40 mm main, 30 m of duct | Middle of the 10 to 60 m range |
| 14 | Rising main by depth | 40 mm PVC to 30 m, 32 mm to 45 m, 25 mm to 60 m | Keeps the rope pull inside the belts' capacity |
| 15 | Steel | S275, yield 275 MPa, E = 210 GPa | Common structural steel |

## A. Drive train (R6, R9)

- [A1] With an 80 mm engine pulley driving a 480 mm layshaft pulley, the layshaft turns at 467 rpm. A 90 mm two-groove pulley on the layshaft drives the 560 mm pump pulley, so the rope wheel turns at 75.0 rpm. A 344 mm layshaft pulley drives the 80 mm blower pulley at 2,007 rpm.
- [A2] The rope runs at 1.57 m/s on its 400 mm circle, inside the 1 to 2 m/s used by motorised rope pumps.
- [A3] Belts, from the model's pulley centres: engine to layshaft 1,166 mm centres, about A126, 160 degrees of wrap on the small pulley, 11.7 m/s; layshaft to pump pulley, two matched belts, 1,101 mm centres, about A128, 155 degrees, 2.2 m/s; layshaft to blower 709 mm centres, about A82, 159 degrees, 8.4 m/s. The lengths are set by the slotted plates at assembly, so the nominal sizes are checked when the belts are bought.
- [A4] The clutch idler, 459 mm along and 764 mm up, presses the slack (upper) strand of the pump belts 25 mm. Lever down, the belts go slack and the blower runs alone.

## B. Rope pump (R3, R4)

*Table 2. Rope pump by depth (40 mm main to 30 m, 32 mm to 45 m, 25 mm to 60 m).*

| Tag | Head | Main | Flow | Rope pull | Power at the pump pulley | Pump belt load | Pump efficiency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B10 | 10 m | 40 mm | 81.5 L/min | 116 N | 0.20 kW | 31 % | 66 % |
| B20 | 20 m | 40 mm | 75.7 L/min | 232 N | 0.41 kW | 61 % | 61 % |
| B30 | 30 m | 40 mm | 69.8 L/min | 348 N | 0.61 kW | 92 % | 56 % |
| B40 | 40 m | 32 mm | 40.5 L/min | 294 N | 0.51 kW | 78 % | 52 % |
| B45 | 45 m | 32 mm | 38.7 L/min | 331 N | 0.58 kW | 87 % | 49 % |
| B60 | 60 m | 25 mm | 19.3 L/min | 257 N | 0.45 kW | 68 % | 42 % |

The flows sit close to the published motorised rope pump figures (120 L/min at 10 m and 20 L/min at 60 m from a 1 to 2 hp engine). The pump belt load peaks at the deepest point of each pipe band; at 30 m with the 40 mm main it reaches 92 % of the allowable pull, so a 40 mm main must not be used below 30 m. The 6 mm polypropylene rope (about 5 kN breaking load) carries at most 348 N, a factor of about 14.

## C. Blower and duct (R5)

- [C30] On 30 m of 200 mm lay-flat duct the blower runs at 0.210 m³/s and 207 Pa; after coupling leakage 0.189 m³/s reaches the duct end, enough for about four people at the planning figure. The blower absorbs 0.10 kW.
- [C60] On 60 m of duct, 0.153 m³/s reaches the end (about three people); 0.12 kW.

The blower forces fresh air down the duct (forcing ventilation). Its intake faces the front of the frame, away from the exhaust riser.

## D. Power and fuel (R6)

*Table 3. Engine shaft power with 30 m of duct.*

| Tag | Head | Engine shaft power | Margin on 3.0 kW continuous | Belt losses | Petrol |
| --- | --- | --- | --- | --- | --- |
| D20 | 20 m | 0.56 kW | 5.4 | 0.05 kW | 0.41 L/h |
| D30 | 30 m | 0.78 kW | 3.8 | 0.08 kW | 0.58 L/h |
| D60 | 60 m | 0.60 kW | 5.0 | 0.06 kW | 0.45 L/h |

The engine is well oversized for the load; the 4.8 kW class is chosen because it is sold and repaired everywhere. Figure 1 shows where the power goes at 20 m.

![Figure 1. Power flow at 20 m head](../../media/flow.png)

*Figure 1. Power flow at 20 m head with the pump and blower running (estimates).*

## E. Exhaust (R2)

- [E1] The riser outlet, 2.4 m above the ground at 7.8 m from the shaft centre, is 7.05 m from the edge of a 1.5 m collar and 6.46 m from the blower intake: both more than the 6 m (20 ft) NIOSH advises between an engine and openings.
- [E2] Exhaust gas runs at about 8.4 m/s through 7.3 m of 40 mm pipe; the back pressure, about 110 Pa, is small against what a small engine's muffler tolerates (a few kPa).

Distance does not guarantee clean intake air when the wind turns toward the frame. The frame is set out with the riser downwind of the prevailing wind, and the gas detector at the working face remains the control that matters.

## F. Frame and ground (R7, R8)

- [F1] The span module bridges 2.45 m between sleeper centres on two RHS 100 x 50 x 3 sills (each I = 112 cm⁴, W = 22.4 cm³).
- [F2] Working loads at 30 m (wheel set and rope pull, hanging main and guide block, hanging duct, layshaft) give 1,215 N·m and 27 MPa: about a tenth of yield.
- [F3] Misuse check: 1.5 kN (a person with a load) over the shaft centre adds up to 2,094 N·m and 47 MPa, with 1.0 mm deflection. The frame would carry it, but it is not a platform and must never be stood on (see the safety stops in CLD-BLD-001).
- [F4] The three 200 x 900 mm sleepers spread 3.8 kN at about 7 kPa, well under what firm soil carries. Their inner edges sit at least 0.35 m back from the edge of a 1.5 m collar, so no load bears on the collar lip.

## G. Shafts and backstop (R9)

- [G1] Pump shaft, 30 mm: 70 N·m from the rope and a 62 N·m bending moment from the overhung pump pulley give an equivalent stress of 33 MPa.
- [G2] Layshaft, 25 mm: 15.2 N·m and 75 N·m from the three overhung pulleys give 50 MPa.
- [G3] When the engine stops, the 30 m water column tries to run the rope back with 61 N·m. The ratchet tooth at 104 mm radius then carries 582 N, which a 10 mm steel tooth and pawl carry easily.

Both shafts are under a quarter of the yield of bright mild steel, leaving margin for keyways and shock.

## H. Mass and cost (R8, R10)

- [H1] Span module with pedestals and cleats 69.6 kg (four people to carry), drive module 34.3 kg, engine about 16 kg, blower about 30 kg; wheel, pump pulley, shaft and ratchet 33.4 kg. No piece needs lifting gear.
- [H2] Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 2,535 (USD 965 under the target).
- [H3] Main cost drivers: blower with plate and inlet guard USD 340; gas detector USD 320; engine and engine plate USD 215; 30 m of lay-flat duct USD 195; pulleys USD 165; belt guard USD 120.

## L. Results against every requirement

*Table 4. Requirements status at TRL 3.*

| ID | Requirement | Target | Result | Status |
| --- | --- | --- | --- | --- |
| R1 | Engine stays on the surface | No combustion below collar level | Engine on the drive module, 1.9 m or more from the shaft centre | Met by design |
| R2 | Exhaust kept away from the shaft | Outlet 6 m or more from the collar and the blower intake | 7.05 m and 6.46 m [E1] | Met on paper |
| R3 | Dewatering flow | 60 L/min or more at 20 m | 75.7 L/min [B20] | Met on paper |
| R4 | Dewatering depth | Useful flow from 60 m | 19.3 L/min with the 25 mm main [B60] | Met on paper, with the 25 mm main below 45 m |
| R5 | Air delivery | 0.1 m³/s or more at the end of 30 m of duct | 0.189 m³/s [C30] | Met on paper |
| R6 | Shared drive | Pump and blower together from one engine of 5 kW or less | 0.78 kW at 30 m from a 4.8 kW class engine [D30] | Met on paper |
| R7 | Fits real collars | Collars 0.8 to 1.5 m across | Sleepers 0.35 m or more clear of a 1.5 m collar [F4] | Met by design |
| R8 | Locally buildable | Common steel sections, stick welder, hand tools | RHS, SHS, plate and bar; heaviest piece 69.6 kg; shafts and keyways from a local machine shop | Met by design |
| R9 | Guarded drive | All belts and pulleys fully guarded | Belt guard, layshaft cover, wheel hood, blower inlet guard, backstop [G3] | Met by design |
| R10 | Cost against the value-engineering target | USD 3,500 | USD 2,535, USD 965 under the target [H2] | Under the target |

Requirements not met: none. Thin margin: the pump belts at 30 m with the 40 mm main (92 % of the allowable pull, [B30]).

## Checks against the TRL 2 figures

The concept precis gave R3 and R5 as estimates from motorised rope pump and blower data; the calculation confirms both with margin. The concept's single pump belt would have been loaded to about 184 % of its allowable pull at 30 m, which is why the constructable design uses two belts (CLD-DDR-002).
