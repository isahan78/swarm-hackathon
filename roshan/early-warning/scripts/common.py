"""Shared CLI configuration; no credentials are read from configuration files."""
from pathlib import Path
import yaml
from swarm.runner import ExperimentConfig


def load_config(path):
    with Path(path).open() as stream:
        config = yaml.safe_load(stream)
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a mapping")
    return config


def experiment_config(config, args):
    settings = dict(config.get("experiment", {}))
    for key in ("run_id", "seed", "steps", "episodes_per_condition"):
        if getattr(args, key, None) is not None:
            settings[key] = getattr(args, key)
    for key in ("conditions", "targets"):
        if getattr(args, key, None):
            settings[key] = tuple(getattr(args, key).split(","))
    return ExperimentConfig(**settings)


def add_arguments(parser, default_config):
    parser.add_argument("--config", default=default_config)
    parser.add_argument("--output", required=True, help="New output directory; existing runs are never overwritten")
    parser.add_argument("--run-id")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--steps", type=int)
    parser.add_argument("--episodes-per-condition", type=int)
    parser.add_argument("--conditions", help="Comma separated clean,direct,delayed,covert subset")
    parser.add_argument("--targets", help="Comma separated B,C,D subset; B gives two-agent smoke test")
