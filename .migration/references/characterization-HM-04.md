# HM-04 — hold placement refusal precedence

The tier-A source check order in `legacy/src/main/java/lib/HoldResource.java:41-54` is: no open loan, requester is the borrower, duplicate active hold, then active-hold limit. When multiple refusals apply, the first matching check determines the response.

The new append-only recording `.migration/characterization/source/goldens/hold-precedence.json` contains three exchanges. The source harness created each starting state through public HTTP requests; no seed data was changed.

| Simultaneous refusals | Predicted first response | Observed legacy response | Result |
|---|---|---|---|
| Requester is borrower and already has an active hold | 409 `member has this book` | 409 `member has this book` | Match |
| Existing duplicate hold and more than three active holds | 409 `already on hold` | 409 `already on hold` | Match |
| Book is available and member has more than three active holds | 409 `book is available` | 409 `book is available` | Match |

The exchanges were recorded and replay-verified by the HM-04 source-precedence runs in `.migration/evidence/runs/HM-04.md`. The source seed hash was unchanged. These observations confirm the existing `HoldApplication.place` order; no discrepancy or new quirk was found.
