# Hold management

## What this slice delivers

The hold API preserves the characterized behavior for placing, listing, and cancelling holds. Holds remain persisted in PostgreSQL, and a fresh database receives the characterized H1 seed record. No hold browser page is added because the source exposes no hold UI.

## Anchors

- Source: `GET /holds`, `POST /holds`, and `POST /holds/{id}/cancel`; all reach the HOLD table, and placement also reaches LOAN.
- Target: preserve the same API paths and response contracts through Django endpoints.
- The slice depends on the existing loan catalog and circulation work for persisted loan state and open/returned loan behavior.

## Acceptance

- `GET /holds` returns uncancelled holds through their expiry date, ordered by sequence and optionally filtered by ISBN. Output retains its semicolon-separated fields and trailing newline; an empty result is a single newline.
- `POST /holds` preserves required-field validation and the conflicts for an available book, the requester's own book, a duplicate active hold, and a reached hold limit. Eligible holds receive the next H identifier and today's date.
- Quirk #170 is preserved: a member with three active holds can place a fourth; a member with four cannot place a fifth.
- `POST /holds/{id}/cancel` returns the characterized 404 and 409 cases and allows an expired, uncancelled hold to be cancelled.
- HOLD records retain the characterized fields and 30-day inclusive expiry; a one-time migration seeds H1 for member `bo` and ISBN `9780134685991`, placed `2026-01-05`, without overwriting persisted records on later startups.
- Repository transaction behavior, including rollback on write failure, is covered at the persistence boundary.
- The endpoints and seed behavior are compared against `.migration/characterization/source/goldens/` and the SY-08 customer spec.

## Tickets

- `HM-01` (`afs-characterizer`): write the per-capability customer spec and finalize the six hold ledger entries.
- `HM-02` (`afs-planner`): design the hold-placement decomposition for the source hot spot before implementation.
- `HM-03` (`afs-migrator`): implement hold placement, listing, cancellation, persistence, and the seed record.

The implementation waits for the characterized spec, the design ticket, and `LL-02` (loan circulation), which itself depends on the catalog.

## Characterization evidence

`.migration/references/characterization-SY-08.md`, `.migration/evidence/runs/SY-08.md`, and the hold golden files record the tier-A behavior. The hold placement source method is CRAP 110, above the profile threshold of 30; the design ticket addresses this hot spot before implementation.
