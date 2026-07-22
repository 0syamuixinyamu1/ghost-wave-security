"""Recovery strategies for the synthetic benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from .codebooks import d8_roots, e8_roots, random_spherical_codebook


class Strategy(StrEnum):
    STATIC = "static"
    SINGLE_ROLLBACK = "single_rollback"
    RANDOM_E8 = "random_e8"
    GHOST_E8 = "ghost_e8"
    GHOST_D8 = "ghost_d8"
    GHOST_RANDOM = "ghost_random"


@dataclass(frozen=True)
class CandidateScoreWeights:
    estimated_attacker_distance: float = 0.45
    current_shell_distance: float = 0.25
    recent_shell_penalty: float = 0.20
    operational_change_penalty: float = 0.10


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator <= 1e-12:
        return 0.0
    return float(np.dot(left, right) / denominator)


def cosine_distance(left: np.ndarray, right: np.ndarray) -> float:
    return 1.0 - cosine_similarity(left, right)


def codebook_for_strategy(strategy: Strategy, seed: int) -> np.ndarray:
    if strategy in {Strategy.SINGLE_ROLLBACK, Strategy.RANDOM_E8, Strategy.GHOST_E8}:
        return e8_roots()
    if strategy == Strategy.GHOST_D8:
        return d8_roots()
    if strategy == Strategy.GHOST_RANDOM:
        return random_spherical_codebook(240, 8, seed=seed)
    return e8_roots()


def choose_diverse_candidate(
    codebook: np.ndarray,
    defender_estimate: np.ndarray,
    current_shell: np.ndarray,
    recent_shells: list[np.ndarray],
    weights: CandidateScoreWeights = CandidateScoreWeights(),
) -> np.ndarray:
    """Select a candidate without reading the attacker's hidden state."""
    # Codebook rows are normalized by construction. Normalize estimates once and
    # score all candidates with vectorized operations for reproducible speed.
    estimate = defender_estimate / (np.linalg.norm(defender_estimate) + 1e-12)
    current = current_shell / (np.linalg.norm(current_shell) + 1e-12)
    estimated_distance = 1.0 - codebook @ estimate
    current_distance = 1.0 - codebook @ current

    recent = recent_shells[-5:]
    if recent:
        recent_matrix = np.asarray(recent, dtype=float)
        recent_matrix /= np.linalg.norm(recent_matrix, axis=1, keepdims=True) + 1e-12
        recent_similarity = np.max(codebook @ recent_matrix.T, axis=1)
    else:
        recent_similarity = np.zeros(len(codebook), dtype=float)

    operational_change = np.mean(np.abs(codebook - current_shell), axis=1)
    scores = (
        weights.estimated_attacker_distance * estimated_distance
        + weights.current_shell_distance * current_distance
        - weights.recent_shell_penalty * recent_similarity
        - weights.operational_change_penalty * operational_change
    )
    return codebook[int(np.argmax(scores))].copy()


def recover_shell(
    strategy: Strategy,
    rng: np.random.Generator,
    codebook: np.ndarray,
    baseline_shell: np.ndarray,
    current_shell: np.ndarray,
    defender_estimate: np.ndarray,
    recent_shells: list[np.ndarray],
) -> np.ndarray:
    if strategy == Strategy.SINGLE_ROLLBACK:
        return baseline_shell.copy()
    if strategy == Strategy.RANDOM_E8:
        return codebook[int(rng.integers(0, len(codebook)))].copy()
    if strategy in {Strategy.GHOST_E8, Strategy.GHOST_D8, Strategy.GHOST_RANDOM}:
        return choose_diverse_candidate(
            codebook=codebook,
            defender_estimate=defender_estimate,
            current_shell=current_shell,
            recent_shells=recent_shells,
        )
    raise ValueError(f"Strategy does not recover shells: {strategy}")
