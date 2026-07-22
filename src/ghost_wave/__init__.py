"""Ghost Wave Security: a benign synthetic recovery simulator."""

from .benchmark import BenchmarkConfig, run_benchmark
from .simulation import SimulationConfig, Strategy, run_trial

__all__ = [
    "BenchmarkConfig",
    "SimulationConfig",
    "Strategy",
    "run_benchmark",
    "run_trial",
]

__version__ = "0.1.0"
