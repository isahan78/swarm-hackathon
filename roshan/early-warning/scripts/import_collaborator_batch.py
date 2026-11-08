"""Normalize the four supplied batches without changing the source or split."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from scripts.import_collaborator import import_export
from swarm.io import write_jsonl


def import_batch(archive, output, dataset_kind):
    archive, output = Path(archive).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    combined, batches = [], []
    for condition in ("overt", "latent", "hidden", "control"):
        folder = output / condition
        rows = import_export(
            archive / "runs/full" / f"{condition}_ticket.jsonl",
            archive / "runs/full" / f"{condition}_ticket.npz", archive, folder,
            dataset_kind=dataset_kind, batch_id="isahan_" + condition, decoder_layer=18)
        for row in rows:
            row["activation_ref"] = str(Path(condition) / row["activation_ref"])
        combined.extend(rows)
        batches.append(json.loads((folder / "run_metadata.json").read_text()))
    write_jsonl(output / "analysis.jsonl", combined)
    split = archive / "runs/split.json"
    shutil.copyfile(split, output / "frozen_split.json")
    metadata = {
        "adapter": "four-condition-batch-v1", "dataset_kind": dataset_kind,
        "source_split_sha256": hashlib.sha256(split.read_bytes()).hexdigest(),
        "batches": batches, "n_decisions": len(combined),
        "n_episodes": len({row["episode_id"] for row in combined}),
        "verified_unauthorized_attempts": sum(row["unauthorized_attempt_at_step"] for row in combined),
        "marker_positive_episodes": sum(row["eventual_marker_attempt"] for row in combined if row["target_step"] == 1),
        "dataset_semantics": sorted({row["dataset_semantics"] for row in combined}),
        "authorization_rule": batches[0]["actual_authorization_rule"],
        "future_label_note": "Combined analysis is offline; per-condition decisions.jsonl retains null future labels.",
    }
    (output / "source_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dataset-kind", choices=("real", "mock"), required=True)
    args = parser.parse_args()
    result = import_batch(args.archive, args.output, args.dataset_kind)
    print(json.dumps({key: result[key] for key in ("n_episodes", "n_decisions", "marker_positive_episodes", "verified_unauthorized_attempts")}))


if __name__ == "__main__":
    main()
