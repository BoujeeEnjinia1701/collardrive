"""CollarDrive product appearance model (build123d), TRL 3, constructable design (CLD-DDR-002).

Finished-product look for photoreal renders, built from the constructable model: every component of
cad/src/model.py components() is used as it is (sleepers and stakes, the two bolted frame modules,
pedestals and pillow blocks, the rope pump wheel, backstop, pulleys, V-belts and idler clutch, engine and
blower on their slotted plates, guards and hood, pipe head and tee, rising main, rope and pistons, guide
block, support wire, duct head, lay-flat duct and flexible link, exhaust hose, pipe, riser and stands, and
the discharge hose). Only context is added: a patch of ground with a 1.2 m square shaft opening, the shaft
walls drawn 2.6 m down (so the shortened pipe, rope and duct hang in a shaft), and a 1.75 m mannequin
standing in front of the blower for scale. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail.
CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the frame (pump end -X, drive end +X), Y across (-Y front, +Y belt side), Z up.
Groups: "frame" (ground hardware and the two modules), "drive" (shafts, wheel, pulleys, belts, clutch,
engine, blower, backstop), "guard" (belt guard, hood, layshaft cover), "down" (pipe head, main, rope,
guide block, duct), "exhaust" and "context" (ground, shaft, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos  # noqa: E402
from model import BOM_EXPLODE, PARAMS, box, components  # noqa: E402

TITLE = "CollarDrive: surface engine driving a rope pump and mine blower from the shaft collar"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["frame", "drive", "guard", "down", "exhaust", "context"], "explode": False,
     "el": 28, "az": -40,
     "note": "Product render from the front right and above (about 28 deg elevation): the two-module frame on "
             "timber sleepers over a shaft collar, engine and blower on the drive module, belts and wheel under "
             "their guards, rising main and duct hanging in the shaft (drawn shortened), exhaust riser at right, "
             "downwind; 1.75 m person in front of the blower for scale"},
    {"name": "exploded", "groups": ["frame", "drive", "guard", "down"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): sleepers and stakes, span "
             "and drive modules, bearings and shafts, wheel, pump pulley, backstop, pulleys, belts, clutch, "
             "engine, blower, guards, pipe head, rising main, guide block, duct head and duct (drawn shortened); "
             "exhaust extension not shown"},
    {"name": "detail", "groups": ["drive"], "explode": False, "el": 16, "az": 35,
     "note": "Detail from the back right (belt side), about 16 deg elevation, with the guards, frame and hood "
             "removed for clarity: engine to layshaft, two belts to the 560 mm pump pulley with the idler "
             "clutch on their slack strand, one belt to the blower, and the ratchet backstop behind the wheel"},
]

C_FRAME = "#3F4650"
C_STEEL = "#8A9099"
C_ZINC = "#B8BEC6"
C_GUARD = "#E0B321"
C_TIMBER = "#7A5A3C"
C_RUBBER = "#1E1F22"
C_ENGINE = "#B42318"
C_BLOWER = "#1C7FB8"
C_PVC = "#E6E7E9"
C_DUCT = "#E66A1E"
C_ROPE = "#E3A21A"
C_ACCENT = "#0F766E"
C_GROUND = "#B9A27E"
C_SHAFT = "#5A4936"
C_CLAY = "#B9B4AC"

# model key: (display name, colour, material, group)
LOOK = {
    "sleepers": ("Timber sleepers (3)", C_TIMBER, "wood", "frame"),
    "stakes": ("Steel stakes (6)", C_STEEL, "metal", "frame"),
    "cleats": ("Hold-down cleats (4)", C_FRAME, "painted", "frame"),
    "screws": ("Coach screws, zinc plated", C_ZINC, "metal", "frame"),
    "span": ("Span module (painted steel)", C_FRAME, "painted", "frame"),
    "pedestals": ("Bearing pedestals (painted steel)", C_FRAME, "painted", "frame"),
    "drive": ("Drive module (painted steel)", C_FRAME, "painted", "frame"),
    "joint_bolts": ("Module joint bolts M16", C_ZINC, "metal", "frame"),
    "bearings": ("Pillow block bearings (cast iron)", "#2B2F36", "painted", "drive"),
    "pump_shaft": ("Pump wheel shaft (bright steel)", C_STEEL, "metal", "drive"),
    "layshaft": ("Layshaft (bright steel)", C_STEEL, "metal", "drive"),
    "wheel": ("Rope pump wheel, tyre rubber V", C_RUBBER, "rubber", "drive"),
    "ring": ("Pump pulley, 560 mm (cast iron, painted)", C_ACCENT, "painted", "drive"),
    "ratchet": ("Backstop ratchet (steel)", "#A15C12", "painted", "drive"),
    "pawl": ("Backstop pawl and post (painted steel)", "#C2271D", "painted", "drive"),
    "lay_pulleys": ("Layshaft pulleys (cast iron)", "#59606A", "painted", "drive"),
    "eng_pulley": ("Engine pulley (cast iron)", "#59606A", "painted", "drive"),
    "blow_pulley": ("Blower pulley (cast iron)", "#59606A", "painted", "drive"),
    "belts": ("V-belts (rubber)", C_RUBBER, "rubber", "drive"),
    "idler": ("Idler pulley", C_ZINC, "metal", "drive"),
    "clutch": ("Clutch lever, arm and pivot (painted steel)", "#C2410C", "painted", "drive"),
    "idler_post": ("Idler pivot post (painted steel)", C_FRAME, "painted", "drive"),
    "eng_plate": ("Engine plate (painted steel)", C_FRAME, "painted", "drive"),
    "engine": ("Engine, 4.8 kW petrol (painted steel)", C_ENGINE, "painted", "drive"),
    "blow_plate": ("Blower plate (painted steel)", C_FRAME, "painted", "drive"),
    "blower": ("Centrifugal blower (painted steel)", C_BLOWER, "painted", "drive"),
    "inlet_guard": ("Blower inlet guard (zinc plated mesh)", C_ZINC, "metal", "drive"),
    "lay_cover": ("Layshaft cover (painted sheet steel)", C_GUARD, "painted", "guard"),
    "guard": ("Belt guard (painted sheet steel and mesh)", C_GUARD, "painted", "guard"),
    "guard_brackets": ("Guard brackets (painted steel)", C_FRAME, "painted", "guard"),
    "hood": ("Pump wheel hood (painted sheet steel)", C_GUARD, "painted", "guard"),
    "pipe_head": ("Pipe head plate and clamp (painted steel)", C_ACCENT, "painted", "down"),
    "tee": ("Outlet tee, spout and rope exit (PVC)", C_PVC, "plastic", "down"),
    "main": ("Rising main, 40 mm PVC", C_PVC, "plastic", "down"),
    "guide": ("Guide block (painted steel)", C_FRAME, "painted", "down"),
    "guide_weights": ("Guide block weights (steel)", C_STEEL, "metal", "down"),
    "roller": ("Guide roller (HDPE)", "#EDEBE7", "plastic", "down"),
    "rope": ("Rope, 6 mm polypropylene", C_ROPE, "plastic", "down"),
    "pistons": ("Rope pistons (HDPE)", "#2563EB", "plastic", "down"),
    "wire": ("Support wire (galvanised)", C_ZINC, "metal", "down"),
    "duct_head": ("Duct head bend (galvanised)", C_ZINC, "metal", "down"),
    "saddle": ("Duct saddle and strap (painted steel)", C_FRAME, "painted", "down"),
    "duct": ("Lay-flat duct, 200 mm (PVC-coated fabric)", C_DUCT, "plastic", "down"),
    "flex": ("Flexible duct link, 200 mm", "#F08A3C", "plastic", "down"),
    "exh_hose": ("Exhaust flexible hose (stainless)", "#C9CCD1", "metal", "exhaust"),
    "exhaust": ("Exhaust pipe, riser and cap (galvanised)", C_ZINC, "metal", "exhaust"),
    "stands": ("Exhaust stands (painted steel)", C_FRAME, "painted", "exhaust"),
    "dis_hose": ("Discharge hose, 40 mm (rubber)", "#1D4ED8", "rubber", "down"),
}


def product_parts(P=PARAMS):
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for c in components(P):
        name, color, material, group = LOOK[c.key]
        add(name, c.shape, color, material, c.bom, group, BOM_EXPLODE.get(c.bom, (0, 0, 0)))

    # context: ground with a 1.2 m square shaft opening, shaft walls, and a 1.75 m person for scale
    ground = box(-2600, 8400, -1700, 1500, -60, 0) - box(-600, 600, -600, 600, -61, 1)
    add("Ground (context)", ground, C_GROUND, "paper", None, "context")
    shaft = box(-700, 700, -700, 700, -2600, -60) - box(-600, 600, -600, 600, -2601, -59)
    add("Shaft walls (context)", shaft, C_SHAFT, "paper", None, "context")
    from context_parts import mannequin
    person = Pos(1650, -1050, 0) * mannequin(1750, "stand")
    add("Person, 1.75 m mannequin (scale)", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:8s} {p['material']:8s} vol={s.volume / 1000:11.1f} cm3")
