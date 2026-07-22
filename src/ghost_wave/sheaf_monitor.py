"""A small sheaf-inspired local-to-global consistency monitor.

This module intentionally implements only a finite graph diagnostic. It should
not be described as persistent sheaf cohomology.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Edge:
    left: int
    right: int


DEFAULT_EDGES: tuple[Edge, ...] = (
    Edge(0, 1),
    Edge(1, 2),
    Edge(2, 3),
    Edge(3, 4),
    Edge(4, 5),
    Edge(5, 6),
    Edge(6, 7),
    Edge(7, 0),
    Edge(0, 4),
    Edge(2, 6),
    Edge(1, 5),
    Edge(3, 7),
)


class SheafCoherenceMonitor:
    """Compute a projected edge inconsistency energy.

    Each service carries a local state [risk, anomaly, privilege drift]. Each
    dependency edge compares a deterministic two-dimensional projection of its
    endpoint states. Identical endpoint states have zero residual.
    """

    def __init__(self, edges: Iterable[Edge] = DEFAULT_EDGES) -> None:
        self.edges = tuple(edges)
        self.restriction = np.asarray(
            [
                [1.0, 0.0, 0.0],
                [0.0, 0.65, 0.35],
            ],
            dtype=float,
        )

    def gluing_energy(self, local_states: np.ndarray) -> float:
        if local_states.ndim != 2 or local_states.shape[1] != 3:
            raise ValueError("local_states must have shape (n_services, 3)")
        if not self.edges:
            return 0.0
        residuals = []
        for edge in self.edges:
            left = self.restriction @ local_states[edge.left]
            right = self.restriction @ local_states[edge.right]
            residuals.append(float(np.dot(left - right, left - right)))
        return float(np.mean(residuals))

    def normalized_inconsistency(self, local_states: np.ndarray) -> float:
        energy = self.gluing_energy(local_states)
        return float(energy / (1.0 + energy))

    def neighbors(self, node_count: int) -> dict[int, list[int]]:
        result = {index: [] for index in range(node_count)}
        for edge in self.edges:
            result[edge.left].append(edge.right)
            result[edge.right].append(edge.left)
        return result
