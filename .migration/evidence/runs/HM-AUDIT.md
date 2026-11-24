# Run journal: HM-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-24T12:48:59+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-24T12:49:13+00:00 | source-graph | 0 | 0.39 | `bash -lc 'python .migration/harness/tools/check_graph_fresh.py --require source && python .migration/harness/tools/graph_gate.py --side source'` | `3ad7d0a76c1f322d` |  | gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125 |
| 2026-11-24T12:49:49+00:00 | fetch-acceptance | 0 | 0.3 | `python .migration/harness/tools/afs-acceptance fetch --run-id 45394010303 --attempt 1 --dest .migration/runs/acceptance-45394010303-1` | `928daa0ff7741933` |  |  |
| 2026-11-24T12:50:02+00:00 | verify-acceptance | 0 | 0.08 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-45394010303-1 --commit a851a7e25d8c4646f1d18f0d778ffa06f046e993 --run-id 45394010303 --attempt 1` | `b9c7b87038decae7` |  | gate=acceptance-evidence status=verified commit=a851a7e25d8c4646f1d18f0d778ffa06f046e993 run_id=45394010303 attempt=1 |
