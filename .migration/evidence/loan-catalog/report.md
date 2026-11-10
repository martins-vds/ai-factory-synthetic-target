# Loan catalog slice — acceptance audit

- Tickets: LL-01 (#59), LL-AUDIT (#82) · Commit: `88605f51a9b919dd3aba3aad04bbaa307b2f24d2` · Date: 2026-11-09
- Acceptance run: [42714661632, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42714661632)
- Artifact: `afs-acceptance-88605f51a9b919dd3aba3aad04bbaa307b2f24d2-42714661632-1`; expires 2026-12-09.

## A. Graph refresh and acceptance evidence

The pinned source SHA is `563c316ed51462b08fd6e58f3781a3c8b2890453`. In this audit, source graph freshness and `graph_gate.py --side source` both passed; the source graph reports the two slice anchors, `GET /loans` and `GET /loans/{id}`, reaching `LOAN`. The run's target graph was independently verified for commit `88605f51a9b919dd3aba3aad04bbaa307b2f24d2`; its target tree hashes are recorded in the verified `result.json`. On this continuation, the artifact was fetched again and re-verified in a detached worktree at that exact commit because the audit branch now contains post-run audit outputs outside the execution-input allowlist. The accepted source and target execution inputs match the reviewed run.

GitHub confirms the run is in `martins-vds/ai-factory-synthetic-target`, on `main`, attempt 1, for the specified commit, with successful graph, acceptance and publish jobs. The workflow at that commit is `.github/workflows/afs-acceptance.yml`; its acceptance job runs the profile gates, uploads evidence with 30-day retention, and its publish job creates `afs/acceptance/42714661632-1`. Fetch and `afs-acceptance verify` both succeeded.

| Gate | Command / evidence | Exit | Notes |
|---|---|---:|---|
| Source graph freshness | `check_graph_fresh.py --require source` (this audit) | 0 | Source graph matches the pinned source. |
| Source graph | `graph_gate.py --side source` (this audit) | 0 | 8 entry points, 6 reach data; no failures. |
| Target graph | Acceptance journal, `graph-target` | 0 | 7 entry points, 4 reach data; all 4 catalog anchors are owned by this slice. |
| Build | `compileall -q src`; `python manage.py check` | 0 | Both passed. |
| Idiom | `ruff check`; `ruff format --check` | 0 | Both passed. |
| Tests | `pytest -q` | 0 | 14 passed. |
| CRAP | Coverage + Lizard + `crap.py --max 30` | 0 | Maximum CRAP 2.0; none over threshold. |
| Full mutation | `afs-mutation --all` | 0 | Score 0.932 (threshold 0.8), 41 killed, 3 survived. |

These are the fetched run's verified results; this audit did not rerun build, tests, CRAP or mutation. Acceptance journal data rows were appended unchanged to `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/runs/LL-AUDIT.md`. The verified `result.json` was copied byte-for-byte to `.migration/evidence/acceptance-runs/42714661632-1.json` (SHA-256 `a7c8444ae0248d7802bd55fd0ceadb99c5c9988d621f9e7bf24184633ca75f4a`).

The target graph paths in `.migration/slices/loan-catalog.yaml` match the generated graph:

- `/loans` → `loan_list` → `list_loans_text` → `LoanRepository.find` → `loans_loan`
- `/loans/<str:loan_id>` → `loan_detail` → `get_loan_text` → `LoanRepository.find` → `loans_loan`
- `/ui/loans/` → `loan_catalog` → `loans_loan`
- `/ui/loans/<str:loan_id>/` → `loan_catalog_detail` → `loans_loan`

The four anchors all reach the loan table, which covers the slice's storage capability. The target graph's non-enforced missing anchors belong to still-open LL-02/LL-03 and other slices, not loan-catalog; no catalog graph inconsistency was found.

## B. Top-down findings

The two characterized text endpoints retain their status, content type, output ordering, trailing newline, and not-found response in the target tests and source goldens. The target also exposes the two planned reading-room routes. `tests/test_ui_smoke.py::test_loan_catalog_renders_in_browser_and_admin_is_removed` exercises the catalog page in a browser and confirms the intentional removal of Django admin; `tests/loans/test_catalog.py::test_browser_detail_page_shows_loan_dates` covers the detail page.

## C. Bottom-up findings

The target uses PostgreSQL-backed Django models and migrations, with ordering and due-date behavior in the model, repository reads/writes behind `LoanRepository`, and CSV quoting in the text-export service. The real PostgreSQL service and full target suite passed in the verified acceptance run. The separate LL-01 verifier journal also records successful PostgreSQL startup checks, including `PORT` override and default-port behavior.

## D. Capability coverage

All nine capabilities listed for LL-01 in the plan were checked against target components and evidence:

| Ledger capability | Target component(s) | Evidence and audit result |
|---|---|---|
| `application.build` | `config.settings`, `config.urls`, initial migration | Build and idiom gates passed; browser smoke test covers the catalog entry point. Admin omission is explicitly in the LL-01 scope update. |
| `application.startup` | `Makefile.run`, settings, URLs, initial migration | `Makefile` binds `0.0.0.0`, defaults to port 8080 and honors `PORT`; LL-01 records startup and persistent-migration checks; verifier records PostgreSQL startup pass. |
| `data.loan-storage` | `Loan`, `LoanRepository` | A saved row is available to a later request; PostgreSQL service passed. Persistent storage rather than reset-on-restart is approved by #42. |
| `data.seed-records` | `seed_loans` in `0001_initial` | The seeded-record endpoint test and golden cover L1–L3; #42 approves seeding only a fresh database. |
| `repository.transactions` | `LoanRepository.create` | `test_repository_write_rolls_back_failed_transaction` verifies rollback on a duplicate-key failure; implementation uses `transaction.atomic`. |
| `loan.due-date` | `Loan.due_on` | `test_due_date_is_fourteen_calendar_days_after_lending` covers the 14-day rule, including leap day. |
| `loan.get` | `loan_detail`, `get_loan_text` | Exact 200 response and missing-id 404 tests match the characterization goldens. |
| `loan.list` | `loan_list`, `list_loans_text` | Seeded output and ID ordering tests match the characterization goldens. |
| `loan.text-export` | `loan_line` | Delimiters, quotes and line breaks are covered; approved quirk #43 authorizes the escaped format. |

LL-01's journal provides test-first evidence: `red-list-endpoint` then `green-list-endpoint`, `red-reading-room-ui` then `green-reading-room-ui`, and `red-transaction-rollback` then `green-transaction-rollback`. The later full acceptance suite passed.

Quirk rulings were checked directly: #42 approves persistent PostgreSQL records and no reseed-over-existing-data on restart; #43 approves quoting delimiter, quote and line-break characters in export. Their respective ledger entries document the divergence and link the ruling.

The three surviving mutants alter the API detail route, catalog route and catalog-detail route to `XX...XX`. They are not equivalent route changes. However, the existing endpoint and browser tests issue requests to each unmutated route and assert successful behavior; the acceptance suite also passed all 14 tests. The mutation artifact does not include per-mutant test traces, so it does not establish a missing catalog capability. I concur with the verifier's treatment as mutation-selection/tool artifacts for capability coverage, while retaining the three survivors in this report rather than treating the score as proof that they were killed.

## E. Tickets created

No capability gap was found, so no new capability ticket was created. No issue was opened or changed during this read-only audit.

## F. Final gap list

- Missing capability, misplaced responsibility, broken flow, missing integration, or untested capability: none found among the nine LL-01 ledger entries.
- The verified acceptance result is now archived at `.migration/evidence/acceptance-runs/42714661632-1.json`; the return cites this committed path, satisfying the ADR-0035 evidence requirement.
- Human flow sign-off under ADR-0031 remains outstanding as the slice coordinator's next step; it is not an audit gap or part of the auditor's verdict.

## G. Assessment

The loan-catalog audit is complete: all 9/9 planned ledger capabilities have passing evidence, no catalog graph or functional gaps were found, and the verified acceptance result is archived. The auditor verdict is `complete`. Slice acceptance remains pending the operator side-by-side sign-off requested by the slice coordinator under ADR-0031; this audit neither performs nor grants that sign-off.
