"""Regenerates the figures of telecom/5g-nr-for-rf-engineers (run from the repository root).

    python scripts/make_5g_figures.py
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join("telecom", "5g-nr-for-rf-engineers", "figures")
os.makedirs(OUT, exist_ok=True)
INK, MUTED, LINE, ACC, ACC2, TEAL, SOFT = "#1d2433", "#5c6370", "#e3e1da", "#3b5bdb", "#c2410c", "#0f766e", "#eef1fb"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "figure.facecolor": "none", "axes.facecolor": "none", "axes.grid": True,
    "grid.color": LINE, "grid.linewidth": 0.8, "legend.frameon": False,
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True)
    plt.close(fig)

# 1. Slots per 1 ms subframe for each numerology, with CP share
def fig_numerology():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.grid(False)
    mus = [0, 1, 2, 3, 4]
    for row, mu in enumerate(mus):
        n = 2 ** mu
        w = 1.0 / n
        for s in range(n):
            ax.add_patch(Rectangle((s * w, -row - 0.38), w * 0.97, 0.76, facecolor=SOFT, edgecolor=ACC, lw=1))
        ax.text(-0.02, -row, f"μ={mu}  {15*n} kHz", ha="right", va="center", color=INK, fontsize=12)
        ax.text(1.02, -row, f"{1000/n:g} µs/slot", ha="left", va="center", color=MUTED, fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(-len(mus) + 0.4, 0.6)
    ax.set_yticks([]); ax.set_xticks([0, .25, .5, .75, 1]); ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1 ms"])
    ax.spines["left"].set_visible(False)
    ax.set_title("One 1 ms subframe: 2^μ slots of 14 symbols (normal CP)", color=INK, fontsize=13, loc="left")
    save(fig, "numerology-slots.svg")

# 2. Doppler ICI (SIR) vs speed for several SCS at 3.5 and 28 GHz
def fig_doppler():
    v = np.linspace(3, 500, 400) / 3.6
    fig, ax = plt.subplots(figsize=(10, 4.4))
    c = 3e8
    styles = [(3.5e9, 30e3, ACC, "-"), (3.5e9, 15e3, ACC, "--"), (28e9, 120e3, ACC2, "-"), (28e9, 60e3, ACC2, "--")]
    for fc, scs, col, ls in styles:
        fd = v * fc / c
        Tu = 1 / scs
        ici = (np.pi * fd * Tu) ** 2 / 3
        ax.plot(v * 3.6, -10 * np.log10(ici), color=col, ls=ls, lw=2, label=f"{fc/1e9:g} GHz, {scs/1e3:g} kHz")
    ax.set_xlabel("UE speed (km/h)"); ax.set_ylabel("SIR from Doppler ICI (dB)")
    ax.set_ylim(10, 70); ax.legend(ncol=2, loc="upper right")
    ax.axhline(25, color=MUTED, lw=1, ls=":"); ax.text(10, 26, "≈ 256QAM needs ~25–30 dB SINR", color=MUTED, fontsize=10)
    save(fig, "doppler-ici.svg")

# 3. TDD DDDSU with 10:2:2 special slot, symbol level
def fig_tdd():
    fig, ax = plt.subplots(figsize=(11, 2.4))
    ax.grid(False)
    slots = ["D", "D", "D", "S", "U"]
    sym = 0
    for i, s in enumerate(slots):
        for k in range(14):
            if s == "D" or (s == "S" and k < 10): col, ed = SOFT, ACC
            elif s == "U" or (s == "S" and k >= 12): col, ed = "#fdf1e8", ACC2
            else: col, ed = "white", MUTED
            ax.add_patch(Rectangle((sym, 0), 0.92, 1, facecolor=col, edgecolor=ed, lw=0.8))
            sym += 1
        ax.text(i * 14 + 7, 1.25, f"slot {i} · {s}", ha="center", color=INK, fontsize=11)
    ax.text(3 * 14 + 11, -0.45, "GP", ha="center", color=MUTED, fontsize=10)
    ax.set_xlim(-0.5, 70.5); ax.set_ylim(-0.7, 1.6); ax.axis("off")
    ax.set_title("DDDSU @ 30 kHz (2.5 ms), special slot 10 D : 2 GP : 2 U", color=INK, fontsize=13, loc="left")
    save(fig, "tdd-dddsu.svg")

# 4. SSB resource map 240 x 4
def fig_ssb():
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.grid(False)
    def blk(l, k0, k1, col, ed, lab=None):
        ax.add_patch(Rectangle((l, k0), 0.95, k1 - k0, facecolor=col, edgecolor=ed, lw=1))
        if lab: ax.text(l + 0.475, (k0 + k1) / 2, lab, ha="center", va="center", fontsize=10, color=INK, rotation=90)
    blk(0, 56, 183, SOFT, ACC, "PSS · k=56…182")
    blk(1, 0, 240, "#fdf1e8", ACC2, "PBCH + DMRS · k=0…239")
    blk(2, 0, 48, "#fdf1e8", ACC2, "PBCH")
    blk(2, 56, 183, SOFT, ACC, "SSS · k=56…182")
    blk(2, 192, 240, "#fdf1e8", ACC2, "PBCH")
    blk(3, 0, 240, "#fdf1e8", ACC2, "PBCH + DMRS · k=0…239")
    ax.set_xlim(-0.2, 4.1); ax.set_ylim(-5, 245)
    ax.set_xticks([0.475, 1.475, 2.475, 3.475]); ax.set_xticklabels(["l=0", "l=1", "l=2", "l=3"])
    ax.set_yticks([0, 56, 120, 182, 239]); ax.set_ylabel("subcarrier k within SSB")
    ax.set_title("SS/PBCH block: 240 subcarriers × 4 OFDM symbols (TS 38.211 Table 7.4.3.1-1)", color=INK, fontsize=12, loc="left")
    save(fig, "ssb-map.svg")

# 5. PRACH format 0 timing at gNB for near and far UE
def fig_prach():
    fig, ax = plt.subplots(figsize=(11, 3.0))
    ax.grid(False)
    CP, SEQ, GT = 103.1, 800.0, 96.9
    for row, (d, lab) in enumerate([(0, "UE at gNB"), (14.5, "UE at 14.5 km")]):
        rtd = 2 * d * 1e3 / 3e8 * 1e6
        y = -row * 1.3
        ax.add_patch(Rectangle((rtd, y), CP, 0.8, facecolor="#fdf1e8", edgecolor=ACC2))
        ax.add_patch(Rectangle((rtd + CP, y), SEQ, 0.8, facecolor=SOFT, edgecolor=ACC))
        ax.text(rtd + CP / 2, y + 0.4, "CP", ha="center", va="center", fontsize=10)
        ax.text(rtd + CP + SEQ / 2, y + 0.4, "ZC sequence, L=839, 800 µs", ha="center", va="center", fontsize=10)
        ax.text(-20, y + 0.4, lab, ha="right", va="center", fontsize=11, color=INK)
    ax.axvline(CP + SEQ + GT, color=MUTED, ls="--", lw=1); ax.text(CP + SEQ + GT + 5, 0.9, "end of 1 ms PRACH slot", fontsize=10, color=MUTED)
    ax.axvline(CP, color=TEAL, ls=":", lw=1.5); ax.text(CP + 4, -1.65, "gNB FFT window starts", fontsize=10, color=TEAL)
    ax.set_xlim(-230, 1080); ax.set_ylim(-1.9, 1.2); ax.set_yticks([]); ax.set_xlabel("time at gNB receiver (µs)")
    ax.spines["left"].set_visible(False)
    ax.set_title("PRACH format 0: CP 103.1 µs, GT 96.9 µs → round trip ≤ 96.9 µs ≈ 14.5 km", color=INK, fontsize=12, loc="left")
    save(fig, "prach-format0.svg")

# 6. Event A3 timeline with hysteresis and TTT
def fig_a3():
    t = np.arange(0, 6000, 40)
    rng = np.random.default_rng(3)
    serving = -80 - t / 6000 * 18 + rng.normal(0, 1.2, t.size)
    neigh = -98 + t / 6000 * 20 + rng.normal(0, 1.2, t.size)
    a = 1 / 2 ** (4 / 4)
    def l3(x):
        y = np.empty_like(x); y[0] = x[0]
        for i in range(1, x.size): y[i] = (1 - a) * y[i - 1] + a * x[i]
        return y
    s, n = l3(serving), l3(neigh)
    off, hys, ttt = 3, 1, 320
    cond = n - hys > s + off
    trig = None; run = 0
    for i, c in enumerate(cond):
        run = run + 40 if c else 0
        if run >= ttt: trig = t[i]; break
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.plot(t, serving, color=ACC, alpha=0.25, lw=1); ax.plot(t, neigh, color=ACC2, alpha=0.25, lw=1)
    ax.plot(t, s, color=ACC, lw=2, label="serving (L3 filtered, k=4)"); ax.plot(t, n, color=ACC2, lw=2, label="neighbour (L3 filtered)")
    ax.plot(t, s + off + hys, color=MUTED, ls="--", lw=1.2, label="serving + offset + hys")
    if trig:
        first = t[np.argmax(cond)]
        ax.axvspan(first, trig, color=TEAL, alpha=0.12)
        ax.axvline(trig, color=TEAL, lw=1.5); ax.text(trig + 60, -76, f"report sent\n(TTT {ttt} ms)", color=TEAL, fontsize=10)
    ax.set_xlabel("time (ms)"); ax.set_ylabel("SS-RSRP (dBm)"); ax.legend(loc="lower left", fontsize=10)
    ax.set_title("Event A3: Mn + Ofn + Ocn − Hys > Mp + Ofp + Ocp + Off, held for TTT", color=INK, fontsize=12, loc="left")
    save(fig, "event-a3.svg")

# 7. 38.901 UMa NLOS path loss vs distance
def fig_pathloss():
    d = np.linspace(50, 5000, 400)
    hBS, hUT = 25, 1.5
    d3 = np.sqrt(d ** 2 + (hBS - hUT) ** 2)
    fig, ax = plt.subplots(figsize=(10, 4.4))
    for fc, col in [(0.7, TEAL), (3.5, ACC), (28, ACC2)]:
        los = 28.0 + 22 * np.log10(d3) + 20 * np.log10(fc)
        nl = 13.54 + 39.08 * np.log10(d3) + 20 * np.log10(fc) - 0.6 * (hUT - 1.5)
        ax.plot(d, np.maximum(los, nl), color=col, lw=2, label=f"UMa NLOS, {fc:g} GHz")
    ax.axhline(119.9, color=MUTED, ls="--", lw=1.2); ax.text(2900, 121.5, "MAPL 119.9 dB (UL budget, Lecture 7)", color=MUTED, fontsize=10)
    ax.set_xlabel("2D distance (m), hBS 25 m, hUT 1.5 m"); ax.set_ylabel("path loss (dB)")
    ax.legend(loc="lower right"); ax.set_ylim(70, 195)
    ax.set_title("TR 38.901 UMa: PL = max(PL_LOS, PL′_NLOS), no shadowing, no O2I", color=INK, fontsize=12, loc="left")
    save(fig, "uma-pathloss.svg")

# 8. Array factor, N=8
def fig_array():
    th = np.radians(np.linspace(-90, 90, 2001))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    def af(N, d, th0):
        psi = 2 * np.pi * d * (np.sin(th) - np.sin(np.radians(th0)))
        n = np.arange(N)[:, None]
        a = np.abs(np.exp(1j * n * psi).sum(axis=0)) / N
        return 20 * np.log10(np.maximum(a, 1e-4))
    ax.plot(np.degrees(th), af(8, 0.5, 0), color=MUTED, lw=1.5, label="d = λ/2, broadside")
    ax.plot(np.degrees(th), af(8, 0.5, 30), color=ACC, lw=2, label="d = λ/2, steered 30°")
    ax.plot(np.degrees(th), af(8, 1.0, 30), color=ACC2, lw=2, ls="--", label="d = λ, steered 30° (grating lobe)")
    ax.set_ylim(-35, 2); ax.set_xlim(-90, 90); ax.set_xlabel("angle θ (degrees)"); ax.set_ylabel("|AF| normalized (dB)")
    ax.legend(loc="lower left", fontsize=10)
    ax.set_title("8-element uniform linear array factor", color=INK, fontsize=12, loc="left")
    save(fig, "array-factor.svg")

for f in [fig_numerology, fig_doppler, fig_tdd, fig_ssb, fig_prach, fig_a3, fig_pathloss, fig_array]:
    f()
print("figures ok")
