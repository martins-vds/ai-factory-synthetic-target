# Characterization evidence — legacy-billing

## Source and detected stack

- Source: `martins-vds/ai-factory-synthetic-target`, commit `3a69026b5d9e5522a8855960e2903efb8ad7c66c`, path `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing`.
- Verified the pinned and checked-out `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/` trees are identical; both resolve to tree `1b7f64ebb8dc30089cf3550e6ad479608d14ce95`.
- Runtime: OpenJDK 17.0.21, Maven 3.10.0.
- Stack from `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/pom.xml`: Java 17 and Maven; JUnit 4.13.2 unit tests; private Northgate Vault client 4.2.1 integration. The source is a command-line billing job, with no web framework or application-owned database configured. The Maven project encoding is UTF-8.

## Commands and observations

Initial attempts from the repository root used the wrong working directory:

| Command | Result |
|---|---|
| `./run.sh` | Exit 127: `/bin/bash: line 1: ./run.sh: No such file or directory`. |
| `mvn -B test` | Exit 1: Maven reported there was no POM in the repository root. |

Reran the source commands from the correct directory:

| Command | Result |
|---|---|
| `cd /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing && ./run.sh` | Exit 1 during Maven dependency collection. `com.northgate.vault:vault-client:4.2.1` could not be resolved from `https://maven.northgate-payments.internal/releases`; the host did not resolve. The job did not start. |
| `cd /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing && mvn -B test` | Exit 1 for the same unresolved private vault dependency; Maven did not reach test execution. |
| `mvn -B org.apache.maven.plugins:maven-dependency-plugin:3.6.1:get -Dartifact=junit:junit:4.13.2 -Dtransitive=true` | Succeeded; public JUnit 4.13.2 and Hamcrest 1.3 test jars became available in the local Maven cache. |

To try the tier-B recipe and run the tests reachable without the private vault client:

```sh
cd /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing
classes_dir=/tmp/sy-01b2-classes
mkdir -p "$classes_dir"
junit="$HOME/.m2/repository/junit/junit/4.13.2/junit-4.13.2.jar"
hamcrest="$HOME/.m2/repository/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar"
javac -sourcepath /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/src/main/java -implicit:class -cp "$junit:$hamcrest" -d "$classes_dir" /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/src/test/java/billing/InvoiceCalculatorTest.java
java -cp "$classes_dir:$junit:$hamcrest" org.junit.runner.JUnitCore billing.InvoiceCalculatorTest
```

The sourcepath compile succeeded and JUnit reported `OK (6 tests)`. It compiled the invoice calculator and line classes reached by `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/src/test/java/billing/InvoiceCalculatorTest.java`; it did not compile or run the billing job and private vault integration.

These results establish **tier B**: source code reached by the existing tests compiles and runs, although the full application build and run are blocked by the inaccessible private dependency. No files under `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy-billing/` were changed.

## Source capability assessment

Assessment is for this source only; target files were not changed.

| Capability | Status | Evidence |
|---|---|---|
| Build/run | gap | The provided runner was attempted; Maven cannot resolve the private Northgate Vault dependency. |
| Characterization harness | gap | Existing tests cover invoice calculation only; there is no harness for characterizing the full billing job or vault behavior. |
| Unit/integration tests | met | The six existing JUnit unit tests compile and pass with public test jars. No integration test ran; Maven cannot resolve the vault dependency. |
| Coverage | gap (best effort) | No source coverage configuration is present. |
| Complexity | met | `lizard` is the configured provider for both sides in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/capabilities.yaml`. |
| CRAP | gap (best effort) | No source coverage data or CRAP gate is configured for this source. |
| Mutation testing | gap | No source mutation-testing runner is configured. |
| Lint/format | gap | No source lint or format gate is configured. |
| Stack idioms | met | The existing profile provides the `java-docs` and `java-junit` skills for the source stack. |
| Data migration | gap | No application-owned database is configured, but the Northgate vault is an external payment-data boundary; portability and migration of its data/credentials are unresolved. |
| UI end-to-end | not applicable | The source is a command-line billing job, not a browser application. |
| Code graph | met | `understand-anything` is the graph tool configured in the existing profile. |
| Graph data links | gap | The existing profile's source enricher is `java-ee`, which does not match this plain Java billing source; no source-appropriate data-link enricher is recorded. |
| Output filtering | met | The existing setup records RTK OSS 1.1.0 as the output-filtering provider. |

Counts: **5 met, 8 gap, 0 waived, 1 not applicable.** Provider statuses for shared setup tools and skills are taken from the existing setup records; they were not reinstalled or changed for this assessment.
