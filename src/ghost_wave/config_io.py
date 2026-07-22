"""TOML configuration loading."""

from __future__ import annotations

import tomllib
from pathlib import Path

from .benchmark import BenchmarkConfig, DEFAULT_STRATEGIES
from .simulation import SimulationConfig
from .strategies import Strategy


def load_benchmark_config(path: Path, output_directory: Path | None = None) -> BenchmarkConfig:
    with path.open("rb") as handle:
        data = tomllib.load(handle)

    benchmark_data = data.get("benchmark", {})
    simulation_data = data.get("simulation", {})
    strategy_names = benchmark_data.get(
        "strategies", [strategy.value for strategy in DEFAULT_STRATEGIES]
    )
    strategies = tuple(Strategy(name) for name in strategy_names)
    simulation = SimulationConfig(**simulation_data)
    return BenchmarkConfig(
        seeds=int(benchmark_data.get("seeds", 5)),
        trials_per_seed=int(benchmark_data.get("trials_per_seed", 100)),
        base_seed=int(benchmark_data.get("base_seed", 20260722)),
        output_directory=output_directory or Path(benchmark_data.get("output_directory", ".")),
        simulation=simulation,
        strategies=strategies,
    )
