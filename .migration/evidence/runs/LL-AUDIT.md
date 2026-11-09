# Run journal: LL-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09T23:15:35+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T23:15:54+00:00 | source-graph-freshness | 0 | 0.04 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `f17763edab2919be` |  |  |
| 2026-11-09T23:15:56+00:00 | source-graph-gate | 0 | 0.09 | `python .migration/harness/tools/graph_gate.py --side source` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
