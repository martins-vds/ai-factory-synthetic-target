# Characterization tier and evidence

## Selected tier: B

The harness's characterization contract defines tier B for source code that can run in isolation when a
fully usable legacy environment is unavailable. The synthetic scenario catalog at the pinned harness
revision (`synthetic/scenarios.yaml`, `partial-runtime`) specifically maps this partial-runtime case to
bootstrapper tier B.

## Evidence supplied for SY-00

- In a temporary copy of the pinned `legacy/` source, `./run.sh` packaged and launched the H2/Jersey/
  Grizzly application. Startup output included `Started listener bound to [0.0.0.0:8080]` and
  `Lending Library listening on 8080`.
- Startup also warned that the root-resource instances `LoanResource`, `LateFeeView`, `FinePayments`, and
  `AboutPage` were ignored.
- Loopback HTTP probes from the sandbox returned `000`; no usable external interface was demonstrated.
- `FinePayments.java` calls an external payment gateway for which no test instance is available.
- The scenario documentation identifies this behavior as `partial-runtime`.

This is not tier A: a process starts, but the externally observable interfaces could not be exercised.
Tier B is selected for the runnable parts; `FinePayments` remains a capability to characterize at an
isolated seam or spec-derived if that cannot be made runnable. The observations above were supplied in the
SY-00 task context; this session did not access `legacy/`.

## Bootstrap limitations

The required `afs-migration-contract` and `afs-setup-check` skills were unavailable in this environment.
Their pinned documentation in harness commit `b781324e25d49a4a95f752e2072ddc2cca69e09e` was consulted
instead. The pinned bootstrap was not run because it writes `.github/agents/` and reads that directory to
create `installed.json`, while this task explicitly prohibits accessing `.github/agents/`.
