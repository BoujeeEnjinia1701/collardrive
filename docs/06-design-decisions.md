---
doc_id: CLD-DEC-001
title: CollarDrive design decisions register
project: CollarDrive
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; every decision made under Amish's 2026-10-03 pre-approval
---

# CollarDrive design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below are safety decisions (exhaust distance, backstop, guards, gas detector, no standing on the frame). Each takes the conservative option; the record says what evidence would relax it.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The pillow blocks' bolt centres and hole size (about 127 mm for UCP206 and 105 mm for UCP205) | They set the holes in the pedestal plates | CLD-DDR-002; CLD-DWG-103 |
| 2 | The engine's foot pattern, shaft height (150 mm assumed) and muffler outlet size | They set the engine plate holes, the belt line and the exhaust hose | CLD-DDR-002; CLD-DWG-112 |
| 3 | The blower's feet, outlet height (112 mm above its plate assumed), inlet flange and its curve at 2,000 rpm (0.15 m³/s at 500 Pa or better) | They set the blower plate holes, the flexible link and the air delivered | CLD-CAL-001, assumption 9 |
| 4 | The V-belt lengths (about A126, A128 and A82) once the plates are set | Standard lengths are chosen from the measured centres | CLD-CAL-001 [A3] |
| 5 | The taper bush sizes for each pulley bought | They set the keyway positions on both shafts | CLD-DWG-106, CLD-DWG-107 |
| 6 | The tyre sidewall thickness and the rope's grip in the V | Sets the wheel's bolt length and whether a liner is needed | CLD-DWG-108 |
| 7 | The rising main's actual bore (36.2 mm assumed for 40 mm PN10) | Sets the piston diameter | CLD-DWG-120 |
| 8 | The collar size and ground at the first site | Sleeper set-back and stake length | CLD-DDR-001, D7 |

## Value engineering

Value-engineering target: USD 3,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,535 (USD 965 under the target). Main cost drivers and savings worth trying:

- The largest lines are the blower with its plate and inlet guard (USD 340), the gas detector (USD 320), the engine and plate (USD 215), 30 m of lay-flat duct (USD 195), the pulleys (USD 165) and the belt guard (USD 120).
- Savings worth trying: a locally made centrifugal blower in place of a bought one; a smaller 2 to 3 kW engine, since the load is under 0.8 kW (kept at the 4.8 kW class for now because it is sold and repaired everywhere); the gas detector shared between kits at one site is not a saving to take, because every crew going below ground needs one.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Engine: 4.8 kW class petrol, governed to 2,800 rpm; a diesel of similar size fits the same plate | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | CLD-DDR-001, D1 |
| 2026-10-03 | Drive: engine to layshaft, two A belts to the pump, one A belt to the blower | Amish, same pre-approval | CLD-DDR-001, D2 |
| 2026-10-03 | Idler clutch on the pump belts, lever latched in the guard | Amish, same pre-approval | CLD-DDR-001, D3 |
| 2026-10-03 | Rope pump with a 400 mm tyre-sidewall wheel; main 40 mm to 30 m, 32 mm to 45 m, 25 mm to 60 m | Amish, same pre-approval | CLD-DDR-001, D4 |
| 2026-10-03 | Forcing ventilation through 200 mm lay-flat duct | Amish, same pre-approval | CLD-DDR-001, D5 |
| 2026-10-03 | Exhaust riser 2.4 m high, at least 6 m from the collar and the intake, downwind; the 6 m stays until intake carbon monoxide readings in varied winds show otherwise | Amish, same pre-approval | CLD-DDR-001, D6 |
| 2026-10-03 | Two carried modules on three staked sleepers set at least 0.35 m back from the collar | Amish, same pre-approval | CLD-DDR-001, D7 |
| 2026-10-03 | Ratchet backstop on every kit, until a test shows running back cannot hurt | Amish, same pre-approval | CLD-DDR-001, D8 |
| 2026-10-03 | Full guarding of belts, pulleys, shafts and wheel; meshed blower inlet | Amish, same pre-approval | CLD-DDR-001, D9 |
| 2026-10-03 | Personal carbon monoxide and oxygen detector in every kit | Amish, same pre-approval | CLD-DDR-001, D10 |
| 2026-10-03 | Pump and air only; no hoist; the frame is never stood on; the collar is fenced | Amish, same pre-approval | CLD-DDR-001, D11 |
| 2026-10-03 | Priced kit for a 30 m shaft with 30 m of duct | Amish, same pre-approval | CLD-DDR-001, D12 |
| 2026-10-03 | First candidate partners to approach (not agreed): an artisanal mining cooperative through a national artisanal miners' body with a university mining department; a local rope pump maker through the Practica Foundation network | Amish, same pre-approval | CLD-DDR-001, D13 |
| 2026-10-03 | First candidate region to approach (not agreed): Zimbabwe (Mashonaland West), then Nigeria (Kano State) | Amish, same pre-approval | CLD-DDR-001, D14 |
| 2026-10-03 | Design for construction: two bolted modules, sleepers and stakes, two-belt pump stage, idler clutch, pedestals, backstop, wheel, pipe head, guide block, duct head, slotted plates, guards, exhaust layout, discharge hose, crossbar positions | Amish, same pre-approval | CLD-DDR-002, Table 1 |
| 2026-10-03 | Cost against the target: USD 2,535 against the USD 3,500 value-engineering target; budget_usd unchanged | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | CLD-CAL-001 [H2] |
