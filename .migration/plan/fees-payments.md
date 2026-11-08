# Fees and payments

## What this slice delivers

Members can view a loan's late fee and pay it through the existing gateway contract. Fee calculation, page content, gateway request, and success/failure responses match characterization; the interrupted-call and HTTP 502 quirks are fixed as ruled on the decision map.

## Anchors

- Source: `GET /fees/{id}` and `POST /payments/{id}` reach loan data.
- Target: retain both API paths; the fee endpoint remains the browser page and payment interaction follows the approved htmx/API response mapping.

## Acceptance

- Fee days, grace period, cap, amount, missing-loan response, and page content match characterization, subject to the approved date/time answer.
- The same gateway request is made; success and failure surface as characterized.
- Interrupted calls surface as gateway failures without losing the interruption.
- Tailwind, daisyUI, and htmx follow the approved asset-delivery and UI pattern.
- Gateway, database, browser, and differential tests pass through `afs-run`.

## Ticket

- `LL-03` (`afs-migrator`): late-fee view and payment.
- Blocked by: `LL-02` (loan and route composition).

## Shared files

`config/urls.py` is extended by this slice and the subsequent library-info slice.
