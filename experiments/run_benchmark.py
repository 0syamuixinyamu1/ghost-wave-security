#!/usr/bin/env python3
"""Repository-local benchmark entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from ghost_wave.benchmark import run_benchmark
from ghost_wave.config_io import load_benchmark_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/configs/default.toml"),
    )
    parser.add_argument("--output", type=Path, default=Path("."))
    args = parser.parse_args()
    config = load_benchmark_config(args.config, output_directory=args.output)
    _, summaries = run_benchmark(config)
    for row in summaries:
        print(row)


if __name__ == "__main__":
    main()
