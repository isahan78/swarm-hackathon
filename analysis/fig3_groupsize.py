"""Figure 3: per-recipient co-opt rate vs group size (Qwen3-8B, pod data).

Points: N=1 (2-agent overt, 20/30), N=3 (pooled broadcast+personal, 8/72),
N=10 (0/80). Wilson 95% intervals; log-ish x spacing via categorical axis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


DATA = [("1", 20, 30), ("3", 8, 72), ("10", 0, 80)]
INK, MUTED, ACCENT = "#1f2430", "#8a8f98", "#3b6ea5"

fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=200)
xs = range(len(DATA))
for x, (label, k, n) in zip(xs, DATA):
    p = k / n
    lo, hi = wilson(k, n)
    ax.errorbar(x, p, yerr=[[p - lo], [hi - p]], fmt="o", color=ACCENT, ms=8,
                capsize=4, elinewidth=1.6, zorder=3)
    ax.annotate(f"{k}/{n}", (x, p), xytext=(12, 4), textcoords="offset points",
                fontsize=9.5, color=INK, fontweight="bold")
ax.plot(list(xs), [k / n for _, k, n in DATA], color=ACCENT, lw=1.2,
        alpha=0.5, zorder=2)
ax.set_xticks(list(xs))
ax.set_xticklabels([f"N = {d[0]}" for d in DATA], fontsize=10.5)
ax.set_ylim(-0.03, 0.85)
ax.set_xlim(-0.4, 2.5)
ax.set_ylabel("Per-recipient co-opt rate", fontsize=10)
ax.set_title("Recruitment collapses with group size\n"
             "(overt ask, ticket tier; Wilson 95% intervals)",
             fontsize=10.5, loc="left", color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
ax.tick_params(colors=INK, labelsize=9)
ax.grid(axis="y", color="#e5e7eb", lw=0.7, zorder=0)
ax.set_axisbelow(True)

out = Path(__file__).resolve().parent.parent / "figures"
fig.tight_layout()
fig.savefig(out / "fig3_groupsize.png", bbox_inches="tight")
fig.savefig(out / "fig3_groupsize.pdf", bbox_inches="tight")
print("wrote figures/fig3_groupsize.{png,pdf}")
