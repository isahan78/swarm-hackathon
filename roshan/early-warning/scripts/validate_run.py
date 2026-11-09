"""Check labels and activation alignment before spending time on a larger batch."""
import argparse
import json
from pathlib import Path
import numpy as np
from evaluation.labels import label_completed_episodes
from swarm.io import read_jsonl


def validate_run(directory):
    directory = Path(directory)
    raw = read_jsonl(directory / "decisions.jsonl")
    analysis = read_jsonl(directory / "analysis.jsonl")
    if not raw:
        raise ValueError("No completed decisions")
    if any(row.get("eventual_unauthorized_attempt") is not None for row in raw):
        raise ValueError("Raw decisions contain future outcome labels")
    if label_completed_episodes(raw) != analysis:
        raise ValueError("Offline labels do not match independently recomputed outcomes")
    refs, shapes, timings = [], set(), set()
    for row in raw:
        meta = row.get("activation_metadata", {})
        timings.add(meta.get("timing", "unknown"))
        ref = row.get("activation_ref")
        if ref is None:
            continue
        path = Path(ref)
        if not path.is_absolute():
            path = directory / path
        vector = np.load(path, allow_pickle=False)
        if vector.ndim != 1 or not np.isfinite(vector).all() or not np.any(vector):
            raise ValueError(f"Invalid activation vector: {path}")
        if meta.get("shape") != list(vector.shape):
            raise ValueError("Activation shape disagrees with metadata")
        for key in ("episode_id", "agent_id", "target_step"):
            if key in meta and meta[key] != row[key]:
                raise ValueError(f"Activation belongs to wrong {key}")
        shapes.add(tuple(vector.shape))
        refs.append(str(path.resolve()))
    if len(refs) != len(set(refs)):
        raise ValueError("Activation artifacts reused across decisions")
    return {"n_decisions": len(raw), "n_targets": len({(r['episode_id'], r['agent_id']) for r in raw}),
            "n_activations": len(refs), "shapes": sorted(map(list, shapes)), "timings": sorted(timings),
            "backend_kinds": sorted({r.get('backend_kind', 'unknown') for r in raw}),
            "tool_parse_error_decisions": sum(bool(r.get('inference_metadata', {}).get('tool_parse_errors')) for r in raw),
            "truncated_decisions": sum(bool(r.get('inference_metadata', {}).get('generation_truncated')) for r in raw),
            "labels": "verified_from_complete_episodes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    args = parser.parse_args()
    print(json.dumps(validate_run(args.directory), indent=2))


if __name__ == "__main__":
    main()
