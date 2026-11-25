# Slice hold-management — acceptance audit

- Tickets: HM-01 (#178), HM-02 (#182), HM-03 (#186), HM-04 (#193), HM-05 (#194), HM-06 (#199) · Commit: `9179fc5ced6a543ca557d877f389c1f3e8c987fe` · Date: 2026-11-25

## A. Acceptance evidence

GitHub confirms AFS acceptance run [45521850054, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/45521850054) completed successfully in `martins-vds/ai-factory-synthetic-target` on `main` for this commit. The graph/understand, acceptance, and publish jobs all succeeded. The verified result binds the acceptance gates and target graph to this exact commit; its source and template tree hashes are `1bc2e8bd54c267473db993f018958e87a044028b` and `6b84672cc62e3cce89b41b562c7f10562d2caa58`. The local source checkout is read-only at locked SHA `96d50b85a9a456d9c0a58f080414b3badb501e59`.

The fetched run at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/runs/acceptance-45521850054-1` passed `afs-acceptance verify` for commit `9179fc5ced6a543ca557d877f389c1f3e8c987fe`, run 45521850054, attempt 1. Its `result.json` was copied unchanged to `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/acceptance-runs/45521850054-1.json`; both files have SHA-256 `310d9b501eaba4337ac920f7364a2628bfa1234d8d51b320ccf8d0fbae8dda22`. The Actions artifact `afs-acceptance-9179fc5ced6a543ca557d877f389c1f3e8c987fe-45521850054-1` is retained through 2026-12-25 01:11:18 UTC. Its HM-ACCEPT journal data rows are appended unchanged to `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/runs/HM-REAUDIT.md`.

| Gate | Verified result |
|---|---|
| Source graph | Pass; 11 entry points, 9 reaching data |
| Target graph | Pass; 30 entry points, 21 reaching data; built for commit `9179fc5ced6a543ca557d877f389c1f3e8c987fe` |
| Build and idiom | All passed |
| Tests | `pytest -q` passed |
| Spec | 59 overall cases, 0 failed, 0 pending; all hold-management cases passed |
| CRAP | Maximum 7.0 across 72 methods; threshold 30 |
| Full mutation | Score 0.921; threshold 0.8; 406 killed, 35 survived, 29 files; `base=all` |
| Layering | 3 contracts, 0 violations, 1 known |

These are the fetched Actions results, not gates rerun by this auditor. The required local source-side freshness and graph checks also passed; their output is in the HM-REAUDIT journal. The accepted target graph is inspectable at `origin/afs/acceptance/45521850054-1:graph/target/full/graph-check.md`.

## B. Characterization and test-first evidence

All six ledger entries identify characterized, in-scope capabilities, target components, and evidence. This audit checked the target services, views, repository, model, and migration against those entries, then matched each capability to the passing acceptance spec and target tests listed in section D. The hold code, tests, specs, ledger entries, and precedence recording are unchanged between the accepted commit and this audit checkout. The HM-01 customer-spec commit (`8e42a0c`) precedes the HM-03 implementation commit (`9bf7ed1`); the HM-03 journal records the focused `loan-query-red` failure followed by `loan-query-green` pass at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/runs/HM-03.md:8-9`.

## C. Customer spec and replay media types

The six per-capability spec files account for the hold ledger rules. The verified spec log lists every hold-management case as `PASS`, including the three combined-refusal cases, successful listing and cancellation recordings, and the separate three-/four-active-hold boundary cases. The replay resolver copies recorded `content_type` into the replay expectation (`/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-spec:520-523`) and compares the recorded and target media types (`/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-spec:774-780`, charset ignored). The successful GET `/holds`, successful cancellation, and all three precedence recordings specify `text/plain`; the passing replays now check these responses as well as status and body.

The three precedence recordings in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/characterization/source/goldens/hold-precedence.json` cover available-book vs limit, borrower vs duplicate, and duplicate vs limit. Each recorded response is `409 text/plain` with its corresponding first refusal. The file's SHA-256 is `8e1a17a74b80c95c1d8ad87074f0c7974500762159456cca268df071d2524b87` at its introduction (`da30d894`), the HM-04 recording commit (`f50f869`), and the accepted commit; the working file has the same hash. The recordings were not altered.

The five hold-ID masks are `(?m)^H[0-9]+(?=;)`; they leave the rest of each line and response exact. The customer ruling remains preserve: a fourth active hold is allowed and a fifth is refused.

## D. Capability coverage (gate 7)

| Ledger capability | Target and inspected evidence | Audit |
|---|---|---|
| `hold.place` | `HoldApplication.place` and `hold_collection` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/services.py` and `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/views.py`; tests and `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.place.yaml` cases 1–13 | Required fields, loan/borrower and duplicate refusals, hold limit, ID/date, and all three precedence combinations have passing evidence. `test_first_refusal_wins_for_combined_placement_refusals` checks the same three ordered refusals. |
| `hold.list-active` | `HoldApplication.list_active[_text]`, `DjangoHoldRepository.active`; service/repository tests in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/`; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.list-active.yaml` cases 1–7 | Sequence order, optional ISBN filtering, inclusive expiry, cancellation exclusion, empty newline, and recorded success media type are covered by passing tests/replays. |
| `hold.cancel` | `HoldApplication.cancel`, `DjangoHoldRepository.cancel`; tests in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/`; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.cancel.yaml` cases 1–5 | Unknown/already-cancelled outcomes, expired-but-cancellable behavior, successful response and active-list removal are covered. The successful replay also verifies recorded `text/plain`. |
| `hold.repository` | `DjangoHoldRepository`; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/test_repository.py`; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.repository.yaml` cases 1–4 | Filtering/order, next sequence/ID, persisted readback, concurrent placement, and PostgreSQL rollback after failed INSERT and UPDATE are evidenced. The rollback tests assert the failed placement is absent and cancellation remains unset. |
| `hold.storage` | `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/models.py`, `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/migrations/0001_initial.py`; storage spec cases 1–4 and persistence/repository tests | Persisted fields, 30-day expiry, inclusive expiry day, cancellation exclusion, and exposed hold details match the characterized rules. |
| `data.hold-seed-record` | `seed_holds` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/migrations/0001_initial.py`; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/test_endpoints.py::test_seeded_hold_matches_the_characterized_record`; two spec cases | H1, sequence 1, member `bo`, ISBN `9780134685991`, placement date `2026-01-05`, and null cancellation date match the recorded seed. |

## E. Design, ruling, and flow

HM-02's decomposition is reflected in the target: the view is an HTTP adapter; the hold application owns `LoanStateLookup`; the composition root injects the loan application; the loan query and repository remain in the loans context. Placement checks are short-circuited in sequence and hold policy does not import Django models. This matches the design in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/plan/hold-management.md`.

Issue #170's human comment rules **preserve**: three active holds permit a fourth, while four reject a fifth with 409. The implementation uses `active_count_for_member(...) > 3`; the unit and spec cases establish both boundaries. No divergence was found.

The slice YAML at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/slices/hold-management.yaml` lists the three hold anchors. In the accepted target graph, GET `/holds` routes to `hold_collection[GET]` → `HoldApplication.list_active_text` → `list_active` → `DjangoHoldRepository.active` → reads `holds_hold`; placement routes through `hold_collection[POST]` → `HoldApplication.place` → `DjangoHoldRepository.create` and reaches both `holds_hold` and `loans_loan`; cancellation routes to `hold_cancel` → `HoldApplication.cancel` → repository lookup and reads `holds_hold`. The accepted knowledge graph also contains calls from `HoldApplication.cancel` to both repository `find` and `cancel`. These per-method paths match `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/views.py`, `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/services.py`, and `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/repository.py`. No graph inconsistency remains.

## F. Surviving mutants

The verified full run reports 35 survivors and a score above threshold. Hold survivors #108 (GET content type) and #118 (successful cancellation content type) remain in the `pytest` mutation artifact; that mutation command does not run the AFS spec. The separately passing spec replays now compare the recorded response media types, so these survivors do not leave the prior equivalence evidence gap open. Survivor #107 changes the GET ISBN query key, which the passing filter spec exercises. Other survivors include missing-field defaults (covered by missing-value replays/service tests), internal data/model details and the advisory lock; no additional observable hold capability gap was found. All survivor diffs are in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/runs/acceptance-45521850054-1/mutants.md`.

## G. Gaps and verdict

The four prior HM-AUDIT gaps are closed by the evidence above. No missing, misplaced, broken-flow, integration, or untested capability gap was found; the accepted target graph has no inconsistency. **Verdict: `complete` for this audit.** The operator's side-by-side sign-off under ADR-0031 remains pending and is not granted by this report.
