# Run journal: LF-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-10T22:46:32+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T22:46:38+00:00 | source-graph-fresh | 0 | 0.04 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `f17763edab2919be` |  |  |
| 2026-11-10T22:46:38+00:00 | source-graph-gate | 0 | 0.1 | `python .migration/harness/tools/graph_gate.py --side source` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-10T22:46:52+00:00 | acceptance-fetch | 0 | 0.2 | `python .migration/harness/tools/afs-acceptance fetch --run-id 42912984554 --attempt 1 --dest .migration/runs/acceptance-42912984554-1` | `843a56c04a5dcfaa` |  |  |
| 2026-11-10T22:46:56+00:00 | acceptance-verify-help | 0 | 0.04 | `python .migration/harness/tools/afs-acceptance verify --help` | `333a0a3ad3e020fd` |  |  |
| 2026-11-10T22:47:04+00:00 | acceptance-verify | 2 | 0.04 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-42912984554-1/result.json --run-id 42912984554 --attempt 1 --commit 8f9a11640eef9801378f3db53a76903363c5e5b5` | `b4a558e9ef4ed8ab` |  |  |
| 2026-11-10T22:47:08+00:00 | acceptance-verify | 0 | 0.06 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-42912984554-1 --run-id 42912984554 --attempt 1 --commit 8f9a11640eef9801378f3db53a76903363c5e5b5` | `e076dcd0e0da3d9b` |  | gate=acceptance-evidence status=verified commit=8f9a11640eef9801378f3db53a76903363c5e5b5 run_id=42912984554 attempt=1 |
| 2026-11-10T22:20:42+00:00 | runtime | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-10T22:20:42+00:00 | harness-integrity | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `dfd55d0883d0dcec` |  |  |
| 2026-11-10T22:20:42+00:00 | services | 0 | 0.23 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-10T22:20:42+00:00 | graph-freshness | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `919151ce11bb145d` |  |  |
| 2026-11-10T22:20:42+00:00 | graph-source | 0 | 0.16 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-10T22:20:43+00:00 | graph-target | 0 | 0.2 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `e337dc9638d13f20` |  | gate=graph side=target verdict=pass failures=0 entry_points=23 reaching_data=18 enriched_edges=148 |
| 2026-11-10T22:20:43+00:00 | build-0 | 0 | 0.05 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T22:20:43+00:00 | build-1 | 0 | 0.64 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-10T22:20:43+00:00 | idiom-0 | 0 | 0.01 | `bash -c 'ruff check src config manage.py tests'` | `82b3e6a6c090a576` |  |  |
| 2026-11-10T22:20:43+00:00 | idiom-1 | 0 | 0.01 | `bash -c 'ruff format --check src config manage.py tests'` | `2de9ddcc7788f957` |  |  |
| 2026-11-10T22:20:58+00:00 | tests-0 | 0 | 14.37 | `bash -c 'pytest -q'` | `cd3bad4d4305c078` |  |  |
| 2026-11-10T22:21:13+00:00 | crap-0 | 0 | 14.67 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `df49fb3c4323369f` |  |  |
| 2026-11-10T22:21:13+00:00 | crap-1 | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-10T22:21:13+00:00 | crap-2 | 0 | 0.06 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `3e97bcd4c38fc824` |  | gate=crap max=7.0 threshold=30 over=0 methods=38 |
| 2026-11-10T22:28:25+00:00 | mutation_full-0 | 0 | 431.81 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `0ced7daef681a111` |  | gate=mutation score=0.975 threshold=0.8 killed=236 survived=6 files=15 base=all |
| 2026-11-10T22:53:00+00:00 | migration-validate | 0 | 0.37 | `python .migration/harness/tools/validate.py .migration` | `2f118c59d9d07eef` |  |  |
