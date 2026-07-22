from ghost_wave.simulation import SimulationConfig, run_trial
from ghost_wave.strategies import Strategy


def test_trial_is_reproducible() -> None:
    config = SimulationConfig(steps=25)
    first = run_trial(Strategy.GHOST_E8, seed=123, config=config)
    second = run_trial(Strategy.GHOST_E8, seed=123, config=config)
    assert first == second


def test_all_strategies_use_same_result_schema() -> None:
    config = SimulationConfig(steps=12)
    for strategy in Strategy:
        result = run_trial(strategy, seed=33, config=config)
        assert result.strategy == strategy.value
        assert 0.0 <= result.shell_compromise_rate <= 1.0
        assert result.core_breached in {0, 1}
        assert result.total_operational_cost >= 0.0


def test_static_accumulates_exposure_cost() -> None:
    config = SimulationConfig(steps=40)
    result = run_trial(Strategy.STATIC, seed=55, config=config)
    assert result.recovery_downtime == 0.0
    assert result.compromise_exposure_cost > 0.0
