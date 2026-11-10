# Run journal: LC-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-10T03:57:09+00:00 | runtime | 0 | 0.04 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-10T03:57:09+00:00 | harness-integrity | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `3710ff655e45aee1` |  |  |
| 2026-11-10T03:57:09+00:00 | services | 0 | 0.1 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-10T03:57:09+00:00 | graph-freshness | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `fb14534c52a9d9dc` |  |  |
| 2026-11-10T03:57:09+00:00 | graph-source | 0 | 0.12 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-10T03:57:09+00:00 | graph-target | 0 | 0.12 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `8f39de4c9e6fcc62` |  | gate=graph side=target verdict=pass failures=0 entry_points=16 reaching_data=12 enriched_edges=77 |
| 2026-11-10T03:57:10+00:00 | build-0 | 0 | 0.03 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T03:57:10+00:00 | build-1 | 0 | 0.82 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-10T03:57:11+00:00 | idiom-0 | 0 | 0.01 | `bash -c 'ruff check src config manage.py tests'` | `82b3e6a6c090a576` |  |  |
| 2026-11-10T03:57:11+00:00 | idiom-1 | 0 | 0.01 | `bash -c 'ruff format --check src config manage.py tests'` | `7715b02781372f87` |  |  |
| 2026-11-10T03:57:14+00:00 | tests-0 | 0 | 3.44 | `bash -c 'pytest -q'` | `4320252b1332d4b5` |  |  |
| 2026-11-10T03:57:18+00:00 | crap-0 | 0 | 3.44 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `a1a4e4276c27a253` |  |  |
| 2026-11-10T03:57:18+00:00 | crap-1 | 0 | 0.05 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T03:57:18+00:00 | crap-2 | 0 | 0.04 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `1a44279a39c11bc6` |  | gate=crap max=7.0 threshold=30 over=0 methods=23 |
| 2026-11-10T03:59:00+00:00 | mutation_full-0 | 0 | 102.52 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `4510bb8211bb915d` |  | gate=mutation score=0.920 threshold=0.8 killed=126 survived=11 files=9 base=all |
| 2026-11-10T17:22:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |

Acceptance rows above were imported unchanged from the verified artifact for [Actions run 42752283868, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42752283868). Its result is archived at `.migration/evidence/acceptance-runs/42752283868-1.json`; artifact retention runs through 2026-12-10.
