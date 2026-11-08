"""Figure 1: pre-action probe AUC by condition, over 50 random episode splits.

Dot = mean, whisker = +/- 1 sd, faint dots = individual splits. Chance at 0.5.
Writes figures/fig1_probe_auc.png (+ .pdf).
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

root = Path(__file__).resolve().parent.parent
CONDITIONS = ["overt", "latent", "hidden", "control"]

marker_step = {}
for c in CONDITIONS:
    for line in open(root / "runs/full" / f"{c}_ticket.jsonl"):
        r = json.loads(line)
        marker_step[(c, r["episode"])] = r["marker_step"]

X, cond, ep, step, y = [], [], [], [], []
for c in CONDITIONS:
    d = np.load(root / "runs/full" / f"{c}_ticket.npz", allow_pickle=True)
    X.append(d["acts"]); cond += [c] * len(d["step"])
    ep.append(d["episode"]); step.append(d["step"]); y.append(d["label"])
X = np.concatenate(X); cond = np.array(cond)
ep = np.concatenate(ep); step = np.concatenate(step); y = np.concatenate(y)
ms = np.array([marker_step[(c, e)] for c, e in zip(cond, ep)])
pre = (ms < 0) | (step <= ms)

rng = np.random.default_rng(1)
PLOT_CONDS = ["overt", "latent", "hidden"]
aucs = {c: [] for c in PLOT_CONDS}
for trial in range(50):
    test_pairs = set()
    for c in CONDITIONS:
        for lab in (0, 1):
            eps_cl = np.array(sorted({e for e in ep[(cond == c) & (y == lab)]}))
            if len(eps_cl) == 0:
                continue
            rng.shuffle(eps_cl)
            for e in eps_cl[:max(1, round(len(eps_cl) * 0.3))]:
                test_pairs.add((c, int(e)))
    in_te = np.array([(c, int(e)) in test_pairs for c, e in zip(cond, ep)])
    tr = ~in_te & pre
    sc = StandardScaler().fit(X[tr])
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(sc.transform(X[tr]), y[tr])
    s = clf.predict_proba(sc.transform(X))[:, 1]
    for c in PLOT_CONDS:
        m = (cond == c) & in_te & pre
        eps_te = sorted({int(e) for e in ep[m]})
        es = [s[m & (ep == e)].max() for e in eps_te]
        el = [int(y[m & (ep == e)][0]) for e in eps_te]
        if len(set(el)) > 1:
            aucs[c].append(roc_auc_score(el, es))

INK = "#1f2430"
MUTED = "#8a8f98"
ACCENT = "#3b6ea5"

fig, ax = plt.subplots(figsize=(5.2, 3.6), dpi=200)
rj = np.random.default_rng(7)
for i, c in enumerate(PLOT_CONDS):
    a = np.array(aucs[c])
    jx = i + rj.uniform(-0.10, 0.10, len(a))
    ax.scatter(jx, a, s=10, color=MUTED, alpha=0.35, linewidths=0, zorder=2)
    ax.errorbar(i, a.mean(), yerr=a.std(), fmt="o", color=ACCENT, ms=7,
                capsize=4, elinewidth=1.6, zorder=3)
    ax.annotate(f"{a.mean():.2f}", (i, a.mean()), xytext=(14, 0),
                textcoords="offset points", va="center", fontsize=10,
                color=INK, fontweight="bold")

ax.axhline(0.5, ls="--", lw=1, color=MUTED, zorder=1)
ax.annotate("chance", (2.42, 0.5), va="bottom", ha="right", fontsize=8.5,
            color=MUTED)
ax.set_xticks(range(len(PLOT_CONDS)))
ax.set_xticklabels([c.capitalize() for c in PLOT_CONDS], fontsize=10.5)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(0.0, 1.05)
ax.set_ylabel("Episode-level AUC (pre-action)", fontsize=10)
ax.set_title("Probe reads the co-option decision before any action\n"
             "(Dev-B layer-18 prefill; 50 episode-level splits)",
             fontsize=10.5, loc="left", color=INK)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"):
    ax.spines[s_].set_color(MUTED)
ax.tick_params(colors=INK, labelsize=9)
ax.grid(axis="y", color="#e5e7eb", lw=0.7, zorder=0)
ax.set_axisbelow(True)

out = root / "figures"
out.mkdir(exist_ok=True)
fig.tight_layout()
fig.savefig(out / "fig1_probe_auc.png", bbox_inches="tight")
fig.savefig(out / "fig1_probe_auc.pdf", bbox_inches="tight")
print("wrote figures/fig1_probe_auc.{png,pdf}")
for c in PLOT_CONDS:
    a = np.array(aucs[c])
    print(f"  {c:8s} {a.mean():.3f} ± {a.std():.3f}")
