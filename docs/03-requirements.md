---
doc_id: CLD-REQ-001
title: CollarDrive requirements
project: CollarDrive
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 update; targets confirmed as planning figures; R10 restated against the value-engineering target; concept status
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status from CLD-CAL-001 v0.2 on the constructable design (CLD-DDR-002); requirements decided under Amish's 2026-10-03 pre-approval
---

# CollarDrive requirements

All ten requirements are met on paper or by design on the constructable design (CLD-CAL-001 v0.2, Table 4). None is missed. One has a thin margin: at the 30 m design depth the two pump belts carry 92 % of their allowable pull, so the 40 mm rising main is not used below 30 m. The targets are planning figures, decided by Amish under his pre-approval of 2026-10-03 (CLD-DDR-001); they are to be checked with the co-design partner and by test at TRL 4.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CLD-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Engine stays on the surface | No part with combustion below collar level | Design review of the general arrangement | Met by design: engine on the drive module, 1.9 m or more from the shaft centre |
| R2 | Exhaust kept away from the shaft | Exhaust outlet at least 6 m (20 ft) from the collar and the blower intake | Layout check; later a carbon monoxide reading at the blower intake during a run | Met on paper: 7.05 m from the edge of a 1.5 m collar and 6.46 m from the intake, outlet 2.4 m high |
| R3 | Dewatering flow | At least 60 L/min at 20 m head | Calculation; later a flow test on a test well or tower | Met on paper: 75.7 L/min |
| R4 | Dewatering depth | Useful flow from 60 m (200 ft) | Calculation; later a flow test at depth | Met on paper with the 25 mm main below 45 m: 19.3 L/min |
| R5 | Air delivery | At least 0.1 m³/s (about 210 cfm) at the end of 30 m of duct | Calculation; later an anemometer at the duct outlet | Met on paper: 0.189 m³/s (0.153 m³/s at the end of 60 m) |
| R6 | Shared drive | Pump and blower run together from one engine of 5 kW (about 7 hp) or less | Power calculation; later a bench run | Met on paper: 0.78 kW at 30 m from a 4.8 kW class engine |
| R7 | Fits real collars | Frame spans collars from 0.8 to 1.5 m across | Model; later a fit check at partner sites | Met by design: sleeper edges at least 0.35 m clear of a 1.5 m collar |
| R8 | Locally buildable | Built from common steel sections with a stick welder and hand tools | Build plan review with a local workshop | Met by design: RHS, SHS, plate and bar; heaviest piece 69.6 kg; shafts turned and keyed by a local machine shop |
| R9 | Guarded drive | All belts, pulleys and shafts fully guarded; the wheel cannot run back | Guarding review; later an inspection | Met by design: belt guard, layshaft cover, wheel hood, meshed blower inlet, ratchet backstop |
| R10 | Cost against the value-engineering target | Value-engineering target USD 3,500 for the full kit | Costed bill of materials | Under the target: estimated USD 2,535, USD 965 under |

## Assumptions

- Miners already own or can buy a small petrol or diesel engine of the 4.8 kW (6.5 hp) class.
- A rope pump handles the grit in shaft water with an acceptable rope and piston life; to be checked at TRL 4.
- The planning figure of 0.05 m³/s of fresh air per person at the face is a starting point, not a regulation; the co-design partner and local rules may require more.
- Shaft collars are stable enough for sleepers set back 0.35 m from their edge.

## Safety

> **Safety:** Meeting these requirements keeps the engine and its exhaust out of the shaft; it does not make the shaft safe to enter. A gas detector (carbon monoxide and oxygen) is used before and during any work below ground. The collar is fenced and the frame is never stood on. All moving parts are guarded, and the engine is stopped before anyone touches the drive.
