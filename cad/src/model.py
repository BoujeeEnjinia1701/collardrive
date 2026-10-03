"""CollarDrive parametric model (build123d), TRL 3, constructable design (CLD-DDR-002).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL to cad/step and cad/stl
    python cad/src/model.py --check    fit checks: no two components overlap, every joint face touches

Axes: X along the frame, from the pump end (-X) to the drive end (+X), with X = 0 on the shaft centre;
Y across the frame, +Y is the belt side; Z up from the ground (Z = 0). All sizes in mm.

The frame is two bolted modules on three timber sleepers: the span module bridges the collar and carries
the rope pump wheel, the pipe head and the duct head; the drive module carries the engine and the blower.
The rising main, the rope and the duct are drawn shortened: they stop 2.4 m down, where the guide block
is drawn. In a real shaft they reach the water at the bottom.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

P = PARAMS = dict(
    # ground and sleepers
    SLEEPER_X=(-1250.0, 1200.0, 2300.0), SLEEPER=(200.0, 900.0, 100.0), STAKE_Y=400.0, STAKE_R=12.5, STAKE_DEPTH=700.0,
    # sills: RHS 100 x 50 x 3, standing (100 tall), centres at +/- SILL_Y
    SILL_H=100.0, SILL_W=50.0, SILL_T=3.0, SILL_Y=300.0, Z0=100.0,
    SPAN_X0=-1450.0, JOINT_X=1300.0, DRIVE_X1=2450.0, END_T=10.0,
    # crossbars: SHS 50 x 50 x 3 between the sills, tops flush with the sills
    XB=50.0, XB_T=3.0,
    SPAN_XBARS=(-1425.0, -480.0, -20.0, 120.0, 620.0, 1265.0),
    DRIVE_XBARS=(1335.0, 1520.0, 1780.0, 1980.0, 2220.0, 2425.0),
    # rope pump wheel
    WHEEL_X=-150.0, WHEEL_Z=600.0, WHEEL_Y=100.0, ROPE_PR=200.0, WHEEL_R=235.0, PUMP_SHAFT_R=15.0,
    PUMP_SHAFT_Y=(-360.0, 470.0),
    # layshaft
    LAY_X=950.0, LAY_Z=550.0, LAY_R=12.5, LAY_Y=(-330.0, 465.0),
    # belt planes (Y) and pulley pitch diameters
    Y_BLOW=360.0, Y_ST1=390.0, Y_ST2=450.0,
    D_ENG=80.0, D_LAY_BIG=480.0, D_LAY_BLOW=344.0, D_LAY_SMALL=90.0, D_BLOWER=80.0, D_RING=560.0, GROOVES_ST2=2, GROOVE_PITCH=15.0,
    # engine (4.8 kW class, 19.05 mm shaft) and blower
    ENG_X=2100.0, ENG_SHAFT_H=150.0, PLATE_T=8.0,
    BLOW_X=1650.0, BLOW_Z=440.0, BLOW_R=200.0, DUCT_R=100.0, DUCT_Z=320.0,
    # pipe, rope, duct drop, guide block (drawn 2.4 m down)
    PIPE_OD=40.0, PIPE_ID=36.2, DUCT_DROP_X=330.0, BEND_R=200.0, DRAWN_DEPTH=2400.0,
    PISTON_D=35.0, PISTON_T=10.0, PISTON_PITCH=1000.0, ROPE_R=3.0,
    # exhaust: 1-1/2 in pipe (48.3 OD) to a riser downwind
    EXH_Y=125.0, EXH_Z=520.0, EXH_X1=7800.0, EXH_TOP=2400.0, EXH_OD=48.3, EXH_ID=40.8,
    STAND_X=(4000.0, 6000.0),
    # guards
    GUARD=(-470.0, 2200.0, 338.0, 490.0, 278.0, 920.0), HOOD=(-440.0, 160.0, -260.0, 260.0, 203.0, 860.0), SHEET=2.0,
    # clutch idler
    IDLER_X=450.0, IDLER_R=30.0, PIVOT=(700.0, 820.0),
)


def _b():
    import build123d as bd
    return bd


# --------------------------------------------------------------------------- primitives
def box(x0, x1, y0, y1, z0, z1):
    bd = _b()
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def cyl_z(r, z0, z1, x=0.0, y=0.0):
    bd = _b()
    return bd.Pos(x, y, (z0 + z1) / 2) * bd.Cylinder(r, z1 - z0)


def cyl_y(r, y0, y1, x, z):
    bd = _b()
    return bd.Pos(x, (y0 + y1) / 2, z) * bd.Rot(90, 0, 0) * bd.Cylinder(r, y1 - y0)


def cyl_x(r, x0, x1, y, z):
    bd = _b()
    return bd.Pos((x0 + x1) / 2, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(r, x1 - x0)


def tube_y(r0, r1, y0, y1, x, z):
    return cyl_y(r1, y0, y1, x, z) - cyl_y(r0, y0 - 1, y1 + 1, x, z)


def tube_x(r0, r1, x0, x1, y, z):
    return cyl_x(r1, x0, x1, y, z) - cyl_x(r0, x0 - 1, x1 + 1, y, z)


def tube_z(r0, r1, z0, z1, x, y):
    return cyl_z(r1, z0, z1, x, y) - cyl_z(r0, z0 - 1, z1 + 1, x, y)


def cyl_between(p0, p1, r):
    bd = _b()
    v = [p1[i] - p0[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    return bd.Solid.make_cylinder(r, L, bd.Plane(origin=tuple(p0), z_dir=tuple(c / L for c in v)))


def revolve_y(profile, x, z):
    """Revolve a (radius, y) profile about an axis along Y through (x, z). Profile y values are global Y."""
    bd = _b()
    pts = [(r, 0.0, a) for r, a in profile]
    face = bd.make_face(bd.Polyline(*pts, close=True))
    solid = bd.revolve(face, axis=bd.Axis.Z)
    return bd.Pos(x, 0, z) * bd.Rot(-90, 0, 0) * solid


def rhs_x(x0, x1, yc, z0, w, h, t):
    """Rectangular hollow section along X: w across (Y), h tall (Z)."""
    return box(x0, x1, yc - w / 2, yc + w / 2, z0, z0 + h) - box(x0 - 1, x1 + 1, yc - w / 2 + t, yc + w / 2 - t, z0 + t, z0 + h - t)


def shs_y(xc, y0, y1, z0, a, t):
    return box(xc - a / 2, xc + a / 2, y0, y1, z0, z0 + a) - box(xc - a / 2 + t, xc + a / 2 - t, y0 - 1, y1 + 1, z0 + t, z0 + a - t)


def shs_z(xc, yc, z0, z1, a, t):
    return box(xc - a / 2, xc + a / 2, yc - a / 2, yc + a / 2, z0, z1) - box(xc - a / 2 + t, xc + a / 2 - t, yc - a / 2 + t, yc + a / 2 - t, z0 - 1, z1 + 1)


def comp(*shapes):
    bd = _b()
    return bd.Compound(children=[s for s in shapes if s is not None])


def union(*shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


# --------------------------------------------------------------------------- derived geometry
def tangents(c1, r1, c2, r2):
    """External tangent points of an open belt between circles c1 (x, z), r1 and c2, r2.
    Returns [(p1, p2) upper, (p1, p2) lower]."""
    (x1, z1), (x2, z2) = c1, c2
    dx, dz = x2 - x1, z2 - z1
    d = math.hypot(dx, dz)
    base = math.atan2(dz, dx)
    a = math.acos((r1 - r2) / d)
    out = []
    for s in (1, -1):
        th = base + s * a
        n = (math.cos(th), math.sin(th))
        out.append(((x1 + r1 * n[0], z1 + r1 * n[1]), (x2 + r2 * n[0], z2 + r2 * n[1])))
    out.sort(key=lambda pq: -(pq[0][1] + pq[1][1]))
    return out


def belt_length(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    return 2 * math.sqrt(d * d - (r1 - r2) ** 2) + math.pi * (r1 + r2) + 2 * (r1 - r2) * math.asin((r1 - r2) / d)


def levels(P=PARAMS):
    z_top = P["Z0"] + P["SILL_H"]
    eng_shaft = z_top + P["PLATE_T"] + P["ENG_SHAFT_H"]
    L = dict(z_top=z_top, plate_top=z_top + P["PLATE_T"], eng_shaft=eng_shaft)
    L["ped_pump_top"] = P["WHEEL_Z"] - 42.9          # UCP206 centre height 42.9 mm
    L["ped_lay_top"] = P["LAY_Z"] - 36.5             # UCP205 centre height 36.5 mm
    L["ring_r"] = P["D_RING"] / 2
    L["rope_up_x"] = P["WHEEL_X"] + P["ROPE_PR"]
    L["rope_down_x"] = P["WHEEL_X"] - P["ROPE_PR"]
    L["bottom"] = -P["DRAWN_DEPTH"]
    return L


def belts(P=PARAMS):
    L = levels(P)
    W = (P["WHEEL_X"], P["WHEEL_Z"]); LS = (P["LAY_X"], P["LAY_Z"])
    E = (P["ENG_X"], L["eng_shaft"]); B = (P["BLOW_X"], P["BLOW_Z"])
    return {
        "st2": (P["Y_ST2"], W, P["D_RING"] / 2, LS, P["D_LAY_SMALL"] / 2),
        "st1": (P["Y_ST1"], LS, P["D_LAY_BIG"] / 2, E, P["D_ENG"] / 2),
        "blow": (P["Y_BLOW"], LS, P["D_LAY_BLOW"] / 2, B, P["D_BLOWER"] / 2),
    }


def idler_centre(P=PARAMS):
    """The idler rides on the back of the slack (upper) strand of the pump belt, pressing it down 25 mm."""
    y, c1, r1, c2, r2 = belts(P)["st2"]
    (p, q), _ = tangents(c1, r1, c2, r2)
    t = (P["IDLER_X"] - p[0]) / (q[0] - p[0])
    z = p[1] + t * (q[1] - p[1])
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    nx, nz = -math.sin(ang), math.cos(ang)
    off = 5.0 + P["IDLER_R"]
    return P["IDLER_X"] + nx * off, z + nz * off


# --------------------------------------------------------------------------- component builders
def pulley(pd, yc, x, z, bore, big=False, width=20.0, grooves=1, pitch=15.0):
    if grooves > 1:
        return pulley_multi(pd, yc, x, z, bore, grooves, pitch)
    od = pd + 6.6
    ro = od / 2
    g = 11.0
    if not big:
        prof = [(bore, yc - 15), (ro - g - 4, yc - 15), (ro - g - 4, yc - width / 2), (ro, yc - width / 2), (ro, yc - width / 2 + 2),
                (ro - g, yc - 2.5), (ro - g, yc + 2.5), (ro, yc + width / 2 - 2), (ro, yc + width / 2),
                (ro - g - 4, yc + width / 2), (ro - g - 4, yc + 15), (bore, yc + 15)]
    else:
        prof = [(bore, yc - 15), (bore + 22, yc - 15), (bore + 22, yc - 5), (ro - g - 10, yc - 5), (ro - g - 10, yc - width / 2),
                (ro, yc - width / 2), (ro, yc - width / 2 + 2), (ro - g, yc - 2.5), (ro - g, yc + 2.5), (ro, yc + width / 2 - 2),
                (ro, yc + width / 2), (ro - g - 10, yc + width / 2), (ro - g - 10, yc + 5), (bore + 22, yc + 5),
                (bore + 22, yc + 15), (bore, yc + 15)]
    return revolve_y(prof, x, z)


def pulley_multi(pd, yc, x, z, bore, n, pitch):
    """Cast multi-groove A-section pulley: web and hub for large sizes, solid for small."""
    ro = (pd + 6.6) / 2; g = 11.0
    w = pitch * n + 5.0
    y0 = yc - w / 2
    prof = [(bore, yc - 20), (bore + 25 if pd > 200 else ro - g - 4, yc - 20)]
    if pd > 200:
        prof += [(bore + 25, yc - 6), (ro - g - 10, yc - 6), (ro - g - 10, y0)]
    else:
        prof += [(ro - g - 4, y0)]
    prof += [(ro, y0)]
    for k in range(n):
        c = y0 + 2.5 + pitch * (k + 0.5)
        prof += [(ro, c - 6.5), (ro - g, c - 2.5), (ro - g, c + 2.5), (ro, c + 6.5)]
    prof += [(ro, y0 + w)]
    if pd > 200:
        prof += [(ro - g - 10, y0 + w), (ro - g - 10, yc + 6), (bore + 25, yc + 6), (bore + 25, yc + 20)]
    else:
        prof += [(ro - g - 4, y0 + w), (ro - g - 4, yc + 20)]
    prof += [(bore, yc + 20)]
    return revolve_y(prof, x, z)


def belt_strands(key, P=PARAMS):
    y, c1, r1, c2, r2 = belts(P)[key]
    ys = [y - P["GROOVE_PITCH"] / 2, y + P["GROOVE_PITCH"] / 2] if key == "st2" else [y]
    out = []
    for yy in ys:
        for p, q in tangents(c1, r1, c2, r2):
            out.append(cyl_between((p[0], yy, p[1]), (q[0], yy, q[1]), 5.0))
    return comp(*out)


def hood(P=PARAMS):
    x0, x1, y0, y1, z0, z1 = P["HOOD"]; t = P["SHEET"]
    L = levels(P)
    walls = [box(x0, x1, y0, y1, z1 - t, z1), box(x0, x0 + t, y0, y1, z0, z1 - t), box(x1 - t, x1, y0, y1, z0, z1 - t),
             box(x0 + t, x1 - t, y0, y0 + t, z0, z1 - t), box(x0 + t, x1 - t, y1 - t, y1, z0, z1 - t)]
    h = union(*walls)
    h = h - cyl_y(P["PUMP_SHAFT_R"] + 5, y0 - 5, y1 + 5, P["WHEEL_X"], P["WHEEL_Z"])
    h = h - cyl_y(24.0, y0 - 5, y0 + 5, L["rope_up_x"], 300.0)       # spout hole
    tabs = [box(x0 - 30, x0, -230, -170, 200, 203), box(x0 - 30, x0, 170, 230, 200, 203),
            box(100, x1, -230, -170, 200, 203), box(100, x1, 205, 245, 200, 203)]
    tabs_up = [box(x0 - 30, x0, -230, -170, 200, 240) - box(x0 - 30 - 1, x0 - t, -231, -169, 203, 241),
               box(x0 - 30, x0, 170, 230, 200, 240) - box(x0 - 30 - 1, x0 - t, 169, 231, 203, 241)]
    return union(h, *tabs[2:], *tabs_up)


def guard(P=PARAMS):
    x0, x1, y0, y1, z0, z1 = P["GUARD"]; t = P["SHEET"]
    walls = union(box(x0, x1, y0, y1, z1 - t, z1), box(x0, x1, y0, y1, z0, z0 + t),
                  box(x0, x0 + t, y0, y1, z0 + t, z1 - t), box(x1 - t, x1, y0, y1, z0 + t, z1 - t),
                  box(x0 + t, x1 - t, y0, y0 + t, z0 + t, z1 - t), box(x0 + t, x1 - t, y1 - t, y1, z0 + t, z1 - t))
    L = levels(P)
    for x, z, r in ((P["WHEEL_X"], P["WHEEL_Z"], P["PUMP_SHAFT_R"] + 5), (P["LAY_X"], P["LAY_Z"], P["LAY_R"] + 5),
                    (P["ENG_X"], L["eng_shaft"], 15.0), (P["BLOW_X"], P["BLOW_Z"], 17.0), (P["PIVOT"][0], P["PIVOT"][1], 10.0)):
        walls = walls - cyl_y(r, y0 - 5, y1 + 5, x, z) if (x, z) == P["PIVOT"] else walls - cyl_y(r, y0 - 5, y0 + 5, x, z)
    latch = box(760, 840, y1, y1 + 5, 880, 990) - box(790, 810, y1 - 1, y1 + 6, 940, 991)
    brackets = [union(box(x, x + 40, 325, 330, 120, 278), box(x, x + 40, 325, y0 + 40, 272, 278)) for x in (-320.0, 480.0, 1400.0)]
    return union(walls, latch), comp(*brackets)


# --------------------------------------------------------------------------- components
class C:
    """One component: key, plain name, shape, colour, BOM line, how it is made, and exploded offset."""
    def __init__(self, key, name, shape, color, bom, how, explode=(0, 0, 0), density=7850.0):
        self.key, self.name, self.shape, self.color = key, name, shape, color
        self.bom, self.how, self.explode, self.density = bom, how, explode, density


def components(P=PARAMS):
    bd = _b()
    L = levels(P)
    out = []
    add = lambda *a, **k: out.append(C(*a, **k))  # noqa: E731
    z0, zt = P["Z0"], L["z_top"]
    sy, sw, sh, st = P["SILL_Y"], P["SILL_W"], P["SILL_H"], P["SILL_T"]
    yin = sy - sw / 2                                   # inner face of a sill
    jx, et = P["JOINT_X"], P["END_T"]

    # 1 sleepers, stakes, cleats and coach screws
    sl = []; stakes = []; cleats = []; screws = []
    for i, x in enumerate(P["SLEEPER_X"]):
        a, b_, c = P["SLEEPER"]
        s_ = box(x - a / 2, x + a / 2, -b_ / 2, b_ / 2, 0, c)
        for yy in (-P["STAKE_Y"], P["STAKE_Y"]):
            s_ = s_ - cyl_z(P["STAKE_R"] + 1.5, -1, c + 1, x, yy)
            stakes.append(union(cyl_z(P["STAKE_R"], -P["STAKE_DEPTH"], c + 30, x, yy), cyl_z(25, c, c + 6, x, yy) - cyl_z(P["STAKE_R"], c - 1, c + 7, x, yy)))
        sl.append(s_)
        if i < 2:                                        # cleats on the span module (pump end and joint sleepers)
            for sgn in (-1, 1):
                yo = sgn * (sy + sw / 2)
                ya, yb = sorted((yo, yo + sgn * 50))
                yc0, yc1 = sorted((yo, yo + sgn * 5))
                ya, yb = sorted((yo, yo + sgn * 40))
                cl = union(box(x - 50, x + 50, yc0, yc1, z0, z0 + 50), box(x - 50, x + 50, ya, yb, z0, z0 + 5))
                cleats.append(cl - cyl_z(7, z0 - 1, z0 + 6, x - 25, yo + sgn * 30) - cyl_z(7, z0 - 1, z0 + 6, x + 25, yo + sgn * 30))
                for dx in (-25, 25):
                    screws.append(union(cyl_z(6, 10, z0 + 5, x + dx, yo + sgn * 30), cyl_z(10, z0 + 5, z0 + 13, x + dx, yo + sgn * 30)))
    add("sleepers", "Timber sleepers (3)", comp(*sl), "#8B6B4A", 1, "buy", (0, 0, -350), density=700.0)
    add("stakes", "Steel stakes (6)", comp(*stakes), "#6B7280", 1, "make", (0, 0, -900))
    add("cleats", "Hold-down cleats (4)", comp(*cleats), "#374151", 2, "make", (0, 0, 0))
    add("screws", "Coach screws (8)", comp(*screws), "#111827", 1, "buy", (0, 0, 250))

    # 2 span module: sills, crossbars, end plates, pedestals
    def module(x0, x1, xbars, end_at_x0, end_at_x1):
        parts = []
        for sgn in (-1, 1):
            parts.append(rhs_x(x0, x1, sgn * sy, z0, sw, sh, st))
        for xc in xbars:
            parts.append(shs_y(xc, -yin, yin, zt - P["XB"], P["XB"], P["XB_T"]))
        for at, joint in ((x0, end_at_x0), (x1, end_at_x1)):
            for sgn in (-1, 1):
                if joint:
                    xa, xb = (at - et, at) if at == x1 else (at, at + et)
                    pl = box(xa, xb, sgn * sy - 75, sgn * sy + 75, z0, z0 + 170)
                    for yy in (sgn * sy - 50, sgn * sy + 50):
                        for zz in (z0 + 25, z0 + 145):
                            pl = pl - cyl_x(9, xa - 1, xb + 1, yy, zz)
                    parts.append(pl)
                else:
                    xa, xb = (at - 3, at) if at == x1 else (at, at + 3)
                    parts.append(box(xa, xb, sgn * sy - sw / 2, sgn * sy + sw / 2, z0, z0 + sh))
        return parts

    span = module(P["SPAN_X0"], jx, P["SPAN_XBARS"], False, True)
    add("span", "Span module", comp(*span), "#4B5563", 2, "make", (0, 0, 0))

    peds = []
    for xc, top, plate_x in ((P["WHEEL_X"], L["ped_pump_top"], 90.0), (P["LAY_X"], L["ped_lay_top"], 80.0)):
        for sgn in (-1, 1):
            peds.append(union(shs_z(xc, sgn * sy, zt, top - 10, 60, 4), box(xc - plate_x, xc + plate_x, sgn * sy - 30, sgn * sy + 30, top - 10, top)))
    add("pedestals", "Bearing pedestals (4)", comp(*peds), "#6B7280", 2, "make", (0, 0, 380))

    drive = module(jx, P["DRIVE_X1"], P["DRIVE_XBARS"], True, False)
    add("drive", "Drive module", comp(*drive), "#374151", 3, "make", (650, 0, 0))

    bolts = []
    for sgn in (-1, 1):
        for yy in (sgn * sy - 50, sgn * sy + 50):
            for zz in (z0 + 25, z0 + 145):
                bolts.append(union(cyl_x(8, jx - et - 10, jx + et + 14, yy, zz), cyl_x(12, jx - et - 10, jx - et, yy, zz),
                                   cyl_x(12, jx + et, jx + et + 13, yy, zz)))
    add("joint_bolts", "Module joint bolts (8 x M16)", comp(*bolts), "#111827", 4, "buy", (300, 0, 0))

    # 5 pillow blocks
    pbs = []
    for xc, top, r_h, bore, base_l in ((P["WHEEL_X"], L["ped_pump_top"], 42.0, P["PUMP_SHAFT_R"], 165.0),
                                       (P["LAY_X"], L["ped_lay_top"], 36.0, P["LAY_R"], 130.0)):
        zc = top + (42.9 if bore == P["PUMP_SHAFT_R"] else 36.5)
        for sgn in (-1, 1):
            yc = sgn * sy
            pb = union(box(xc - base_l / 2, xc + base_l / 2, yc - 19, yc + 19, top, top + 16),
                       box(xc - 30, xc + 30, yc - 19, yc + 19, top + 10, zc),
                       cyl_y(r_h, yc - 20, yc + 20, xc, zc)) - cyl_y(bore, yc - 25, yc + 25, xc, zc)
            pbs.append(pb)
    add("bearings", "Pillow block bearings (4)", comp(*pbs), "#1F2937", 5, "buy", (0, 0, 600))

    # 6 shafts
    add("pump_shaft", "Pump wheel shaft, 30 mm", cyl_y(P["PUMP_SHAFT_R"], *P["PUMP_SHAFT_Y"], P["WHEEL_X"], P["WHEEL_Z"]),
        "#9CA3AF", 6, "make", (0, -700, 300))
    add("layshaft", "Layshaft, 25 mm", cyl_y(P["LAY_R"], *P["LAY_Y"], P["LAY_X"], P["LAY_Z"]), "#9CA3AF", 6, "make", (0, -700, 400))

    # 7 pump wheel: hub, web, tyre sidewall V groove
    wy = P["WHEEL_Y"]; R = P["WHEEL_R"]; br = P["PUMP_SHAFT_R"]
    wheel = revolve_y([(br, wy - 40), (35, wy - 40), (35, wy - 3), (185, wy - 3), (185, wy - 45), (R, wy - 45), (R, wy - 42),
                       (197, wy - 2), (197, wy + 2), (R, wy + 42), (R, wy + 45), (185, wy + 45), (185, wy + 3), (35, wy + 3),
                       (35, wy + 40), (br, wy + 40)], P["WHEEL_X"], P["WHEEL_Z"])
    add("wheel", "Rope pump wheel", wheel, "#1F2937", 7, "make", (0, 0, 900), density=2600.0)

    # 8 pump pulley: 560 mm two-groove A-section cast pulley on a taper bush
    add("ring", "Pump pulley, 560 mm two-groove", pulley(P["D_RING"], P["Y_ST2"], P["WHEEL_X"], P["WHEEL_Z"], br, grooves=2),
        "#0F766E", 8, "buy", (0, 600, 900))

    # 9 backstop: ratchet on the shaft, pawl on a post from the crossbar
    rat_y = -200.0
    rat = cyl_y(110, rat_y - 5, rat_y + 5, P["WHEEL_X"], P["WHEEL_Z"])
    for k in range(12):
        a = 30 * k
        tooth = bd.Pos(P["WHEEL_X"], rat_y, P["WHEEL_Z"]) * bd.Rot(0, -a, 0) * box(96, 112, -7, 7, -6, 6)
        rat = rat - tooth
    rat = rat - cyl_y(br, rat_y - 10, rat_y + 10, P["WHEEL_X"], P["WHEEL_Z"])
    rat = union(rat, tube_y(br, 30, rat_y + 5, rat_y + 25, P["WHEEL_X"], P["WHEEL_Z"]))
    post_x, post_top = -20.0, 480.0
    post = box(post_x - 20, post_x + 20, rat_y - 10, rat_y + 10, zt, post_top + 15)
    ca, sa = math.cos(math.radians(-60)), math.sin(math.radians(-60))
    tip = (P["WHEEL_X"] + 118 * ca, P["WHEEL_Z"] + 118 * sa)
    nose = bd.Pos(P["WHEEL_X"], rat_y, P["WHEEL_Z"]) * bd.Rot(0, 60, 0) * box(100, 120, -5, 5, -5, 5)
    pawl = union(cyl_y(10, rat_y - 5, rat_y + 5, post_x, post_top), cyl_between((post_x, rat_y, post_top), (tip[0], rat_y, tip[1]), 6.0), nose)
    pin = cyl_y(5, rat_y - 15, rat_y + 15, post_x, post_top)
    add("ratchet", "Backstop ratchet", rat, "#B45309", 9, "make", (0, -500, 300))
    add("pawl", "Backstop pawl and post", union(post - cyl_y(5, rat_y - 11, rat_y + 11, post_x, post_top), pawl - cyl_y(5, rat_y - 6, rat_y + 6, post_x, post_top), pin),
        "#DC2626", 9, "make", (0, -500, 0))

    # 10 pulleys
    pls = [pulley(P["D_LAY_BIG"], P["Y_ST1"], P["LAY_X"], P["LAY_Z"], P["LAY_R"], big=True),
           pulley(P["D_LAY_BLOW"], P["Y_BLOW"], P["LAY_X"], P["LAY_Z"], P["LAY_R"], big=True),
           pulley(P["D_LAY_SMALL"], P["Y_ST2"], P["LAY_X"], P["LAY_Z"], P["LAY_R"], grooves=2)]
    add("lay_pulleys", "Layshaft pulleys (480, 344, 90 mm)", comp(*pls), "#64748B", 10, "buy", (0, 500, 0))
    add("eng_pulley", "Engine pulley, 80 mm", pulley(P["D_ENG"], P["Y_ST1"], P["ENG_X"], L["eng_shaft"], 9.525), "#64748B", 10, "buy", (0, 400, 0))
    add("blow_pulley", "Blower pulley, 80 mm", pulley(P["D_BLOWER"], P["Y_BLOW"], P["BLOW_X"], P["BLOW_Z"], 12.5), "#64748B", 10, "buy", (0, 400, 0))

    # 11 belts
    add("belts", "V-belts (3, A section)", comp(belt_strands("st2", P), belt_strands("st1", P), belt_strands("blow", P)),
        "#111827", 11, "buy", (0, 800, 0), density=1200.0)

    # 12 clutch idler
    ix, iz = idler_centre(P)
    px, pz = P["PIVOT"]
    idl = tube_y(8, P["IDLER_R"], P["Y_ST2"] - 18, P["Y_ST2"] + 18, ix, iz)
    add("idler", "Idler pulley", idl, "#64748B", 12, "buy", (0, 300, 250))
    lever = union(cyl_y(8, 335, 530, px, pz),
                  cyl_between((px, 418, pz), (ix, 418, iz), 8.0), cyl_y(8, 410, P["Y_ST2"] + 22, ix, iz),
                  cyl_between((px, 520, pz), (px + 100, 520, pz + 230), 9.0), cyl_y(16, 505, 540, px + 100, pz + 230))
    idpost = box(px - 20, px + 20, sy + sw / 2, sy + sw / 2 + 10, 120, pz + 25) - cyl_y(8, sy + sw / 2 - 1, sy + sw / 2 + 11, px, pz)
    add("clutch", "Clutch lever, arm and pivot", lever, "#C2410C", 12, "make", (0, 300, 250))
    add("idler_post", "Idler pivot post", idpost - cyl_y(7, sy + sw / 2 - 1, sy + sw / 2 + 11, px, 160), "#374151", 12, "make", (0, 300, 0))

    # 13 engine plate and engine
    ex = P["ENG_X"]; pt = L["plate_top"]
    eplate = box(ex - 170, ex + 170, -80, 320, zt, pt)
    for xx in (P["DRIVE_XBARS"][3], P["DRIVE_XBARS"][4]):
        for yy in (-40, 280):
            eplate = eplate - box(xx - 30, xx + 30, yy - 7, yy + 7, zt - 1, pt + 1)
    add("eng_plate", "Engine plate (slotted)", eplate, "#4B5563", 13, "make", (0, 0, 250))
    es = L["eng_shaft"]
    engine = union(box(ex - 170, ex + 170, -50, 300, pt, pt + 30),                 # base and sump
                   box(ex - 150, ex + 150, -40, 290, pt + 30, pt + 230),            # crankcase
                   box(ex - 160, ex - 20, -30, 200, pt + 230, pt + 400),            # cylinder and head
                   box(ex - 10, ex + 160, -40, 260, pt + 240, pt + 410),            # fuel tank
                   cyl_y(115, -80, -40, ex, es + 60),                               # recoil starter
                   cyl_y(9.525, 290, 400, ex, es),                                  # crankshaft
                   box(ex + 150, ex + 260, 10, 240, pt + 230, pt + 390))            # muffler
    engine = union(engine, cyl_x(P["EXH_OD"] / 2, ex + 255, ex + 300, P["EXH_Y"], P["EXH_Z"]))
    add("engine", "Engine, 4.8 kW petrol", engine, "#B91C1C", 13, "buy", (0, 0, 700))

    # 14 blower and its plate
    bx, bz, brr = P["BLOW_X"], P["BLOW_Z"], P["BLOW_R"]
    bplate = box(bx - 190, bx + 190, -110, 330, zt, pt)
    for xx in (P["DRIVE_XBARS"][1], P["DRIVE_XBARS"][2]):
        for yy in (-60, 280):
            bplate = bplate - box(xx - 30, xx + 30, yy - 7, yy + 7, zt - 1, pt + 1)
    add("blow_plate", "Blower plate (slotted)", bplate, "#4B5563", 14, "make", (0, 0, 250))
    dz = P["DUCT_Z"]; dr = P["DUCT_R"]
    blower = union(cyl_y(brr, -110, 110, bx, bz),
                   cyl_x(dr, bx - 250, bx - 70, 0, dz),
                   box(bx - 150, bx + 150, -90, 90, pt, bz - brr + 20),
                   tube_y(dr, dr + 8, -140, -110, bx, bz),
                   box(bx - 50, bx + 50, 120, 320, pt, bz + 40),
                   cyl_y(12.5, 110, P["Y_BLOW"] + 10, bx, bz))
    blower = (blower - cyl_x(dr - 3, bx - 251, bx - 120, 0, dz)).clean()
    add("blower", "Centrifugal blower", blower, "#0EA5E9", 14, "buy", (0, 0, 750))
    add("inlet_guard", "Blower inlet guard", cyl_y(dr + 8, -144, -140, bx, bz), "#CA8A04", 14, "make", (0, -350, 0))

    # 15 layshaft cover
    lx = P["LAY_X"]
    lz = P["LAY_Z"]
    cover = box(lx - 45, lx + 45, -270, 270, lz - 55, lz + 60) - box(lx - 43, lx + 43, -271, 271, lz - 56, lz + 58)
    add("lay_cover", "Layshaft cover", cover, "#CA8A04", 15, "make", (0, 0, 400))

    # 16 belt guard, 17 hood
    g, gb = guard(P)
    add("guard", "Belt guard", g, "#EAB308", 16, "make", (0, 900, 200))
    add("guard_brackets", "Guard brackets (3)", gb, "#374151", 16, "make", (0, 500, 0))
    add("hood", "Pump wheel hood", hood(P), "#EAB308", 17, "make", (0, 0, 1300))

    # 18 pipe head: plate, clamp, tee, rope exit stub, spout
    ux = L["rope_up_x"]; uy = P["WHEEL_Y"]; ro = P["PIPE_OD"] / 2; ri = P["PIPE_ID"] / 2
    hplate = box(-45, 145, 0, 200, zt, zt + 8) - cyl_z(21, zt - 1, zt + 9, ux, uy)
    clamp = tube_z(ro, 35, zt + 8, zt + 38, ux, uy)
    tee = union(tube_z(ro, 24, 255, 345, ux, uy), tube_y(ro, 24, uy - 70, uy - 20, ux, 300))
    tee = tee - cyl_z(ro, 254, 346, ux, uy) - cyl_y(ro, uy - 71, uy, ux, 300)
    stub = tube_z(ri, ro, 320, 420, ux, uy)
    spout = tube_y(ri, ro, -460, uy - 45, ux, 300)
    add("pipe_head", "Pipe head plate and clamp", comp(hplate, clamp), "#0F766E", 18, "make", (0, 0, 650))
    add("tee", "Outlet tee, spout and rope exit", comp(tee, stub, spout), "#E5E7EB", 18, "buy", (0, -300, 650), density=1400.0)

    # 19 rising main (drawn shortened)
    bot = L["bottom"]
    add("main", "Rising main, 40 mm PVC (drawn shortened)", tube_z(ri, ro, bot, 290, ux, uy), "#E5E7EB", 19, "buy", (0, 0, -300), density=1400.0)

    # 20 guide block
    gx0, gx1, gy0, gy1 = -80.0, 120.0, 40.0, 160.0
    gz0, gz1 = bot - 300, bot
    shell = box(gx0, gx1, gy0, gy1, gz0, gz1) - box(gx0 + 6, gx1 - 6, gy0 + 6, gy1 - 6, gz0 + 6, gz1 - 6)
    shell = shell - cyl_z(ro, gz1 - 7, gz1 + 1, ux, uy) - cyl_z(10, gz1 - 7, gz1 + 1, ux - 80, uy)
    rcx, rcz = ux - 40, gz0 + 80
    shell = shell - cyl_y(6, gy0 - 1, gy1 + 1, rcx, rcz)
    for k in range(4):
        shell = shell - box(gx0 + 30 + 40 * k, gx0 + 50 + 40 * k, gy0 - 1, gy1 + 1, gz0 + 160, gz0 + 260)
    sock = tube_z(ro, ro + 6, gz1, gz1 + 60, ux, uy)
    weights = [box(-60, 100, gy0 - 25, gy0, gz0 + 10, gz0 + 240), box(-60, 100, gy1, gy1 + 25, gz0 + 10, gz0 + 240)]
    add("guide", "Guide block", comp(shell, sock), "#374151", 20, "make", (0, 0, -400))
    add("guide_weights", "Guide block weights (2)", comp(*weights), "#6B7280", 20, "make", (0, 0, -600))
    add("roller", "Guide roller and pin", union(tube_y(6, 37, uy - 30, uy + 30, rcx, rcz), cyl_y(6, gy0, gy1, rcx, rcz)), "#F5F5F4", 20, "make",
        (0, 300, -400), density=960.0)

    # 21 rope and pistons
    rr = P["ROPE_R"]
    dx_ = L["rope_down_x"]
    top_pt = (dx_, uy, P["WHEEL_Z"]); low_pt = (ux - 80, uy, gz1 + 5)
    rope = [cyl_z(rr, rcz, P["WHEEL_Z"], ux, uy), cyl_z(rr, rcz, gz1 + 5, ux - 80, uy), cyl_between(low_pt, top_pt, rr)]
    tor = bd.Pos(P["WHEEL_X"], uy, P["WHEEL_Z"]) * bd.Rot(90, 0, 0) * bd.Torus(P["ROPE_PR"], rr)
    rope.append(tor & box(P["WHEEL_X"] - 300, P["WHEEL_X"] + 300, uy - 10, uy + 10, P["WHEEL_Z"], P["WHEEL_Z"] + 300))
    tor2 = bd.Pos(rcx, uy, rcz) * bd.Rot(90, 0, 0) * bd.Torus(40, rr)
    rope.append(tor2 & box(rcx - 60, rcx + 60, uy - 10, uy + 10, rcz - 60, rcz))
    pist = []
    for zz in (-2000.0, -1000.0, 0.0):
        pist.append(tube_z(rr, P["PISTON_D"] / 2, zz - 5, zz + 5, ux, uy))
    for t in (0.2, 0.55):
        c_ = [low_pt[i] + t * (top_pt[i] - low_pt[i]) for i in range(3)]
        v = [top_pt[i] - low_pt[i] for i in range(3)]
        n = math.sqrt(sum(a * a for a in v)); v = [a / n for a in v]
        pl = bd.Solid.make_cylinder(P["PISTON_D"] / 2, 10, bd.Plane(origin=tuple(c_[i] - 5 * v[i] for i in range(3)), z_dir=tuple(v)))
        pist.append(pl - cyl_between([c_[i] - 6 * v[i] for i in range(3)], [c_[i] + 6 * v[i] for i in range(3)], rr))
    add("rope", "Rope, 6 mm (drawn shortened)", union(*rope), "#F59E0B", 21, "buy", (0, 0, 0), density=910.0)
    add("pistons", "Pistons on the rope", comp(*pist), "#2563EB", 21, "make", (0, 0, 0), density=960.0)

    # 22 support wire
    add("wire", "Support wire, 6 mm", cyl_z(3.0, gz1, zt, ux, 45.0), "#9CA3AF", 22, "buy", (0, 0, -300))

    # 23 duct head: rigid bend and stubs, saddle and strap; 24 lay-flat duct; 25 flexible link
    ddx = P["DUCT_DROP_X"]; br_ = P["BEND_R"]
    bend_c = (ddx + br_, dz - br_)
    tor3 = bd.Pos(bend_c[0], 0, bend_c[1]) * bd.Rot(90, 0, 0) * bd.Torus(br_, dr)
    tor3i = bd.Pos(bend_c[0], 0, bend_c[1]) * bd.Rot(90, 0, 0) * bd.Torus(br_, dr - 3)
    q = box(bend_c[0] - br_ - dr - 5, bend_c[0], -dr - 5, dr + 5, bend_c[1], bend_c[1] + br_ + dr + 5)
    bend = (tor3 & q) - (tor3i & q)
    hstub = tube_x(dr - 3, dr, bend_c[0], 820, 0, dz)
    vstub = tube_z(dr - 3, dr, -100, bend_c[1], ddx, 0)
    add("duct_head", "Duct head (rigid bend)", union(bend, hstub, vstub), "#94A3B8", 23, "buy", (0, 0, 500), density=7850.0)
    xb = P["SPAN_XBARS"][4]
    saddle = box(xb - 25, xb + 25, -70, 70, zt, dz - dr + 2) - cyl_x(dr, xb - 26, xb + 26, 0, dz)
    strap = (tube_x(dr, dr + 3, xb - 15, xb + 15, 0, dz) & box(xb - 20, xb + 20, -110, 110, dz - dr + 2, dz + dr + 5))
    strap = union(strap, box(xb - 15, xb + 15, -110, -dr, zt + 2, dz - dr + 5) - cyl_x(dr, xb - 16, xb + 16, 0, dz),
                  box(xb - 15, xb + 15, dr, 110, zt + 2, dz - dr + 5) - cyl_x(dr, xb - 16, xb + 16, 0, dz))
    add("saddle", "Duct saddle and strap", union(saddle, strap), "#374151", 23, "make", (0, 0, 300))
    add("duct", "Lay-flat duct, 200 mm (drawn shortened)", tube_z(dr, dr + 2, bot, -80, ddx, 0), "#F97316", 24, "buy", (0, 0, -300), density=1300.0)
    add("flex", "Flexible duct link, 200 mm", tube_x(dr, dr + 2, 800, bx - 200, 0, dz), "#FB923C", 25, "buy", (0, -500, 0), density=1300.0)

    # 26 exhaust: flexible hose, pipe, bend, riser, rain cap; 27 stands
    ey, ez = P["EXH_Y"], P["EXH_Z"]; eo, ei = P["EXH_OD"] / 2, P["EXH_ID"] / 2
    hose = tube_x(eo, eo + 6, ex + 280, ex + 600, ey, ez)
    pipe_x0 = ex + 550
    br2 = 120.0
    pipe = tube_x(ei, eo, pipe_x0, P["EXH_X1"] - br2, ey, ez)
    tor4 = bd.Pos(P["EXH_X1"] - br2, ey, ez + br2) * bd.Rot(90, 0, 0) * bd.Torus(br2, eo)
    tor4i = bd.Pos(P["EXH_X1"] - br2, ey, ez + br2) * bd.Rot(90, 0, 0) * bd.Torus(br2, ei)
    q4 = box(P["EXH_X1"] - br2, P["EXH_X1"] + eo + 5, ey - eo - 5, ey + eo + 5, ez - eo - 5, ez + br2)
    ebend = (tor4 & q4) - (tor4i & q4)
    riser = tube_z(ei, eo, ez + br2, P["EXH_TOP"], P["EXH_X1"], ey)
    cap = union(cyl_z(70, P["EXH_TOP"] + 50, P["EXH_TOP"] + 53, P["EXH_X1"], ey),
                *[cyl_z(3, P["EXH_TOP"], P["EXH_TOP"] + 50, P["EXH_X1"] + 22 * math.cos(math.radians(a)), ey + 22 * math.sin(math.radians(a)))
                  for a in (90, 210, 330)])
    add("exh_hose", "Exhaust flexible hose", hose, "#A8A29E", 26, "buy", (0, 0, 300))
    add("exhaust", "Exhaust pipe, bend, riser and cap", comp(pipe, ebend, riser, cap), "#78716C", 26, "make", (0, 0, 300))
    stands = []
    for xs_ in P["STAND_X"]:
        stands.append(union(box(xs_ - 100, xs_ + 100, ey - 100, ey + 100, 0, 6), box(xs_ - 20, xs_ + 20, ey - 20, ey + 20, 6, ez - eo)))
    xs_ = P["EXH_X1"]
    stands.append(union(box(xs_ - 100, xs_ + 100, ey - eo - 140, ey - eo + 60, 0, 6), box(xs_ - 20, xs_ + 20, ey - eo - 40, ey - eo, 6, 1800)))
    add("stands", "Exhaust stands (3)", comp(*stands), "#374151", 27, "make", (0, -400, 0))

    # 28 discharge hose (drawn short)
    dh = union(tube_y(ro, ro + 6, -900, -420, ux, 300), cyl_between((ux, -900, 300), (ux, -1500, 40), ro + 6) - cyl_between((ux, -901, 300), (ux, -1501, 40), ro))
    add("dis_hose", "Discharge hose, 40 mm (drawn short)", dh, "#1D4ED8", 28, "buy", (0, -300, 0), density=1200.0)
    return out


# --------------------------------------------------------------------------- grouping
BOM_NAMES = {
    1: "Sleepers, stakes and coach screws", 2: "Span module with pedestals and cleats", 3: "Drive module", 4: "Module joint bolts",
    5: "Pillow block bearings", 6: "Pump wheel shaft and layshaft", 7: "Rope pump wheel", 8: "Pump pulley",
    9: "Backstop ratchet and pawl", 10: "Pulleys", 11: "V-belts", 12: "Clutch idler and lever", 13: "Engine and engine plate",
    14: "Blower, plate and inlet guard", 15: "Layshaft cover", 16: "Belt guard", 17: "Pump wheel hood",
    18: "Pipe head, tee and spout", 19: "Rising main (drawn shortened)", 20: "Guide block", 21: "Rope and pistons",
    22: "Support wire", 23: "Duct head and saddle", 24: "Lay-flat duct (drawn shortened)", 25: "Flexible duct link",
    26: "Exhaust extension", 27: "Exhaust stands", 28: "Discharge hose",
}
BOM_COLORS = {1: "#8B6B4A", 2: "#4B5563", 3: "#374151", 4: "#111827", 5: "#1F2937", 6: "#9CA3AF", 7: "#1F2937", 8: "#0F766E",
              9: "#B45309", 10: "#64748B", 11: "#111827", 12: "#C2410C", 13: "#B91C1C", 14: "#0EA5E9", 15: "#CA8A04",
              16: "#EAB308", 17: "#EAB308", 18: "#0F766E", 19: "#E5E7EB", 20: "#374151", 21: "#F59E0B", 22: "#9CA3AF",
              23: "#94A3B8", 24: "#F97316", 25: "#FB923C", 26: "#78716C", 27: "#374151", 28: "#1D4ED8"}
BOM_EXPLODE = {1: (0, 0, -500), 2: (0, 0, 0), 3: (700, 0, 0), 4: (350, 0, -250), 5: (0, 0, 450), 6: (0, -900, 450),
               7: (0, 0, 900), 8: (0, 700, 700), 9: (0, -600, 250), 10: (0, 650, 300), 11: (0, 950, 450), 12: (0, 650, 900),
               13: (700, 0, 800), 14: (0, -850, 800), 15: (0, 0, 650), 16: (0, 1200, 500), 17: (0, 0, 1500),
               18: (0, -600, 1100), 19: (0, 0, -400), 20: (0, 0, -900), 21: (0, 300, 0), 22: (0, -250, -200),
               23: (0, -500, 700), 24: (0, -400, -500), 25: (0, -700, 300), 26: (1200, 0, 600), 27: (1200, -500, 0), 28: (0, -900, 0)}


def build_parts(P=PARAMS, comps=None):
    """Components grouped by BOM line: (name, shape, colour, bom, explode)."""
    bd = _b()
    comps = comps or components(P)
    parts = []
    for bom, name in BOM_NAMES.items():
        kids = [c.shape for c in comps if c.bom == bom]
        if kids:
            parts.append((name, bd.Compound(children=kids), BOM_COLORS[bom], bom, BOM_EXPLODE[bom]))
    return parts


def assembly(parts=None):
    bd = _b()
    parts = parts or build_parts()
    return bd.Compound(children=[p[1] for p in parts])


def masses(comps=None):
    comps = comps or components()
    return {c.key: c.shape.volume * 1e-9 * c.density for c in comps}


# --------------------------------------------------------------------------- fit checks
CONTACTS = [
    ("span", "sleepers"), ("drive", "sleepers"), ("cleats", "span"), ("cleats", "sleepers"), ("screws", "cleats"),
    ("stakes", "sleepers"), ("span", "drive"), ("joint_bolts", "span"), ("joint_bolts", "drive"), ("pedestals", "span"),
    ("bearings", "pedestals"), ("pump_shaft", "bearings"), ("layshaft", "bearings"), ("wheel", "pump_shaft"),
    ("ring", "pump_shaft"), ("ratchet", "pump_shaft"), ("pawl", "span"), ("lay_pulleys", "layshaft"),
    ("eng_pulley", "engine"), ("blow_pulley", "blower"), ("idler", "clutch"), ("clutch", "idler_post"), ("idler_post", "span"),
    ("eng_plate", "drive"), ("engine", "eng_plate"), ("blow_plate", "drive"), ("blower", "blow_plate"), ("inlet_guard", "blower"),
    ("guard_brackets", "span"), ("guard_brackets", "guard"), ("hood", "span"), ("pipe_head", "span"),
    ("main", "pipe_head"), ("main", "tee"), ("main", "guide"), ("guide_weights", "guide"), ("roller", "guide"),
    ("wire", "pipe_head"), ("wire", "guide"), ("duct_head", "saddle"), ("saddle", "span"), ("duct", "duct_head"),
    ("flex", "duct_head"), ("flex", "blower"), ("exh_hose", "engine"), ("exh_hose", "exhaust"), ("exhaust", "stands"),
    ("dis_hose", "tee"), ("rope", "wheel"), ("rope", "roller"), ("pistons", "rope"),
    ("idler", "belts"), ("lay_cover", "pedestals"),
]
# Pairs that share volume on purpose: belts sit in pulley grooves (drawn on the pitch line), the stakes and coach
# screws go into the timber, the rope runs in the wheel groove and the pipe.
ALLOWED = {frozenset(p) for p in [("belts", "lay_pulleys"), ("belts", "eng_pulley"), ("belts", "blow_pulley"), ("belts", "ring"),
                                  ("screws", "sleepers"), ("belts", "idler"), ("rope", "wheel"), ("rope", "roller"),
                                  ("rope", "tee"), ("rope", "main"), ("rope", "guide")]}


def _solids(shape):
    return list(shape.solids()) or [shape]


def _apart(A, B, pad=0.0):
    return (A.min.X > B.max.X + pad or B.min.X > A.max.X + pad or A.min.Y > B.max.Y + pad or B.min.Y > A.max.Y + pad
            or A.min.Z > B.max.Z + pad or B.min.Z > A.max.Z + pad)


def check_fits(comps=None, tol=1.0, verbose=True):
    comps = comps or components()
    sol = {c.key: [(s, s.bounding_box()) for s in _solids(c.shape)] for c in comps}
    bbs = {c.key: c.shape.bounding_box() for c in comps}
    overlaps = []
    for i, a in enumerate(comps):
        for b in comps[i + 1:]:
            if frozenset((a.key, b.key)) in ALLOWED or _apart(bbs[a.key], bbs[b.key]):
                continue
            v = 0.0
            for sa, ba in sol[a.key]:
                if _apart(ba, bbs[b.key]):
                    continue
                for sb, bb in sol[b.key]:
                    if _apart(ba, bb):
                        continue
                    r = sa & sb
                    try:
                        v += r.volume if r is not None else 0.0
                    except Exception:
                        pass
            if v >= tol:
                overlaps.append((a.key, b.key, v))
    gaps = []
    for ka, kb in CONTACTS:
        pairs = [(sa, sb) for sa, ba in sol[ka] for sb, bb in sol[kb] if not _apart(ba, bb, 1.0)]
        d = min((sa.distance_to(sb) for sa, sb in pairs), default=99.0)
        if d > 0.05:
            gaps.append((ka, kb, d))
    if verbose:
        print(f"fit check: {len(comps)} components; {len(overlaps)} overlaps; {len(gaps)} missing contacts")
        for o in overlaps:
            print(f"  OVERLAP {o[0]} / {o[1]}: {o[2]:.1f} mm3")
        for g in gaps:
            print(f"  NO CONTACT {g[0]} / {g[1]}: {g[2]:.2f} mm apart")
    return overlaps, gaps


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    comps = components()
    if "--check" in sys.argv:
        o, g = check_fits(comps)
        m = masses(comps)
        for k in ("span", "drive", "pedestals", "engine", "blower"):
            print(f"  mass {k}: {m[k]:.1f} kg")
        sys.exit(1 if (o or g) else 0)
    from build123d import export_step, export_stl
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    by = {c.key: c for c in comps}
    for key in ("span", "drive", "pedestals", "wheel", "ring", "ratchet", "pawl", "hood", "guard", "pipe_head", "guide",
                "eng_plate", "blow_plate", "clutch", "idler_post", "lay_cover", "saddle", "stands", "pistons", "roller"):
        export_step(by[key].shape, str(root / "step" / f"collardrive-{key}.step"))
        export_stl(by[key].shape, str(root / "stl" / f"collardrive-{key}.stl"), tolerance=0.5, angular_tolerance=0.3)
    # a shape can belong to one compound only, so the assembly is built from fresh components
    export_step(assembly(build_parts()), str(root / "step" / "collardrive-assembly.step"))
    print("wrote", len(list((root / 'step').glob('*.step'))), "STEP files")
