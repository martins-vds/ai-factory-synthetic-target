# Run journal: HM-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-24T12:48:59+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-24T12:49:13+00:00 | source-graph | 0 | 0.39 | `bash -lc 'python .migration/harness/tools/check_graph_fresh.py --require source && python .migration/harness/tools/graph_gate.py --side source'` | `3ad7d0a76c1f322d` |  | gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125 |
