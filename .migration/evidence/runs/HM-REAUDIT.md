# Run journal: HM-REAUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-25T01:14:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-25T01:14:51+00:00 | source-graph-fresh | 0 | 0.06 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `f17763edab2919be` |  |  |
| 2026-11-25T01:14:52+00:00 | source-graph-gate | 0 | 0.18 | `python .migration/harness/tools/graph_gate.py --side source` | `a9487981d5092c93` |  | gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125 |
| 2026-11-25T01:14:57+00:00 | fetch-acceptance-45521850054-1 | 0 | 0.26 | `python .migration/harness/tools/afs-acceptance fetch --run-id 45521850054 --attempt 1 --dest .migration/runs/acceptance-45521850054-1` | `f7ede69bfc809789` |  |  |
| 2026-11-25T01:15:08+00:00 | verify-acceptance-45521850054-1 | 0 | 0.1 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-45521850054-1 --commit 9179fc5ced6a543ca557d877f389c1f3e8c987fe --run-id 45521850054 --attempt 1` | `394caae51b5963fa` |  | gate=acceptance-evidence status=verified commit=9179fc5ced6a543ca557d877f389c1f3e8c987fe run_id=45521850054 attempt=1 |
