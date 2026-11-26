# Run journal: HM-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-25T14:35:04+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-25T14:46:50+00:00 | spec-mutation | 0 | 673.81 | `python .migration/harness/tools/afs-mutation --all --spec` | `1a82ef9977493bbf` |  | gate=spec-mutation score=0.510 killed=225 survived=216 files=29 base=all |
| 2026-11-25T01:01:53+00:00 | runtime | 0 | 0.07 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-25T01:01:53+00:00 | harness-integrity | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `b47d99e72f199adc` |  |  |
| 2026-11-25T01:01:54+00:00 | services | 0 | 0.15 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-25T01:01:54+00:00 | graph-freshness | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `fa9273af50cd73b9` |  |  |
| 2026-11-25T01:01:54+00:00 | graph-source | 0 | 0.18 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `a9487981d5092c93` |  | gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125 |
| 2026-11-25T01:01:54+00:00 | graph-target | 0 | 0.24 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `2a966c5cc587efcd` |  | gate=graph side=target verdict=pass failures=0 entry_points=30 reaching_data=21 enriched_edges=313 |
| 2026-11-25T01:01:55+00:00 | build-0 | 0 | 0.06 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-25T01:01:55+00:00 | build-1 | 0 | 0.8 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-25T01:01:56+00:00 | idiom-0 | 0 | 0.01 | `bash -c 'ruff check src config manage.py tests'` | `82b3e6a6c090a576` |  |  |
| 2026-11-25T01:01:56+00:00 | idiom-1 | 0 | 0.01 | `bash -c 'ruff format --check src config manage.py tests'` | `60b1abe1dfdcd741` |  |  |
| 2026-11-25T01:01:56+00:00 | idiom-2 | 0 | 0.11 | `bash -c 'python .migration/harness/tools/check_layers.py'` | `d970c18c2dcfe59c` |  | gate=layering contracts=3 violations=0 known=1 |
| 2026-11-25T01:01:56+00:00 | idiom-3 | 0 | 0.21 | `bash -c 'python .migration/harness/tools/check_ui.py'` | `b9ae03306fe277bb` |  | gate=ui scope="templates changed since origin/main" templates=0 findings=0 |
| 2026-11-25T01:02:14+00:00 | tests-0 | 0 | 17.68 | `bash -c 'pytest -q'` | `6e51bb7d2fb7d064` |  |  |
| 2026-11-25T01:02:18+00:00 | spec-0 | 0 | 3.55 | `bash -c 'python .migration/harness/tools/afs-spec run'` | `2663a8a26061d90c` | AFS-RESULT gate=spec cases=59 failed=0 pending=0 | gate=spec cases=59 failed=0 pending=0 |
| 2026-11-25T01:02:36+00:00 | crap-0 | 0 | 18.62 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `aeac7b0f33e3b0b5` |  |  |
| 2026-11-25T01:02:36+00:00 | crap-1 | 0 | 0.09 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-25T01:02:37+00:00 | crap-2 | 0 | 0.06 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `e66e4426f459744c` |  | gate=crap max=7.0 threshold=30 over=0 methods=72 |
| 2026-11-25T01:11:18+00:00 | mutation_full-0 | 0 | 521.48 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `a68007e3984c9ff7` |  | gate=mutation score=0.921 threshold=0.8 killed=406 survived=35 files=29 base=all |
