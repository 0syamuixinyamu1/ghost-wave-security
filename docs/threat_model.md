# Threat Model

## Protected assets

The conceptual architecture aims to protect:

- integrity of recovery manifests;
- availability of disposable service shells;
- append-only incident evidence;
- independence of manual fallback and external shutdown paths;
- separation between an AI proposal layer and production authorization.

## Modeled adversary

The simulator represents an adaptive adversary that:

- learns the currently exposed abstract shell;
- creates stochastic compromise pressure;
- propagates compromise over service dependencies;
- benefits when the defender repeatedly restores similar shells.

This is not a real attacker implementation.

## Out of scope

- real vulnerabilities and exploits;
- social engineering;
- supply-chain compromise of the persistent core;
- nation-state operational capability;
- physical process manipulation;
- covert channels and side channels;
- malicious maintainers or compromised CI infrastructure.

## Failure modes to study

1. Recovery thrashing becomes a denial of service.
2. The defender estimate is systematically wrong.
3. All codebook candidates share a common-mode vulnerability.
4. The persistent core becomes a single institutional or technical point of failure.
5. The same model proposes and validates a recovery.
6. Human approval becomes a rubber stamp because the output volume exceeds review capacity.
