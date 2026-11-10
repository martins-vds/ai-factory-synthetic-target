# Run journal: LL-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09T22:49:49+00:00 | runtime | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-09T22:49:49+00:00 | harness-integrity | 0 | 0.07 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `b63333fda479c2c0` |  |  |
| 2026-11-09T22:49:49+00:00 | services | 0 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-09T22:49:49+00:00 | graph-freshness | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `e33349832f369d9d` |  |  |
| 2026-11-09T22:49:49+00:00 | graph-source | 0 | 0.17 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-09T22:49:50+00:00 | graph-target | 0 | 0.18 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `7eaad5bab3f05c41` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=4 enriched_edges=21 |
| 2026-11-09T22:49:50+00:00 | build-0 | 0 | 0.04 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T22:49:51+00:00 | build-1 | 0 | 0.96 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-09T22:49:51+00:00 | idiom-0 | 0 | 0.01 | `bash -c 'ruff check src config manage.py tests'` | `82b3e6a6c090a576` |  |  |
| 2026-11-09T22:49:51+00:00 | idiom-1 | 0 | 0.01 | `bash -c 'ruff format --check src config manage.py tests'` | `793e2905062e677b` |  |  |
| 2026-11-09T22:49:54+00:00 | tests-0 | 0 | 2.76 | `bash -c 'pytest -q'` | `f9686ad643c45263` |  |  |
| 2026-11-09T22:49:56+00:00 | crap-0 | 0 | 2.77 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `00e6b0dc60c10000` |  |  |
| 2026-11-09T22:49:57+00:00 | crap-1 | 0 | 0.07 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T22:49:57+00:00 | crap-2 | 0 | 0.06 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `60d738a9c32c42c6` |  | gate=crap max=2.0 threshold=30 over=0 methods=13 |
| 2026-11-09T22:50:35+00:00 | mutation_full-0 | 0 | 38.19 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `6af2a8d441674a94` |  | gate=mutation score=0.932 threshold=0.8 killed=41 survived=3 files=6 base=all |
| 2026-11-10T01:58:48+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |

Acceptance rows above were copied unchanged from the independently verified `.migration/evidence/runs/LL-AUDIT.md` record for run 42714661632, attempt 1. The coordinator did not rerun acceptance gates. The verified result is committed at `.migration/evidence/acceptance-runs/42714661632-1.json`; see `.migration/evidence/loan-catalog/acceptance.md` for the summary.
| 2026-11-10T03:59:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T04:00:15+00:00 | finish-check-issues-drill | 0 | 1.69 | `python .migration/harness/tools/afs-finish-check --ticket LL-ACCEPT --role afs-slice-coordinator` | `ee836a7d810f8805` |  | gate=finish-check ticket=LL-ACCEPT role=afs-slice-coordinator findings=0 |
