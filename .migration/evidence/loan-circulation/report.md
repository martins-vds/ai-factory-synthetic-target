# Loan circulation — acceptance evidence

- Tickets: LL-02 (#61), verifier #84 / PR #85 · Commit: `70fef8e7bc822092770b04b1bf9b5288e04d8bb6` · Date: 2026-11-10
- Re-audit: LC-REAUDIT (#100), following PR #98; the archived acceptance run is unchanged. No gates or mutation were rerun.
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
| `loan.lend` | Ledger now names `src.loans.forms.LoanForm`, `src.loans.services.LoanApplication.lend`, `src.loans.views.loan_collection`, and `src.loans.views.loan_lend_page`; each resolves to the current implementation. `loan_collection` delegates POST to `loan_lend`, which calls `LoanApplication.lend`. | `tests/loans/test_catalog.py` exercises POST `/loans` with a 201 response, current lend date, 14-day due date, persisted values, delimiter escaping, missing/blank field errors, and browser/HTMX lending. | Behavior is present and connected end to end; the previously misplaced ledger references were corrected by PR #98. Blank rejection and delimiter escaping follow approved rulings #39 and #43. |
| `loan.return` | Ledger names `src.loans.views.loan_return`, `src.loans.views.loan_return_page`, and `src.loans.urls`; each resolves to its current implementation. | Tests assert successful API return, exact 404 and 409 bodies/statuses, browser/HTMX return, unknown-loan handling, and repeat-return UI errors. | Present and connected end to end; repeat behavior follows approved ruling #41. |
| `loan.return-date` | Ledger now names `src.loans.repository.DjangoLoanRepository.mark_returned` and `src.loans.services.LoanApplication.return_loan`; both resolve to the current persistence adapter and application use case. | Tests assert first return persists today's date and a repeated API or browser return preserves the original date. `tests/loans/test_services.py` exercises the application service with injected fake repository and clock. | Behavior is present and connected end to end; the previously misplaced ledger references were corrected by PR #98. Approved ruling #41 is represented in behavior and ledger notes. |

The re-audit confirmed all three circulation ledger entries name their current implementation components. The two `misplaced` references from LC-AUDIT were corrected in PR #98, and migration validation passes with the target-component existence check. There are no remaining ledger gaps for this slice.

## Port/adapter design

`LoanApplication` depends on its application-owned `Clock` and `LoanRepository` protocols (`src/loans/services.py`); `composition.py` wires the Django repository and system clock. `DjangoLoanRepository` owns ORM persistence and uses a transaction/row lock for return updates. The service tests use in-memory fakes and a fixed clock; the acceptance suite runs with the configured PostgreSQL service.

## Graph paths and discrepancy

The verified target graph records the return API path through `loan_return` → `LoanApplication.return_loan` → `LoanRepository.mark_returned` → `loans_loan`, and the browser lending and return paths through the expected application ports and persistence adapter. All four target anchors in `.migration/slices/loan-circulation.yaml` match routes.

The unchanged accepted target graph still has one path that is not faithful to the request branch: for `POST /loans`, `graph-check.md` reports `loan_collection` → `LoanApplication.list_loans_text` → `LoanRepository.all` (a read). The inspected view branches POST to `loan_lend`, which calls `LoanApplication.lend`; API behavior tests exercise that route and assert the resulting persisted loan. This remains a graph-path inconsistency, not a missing or broken capability, and is reported for coordinator follow-up.

## Surviving mutants

The full run reports 11 survivors: six URL literals, four HTTP-method decorators, and `LoanForm.Meta.model`. I independently checked their behavior coverage rather than treating the aggregate mutation score as proof: tests invoke the corresponding API and browser routes; `test_loan_write_routes_reject_unsupported_methods` asserts 405 responses for unsupported methods; and successful API/browser lending tests assert the created database record. The verifier documents the module-level mutation test-selection limitation. These survivors do not show an uncovered circulation behavior in the inspected suite.

## Human check

The independent re-audit reviewed all three ledger capabilities. Their target references now resolve, with no ledger gaps; the graph-path inconsistency remains for coordinator follow-up. The operator's side-by-side flow sign-off is the coordinator's subsequent step and is not represented as a gap in this verdict.
