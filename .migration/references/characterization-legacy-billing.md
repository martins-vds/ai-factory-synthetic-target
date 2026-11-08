# Characterization evidence — legacy-billing

## Source and environment

- Source: `martins-vds/ai-factory-synthetic-target`, commit `3a69026b5d9e5522a8855960e2903efb8ad7c66c`, path `legacy-billing`.
- Verified the pinned and checked-out `legacy-billing/` trees are identical: both resolve to tree `1b7f64ebb8dc30089cf3550e6ad479608d14ce95`.
- Runtime: OpenJDK 17.0.21, Maven 3.10.0.
- Stack from `legacy-billing/pom.xml`: Java 17, Maven, JUnit 4.13.2. The production code integrates with Northgate Vault client 4.2.1 from a private Maven repository. The source declares UTF-8; files are ASCII (UTF-8-compatible). No local database or user interface is present.

## Commands and observations

The pinned tree was extracted to a temporary directory so the source directory remained unchanged:

```sh
tmp=$(mktemp -d /tmp/sy01b.XXXXXX) &&
git archive 3a69026b5d9e5522a8855960e2903efb8ad7c66c legacy-billing | tar -x -C "$tmp" &&
cd "$tmp/legacy-billing" &&
env -u NORTHGATE_MERCHANT -u NORTHGATE_KEY timeout 90s ./run.sh
```

`./run.sh` ran `mvn -q -B package`, which exited 1 before compiling or launching the application. Maven could not resolve `com.northgate.vault:vault-client:4.2.1` from `https://maven.northgate-payments.internal/releases`; the repository hostname did not resolve.

Then, from the same extracted directory:

```sh
timeout 90s mvn -B -ntp test
```

This also exited 1 during dependency resolution with the same missing artifact and hostname error. The source contains six JUnit tests in `InvoiceCalculatorTest`, but none executed.

The application was not separately launched. `BillingJob.main` constructs `CardVault` and runs a billing job that charges the card on file; without an approved sandbox vault, bypassing the failed build to invoke it would risk a real payment.

These observations establish characterization tier C. The required private vault client is a production runtime integration, not a compile-only dependency; the pinned source could not be built or safely run, and its tests could not execute. Tier B is therefore not supported by the evidence.

## Source capability assessment

Counts are for this source only: 4 met, 8 gap, 0 waived, and 2 not applicable.

| Capability | Status | Evidence |
|---|---|---|
| Build/run | gap | Build is blocked by the unresolved private runtime dependency. |
| Characterization harness | gap | The source has unit tests, but no runnable system characterization harness. |
| Unit/integration tests | gap | Six JUnit tests exist, but Maven cannot resolve the production dependency and no tests execute. |
| Coverage | gap (best effort) | No coverage instrumentation or report configuration is present. |
| Complexity | met | `lizard` is provided by the existing migration capability setup. |
| CRAP | gap (best effort) | No executable test run or coverage data is available for this source. |
| Mutation testing | gap | No source mutation-testing runner is configured. |
| Lint/format | gap | No Java lint or formatting gate is configured for this source. |
| Stack idioms | met | The existing profile provides `java-docs` and `java-junit` skills for this source stack. |
| Data migration | not applicable | The source has no local database or persistent records to migrate. |
| UI end-to-end | not applicable | The source has no user interface. |
| Code graph | met | The existing profile provides `understand-anything` at commit `4e6d3299017a7432da15957874992837a315c5b4`. |
| Graph data links | gap | The configured Java EE enricher does not match this plain Java billing source; no suitable source enricher is provided. |
| Output filtering | met | The existing profile provides RTK OSS 1.1.0. |
