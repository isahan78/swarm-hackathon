"""Run a real model on an already authorized independent GPU environment."""
import argparse
from scripts.common import add_arguments, experiment_config, load_config
from swarm.backends.qwen import QwenBackend
from swarm.runner import run_experiment
from monitoring.transcript_monitor import TranscriptMonitor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser, "configs/qwen.yaml")
    parser.add_argument("--llm-monitor", action="store_true", help="Score sanitized transcripts using the same loaded model in independent calls")
    args = parser.parse_args()
    settings = load_config(args.config)
    backend = QwenBackend(**settings.get("backend", {}))
    config = experiment_config(settings, args)
    monitor = TranscriptMonitor(backend, seed=config.seed) if args.llm_monitor else None
    rows = run_experiment(backend, args.output, config, transcript_monitor=monitor)
    print(f"Real Qwen: {len(rows)} decision records written to {args.output}; validate files before scaling.")


if __name__ == "__main__":
    main()
