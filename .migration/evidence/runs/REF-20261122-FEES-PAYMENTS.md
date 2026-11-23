# Run journal: REF-20261122-FEES-PAYMENTS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-22T23:44:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:45:14+00:00 | behavior-baseline | 0 | 14.43 | `pytest -q tests/fees` | `e0d8e0017f6df3a4` |  |  |
| 2026-11-22T23:46:07+00:00 | behavior | 1 | 40.27 | `pytest -q tests/fees` | `3d7479ca1e7b0b8f` | /opt/hostedtoolcache/Python/3.13.18/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-22T23:46:23+00:00 | behavior | 0 | 10.22 | `pytest -q tests/fees` | `feed79f26e1dcffa` |  |  |
| 2026-11-22T23:46:45+00:00 | build-compile | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:46:46+00:00 | build-django-check | 0 | 0.29 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-22T23:46:58+00:00 | behavior | 0 | 10.17 | `pytest -q tests/fees` | `40b42e52fa95b38a` |  |  |
| 2026-11-22T23:47:01+00:00 | spec | 0 | 2.25 | `python .migration/harness/tools/afs-spec run` | `6c0349a262bf1d6b` | AFS-RESULT gate=spec cases=20 failed=0 pending=0 | gate=spec cases=20 failed=0 pending=0 |
| 2026-11-22T23:47:04+00:00 | idiom-ruff | 0 | 0.01 | `ruff check src config manage.py tests` | `82b3e6a6c090a576` |  |  |
| 2026-11-22T23:47:04+00:00 | idiom-format | 0 | 0.01 | `ruff format --check src config manage.py tests` | `aec51819fa2b338a` |  |  |
| 2026-11-22T23:47:04+00:00 | idiom-layers | 0 | 0.06 | `python .migration/harness/tools/check_layers.py` | `d970c18c2dcfe59c` |  | gate=layering contracts=3 violations=0 known=1 |
| 2026-11-22T23:47:05+00:00 | idiom-ui | 0 | 0.13 | `python .migration/harness/tools/check_ui.py` | `b9ae03306fe277bb` |  | gate=ui scope="templates changed since origin/main" templates=0 findings=0 |
| 2026-11-22T23:47:23+00:00 | crap-coverage | 0 | 15.07 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `25f44fd872956b63` |  |  |
| 2026-11-22T23:47:23+00:00 | crap-lizard | 0 | 0.05 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:47:23+00:00 | crap | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `a47a2d4e983b31df` |  | gate=crap max=7.0 threshold=30 over=0 methods=46 |
| 2026-11-22T23:52:02+00:00 | mutation-changed | 0 | 274.98 | `python .migration/harness/tools/afs-mutation` | `98110dc590d31050` |  | gate=mutation score=1.000 threshold=0.8 killed=61 survived=0 files=2 base=origin/main |
| 2026-11-22T23:52:16+00:00 | regression | 0 | 13.06 | `pytest -q` | `8a9e1a94e6eeed01` |  |  |
