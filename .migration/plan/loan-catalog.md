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

## TD-20261122-UI: Make the browser tests wait for the page

**Test debt** in the `loan-catalog` slice: lines `afs-test-health` flags in tests written before the coupling guard (ADR-0064, ADR-0065):

  - `tests/fees/test_endpoints.py:260` non-waiting browser assertion: `inner_text()`
  - `tests/library_info/test_about_page.py:42` non-waiting browser assertion: `is_visible()`
  - `tests/library_info/test_about_page.py:43` non-waiting browser assertion: `is_visible()`
  - `tests/library_info/test_about_page.py:46` non-waiting browser assertion: `is_visible()`
  - `tests/library_info/test_about_page.py:47` non-waiting browser assertion: `is_visible()`
  - `tests/library_info/test_about_page.py:48` non-waiting browser assertion: `get_attribute()`
  - `tests/library_info/test_about_page.py:52` non-waiting browser assertion: `get_attribute()`
  - `tests/loans/test_catalog.py:116` non-waiting browser assertion: `count()`
  - `tests/loans/test_catalog.py:324` non-waiting browser assertion: `count()`
  - `tests/loans/test_catalog.py:325` non-waiting browser assertion: `count()`
  - `tests/loans/test_catalog.py:357` non-waiting browser assertion: `count()`
  - `tests/loans/test_catalog.py:416` non-waiting browser assertion: `inner_text()`
  - `tests/loans/test_catalog.py:408` non-waiting browser assertion: `inner_text()`
  - `tests/test_htmx_errors.py:79` non-waiting browser assertion: `inner_text()`
  - `tests/test_ui_smoke.py:21` non-waiting browser assertion: `is_visible()`
  - `tests/test_ui_smoke.py:22` non-waiting browser assertion: `is_visible()`

Rewrite each one to assert with Playwright's `expect(locator).to_be_visible()` / `.to_have_text(...)`, which waits for the page (ADR-0065), and look headers up by their lowercase name.

**Behaviour doesn't change.** Change production code only to expose a clean seam a test needs, and say why in your return's `notes`. Every rewritten test must still fail if the behaviour it covers breaks. When you finish, `python .migration/harness/tools/afs-test-health` must list none of these lines (an exempted line with a reason is fine).
