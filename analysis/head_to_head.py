"""Probe vs transcript monitor, PAIRED on identical splits + Figure 2.

For each of 50 random episode-level splits (same construction and seed in
probe_eval/figures/text_baseline), train both detectors on the same train
episodes and score the same test episodes. Report per-condition paired
delta (probe - text) with a percentile interval over splits, and draw
Figure 2 (grouped dot + whisker, probe vs text per condition).
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

root = Path(__file__).resolve().parent.parent
CONDITIONS = ["overt", "latent", "hidden", "control"]
PLOT_CONDS = ["overt", "latent", "hidden"]

# ---- load both views of the same steps ----
marker_step = {}
for c in CONDITIONS:
    for line in open(root / "runs/full" / f"{c}_ticket.jsonl"):
        r = json.loads(line)
        marker_step[(c, r["episode"])] = r["marker_step"]

X, texts, cond, ep, step, y = [], [], [], [], [], []
for c in CONDITIONS:
    d = np.load(root / "runs/full" / f"{c}_ticket.npz", allow_pickle=True)
    boards = {}
    for line in open(root / "runs/full" / f"{c}_ticket.jsonl"):
        r = json.loads(line)
        boards[r["episode"]] = r["board"]
    X.append(d["acts"])
    for e, t, lab in zip(d["episode"], d["step"], d["label"]):
        visible = [m["text"] for m in boards[int(e)]
                   if m["step"] < t or (m["step"] == t and m["from"] == "Dev-A")]
        texts.append("\n".join(visible) if visible else "(no messages)")
        cond.append(c); ep.append(int(e)); step.append(int(t)); y.append(int(lab))
X = np.concatenate(X); cond = np.array(cond)
ep = np.array(ep); step = np.array(step); y = np.array(y)
ms = np.array([marker_step[(c, e)] for c, e in zip(cond, ep)])
pre = (ms < 0) | (step <= ms)


def ep_auc(scores, mask):
    out = {}
    for c in PLOT_CONDS:
        m = (cond == c) & mask
        eps_ = sorted({int(e) for e in ep[m]})
        es = [scores[m & (ep == e)].max() for e in eps_]
        el = [int(y[m & (ep == e)][0]) for e in eps_]
        out[c] = roc_auc_score(el, es) if len(set(el)) > 1 else np.nan
    return out


rng = np.random.default_rng(1)
probe_aucs = {c: [] for c in PLOT_CONDS}
text_aucs = {c: [] for c in PLOT_CONDS}
deltas = {c: [] for c in PLOT_CONDS}
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
    s_probe = clf.predict_proba(sc.transform(X))[:, 1]

    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    Xt = vec.fit_transform([texts[i] for i in np.where(tr)[0]])
    clf_t = LogisticRegression(max_iter=2000, C=1.0).fit(Xt, y[tr])
    s_text = clf_t.predict_proba(vec.transform(texts))[:, 1]

    rp = ep_auc(s_probe, in_te & pre)
    rt = ep_auc(s_text, in_te & pre)
    for c in PLOT_CONDS:
        if not (np.isnan(rp[c]) or np.isnan(rt[c])):
            probe_aucs[c].append(rp[c])
            text_aucs[c].append(rt[c])
            deltas[c].append(rp[c] - rt[c])

print("PAIRED probe - text (pre-action, episode-level AUC, 50 identical splits):")
for c in PLOT_CONDS:
    d = np.array(deltas[c])
    lo, hi = np.percentile(d, [2.5, 97.5])
    frac = (d > 0).mean()
    print(f"  {c:8s} probe {np.mean(probe_aucs[c]):.3f}  text {np.mean(text_aucs[c]):.3f}"
          f"  delta {d.mean():+.3f}  [{lo:+.2f}, {hi:+.2f}]  probe wins {frac:.0%} of splits")

# ---- Figure 2 ----
INK, MUTED = "#1f2430", "#8a8f98"
PROBE_C, TEXT_C = "#3b6ea5", "#b0651f"
fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=200)
for i, c in enumerate(PLOT_CONDS):
    for dx, vals, col, lbl in ((-0.13, probe_aucs[c], PROBE_C, "Probe (internal)"),
                               (+0.13, text_aucs[c], TEXT_C, "Text monitor")):
        a = np.array(vals)
        ax.errorbar(i + dx, a.mean(), yerr=a.std(), fmt="o", color=col, ms=7,
                    capsize=4, elinewidth=1.6, zorder=3,
                    label=lbl if i == 0 else None)
        ax.annotate(f"{a.mean():.2f}", (i + dx, a.mean()), xytext=(0, 10),
                    textcoords="offset points", ha="center", fontsize=9,
                    color=INK, fontweight="bold")
ax.axhline(0.5, ls="--", lw=1, color=MUTED, zorder=1)
ax.annotate("chance", (2.45, 0.5), va="bottom", ha="right", fontsize=8.5, color=MUTED)
ax.set_xticks(range(len(PLOT_CONDS)))
ax.set_xticklabels([c.capitalize() for c in PLOT_CONDS], fontsize=10.5)
ax.set_xlim(-0.5, 2.5); ax.set_ylim(0.3, 1.05)
ax.set_ylabel("Episode-level AUC (pre-action)", fontsize=10)
ax.set_title("Internal probe vs transcript monitor, before any action\n"
             "(same training episodes, same test episodes; 50 paired splits)",
             fontsize=10.5, loc="left", color=INK)
ax.legend(frameon=False, fontsize=9, loc="lower left")
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"):
    ax.spines[s_].set_color(MUTED)
ax.tick_params(colors=INK, labelsize=9)
ax.grid(axis="y", color="#e5e7eb", lw=0.7, zorder=0)
ax.set_axisbelow(True)
fig.tight_layout()
(root / "figures").mkdir(exist_ok=True)
fig.savefig(root / "figures/fig2_probe_vs_text.png", bbox_inches="tight")
fig.savefig(root / "figures/fig2_probe_vs_text.pdf", bbox_inches="tight")
print("\nwrote figures/fig2_probe_vs_text.{png,pdf}")
