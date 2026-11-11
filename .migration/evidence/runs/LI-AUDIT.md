# Run journal: LI-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-11T01:53:49+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-11T01:53:55+00:00 | source-graph-fresh | 0 | 0.05 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `f17763edab2919be` |  |  |
| 2026-11-11T01:53:58+00:00 | source-graph-gate | 0 | 0.15 | `python .migration/harness/tools/graph_gate.py --side source` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-11T01:54:02+00:00 | acceptance-fetch | 0 | 0.24 | `python .migration/harness/tools/afs-acceptance fetch --run-id 42938753426 --attempt 1 --dest .migration/runs/acceptance-42938753426-1` | `c7c9a53fb3bf8312` |  |  |
| 2026-11-11T01:54:34+00:00 | acceptance-verify | 0 | 0.09 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-42938753426-1 --commit 7d4b249e342a94e7176ebf3e1d370f81d7156b16 --run-id 42938753426 --attempt 1` | `c3408f1078ef364d` |  | gate=acceptance-evidence status=verified commit=7d4b249e342a94e7176ebf3e1d370f81d7156b16 run_id=42938753426 attempt=1 |
| 2026-11-11T01:28:36+00:00 | runtime | 0 | 0.04 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-11T01:28:36+00:00 | harness-integrity | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `f170397ac80229ab` |  |  |
| 2026-11-11T01:28:36+00:00 | services | 0 | 0.1 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-11T01:28:36+00:00 | graph-freshness | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `f0680e97b7e7ff96` |  |  |
| 2026-11-11T01:28:36+00:00 | graph-source | 0 | 0.11 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-11T01:28:36+00:00 | graph-target | 0 | 0.13 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `de2391594e497a4d` |  | gate=graph side=target verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=146 |
| 2026-11-11T01:28:36+00:00 | build-0 | 0 | 0.03 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-11T01:28:37+00:00 | build-1 | 0 | 0.7 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-11T01:28:37+00:00 | idiom-0 | 0 | 0.01 | `bash -c 'ruff check src config manage.py tests'` | `82b3e6a6c090a576` |  |  |
| 2026-11-11T01:28:37+00:00 | idiom-1 | 0 | 0.01 | `bash -c 'ruff format --check src config manage.py tests'` | `ec547b9784fec079` |  |  |
| 2026-11-11T01:28:52+00:00 | tests-0 | 0 | 14.42 | `bash -c 'pytest -q'` | `1af8f8263ade5482` |  |  |
| 2026-11-11T01:29:05+00:00 | crap-0 | 0 | 13.63 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `592c9d871a366964` |  |  |
| 2026-11-11T01:29:05+00:00 | crap-1 | 0 | 0.05 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-11T01:29:06+00:00 | crap-2 | 0 | 0.04 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `0b9ded77b747ce40` |  | gate=crap max=7.0 threshold=30 over=0 methods=40 |
| 2026-11-11T01:36:13+00:00 | mutation_full-0 | 0 | 427.39 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `1176413a19bef562` |  | gate=mutation score=0.976 threshold=0.8 killed=244 survived=6 files=17 base=all |
| 2026-11-11T01:57:37+00:00 | migration-validate | 0 | 0.58 | `python .migration/harness/tools/validate.py .migration` | `0cf35336654ab867` |  |  |
| 2026-11-11T01:58:10+00:00 | final-validate | 0 | 0.59 | `python .migration/harness/tools/validate.py .migration` | `0cf35336654ab867` |  |  |
