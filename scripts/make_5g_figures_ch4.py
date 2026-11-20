"""Extra figures for Chapter 4 (Beams, Antennas & Hardware)."""
import math, os, sys
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Wedge, Rectangle

BASE = sys.argv[1] if len(sys.argv) > 1 else "telecom"
OUT = os.path.join(BASE, "ch4-beams-antennas-hardware", "figures")
os.makedirs(OUT, exist_ok=True)
INK, MUTED, LINE, ACC, ACC2, TEAL, SOFT, WARM, GOLD = "#1d2433", "#5c6370", "#e3e1da", "#3b5bdb", "#c2410c", "#0f766e", "#eef1fb", "#fdf1e8", "#fde68a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "figure.facecolor": "none", "axes.facecolor": "none", "legend.frameon": False,
    "axes.grid": True, "grid.color": LINE, "grid.linewidth": 0.7})
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True); plt.close(fig)
def title(ax, t, fs=12): ax.set_title(t, color=INK, fontsize=fs, loc="left")
def box(ax, x, y, w, h, text, fc=SOFT, ec=ACC, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK)
def arrow(ax, x0, y0, x1, y1, col=MUTED):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=col, lw=1.3))
def db(x): return 10 * np.log10(x)

def af(n, d, steer, th):
    psi = 2 * np.pi * d * (np.sin(th) - np.sin(steer))
    a = np.abs(np.exp(1j * np.outer(np.arange(n), psi)).sum(0)) / n
    return 20 * np.log10(np.maximum(a, 1e-4))

# 1. Gain and beamwidth vs number of elements
def array_gain():
    n = np.array([1, 2, 4, 8, 16, 32, 64])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
    a1.plot(n, 20 * np.log10(n), "o-", color=ACC, label="EIRP gain, one PA per element (20·lg N)")
    a1.plot(n, 10 * np.log10(n), "o-", color=TEAL, label="same total power split over N (10·lg N)")
    a1.set_xscale("log", base=2); a1.set_xticks(n); a1.set_xticklabels(n); a1.set_xlabel("elements in one row (N)"); a1.set_ylabel("dB")
    a1.legend(fontsize=9.5); title(a1, "Array gain")
    a2.plot(n[1:], 102 / n[1:], "o-", color=ACC2)
    for x in (8, 16, 32):
        a2.annotate(f"{102/x:.1f}°", (x, 102 / x), textcoords="offset points", xytext=(4, 6), fontsize=9.5, color=ACC2)
    a2.set_xscale("log", base=2); a2.set_xticks(n[1:]); a2.set_xticklabels(n[1:]); a2.set_xlabel("elements in one row (N), λ/2 spacing"); a2.set_ylabel("3 dB beamwidth (°)")
    title(a2, "Beamwidth ≈ 102°/N at broadside")
    fig.tight_layout(); save(fig, "array-gain.svg")

# 2. Polar beam patterns
def polar_beams():
    th = np.linspace(-np.pi / 2, np.pi / 2, 1441)
    fig = plt.figure(figsize=(11, 4))
    for k, (n, steer, lab) in enumerate([(8, 0, "8 elements, broadside"), (8, 30, "8 elements, steered 30°"), (32, 30, "32 elements, steered 30°")]):
        ax = fig.add_subplot(1, 3, k + 1, projection="polar")
        g = np.maximum(af(n, 0.5, np.radians(steer), th), -40) + 40
        ax.plot(th, g, color=[ACC, TEAL, ACC2][k], lw=1.6)
        ax.set_thetamin(-90); ax.set_thetamax(90); ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
        ax.set_yticks([10, 20, 30, 40]); ax.set_yticklabels(["−30", "−20", "−10", "0 dB"], fontsize=8, color=MUTED)
        ax.set_xticks(np.radians([-90, -60, -30, 0, 30, 60, 90])); ax.tick_params(labelsize=9)
        ax.set_title(lab, fontsize=11, color=INK, pad=4)
    save(fig, "polar-beams.svg")

# 3. Grating lobes
def grating():
    th = np.linspace(-np.pi / 2, np.pi / 2, 2001)
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for d, col, lw in [(0.5, ACC, 2), (0.8, TEAL, 1.2), (1.0, ACC2, 1.2)]:
        ax.plot(np.degrees(th), af(16, d, np.radians(40), th), color=col, lw=lw, label=f"spacing {d} λ")
    ax.set_ylim(-35, 9); ax.set_xlabel("angle (°)"); ax.set_ylabel("array factor (dB)"); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=10)
    ax.annotate("grating lobe (1.0 λ)", (-21, 0), xytext=(-8, 4), fontsize=9.5, color=ACC2, arrowprops=dict(arrowstyle="->", color=ACC2))
    ax.annotate("grating lobe (0.8 λ)", (-37, 0), xytext=(-75, 4), fontsize=9.5, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL))
    title(ax, "16 elements steered to 40°: spacing above λ/2 creates copies of the main beam")
    save(fig, "grating-lobes.svg")

# 4. Analog / digital / hybrid
def architectures():
    fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.4))
    for ax in axs: ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    # analog
    ax = axs[0]; title(ax, "Analog: 1 chain, phase shifters", 11)
    box(ax, 0.2, 3.3, 2.2, 1.4, "baseband\n1 stream", GOLD, "#b45309", 9); box(ax, 3, 3.3, 1.8, 1.4, "DAC +\nRF", SOFT, ACC, 9)
    arrow(ax, 2.4, 4, 3, 4)
    for i, y in enumerate([0.6, 2.4, 4.2, 6.0]):
        arrow(ax, 4.8, 4, 6, y + 0.5); box(ax, 6, y, 1.4, 1, "φ", WARM, ACC2, 10); ax.text(8.3, y + 0.5, "▲", fontsize=14, color=INK, ha="center", va="center")
    # digital
    ax = axs[1]; title(ax, "Digital: 1 chain per element", 11)
    box(ax, 0.2, 2.6, 2.4, 2.8, "baseband\nprecoder\nN streams", GOLD, "#b45309", 9)
    for y in [0.6, 2.4, 4.2, 6.0]:
        arrow(ax, 2.6, 4, 4, y + 0.5); box(ax, 4, y, 2.4, 1, "DAC + RF", SOFT, ACC, 9); ax.text(8, y + 0.5, "▲", fontsize=14, ha="center", va="center")
    # hybrid
    ax = axs[2]; title(ax, "Hybrid: few chains, sub-arrays", 11)
    box(ax, 0.2, 2.6, 2.2, 2.8, "baseband\nprecoder\n2 streams", GOLD, "#b45309", 9)
    for yc, ys in [(5.5, [4.6, 6.4]), (2.5, [0.8, 2.6])]:
        arrow(ax, 2.4, 4, 3.2, yc); box(ax, 3.2, yc - 0.6, 1.8, 1.2, "DAC +\nRF", SOFT, ACC, 9)
        for y in ys:
            arrow(ax, 5, yc, 6, y + 0.4); box(ax, 6, y, 1.3, 0.8, "φ", WARM, ACC2, 10); ax.text(8.3, y + 0.4, "▲", fontsize=14, ha="center", va="center")
    save(fig, "bf-architectures.svg")

# 5. P1 / P2 / P3
def p123():
    fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.3))
    for ax in axs: ax.axis("off"); ax.set_xlim(-1, 11); ax.set_ylim(-4.5, 4.5); ax.set_aspect("equal")
    def gnb(ax): ax.add_patch(Rectangle((-0.6, -0.8), 0.6, 1.6, facecolor=INK));
    def ue(ax, x=9.3, y=0.6): ax.add_patch(Rectangle((x - 0.25, y - 0.45), 0.5, 0.9, facecolor=ACC2))
    ax = axs[0]; gnb(ax); ue(ax); title(ax, "P1: wide beams sweep, UE reports best", 11)
    for a in range(-40, 41, 20): ax.add_patch(Wedge((0, 0), 8, a - 9, a + 9, facecolor=SOFT if a != 0 else GOLD, edgecolor=ACC, lw=0.8, alpha=0.9))
    ax = axs[1]; gnb(ax); ue(ax); title(ax, "P2: narrow beams inside the best one", 11)
    for a in (-6, -2, 2, 6): ax.add_patch(Wedge((0, 0), 9, a - 2, a + 2, facecolor=GOLD if a == 2 else SOFT, edgecolor=ACC, lw=0.8))
    ax = axs[2]; gnb(ax); ue(ax, 9.3, 0.0); title(ax, "P3: one gNB beam, UE sweeps its RX beam", 11)
    ax.add_patch(Wedge((0, 0), 8.6, -2, 2, facecolor=GOLD, edgecolor=ACC, lw=0.8))
    for a in (150, 170, 190, 210): ax.add_patch(Wedge((9.3, 0), 3, a - 9, a + 9, facecolor=WARM if a != 190 else "#fbbf8a", edgecolor=ACC2, lw=0.8))
    save(fig, "p1-p2-p3.svg")

# 6. QCL chain
def qcl_chain():
    fig, ax = plt.subplots(figsize=(11, 2.8)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 3)
    items = [(0.1, "SSB #i\nwide beam", GOLD, "#b45309"), (3.0, "TRS\n(CSI-RS for tracking)", SOFT, ACC), (5.9, "CSI-RS\nfor CSI / beams", SOFT, ACC), (8.8, "PDCCH / PDSCH\nDMRS", WARM, ACC2)]
    for x, t, fc, ec in items: box(ax, x, 0.9, 2.1, 1.3, t, fc, ec, 9.5)
    for x0, lab in [(2.2, "Type C + D"), (5.1, "Type A + D"), (8.0, "Type A + D")]:
        arrow(ax, x0, 1.55, x0 + 0.8, 1.55); ax.text(x0 + 0.4, 2.35, lab, ha="center", fontsize=9.5, color=MUTED)
    ax.text(0.1, 0.35, "Type A: Doppler shift + spread, average delay, delay spread · Type C: Doppler shift, average delay · Type D: receive beam", fontsize=9.5, color=MUTED)
    title(ax, "QCL chain: each signal borrows timing, frequency and beam from the one before")
    save(fig, "qcl-chain.svg")

# 7. Beam failure recovery
def bfr():
    fig, ax = plt.subplots(figsize=(11, 3)); ax.axis("off"); ax.set_xlim(0, 11.6); ax.set_ylim(0, 3)
    steps = [("BFD-RS quality\nbelow threshold\n(hypothetical BLER)", SOFT, ACC), ("count instances\nup to\nbeamFailure-\nInstanceMaxCount", SOFT, ACC), ("pick candidate\nbeam above\nrsrp-Threshold", SOFT, ACC),
             ("PRACH on the\ncandidate's\nresource (CFRA)", WARM, ACC2), ("gNB answers on\nrecovery search\nspace → done", GOLD, "#b45309")]
    for i, (t, fc, ec) in enumerate(steps):
        x = i * 2.35; box(ax, x, 0.6, 2.0, 1.8, t, fc, ec, 9)
        if i: arrow(ax, x - 0.35, 1.5, x, 1.5)
    title(ax, "Beam failure recovery: a fast repair inside the cell, without RLF")
    save(fig, "bfr-flow.svg")

# 8. Phase noise PSD and SCS
def pn_psd():
    f = np.logspace(3, 8, 400)
    def psd(fc):  # simple 3-slope model at 3.5 GHz, + 20lg(fc/3.5)
        base = -80 - 10 * np.log10(1 + (f / 1e5) ** 2) - 10 * np.log10(1 + (f / 1e7) ** 1)
        return base + 20 * np.log10(fc / 3.5)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogx(f, psd(3.5), color=ACC, lw=2, label="LO at 3.5 GHz")
    ax.semilogx(f, psd(28), color=ACC2, lw=2, label="same design at 28 GHz (+18 dB)")
    for s, lab in [(30e3, "30 kHz SCS"), (120e3, "120 kHz SCS")]:
        ax.axvline(s, color=MUTED, ls=":"); ax.text(s * 1.08, -75, lab, fontsize=9.5, color=MUTED, rotation=90, va="top")
    ax.set_xlabel("offset from carrier (Hz)"); ax.set_ylabel("phase noise (dBc/Hz)"); ax.legend(loc="lower left")
    title(ax, "Phase noise rises 20·lg(f) with carrier frequency; wider SCS pushes ICI further out")
    save(fig, "pn-psd.svg")

# 9. Constellation with phase noise (simulated)
def pn_const():
    rng = np.random.default_rng(1); N = 1024; nsym = 14
    lv = np.array([-3, -1, 1, 3]) / np.sqrt(10)
    pts, ptsc = [], []
    for s in range(nsym):
        X = rng.choice(lv, N) + 1j * rng.choice(lv, N)
        x = np.fft.ifft(X)
        phi = np.cumsum(rng.normal(0, 0.0035, N)) + rng.normal(0, 0.0) + s * 0.0
        phi += rng.normal(0, 0.18)  # symbol-level drift (CPE)
        Y = np.fft.fft(x * np.exp(1j * phi)) + (rng.normal(0, 0.006, N) + 1j * rng.normal(0, 0.006, N))
        pts.append(Y[:150]); cpe = np.angle(np.sum(Y * np.conj(X))); ptsc.append((Y * np.exp(-1j * cpe))[:150])
    pts, ptsc = np.concatenate(pts), np.concatenate(ptsc)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 4.4))
    for ax, p, t in [(a1, pts, "Before: common rotation (CPE) + blur (ICI)"), (a2, ptsc, "After PT-RS CPE correction: only ICI blur")]:
        ax.scatter(p.real, p.imag, s=3, color=ACC, alpha=0.4, edgecolors="none"); ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
        ax.set_xticks([]); ax.set_yticks([]); title(ax, t, 10.5)
    fig.tight_layout(); save(fig, "pn-constellation.svg")

# 10. PA AM/AM and spectral regrowth (simulated)
def pa():
    rng = np.random.default_rng(2)
    def rapp(x, a=1.0, p=2.0): r = np.abs(x); return x / (1 + (r / a) ** (2 * p)) ** (1 / (2 * p))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    pin = np.linspace(0, 1.8, 300)
    a1.plot(pin, pin, color=MUTED, ls="--", label="ideal linear"); a1.plot(pin, rapp(pin), color=ACC2, lw=2, label="real PA (Rapp model)")
    a1.axvline(0.35, color=TEAL, ls=":"); a1.text(0.37, 1.5, "average\npower", fontsize=9, color=TEAL)
    a1.axvline(0.35 * 10 ** (10 / 20), color=ACC2, ls=":"); a1.text(1.14, 1.35, "peaks\n(+10 dB)", fontsize=9, color=ACC2)
    a1.set_xlabel("input amplitude"); a1.set_ylabel("output amplitude"); a1.legend(loc="lower right"); title(a1, "AM/AM: peaks are squeezed")
    N, os_ = 4096, 4; nsc = 600
    X = np.zeros(N * os_, complex); idx = np.r_[1:nsc // 2 + 1, -nsc // 2:0]
    spec = np.zeros(N * os_)
    for _ in range(40):
        X[:] = 0; X[idx] = (rng.choice([-1, 1], nsc) + 1j * rng.choice([-1, 1], nsc))
        x = np.fft.ifft(X); x = x / np.sqrt(np.mean(np.abs(x) ** 2))
        spec_ideal = np.abs(np.fft.fft(x)) ** 2
        y = rapp(x * 0.35) / 0.35
        spec += np.abs(np.fft.fft(y)) ** 2
        if _ == 0: s0 = spec_ideal
    fr = np.fft.fftshift(np.fft.fftfreq(N * os_)) * os_ * N / nsc
    sm = lambda s: np.convolve(np.fft.fftshift(s), np.ones(64) / 64, "same")
    ref = sm(spec).max()
    a2.plot(fr, db(sm(s0 * 40) / ref + 1e-9), color=MUTED, ls="--", label="ideal")
    a2.plot(fr, db(sm(spec) / ref + 1e-9), color=ACC2, lw=1.5, label="after PA, ~9 dB back-off")
    a2.axvspan(-0.5, 0.5, color=SOFT, zorder=0); a2.axvspan(0.55, 1.55, color=WARM, zorder=0)
    a2.text(0.62, -8, "adjacent\nchannel", fontsize=9, color=ACC2)
    a2.set_xlim(-2, 2); a2.set_ylim(-80, 5); a2.set_xlabel("frequency (channel bandwidths)"); a2.set_ylabel("PSD (dB)"); a2.legend(loc="lower left")
    title(a2, "Compression leaks into the neighbour (ACLR)")
    fig.tight_layout(); save(fig, "pa-regrowth.svg")

# 11. PAPR CCDF: OFDM vs DFT-s-OFDM
def papr():
    rng = np.random.default_rng(4); N, os_, M = 1024, 4, 300
    def sim(dfts, mod):
        out = []
        for _ in range(3000):
            if mod == "q": d = (rng.choice([-1, 1], M) + 1j * rng.choice([-1, 1], M)) / np.sqrt(2)
            else:
                lv = np.array([-3, -1, 1, 3]) / np.sqrt(10); d = rng.choice(lv, M) + 1j * rng.choice(lv, M)
            if dfts: d = np.fft.fft(d) / np.sqrt(M)
            X = np.zeros(N * os_, complex); X[:M] = d
            x = np.fft.ifft(X); p = np.abs(x) ** 2; out.append(db(p.max() / p.mean()))
        return np.sort(out)
    fig, ax = plt.subplots(figsize=(9, 4))
    for dfts, mod, col, lab in [(False, "q", ACC2, "CP-OFDM"), (True, "q", TEAL, "DFT-s-OFDM, QPSK"), (True, "16", ACC, "DFT-s-OFDM, 16QAM")]:
        v = sim(dfts, mod); c = 1 - np.arange(v.size) / v.size
        ax.semilogy(v, c, color=col, lw=2, label=lab)
    ax.set_ylim(1e-3, 1); ax.set_xlim(3, 12); ax.set_xlabel("PAPR (dB)"); ax.set_ylabel("Pr(PAPR > x)"); ax.legend()
    title(ax, "PAPR: DFT-spreading saves the UE several dB of back-off (simulated, 300 subcarriers)")
    save(fig, "papr-ccdf.svg")

# 12. SBFD layout
def sbfd():
    fig, ax = plt.subplots(figsize=(10, 3.4)); ax.grid(False)
    slots = ["D", "S", "SBFD", "SBFD", "SBFD", "S", "U", "D", "SBFD", "U"]
    slots = ["D", "SBFD", "SBFD", "SBFD", "U"] * 2
    for i, s in enumerate(slots):
        if s == "D": ax.add_patch(Rectangle((i, 0), 0.95, 10, facecolor=SOFT, edgecolor=ACC))
        elif s == "U": ax.add_patch(Rectangle((i, 0), 0.95, 10, facecolor=WARM, edgecolor=ACC2))
        else:
            ax.add_patch(Rectangle((i, 0), 0.95, 3.6, facecolor=SOFT, edgecolor=ACC)); ax.add_patch(Rectangle((i, 6.4), 0.95, 3.6, facecolor=SOFT, edgecolor=ACC))
            ax.add_patch(Rectangle((i, 4.0), 0.95, 2.0, facecolor=WARM, edgecolor=ACC2))
            ax.add_patch(Rectangle((i, 3.6), 0.95, 0.4, facecolor=LINE, edgecolor="none")); ax.add_patch(Rectangle((i, 6.0), 0.95, 0.4, facecolor=LINE, edgecolor="none"))
        ax.text(i + 0.47, -0.8, s if s != "SBFD" else "SBFD", ha="center", fontsize=9, color=MUTED)
    ax.text(10.2, 5, "UL sub-band", fontsize=10, color=ACC2, va="center"); ax.text(10.2, 8.2, "DL", fontsize=10, color=ACC, va="center"); ax.text(10.2, 1.8, "DL", fontsize=10, color=ACC, va="center")
    ax.text(10.2, 3.8, "guard", fontsize=8.5, color=MUTED, va="center")
    ax.set_xlim(-0.2, 11.5); ax.set_ylim(-1.4, 10.5); ax.axis("off")
    title(ax, "Sub-band full duplex: uplink in the middle of downlink slots, at the gNB only")
    save(fig, "sbfd-layout.svg")

# 13. Release roadmap
def roadmap():
    rel = [("Rel-15", 2018, 2019.5, "5G NR first"), ("Rel-16", 2019.5, 2020.6, "URLLC, IAB, 2-step RACH"), ("Rel-17", 2020.6, 2022.3, "RedCap, NTN, FR2-2"),
           ("Rel-18", 2022.3, 2024.5, "5G-Advanced: energy, AI/ML study"), ("Rel-19", 2024.5, 2025.9, "SBFD, AI/ML, LTM"), ("Rel-20", 2025.5, 2027.3, "6G study + 5G-A"), ("Rel-21", 2027.0, 2029.0, "first 6G specs")]
    fig, ax = plt.subplots(figsize=(11, 3.6)); ax.grid(axis="y", visible=False)
    for i, (r, a, b, t) in enumerate(rel):
        col = TEAL if i < 3 else (ACC if i < 5 else ACC2)
        ax.barh(i, b - a, left=a, color=col, height=0.6, alpha=0.85)
        ax.text(b + 0.08, i, t, va="center", fontsize=9.5, color=INK)
    ax.set_yticks(range(len(rel))); ax.set_yticklabels([r[0] for r in rel]); ax.invert_yaxis()
    ax.set_xlim(2017.8, 2031.8); ax.set_xlabel("year (approximate; check 3GPP for current dates)")
    title(ax, "3GPP releases: 5G (green), 5G-Advanced (blue), 6G (orange)")
    save(fig, "roadmap.svg")

for fn in [array_gain, polar_beams, grating, architectures, p123, qcl_chain, bfr, pn_psd, pn_const, pa, papr, sbfd, roadmap]:
    fn()
print("ok")
