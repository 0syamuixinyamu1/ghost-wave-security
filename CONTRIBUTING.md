# Contributing

Contributions are welcome when they improve reproducibility, evaluation quality,
mathematical clarity, or defensive safety.

Good contributions include:

- additional benign codebook baselines;
- confidence intervals and sensitivity analyses;
- explicit cellular-sheaf constructions;
- alternative graph topologies;
- better separation of observable and hidden attacker state;
- tests that detect evaluation leakage or strategy-specific advantages;
- documentation corrections.

Out of scope:

- exploit generation;
- unauthorized network interaction;
- credential theft or bypass;
- persistence, evasion, or destructive payloads;
- autonomous production deployment.

Before opening a pull request:

```bash
pip install -e '.[dev]'
ruff check .
pytest
```
