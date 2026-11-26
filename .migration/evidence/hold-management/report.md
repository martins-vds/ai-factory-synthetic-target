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

## H. HM-ACCEPT slice acceptance update

### Acceptance run and audits

The verified AFS acceptance run [45521850054, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/45521850054) passed on `main` commit `9179fc5ced6a543ca557d877f389c1f3e8c987fe`. It recorded 59 spec cases with 0 failures, passing source and target graphs, CRAP maximum 7.0, 0 layering violations, and full mutation score 0.921 (406 killed, 35 survived; threshold 0.8). No acceptance gates were rerun for this acceptance ticket.

| Audit | Issue / PR | Result |
|---|---|---|
| HM-AUDIT | #189 / #190 | `gaps-remain`; superseded after HM-04, HM-05 and HM-06 addressed its findings. |
| HM-REAUDIT | #201 / #202 | `complete`; six capabilities checked, no gaps or graph inconsistencies. |

### Spec mutation report

The required report run was `.migration/harness/tools/afs-run --ticket HM-ACCEPT --name spec-mutation -- python .migration/harness/tools/afs-mutation --all --spec`. It passed as a report command in 673.81 seconds and recorded **`spec_mutation_score: 0.510`** (225 killed, 216 survived, 0 skipped, 29 files, base `all`; threshold 0.8). This is a characterization report, not an acceptance gate, and does not replace the passing full-mutation gate score above. The raw run and its `AFS-RESULT` are in [.migration/evidence/runs/HM-ACCEPT.md](../runs/HM-ACCEPT.md); the tool-generated survivor diffs are in [.migration/evidence/mutants/HM-ACCEPT.spec.md](../mutants/HM-ACCEPT.spec.md).

The all-spec run spans the project's customer cases, so survivors also occur outside hold management. The following maps every survivor ID to the changed behavior or property that its customer cases did not distinguish. Internal representation and storage-constraint survivors are noted as such; they are not claims of additional hold API failures.

| Source | Survivor IDs | Behavior or property not pinned down by those cases |
|---|---|---|
| `src/holds/services.py` | #1, #17; #3, #5, #7, #9, #11, #13, #15; #33 | Hold value-object mutability; internal failure-code values; the exact whitespace-only member validation branch. |
| `src/holds/views.py` | #104, #116 | Whether unsupported methods on the hold collection and cancellation endpoints are rejected by their method guards. |
| `src/holds/repository.py` | #15, #16; #28; #34, #35 | Advisory-lock key / lock use under concurrent placement; first sequence value when storage is empty; atomicity of placement and cancellation writes. |
| `src/holds/models.py` | #62, #67, #69; #65; #72, #73; #76 | Maximum lengths of hold ID, member, and ISBN; uniqueness of sequence; nullable/blank cancellation-date storage; model-default ordering (the endpoint repository applies its own ordering). |
| `src/loans/repository.py` | #51, #52; #56, #57 | Transaction boundaries on loan writes; active-loan filtering and the lookup's returned status when a loan is absent or returned. |
| `src/loans/services.py` | #1; #5; #6; #12; #14 | Loan value-object mutability; separator in multi-loan text; missing-loan lookup; CSV line ending; formatting of a missing return date. |
| `src/loans/models.py` | #131, #134, #136; #139, #140; #143 | Loan ID/member/ISBN maximum lengths; null/blank handling for return date; model-default ordering. |
| `src/loans/forms.py` | #93, #94, #95, #96; #104, #108 | Whether member and ISBN values are stripped or their fields exist; exact required-field validation message. |
| `src/loans/urls.py` | #82, #83, #84, #85, #86 | The five loan detail/catalog/new/return route paths. |
| `src/loans/views.py` | #1, #2; #3, #4, #5; #6, #8, #22, #23, #24, #54, #65; #11, #18, #21, #52, #53, #59, #63, #64, #70 | Loan list/detail templates and contexts; detail lookup; supported-method guards; text response media types. |
| `src/loans/views.py` | #14, #15, #16, #17; #20; #25, #26, #27, #28, #29, #30, #31; #32, #33, #34, #35, #36, #37, #38; #39, #40, #41, #42, #43, #44, #45, #46, #47 | Lending validation/error rendering and status; form binding and policy execution; successful status; HTMX detection, partial templates, context fields, and redirect destinations. |
| `src/loans/views.py` | #48, #49, #50, #51; #57, #58; #61, #62; #66, #67, #68, #69; #71, #72, #73, #74, #75, #76, #77, #78, #79, #80, #81, #82, #83 | Loan detail/return missing-ID and already-returned responses; return operation and status; HTMX return rendering, updated-state branch, failure template/context/status, and redirect. |
| `src/reports/composition.py` | #80 | Whether the monthly-report application is composed and available to its command. |
| `src/reports/services.py` | #1, #2, #3; #4, #5, #6, #7, #8, #9; #10, #11; #12, #13, #14, #15, #16, #17; #18, #19; #20, #21, #22; #23, #24, #25; #26, #27, #28; #29, #30; #31, #32; #33, #34 | Report value-object mutability/dataclass construction and default totals; injected loan/fee dependencies; monthly period boundaries and accumulator initialization; loan/late-return/fee aggregation, late-date boundary, and report sort order. |
| `src/reports/management/commands/monthly_report.py` | #119, #120; #121; #122, #123, #124, #125; #126, #127, #128, #129; #130 | Command help text and report retrieval; CSV buffer/writer and line ending; each output header; final stdout newline behavior. |
| `src/core/database.py` | #81, #82 | Database health-check query and returned result column. |
| `src/fees/services.py` | #39, #41 | Mutability of fee/payment value objects. |
| `src/fees/urls.py` | #150 | Payment-page route path. |
| `src/fees/views.py` | #35, #42, #50, #56; #57, #58, #59, #60, #61, #62; #63, #64, #65, #66, #67; #68, #69, #70, #71, #72, #73, #74, #75, #76, #77 | Supported-method guards; payment gateway result and 404 response; payment status/context fields; HTMX selection, status/detail templates, and template context. |
| `src/fees/gateway.py` | #78, #79; #85, #86, #88, #89; #91, #92 | Default gateway URL; response charset fallback/decoding; gateway-failure message. |
| `src/library_info/urls.py` | #156, #157 | Legacy and UI about-page route paths. |
| `src/library_info/views.py` | #109, #112; #110, #113; #111 | Supported-method guards; legacy/UI about templates; legacy response media type. |

HM-REAUDIT observed that full pytest mutation survivors #108 (hold-list content type) and #118 (successful-cancellation content type) were not killed by the pytest-only run. Neither content-type change is a survivor in this spec-mutation report: the spec's recorded-media-type replays kill both. The surviving hold-view mutants here are method-guard removals (#104, #116), not media-type changes.

### Ledger status

Every `hold-management` ledger entry is evidenced as migrated; the existing ledger statuses were already correct and are retained.

| Ledger entry | Status |
|---|---|
| `hold.place` | `migrated` |
| `hold.list-active` | `migrated` |
| `hold.cancel` | `migrated` |
| `hold.repository` | `migrated` |
| `hold.storage` | `migrated` |
| `data.hold-seed-record` | `migrated` |

### Human side-by-side check — requested

Compare the pinned legacy behavior against the target, using the same inputs and recording status, response body/line, and relevant persisted state:

- `GET /holds`: compare the complete active list and the result for `?isbn=<ISBN>`, including ordering, empty-result formatting, and response media type.
- `POST /holds`: compare every refusal's exact message and status; compare a successful placement's complete line; verify that a fourth active hold is allowed and a fifth is refused.
- `POST /holds/{id}/cancel`: compare successful and refusal responses, and verify that an expired but uncancelled hold can still be cancelled.
- Startup seed: compare the H1 record's ID, sequence, member, ISBN, placement date, and null cancellation date.

The check is requested only. The human approver must record its outcome; this report does not grant sign-off.
