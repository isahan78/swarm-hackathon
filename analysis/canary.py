"""Canary probe: go/no-go pipeline check on the FIRST batch, before the
pre-registered analysis. Logged in prereg deviations. The AUC here is NOT a
result (single condition, small n) — it answers one question: do the captured
activations carry co-option signal at all?

Split is BY EPISODE (never by step) so no episode leaks across the split.
"""

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

npz_path = sys.argv[1] if len(sys.argv) > 1 else "runs/full/overt_ticket.npz"
d = np.load(npz_path, allow_pickle=True)
X, ep, step, y = d["acts"], d["episode"], d["step"], d["label"]
print(f"{Path(npz_path).name}: {X.shape[0]} step-vectors, dim {X.shape[1]}, "
      f"{len(np.unique(ep))} episodes, co-opted episodes: "
      f"{len(np.unique(ep[y == 1]))}/{len(np.unique(ep))}")

rng = np.random.default_rng(0)
aucs = []
for trial in range(20):  # repeated random episode-level splits (tiny n)
    eps = np.unique(ep)
    co = np.unique(ep[y == 1]); cl = np.unique(ep[y == 0])
    rng.shuffle(co); rng.shuffle(cl)
    n_co_te = max(2, len(co) // 3); n_cl_te = max(2, len(cl) // 3)
    test_eps = set(co[:n_co_te]) | set(cl[:n_cl_te])
    te = np.isin(ep, list(test_eps)); tr = ~te
    sc = StandardScaler().fit(X[tr])
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(sc.transform(X[tr]), y[tr])
    aucs.append(roc_auc_score(y[te], clf.predict_proba(sc.transform(X[te]))[:, 1]))

aucs = np.array(aucs)
print(f"step-level AUC over 20 episode-level splits: "
      f"mean {aucs.mean():.3f}  min {aucs.min():.3f}  max {aucs.max():.3f}")
verdict = "SIGNAL" if aucs.mean() > 0.70 else ("WEAK" if aucs.mean() > 0.60 else "NO SIGNAL")
print(f"CANARY VERDICT: {verdict}")
