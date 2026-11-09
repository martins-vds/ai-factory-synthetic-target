# Fees and payments

## What this slice delivers

Members can view a loan's late fee and pay it through the existing gateway contract. Fee calculation, page content, gateway request, and success/failure responses match characterization; the interrupted-call and HTTP 502 quirks are fixed as ruled on the decision map. Browser pages and htmx actions use separate `/ui/` paths; the API routes retain their characterized responses exactly.

## Anchors

- Source: `GET /fees/{id}` and `POST /payments/{id}` reach loan data.
- Target: preserve `GET /fees/{id}` and `POST /payments/{id}` with their characterized responses exactly. The fee page is `/ui/fees/{id}/`; its htmx payment action uses `/ui/payments/{id}/`.

## Acceptance

- Fee days, grace period, cap, amount, missing-loan response, and API response match characterization. Date calculation uses the server's default time zone and observed date formats.
- The same gateway request is made; success and failure surface as characterized.
- Interrupted calls surface as gateway failures without losing the interruption.
- The fee page uses the Tailwind/daisyUI and pinned htmx assets introduced in `LL-01`; htmx actions remain under `/ui/`.
- Gateway, database, browser, and differential tests pass through `afs-run`.

## Ticket

- `LL-03` (`afs-migrator`): late-fee view and payment.
- Blocked by: `LL-02` (loan and route composition).

## Shared files

`config/urls.py` is extended by this slice and the subsequent library-info slice.
