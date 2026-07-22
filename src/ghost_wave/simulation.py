"""Synthetic defensive recovery simulation.

The simulator contains no network interaction or exploit logic. All compromise
and recovery events are abstract stochastic state transitions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .sheaf_monitor import DEFAULT_EDGES, SheafCoherenceMonitor
from .strategies import Strategy, codebook_for_strategy, cosine_similarity, recover_shell


@dataclass(frozen=True)
class SimulationConfig:
    steps: int = 100
    node_count: int = 8
    recovery_threshold: float = 0.46
    recovery_cost: float = 2.5
    exposure_cost_per_compromised_service: float = 0.08
    core_hazard_scale: float = 0.008
    core_breach_penalty: float = 100.0
    attacker_adaptation: float = 0.10
    attacker_noise: float = 0.035
    defender_estimate_rate: float = 0.18
    defender_noise: float = 0.20
    lateral_movement_scale: float = 0.09


@dataclass(frozen=True)
class TrialResult:
    strategy: str
    seed: int
    shell_compromise_rate: float
    core_breached: int
    recovery_downtime: float
    compromise_exposure_cost: float
    total_operational_cost: float
    recovery_count: int
    mean_collapse_index: float
    reinfections: int
    mean_gluing_inconsistency: float


def _unit(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm <= 1e-12:
        raise ValueError("Cannot normalize a zero vector")
    return vector / norm


def _local_states(
    compromised: np.ndarray,
    anomaly: np.ndarray,
    privilege_drift: np.ndarray,
) -> np.ndarray:
    return np.column_stack(
        [compromised.astype(float), np.clip(anomaly, 0.0, 1.0), np.clip(privilege_drift, 0.0, 1.0)]
    )


def run_trial(
    strategy: Strategy,
    seed: int,
    config: SimulationConfig = SimulationConfig(),
) -> TrialResult:
    if config.node_count != 8:
        raise ValueError("The current codebooks and graph require node_count=8")

    rng = np.random.default_rng(seed)
    monitor = SheafCoherenceMonitor(DEFAULT_EDGES)
    neighbors = monitor.neighbors(config.node_count)
    codebook = codebook_for_strategy(strategy, seed=seed + 1_000_003)

    baseline_shell = codebook[0].copy()
    shell = baseline_shell.copy()
    hidden_attacker = _unit(shell + rng.normal(0.0, 0.18, size=8))
    defender_estimate = _unit(rng.normal(size=8))

    compromised = np.zeros(config.node_count, dtype=bool)
    anomaly = np.zeros(config.node_count, dtype=float)
    privilege_drift = np.zeros(config.node_count, dtype=float)
    persistence_age = np.zeros(config.node_count, dtype=int)
    critical_nodes = np.asarray([1, 2, 4], dtype=int)

    recent_shells = [shell.copy()]
    last_recovery_step: int | None = None
    core_breached = 0
    recovery_count = 0
    reinfections = 0
    recovery_downtime = 0.0
    compromise_exposure_cost = 0.0
    compromise_sum = 0.0
    collapse_values: list[float] = []
    gluing_values: list[float] = []

    for step in range(config.steps):
        # Hidden attacker adapts to the currently exposed shell.
        hidden_attacker = _unit(
            (1.0 - config.attacker_adaptation) * hidden_attacker
            + config.attacker_adaptation * shell
            + rng.normal(0.0, config.attacker_noise, size=8)
        )

        true_alignment = (cosine_similarity(shell, hidden_attacker) + 1.0) / 2.0
        periodic_pressure = 0.42 + 0.22 * math.sin((step + 1) / 8.0)
        attack_intensity = float(np.clip(periodic_pressure + rng.uniform(0.0, 0.18), 0.05, 0.96))

        new_compromised = compromised.copy()
        for node in range(config.node_count):
            anomaly[node] = float(
                np.clip(
                    0.72 * anomaly[node]
                    + 0.28 * attack_intensity * true_alignment
                    + rng.normal(0.0, 0.04),
                    0.0,
                    1.0,
                )
            )
            if not compromised[node]:
                node_exposure = 0.75 + 0.10 * node
                probability = np.clip(
                    0.025 + 0.34 * attack_intensity * true_alignment * node_exposure,
                    0.0,
                    0.72,
                )
                if rng.random() < probability:
                    new_compromised[node] = True

        # Abstract lateral propagation on the dependency graph.
        for node in range(config.node_count):
            if compromised[node]:
                for neighbor in neighbors[node]:
                    if not new_compromised[neighbor]:
                        probability = config.lateral_movement_scale * attack_intensity
                        if rng.random() < probability:
                            new_compromised[neighbor] = True

        compromised = new_compromised
        persistence_age = np.where(compromised, persistence_age + 1, 0)
        privilege_drift = np.where(
            compromised,
            np.clip(privilege_drift + 0.08 + rng.uniform(0.0, 0.06, size=8), 0.0, 1.0),
            np.clip(privilege_drift * 0.82, 0.0, 1.0),
        )

        local_states = _local_states(compromised, anomaly, privilege_drift)
        gluing = monitor.normalized_inconsistency(local_states)
        compromised_fraction = float(np.mean(compromised))

        # Defender sees noisy operational pressure, not the hidden attacker vector.
        observable_pressure = compromised_fraction + gluing + float(np.mean(anomaly))
        if observable_pressure > 0.20:
            observation = _unit(shell + rng.normal(0.0, config.defender_noise, size=8))
            defender_estimate = _unit(
                (1.0 - config.defender_estimate_rate) * defender_estimate
                + config.defender_estimate_rate * observation
            )

        estimated_route_concentration = (
            cosine_similarity(shell, defender_estimate) + 1.0
        ) / 2.0
        collapse_index = (
            0.50 * compromised_fraction
            + 0.30 * gluing
            + 0.20 * estimated_route_concentration
        )

        compromise_sum += compromised_fraction
        collapse_values.append(float(collapse_index))
        gluing_values.append(float(gluing))
        compromise_exposure_cost += (
            config.exposure_cost_per_compromised_service * float(np.sum(compromised))
        )

        # Same core-hazard mechanism for every strategy.
        critical_fraction = float(np.mean(compromised[critical_nodes]))
        persistence_factor = float(np.mean(persistence_age[critical_nodes])) / 10.0
        core_hazard = config.core_hazard_scale * (
            compromised_fraction**2
            + 0.8 * critical_fraction
            + 0.5 * persistence_factor
            + 0.4 * gluing
        )
        if core_breached == 0 and rng.random() < np.clip(core_hazard, 0.0, 0.35):
            core_breached = 1

        should_recover = (
            strategy != Strategy.STATIC and collapse_index > config.recovery_threshold
        )
        if should_recover:
            recovery_count += 1
            if last_recovery_step is not None and step - last_recovery_step <= 8:
                reinfections += 1
            last_recovery_step = step
            shell = recover_shell(
                strategy=strategy,
                rng=rng,
                codebook=codebook,
                baseline_shell=baseline_shell,
                current_shell=shell,
                defender_estimate=defender_estimate,
                recent_shells=recent_shells,
            )
            recent_shells.append(shell.copy())
            compromised[:] = False
            persistence_age[:] = 0
            anomaly *= 0.40
            privilege_drift *= 0.20
            recovery_downtime += config.recovery_cost

    total_operational_cost = (
        recovery_downtime
        + compromise_exposure_cost
        + config.core_breach_penalty * core_breached
    )
    return TrialResult(
        strategy=strategy.value,
        seed=seed,
        shell_compromise_rate=compromise_sum / config.steps,
        core_breached=core_breached,
        recovery_downtime=recovery_downtime,
        compromise_exposure_cost=compromise_exposure_cost,
        total_operational_cost=total_operational_cost,
        recovery_count=recovery_count,
        mean_collapse_index=float(np.mean(collapse_values)),
        reinfections=reinfections,
        mean_gluing_inconsistency=float(np.mean(gluing_values)),
    )
