# Security Policy

## Scope

This repository contains an offline, synthetic simulator. It does not contain
network scanners, exploit generators, credential tools, persistence mechanisms,
or production deployment automation.

## Reporting a vulnerability

Do not publish a security-sensitive report in a public issue.
Use GitHub private vulnerability reporting after the repository is created, or
contact the repository owner through a private channel listed in the GitHub profile.

Include:

- affected version or commit;
- minimal reproduction steps;
- expected and observed behavior;
- potential impact;
- suggested mitigation, when available.

## Defensive-use boundary

Contributions must remain within benign research and defensive simulation.
Pull requests that add real-world exploitation, unauthorized scanning, credential
access, stealth, persistence, destructive actions, or production self-deployment
will not be accepted.

## Production warning

This software is not production-ready. It must not be connected directly to
medical, financial, governmental, industrial-control, or other safety-critical
systems. The simulator does not establish that an autonomous recovery policy is
safe, complete, or robust against real adversaries.
