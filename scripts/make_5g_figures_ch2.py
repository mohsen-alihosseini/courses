"""Extra figures for Chapter 2 (Finding the Network)."""
import math, os, sys
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

BASE = sys.argv[1] if len(sys.argv) > 1 else "telecom"
OUT = os.path.join(BASE, "ch2-finding-the-network", "figures")
os.makedirs(OUT, exist_ok=True)
INK, MUTED, LINE, ACC, ACC2, TEAL, SOFT, WARM, GOLD = "#1d2433", "#5c6370", "#e3e1da", "#3b5bdb", "#c2410c", "#0f766e", "#eef1fb", "#fdf1e8", "#fde68a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "figure.facecolor": "none", "axes.facecolor": "none", "axes.grid": False, "legend.frameon": False})
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True); plt.close(fig)

def box(ax, x, y, w, h, text, fc=SOFT, ec=ACC, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK)

def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.3))

# 1. SSB burst positions, Case B and Case C (>3 GHz), 4 slots at 30 kHz
def ssb_burst():
    fig, ax = plt.subplots(figsize=(11, 2.9))
    cases = [("Case B", [4, 8, 16, 20, 32, 36, 44, 48]), ("Case C", [2, 8, 16, 22, 30, 36, 44, 50])]
    for r, (lab, starts) in enumerate(cases):
        y = -r * 1.3
        for s in range(56):
            ax.add_patch(Rectangle((s, y), 0.9, 0.8, facecolor="white", edgecolor=LINE, lw=0.5))
        for i, s0 in enumerate(starts):
            ax.add_patch(Rectangle((s0, y), 3.9, 0.8, facecolor=GOLD, edgecolor="#b45309", lw=1))
            ax.text(s0 + 1.95, y + 0.4, f"#{i}", ha="center", va="center", fontsize=9)
        ax.text(-1, y + 0.4, lab, ha="right", va="center", fontsize=11, color=INK)
    for k in range(5):
        ax.axvline(14 * k - 0.05, color=MUTED, lw=1, ls=":")
        if k < 4: ax.text(14 * k + 7, 1.05, f"slot {k}", ha="center", fontsize=10, color=MUTED)
    ax.set_xlim(-8, 57); ax.set_ylim(-1.6, 1.4); ax.axis("off")
    ax.set_title("8 SSB candidates in the first 2 ms of the half-frame at 30 kHz (above 3 GHz)", color=INK, fontsize=12, loc="left")
    save(fig, "ssb-burst-cases.svg")

# 2. PBCH coding chain
def pbch_chain():
    fig, ax = plt.subplots(figsize=(11, 2.6))
    steps = [("MIB\n24 bits", GOLD, "#b45309"), ("+ 8 PHY bits\n(SFN LSBs,\nhalf-frame,\nSSB index)", SOFT, ACC), ("+ 24 CRC\n= 56 bits", SOFT, ACC),
             ("polar code\n+ rate match\n→ 864 bits", SOFT, ACC), ("scrambling\n(cell ID, SFN,\nSSB index)", SOFT, ACC), ("QPSK\n432 symbols", SOFT, ACC), ("map with\n144 DMRS REs", WARM, ACC2)]
    w, gap = 1.55, 0.3
    for i, (t, fc, ec) in enumerate(steps):
        x = i * (w + gap)
        box(ax, x, 0, w, 1.2, t, fc, ec, fs=9.5)
        if i: arrow(ax, x - gap, 0.6, x, 0.6)
    ax.set_xlim(-0.1, len(steps) * (w + gap)); ax.set_ylim(-0.2, 1.5); ax.axis("off")
    ax.set_title("PBCH: from 24 MIB bits to 432 QPSK symbols in each SSB", color=INK, fontsize=12, loc="left")
    save(fig, "pbch-chain.svg")

# 3. PSS detection by correlation (computed)
def pss_seq(nid2):
    x = [0, 1, 1, 0, 1, 1, 1]
    for i in range(127 - 7):
        x.append((x[i + 4] + x[i]) % 2)
    return np.array([1 - 2 * x[(n + 43 * nid2) % 127] for n in range(127)], float)

def pss_corr():
    rng = np.random.default_rng(7)
    N = 256
    def ofdm(freq):
        X = np.zeros(N, complex); X[np.arange(-63, 64) % N] = freq; return np.fft.ifft(X) * np.sqrt(N)
    sig = []
    for _ in range(3): sig.append(ofdm((rng.choice([-1, 1], 127) + 1j * rng.choice([-1, 1], 127)) / np.sqrt(2)))
    true = 1
    sig.append(ofdm(pss_seq(true)))
    for _ in range(3): sig.append(ofdm((rng.choice([-1, 1], 127) + 1j * rng.choice([-1, 1], 127)) / np.sqrt(2)))
    rx = np.concatenate(sig)
    rx = rx * np.exp(1j * 2 * np.pi * 0.02 * np.arange(rx.size) / N)          # small CFO
    rx += (rng.normal(size=rx.size) + 1j * rng.normal(size=rx.size)) * np.sqrt(0.5 * 10 ** (0.3))  # SNR ≈ −3 dB
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for nid2, col in zip(range(3), [MUTED, ACC, ACC2]):
        ref = ofdm(pss_seq(nid2))
        c = np.abs(np.correlate(rx, ref, mode="valid")) / N
        ax.plot(np.arange(c.size), c, color=col, lw=1.6 if nid2 == true else 1.1, label=f"reference N_ID(2) = {nid2}")
    ax.axvline(3 * N, color=TEAL, ls=":", lw=1.2); ax.text(3 * N + 15, ax.get_ylim()[1] * 0.92, "true PSS start", color=TEAL, fontsize=10)
    ax.set_xlabel("sample offset"); ax.set_ylabel("|correlation|"); ax.legend(loc="upper right", fontsize=10)
    ax.set_title("Correlating against the 3 PSS sequences at SNR ≈ −3 dB: one clear peak gives timing and N_ID(2)", color=INK, fontsize=12, loc="left")
    save(fig, "pss-correlation.svg")

# 4. CORESET#0 placement example
def coreset0():
    fig, ax = plt.subplots(figsize=(11, 2.9))
    ax.add_patch(Rectangle((0, 0), 51, 0.5, facecolor="white", edgecolor=MUTED)); ax.text(25.5, 0.25, "carrier: 51 RBs at 30 kHz (20 MHz)", ha="center", va="center", fontsize=10, color=MUTED)
    ax.add_patch(Rectangle((0, 0.8), 48, 0.6, facecolor="#d1fae5", edgecolor=TEAL)); ax.text(24, 1.1, "CORESET#0: 48 RBs, 1 symbol (index 10)", ha="center", va="center", fontsize=10, color=INK)
    ax.add_patch(Rectangle((12, 1.7), 20, 0.6, facecolor=GOLD, edgecolor="#b45309")); ax.text(22, 2.0, "SSB: 20 RBs", ha="center", va="center", fontsize=10)
    ax.annotate("", xy=(0, 2.45), xytext=(12, 2.45), arrowprops=dict(arrowstyle="<->", color=INK)); ax.text(6, 2.6, "offset 12 RBs", ha="center", fontsize=10)
    ax.annotate("Point A = CRB 0", xy=(0, 0), xytext=(-6, -0.7), fontsize=10, arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(-8, 53); ax.set_ylim(-0.9, 2.9); ax.axis("off")
    ax.set_title("CORESET#0 is placed relative to the SSB (example: offsetToPointA 12 RBs at 30 kHz)", color=INK, fontsize=12, loc="left")
    save(fig, "coreset0-placement.svg")

# 5. SSB → RACH occasion mapping
def ssb_ro():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    cols = plt.cm.tab10(np.linspace(0, 1, 10))[:8]
    for i in range(8):
        ax.add_patch(Rectangle((i * 0.9, 1.6), 0.8, 0.6, facecolor=cols[i], alpha=0.55, edgecolor=INK, lw=0.6)); ax.text(i * 0.9 + 0.4, 1.9, f"SSB{i}", ha="center", va="center", fontsize=8)
    ax.text(-0.3, 1.9, "DL burst", ha="right", va="center", fontsize=10)
    for t in range(4):
        for f in range(2):
            i = 2 * t + f
            x, y = 9 + t * 1.6, f * 0.65
            ax.add_patch(Rectangle((x, y), 1.4, 0.55, facecolor=cols[i], alpha=0.55, edgecolor=INK, lw=0.6)); ax.text(x + 0.7, y + 0.27, f"RO for SSB{i}", ha="center", va="center", fontsize=8)
    ax.text(8.7, 0.6, "PRACH occasions\n(msg1-FDM = 2)", ha="right", va="center", fontsize=10)
    ax.annotate("UE hears SSB5 best → sends its preamble in SSB5's occasion", xy=(9 + 2 * 1.6 + 0.7, 1.2), xytext=(4.5, 2.7), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=ACC2), color=ACC2)
    ax.set_xlim(-2, 16); ax.set_ylim(-0.2, 3.0); ax.axis("off")
    ax.set_title("One SSB per RACH occasion: where the preamble arrives tells the gNB the best beam", color=INK, fontsize=12, loc="left")
    save(fig, "ssb-to-ro.svg")

# 6. 4-step vs 2-step sequence charts
def ra_sequence():
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
    for ax, title, msgs in [(axs[0], "4-step (contention based)", [("Msg1: preamble", 1), ("Msg2: RAR (TA, UL grant, TC-RNTI)", -1), ("Msg3: RRC Setup Request", 1), ("Msg4: contention resolution", -1)]),
                            (axs[1], "2-step (Rel-16)", [("MsgA: preamble + PUSCH", 1), ("MsgB: TA, C-RNTI, contention ID", -1)])]:
        ax.axvline(0, color=INK, lw=1.5); ax.axvline(1, color=INK, lw=1.5)
        ax.text(0, 0.3, "UE", ha="center", fontsize=11, fontweight="bold"); ax.text(1, 0.3, "gNB", ha="center", fontsize=11, fontweight="bold")
        for k, (m, d) in enumerate(msgs):
            y = -0.8 - k * 0.9
            ax.annotate("", xy=(1 if d > 0 else 0, y - 0.25), xytext=(0 if d > 0 else 1, y), arrowprops=dict(arrowstyle="->", color=ACC if d > 0 else ACC2, lw=1.6))
            ax.text(0.5, y + 0.08, m, ha="center", fontsize=9.5, color=INK)
        ax.set_xlim(-0.25, 1.25); ax.set_ylim(-4.4, 0.6); ax.axis("off"); ax.set_title(title, fontsize=12, color=INK)
    save(fig, "ra-4step-2step.svg")

# 7. PRACH power ramping
def ramping():
    att = np.arange(1, 9)
    fig, ax = plt.subplots(figsize=(10, 3.4))
    for pl, step, col in [(120, 2, ACC), (114, 4, ACC2)]:
        p = np.minimum(23, -104 + pl + (att - 1) * step)
        ax.plot(att, p, "o-", color=col, lw=2, label=f"PL {pl} dB, step {step} dB")
    ax.axhline(23, color=MUTED, ls="--"); ax.text(6.2, 22.2, "P_CMAX = 23 dBm", fontsize=10, color=MUTED)
    ax.set_xlabel("preamble attempt"); ax.set_ylabel("PRACH power (dBm)"); ax.legend(loc="lower right", fontsize=10); ax.grid(True, color=LINE)
    ax.set_title("Power ramping with target −104 dBm: louder each time, until the cap", color=INK, fontsize=12, loc="left")
    save(fig, "prach-ramping.svg")

# 8. N_CS and roots per cell vs radius
def ncs_roots():
    allowed = [13, 15, 18, 22, 26, 32, 38, 46, 59, 76, 93, 119, 167, 279, 419]
    r = np.linspace(0.5, 58, 600)
    roots, ncs = [], []
    for ri in r:
        need = (2 * ri * 1e3 / 3e8 * 1e6 + 5) / (800 / 839)
        n = next((a for a in allowed if a >= need), None)
        ncs.append(n if n else np.nan)
        roots.append(math.ceil(64 / (839 // n)) if n else np.nan)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.step(r, roots, where="post", color=ACC, lw=2)
    ax.set_xlabel("cell radius (km), long preamble, 5 µs delay spread"); ax.set_ylabel("ZC roots per cell", color=ACC)
    ax2 = ax.twinx(); ax2.step(r, ncs, where="post", color=ACC2, lw=1.4, ls="--"); ax2.set_ylabel("N_CS", color=ACC2)
    ax2.spines["top"].set_visible(False)
    ax.axvline(14.5, color=MUTED, ls=":"); ax.text(15.2, 24, "format 0 limit\n(≈ 14.5 km)", fontsize=9, color=MUTED)
    ax.grid(True, color=LINE)
    ax.set_title("Larger cells need larger cyclic shifts, so each cell consumes more root sequences", color=INK, fontsize=12, loc="left")
    save(fig, "ncs-roots.svg")

# 9. Initial access flow
def access_flow():
    fig, ax = plt.subplots(figsize=(11, 3.3))
    steps = [("Cell search\nPSS/SSS", "SSB"), ("MIB\n(PBCH)", "SSB"), ("SIB1\n(CORESET#0)", "PDCCH/PDSCH"), ("Cell\nselection", "SS-RSRP"),
             ("Random\naccess", "PRACH…Msg4"), ("RRC setup +\nregistration", "SRB1, NAS"), ("Security +\ncapability", "RRC/NAS"), ("PDU\nsession", "first IP packet")]
    w, gap = 1.15, 0.25
    for i, (t, sub) in enumerate(steps):
        x = i * (w + gap)
        fc, ec = (GOLD, "#b45309") if i < 2 else ((SOFT, ACC) if i < 4 else ((WARM, ACC2) if i == 4 else ("#d1fae5", TEAL)))
        box(ax, x, 0.5, w, 1.0, t, fc, ec, fs=9.5)
        ax.text(x + w / 2, 0.25, sub, ha="center", fontsize=8.5, color=MUTED)
        ax.text(x + w / 2, 1.65, str(i + 1), ha="center", fontsize=10, color=INK, fontweight="bold")
        if i: arrow(ax, x - gap, 1.0, x, 1.0)
    ax.set_xlim(-0.1, len(steps) * (w + gap)); ax.set_ylim(0, 1.9); ax.axis("off")
    ax.set_title("Power-on to first byte: what each step uses", color=INK, fontsize=12, loc="left")
    save(fig, "access-flow.svg")

for f in [ssb_burst, pbch_chain, pss_corr, coreset0, ssb_ro, ra_sequence, ramping, ncs_roots, access_flow]:
    f()
print("ok")
