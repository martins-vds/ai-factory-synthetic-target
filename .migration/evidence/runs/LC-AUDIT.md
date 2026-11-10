# Run journal: LC-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-10T04:23:23+00:00 | source-graph-fresh | 0 | 0.06 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `f17763edab2919be` |  |  |
| 2026-11-10T04:23:26+00:00 | source-graph-gate | 0 | 0.2 | `python .migration/harness/tools/graph_gate.py --side source` | `dde05b7ab64808ca` |  | gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67 |
| 2026-11-10T04:23:48+00:00 | setup-probe | 0 | 0.01 | `true` | `e3b0c44298fc1c14` |  |  |
