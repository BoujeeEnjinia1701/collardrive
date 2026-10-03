---
doc_id: CLD-DDR-002
title: CollarDrive design for construction
project: CollarDrive
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Changes that make the concept constructable, decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." None of the changes alters what CollarDrive does, its pitch or its safety case, except to make the safety case stronger (backstop, guards, sleepers set back from the collar).

## Context

The TRL 2 concept was a massing model: one welded frame "bolted and staked over the collar", an engine, a layshaft, a wheel with "a clutch", one belt to the pump, a blower, a duct and an exhaust extension. Writing the build plan (CLD-BLD-001) meant deciding how every part is made and how it joins its neighbours, following Amish's rule of 2026-09-30: "fix the design assumptions to match and be physically feasible". The model `cad/src/model.py` was changed until its fit check (`python cad/src/model.py --check`) reports no two components overlapping and every joint face touching (48 components, 0 overlaps, 0 missing contacts).

> **Safety:** These changes concern a machine with a running engine, belts and a rope beside an open shaft. The backstop, the guards and the set-back sleepers are safety features and are not to be left out of a build. The frame is not a working platform; the collar is fenced; the gas detector is used below ground.

## Options considered

For each problem the simplest physically sound fix that keeps what the concept does was chosen. Alternatives considered are named in the "Why" column of Table 1.

## Decision

*Table 1. Changes made for construction.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| 1 | Frame | One welded frame about 3.9 m long, over 100 kg | Two modules bolted at a joint: a span module 2.75 m long (69.6 kg with its pedestals and cleats) and a drive module 1.15 m long (34.3 kg); 10 mm joint plates and eight M16 grade 8.8 bolts | Each piece can be carried by hand to a remote collar; a single frame would need lifting gear |
| 2 | Ground support | "Bolted and staked over the collar", bearing on the collar | Three 200 x 100 x 900 mm timber sleepers, their edges at least 0.35 m back from the edge of a 1.5 m collar, each held by two 25 mm stakes 700 mm into the ground; welded cleats and M12 coach screws hold the sills to the sleepers | Nothing loads the collar lip, which may crumble; the stakes stop the frame walking under belt pull |
| 3 | Pump belt | One belt from the layshaft to the wheel | Two matched A belts on a 90 mm two-groove layshaft pulley and a 560 mm two-groove cast pump pulley | One belt would carry about 184 % of its allowable pull at 30 m; two carry 92 % |
| 4 | Clutch | "Clutch" on the wheel, not defined | Over-centre idler on the slack strand of the pump belts, a lever through the belt guard with a latch plate | No bought clutch; the blower runs alone with the lever down |
| 5 | Bearings | Shafts floating at their heights | UCP206 and UCP205 pillow blocks on welded pedestals of SHS 60 x 60 x 4 with 10 mm top plates | The shafts must sit at set heights above the sills |
| 6 | Backstop | None | 12-tooth ratchet keyed to the pump shaft and a sprung pawl on a post welded to a crossbar | A 30 m water column runs the rope back with 61 N·m when the engine stops |
| 7 | Pump wheel | A disc | Steel hub, 6 mm web and two car tyre sidewalls bolted to form a V that grips the rope on a 400 mm circle | The open rope pump wheel, buildable anywhere |
| 8 | Pipe head | Pipe "hung down the shaft" | 8 mm plate across two crossbars with a split collar clamping the main; outlet tee with a rope exit stub above it; spout to the front; M12 eye bolt for a 6 mm support wire | The main and the guide block hang from the wire and the plate, not from the PVC |
| 9 | Guide block | Not drawn | Weighted 6 mm steel box with an HDPE roller on a stainless pin, an inlet socket and slotted sides | Turns the rope into the main at the bottom and keeps it down |
| 10 | Duct head | Duct "from the blower" | Rigid 200 mm galvanised bend on a saddle and strap on a crossbar; a 0.7 m flexible link to the blower outlet | The lay-flat duct needs a rigid turn and a fixed point |
| 11 | Engine and blower mounting | Sitting on the frame | 8 mm plates with four slots each, bolted to crossbars placed under them; engine and blower bolted to the plates | Slots tension the belts; crossbars carry the feet |
| 12 | Guards | "Belt and pulley guards" | Belt guard of angle, sheet and 12.7 mm mesh on three brackets; wheel hood; layshaft cover; 6 mm mesh blower inlet guard | Every moving part enclosed (R9) |
| 13 | Exhaust | "Extension carries fumes downwind" | Stainless flexible hose, 40 mm galvanised pipe on two low stands, bend and riser on a tall stand, outlet 2.4 m high with a rain cap, 7.8 m from the shaft centre | Meets the 6 m distance with the riser above head height |
| 14 | Water outlet | Not drawn | Spout to the front of the frame and a 10 m discharge hose | Water laid at least 5 m from the collar |
| 15 | Crossbars | Not placed | Six crossbars in each module, placed under the pedestals, pawl post, pipe head plate, duct saddle and the two plates | Every fixing has steel under it |

## Consequences

- The model, STEP and STL exports, the general arrangement CLD-DWG-001 (Rev P2) and the concept media were regenerated from the changed model.
- The calculations were rerun (CLD-CAL-001 v0.2); every requirement is met on paper.
- The bill of materials gained lines for sleepers and stakes, joint bolts, pedestals, the backstop, the clutch, the pipe head, the guide block, the support wire, the duct head and the discharge hose. Estimated cost USD 2,535 against the USD 3,500 value-engineering target.
- Facts that can only be settled with real parts (pillow block bolt centres, blower feet, engine base, belt lengths) are listed under "To confirm when parts are bought" in the design decisions register (CLD-DEC-001).
