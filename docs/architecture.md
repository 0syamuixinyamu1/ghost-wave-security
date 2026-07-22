# Architecture

## Persistent Core

The Persistent Core is a trust boundary, not a Python object in this simulator.
A production design would keep recovery keys, approved manifests, append-only
evidence, and manual fallback controls outside the disposable agent plane.

Allowed conceptual interfaces:

```text
verify_manifest(request) -> decision
sign_approved_manifest(request) -> signature
append_evidence(record) -> receipt
```

Forbidden conceptual interfaces:

```text
return_secret_key()
delete_backups()
disable_external_kill_switch()
promote_to_production_without_independent_approval()
```

## Disposable Shell

The shell is an abstract eight-dimensional configuration vector in the toy
simulation. A future isolated testbed could map a vector to bounded choices such
as replica placement, dependency implementation, privilege profile, or network
segmentation policy. Such a mapping must remain auditable and reversible.

## Sheaf-inspired coherence

Each service carries a three-dimensional local state:

```text
[risk, anomaly, privilege drift]
```

Each dependency edge compares a projected version of its endpoint states. The
mean squared residual is a local-to-global inconsistency signal. This is a small
cellular-sheaf-inspired construction, not persistent sheaf cohomology.

## Multipolar recovery

The recovery policy scores candidate shells using only a noisy defender estimate:

```text
score =
  distance from estimated attacker focus
+ distance from current shell
- similarity to recently used shells
- operational-change penalty
```

The hidden attacker state is never passed to the recovery function.
