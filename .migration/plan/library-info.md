# Library information

## What this slice delivers

The public about page remains available at `/about`, with its opening hours, lending policy, and contact information, refreshed to the approved Tailwind/daisyUI and htmx UI direction.

## Anchors

- Source: `GET /about` serves a static page and intentionally has no path to a table; this is a non-data flow, not a graph-enricher gap.
- Target: `GET /about` is owned by this slice and likewise does not access a table.

## Acceptance

- All characterized about-page information remains present and usable.
- The page follows the approved UI direction and dependency-delivery pattern.
- Browser tests pass through `afs-run`.

## Ticket

- `LL-04` (`afs-migrator`): modernize the public library-information page.
- Blocked by: `LL-03` (shared route composition).

## Shared files

`config/urls.py` extends the route composition introduced by earlier slices.
