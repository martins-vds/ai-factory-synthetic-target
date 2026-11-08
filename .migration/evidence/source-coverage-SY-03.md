# Source coverage (best effort)

- No Java test sources were found under `legacy/src/test`.
- JaCoCo 0.8.13 instrumented `legacy/run.sh` through `JAVA_TOOL_OPTIONS` while the source characterization runner exercised all seven graph endpoints and opened the `/about` and `/fees/L3` pages in Chromium.
- JaCoCo reported 89 covered / 9 missed lines, 460 covered / 53 missed instructions, 10 covered / 10 missed branches, 35 covered / 2 missed methods, and 7 covered / 0 missed classes.
- Evidence: `.migration/evidence/runs/SY-03.md` rows `source-coverage-characterization`, `source-jacoco-report`, and `source-coverage-summary`.
