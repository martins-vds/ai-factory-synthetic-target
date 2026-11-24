# Run journal: HM-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-24T04:56:53+00:00 | runtime | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-24T04:56:53+00:00 | harness-integrity | 0 | 0.07 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_installed.py` | `a2187e62a42e5312` |  |  |
| 2026-11-24T04:56:54+00:00 | services | 0 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-24T04:56:54+00:00 | graph-freshness | 0 | 0.07 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `72a787b577623822` |  |  |
| 2026-11-24T04:56:54+00:00 | graph-source | 0 | 0.24 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `a9487981d5092c93` |  | gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125 |
| 2026-11-24T04:56:54+00:00 | graph-target | 1 | 0.21 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `549dcfa1ee672067` | ::error::graph gate (target): slice monthly-report: data path from 'command=monthly_report': **NO PATH** from 1 matching | gate=graph side=target verdict=fail failures=1 entry_points=30 reaching_data=21 enriched_edges=284 |
