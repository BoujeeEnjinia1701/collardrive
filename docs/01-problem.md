---
doc_id: CLD-PRB-001
title: CollarDrive problem statement
project: CollarDrive
doc_type: Problem statement
version: "0.2"
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
  change: TRL 2 and TRL 3 update; open questions answered from CLD-CAL-001 and CLD-DDR-001; first candidate partners and region; safety section
---

# CollarDrive problem statement

Artisanal miners need to pump water out of their shafts and get air in. The machines they can afford are small petrol pumps and generators, and they take them down the shaft, where the exhaust has nowhere to go.

## The problem

Small-engine exhaust can build to fatal carbon monoxide levels within minutes in partly enclosed spaces ([NIOSH](https://www.cdc.gov/niosh/topics/co/)). Artisanal shafts are narrow, deep and usually have no ventilation, so an engine running below the collar poisons the air for everyone in the shaft. Deaths are reported from Nigeria ([Channels TV, 2026](https://www.channelstv.com/2026/07/02/toxic-fumes-kill-three-miners-in-kano/)) and Zimbabwe ([ZBC News, 2024](https://www.zbcnews.co.zw/three-artisanal-miners-die-from-poisonous-gas-in-mapinga/)), and in the Philippines rescuers died after the first miner collapsed ([Inquirer, 2023](https://newsinfo.inquirer.net/1741817/3-miners-die-in-alleged-noxious-fume-poisoning-in-davao-de-oro-gold-mining-tunnel)).

The pieces of a safer setup exist. The rope pump is an old, open design that lifts water with a loop of rope and pistons in a pipe; about 120,000 are in use in over 25 countries ([Akvopedia](https://akvopedia.org/wiki/Rope_pump)). A motorised version delivers 120 L/min at 10 m and 20 L/min at 60 m from a 1 to 2 hp engine on a belt ([Engineering for Change](https://www.engineeringforchange.org/solutions/product/practica-motorized-rope-pump/)). Commercial confined-space blowers push air down ducts, losing about a third of their flow through 7.6 m (25 ft) of duct with one bend ([Air Systems](https://www.airsystems.com/manuals/SVB%20Series.pdf)). What is missing is one open frame, sized for a hand-dug shaft collar, that runs both from a single engine kept on the surface.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Artisanal miners and pit owners | Drain water and get fresh air to the working face without taking an engine down | Hand-dug shafts, often 10 to 60 m deep, in remote sites |
| Local welders and pump makers | A frame and drive they can build from common steel and parts | Small workshops in mining towns |
| Mining cooperatives and formalisation programmes | An affordable safety upgrade to promote with licensing and training | Government and NGO programmes |
| Hand-dug well builders | Dewatering and air while digging below the water table | Village well construction |

## Operating environment

- Outdoor collar on soft, wet or rocky ground; hot, dusty and rainy seasons.
- Shaft depths assumed 10 to 60 m (33 to 200 ft) and collar openings about 0.8 to 1.5 m (estimate, to be checked with partners).
- Water in the shaft may be muddy and carry sand and grit.
- Shaft air may already be low in oxygen or carry gases from blasting and ground.
- Engines are small petrol or diesel units sold locally, run and repaired by miners.

## Constraints

- Prototype budget ceiling USD 3,500 for frame, drive, rope pump, blower and duct.
- One engine drives both the pump and the blower; the engine never goes below the collar.
- Engine exhaust discharged well away from the collar and the blower intake.
- Buildable by local welders with common steel sections and hand tools.
- Open design: hardware under CERN-OHL-S-2.0.

## Out of scope

- Hoisting ore or people.
- Ground support, shaft lining and collapse prevention.
- Blasting fumes management beyond general ventilation.
- Mercury and processing hazards.
- Certified mine ventilation design for regulated mines.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Rope pump (rope and washer pump) | Open, centuries-old design lifting water with a rope loop and pistons in a pipe | Designed for wells, not for mine collars or paired with ventilation | [link](https://akvopedia.org/wiki/Rope_pump) |
| Practica motorized rope pump | Belt-driven rope pump for depths of 7 to 60 m, about USD 645 | Pump only; no ventilation and no collar frame | [link](https://www.engineeringforchange.org/solutions/product/practica-motorized-rope-pump/) |
| Multifunctional platform (MFP) | Village diesel engine driving mills, pumps and generators; about 500 installed in Mali from 1999 to 2004 | Built for village services, not for mine shafts or ventilation | [link](https://en.wikipedia.org/wiki/Multifunction_platform) |
| Air Systems saddle vent blower | Confined-space blower with duct; petrol and electric models | Costly, separate from dewatering, and a petrol model near a shaft opening can itself draw in exhaust | [link](https://www.airsystems.com/manuals/SVB%20Series.pdf) |

## Co-design

An artisanal mining cooperative working with a mining NGO or a university mining department, so the frame is sized to real collars and shaft depths, and a local rope pump maker who already builds and services pumps in the region.

## Questions answered at TRL 3

| Question | Answer | Source |
| --- | --- | --- |
| What pump flow and air flow do typical shafts need? | Planning figures: 60 L/min at 20 m for dewatering, and 0.05 m³/s for each person at the face; the design gives about 76 L/min at 20 m and 0.19 m³/s, enough for about four people | CLD-REQ-001, CLD-CAL-001 sections B and C |
| How much air is lost over 30 to 60 m of flexible duct? | About 10 % of the air through couplings per 30 m, and friction that cuts the blower's flow from 0.25 to 0.21 m³/s at 30 m; 0.15 m³/s still reaches the end of 60 m | CLD-CAL-001 section C |
| Should the frame also carry a hoist? | No. Pump and air only; hoisting is a separate, much higher hazard | CLD-DDR-001, D11 |
| How to stop miners moving the engine back into the shaft? | The engine is bolted to a plate on the drive module, away from the opening, and the pump and air only work from the frame; the kit adds a gas detector. Training with the co-design partner is the main control | CLD-DDR-001, D1, D10 |
| Which cooperative and region would host a first trial? | First candidates to approach, not agreed: an artisanal mining cooperative in Zimbabwe (Mashonaland West), through a national artisanal miners' body, with a university mining department; Nigeria (Kano State) next | CLD-DDR-001, D13 and D14 |

## Safety

> **Safety:** The problem is a deadly one, and CollarDrive only removes one cause of it: an engine running below the collar. Shafts can also be short of oxygen or hold gases from blasting and the ground, so a gas detector is used before and during any work below ground. The collar is an open drop; it is fenced, and nobody stands on the frame. The drive has belts and a rope that can catch hands and clothing; it is fully guarded, and the engine is stopped before anyone touches it.
