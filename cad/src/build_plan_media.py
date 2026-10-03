"""CollarDrive prototype build plan pictures (CLD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. A single sheet, joint or step can be drawn with sheets:105,
joints:3 or steps:7 (one picture per process on a small machine). Every picture is drawn from
cad/src/model.py (components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CLD-DWG-101 to 123        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.

Axes as model.py: X along the frame (pump end -X, drive end +X, X = 0 on the shaft centre), Y across
(+Y is the belt side, -Y the front where the spout and the blower intake are), Z up from the ground.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, components, levels, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
PROJECT = "CollarDrive"
L = levels(P)


def _comps():
    return {c.key: c for c in components(P)}


C = _comps()


def child(key, i):
    """The i-th child of a compound component (children are in the order model.py builds them)."""
    ch = list(C[key].shape)
    return ch[i] if ch else C[key].shape


def fuse(shapes):
    from build123d import Compound
    return Compound(children=list(shapes))


def part(key_or_name, shape=None, color=None, explode=(0, 0, 0), alpha=1.0, name=None):
    if shape is None:
        c = C[key_or_name]
        return Part(name or c.name, c.shape, color or c.color, None, tuple(explode), alpha)
    return Part(key_or_name, shape, color or "#9CA3AF", None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & box(x0, x1, y0, y1, z0, z1)


def short(shape, z_min=-650.0):
    """Down-shaft parts drawn shorter still in the later pictures, so the frame stays large."""
    return shape & box(-3000, 9000, -3000, 3000, z_min, 4000)


def ground_context():
    g = box(-1800, 2700, -1100, 1100, -40, 0) - box(-600, 600, -600, 600, -41, 1)
    return Part("Ground; 1.2 m shaft opening (context)", g, "#D6C7A8", None, (0, 0, 0), 0.6)


# ----------------------------------------------------------------- named groups, in build order
def groups():
    pump_brg = fuse([child("bearings", 0), child("bearings", 1)])
    lay_brg = fuse([child("bearings", 2), child("bearings", 3)])
    return {
        "sleepers": part("Timber sleepers (3)", C["sleepers"].shape, C["sleepers"].color),
        "stakes": part("Steel stakes (6)", C["stakes"].shape, C["stakes"].color),
        "span": part("Span module with pedestals and cleats", fuse([C["span"].shape, C["pedestals"].shape, C["cleats"].shape]), C["span"].color),
        "screws": part("Coach screws (8)", C["screws"].shape, C["screws"].color),
        "drive": part("Drive module", C["drive"].shape, C["drive"].color),
        "bolts": part("Module joint bolts (8 x M16)", C["joint_bolts"].shape, C["joint_bolts"].color),
        "pump_set": part("Pump shaft, wheel, ratchet, bearings", fuse([C["pump_shaft"].shape, C["wheel"].shape, C["ratchet"].shape, pump_brg]), "#1F2937"),
        "ring": part("Pump pulley, 560 mm", C["ring"].shape, C["ring"].color),
        "pawl": part("Backstop pawl and post", C["pawl"].shape, C["pawl"].color),
        "lay_set": part("Layshaft, pulleys, bearings", fuse([C["layshaft"].shape, C["lay_pulleys"].shape, lay_brg]), C["lay_pulleys"].color),
        "eng_plate": part("Engine plate", C["eng_plate"].shape, C["eng_plate"].color),
        "engine": part("Engine with 80 mm pulley", fuse([C["engine"].shape, C["eng_pulley"].shape]), C["engine"].color),
        "blow_plate": part("Blower plate", C["blow_plate"].shape, C["blow_plate"].color),
        "blower": part("Blower with pulley and inlet guard", fuse([C["blower"].shape, C["blow_pulley"].shape, C["inlet_guard"].shape]), C["blower"].color),
        "belts": part("V-belts (4)", C["belts"].shape, C["belts"].color),
        "clutch": part("Clutch: idler, lever, pivot post", fuse([C["idler"].shape, C["clutch"].shape, C["idler_post"].shape]), C["clutch"].color),
        "guide": part("Guide block with roller and weights", fuse([C["guide"].shape, C["guide_weights"].shape, C["roller"].shape]), C["guide"].color),
        "main": part("Rising main and support wire", fuse([C["main"].shape, C["wire"].shape]), "#CBD5E1"),
        "rope": part("Rope and pistons", fuse([C["rope"].shape, C["pistons"].shape]), C["rope"].color),
        "pipe_head": part("Pipe head plate and clamp", C["pipe_head"].shape, C["pipe_head"].color),
        "tee": part("Outlet tee, spout, discharge hose", fuse([C["tee"].shape, C["dis_hose"].shape]), "#1D4ED8"),
        "duct_head": part("Duct head on saddle", fuse([C["duct_head"].shape, C["saddle"].shape]), C["duct_head"].color),
        "duct": part("Lay-flat duct", C["duct"].shape, C["duct"].color),
        "flex": part("Flexible duct link", C["flex"].shape, C["flex"].color),
        "lay_cover": part("Layshaft cover", C["lay_cover"].shape, C["lay_cover"].color),
        "guard": part("Belt guard with brackets", fuse([C["guard"].shape, C["guard_brackets"].shape]), C["guard"].color),
        "hood": part("Pump wheel hood", C["hood"].shape, C["hood"].color),
        "exhaust": part("Exhaust hose, pipe, riser, cap", fuse([C["exh_hose"].shape, C["exhaust"].shape]), C["exhaust"].color),
        "stands": part("Exhaust stands (3)", C["stands"].shape, C["stands"].color),
    }


ORDER = ["sleepers", "stakes", "span", "screws", "drive", "bolts", "pump_set", "ring", "pawl", "lay_set", "eng_plate",
         "engine", "blow_plate", "blower", "belts", "clutch", "guide", "main", "rope", "pipe_head", "tee", "duct_head",
         "duct", "flex", "lay_cover", "guard", "hood", "exhaust", "stands"]


def overview():
    G = groups()
    off = {"sleepers": (0, 0, -500), "stakes": (0, 0, -1400), "span": (0, 0, 0), "screws": (0, 0, -260),
           "drive": (700, 0, 0), "bolts": (350, 0, -300), "pump_set": (0, 0, 650), "ring": (0, 750, 900),
           "pawl": (0, -650, 250), "lay_set": (0, 600, 450), "eng_plate": (700, 0, 300), "engine": (700, 0, 850),
           "blow_plate": (700, 0, 300), "blower": (700, -350, 850), "belts": (0, 1150, 450), "clutch": (0, 750, 1050),
           "guide": (0, 0, -900), "main": (0, 0, -350), "rope": (0, -500, -100), "pipe_head": (0, 0, 550),
           "tee": (0, -650, 600), "duct_head": (0, -550, 900), "duct": (0, -550, -350), "flex": (300, -850, 450),
           "lay_cover": (0, 0, 850), "guard": (0, 1500, 650), "hood": (0, 0, 1650), "exhaust": (700, 0, 400),
           "stands": (700, 0, 0)}
    parts = []
    for k in ORDER:
        p = G[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CollarDrive prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; pipe, rope and duct drawn shortened",
                       elev=22, azim=-55, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Plane
    G = groups()
    frame_ctx = [G["span"], G["drive"]]
    base = dict(project=PROJECT, date=DATE)
    out = []
    zt = L["z_top"]

    def sheet(n, prt, neigh, title, material, notes, **kw):
        if only is not None and n != only:
            return
        out.append(bv.component_sheet(prt, neigh, dwg_no=f"CLD-DWG-{n}", title=f"CollarDrive {title}: making sketch",
                                      material=material, notes=notes, out_dir=str(DWG), **base, **kw))

    sheet(101, part("span"), [G["sleepers"], G["drive"]], "span module",
          "RHS 100 x 50 x 3 and SHS 50 x 50 x 3, S275; 10 mm plate",
          ["Two sills: RHS 100 x 50 x 3, 2,750 mm, standing 100 mm tall.",
           "Sill centres 600 mm apart: outside width 650 mm.",
           "Six crossbars SHS 50 x 50 x 3, 550 mm, between the sills,",
           "  tops flush with the sill tops. Centres from the pump end:",
           "  25, 970, 1,430, 1,570, 2,070 and 2,715 mm.",
           "Pump end: weld a 3 mm cap over each sill end.",
           "Joint end: a 10 mm plate 150 x 170 mm on each sill end,",
           "  flush with the sill bottom, 50 mm out each side; four",
           "  18 mm holes 50 mm each side of the sill centre line,",
           "  25 and 145 mm up from the bottom of the plate.",
           "Drill the two plates clamped to the drive module's plates.",
           "Weld on a flat table, diagonals equal within 3 mm.",
           "Pedestals (DWG-103) and cleats (DWG-104) weld on after.",
           "Check: the frame sits flat; no rock on a level floor."],
          inset_view=(28, -55))
    sheet(102, part("drive"), [G["span"], G["sleepers"]], "drive module",
          "RHS 100 x 50 x 3 and SHS 50 x 50 x 3, S275; 10 mm plate",
          ["Two sills: RHS 100 x 50 x 3, 1,150 mm; centres 600 mm apart.",
           "Six crossbars SHS 50 x 50 x 3, 550 mm, tops flush.",
           "  Centres from the joint end: 35, 220, 480, 680, 920",
           "  and 1,125 mm. The 220 and 480 mm bars carry the",
           "  blower plate; the 680 and 920 mm bars the engine plate.",
           "Joint plates as the span module, at the joint end: 10 mm,",
           "  150 x 170 mm, four 18 mm holes drilled with the span",
           "  module's plates clamped to them, so the holes line up.",
           "Far end: a 3 mm cap over each sill end.",
           "Weld on a flat table, diagonals equal within 2 mm.",
           "Check: bolt it to the span module dry; the sill tops",
           "  line up within 2 mm across the joint."],
          inset_view=(28, -55))
    ped = child("pedestals", 0)
    sheet(103, Part("Bearing pedestal", ped, C["pedestals"].color), frame_ctx + [part("bearings")], "bearing pedestal",
          "SHS 60 x 60 x 4 and 10 mm plate, S275; make 4",
          ["Post SHS 60 x 60 x 4 with a 10 mm top plate 60 wide.",
           "Pump wheel pedestals (2, drawn): post 347 mm, plate",
           "  180 x 60 mm; plate top 357 mm above the sill top.",
           "Layshaft pedestals (2): post 304 mm, plate 160 x 60 mm;",
           "  plate top 314 mm above the sill top.",
           "Plate long way along the sill, centred on the post.",
           "Holes in the plate: two, to suit the pillow block bought",
           "  (about 127 mm centres for UCP206, 105 mm for UCP205);",
           "  mark them from the bearing itself.",
           "Weld each post square on the sill top, centred on the",
           "  sill: pump pair 150 mm toward the pump end from the",
           "  shaft centre, layshaft pair 950 mm toward the drive end.",
           "Check: a straight edge across each pair of plates; tops",
           "  level and in line within 1 mm."],
          inset_view=(30, -50))
    cle = child("cleats", 0)
    sheet(104, Part("Hold-down cleat", cle, C["cleats"].color), [G["span"], G["sleepers"], G["screws"]], "hold-down cleat",
          "Steel angle 50 x 50 x 5 or bent 5 mm plate, S275; make 4",
          ["Angle 50 x 50 x 5 cut 100 mm long; trim one leg to 40 mm.",
           "Upright leg 50 mm tall against the outside of the sill.",
           "Foot 40 mm wide lies on the sleeper.",
           "Two 14 mm holes in the foot, 50 mm apart, 30 mm out",
           "  from the sill face, for M12 coach screws.",
           "Weld the upright leg to the sill side, foot flat on the",
           "  sleeper: two cleats on the pump-end sleeper and two",
           "  on the joint sleeper, one each side.",
           "Weld with the frame sitting on its sleepers, so every",
           "  foot beds down flat.",
           "Check: each foot touches the timber all over."],
          inset_view=(30, -40))
    stk = child("stakes", 0)
    sheet(105, Part("Steel stake", stk, C["stakes"].color), [G["sleepers"]], "steel stake",
          "25 mm reinforcing bar and 6 mm plate washer; make 6",
          ["25 mm reinforcing bar, 830 mm long; grind one end to a point.",
           "Washer: 50 mm disc of 6 mm plate, 26 mm hole.",
           "Slide the washer on; weld it, underside 30 mm below the top.",
           "Drill each sleeper with a 28 mm hole, 400 mm each side",
           "  of its middle, before setting it out.",
           "Drive the stake through the sleeper until the washer",
           "  bears on the timber: 700 mm goes into the ground.",
           "In rock or hard laterite, drill a pilot hole first.",
           "Check: the stake does not move when pulled by hand."],
          inset_view=(30, -40))
    sheet(106, part("pump_shaft"), [part("bearings"), part("wheel"), part("ratchet"), part("ring")], "pump wheel shaft",
          "30 mm bright steel bar, EN8 or C45 class",
          ["30 mm bar, 830 mm long; chamfer both ends 1 mm.",
           "Distances from the hood-side end (front, -Y):",
           "  ratchet hub 155 to 185 mm;",
           "  bearing centres 60 and 660 mm;",
           "  wheel hub 420 to 500 mm;",
           "  pump pulley taper bush 790 to 830 mm.",
           "Cut an 8 mm keyway under the ratchet hub, the wheel hub",
           "  and the taper bush; keys 8 x 7 mm.",
           "Drill and tap M8 on each key seat for a grub screw.",
           "Bearings lock to the bar with their own grub screws.",
           "Check: the bar runs true in V-blocks within 0.2 mm."],
          inset_view=(25, -60))
    sheet(107, part("layshaft"), [part("bearings"), part("lay_pulleys"), part("lay_cover")], "layshaft",
          "25 mm bright steel bar, EN8 or C45 class",
          ["25 mm bar, 795 mm long; chamfer both ends 1 mm.",
           "Distances from the front end (-Y):",
           "  bearing centres 30 and 630 mm;",
           "  344 mm blower pulley bush 675 to 705 mm;",
           "  480 mm engine-stage pulley bush 705 to 735 mm;",
           "  90 mm two-groove pulley bush 760 to 795 mm.",
           "One 8 mm keyway from 670 mm to the end; keys 8 x 7 mm.",
           "Check: the bar runs true in V-blocks within 0.2 mm."],
          inset_view=(25, -60))
    sheet(108, part("wheel"), [part("pump_shaft"), part("bearings"), part("ratchet")], "rope pump wheel",
          "Steel tube hub, 6 mm plate web, two car tyre sidewalls",
          ["Hub: steel tube 70 mm OD, 80 mm long, bored 30 mm with",
           "  an 8 mm keyway; M8 grub screw over the key.",
           "Web: 6 mm plate disc 370 mm across, welded to the hub",
           "  at its middle, square to the bore.",
           "Rim: cut two sidewalls from a used car tyre, the bead",
           "  ring trimmed off, 470 mm outside diameter.",
           "Bolt them either side of the web rim with 12 M8 bolts",
           "  on a 420 mm circle; the two inner faces lean together",
           "  to form a V that grips the rope at a 400 mm circle.",
           "Width over the rubber 90 mm; groove 4 mm wide at the root.",
           "Check: spin it on the shaft; the V runs true within",
           "  3 mm; a 6 mm rope sits in it without bottoming."],
          inset_view=(20, -60))
    sheet(109, part("ratchet"), [part("pump_shaft"), part("pawl"), part("wheel")], "backstop ratchet",
          "10 mm steel plate and tube, S275",
          ["Plate: 10 mm, 220 mm across, 30 mm bore with keyway.",
           "Twelve teeth: notches 16 mm deep and 14 mm wide, every",
           "  30 degrees, the steep face leading in the pumping",
           "  direction, so the pawl drops in if the wheel runs back.",
           "Hub: tube 60 mm OD, 20 mm long, bored 30 mm with the",
           "  same keyway, welded to the face toward the wheel.",
           "Grind the tooth faces square and remove burrs.",
           "Check: the pawl nose sits fully in every notch."],
          inset_view=(15, -90))
    sheet(110, part("pawl"), [part("ratchet"), part("span"), part("pump_shaft")], "backstop pawl and post",
          "40 x 20 mm flat bar, 12 mm round bar, 10 mm pin; spring",
          ["Post: 40 x 20 mm bar, 295 mm, welded upright on the",
           "  crossbar 20 mm toward the pump end from the shaft",
           "  centre, 100 mm in from the front sill centre line.",
           "Pivot: 10 mm hole 280 mm above the crossbar top.",
           "Pawl: 12 mm round bar from the pivot to the nose, about",
           "  75 mm; nose block 20 x 10 x 10 mm welded on the end.",
           "Pin: 10 mm, 30 mm long, with a washer and split pin.",
           "Spring: light tension spring from the pawl to the post",
           "  keeps the nose on the ratchet.",
           "Check: turning the wheel forward the pawl clicks over",
           "  each tooth; turning it back the pawl locks it at once."],
          inset_view=(15, -90))
    sheet(111, Part("Clutch lever, arm and pivot post", fuse([C["clutch"].shape, C["idler_post"].shape]), C["clutch"].color),
          [part("idler"), part("belts"), part("span"), part("ring")], "clutch lever and pivot post",
          "16 and 18 mm round bar, 40 x 10 mm flat bar; bought idler",
          ["Pivot post: 40 x 10 mm flat bar, 725 mm, welded to the",
           "  outside of the back sill 700 mm from the shaft centre;",
           "  one M12 bolt through the sill as a second fixing.",
           "Pivot hole 16 mm, 620 mm above the sill top.",
           "Pivot pin: 16 mm bar 195 mm, through the post and the",
           "  belt guard, welded to the arm and the lever.",
           "Arm: 16 mm bar from the pivot to the idler axle,",
           "  about 250 mm; idler axle 16 mm, 62 mm long.",
           "Lever: 18 mm bar 250 mm up from the pivot outside the",
           "  guard, with a 32 mm knob.",
           "Over centre: in the up position the idler presses the",
           "  slack strand 25 mm; latch the lever in the guard plate.",
           "Check: lever down, the pump belts go slack and the",
           "  wheel stops while the layshaft turns."],
          inset_view=(15, 60))
    sheet(112, part("eng_plate"), [part("drive"), part("engine")], "engine plate",
          "8 mm steel plate, S275",
          ["Plate 8 mm, 340 x 400 mm (400 across the frame).",
           "Four slots 14 mm wide, 60 mm long, along the frame,",
           "  over the crossbars 680 and 920 mm from the joint end,",
           "  40 mm in from the front edge and 40 mm from the back.",
           "M12 bolts through the slots into the crossbars (drill",
           "  the crossbars through the slot middles).",
           "Engine holes: mark from the engine's own base, so the",
           "  shaft sits 150 mm above the plate, crankshaft toward",
           "  the belt side, square to the frame.",
           "Check: the plate slides 60 mm along the frame to",
           "  tension the engine belt."],
          inset_view=(30, -55))
    sheet(113, part("blow_plate"), [part("drive"), part("blower")], "blower plate",
          "8 mm steel plate, S275",
          ["Plate 8 mm, 380 x 440 mm (440 across the frame).",
           "Four slots 14 mm wide, 60 mm long, along the frame,",
           "  over the crossbars 220 and 480 mm from the joint end,",
           "  50 mm in from the front edge and 50 mm from the back.",
           "M12 bolts through the slots into the crossbars.",
           "Blower feet holes: mark from the blower bought, outlet",
           "  toward the pump end, inlet facing the front (-Y).",
           "Check: the plate slides 60 mm to tension the belt;",
           "  the blower outlet lines up with the flexible link."],
          inset_view=(30, -55))
    sheet(114, part("inlet_guard"), [part("blower")], "blower inlet guard",
          "6 mm welded mesh, 2 mm sheet ring; zinc plated or painted",
          ["Disc of 6 mm square mesh, 216 mm across, on a 2 mm",
           "  sheet ring 216 mm outside, 196 mm inside.",
           "Four tabs with 7 mm holes to the blower inlet flange.",
           "Mesh openings must stop a finger reaching the impeller.",
           "Check: a 6 mm rod cannot pass the mesh."],
          inset_view=(15, -80))
    sheet(115, part("lay_cover"), [part("layshaft"), part("pedestals"), part("lay_pulleys")], "layshaft cover",
          "2 mm steel sheet",
          ["Folded inverted U: 90 mm wide, 115 mm tall, 540 mm long.",
           "Open at the bottom; covers the layshaft between the",
           "  two pillow blocks.",
           "Two 20 x 2 mm tabs each side at the bottom, with 7 mm",
           "  holes, bolted to the pedestal plates with M6 bolts.",
           "Clearance to the turning shaft at least 20 mm all round.",
           "Check: the shaft turns without touching it."],
          inset_view=(25, -60))
    sheet(116, Part("Belt guard with brackets", fuse([C["guard"].shape, C["guard_brackets"].shape]), C["guard"].color),
          [part("belts"), part("lay_pulleys"), part("ring"), part("span"), part("drive")], "belt guard",
          "Angle 20 x 20 x 3, 2 mm sheet, 12.7 x 1.6 mm welded mesh",
          ["Box 2,670 mm long, 152 mm deep, 642 mm tall, over",
           "  every belt and pulley on the belt side.",
           "Frame of 20 x 20 x 3 angle; top, bottom and ends 2 mm",
           "  sheet; sides of 12.7 mm welded mesh.",
           "Holes in the inner side for the four shafts: pump",
           "  shaft 40 mm, layshaft 35 mm, engine 30 mm, blower 34 mm,",
           "  centred on each shaft (mark them off the frame).",
           "Clutch pivot: 20 mm hole through both sides.",
           "Latch plate 80 x 110 mm on the outer side, slot for",
           "  the lever.",
           "Three brackets of 40 x 5 mm bar, L shaped, welded to the",
           "  outside of the back sill; the guard bolts to them, M8.",
           "Check: no belt or pulley can be touched from outside."],
          inset_view=(20, 60))
    sheet(117, part("hood"), [part("wheel"), part("span"), part("ring")], "pump wheel hood",
          "2 mm steel sheet",
          ["Box 600 mm along the frame, 520 mm across, 657 mm tall,",
           "  open at the bottom; 2 mm sheet folded and welded.",
           "Holes for the pump shaft, 40 mm, in both sides.",
           "Spout hole 48 mm in the front side, 100 mm up.",
           "Four tabs at the bottom, bolted to the crossbars,",
           "  M8: two flat at the drive end, two bent up at the",
           "  pump end.",
           "Clearance to the wheel and the ratchet at least 20 mm.",
           "Check: the wheel and pawl are covered on every side",
           "  above the frame."],
          inset_view=(25, -55))
    sheet(118, part("pipe_head"), [part("main"), part("tee"), part("span"), part("wire")], "pipe head plate and clamp",
          "8 mm steel plate; split collar from 70 mm tube",
          ["Plate 8 mm, 190 x 200 mm, lying across the two crossbars",
           "  either side of the shaft centre.",
           "42 mm hole for the rising main, 95 mm from the pump-end",
           "  edge and 100 mm from the front edge.",
           "Clamp: 70 mm tube, 30 mm long, bored 40 mm, sawn in",
           "  two and bolted round the main with two M8 bolts;",
           "  one half welded to the plate over the hole.",
           "M12 eye bolt underneath, 55 mm in front of the hole,",
           "  for the support wire.",
           "Four M10 bolts to the crossbars.",
           "Check: the main hangs plumb in the middle of the hole."],
          inset_view=(25, -55))
    sheet(119, Part("Guide block with roller and weights", fuse([C["guide"].shape, C["guide_weights"].shape, C["roller"].shape]), C["guide"].color),
          [part("main"), part("rope"), part("wire")], "guide block",
          "6 mm steel plate; HDPE roller; 12 mm stainless pin",
          ["Box of 6 mm plate, 200 x 120 x 300 mm tall.",
           "Top holes: 40 mm for the main, 20 mm for the rope down",
           "  run, 80 mm apart; a 52 mm socket 60 mm tall over the",
           "  main hole.",
           "Four slots 20 x 100 mm in each long side let water in.",
           "Roller: HDPE 74 mm across, 60 mm long, on a 12 mm",
           "  stainless pin through both long sides, 80 mm up from",
           "  the bottom; rope runs round it.",
           "Weights: two 25 mm steel plates 160 x 230 mm, about",
           "  7 kg each, bolted to the long sides.",
           "Eye on top for the support wire.",
           "Check: the rope runs round the roller and up the socket",
           "  without rubbing the box."],
          inset_view=(20, -55))
    pis = child("pistons", 0)
    sheet(120, Part("Piston", pis, C["pistons"].color), [part("rope")], "rope piston",
          "10 mm HDPE sheet; make 70 (one a metre)",
          ["Disc 35 mm across, 10 mm thick, from HDPE sheet.",
           "6.5 mm hole in the middle for the 6 mm rope.",
           "Light chamfer on the top edge so it enters the pipe.",
           "Hold each piston with a knot under it; one every metre.",
           "Deeper bands use smaller pistons: 27 mm for the 32 mm",
           "  main, 20 mm for the 25 mm main (1 mm clear in the bore).",
           "Check: each piston slides through a 1 m test length of",
           "  the main with a light, even drag."],
          inset_view=(25, -55))
    sheet(121, part("saddle"), [part("duct_head"), part("span")], "duct saddle and strap",
          "10 mm steel plate; 30 x 3 mm flat bar",
          ["Saddle: 50 mm plate block 140 mm across, 22 mm tall,",
           "  cut to a 100 mm radius on top to cradle the duct bend.",
           "Weld the saddle on the crossbar 2,070 mm from the pump",
           "  end of the span module.",
           "Strap: 30 x 3 mm flat bar bent round the duct with feet",
           "  down to the crossbar, an M8 bolt each side.",
           "Check: the duct head sits level and does not rock."],
          inset_view=(25, -55))
    ex = C["exhaust"].shape
    sheet(122, Part("Exhaust pipe, bend, riser and cap", ex, C["exhaust"].color), [part("stands"), part("exh_hose")],
          "exhaust extension", "40 mm (1-1/2 in) galvanised steel pipe; 3 mm sheet cap",
          ["Pipe: 40 mm nominal (48.3 mm OD) galvanised, about 5.0 m,",
           "  in two lengths joined with a socket.",
           "Bend: 90 degrees, 120 mm radius, threaded or welded.",
           "Riser: about 1.8 m, so the outlet is 2.4 m above the ground.",
           "Cap: 140 mm disc on three 6 mm legs 50 mm tall,",
           "  welded to the riser top: rain kept out, gas let out.",
           "Pipe end at the engine: fits the 0.3 m stainless",
           "  flexible hose with a band clamp.",
           "Grind off zinc before any weld; weld outdoors.",
           "Check: the outlet is at least 6 m from the collar edge",
           "  and from the blower intake."],
          inset_view=(25, -55))
    st0 = child("stands", 0)
    sheet(123, Part("Exhaust stand (low)", st0, C["stands"].color), [part("exhaust")], "exhaust stand",
          "SHS 40 x 40 x 3 and 6 mm plate, S275; two low, one tall",
          ["Base plate 6 mm, 200 x 200 mm, two 28 mm stake holes.",
           "Post SHS 40 x 40 x 3 welded in the middle, square.",
           "Low stands (2): post 490 mm, pipe centre 520 mm up.",
           "Tall stand (1): post 1,800 mm, beside the riser.",
           "U-bolt for the 48 mm pipe near the top of each post.",
           "Stake each base with two 25 mm stakes.",
           "Check: the pipe falls gently to the riser so water",
           "  drains away from the engine."],
          inset_view=(25, -55))
    return out


# ----------------------------------------------------------------- joint close-ups
def joints(only=None):
    out = []
    W = lambda key, *b: win(C[key].shape, *b)  # noqa: E731

    def jt(n, parts, title, sub, **kw):
        if only is not None and n != only:
            return
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    b = (-1380, -1120, 230, 470, -120, 290)
    jt(1, [part("Timber sleeper", W("sleepers", *b), C["sleepers"].color),
           part("Steel stake with washer", W("stakes", *b), C["stakes"].color),
           part("Span module sill", W("span", *b), C["span"].color),
           part("Hold-down cleat, welded to the sill", W("cleats", *b), "#B45309"),
           part("M12 coach screws", W("screws", *b), C["screws"].color)],
       "span module on the pump-end sleeper",
       "The sill sits on the timber; the cleat is welded to the sill and screwed down; the stake holds the sleeper",
       elev=28, azim=-40, size=(8, 6))
    b = (1180, 1430, 180, 430, 80, 300)
    jt(2, [part("Span module sill and joint plate", W("span", *b), C["span"].color),
           part("Drive module sill and joint plate", W("drive", *b), "#0F766E"),
           part("M16 bolts, nuts and washers (4 a side)", W("joint_bolts", *b), C["joint_bolts"].color)],
       "span module to drive module",
       "Two 10 mm plates face to face; four M16 grade 8.8 bolts on each sill. Seen from the back right",
       elev=22, azim=35, size=(8, 6))
    b = (-270, -30, -370, -230, 180, 680)
    jt(3, [part("Sill", W("span", *b), C["span"].color),
           part("Bearing pedestal", W("pedestals", *b), "#6B7280"),
           part("Pillow block UCP206", W("bearings", *b), "#0F766E"),
           part("Pump wheel shaft, 30 mm", W("pump_shaft", *b), C["pump_shaft"].color)],
       "pump shaft bearing on its pedestal",
       "Post welded on the sill; the bearing bolts to the plate on top; grub screws lock it to the shaft",
       elev=18, azim=-55, size=(7, 6))
    b = (-300, 40, -240, -160, 180, 740)
    jt(4, [part("Ratchet, keyed to the shaft", W("ratchet", *b), C["ratchet"].color),
           part("Pawl, post and pin", W("pawl", *b), C["pawl"].color),
           part("Pump wheel shaft", W("pump_shaft", *b), C["pump_shaft"].color),
           part("Crossbar", W("span", *b), C["span"].color)],
       "backstop",
       "Seen from the front with the hood off. The pawl clicks over the teeth when pumping and locks if the wheel runs back",
       elev=6, azim=-90, size=(7, 6))
    b = (680, 1220, 270, 520, 280, 830)
    jt(5, [part("Layshaft, 25 mm", W("layshaft", *b), C["layshaft"].color),
           part("480 mm pulley (from the engine)", win(child("lay_pulleys", 0), *b), "#64748B"),
           part("344 mm pulley (to the blower)", win(child("lay_pulleys", 1), *b), "#0EA5E9"),
           part("90 mm two-groove pulley (to the pump)", win(child("lay_pulleys", 2), *b), "#0F766E"),
           part("Pillow block UCP205", W("bearings", *b), "#1F2937"),
           part("Pedestal", W("pedestals", *b), "#9CA3AF")],
       "layshaft pulleys",
       "Three pulleys on taper bushes, side by side outside the back bearing. Seen from the back right",
       elev=18, azim=40, size=(8, 6))
    b = (380, 900, 300, 560, 600, 1090)
    jt(6, [part("Idler pulley on the arm", W("idler", *b), C["idler"].color),
           part("Clutch lever and arm", W("clutch", *b), C["clutch"].color),
           part("Pivot post", W("idler_post", *b), "#374151"),
           part("Pump belts (slack strand)", W("belts", *b), "#111827")],
       "clutch idler on the pump belts",
       "Lever up: the idler presses the slack strand 25 mm and the pump runs. Lever down: the belts go slack. Guard off",
       elev=12, azim=75, size=(8, 6))
    b = (1900, 2300, -110, 360, 150, 470)
    jt(7, [part("Crossbars", W("drive", *b), C["drive"].color),
           part("Engine plate, slotted", W("eng_plate", *b), "#0F766E"),
           part("Engine base", W("engine", *b), C["engine"].color)],
       "engine on its slotted plate",
       "The plate bolts through four slots into two crossbars; slide it toward the drive end to tension the belt",
       elev=30, azim=-60, size=(8, 6))
    b = (-60, 160, -30, 230, 120, 440)
    jt(8, [part("Crossbars", W("span", *b), C["span"].color),
           part("Pipe head plate and clamp", W("pipe_head", *b), C["pipe_head"].color),
           part("Outlet tee and rope exit stub", W("tee", *b), "#94A3B8"),
           part("Rising main", W("main", *b), "#CBD5E1"),
           part("Rope", W("rope", *b), C["rope"].color),
           part("Support wire eye", W("wire", *b), "#6B7280")],
       "pipe head, cut through the rising main",
       "Cut through the main. The clamp carries it; water leaves by the tee to the front; the rope by the stub above",
       cut="-X", elev=14, azim=20, size=(8, 6))
    b = (-100, 140, -20, 220, -2720, -2290)
    jt(9, [part("Guide block", W("guide", *b), C["guide"].color),
           part("Weights", W("guide_weights", *b), "#9CA3AF"),
           part("HDPE roller on a stainless pin", W("roller", *b), "#E7E5E4"),
           part("Rope", W("rope", *b), C["rope"].color),
           part("Rising main in its socket", W("main", *b), "#CBD5E1")],
       "guide block at the shaft bottom, cut open",
       "The rope comes down, turns round the roller and enters the main. Water comes in through the slots",
       cut="+Y", elev=8, azim=-85, size=(7, 6))
    b = (180, 1470, -140, 140, -160, 470)
    jt(10, [part("Crossbar", W("span", *b), C["span"].color),
            part("Saddle and strap", W("saddle", *b), C["saddle"].color),
            part("Duct head (rigid bend)", W("duct_head", *b), C["duct_head"].color),
            part("Lay-flat duct, clamped on", W("duct", *b), C["duct"].color),
            part("Flexible link to the blower", W("flex", *b), C["flex"].color)],
       "duct head",
       "The bend sits on the saddle and strap; the flexible link and the lay-flat duct go over its stubs with clamps",
       elev=20, azim=-60, size=(8, 6))
    b = (2330, 4150, 0, 260, -10, 640)
    jt(11, [part("Engine muffler outlet", W("engine", *b), C["engine"].color),
            part("Stainless flexible hose", W("exh_hose", *b), "#A8A29E"),
            part("Exhaust pipe", W("exhaust", *b), C["exhaust"].color),
            part("Low stand with U-bolt", W("stands", *b), "#374151")],
       "exhaust hose and pipe",
       "Band clamps at both ends of the hose; the hose takes the engine's shake; the pipe rests on the stands",
       elev=22, azim=-60, size=(9, 5))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    G = groups()
    out = []

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    def st(n, done, new, title, sub, **kw):
        if only is not None and n != only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    gctx = [ground_context()]
    s = lambda k: Part(G[k].name, short(G[k].shape), G[k].color, None, (0, 0, 0))  # noqa: E731
    st(1, [], [mv(G["sleepers"], (0, 0, 300)), mv(G["stakes"], (0, 0, 900))], "sleepers and stakes",
       "Sleepers square to the shaft, their edges at least 0.35 m back from the collar edge; stakes driven through",
       context=gctx, elev=28, azim=-55)
    f1 = [G["sleepers"], G["stakes"]]
    st(2, f1, [mv(G["span"], (0, 0, 500)), mv(G["screws"], (0, 0, 250))], "span module onto the sleepers",
       "Four people lift it over the opening from the sides; never step onto it. Cleats screwed down with M12 coach screws",
       context=gctx, elev=28, azim=-55, label_done=False)
    f2 = f1 + [G["span"], G["screws"]]
    st(3, f2, [mv(G["drive"], (600, 0, 0)), mv(G["bolts"], (250, 0, 0))], "drive module and joint bolts",
       "Butt the joint plates together and fit eight M16 bolts; tighten once both modules sit level",
       context=gctx, elev=28, azim=-55, label_done=False)
    f3 = f2 + [G["drive"], G["bolts"]]
    st(4, f3, [mv(G["pump_set"], (0, 0, 600))], "pump shaft assembly onto its pedestals",
       "Wheel, ratchet and both pillow blocks are slid onto the shaft on the bench first; bolt the blocks down",
       elev=24, azim=-55, label_done=False)
    f4 = f3 + [G["pump_set"]]
    st(5, f4, [mv(G["ring"], (0, 450, 0)), mv(G["pawl"], (0, -450, 0))], "pump pulley and backstop pawl",
       "Pulley on its taper bush at the belt-side end; pawl pinned on its post with the spring hooked on",
       elev=24, azim=-55, label_done=False)
    f5 = f4 + [G["ring"], G["pawl"]]
    st(6, f5, [mv(G["lay_set"], (0, 0, 500))], "layshaft assembly onto its pedestals",
       "Pulleys and pillow blocks on the shaft first; line the pulley grooves up with the engine, blower and pump grooves",
       elev=22, azim=40, label_done=False)
    f6 = f5 + [G["lay_set"]]
    st(7, f6, [mv(G["eng_plate"], (0, 0, 250)), mv(G["engine"], (0, 0, 650)), mv(G["blow_plate"], (0, 0, 250)),
               mv(G["blower"], (0, 0, 650))], "engine and blower on their plates",
       "Plates bolted through their slots, slid fully toward the layshaft; engine and blower bolted to their plates",
       elev=26, azim=-50, label_done=False)
    f7 = f6 + [G["eng_plate"], G["engine"], G["blow_plate"], G["blower"]]
    st(8, f7, [mv(G["belts"], (0, 450, 0)), mv(G["clutch"], (0, 350, 200))], "belts and clutch",
       "Fit the belts; slide the engine and blower plates out until each belt deflects about 16 mm per metre of span under a thumb",
       elev=20, azim=40, label_done=False)
    f8 = f7 + [G["belts"], G["clutch"]]
    st(9, f8, [mv(G["guide"], (0, 0, 1500)), mv(G["main"], (0, 0, 1500)), mv(G["rope"], (0, 0, 1500))],
       "guide block, rising main and rope down the shaft",
       "Rope threaded through the guide block and the main on the ground; lowered length by length on the support wire",
       elev=16, azim=-55, label_done=False, size=(8, 8))
    f8s = f8
    low = [s("main"), s("rope")]
    st(10, f8s + low, [mv(G["pipe_head"], (0, 0, 300)), mv(G["tee"], (0, -350, 250))],
       "pipe head, outlet tee and discharge hose",
       "Clamp the main in the pipe head plate and bolt the plate to the crossbars; splice the rope over the wheel",
       elev=24, azim=-55, label_done=False)
    f10 = f8s + low + [G["pipe_head"], G["tee"]]
    duct_short = Part(G["duct"].name, short(G["duct"].shape), C["duct"].color, None, (0, 0, 900))
    st(11, f10, [mv(G["duct_head"], (0, 0, 400)), duct_short, mv(G["flex"], (0, -400, 0))],
       "duct head, lay-flat duct and flexible link",
       "Duct lowered from its hanging rings first; bend onto the saddle and strapped; link clamped to the blower outlet",
       elev=24, azim=-55, label_done=False)
    f11 = f10 + [G["duct_head"], Part(G["duct"].name, short(G["duct"].shape), C["duct"].color, None, (0, 0, 0)), G["flex"]]
    st(12, f11, [mv(G["lay_cover"], (0, 0, 350)), mv(G["guard"], (0, 600, 150)), mv(G["hood"], (0, 0, 800))],
       "guards and hood",
       "Layshaft cover, belt guard on its brackets with the clutch lever through it, then the hood over the wheel",
       elev=26, azim=40, label_done=False)
    f12 = f11 + [G["lay_cover"], G["guard"], G["hood"]]
    st(13, f12, [mv(G["stands"], (0, -500, 0)), mv(G["exhaust"], (0, 0, 500))], "exhaust extension",
       "Riser downwind of the collar and of the blower intake; stands staked; hose clamped to the muffler outlet",
       elev=30, azim=-60, label_done=False, size=(10, 6))
    return out


if __name__ == "__main__":
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}
    for w in sys.argv[1:] or ["overview", "sheets", "joints", "steps"]:
        name, _, n = w.partition(":")
        r = fns[name](int(n)) if n else fns[name]()
        print(w, "->", r)
