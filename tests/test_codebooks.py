import numpy as np

from ghost_wave.codebooks import d8_roots, e8_roots, random_spherical_codebook


def test_e8_shape_and_norms() -> None:
    roots = e8_roots()
    assert roots.shape == (240, 8)
    assert np.allclose(np.linalg.norm(roots, axis=1), 1.0)
    assert len(np.unique(np.round(roots, 8), axis=0)) == 240


def test_d8_shape_and_norms() -> None:
    roots = d8_roots()
    assert roots.shape == (112, 8)
    assert np.allclose(np.linalg.norm(roots, axis=1), 1.0)


def test_random_codebook_is_reproducible() -> None:
    first = random_spherical_codebook(20, 8, seed=7)
    second = random_spherical_codebook(20, 8, seed=7)
    assert np.allclose(first, second)
