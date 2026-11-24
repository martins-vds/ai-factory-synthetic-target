# Slice hold-management — acceptance audit

- Tickets: HM-01 (#178), HM-02 (#182), HM-03 (#186) · Commit: `a851a7e25d8c4646f1d18f0d778ffa06f046e993` · Date: 2026-11-24

## A. Acceptance evidence

GitHub confirms AFS acceptance run [45394010303, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/45394010303) completed successfully in `martins-vds/ai-factory-synthetic-target` on `main` for the commit above. The graph/understand, acceptance, and publish jobs succeeded. The verified result identifies the target graph built for that same commit and records the graph tree hashes. The local source checkout is read-only at the locked SHA `96d50b85a9a456d9c0a58f080414b3badb501e59`.

The fetched run at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/runs/acceptance-45394010303-1` passed `afs-acceptance verify` for the specified commit, run, and attempt. Its `result.json` was copied unchanged to `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/acceptance-runs/45394010303-1.json`; both files have SHA-256 `27b6c6237c17487cbffb1c212238be2c5460548bedba541506beb31dc34960c0`. The Actions artifact is retained through 2026-12-24 12:44:39 UTC. Acceptance journal data rows were appended unchanged to `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/runs/HM-AUDIT.md`.

| Gate | Verified result |
|---|---|
| Source graph | Pass; 11 entry points, 9 reaching data |
| Target graph | Pass; 30 entry points, 21 reaching data |
| Build and idiom | All passed |
| Tests | `pytest -q` passed |
| Spec | 56 overall cases, 0 failed, 0 pending; 36 are hold-management cases |
| CRAP | Maximum 7.0 across 72 methods; threshold 30 |
| Full mutation | Score 0.921; threshold 0.8; 406 killed, 35 survived, 29 files |
| Layering | 3 contracts, 0 violations, 1 known |

These are the fetched Actions results, not gates rerun by this auditor. The only graph gate run in this audit was the required source-side freshness/gate check; it passed. The earlier failed run 45328285967 is excluded; its attempt-2 job log reports a target-graph failure for the unrelated `monthly-report` command path.

## B. Characterization and test-first evidence

The six ledger entries are characterized at tier A and link to SY-08 evidence and hold goldens. Git history confirms the HM-01 spec commit (`8e42a0c`) precedes the HM-03 implementation commit (`9bf7ed1`). HM-03's journal records a failing `loan-query-red` assertion followed by the passing `loan-query-green` run ( `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/evidence/runs/HM-03.md`, rows at 03:23:51 and 03:24:02 UTC). The earlier hold-service collection errors are not treated as behavioral red evidence.

## C. Customer spec

All six per-capability spec files account for the 21 ledger rules. The verified spec log lists all 36 hold cases as `PASS`, including the two separate hold-limit recordings for three and four existing holds. The replay resolver takes the expected HTTP status from the source recording, and the runner compares that status and the body (`/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/harness/tools/afs-spec`: lines 503–516 and 670–672). The spec therefore proves the recorded status/body outcomes, including the preserve ruling.

The five ID masks are `(?m)^H[0-9]+(?=;)`. They match only an `H`-number token at the beginning of a body line, ending immediately before its field delimiter; member, ISBN, dates, separators, line ordering, and response bodies remain unmasked. The regex is narrow for the generated hold identifier.

The replays do not compare response headers/content type. The source recordings set `text/plain` for successful GET, placement, and cancellation responses (`/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/characterization/source/goldens/http.json`). The endpoint tests assert `text/plain` for placement and cancellation failures and successful placement, but not for a successful GET or successful cancellation. The two missing success-header assertions are also represented by surviving mutants #108 and #118; see sections F–G.

## D. Capability coverage (gate 7)

| Ledger capability | Target and inspected evidence | Audit |
|---|---|---|
| `hold.place` | `HoldApplication.place` and its four ordered policy helpers in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/services.py`; `hold_collection`; tests in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/test_services.py` and `test_endpoints.py`; spec cases 1–10 | The required-fields, open-loan/borrower, duplicate, hold-limit, identifier, and date outcomes match the characterized behavior. Source and target both allow a fourth active hold and reject a fifth. The target's checks are in source order. No spec or test combines two simultaneously failing policies, so the characterized first-error precedence is not independently proved. |
| `hold.list-active` | `HoldApplication.list_active[_text]`, `DjangoHoldRepository.active` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/`; service/repository tests; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.list-active.yaml` cases 1–7 | Ordering, optional ISBN filtering, expiry-day inclusion/exclusion, cancellation filtering, and the empty newline are covered. The HTTP success content type is not asserted. |
| `hold.cancel` | `HoldApplication.cancel`, `DjangoHoldRepository.cancel` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/`; service/endpoint tests; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.cancel.yaml` cases 1–5 | Unknown, already-cancelled, expired-but-cancellable, successful response body, and active-list removal are covered. The successful HTTP response content type is not asserted. |
| `hold.repository` | `DjangoHoldRepository` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/repository.py`; repository and persistence endpoint tests; `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/spec/hold-management/hold.repository.yaml` cases 1–4 | Filtering/order, sequence allocation, persistence/readback, and concurrent placement locking are evidenced. The plan explicitly requires rollback-on-write-failure coverage, but `test_repository_cancellation_is_atomic` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/test_repository.py` only exercises a successful write; it does not induce a failure or assert rollback. |
| `hold.storage` | `Hold` and `0001_initial` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/`; seeded-record, persistence, repository, and spec tests | The persisted fields, 30-day inclusive expiry, cancellation exclusion, and exposed hold details match the source behavior. |
| `data.hold-seed-record` | `seed_holds` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/migrations/0001_initial.py`; `test_seeded_hold_matches_the_characterized_record` in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/tests/holds/test_endpoints.py`; two spec cases | H1, sequence 1, member `bo`, ISBN `9780134685991`, placement date `2026-01-05`, and null cancellation date match the source seed. The migration runs once through Django's migration state; it does not replace later persisted rows on subsequent startups. |

## E. Design, ruling, and flow

HM-02's decomposition is reflected in the target: the view is an HTTP adapter; the hold application owns `LoanStateLookup`; the composition root injects the loan application; the loan query and repository remain in the loans context. Placement checks are short-circuited in sequence and hold policy does not import Django models. This matches the design in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/plan/hold-management.md`.

Issue #170's human comment rules **preserve**: three active holds permit a fourth, while four reject a fifth with 409. The implementation uses `active_count_for_member(...) > 3`; the unit and spec cases establish both boundaries. No divergence was found.

The slice YAML at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/slices/hold-management.yaml` lists source anchors `GET /holds`, `POST /holds`, and `POST /holds/{id}/cancel`, with target anchors `GET /holds`, `POST /holds`, and `POST /holds/<str:hold_id>/cancel`. The accepted target graph's `graph-check.md` line 23 incorrectly traces `GET /holds` through `HoldApplication.place` to `DjangoHoldRepository.create`/`writes_to`. The inspected view at `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/src/holds/views.py` branches GET to `list_active_text`, and the repository reads active holds. The code flow is present and exercised; this is a target-graph inconsistency, not a broken implementation flow.

## F. Surviving mutants

The verified full run reports 35 survivors; the score exceeds the configured threshold but does not mean every observable behavior was mutation-tested. Of the 23 survivors in `src/holds/`, the most significant are #108 (GET listing content type) and #118 (successful cancellation content type): both are visible response changes that no current endpoint assertion catches. Mutant #107 changes the GET ISBN query key; the spec does exercise the public filter, although the regular pytest mutation run does not execute the spec. Mutants #110 and #112 alter missing-field defaults; the spec has separate missing-member and missing-ISBN replays, and service tests cover blank inputs.

The remaining hold survivors concern internal dataclass mutability and enum tokens, the advisory-lock literal, nested atomic decoration inside the placement transaction, and model metadata redundant with explicit ordering or the checked-in migration schema. I found no separate observable gap demonstrated by those survivors. All 35 diffs remain available unchanged in `/home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/.migration/runs/acceptance-45394010303-1/mutants.md`; 12 are outside this slice.

## G. Gaps and verdict

Four evidence gaps remain; the relevant implementation currently matches the inspected source:

1. `untested` — `hold.place`: add a characterized case with competing policy failures to prove first-error precedence, which HM-02 explicitly assigns to the end-to-end cases.
2. `untested` — `hold.list-active`: assert the successful GET's recorded `text/plain` content type.
3. `untested` — `hold.cancel`: assert the successful cancellation's recorded `text/plain` content type.
4. `untested` — `hold.repository`: exercise a failed write and prove rollback at the persistence boundary, as required by the slice acceptance notes.

No follow-up issues were created in this read-only audit; the return records these with `ticket: null` for the operator to ticket before acceptance. The target-graph mismatch is separately recorded in `graph_inconsistencies`. **Verdict: `gaps-remain`**. The operator's side-by-side sign-off under ADR-0031 remains a later step and is not granted by this audit.
