# Run journal: LL-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09T21:24:16+00:00 | runtime | 0 | 0.04 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-09T21:24:17+00:00 | harness-integrity | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `34ef99eb01daa8a3` |  |  |
| 2026-11-09T21:24:17+00:00 | services | 0 | 0.11 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-09T21:24:17+00:00 | graph-freshness | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `f33b82c4d90f49ec` |  |  |
| 2026-11-09T21:24:17+00:00 | graph-source | 0 | 0.12 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-09T21:24:17+00:00 | graph-target | 1 | 0.12 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `d665b39cb5d214ac` | ::error::graph gate (target): slice loan-catalog: data path from 'endpoint=GET /loans': no matching node (match a node's | gate=graph side=target verdict=fail failures=11 entry_points=7 reaching_data=3 enriched_edges=20 |
