# SY-05 — legacy capability characterization

## Scope and method

- Source: `legacy/` at `563c316ed51462b08fd6e58f3781a3c8b2890453`.
- The existing tier-A harness was extended to run a temporary copy of `legacy/`, keeping Maven output out of the pinned source tree.
- Suite: 7 graph endpoints, 12 edge probes, 2 browser pages, one restart probe and 3 payment-gateway outcomes (25 cases total).
- Legacy test inventory: no test directory or test files exist under `legacy/`; no source test suite was available to replay.
- Characterization: 16 capabilities at tier A; `reports.monthly-spec` at tier C because only a retired report specification remains.
- Fresh coverage: 93/98 lines, 497/513 instructions and 18/20 branches. Refreshed CRAP map: 19 methods, maximum 4.0, none above 30; see `.migration/risk-map/SY-05.md`.
- Run journal: `.migration/evidence/runs/SY-05.md`; HTTP, edge, browser, restart and gateway goldens are under `.migration/characterization/source/goldens/`.

## Predicted versus observed

| Capability | Predicted from the inventory/source | Observed | Result |
|---|---|---|---|
| `about.page` | `/about` serves the packaged public HTML. | HTTP and browser both returned 200; the browser heading and page content identify the Lending Library, hours, lending period and contact address. | Match — tier A; `http.json`, `browser.json`. |
| `application.build` | `run.sh` packages the Java 17 app and launches `lib.App`. | The copied source built and started successfully for the default and configured-port runs. | Match — tier A; run journal. |
| `application.startup` | Default port is 8080; `PORT` selects another port; startup loads resources and seed data. | The default app answered on 8080, and a second app answered on a dynamically selected `PORT`; restart served the seed set again. | Match — tier A; `restart.json`. |
| `data.loan-storage` | Loan rows persist within the H2 persistence unit for reads and writes. | Lend and return mutations appeared in later reads in the same process; after restart, only the three seed rows remained. | Match — tier A; `http.json`, `edge-cases.json`, `restart.json`; reset behavior linked to #42. |
| `data.seed-records` | Startup seeds L1, L2 and L3 with the listed members, ISBNs and dates. | Initial list contained exactly L1–L3 in ID order with matching seed values; restart restored the same list. | Match — tier A; `http.json`, `restart.json`; linked to #42. |
| `fees.calculation` | Late days are clamped at zero; fees are waived through two days late, then 25 cents/day up to $10. | L1 was 296 days late and capped at $10.00; early-returned L2 had zero late days and $0.00; L3 displayed 19 days and $4.75. The fixed seed/API does not permit constructing an exact 1-, 2- or 3-day-late loan through HTTP. | Match for reachable dates; exact waiver boundary remains source-predicted — tier A; `http.json`, `edge-cases.json`; formula at `legacy/src/main/java/lib/LateFeeView.java:31-37`. |
| `fees.page` | Existing loan renders an HTML fee page; an unknown loan returns 404 and the no-loan fragment. | L3 and the browser page returned 200 HTML; unknown ID returned 404 with `<p>No such loan.</p>`. | Match — tier A; `http.json`, `edge-cases.json`, `browser.json`. |
| `integration.payment-gateway` | Unknown loans do not call the gateway; 200 maps to 200, other responses and I/O failures map to 502. | The default endpoint returned 502/unavailable; a local gateway's 200 response and body were forwarded, 503 mapped to 502 with its body, and unknown loan returned 404 without a gateway request. Interruption itself was not injected. | Match for reachable outcomes — tier A; `http.json`, `gateway.json`; interruption quirk linked to #40. |
| `loan.due-date` | Due date is 14 days after `lentOn`. | A new loan dated on the run date had a due date exactly 14 calendar days later; seeded due dates also match the listed values. | Match — tier A; `http.json`, `edge-cases.json`; formula at `legacy/src/main/java/lib/Loan.java:44-46`. |
| `loan.get` | Known ID returns its formatted line with newline; unknown ID returns 404. | L1 returned its semicolon line and trailing newline; unknown ID returned 404 with `no such loan`. | Match — tier A; `http.json`, `edge-cases.json`. |
| `loan.lend` | Missing member or ISBN returns 400; valid values create a loan dated today. | Normal input created L4 with 201; either missing field returned 400; empty values were accepted as L5 with 201. | Match — tier A; `http.json`, `edge-cases.json`; blank-field quirk linked to #39. |
| `loan.list` | All loans are ordered by ID and rendered as newline-terminated semicolon records. | Initial list contained the three ordered seeds; after writes it included the created rows in ID order and ended with a newline. | Match — tier A; `http.json`, `edge-cases.json`. |
| `loan.return-date` | A return stores the supplied date, including replacing an existing date. | Returning L2 again replaced its earlier date with the run date. | Match — tier A; `http.json`, `edge-cases.json`; overwrite behavior linked to #41. |
| `loan.return` | Existing ID returns updated row with 200; unknown ID returns 404. | L1 returned 200 with a return date; unknown IDs return 404. | Match — tier A; `http.json`, `edge-cases.json`; repeated-return behavior linked to #41. |
| `loan.text-export` | Export fields are joined raw with semicolons; null return date is empty. | Seed and new-loan lines use the expected order and empty final field; `a;b` and `123;456` were emitted without escaping. | Match — tier A; `http.json`, `edge-cases.json`; delimiter behavior linked to #43. |
| `reports.monthly-spec` | The report document specifies a first-of-month prior-month report, one row per qualifying member, ordered by fees then member ID. | No report executable, runtime or tests exist; only `legacy/docs/reports-spec.md:1-9` remains, so no runtime output can be observed. | Spec-derived — tier C; no code or tests available. |
| `repository.transactions` | Reads close their entity manager; writes commit, roll back an active transaction after failure and close the manager. | Public reads and writes behaved normally and mutations were visible within the process. The rollback-on-failure branch cannot be forced through the public routes; its cleanup behavior is source-confirmed at `legacy/src/main/java/lib/LoanRepository.java:47-69`. | Match for reachable operations; rollback branch source-predicted — tier A; `http.json`, `edge-cases.json`. |

No new quirks were found beyond the existing issue links #39–#43 (under decision map #38). Their source behavior is recorded above without changing or adjudicating any ruling. No capability required a review-only request.
