# Reference results

These files were generated with:

```bash
python experiments/run_benchmark.py --config experiments/configs/default.toml
```

The default run contains 120 trials per strategy. Metrics are synthetic and must
not be interpreted as production breach probabilities.

Key observation: no codebook dominates all metrics. `ghost_d8` has the lowest
mean total operational cost in the committed run, while `random_e8` has the
lowest shell-compromise rate and `single_rollback` has the lowest core-breach
rate at a much higher recovery cost.
