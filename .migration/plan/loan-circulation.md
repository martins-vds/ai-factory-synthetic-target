# Loan circulation

## What this slice delivers

Members can lend and return books through the characterized API behaviors and separate modernized browser paths under `/ui/`. The loan is stored durably, due dates use the server's default time zone as characterized and preserve observed date formats, and a repeated return is rejected without replacing the original return date.

## Anchors

- Source: `POST /loans` and `POST /loans/{id}/return` reach the `LOAN` table.
- Target: preserve those API paths and characterized responses exactly. Browser routes are `/ui/loans/new/`, `/ui/loans/`, and `/ui/loans/{id}/return/`; htmx interactions use `/ui/` paths rather than changing API responses.

## Acceptance

- Required and blank member/ISBN values produce the ruled field errors.
- Successful lending creates the characterized record and response; due dates remain 14 calendar days after lending, using the server's default time zone and observed date formats.
- First return persists the return date; repeated returns are rejected and preserve it.
- The semicolon export escapes delimiter characters.
- Browser interactions use the Tailwind/daisyUI/htmx assets introduced in `LL-01`, while API requests retain characterized responses exactly.
- Real-PostgreSQL, browser, and differential tests pass through `afs-run`.

## Ticket

- `LL-02` (`afs-migrator`): lend and return books.
- Blocked by: `LL-01` (loan model, persistence and route composition).

## Shared files

`config/urls.py`, `src/loans/`, `templates/loans/`, and `tests/loans/` extend files established by `LL-01`.
