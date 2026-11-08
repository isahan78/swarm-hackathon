"""Recover offline labels from complete episode checkpoints after a failed run."""
import argparse
from evaluation.labels import label_completed_episodes
from swarm.io import read_jsonl, write_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True, help="A new analysis JSONL file")
    args = parser.parse_args()
    rows = read_jsonl(args.input)
    write_jsonl(args.output, label_completed_episodes(rows))
    print(f"Labeled {len(rows)} decisions from completed episode checkpoints.")


if __name__ == "__main__":
    main()
