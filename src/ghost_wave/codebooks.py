"""Candidate recovery codebooks.

The vectors are abstract shell configurations. They are not cryptographic keys,
network routes, or production deployment manifests.
"""

from __future__ import annotations

import itertools

import numpy as np


def _normalize_rows(values: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    if np.any(norms <= 0):
        raise ValueError("Codebook contains a zero vector")
    return values / norms


def d8_roots() -> np.ndarray:
    """Return the 112 normalized roots of D8: ±e_i ±e_j."""
    roots: list[np.ndarray] = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1.0, 1.0):
                for sj in (-1.0, 1.0):
                    vector = np.zeros(8, dtype=float)
                    vector[i] = si
                    vector[j] = sj
                    roots.append(vector)
    result = _normalize_rows(np.asarray(roots, dtype=float))
    if result.shape != (112, 8):
        raise AssertionError(f"Unexpected D8 shape: {result.shape}")
    return result


def e8_roots() -> np.ndarray:
    """Return the 240 normalized roots of E8.

    Construction:
      * 112 vectors of the form (±1, ±1, 0, ..., 0)
      * 128 half-integer sign vectors with an even number of minus signs
    """
    roots = list(d8_roots() * np.sqrt(2.0))
    for signs in itertools.product((-1.0, 1.0), repeat=8):
        if sum(value < 0 for value in signs) % 2 == 0:
            roots.append(0.5 * np.asarray(signs, dtype=float))
    result = _normalize_rows(np.asarray(roots, dtype=float))
    if result.shape != (240, 8):
        raise AssertionError(f"Unexpected E8 shape: {result.shape}")
    return result


def random_spherical_codebook(size: int, dimension: int, seed: int) -> np.ndarray:
    """Return a deterministic random spherical codebook."""
    if size <= 0 or dimension <= 0:
        raise ValueError("size and dimension must be positive")
    rng = np.random.default_rng(seed)
    return _normalize_rows(rng.normal(size=(size, dimension)))


def gaussian_codebook(size: int, dimension: int, seed: int) -> np.ndarray:
    """Alias retained for explicit benchmark naming."""
    return random_spherical_codebook(size=size, dimension=dimension, seed=seed)


def get_codebook(name: str, seed: int = 20260722) -> np.ndarray:
    normalized = name.strip().lower()
    if normalized == "e8":
        return e8_roots()
    if normalized == "d8":
        return d8_roots()
    if normalized in {"random", "random_sphere", "gaussian"}:
        return random_spherical_codebook(size=240, dimension=8, seed=seed)
    raise ValueError(f"Unknown codebook: {name}")
