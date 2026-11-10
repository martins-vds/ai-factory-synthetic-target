# Run journal: LC-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-10T02:00:34+00:00 | runtime | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-10T02:00:34+00:00 | harness-integrity | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `b63333fda479c2c0` |  |  |
| 2026-11-10T02:00:34+00:00 | services | 0 | 0.12 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-10T02:00:34+00:00 | graph-freshness | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `5570c9c0cb2d36b2` |  |  |
| 2026-11-10T02:00:34+00:00 | graph-source | 0 | 0.13 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-10T02:00:35+00:00 | graph-target | 1 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `9bab8a6425d137f4` | ::error::graph gate (target): slice loan-catalog: data path from 'endpoint=/loans': no matching node (match a node's nam | gate=graph side=target verdict=fail failures=8 entry_points=16 reaching_data=4 enriched_edges=68 |
