# Monthly lending report

## What this slice delivers

A monthly report is produced from persisted loans according to the surviving tier-C specification: one row per member with loans started, late returns, and late fees in cents, sorted by fee descending then member id, omitting members without loans started in the month. The report runs on the month's first day for the prior month.

## Anchors

- Source: no executable endpoint or job remains; the only source is `legacy/docs/reports-spec.md` (tier C).
- Target: `command=monthly_report` is the proposed durable entry point. Its scheduling mechanism and month-boundary time zone require operator direction.

## Acceptance

- Report content, row inclusion, ordering, monetary units, and month window match the surviving specification.
- The command can be run deterministically against real PostgreSQL data.
- The agreed scheduler invokes it on the agreed first-of-month boundary.
- Specification-derived tests pass through `afs-run`.

## Ticket

- `LL-05` (`afs-migrator`): implement the specified monthly report.
- Blocked by: `LL-03` (loan persistence and fee calculation).

## Data migration

No legacy-record migration slice is planned: the operator waived it in issue #20. `data.seed-records` remains part of the loan-catalog slice and is not a legacy data migration.
