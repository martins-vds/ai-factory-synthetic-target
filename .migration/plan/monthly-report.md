# Monthly lending report

## What this slice delivers

A monthly report is produced by a Django management command from persisted loans according to the surviving tier-C specification: one row per member with loans started, late returns, and late fees in cents, sorted by fee descending then member id, omitting members without loans started in the month. An external operator or scheduler runs `monthly_report` on the month's first day for the prior month; the application contains no scheduler. Date boundaries use the server's default time zone as characterized and observed date formats.

## Anchors

- Source: no executable endpoint or job remains; the only source is `legacy/docs/reports-spec.md` (tier C).
- Target: `command=monthly_report` is the management command entry point. It is run or scheduled outside the application; there is no in-app scheduler.

## Acceptance

- Report content, row inclusion, ordering, monetary units, and month window match the surviving specification.
- The command can be run deterministically against real PostgreSQL data.
- The command's month boundary uses the server's default time zone as characterized; external operations invoke or schedule it on the month's first day.
- Specification-derived tests pass through `afs-run`.

## Ticket

- `LL-05` (`afs-migrator`): implement the specified monthly report.
- Blocked by: `LL-04` (approved slice order; loan persistence and fee calculation are provided by earlier slices).

## Data migration

No legacy-record migration slice is planned: the operator waived it in issue #20. `data.seed-records` remains part of the loan-catalog slice and is not a legacy data migration.
