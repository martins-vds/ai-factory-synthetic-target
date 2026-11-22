# Run journal: REF-20261122-FEES-PAYMENTS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-22T23:44:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:45:14+00:00 | behavior-baseline | 0 | 14.43 | `pytest -q tests/fees` | `e0d8e0017f6df3a4` |  |  |
| 2026-11-22T23:46:07+00:00 | behavior | 1 | 40.27 | `pytest -q tests/fees` | `3d7479ca1e7b0b8f` | /opt/hostedtoolcache/Python/3.13.18/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-22T23:46:23+00:00 | behavior | 0 | 10.22 | `pytest -q tests/fees` | `feed79f26e1dcffa` |  |  |
