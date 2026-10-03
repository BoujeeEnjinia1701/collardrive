"""CollarDrive general arrangement drawing CLD-DWG-001 (Rev P2).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/CLD-DWG-001.svg, .pdf and .png from the parametric model. The orthographic views show the
frame, drive and shaft hardware (pipe, rope and duct drawn shortened, 2.4 m down); the exhaust extension appears
in the site layout view. Figures in the notes come from CLD-CAL-001 (python docs/04-calcs/sizing.py).
The concept sheet in media/ is CLD-DWG-010; the making sketches are CLD-DWG-101 onward.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src"), str(ROOT / "docs/04-calcs")]
from drawing import Sheet, project_views  # noqa: E402
from build123d import Compound  # noqa: E402
from model import PARAMS as P, components  # noqa: E402
import sizing  # noqa: E402

SITE_ONLY = ("exhaust", "stands")
# Each compound gets its own components: a shape can belong to one compound only
frame = Compound(children=[c.shape for c in components() if c.key not in SITE_ONLY])
site = Compound(children=[c.shape for c in components()])
work = ROOT / "cad/drawings/_views"
views = project_views(frame, work)
site_views = project_views(site, work / "site")

d = sizing.drive(); p20 = sizing.pump(20.0); p60 = sizing.pump(60.0); b30 = sizing.blower(30.0); ex = sizing.exhaust()
pw = sizing.power(30.0); m = sizing.mass()
s = Sheet(project="CollarDrive", title="Collar frame with surface engine, rope pump and blower: general arrangement",
          dwg_no="CLD-DWG-001", rev="P2", author="Amish Chadha", date="2026-10-03", concept=True, scale=None,
          material="RHS 100 x 50 x 3 and SHS 50 x 50 x 3, S275; bought engine, blower, bearings, pulleys. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (CLD-CAL-001)", "2026-10-03", "AC"),
                     ("P2", "Design for construction (CLD-DDR-002): two modules, two-belt pump drive", "2026-10-03", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 46, label="Isometric view", sublabel="Not to scale; pipe, rope and duct drawn shortened")
s.add_svg(site_views["top"], 276, 98, 140, 18, label="Site layout, top view",
          sublabel="Looking down; exhaust riser at right, downwind")
s.add_notes("Key dimensions (mm) and data", [
    f"Frame {(P['DRIVE_X1'] - P['SPAN_X0']):.0f} long x {2 * P['SILL_Y'] + P['SILL_W']:.0f} wide, two modules bolted at the joint",
    f"Sleepers at {P['SLEEPER_X'][0]:.0f}, {P['SLEEPER_X'][1]:.0f} and {P['SLEEPER_X'][2]:.0f} from the shaft centre",
    f"Rope wheel 400 rope circle at {P['WHEEL_Z']:.0f} up; rope down {abs(P['WHEEL_X'] - P['ROPE_PR']):.0f} left of centre",
    f"Rising main {P['WHEEL_X'] + P['ROPE_PR']:.0f} right of centre; duct drop {P['DUCT_DROP_X']:.0f} right of centre",
    f"Engine 2,800 rpm; layshaft {d['lay_rpm']:.0f}; wheel {d['wheel_rpm']:.0f}; blower {d['blower_rpm']:.0f} rpm",
    f"Pump belts 2 x A, idler clutch; belt lengths {d['st1']['nominal']}, {d['st2']['nominal']}, {d['blow']['nominal']}",
    f"Water {p20['q_lpm']:.0f} L/min at 20 m (40 mm main); {p60['q_lpm']:.0f} L/min at 60 m (25 mm)",
    f"Air {b30['q_end']:.2f} m3/s at the end of 30 m of 200 mm duct (est.)",
    f"Engine shaft {pw['shaft_kw']:.2f} kW at 30 m head; petrol about {pw['fuel_lph']:.1f} L/h",
    f"Exhaust outlet {P['EXH_TOP'] / 1000:.2f} m high, {ex['d_collar']:.1f} m from collar, {ex['d_intake']:.1f} m from intake",
    f"Span module about {m['span']:.0f} kg (four people); drive module {m['drive']:.0f} kg",
    "Backstop on the wheel; all belts, pulleys and the wheel guarded",
    "Never stand on the frame; fence the collar; gas detector below",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/CLD-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CLD-DWG-001.svg, .pdf, .png")
