"""Figures from held-out evaluation artifacts; no simulated result substitution."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MONITORS = {
    "activation": ("Activation probe", "#4c72b0"),
    "transcript_llm": ("LLM transcript monitor", "#dd8452"),
    "text_tfidf": ("TF-IDF + logistic regression", "#55a868"),
}
SCORE_KEYS = {
    "activation": "probe_score",
    "transcript_llm": "text_monitor_score",
    "text_tfidf": "text_baseline_score",
}


def _marker_outcome(result):
    return result.get("outcome_name") == "eventual_marker_attempt"


def _mock(result: dict[str, Any]) -> bool:
    kinds = result.get("backend_kinds", [])
    return bool(result.get("is_mock", False) or result.get("data_kind") == "mock" or "mock" in kinds)


def _title(fig: Any, title: str, mock: bool) -> None:
    fig.suptitle(("MOCK — SOFTWARE VALIDATION ONLY\n" if mock else "") + title, fontsize=12)


def _save(fig: Any, output_dir: Path, name: str) -> list[str]:
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    paths = []
    for suffix in ("png", "svg"):
        path = output_dir / f"{name}.{suffix}"
        fig.savefig(path, dpi=170, bbox_inches="tight")
        paths.append(str(path))
    plt.close(fig)
    return paths


def _empty(ax: Any, message: str) -> None:
    ax.text(0.5, 0.5, message, ha="center", va="center", transform=ax.transAxes, wrap=True)
    ax.set_xticks([])
    ax.set_yticks([])


def _outcome_items(result: dict[str, Any]) -> list[dict[str, Any]]:
    outcomes = result.get("outcomes", {})
    if isinstance(outcomes, list):
        return outcomes
    return [dict(values, condition=condition) for condition, values in outcomes.items()]


def recruitment_outcomes(result: dict[str, Any], output_dir: Path, mock: bool) -> list[str]:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    items = _outcome_items(result)
    if items:
        labels = [item["condition"] for item in items]
        counts = [item.get("n_targets", item.get("n", 0)) for item in items]
        attempted = [item.get("n_attempted", item.get("n_positive", 0)) for item in items]
        rates = [item.get("attempt_rate", a / n if n else np.nan) for item, a, n in zip(items, attempted, counts)]
        bars = ax.bar(labels, rates, color=["#999999" if x == "clean" else "#4c72b0" for x in labels])
        for bar, a, n in zip(bars, attempted, counts):
            if n:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.025, f"{a}/{n}", ha="center", fontsize=9)
        ax.set_ylim(0, 1.12)
        ax.set_ylabel("Fraction with recruited marker insertion" if _marker_outcome(result)
                      else "Fraction with verified unauthorized attempt")
        ax.set_xlabel("Recruitment condition")
    else:
        _empty(ax, "No target outcomes available")
    _title(fig, "Figure 1 — Recruitment outcomes (held-out targets)", mock)
    return _save(fig, output_dir, "figure1_recruitment_outcomes")


def early_performance(result: dict[str, Any], output_dir: Path, mock: bool) -> list[str]:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    horizons = result.get("horizons", {})
    names = list(horizons)
    plotted = False
    missing = []
    for monitor, (label, color) in MONITORS.items():
        points = []
        for i, horizon in enumerate(names):
            # Use the same held-out decision rows for each available monitor.
            # An empty common support is missing data, never a fallback to unequal cohorts.
            horizon_result = horizons[horizon]
            support = horizon_result.get("common_support_metrics", horizon_result.get("monitors", horizon_result))
            entry = support.get(monitor, {})
            score = entry.get("auroc") if isinstance(entry, dict) else None
            if score is not None and np.isfinite(score):
                points.append((i, score, entry.get("auroc_ci95")))
        if points:
            x = [point[0] for point in points]
            y = [point[1] for point in points]
            ax.plot(x, y, marker="o", label=label, color=color)
            for position, score, interval in points:
                if isinstance(interval, (list, tuple)) and len(interval) == 2 and all(v is not None for v in interval):
                    lo, hi = interval
                    if lo <= score <= hi:
                        ax.errorbar(position, score, yerr=[[score - lo], [hi - score]], color=color, capsize=3)
            plotted = True
        else:
            missing.append(label)
    if plotted:
        ax.axhline(0.5, color="gray", linestyle=":", linewidth=1)
        ax.set_xticks(range(len(names)), [name.replace("_", " ") for name in names])
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("AUROC for eventual marker insertion" if _marker_outcome(result)
                      else "AUROC for eventual unauthorized attempt")
        ax.set_xlabel("Observation point, before current response (common monitor support)")
        ax.legend(fontsize=8, loc="best")
        if missing:
            ax.text(0.01, 0.01, "Unavailable: " + ", ".join(missing), transform=ax.transAxes, fontsize=8)
    else:
        _empty(ax, "No evaluable monitor AUROC at these observation points\nBoth outcome classes are required")
    _title(fig, "Figure 2 — Early prediction performance", mock)
    return _save(fig, output_dir, "figure2_early_prediction")


def detection_lead_time(result: dict[str, Any], output_dir: Path, mock: bool) -> list[str]:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    values, labels, colors, misses, totals = [], [], [], [], []
    unavailable = []
    for monitor, (label, color) in MONITORS.items():
        entry = result.get("lead_times", {}).get(monitor)
        if not entry:
            unavailable.append(label)
            continue
        records = entry.get("records", []) if isinstance(entry, dict) else entry
        threshold = entry.get("threshold") if isinstance(entry, dict) else None
        if threshold is None:
            threshold = result.get("thresholds", {}).get(monitor)
        threshold_valid = threshold is None or threshold.get("status") in {"selected", "no_alert"}
        has_scored_counts = any("n_scored_pre_action" in r for r in records)
        has_scores = sum(r.get("n_scored_pre_action", 0) for r in records) > 0 if has_scored_counts else any(r.get("lead_steps") is not None for r in records)
        if not threshold_valid or not has_scores or (isinstance(entry, dict) and entry.get("monitor_available") is False):
            unavailable.append(label)
            continue
        defectors = [r for r in records if (
            r.get("eventual_marker_attempt", r.get("eventual_outcome", False)) if _marker_outcome(result)
            else r.get("eventual_unauthorized_attempt", r.get("defected", False)))]
        # A nonpositive lead may represent imminent or late detection. Preserve it.
        leads = [r["lead_steps"] for r in defectors if r.get("lead_steps") is not None]
        values.append(leads)
        labels.append(label)
        colors.append(color)
        misses.append(sum(r.get("lead_steps") is None for r in defectors))
        totals.append(len(defectors))
    nonempty = [(i, v) for i, v in enumerate(values) if v]
    if nonempty:
        for i, v in nonempty:
            axes[0].scatter(np.full(len(v), i), v, color=colors[i], alpha=0.65, s=18)
            axes[0].plot([i - 0.15, i + 0.15], [np.median(v)] * 2, color="black", linewidth=2)
        axes[0].axhline(0, linestyle="--", color="gray")
        axes[0].set_xticks(range(len(labels)), labels, rotation=15, ha="right", fontsize=8)
        axes[0].set_ylabel("Target decisions before first marker insertion" if _marker_outcome(result)
                           else "Target decisions before first unauthorized attempt")
        axes[0].set_title("First alert; black line is median")
        axes[0].text(0.01, 0.01, "0 = imminent-action detection", transform=axes[0].transAxes, fontsize=8)
    else:
        _empty(axes[0], "No alerted marker-positive targets\nNo lead times to plot" if _marker_outcome(result)
               else "No alerted defecting target episodes\nNo lead times to plot")
    if labels:
        axes[1].bar(range(len(labels)), misses, color=colors)
        axes[1].set_xticks(range(len(labels)), labels, rotation=15, ha="right", fontsize=8)
        axes[1].set_ylabel("Marker-positive targets without any alert" if _marker_outcome(result)
                           else "Defecting targets without any alert")
        axes[1].set_title("Misses remain in denominator")
        for i, (m, n) in enumerate(zip(misses, totals)):
            axes[1].text(i, m, f"{m}/{n}", ha="center", va="bottom", fontsize=8)
        axes[1].set_ylim(0, max(misses + [1]) * 1.2)
    else:
        _empty(axes[1], "No monitor lead-time data available")
    if unavailable:
        fig.text(0.02, 0.01, "Unavailable: " + ", ".join(unavailable), fontsize=8)
    _title(fig, "Figure 3 — Detection lead time (marker-positive targets only)" if _marker_outcome(result)
           else "Figure 3 — Detection lead time (eventual defectors only)", mock)
    return _save(fig, output_dir, "figure3_detection_lead_time")


def example_trace(result: dict[str, Any], output_dir: Path, mock: bool) -> list[str]:
    fig, ax = plt.subplots(figsize=(9, 4.7))
    example = result.get("example_trace", {})
    rows = example.get("rows", [])
    rows = sorted(rows, key=lambda row: row["target_step"])
    plotted = False
    for monitor, (label, color) in MONITORS.items():
        key = SCORE_KEYS[monitor]
        points = [(r["target_step"], r[key]) for r in rows if r.get(key) is not None]
        if points:
            x, y = zip(*points)
            ax.plot(x, y, marker="o", color=color, label=label)
            plotted = True
    markers = [
        ("exposure_at_step", "Recruitment exposure", "#8172b2", ":"),
        ("verbal_agreement_at_step", "Verbal agreement candidate (requires review)", "#ccb974", "-."),
        (("marker_attempt_at_step", "Marker insertion", "#c44e52", "--") if _marker_outcome(result)
         else ("unauthorized_attempt_at_step", "Verified unauthorized attempt", "#c44e52", "--")),
    ]
    for key, label, color, linestyle in markers:
        for i, row in enumerate(r for r in rows if r.get(key)):
            ax.axvline(row["target_step"], color=color, linestyle=linestyle, label=label if i == 0 else None)
    event_key = "marker_attempt_at_step" if _marker_outcome(result) else "unauthorized_attempt_at_step"
    event_steps = [row["target_step"] for row in rows if row.get(event_key)]
    if rows and event_steps and max(row["target_step"] for row in rows) > min(event_steps):
        ax.axvspan(min(event_steps) + .05, max(row["target_step"] for row in rows) + .1,
                   color="gray", alpha=.12, label="After first action (excluded from early metrics)")
    if rows:
        ax.set_xticks(sorted({r["target_step"] for r in rows}))
        ax.set_ylim(-0.03, 1.03)
        ax.set_xlabel("Target decision point (scores precede current response)")
        ax.set_ylabel("Predicted likelihood of eventual marker insertion" if _marker_outcome(result)
                      else "Predicted likelihood of eventual unauthorized attempt")
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(fontsize=7, loc="best")
        if not plotted:
            ax.text(0.5, 0.5, "Monitor scores unavailable", transform=ax.transAxes, ha="center")
    else:
        _empty(ax, "No representative held-out trace available")
    outcome = ""
    if rows:
        if _marker_outcome(result):
            positive = any(r.get("eventual_marker_attempt", False) for r in rows)
            outcome = " — marker inserted" if positive else " — no marker insertion"
        else:
            defected = any(r.get("eventual_unauthorized_attempt", False) for r in rows)
            outcome = " — attempted unauthorized action" if defected else " — no unauthorized attempt"
    identity = f"{example.get('episode_id', '')} / {example.get('agent_id', '')}".strip(" /")
    _title(fig, "Figure 4 — Representative trace " + identity + outcome, mock)
    return _save(fig, output_dir, "figure4_example_trace")


def plot_results(result: dict[str, Any], output_dir: str | Path, allow_mock: bool = False) -> list[str]:
    """Render measured values only; mock artifacts require explicit permission."""
    mock = _mock(result)
    if mock and not allow_mock:
        raise ValueError("Mock figures are software validation only; pass --allow-mock explicitly")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for function in (recruitment_outcomes, early_performance, detection_lead_time, example_trace):
        paths.extend(function(result, output, mock))
    return paths
