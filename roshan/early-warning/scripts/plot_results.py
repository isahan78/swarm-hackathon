"""Render research figures from an evaluation artifact."""
import argparse
import json
from pathlib import Path

from evaluation.plots import plot_results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-mock", action="store_true", help="Watermark mock software-validation figures")
    args = parser.parse_args()
    result = json.loads(args.input.read_text())
    for path in plot_results(result, args.output, allow_mock=args.allow_mock):
        print(path)


if __name__ == "__main__":
    main()
