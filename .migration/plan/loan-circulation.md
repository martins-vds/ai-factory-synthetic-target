# Loan circulation

## What this slice delivers

Members can lend and return books through the characterized API behaviors and the approved modernized browser flow. The loan is stored durably, due dates are calculated consistently, and a repeated return is rejected without replacing the original return date.

## Anchors

- Source: `POST /loans` and `POST /loans/{id}/return` reach the `LOAN` table.
- Target: preserve those API paths. Proposed browser routes are `/ui/loans/new`, `/ui/loans`, and `/ui/loans/{id}/return`; confirm their paths and htmx/API response behavior before implementation.

## Acceptance

- Required and blank member/ISBN values produce the approved field errors.
- Successful lending creates the characterized record and response; due dates remain 14 calendar days after lending.
- First return persists the return date; repeated returns are rejected and preserve it.
- The semicolon export escapes delimiter characters.
- Browser interactions use the approved Tailwind/daisyUI/htmx pattern while unchanged API requests retain characterized responses.
- Real-PostgreSQL, browser, and differential tests pass through `afs-run`.

## Ticket

- `LL-02` (`afs-migrator`): lend and return books.
- Blocked by: `LL-01` (loan model, persistence and route composition).

## Shared files

`config/urls.py`, `src/loans/`, `templates/loans/`, and `tests/loans/` extend files established by `LL-01`.
