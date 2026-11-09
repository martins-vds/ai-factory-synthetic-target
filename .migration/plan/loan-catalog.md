# Loan catalog

## What this slice delivers

The persistent loan catalog is available through the characterized list and lookup behavior, including the seed examples, stable transaction handling, due dates, and semicolon-delimited export. The Django application starts against PostgreSQL. Its modernized browser catalog lives under `/ui/`; the API routes retain their characterized responses exactly.

## Anchors

- Source: `GET /loans` and `GET /loans/{id}` reach the `LOAN` table.
- Target: preserve those API paths and their characterized responses exactly. Browser pages use separate `/ui/loans/` and `/ui/loans/{id}/` paths.
- Remove Django admin from installed apps and routes; `/admin/` is not part of the target.

## Acceptance

- PostgreSQL-backed records survive application restarts; startup does not overwrite persisted records with seeds.
- The seed records remain available for an empty database.
- List, lookup, due-date, ordering, output fields, delimiters, and trailing newline match characterization, except the approved delimiter-escaping fix.
- Loan dates use the server's default time zone as characterized and preserve the observed date formats in pages and exports.
- The browser catalog uses Tailwind v4 via the standalone CLI and Makefile targets `tailwind-install` and `tailwind-build`; `tailwind-build` generates `static/css/tailwind.css`. htmx 2.0.11 is loaded from the pinned jsDelivr URL. These assets are introduced in this first page-rendering slice, following pilot ADR-0002.
- Remove Django admin from `INSTALLED_APPS` and the URLconf while wiring the catalog routes.
- The browser pages use separate `/ui/` paths; the existing API routes keep their characterized responses exactly.
- Build and startup checks, real-PostgreSQL tests, UI checks, and differential tests pass through `afs-run`.

## Ticket

- `LL-01` (`afs-migrator`): loan catalog, persistence, startup, list and lookup.
- Blocked by: none.

## Shared files

`config/settings.py` and `config/urls.py` are extended by later slices. Later slices are blocked along the approved composition order; see `cross_slice` in the tickets file.
