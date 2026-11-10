# Slice fees-payments — acceptance evidence

- Tickets: LL-03 (#63), re-verification (#96) · Commit: `8f9a11640eef9801378f3db53a76903363c5e5b5` · Date: 2026-11-10

## Acceptance provenance

AFS acceptance gates run [42912984554](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42912984554), attempt 1, completed successfully for the exact commit above. The published branch resolved to `3193ed5ed82f852630699e5f5274dfbbb47a0117`; `afs-acceptance verify` independently verified the fetched directory against the run ID, attempt, commit, tracked inputs, and gate evidence. The archived result is `.migration/evidence/acceptance-runs/42912984554-1.json`, byte-identical to the fetched `result.json` (SHA-256 `d819963580a985d4e441f23f599dfc1fc01d786dde2d197d10f71087cbb08364`). The verified download remains at `.migration/runs/acceptance-42912984554-1` for review. The Actions artifact expires 2026-12-10 22:28:25 UTC (30-day retention).

The auditor checkout is the acceptance commit plus audit evidence only; no fees implementation, test, ledger, or graph-input paths changed after that commit.

## Gates

All rows below are from the verified acceptance artifact; the original rows are preserved in `.migration/evidence/runs/LF-AUDIT.md`.

| Gate | Command | Exit | Notes |
|---|---|---:|---|
| Runtime | `check_runtime.py` | 0 | Python 3.13 |
| Harness integrity | `check_installed.py` | 0 | Installed pins valid |
| Services | `afs-services check` | 0 | Test services healthy |
| Graph freshness | `check_graph_fresh.py --require source,target` | 0 | Both sides fresh |
| Source graph | `graph_gate.py --side source --require-graph` | 0 | 8 entry points; 6 reach data |
| Target graph | `graph_gate.py --side target --require-graph --enforce-ownership` | 0 | 23 entry points; 18 reach data; 13 owned, none unowned |
| Build | `python -m compileall -q src`; `python manage.py check` | 0 | Both steps passed |
| Idiom | `ruff check src config manage.py tests`; `ruff format --check src config manage.py tests` | 0 | Both steps passed |
| Tests | `pytest -q` | 0 | Full suite |
| CRAP | Coverage pytest, `lizard --csv src`, then `crap.py ... --max 30` | 0 | Max 7.0; threshold 30 |
| Full mutation | `python .migration/harness/tools/afs-mutation --all` | 0 | 0.975; threshold 0.8; 236 killed, 6 survived, 15 files |

The auditor did not rerun build, tests, CRAP, or mutation.

## Characterization (tier A)

The LL-03 differential record in `.migration/evidence/runs/LL-03.md` and the characterization goldens establish:

- Fee calculation uses the source-predicted date rule, two-day waiver, 25 cents per late day, and $10 cap. The target unit tests cover 0, 1, 2, 3, 11, and 100 late days and a returned loan's `returned_on` date (`tests/fees/test_fee_calculation.py`).
- `GET /fees/{id}` matches the characterized HTML and unknown-loan 404 body. The browser fee page displays the same capped amount.
- Payment sends an empty-body `POST /charge?loan={id}` to the configured/default gateway URL; a 200 response is returned as 200, other responses map to 502, and unknown loans return 404 without a gateway call (`.migration/characterization/source/goldens/gateway.json`, `tests/fees/test_endpoints.py`).
- Test-first evidence is chronological in the LL-03 journal: the focused fees run failed an expected-200 assertion at 02:04:21 UTC, then passed at 02:04:36; the implementation commit was recorded at 02:09:50 UTC. The initial collection failure at 02:03:42 is not treated as the red behavior assertion.

## Capability coverage (gate 7)

All three `fees-payments` ledger entries are `migrated`, have target components and differential evidence, and are checked against the acceptance graph and their cited tests.

| Ledger capability | Target and evidence | Audit |
|---|---|---|
| `fees.calculation` | `FeeApplication.fee_for`; `tests/fees/test_fee_calculation.py`; fee golden and LL-03 run record | Formula, returned-date behavior, boundaries, grace period, and cap match the described contract. |
| `fees.page` | `fee_detail`, `fee_page`, routes and detail template; `tests/fees/test_endpoints.py`, including browser flow and seed-restoration test | API HTML/404 and browser fee display/payment action are covered. |
| `integration.payment-gateway` | `FeeApplication.pay`, `PaymentGateway` Protocol, `HttpPaymentGateway`, `DjangoFeeLoanRepository`, and `composition.py`; gateway golden and endpoint/gateway tests | Port is owned by the application service; composition wires the repository, clock, and HTTP adapter. Local HTTP fixture verifies the real request shape and responses. |

The accepted target graph lists all four slice anchors and traces each to `loans_loan`: fee detail and page through `fee_for`; API payment through `pay`; UI payment reaches the loan table through its fee re-read. The UI payment shortest data path does not display its outbound gateway branch; inspection of `payment_page` shows `_gateway_result` runs before that re-read, and the UI payment test verifies the gateway request. This is a path-selection detail, not a graph/code contradiction. The unconnected `templates/fees/payment-status.html` is a rendered fragment, not a ledger capability or standalone route. The payment gateway is external I/O, so its request/response path is evidenced by adapter code, golden data, and tests rather than a database node.

### Quirk rulings

- #40 approved fixing the swallowed-interruption behavior. `HttpPaymentGateway` raises `PaymentGatewayFailure` chained from `InterruptedError`; the endpoint maps it to 502, and the tests check both the failure response and preserved cause. This matches the ruling.
- #42 approved persistent loan storage. The fees ticket does not alter storage; the browser test's seed-restoration fixture restores seeded rows after the live-server test, and the targeted assertion confirms they remain available. No reset-on-startup behavior was reintroduced.

### Surviving mutants

The verified full run reports six survivors. Four are in loan views/routes/forms, outside this slice. The two fees survivors change `Fee` and `GatewayResponse` from frozen to mutable dataclasses (`.migration/runs/acceptance-42912984554-1/mutants.md`). The reviewed fee/payment boundaries expose HTTP behavior, not these internal value objects; no path mutates either value. I therefore assess these two as equivalent for the specified observable contract, not as missing capability coverage. They remain documented survivors rather than being represented as killed.

## Human check

Independent auditor review completed 2026-11-10. No missing, misplaced, broken-flow, integration, or untested capability gap was found; graph inconsistencies: none. Audit verdict: **complete**. Coordinator/operator flow sign-off remains the next step (ADR-0031); this report does not substitute for it.
