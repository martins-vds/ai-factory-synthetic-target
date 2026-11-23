# SY-08 — re-pinned hold capability characterization

## Scope and method

- Source: `.source/legacy/` at `96d50b85a9a456d9c0a58f080414b3badb501e59`.
- Tier A: the source application was built and started from an isolated copy; HTTP requests exercised its running endpoints.
- The legacy source has no Java test files. The existing characterization harness was extended; seeded boundary cases replace only the temporary copy's `seed.sql`, and `run_source` restores the original file in a `finally` block.
- Recording merges newly observed exchange keys into existing golden files and never overwrites an existing key. The pre-existing exchanges in `http.json` and `edge-cases.json` are byte-for-byte unchanged from `origin/main`.
- Run journal: `.migration/evidence/runs/SY-08.md`; recorded source outputs: `.migration/characterization/source/goldens/`.
- The latest `--record` run and the subsequent verification run both passed through `afs-run`. The spec gate passed all 20 cases, including the replayed fee exchange at its original 2026-11-08 oracle. An earlier characterization attempt is recorded as flaky in `.migration/evidence/flaky/SY-08.md`.

## Predicted versus observed

| Capability | Predicted | Observed | Result |
|---|---|---|---|
| `hold.list-active` | `GET /holds` returns active, un-cancelled holds in sequence order, optionally filtered by ISBN; the empty result is a newline. A hold is active through day 30 and inactive on day 31. | The endpoint returned HTTP 200 `text/plain`; empty/default, blank-ISBN and unknown-ISBN results were `"\n"`. Matching ISBNs returned only matching lines, sorted H1/H2/H3. H1 appeared on its expiry date and was absent one day later. | Match; `http.json`, `edge-cases.json`, `hold-listing.json`, `hold-expired.json`. |
| `hold.place` | Missing/blank fields are 400; unavailable ISBN, borrower's own book, duplicate active hold, and limit reached are 409. Eligible placement is 201 with the next H-number and today's date. The legacy `> 3` check admits a fourth hold and rejects a fifth. | Missing member, missing ISBN, and whitespace/empty values returned 400 `member and isbn are required`. A returned/available book returned 409 `book is available`; the borrower returned 409 `member has this book`; a duplicate returned 409 `already on hold`. Eligible placements returned 201 with H2/H3/H4/H5 lines. With three existing holds a fourth was accepted; with four existing holds a fifth returned 409 `hold limit reached`. | Match; `http.json`, `edge-cases.json`, `hold-limit.json`. Quirk #170 is ruled preserve. |
| `hold.cancel` | Unknown ID is 404; already-cancelled is 409; a not-yet-cancelled hold can be cancelled even after expiry, returning its line with 200 and today's cancellation date. | Unknown ID returned 404 `no such hold`; repeat cancellation returned 409 `hold already cancelled`. H2 cancellation returned 200 with its line, and expired seeded H1 cancellation also returned 200 with `H1;bo;9780134685991;2026-01-05;2026-02-04`; another cancellation of H1 returned 409. | Match; `http.json`, `edge-cases.json`. |
| `hold.repository` | Reads order by sequence and optionally filter ISBN; placement assigns max sequence + 1; writes commit, and an active transaction is rolled back on failure before close. | Public listing, filtering, placement and cancellation produced the expected ordered results and IDs; each successful write was visible to later requests. The rollback-on-failure branch cannot be induced through the public HTTP boundary and remains source-predicted at `HoldRepository.java:69-81`. | Match for reachable operations; rollback path source-confirmed, not runtime-injected; `hold-listing.json`, `edge-cases.json`. |
| `hold.storage` | HOLD stores identifier, sequence, member, ISBN, placed date and nullable cancellation date; expiry is placed date + 30 days, inclusive, unless cancelled. | The recorded day-30 listing included H1 with the expected expiry; day 31 returned no hold. Cancelling H1 removed it from active results. | Match; `hold-listing.json`, `hold-expired.json`, `edge-cases.json`. |
| `data.hold-seed-record` | Startup seeds H1, sequence 1, for bo/ISBN 9780134685991 on 2026-01-05, uncancelled. | The default current-date listing omitted the now-expired seed. Cancelling H1 still returned its seeded values and expiry date, confirming the row was loaded. | Match; `http.json`, `edge-cases.json`. |
| `application.startup` (touched behavior only) | Startup wires the hold repository/resource into the running application and retains the existing HTTP server lifecycle. | `GET /holds` returned 200 from the running app; the isolated server started and shut down for the harness. | Match for the added hold-resource wiring; `http.json`, `hold-listing.json`. |
| `data.loan-storage` (touched behavior only) | The persistence unit registers the added HOLD entity alongside LOAN without changing LOAN fields. | Hold reads/writes operated against the started source persistence unit; the existing loan records and restart reset remained as previously characterized. | Match for the added entity registration; `hold-listing.json`, `hold-expired.json`, `restart.json`. |
| `data.seed-records` (touched behavior only) | The seed adds the separate H1 HOLD row while retaining the three loan seeds. | H1 was retrievable/cancellable with the seed's member, ISBN and dates; the loan list still contained the original three seed records after restart. | Match; `edge-cases.json`, `restart.json`. |

No new quirks were found. Quirk `martins-vds/ai-factory-synthetic-target#170` is closed with the operator's **Ruling** comment: preserve; this report records the fourth-accepted/fifth-rejected behavior.

## Source references

- HTTP outcomes and line formatting: `legacy/src/main/java/lib/HoldResource.java:30-75`.
- Repository ordering, sequence allocation and transaction cleanup: `legacy/src/main/java/lib/HoldRepository.java:20-81`.
- Expiry and active-state rule: `legacy/src/main/java/lib/Hold.java:10-58`.
- Startup wiring: `legacy/src/main/java/lib/App.java:13-27`.
- Persistence entity registration: `legacy/src/main/resources/META-INF/persistence.xml:3-12`.
- Seeded hold row: `legacy/src/main/resources/META-INF/seed.sql:4`.
