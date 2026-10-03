"""CollarDrive sizing calculations, CLD-CAL-001.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every figure quoted in docs/04-calcs/01-sizing.md with its tag (for example [B3]) and writes
docs/04-calcs/results.csv. Geometry comes from cad/src/model.py (PARAMS, levels(), belts(), components()),
prices from bom/bom.csv and the value-engineering target from project.yaml.
All figures are first-principles estimates for a paper proof of concept.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad/src"), str(ROOT / ".kit")]
from model import PARAMS as P, levels, belts, tangents, belt_length, idler_centre  # noqa: E402

G, RHO_W, RHO_AIR = 9.81, 1000.0, 1.2

# ----------------------------------------------------------------------------- assumptions
A = dict(
    eng_rpm=2800.0,            # governed running speed of the 4.8 kW class engine
    eng_cont_kw=3.0,           # continuous power available at 2,800 rpm (about 60 % of the 4.8 kW rating at 3,600 rpm)
    bsfc=0.55,                 # kg of petrol per kWh at part load (small engines run lightly loaded are thirsty)
    petrol_rho=0.74, petrol_mj=44.0,
    eta_belt=0.95,             # per V-belt stage
    eta_wheel=0.90,            # rope wheel and bearings
    rope_friction=1.15,        # rope pull = column weight x 1.15 (pistons rubbing in the pipe)
    eta_v0=0.90, eta_v_slope=0.006,   # volumetric efficiency = 0.90 - 0.006 x head (m), leakage past pistons
    belt_fe_allow=150.0,       # allowable effective pull per A-section belt on a 90 mm pulley at low speed, N
    fan_p0=700.0, fan_qmax=0.25,      # blower at 2,000 rpm: shut-off 700 Pa, free delivery 0.25 m3/s, p = p0 (1 - (Q/Qmax)^2)
    fan_eta=0.45,
    duct_f=0.035, duct_k=2.5,  # lay-flat duct friction factor; entry, rigid bend and exit losses
    duct_leak_per_30m=0.10,    # fraction of air lost through couplings per 30 m of duct
    air_per_person=0.05,       # m3/s per person at the face (assumed planning figure)
    exh_temp_c=500.0,
)

# Rising main by depth band: (max depth m, name, inside diameter mm). Rope pumps use a smaller pipe deeper
# down so the rope pull stays inside what two A belts and the rope can carry.
BANDS = [(30.0, "40 mm PVC PN10", 36.2), (45.0, "32 mm PVC PN10", 28.8), (60.0, "25 mm PVC PN16", 22.0)]
DESIGN_DEPTH = 30.0           # the priced kit: a 30 m shaft, 40 mm main, 30 m of duct


def band(depth):
    for dmax, name, idm in BANDS:
        if depth <= dmax + 1e-9:
            return name, idm
    return BANDS[-1][1], BANDS[-1][2]


# ----------------------------------------------------------------------------- drive train
def drive():
    L = levels()
    lay = A["eng_rpm"] * P["D_ENG"] / P["D_LAY_BIG"]
    wheel = lay * P["D_LAY_SMALL"] / P["D_RING"]
    blower = lay * P["D_LAY_BLOW"] / P["D_BLOWER"]
    rope_v = math.pi * 2 * P["ROPE_PR"] / 1000 * wheel / 60
    out = dict(lay_rpm=lay, wheel_rpm=wheel, blower_rpm=blower, rope_v=rope_v)
    for k, (y, c1, r1, c2, r2) in belts().items():
        lp = belt_length(c1, r1, c2, r2)
        small = min(r1, r2); big = max(r1, r2)
        d = math.dist(c1, c2)
        wrap = 180 - 2 * math.degrees(math.asin((big - small) / d))
        rpm_small = {"st2": lay, "st1": A["eng_rpm"], "blow": blower}[k]
        v = math.pi * 2 * small / 1000 * rpm_small / 60
        out[k] = dict(centres=d, pitch_len=lp, nominal=f"A{round((lp - 33) / 25.4)}", wrap=wrap, v=v)
    return out


# ----------------------------------------------------------------------------- rope pump
def pump(depth, idm=None, rope_v=None):
    name, idm_b = band(depth)
    idm = idm or idm_b
    rope_v = rope_v or drive()["rope_v"]
    area = math.pi * (idm / 2000) ** 2
    eta_v = max(0.0, A["eta_v0"] - A["eta_v_slope"] * depth)
    q = area * rope_v * eta_v                                    # m3/s
    pull = RHO_W * G * area * depth * A["rope_friction"]         # N, tight side
    rope_kw = pull * rope_v / 1000
    hyd_kw = RHO_W * G * q * depth / 1000
    ring_kw = rope_kw / A["eta_wheel"]
    belt_v = math.pi * P["D_RING"] / 1000 * drive()["wheel_rpm"] / 60
    fe = ring_kw * 1000 / belt_v
    return dict(depth=depth, pipe=name, idm=idm, q_lpm=q * 60000, pull=pull, rope_kw=rope_kw, hyd_kw=hyd_kw,
                ring_kw=ring_kw, fe=fe, belt_use=fe / (P["GROOVES_ST2"] * A["belt_fe_allow"]), eta=hyd_kw / ring_kw if ring_kw else 0)


# ----------------------------------------------------------------------------- blower and duct
def duct_dp(q, length):
    d = 2 * P["DUCT_R"] / 1000
    v = q / (math.pi * d * d / 4)
    return (A["duct_f"] * length / d + A["duct_k"]) * RHO_AIR * v * v / 2


def blower(length):
    """Operating point of the blower on the duct (bisection on fan curve = system curve)."""
    lo, hi = 0.0, A["fan_qmax"]
    for _ in range(60):
        q = (lo + hi) / 2
        fan = A["fan_p0"] * (1 - (q / A["fan_qmax"]) ** 2)
        if fan > duct_dp(q, length):
            lo = q
        else:
            hi = q
    q = (lo + hi) / 2
    p = A["fan_p0"] * (1 - (q / A["fan_qmax"]) ** 2)
    delivered = q * (1 - A["duct_leak_per_30m"] * length / 30)
    shaft_kw = q * p / A["fan_eta"] / 1000
    return dict(length=length, q_fan=q, p=p, q_end=delivered, shaft_kw=shaft_kw, people=delivered / A["air_per_person"])


# ----------------------------------------------------------------------------- power, fuel
def power(depth, duct_len=30.0):
    pm = pump(depth); bl = blower(duct_len)
    lay_kw = pm["ring_kw"] / A["eta_belt"] + bl["shaft_kw"] / A["eta_belt"]
    shaft_kw = lay_kw / A["eta_belt"]
    fuel_lph = shaft_kw * A["bsfc"] / A["petrol_rho"]
    fuel_kw = fuel_lph * A["petrol_rho"] * A["petrol_mj"] * 1000 / 3600
    return dict(lay_kw=lay_kw, shaft_kw=shaft_kw, belt_loss_kw=shaft_kw - pm["ring_kw"] - bl["shaft_kw"],
                fuel_lph=fuel_lph, fuel_kw=fuel_kw, margin=A["eng_cont_kw"] / shaft_kw)


# ----------------------------------------------------------------------------- exhaust
def exhaust():
    L = levels()
    out_pt = (P["EXH_X1"], P["EXH_Y"], P["EXH_TOP"])
    intake = (P["BLOW_X"], -140.0, P["BLOW_Z"])
    collar_edge_x = 750.0                       # edge of a 1.5 m collar on the drive side
    d_collar = (out_pt[0] - collar_edge_x) / 1000
    d_intake = math.dist(out_pt, intake) / 1000
    # back pressure in the 1-1/2 in pipe
    m_dot = 0.196e-3 * A["eng_rpm"] / 2 / 60 * 0.85 * RHO_AIR * 1.07
    rho = 101325 / (287 * (A["exh_temp_c"] + 273))
    idm = P["EXH_ID"] / 1000
    v = m_dot / rho / (math.pi * idm * idm / 4)
    length = (P["EXH_X1"] - P["ENG_X"] - 300) / 1000 + (P["EXH_TOP"] - P["EXH_Z"]) / 1000
    dp = (0.03 * length / idm + 1.5) * rho * v * v / 2
    return dict(d_collar=d_collar, d_intake=d_intake, v=v, dp=dp, length=length)


# ----------------------------------------------------------------------------- frame and shafts
def rhs_props(h, w, t):
    I = (w * h ** 3 - (w - 2 * t) * (h - 2 * t) ** 3) / 12
    return I, I / (h / 2)


def frame():
    span = (P["SLEEPER_X"][1] - P["SLEEPER_X"][0]) / 1000      # m between sleeper centres
    xa = P["SLEEPER_X"][0] / 1000
    I, W = rhs_props(P["SILL_H"], P["SILL_W"], P["SILL_T"])     # mm4, mm3 per sill
    pm = pump(DESIGN_DEPTH)
    loads = [  # (x m, N) point loads on the span module, both sills together
        (P["WHEEL_X"] / 1000, 70 * G + pm["pull"] + 20 * G),    # wheel, pulley, shaft, bearings; rope pull both sides
        (P["WHEEL_X"] / 1000 + 0.2, (0.6 * DESIGN_DEPTH + 25) * G),  # rising main and guide block on the support wire
        (P["DUCT_DROP_X"] / 1000, (0.5 * DESIGN_DEPTH + 5) * G),  # duct hanging from the duct head
        (P["LAY_X"] / 1000, 25 * G),                            # layshaft, pulleys, bearings
    ]
    misuse = (0.0, 1500.0)                                       # a person on the frame over the shaft (must not happen)
    w_self = 56 * G / 2.75                                       # N/m self weight
    def moment(pts):
        ra = sum(f * (xa + span - x) for x, f in pts) / span + w_self * span / 2
        best = 0.0
        for k in range(200):
            x = xa + span * k / 199
            m = ra * (x - xa) - w_self * (x - xa) ** 2 / 2 - sum(f * (x - xx) for xx, f in pts if xx < x)
            best = max(best, m)
        return best
    m_work = moment(loads); m_mis = moment(loads + [misuse])
    s_work = m_work * 1000 / (2 * W); s_mis = m_mis * 1000 / (2 * W)
    E = 210e3
    defl_mis = (misuse[1] * (span * 1000) ** 3) / (48 * E * 2 * I)
    total_n = sum(f for _, f in loads) + w_self * 2.75 + 90 * G + 30 * G
    bearing = total_n / (3 * P["SLEEPER"][0] * P["SLEEPER"][1] / 1e6) / 1000
    return dict(span=span, I=I, W=W, m_work=m_work, m_mis=m_mis, s_work=s_work, s_mis=s_mis, defl_mis=defl_mis,
                bearing_kpa=bearing, total_kn=total_n / 1000)


def shafts():
    d = drive(); pm = pump(DESIGN_DEPTH); bl = blower(30.0)
    # pump shaft 30 mm: torque from the rope, belt pull overhung 150 mm outside the bearing
    T = pm["pull"] * P["ROPE_PR"] / 1000                       # N m
    Fe = pm["fe"]; F_shaft = 1.5 * Fe
    M = F_shaft * (P["Y_ST2"] - P["SILL_Y"]) / 1000
    dsh = 2 * P["PUMP_SHAFT_R"] / 1000
    s_eq = 32 / (math.pi * dsh ** 3) * math.sqrt(M ** 2 + 0.75 * T ** 2) / 1e6
    # layshaft 25 mm: the three pulleys overhang 60 to 150 mm; add their shaft loads (conservative)
    st1_fe = power(DESIGN_DEPTH)["lay_kw"] * 1000 / d["st1"]["v"]
    blow_fe = bl["shaft_kw"] / A["eta_belt"] * 1000 / (math.pi * P["D_LAY_BLOW"] / 1000 * d["lay_rpm"] / 60)
    st2_fe = Fe / A["eta_belt"]
    Ml = (1.5 * st1_fe * (P["Y_ST1"] - P["SILL_Y"]) + 1.5 * blow_fe * (P["Y_BLOW"] - P["SILL_Y"]) + 1.5 * st2_fe * (P["Y_ST2"] - P["SILL_Y"])) / 1000
    Tl = power(DESIGN_DEPTH)["lay_kw"] * 1000 / (2 * math.pi * d["lay_rpm"] / 60)
    dl = 2 * P["LAY_R"] / 1000
    s_lay = 32 / (math.pi * dl ** 3) * math.sqrt(Ml ** 2 + 0.75 * Tl ** 2) / 1e6
    # backstop: the full column wants to run the rope back
    T_back = pump(30.0)["pull"] / A["rope_friction"] * P["ROPE_PR"] / 1000
    tooth = T_back / 0.104
    return dict(T=T, M=M, s_pump=s_eq, Tl=Tl, Ml=Ml, s_lay=s_lay, T_back=T_back, tooth=tooth)


# ----------------------------------------------------------------------------- mass and cost
def bom_rows():
    with (ROOT / "bom/bom.csv").open() as f:
        return list(csv.DictReader(f))


def cost():
    rows = bom_rows()
    total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
    import yaml
    target = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
    top = sorted(((float(r["unit_cost_usd"]) * float(r["qty"]), r["item"]) for r in rows), reverse=True)[:6]
    return dict(total=total, target=target, diff=total - target, top=top)


def mass():
    from model import components
    cs = {c.key: c for c in components()}
    made = lambda k: cs[k].shape.volume * 1e-9 * cs[k].density  # noqa: E731
    span = made("span") + made("pedestals") + made("cleats")
    drive_ = made("drive")
    return dict(span=span, drive=drive_, engine=16.0, blower=30.0, wheel_set=made("wheel") + 14.0 + made("pump_shaft") + made("ratchet"),
                guard=made("guard"), hood=made("hood"))


def results():
    d = drive(); pw20 = power(20.0); pm20 = pump(20.0); bl30 = blower(30.0); ex = exhaust(); m = mass()
    return dict(q20=pm20["q_lpm"], q60=pump(60.0)["q_lpm"], air_end30=bl30["q_end"], shaft_kw=pw20["shaft_kw"],
                fuel_kw=pw20["fuel_kw"], lay_kw=pw20["lay_kw"], rope_kw_20=pm20["ring_kw"], hyd_kw_20=pm20["hyd_kw"],
                belt_loss_kw=pw20["belt_loss_kw"], blower_kw=bl30["shaft_kw"], exh_collar=ex["d_collar"], exh_intake=ex["d_intake"],
                frame_len=(P["DRIVE_X1"] - P["SPAN_X0"]) / 1000, frame_w=(2 * P["SILL_Y"] + P["SILL_W"]) / 1000, span_kg=m["span"])


def main():
    rows = []
    def out(tag, text, value=None):
        print(f"[{tag}] {text}")
        rows.append((tag, text, "" if value is None else f"{value:.4g}"))
    d = drive()
    out("A1", f"Layshaft {d['lay_rpm']:.0f} rpm; rope wheel {d['wheel_rpm']:.1f} rpm; blower {d['blower_rpm']:.0f} rpm at {A['eng_rpm']:.0f} rpm engine", d["wheel_rpm"])
    out("A2", f"Rope speed {d['rope_v']:.2f} m/s on a {2 * P['ROPE_PR']:.0f} mm rope circle", d["rope_v"])
    for k, label in (("st1", "Engine to layshaft"), ("st2", "Layshaft to pump pulley (two belts)"), ("blow", "Layshaft to blower")):
        b = d[k]
        out(f"A3-{k}", f"{label}: centres {b['centres']:.0f} mm, pitch length {b['pitch_len']:.0f} mm (about {b['nominal']}), "
                       f"wrap on the small pulley {b['wrap']:.0f} deg, belt speed {b['v']:.1f} m/s", b["pitch_len"])
    ix, iz = idler_centre()
    out("A4", f"Clutch idler centre at {ix:.0f} mm along, {iz:.0f} mm up; presses the slack strand of the pump belts", iz)
    for dep in (10.0, 20.0, 30.0, 40.0, 45.0, 60.0):
        p = pump(dep)
        out(f"B{int(dep)}", f"{dep:.0f} m head, {p['pipe']}: {p['q_lpm']:.1f} L/min; rope pull {p['pull']:.0f} N; rope power {p['rope_kw']:.2f} kW; "
                            f"at the pump pulley {p['ring_kw']:.2f} kW; belt pull {p['fe']:.0f} N ({100 * p['belt_use']:.0f} % of two A belts); "
                            f"pump efficiency {100 * p['eta']:.0f} %", p["q_lpm"])
    for L_ in (30.0, 60.0):
        b = blower(L_)
        out(f"C{int(L_)}", f"Duct {L_:.0f} m: blower {b['q_fan']:.3f} m3/s at {b['p']:.0f} Pa; {b['q_end']:.3f} m3/s at the duct end "
                           f"(enough for {b['people']:.1f} people at {A['air_per_person']} m3/s each); blower shaft {b['shaft_kw']:.2f} kW", b["q_end"])
    for dep in (20.0, 30.0, 60.0):
        pw = power(dep)
        out(f"D{int(dep)}", f"{dep:.0f} m head with 30 m duct: engine shaft {pw['shaft_kw']:.2f} kW ({pw['margin']:.1f} x margin on "
                            f"{A['eng_cont_kw']} kW continuous); belt losses {pw['belt_loss_kw']:.2f} kW; petrol {pw['fuel_lph']:.2f} L/h", pw["shaft_kw"])
    ex = exhaust()
    out("E1", f"Exhaust outlet {ex['d_collar']:.2f} m from the edge of a 1.5 m collar and {ex['d_intake']:.2f} m from the blower intake", ex["d_intake"])
    out("E2", f"Exhaust gas {ex['v']:.1f} m/s in {ex['length']:.1f} m of pipe; back pressure about {ex['dp']:.0f} Pa", ex["dp"])
    f = frame()
    out("F1", f"Span module: {f['span']:.2f} m between sleeper centres; per sill I = {f['I'] / 1e4:.0f} cm4, W = {f['W'] / 1e3:.1f} cm3", f["W"])
    out("F2", f"Working loads at {DESIGN_DEPTH:.0f} m: moment {f['m_work']:.0f} N m, bending stress {f['s_work']:.0f} MPa", f["s_work"])
    out("F3", f"Misuse check, 1.5 kN on the frame over the shaft centre: {f['m_mis']:.0f} N m, {f['s_mis']:.0f} MPa, "
              f"deflection {f['defl_mis']:.1f} mm (S275 yield 275 MPa)", f["s_mis"])
    out("F4", f"Ground bearing under the three sleepers about {f['bearing_kpa']:.0f} kPa for {f['total_kn']:.1f} kN in total", f["bearing_kpa"])
    s = shafts()
    out("G1", f"Pump shaft 30 mm: torque {s['T']:.0f} N m, overhung belt moment {s['M']:.0f} N m, equivalent stress {s['s_pump']:.0f} MPa", s["s_pump"])
    out("G2", f"Layshaft 25 mm: torque {s['Tl']:.1f} N m, overhung moment {s['Ml']:.0f} N m, equivalent stress {s['s_lay']:.0f} MPa", s["s_lay"])
    out("G3", f"Backstop holds {s['T_back']:.0f} N m; tooth load {s['tooth']:.0f} N at 104 mm", s["tooth"])
    m = mass()
    out("H1", f"Span module with pedestals and cleats {m['span']:.1f} kg; drive module {m['drive']:.1f} kg; engine about {m['engine']:.0f} kg; "
              f"blower about {m['blower']:.0f} kg; wheel, pump pulley, shaft and ratchet {m['wheel_set']:.1f} kg", m["span"])
    c = cost()
    out("H2", f"Bill of materials USD {c['total']:,.0f}; value-engineering target USD {c['target']:,.0f}; "
              f"USD {abs(c['diff']):,.0f} {'over' if c['diff'] > 0 else 'under'} the target", c["total"])
    for v, item in c["top"]:
        out("H3", f"  cost driver: {item} USD {v:,.0f}", v)
    with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["tag", "result", "value"]); w.writerows(rows)


if __name__ == "__main__":
    main()
