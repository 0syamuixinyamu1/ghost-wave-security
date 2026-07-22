import numpy as np

from ghost_wave.sheaf_monitor import SheafCoherenceMonitor


def test_identical_local_states_have_zero_energy() -> None:
    monitor = SheafCoherenceMonitor()
    states = np.tile(np.asarray([0.2, 0.3, 0.4]), (8, 1))
    assert monitor.gluing_energy(states) == 0.0


def test_inconsistency_is_bounded() -> None:
    monitor = SheafCoherenceMonitor()
    states = np.zeros((8, 3))
    states[0] = np.asarray([1.0, 1.0, 1.0])
    value = monitor.normalized_inconsistency(states)
    assert 0.0 < value < 1.0
