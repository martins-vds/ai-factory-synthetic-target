# Characterization evidence — `legacy-reports/`

## Scope and source stack

- Source: `martins-vds/ai-factory-synthetic-target`, pinned commit `3a69026b5d9e5522a8855960e2903efb8ad7c66c`, path `legacy-reports/`.
- The current checkout is at `9b2091401f61491c0d30c80368f7149a990d8cf3`. `git diff --quiet 3a69026b5d9e5522a8855960e2903efb8ad7c66c -- legacy-reports` exited 0, so the checked-out source matches the pin.
- The source consists of a README, two Markdown report specifications, one CSV report sample, and one plain-text overdue notice sample. All five files are ASCII text.
- This is an archival specification/output set, not an executable software stack. The README says the reporting server was retired in 2019 and its report definitions were not kept. No source code, build configuration, test files, or executable scripts are present.
- Target stacks, read from `.migration/profile.yaml` as instructed: Python 3.13/Django 5, Django templates, and PostgreSQL 17.

## Commands run and observations

| Command | Observation |
|---|---|
| `git rev-parse HEAD` | `9b2091401f61491c0d30c80368f7149a990d8cf3`. |
| `git rev-parse 3a69026b5d9e5522a8855960e2903efb8ad7c66c` | The pinned commit exists locally and resolves to the requested SHA. |
| `git ls-tree -r --name-only 3a69026b5d9e5522a8855960e2903efb8ad7c66c -- legacy-reports` | Listed exactly the five files described above. |
| `find legacy-reports -type f \( -name 'pom.xml' -o -name 'build.gradle*' -o -name 'Makefile' -o -name 'package.json' -o -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'pytest.ini' -o -name 'tox.ini' -o -name 'run.sh' -o -name 'Dockerfile*' -o -name '*.java' -o -name '*.py' -o -name '*.js' -o -name '*.ts' \) -print` | No output: no recognized build/test manifests, application source, or run script. |
| `file legacy-reports/README.md legacy-reports/docs/* legacy-reports/samples/*` | All five files are ASCII text; the sample report is CSV and the notice is plain text. |
| `find legacy-reports -type f -perm /111 -print` | No output: no executable files. |
| `command -v rtk` | `rtk: not installed`; output filtering is not available in this checkout, despite the RTK setting in the existing profile. |
| `git diff --quiet 3a69026b5d9e5522a8855960e2903efb8ad7c66c -- legacy-reports` | Exit 0: no differences from the pinned source. |

No build, run, or test command was attempted: the pinned source offers no application, build/test manifest, executable, or documented command to invoke. The report specification and examples can be read, but they do not provide a legacy runtime to exercise.

## Characterization tier

**Tier C.** The source is not buildable or runnable because it contains only specifications and historical output samples; there is no legacy environment, source implementation, or test suite. The artifacts provide requirements and examples for a future implementation, not executable behavior that can be characterized through a running source system.

## Source capability assessment

Counts are for this source only, not the target or the combined checklist in `.migration/capabilities.yaml`.

| Capability | Status | Evidence |
|---|---|---|
| `build-run` | gap | No application source, build manifest, or run entrypoint. |
| `characterization-harness` | gap | No repeatable harness is present; only static specifications and samples are available. |
| `unit-integration-tests` | gap | No test files or test runner configuration are present. |
| `coverage` | gap (best-effort) | No executable source or tests to instrument. |
| `complexity` | not applicable | There are no implementation methods to measure. |
| `crap` | not applicable | There is no executable code or coverage data. |
| `mutation-testing` | not applicable | There is no executable source to mutate. |
| `lint-format` | not applicable | There is no implementation language or source-code lint/format gate. |
| `stack-idioms` | not applicable | No application implementation stack is represented. |
| `data-migration` | not applicable | The source provides report outputs but no database, data store, or migration interface. |
| `ui-end-to-end` | not applicable | No application UI is present. |
| `code-graph` | not applicable | No application code is present to graph. |
| `graph-data-links` | not applicable | No source application/data graph can be produced from these artifacts. |
| `output-filtering` | gap | `rtk` is configured in the profile but is not installed in the current checkout. |

**Counts:** met 0, gap 5, waived 0, not applicable 9.
