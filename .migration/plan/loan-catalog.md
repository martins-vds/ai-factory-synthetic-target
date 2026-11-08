# Loan catalog

## What this slice delivers

The persistent loan catalog is available through the characterized list and lookup behavior, including the seed examples, stable transaction handling, due dates, and semicolon-delimited export. The Django application starts against PostgreSQL. A modernized browser catalog is proposed alongside the unchanged API routes.

## Anchors

- Source: `GET /loans` and `GET /loans/{id}` reach the `LOAN` table.
- Target: preserve those API paths and use the proposed `/ui/loans` and `/ui/loans/{id}` browser pages. Their paths and the response negotiation with the existing API require operator approval.
- The target scaffold currently exposes `/admin/`; this plan temporarily assigns it here for graph ownership. The operator must decide whether to retain or remove it.

## Acceptance

- PostgreSQL-backed records survive application restarts; startup does not overwrite persisted records with seeds.
- The seed records remain available for an empty database.
- List, lookup, due-date, ordering, output fields, delimiters, and trailing newline match characterization, except the approved delimiter-escaping fix.
- The browser catalog follows the approved UI routes and uses the decided Tailwind, daisyUI, and htmx delivery pattern without changing characterized API responses.
- Build and startup checks, real-PostgreSQL tests, UI checks, and differential tests pass through `afs-run`.

## Ticket

- `LL-01` (`afs-migrator`): loan catalog, persistence, startup, list and lookup.
- Blocked by: none.

## Shared files

`config/settings.py` and `config/urls.py` are extended by later slices. Later slices are blocked along the required composition order; see `cross_slice` in the tickets file.
