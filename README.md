# Ghost Wave Security

**Ghost Wave Security** is a defensive research prototype for testing whether
**diversity-aware recovery** can reduce repeated compromise in disposable
service infrastructures.

The project separates:

- a **Persistent Core** that holds recovery-critical state behind restricted interfaces;
- **Disposable Shells** that may be quarantined and replaced;
- a **Sheaf-Inspired Coherence Monitor** for local-to-global inconsistency;
- a **Multipolar Recovery Engine** that selects structurally different replacement shells.

The repository is deliberately a **benign toy simulator**. It does not scan
networks, generate exploits, deploy containers, modify external systems, or
claim production-ready protection.

> Preserve what must not move. Replace what can be replaced. Keep more than one credible route back to safety.

## Status

`v0.1.0` — research prototype / toy simulation.

This release is intended for inspection, criticism, and reproducible comparison.
It is **not** a security product.

## Why “Ghost Wave”?

- **Ghost**: the exposed shell is not a permanent target.
- **Wave**: recovery moves among controlled replacement states.
- **Core**: recovery keys, evidence, policy constraints, and manual fallback remain outside the disposable layer.

## Research question

> Compared with static defense, single rollback, and random rotation, can a
> diversity-constrained recovery policy reduce repeated compromise without
> giving an automated agent access to the persistent core?

## What is E8 doing here?

The E8 root system is used only as a **fixed, auditable candidate codebook**.
It is not treated as cryptography, a literal infrastructure symmetry, or a proof
of security. The benchmark also includes D8 and random spherical codebooks so
that the E8 hypothesis can fail.

## Repository layout

```text
ghost-wave-security/
├── src/ghost_wave/          # simulator and recovery policies
├── experiments/             # reproducible benchmark entry point
├── tests/                   # unit and invariance tests
├── docs/                    # architecture, threat model, limitations
├── paper/                   # NeurIPS-style concept paper draft
├── results/                 # generated CSV summaries
├── figures/                 # generated benchmark plots
├── SECURITY.md
├── CITATION.cff
└── pyproject.toml
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
pytest
python experiments/run_benchmark.py --config experiments/configs/default.toml
```

The benchmark writes:

- `results/summary.csv`
- `results/runs.csv`
- `figures/benchmark_rates.png`
- `figures/benchmark_costs.png`
- `paper/results_generated.tex`

## CLI

After installation:

```bash
ghost-wave benchmark --config experiments/configs/default.toml
```

A smaller smoke run:

```bash
ghost-wave benchmark --seeds 2 --trials 10 --steps 40
```

## Strategies

| Strategy | Behavior |
|---|---|
| `static` | Never replaces the shell. |
| `single_rollback` | Always returns to the same baseline shell. |
| `random_e8` | Randomly selects an E8-codebook shell. |
| `ghost_e8` | Diversity-constrained selection over E8 roots. |
| `ghost_d8` | Same policy over D8 roots. |
| `ghost_random` | Same policy over random spherical candidates. |

## Fairness corrections in v0.1.0

The original exploratory simulation contained two serious evaluation shortcuts.
This repository removes them:

1. **Core breach probability is not strategy-specific.** It is generated from
   the same hazard process for every strategy and depends on compromise extent,
   critical-node exposure, and persistence.
2. **The defender does not read the attacker’s private state.** Recovery uses a
   noisy estimate built from observable shell pressure and compromise events.

The benchmark also separates:

- recovery downtime;
- compromised-service exposure;
- total operational cost, including an explicit synthetic penalty for persistent-core breach.

## Reference run

The committed reference run uses 3 seeds × 40 trials × 100 steps per strategy
(120 trials per strategy). The point is comparative behavior, not real-world risk.

| Strategy | Shell compromise | Core breach | Total synthetic cost |
|---|---:|---:|---:|
| `ghost_d8` | 0.319 | 0.358 | **105.8** |
| `ghost_e8` | 0.332 | 0.367 | 108.4 |
| `ghost_random` | 0.334 | 0.350 | 107.3 |
| `random_e8` | **0.284** | 0.325 | 112.0 |
| `single_rollback` | 0.300 | **0.275** | 156.3 |
| `static` | 0.974 | 0.933 | 155.7 |

No strategy dominates every metric. In particular, the E8-based Ghost Wave
policy does not outperform D8 or random candidates in this configuration. That
is an intended falsifiability feature, not a defect to hide.

## Security boundaries

A production interpretation must preserve:

```text
AI proposal != production authorization
```

The disposable layer must not receive:

- offline or hardware-backed recovery keys;
- unrestricted production write access;
- backup deletion capability;
- permission to disable external kill switches;
- authority to erase audit evidence.

See [`docs/threat_model.md`](docs/threat_model.md) and
[`SECURITY.md`](SECURITY.md).

## Non-claims

This project does **not** claim:

- guaranteed detection of zero-day attacks;
- invulnerable infrastructure;
- literal E8, E6, or SU(3) implementation in production systems;
- production-valid breach probabilities;
- safe autonomous patching of hospitals, banks, public infrastructure, or industrial control systems.

## Paper

The `paper/` directory contains a NeurIPS-style concept-and-feasibility draft.
Place the official `neurips_2026.sty` file in that directory before compiling.
The paper intentionally frames the sheaf component as **sheaf-inspired** until a
full cellular-sheaf implementation and realistic testbed are completed.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

Use of the code remains subject to applicable law, system-owner authorization,
and the defensive scope described in this repository.
