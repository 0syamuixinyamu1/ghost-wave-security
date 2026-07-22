"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import BenchmarkConfig, run_benchmark
from .config_io import load_benchmark_config
from .simulation import SimulationConfig


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ghost-wave")
    subparsers = parser.add_subparsers(dest="command", required=True)
    benchmark = subparsers.add_parser("benchmark", help="Run the synthetic benchmark")
    benchmark.add_argument("--config", type=Path)
    benchmark.add_argument("--output", type=Path, default=Path("."))
    benchmark.add_argument("--seeds", type=int)
    benchmark.add_argument("--trials", type=int)
    benchmark.add_argument("--steps", type=int)
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command != "benchmark":
        raise AssertionError("Unhandled command")

    if args.config:
        config = load_benchmark_config(args.config, output_directory=args.output)
    else:
        simulation = SimulationConfig(steps=args.steps or 100)
        config = BenchmarkConfig(
            seeds=args.seeds or 5,
            trials_per_seed=args.trials or 100,
            output_directory=args.output,
            simulation=simulation,
        )

    if args.seeds is not None:
        config = BenchmarkConfig(
            seeds=args.seeds,
            trials_per_seed=config.trials_per_seed,
            base_seed=config.base_seed,
            output_directory=config.output_directory,
            simulation=config.simulation,
            strategies=config.strategies,
        )
    if args.trials is not None:
        config = BenchmarkConfig(
            seeds=config.seeds,
            trials_per_seed=args.trials,
            base_seed=config.base_seed,
            output_directory=config.output_directory,
            simulation=config.simulation,
            strategies=config.strategies,
        )
    if args.steps is not None:
        simulation = SimulationConfig(**{**config.simulation.__dict__, "steps": args.steps})
        config = BenchmarkConfig(
            seeds=config.seeds,
            trials_per_seed=config.trials_per_seed,
            base_seed=config.base_seed,
            output_directory=config.output_directory,
            simulation=simulation,
            strategies=config.strategies,
        )

    _, summaries = run_benchmark(config)
    for row in summaries:
        print(
            f"{row['strategy']}: compromise={row['shell_compromise_rate_mean']:.3f}, "
            f"core={row['core_breached_mean']:.3f}, "
            f"cost={row['total_operational_cost_mean']:.1f}"
        )


if __name__ == "__main__":
    main()
