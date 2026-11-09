"""Analyze collaborator traces using the exact archived outer train/test split."""
import argparse
import json
from pathlib import Path
from evaluation.collaborator import evaluate_collaborator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--max-fpr', type=float, default=.05)
    parser.add_argument('--bootstrap', type=int, default=200)
    parser.add_argument('--validation-fraction', type=float, default=.2)
    args = parser.parse_args()
    rows = [json.loads(line) for line in Path(args.input).read_text().splitlines() if line.strip()]
    result = evaluate_collaborator(rows, args.output, args.archive, args.input,
        args.seed, args.max_fpr, args.bootstrap, args.validation_fraction)
    print(json.dumps({'output': str(Path(args.output).resolve()), 'outcome': result['outcome_name'],
        'claim_scope': result['claim_scope'], 'coverage': result['coverage']}))


if __name__ == '__main__':
    main()
