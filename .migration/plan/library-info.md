# Library information

## What this slice delivers

The characterized `/about` response remains unchanged, including its opening hours, lending policy, and contact information. The modernized browser page is served separately at `/ui/about/` using the Tailwind/daisyUI and pinned htmx assets introduced in `LL-01`.

## Anchors

- Source: `GET /about` serves a static page and intentionally has no path to a table; this is a non-data flow, not a graph-enricher gap.
- Target: preserve the characterized `GET /about` response exactly and serve the modernized page at `GET /ui/about/`; neither route accesses a table.

## Acceptance

- All characterized about-page information remains present and usable.
- The `/ui/about/` page follows the approved UI and asset-delivery pattern.
- Browser tests pass through `afs-run`.

## Ticket

- `LL-04` (`afs-migrator`): modernize the public library-information page.
- Blocked by: `LL-03` (shared route composition).

## Shared files

`config/urls.py` extends the route composition introduced by earlier slices.
