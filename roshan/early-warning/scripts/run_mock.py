"""Synthetic end-to-end software validation, never research measurements."""
import argparse
from scripts.common import add_arguments, experiment_config, load_config
from swarm.backends.mock import MockBackend
from swarm.runner import run_experiment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser, "configs/mock.yaml")
    args = parser.parse_args()
    config = experiment_config(load_config(args.config), args)
    rows = run_experiment(MockBackend(), args.output, config)
    print(f"MOCK — SOFTWARE VALIDATION ONLY: {len(rows)} decision records written to {args.output}")


if __name__ == "__main__":
    main()
