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

## REF-20261122-FEES-PAYMENTS: Move src/fees/views.py's private helpers into their own module, preserving behaviour

**Role:** `afs-migrator`, ticket `REF-20261122-FEES-PAYMENTS`: **restructure `src/fees/views.py` without changing what it does** (ADR-0072, a periodic refactor of the `fees-payments` slice).

`src/fees/views.py` keeps 3 private helpers: `_fee_amount`, `_gateway_result`, `_fee_or_404`. Move them into a new module in `src/fees/`, as public functions named for what they do, and have the code that used them import them from there. Every page, response, command output and stored value stays exactly as it is.

**Tests are the safety net, not part of the job.** Change an existing test only if the restructuring itself makes it fail, and for every test you change say why in your return's `notes`. Don't keep aliases or wrappers so the old private names still work. The tests you had to change are this ticket's measurement: each one knows how the code is built, not what it does.

Load `afs-migration-contract` and run `afs-setup-check` first. Run every gate through `afs-run`: build, behaviour, spec, idiom, CRAP, mutation on the changed code, regression. Commit your return `.migration/returns/REF-20261122-FEES-PAYMENTS.afs-migrator.yaml`, or a handoff.
