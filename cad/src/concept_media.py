"""CollarDrive concept media from the TRL 3 parametric model (constructable design, CLD-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything. On a small machine run one picture per process.
Geometry comes from cad/src/model.py; flow values come from CLD-CAL-001 (docs/04-calcs/sizing.py).

Axes: X along the frame (pump end -X, drive end +X), Y across (+Y belt side), Z up from the ground.
The ground patch round the collar is context only: it shows where the shaft opening is (1.2 m square
drawn). The rising main, rope and duct are drawn shortened, 2.4 m down.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src"), str(ROOT / "docs/04-calcs")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
from model import build_parts, box  # noqa: E402

PROJECT, TITLE, DWG, DATE = "CollarDrive", "Surface drive for a rope pump and blower at a shaft collar", "CLD-DWG-010", "2026-10-03"
MD = ROOT / "media"
NO_CUT = ("Belt guard", "Pump wheel hood", "Exhaust extension", "Exhaust stands")


def parts():
    return [Part(n, s, c, b, e) for n, s, c, b, e in build_parts()]


def ground():
    g = box(-2100, 2800, -1400, 1100, -60, 0) - box(-600, 600, -600, 600, -61, 1)
    return Part("Ground and shaft collar (context)", g, "#D6C7A8", None, (0, 0, 0), 1.0)


def person():
    return K.human_figure(1750.0, x=-1500.0, y=-1000.0, z=0.0)


def hero():
    ps = parts() + [ground(), person()]
    return K._render(ps, MD / "hero.png", title=PROJECT, elev=26, azim=-62,
                     note="Seen from the front right and above, 26 deg elevation. Grey figure: 1.75 m person for scale, "
                          "standing beside the collar. Pipe, rope and duct drawn shortened; exhaust riser at right")


def cutaway():
    ps = [p for p in parts() if p.name not in NO_CUT]
    ps = [p for p in ps if p.shape.bounding_box().min.X < 2300]
    return K._render(K.cutaway_parts(ps, keep="+Y"), MD / "cutaway.png", azim=-90, elev=12, title=f"{PROJECT}: cutaway",
                     note="Cut on the frame centre line, front half removed, guards and exhaust left out; seen from the front, "
                          "12 deg elevation. Rope up the rising main, over the wheel, down to the guide block; duct beside it")


def exploded():
    ps = [p for p in parts() if p.bom not in (26, 27)]
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     elev=24, azim=-58, size=(10, 7.5),
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv. "
                          "Exhaust extension (26, 27) not shown")


def web():
    """Coarse glTF tessellation (1 mm chord, 0.35 rad) keeps media/model.glb small enough for the website."""
    import functools
    import build123d as bd
    orig = bd.export_gltf
    bd.export_gltf = functools.partial(orig, linear_deflection=1.0, angular_deflection=0.35)
    try:
        return K.export_web_model(parts(), "media", title=f"{PROJECT}: {TITLE}")
    finally:
        bd.export_gltf = orig


def flow():
    import sizing
    r = sizing.results()
    return K.flow_diagram(
        [("Fuel", round(r["fuel_kw"], 1)), ("Engine shaft", round(r["shaft_kw"], 2)), ("Layshaft", round(r["lay_kw"], 2)),
         ("Rope pump at 20 m", round(r["rope_kw_20"], 2)), ("Water lifted", round(r["hyd_kw_20"], 2))],
        MD / "flow.png", f"{PROJECT}: power flow at 20 m head, pump and blower running (all values are estimates)", "kW",
        [(0, "Engine heat and exhaust (est.)", round(r["fuel_kw"] - r["shaft_kw"], 1)),
         (1, "Belt losses (est.)", round(r["belt_loss_kw"], 2)),
         (2, "Blower, to 0.15 m3/s air (est.)", round(r["blower_kw"], 2)),
         (3, "Rope pump losses and leakage (est.)", round(r["rope_kw_20"] - r["hyd_kw_20"], 2))])


def blueprint():
    import sizing
    from build123d import Compound
    from drawing import Sheet, project_views
    r = sizing.results()
    ps = parts()
    fig = person()
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in parts()] + [fig.shape]), MD / "_views_fig")["iso"]  # fresh shapes
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Massing model for concept communication", revisions=[("P1", "Concept sheet from the constructable model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", [
        "One 4.8 kW class engine kept on the surface",
        f"Water: {r['q20']:.0f} L/min at 20 m, {r['q60']:.0f} L/min at 60 m (est.)",
        f"Air: {r['air_end30']:.2f} m3/s at the end of 30 m of 200 mm duct (est.)",
        f"Shaft power used about {r['shaft_kw']:.1f} kW at 20 m head (est.)",
        f"Exhaust outlet {r['exh_collar']:.1f} m from the collar, {r['exh_intake']:.1f} m from the blower intake",
        f"Frame {r['frame_len']:.2f} m x {r['frame_w']:.2f} m in two bolted modules",
        f"Heaviest piece: span module, about {r['span_kg']:.0f} kg (four people)",
        "Belts, pulleys and wheel fully guarded; backstop on the wheel"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    import shutil
    shutil.rmtree(MD / "_views", ignore_errors=True); shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w]())
