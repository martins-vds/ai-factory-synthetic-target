# Loan circulation — acceptance evidence

- Tickets: LL-02 (#61), verifier #84 / PR #85 · Commit: `70fef8e7bc822092770b04b1bf9b5288e04d8bb6` · Date: 2026-11-10
- Acceptance: [Actions run 42752283868, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42752283868), successful on `main` at the audited commit. The verified artifact is `afs-acceptance-70fef8e7bc822092770b04b1bf9b5288e04d8bb6-42752283868-1`, retained until 2026-12-10. Its unchanged `result.json` is archived at `.migration/evidence/acceptance-runs/42752283868-1.json`; `afs-acceptance verify` returned `status=verified` for the expected commit, run, and attempt. The artifact journal rows are appended unchanged to `.migration/evidence/runs/LC-AUDIT.md`.

## Gates

| Gate | Command | Exit | Notes |
|---|---|---:|---|
| Source graph freshness | `check_graph_fresh.py --require source` (this audit, through `afs-run`) | 0 | Fresh source graph |
| Source graph | `graph_gate.py --side source` (this audit, through `afs-run`) | 0 | 8 entry points, 6 reaching data |
| Acceptance graph and environment | Acceptance workflow runtime, harness-integrity, services, graph freshness, graph-source, graph-target | 0 | Target graph is for the audited commit; 16 entry points, 12 reaching data |
| Build | `python -m compileall -q src`; `python manage.py check` | 0 | Both acceptance steps passed |
| Idiom | `ruff check src config manage.py tests`; `ruff format --check src config manage.py tests` | 0 | Both acceptance steps passed |
| Behavior | `pytest -q` | 0 | Full acceptance suite passed |
| CRAP | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov`; `lizard --csv src`; `crap.py ... --max 30` | 0 | Maximum CRAP 7.0; threshold 30 |
| Full mutation | `python .migration/harness/tools/afs-mutation --all` | 0 | Score 0.920; threshold 0.8; 126 killed, 11 survived |

Gate details and raw-log hashes are in the verified `LC-ACCEPT` artifact and its imported journal rows. I did not rerun tests, build, CRAP, or mutation.

## Characterization and test-first evidence

The three circulation capabilities are tier-A characterized. LL-02's committed journal records failing then passing endpoint, browser, and return tests (including `red-lend-endpoint`/`green-lend-endpoint` and `red-return-date`/`green-return-date`), followed by successful behavior suites. The initial verifier's `changes-required` finding (#78 / PR #79) identified application-policy coupling to Django; the final verifier (#84 / PR #85) records the port remediation and a pass. The final verifier also records passing focused tests for blank fields, repeated browser returns, unknown browser returns, and unsupported methods.

## Capability coverage

| Ledger capability | Target components | Independent code and behavior evidence | Audit |
|---|---|---|---|
| `loan.lend` | Ledger names `src.loans.services.lend_loan`, `LoanForm`, `loan_collection`, `loan_lend_page`; `lend_loan` does not exist. The actual use case is `LoanApplication.lend`. | `tests/loans/test_catalog.py` exercises POST `/loans` with a 201 response, current lend date, 14-day due date, persisted values, delimiter escaping, missing/blank field errors, and browser/HTMX lending. | Behavior is present and connected end to end; the ledger target path is misplaced. Blank rejection and delimiter escaping follow approved rulings #39 and #43. |
| `loan.return` | `loan_return`, `loan_return_page`, `urls` | Tests assert successful API return, exact 404 and 409 bodies/statuses, browser/HTMX return, unknown-loan handling, and repeat-return UI errors. | Present and connected end to end; repeat behavior follows approved ruling #41. |
| `loan.return-date` | Ledger names `src.loans.repository.LoanRepository.mark_returned`, but `LoanRepository` is the protocol in `services.py`; the ORM adapter is `DjangoLoanRepository.mark_returned`. `LoanApplication.return_loan` is present. | Tests assert first return persists today's date and a repeated API or browser return preserves the original date. `tests/loans/test_services.py` exercises the application service with injected fake repository and clock. | Behavior is present and connected end to end; the ledger target path is misplaced. Approved ruling #41 is represented in behavior and ledger notes. |

Two target-component references in the ledger do not resolve to the implementation's current names after re-architecture. The behavior and idiomatic port/adapter implementations exist, so these are `misplaced` ledger gaps, not missing behaviors. They require a follow-up ticket and ledger correction; the auditor's read-only scope did not permit creating that ticket.

## Port/adapter design

`LoanApplication` depends on its application-owned `Clock` and `LoanRepository` protocols (`src/loans/services.py`); `composition.py` wires the Django repository and system clock. `DjangoLoanRepository` owns ORM persistence and uses a transaction/row lock for return updates. The service tests use in-memory fakes and a fixed clock; the acceptance suite runs with the configured PostgreSQL service.

## Graph paths and discrepancy

The verified target graph records the return API path through `loan_return` → `LoanApplication.return_loan` → `LoanRepository.mark_returned` → `loans_loan`, and the browser lending and return paths through the expected application ports and persistence adapter. All four target anchors in `.migration/slices/loan-circulation.yaml` match routes.

One target-graph path is not faithful to the request branch: for `POST /loans`, `graph-check.md` reports `loan_collection` → `LoanApplication.list_loans_text` → `LoanRepository.all` (a read). The inspected view branches POST to `loan_lend`, which calls `LoanApplication.lend`; API behavior tests exercise that route and assert the resulting persisted loan. This is a graph-path inconsistency, not a missing or broken capability; it is reported for coordinator follow-up.

## Surviving mutants

The full run reports 11 survivors: six URL literals, four HTTP-method decorators, and `LoanForm.Meta.model`. I independently checked their behavior coverage rather than treating the aggregate mutation score as proof: tests invoke the corresponding API and browser routes; `test_loan_write_routes_reject_unsupported_methods` asserts 405 responses for unsupported methods; and successful API/browser lending tests assert the created database record. The verifier documents the module-level mutation test-selection limitation. These survivors do not show an uncovered circulation behavior in the inspected suite.

## Human check

The independent auditor reviewed all three ledger capabilities and reports the two misplaced target references above. The operator's side-by-side flow sign-off is the coordinator's subsequent step; it is not represented as a gap in this verdict.
