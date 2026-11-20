"""Extra figures for Chapter 1 (The Air Interface)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

BASE = sys.argv[1] if len(sys.argv) > 1 else "telecom"
OUT = os.path.join(BASE, "ch1-the-air-interface", "figures")
os.makedirs(OUT, exist_ok=True)
INK, MUTED, LINE, ACC, ACC2, TEAL, SOFT, WARM = "#1d2433", "#5c6370", "#e3e1da", "#3b5bdb", "#c2410c", "#0f766e", "#eef1fb", "#fdf1e8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "figure.facecolor": "none", "axes.facecolor": "none", "axes.grid": False, "legend.frameon": False})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True); plt.close(fig)

def symbol_timeline():
    """Half a millisecond at 15 kHz and 30 kHz, CP shaded."""
    fig, ax = plt.subplots(figsize=(11, 2.8))
    Tc = 1 / (480e3 * 4096)
    for row, (mu, n) in enumerate([(0, 7), (1, 14)]):
        t = 0.0
        for l in range(n):
            ncp = 144 * 64 * 2 ** -mu + (16 * 64 if l == 0 else 0)
            nu = 2048 * 64 * 2 ** -mu
            cp, su = ncp * Tc * 1e6, nu * Tc * 1e6
            y = -row * 1.2
            ax.add_patch(Rectangle((t, y), cp, 0.8, facecolor=WARM, edgecolor=ACC2, lw=0.8))
            ax.add_patch(Rectangle((t + cp, y), su, 0.8, facecolor=SOFT, edgecolor=ACC, lw=0.8))
            t += cp + su
        ax.text(-8, -row * 1.2 + 0.4, f"{15*2**mu} kHz", ha="right", va="center", fontsize=12, color=INK)
    ax.set_xlim(-60, 505); ax.set_ylim(-1.4, 1.2); ax.set_yticks([])
    ax.spines["left"].set_visible(False); ax.set_xlabel("time (µs) — one half-subframe")
    ax.add_patch(Rectangle((300, 0.95), 12, 0.18, facecolor=WARM, edgecolor=ACC2)); ax.text(316, 1.04, "cyclic prefix", va="center", fontsize=10, color=MUTED)
    ax.add_patch(Rectangle((400, 0.95), 12, 0.18, facecolor=SOFT, edgecolor=ACC)); ax.text(416, 1.04, "useful symbol", va="center", fontsize=10, color=MUTED)
    ax.set_title("0.5 ms holds 7 symbols at 15 kHz and 14 at 30 kHz; the first CP is slightly longer", color=INK, fontsize=12, loc="left")
    save(fig, "symbol-timeline.svg")

def cp_echo():
    fig, ax = plt.subplots(figsize=(11, 3.3))
    cp, su = 2.34, 33.33
    rows = [("transmitted", 0, 1.0), ("direct path", 0, 1.0), ("echo 1.5 µs (inside CP)", 1.5, 0.6), ("echo 4 µs (beyond CP)", 4.0, 0.5)]
    for i, (lab, d, a) in enumerate(rows):
        y = -i
        for k in range(2):
            x0 = d + k * (cp + su)
            ax.add_patch(Rectangle((x0, y), cp, 0.7, facecolor=WARM, edgecolor=ACC2, alpha=a))
            ax.add_patch(Rectangle((x0 + cp, y), su, 0.7, facecolor=SOFT, edgecolor=ACC, alpha=a))
        ax.text(-1, y + 0.35, lab, ha="right", va="center", fontsize=11, color=INK)
    ax.axvspan(cp + su + cp, 2 * (cp + su), color=TEAL, alpha=0.08)
    ax.axvline(cp + su + cp, color=TEAL, ls="--", lw=1.2); ax.text(cp + su + cp + 0.4, 0.85, "FFT window of symbol 2", color=TEAL, fontsize=10)
    ax.annotate("spills into the next symbol (ISI)", xy=(cp + su + 4.0 + 0.2, -2.7), xytext=(52, -3.6), fontsize=10, color=ACC2,
                arrowprops=dict(arrowstyle="->", color=ACC2))
    ax.set_xlim(-25, 75); ax.set_ylim(-3.9, 1.2); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("time (µs) at 30 kHz SCS (CP 2.34 µs)")
    ax.set_title("Echoes inside the CP only rotate phase; echoes beyond it cause interference", color=INK, fontsize=12, loc="left")
    save(fig, "cp-echo.svg")

def pdp():
    t = np.linspace(0, 6, 600)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    for sig, col, lab in [(0.1, TEAL, "σ = 100 ns (nominal)"), (0.364, ACC, "σ = 364 ns (UMa NLOS median)"), (1.15, ACC2, "σ = 1.15 µs (UMa NLOS 90 %)")]:
        ax.plot(t, -10 * np.log10(np.e) * t / sig, color=col, lw=2, label=lab)
    for cp, lab in [(4.69, "CP 15 kHz"), (2.34, "CP 30 kHz"), (0.59, "CP 120 kHz")]:
        ax.axvline(cp, color=MUTED, ls=":", lw=1.2); ax.text(cp + 0.05, -29.5, lab, rotation=90, va="bottom", fontsize=9, color=MUTED)
    ax.axhline(-15, color=MUTED, lw=0.8); ax.text(5.0, -14.2, "−15 dB", fontsize=9, color=MUTED)
    ax.set_ylim(-30, 1); ax.set_xlim(0, 6); ax.set_xlabel("excess delay (µs)"); ax.set_ylabel("relative power (dB)")
    ax.grid(True, color=LINE); ax.legend(loc="upper right", fontsize=10)
    ax.set_title("Exponential power-delay profiles against the CP lengths", color=INK, fontsize=12, loc="left")
    save(fig, "pdp-vs-cp.svg")

def resource_grid():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    nsym, nsc = 14, 24
    for l in range(nsym):
        for k in range(nsc):
            if l < 2: c, e = "#fde68a", "#b45309"          # CORESET / PDCCH
            elif l == 2 and k % 2 == 0: c, e = WARM, ACC2   # DMRS type 1
            elif l == 11 and k % 2 == 0: c, e = WARM, ACC2  # additional DMRS
            elif l in (5, 9) and k == 4: c, e = "#d1fae5", TEAL  # PT-RS-like / CSI-RS RE
            else: c, e = SOFT, ACC
            ax.add_patch(Rectangle((l, k), 0.95, 0.95, facecolor=c, edgecolor=e, lw=0.5))
    ax.add_patch(Rectangle((-0.05, -0.05), 14, 12, fill=False, edgecolor=INK, lw=1.6))
    ax.text(14.3, 6, "1 RB =\n12 subcarriers", va="center", fontsize=10, color=INK)
    ax.text(14.3, 18, "next RB", va="center", fontsize=10, color=MUTED)
    ax.set_xlim(-0.3, 17.5); ax.set_ylim(-0.6, 24.6)
    ax.set_xticks(np.arange(14) + 0.47); ax.set_xticklabels(range(14), fontsize=9); ax.set_xlabel("OFDM symbol in slot")
    ax.set_yticks([0.47, 11.47, 23.47]); ax.set_yticklabels(["0", "11", "23"], fontsize=9); ax.set_ylabel("subcarrier")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor="#fde68a", edgecolor="#b45309", label="CORESET (PDCCH)"), Patch(facecolor=WARM, edgecolor=ACC2, label="DMRS"),
                       Patch(facecolor="#d1fae5", edgecolor=TEAL, label="CSI-RS / PT-RS RE"), Patch(facecolor=SOFT, edgecolor=ACC, label="PDSCH data")],
              loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=4, fontsize=10)
    ax.set_title("One slot, two resource blocks: who uses which resource element (example)", color=INK, fontsize=12, loc="left")
    save(fig, "resource-grid.svg")

def carrier_layout():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.add_patch(Rectangle((0, 0), 100, 0.5, facecolor="white", edgecolor=MUTED))
    ax.text(50, 0.25, "channel bandwidth 100 MHz", ha="center", va="center", fontsize=10, color=MUTED)
    ax.add_patch(Rectangle((0.85, 0.7), 98.28, 0.6, facecolor=SOFT, edgecolor=ACC))
    ax.text(50, 1.0, "transmission bandwidth: 273 RBs × 360 kHz = 98.28 MHz", ha="center", va="center", fontsize=10, color=INK)
    ax.add_patch(Rectangle((0, 0.7), 0.85, 0.6, facecolor=WARM, edgecolor=ACC2)); ax.add_patch(Rectangle((99.13, 0.7), 0.87, 0.6, facecolor=WARM, edgecolor=ACC2))
    ax.text(0.4, 1.45, "guard\n845 kHz", ha="center", fontsize=8, color=ACC2); ax.text(99.6, 1.45, "guard", ha="center", fontsize=8, color=ACC2)
    ax.add_patch(Rectangle((30, 1.5), 25, 0.5, facecolor="#d1fae5", edgecolor=TEAL)); ax.text(42.5, 1.75, "active BWP", ha="center", va="center", fontsize=10, color=TEAL)
    ax.add_patch(Rectangle((44, 2.2), 7.2, 0.5, facecolor="#fde68a", edgecolor="#b45309")); ax.text(47.6, 2.45, "SSB", ha="center", va="center", fontsize=10)
    ax.annotate("Point A (CRB 0, subcarrier 0)", xy=(0.85, 0.7), xytext=(5, 2.6), fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK))
    ax.annotate("offsetToPointA + k_SSB", xy=(44, 2.2), xytext=(60, 2.9), fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK))
    ax.set_xlim(-2, 102); ax.set_ylim(-0.2, 3.2); ax.axis("off")
    ax.set_title("Carrier layout: guard bands, Point A, BWP and SSB (not to scale vertically)", color=INK, fontsize=12, loc="left")
    save(fig, "carrier-layout.svg")

def peak_rate():
    def rate(v, qm, nprb, mu, oh, f=1.0):
        return 1e-6 * v * qm * f * 948 / 1024 * nprb * 12 / (1e-3 / (14 * 2 ** mu)) * (1 - oh)
    cases = [("LTE-like: 20 MHz, 15 kHz\n2 layers, 64QAM", rate(2, 6, 106, 0, 0.14)),
             ("n78: 100 MHz, 30 kHz\n4 layers, 256QAM", rate(4, 8, 273, 1, 0.14)),
             ("FR2: 400 MHz, 120 kHz\n2 layers, 64QAM", rate(2, 6, 264, 3, 0.18)),
             ("n78 ×2 CA: 2×100 MHz\n4 layers, 256QAM", 2 * rate(4, 8, 273, 1, 0.14))]
    fig, ax = plt.subplots(figsize=(10, 3.8))
    labels = [c[0] for c in cases]; vals = [c[1] for c in cases]
    bars = ax.barh(labels[::-1], vals[::-1], color=[ACC, ACC2, ACC, TEAL][::-1])
    for b, v in zip(bars, vals[::-1]):
        ax.text(v + 40, b.get_y() + b.get_height() / 2, f"{v:,.0f} Mbps", va="center", fontsize=11, color=INK)
    ax.set_xlim(0, max(vals) * 1.25); ax.set_xlabel("theoretical peak DL rate (TS 38.306 formula)")
    ax.tick_params(axis="y", labelsize=10)
    ax.set_title("What the grid can carry at most (before TDD and real overhead)", color=INK, fontsize=12, loc="left")
    save(fig, "peak-rate.svg")
    return vals

def bwp_timeline():
    fig, ax = plt.subplots(figsize=(11, 3.2))
    segs = [(0, 30, 0.35, 0.2, "BWP 1 · 20 MHz", TEAL), (30, 32.5, 0, 1, "", MUTED), (32.5, 70, 0, 1, "BWP 2 · 100 MHz (download)", ACC), (70, 120, 0, 1, "inactivity timer running…", "#93a4ee"),
            (120, 122.5, 0, 1, "", MUTED), (122.5, 160, 0.35, 0.2, "default BWP 1", TEAL)]
    for x0, x1, y0, h, lab, col in segs:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, h, facecolor=col, alpha=0.25 if col != MUTED else 0.5, edgecolor=col))
        if lab: ax.text((x0 + x1) / 2, y0 + h / 2, lab, ha="center", va="center", fontsize=10, color=INK)
    ax.annotate("DCI with BWP indicator = 1\n(short switching gap)", xy=(30, 1.0), xytext=(4, 1.25), fontsize=10, color=INK, arrowprops=dict(arrowstyle="->"))
    ax.annotate("timer expires", xy=(120, 1.0), xytext=(124, 1.35), fontsize=10, color=INK, arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(0, 160); ax.set_ylim(-0.2, 1.75); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("time (ms, illustrative)")
    ax.set_title("BWP switching: by DCI up to the wide BWP, back to the default when the timer expires", color=INK, fontsize=12, loc="left")
    save(fig, "bwp-timeline.svg")

def tdd_patterns():
    pats = [("DDDSU (2.5 ms)", "DDDSU"), ("DDDDDDDSUU (5 ms)", "DDDDDDDSUU"), ("DSUUU (2.5 ms, UL-heavy)", "DSUUU"), ("DDSU (2 ms)", "DDSU")]
    fig, ax = plt.subplots(figsize=(11, 3.4))
    for r, (lab, p) in enumerate(pats):
        y = -r
        for i, s in enumerate(p):
            col, ed = {"D": (SOFT, ACC), "U": (WARM, ACC2), "S": ("white", MUTED)}[s]
            ax.add_patch(Rectangle((i, y), 0.92, 0.7, facecolor=col, edgecolor=ed)); ax.text(i + 0.46, y + 0.35, s, ha="center", va="center", fontsize=11)
        d = p.count("D") * 14 + p.count("S") * 10; u = p.count("U") * 14 + p.count("S") * 2; tot = len(p) * 14
        ax.text(10.5, y + 0.35, f"{lab}:  DL {100*d/tot:.0f} %  ·  UL {100*u/tot:.0f} %", va="center", fontsize=11, color=INK)
    ax.set_xlim(-0.2, 24); ax.set_ylim(-3.5, 0.9); ax.axis("off")
    ax.set_title("Common TDD patterns at 30 kHz (special slot 10:2:2)", color=INK, fontsize=12, loc="left")
    save(fig, "tdd-patterns.svg")

def gp_radius():
    syms = np.arange(1, 9)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for scs, col, off in [(15, ACC2, -0.2), (30, ACC, 0.2)]:
        T = 71.35 if scs == 15 else 35.68
        r = syms * T * 1e-6 * 3e8 / 2 / 1e3
        ax.bar(syms + off, r, width=0.38, color=col, label=f"{scs} kHz")
    ax.set_xlabel("guard-period symbols"); ax.set_ylabel("max cell radius (km)"); ax.legend()
    ax.grid(True, axis="y", color=LINE)
    ax.set_title("Guard period → maximum TDD cell radius (switching time ignored)", color=INK, fontsize=12, loc="left")
    save(fig, "gp-radius.svg")

def sync_drift():
    t = np.logspace(0, 6, 400)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    for df, col, lab in [(1e-8, ACC2, "TCXO-class, 1×10⁻⁸"), (1e-10, ACC, "OCXO, 1×10⁻¹⁰"), (5e-12, TEAL, "rubidium, 5×10⁻¹²")]:
        ax.loglog(t / 3600, df * t * 1e6, color=col, lw=2, label=lab)
    ax.axhline(1.5, color=MUTED, ls="--"); ax.text(2e-4, 1.8, "±1.5 µs budget", color=MUTED, fontsize=10)
    ax.set_xlabel("time since GNSS loss (hours)"); ax.set_ylabel("time error (µs)"); ax.set_ylim(1e-3, 1e4)
    ax.grid(True, color=LINE, which="both", lw=0.5); ax.legend(loc="upper left", fontsize=10)
    ax.set_title("Holdover: time error grows with the oscillator's frequency offset (illustrative, constant offset)", color=INK, fontsize=12, loc="left")
    save(fig, "sync-drift.svg")

def ducting():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    sym = 35.68
    pat = "DDDSU"
    def frame(y, shift, lab, alpha=1.0):
        x = shift
        for s in pat:
            for k in range(14):
                if s == "D" or (s == "S" and k < 10): col, ed = SOFT, ACC
                elif s == "U" or (s == "S" and k >= 12): col, ed = WARM, ACC2
                else: col, ed = "white", MUTED
                ax.add_patch(Rectangle((x, y), sym * 0.95, 0.6, facecolor=col, edgecolor=ed, lw=0.4, alpha=alpha)); x += sym
        ax.text(-30, y + 0.3, lab, ha="right", va="center", fontsize=10, color=INK)
    frame(0, 0, "victim gNB")
    frame(-1, 50, "aggressor 15 km (50 µs)", 0.9)
    frame(-2, 1000, "aggressor 300 km (1 ms)", 0.9)
    ax.axvspan(3 * 14 * sym + 12 * sym, 5 * 14 * sym, color=ACC2, alpha=0.08)
    ax.text(3 * 14 * sym + 12 * sym + 10, 0.85, "victim UL symbols", color=ACC2, fontsize=10)
    ax.set_xlim(-400, 5 * 14 * sym + 1050); ax.set_ylim(-2.4, 1.2); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("time at the victim (µs)")
    ax.set_title("A far aggressor's downlink, delayed by propagation, lands on the victim's uplink", color=INK, fontsize=12, loc="left")
    save(fig, "ducting-delay.svg")

for f in [symbol_timeline, cp_echo, pdp, resource_grid, carrier_layout, bwp_timeline, tdd_patterns, gp_radius, sync_drift, ducting]:
    f()
print("peak", [round(v) for v in peak_rate()])
