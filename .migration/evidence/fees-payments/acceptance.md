# Fees and payments — acceptance evidence

- Slice: `fees-payments` · Epic: #62 · Acceptance ticket: LF-ACCEPT (#117)
- Acceptance run: [42912984554, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42912984554)
- Commit: `8f9a11640eef9801378f3db53a76903363c5e5b5`
- Archived result: `.migration/evidence/acceptance-runs/42912984554-1.json`

## Acceptance run

The archived result is passed for the exact commit above. The source and target graphs both pass: source has 8 entry points and 6 reaching data; target has 23 entry points, 18 reaching data, and 13 owned with none unowned. Build, idiom, and full test suite pass. CRAP maximum is 7.0 (threshold 30). Full mutation is 0.975 (threshold 0.8; 236 killed, 6 survived). These results are from the verified acceptance-run evidence recorded in `.migration/evidence/runs/LF-AUDIT.md`; this coordinator did not rerun the gates or mutation.

## Verifications and audit

- **Initial verification, #90 / PR #91:** `blocked`. The full suite failed because the live-server loan-catalog browser test could not find a seed loan after test isolation was lost; changed-code mutation did not produce a score because mutmut could not collect the selected fee modules. The fee-route method matrix and fee-service behavior tests passed.
- **Re-verification, #96 / PR #97:** `pass`. The test-isolation fix restored the default-order full suite; build, behavior, idiom, CRAP, changed-code mutation (0.914), and regression gates passed.
- **Audit, #114 / PR #116:** `complete`. The independent audit found no capability gaps or graph inconsistencies across the three fees ledger entries. It reviewed the quirk rulings and payment-gateway design. Six full-run mutants survived; two in the fees slice make internal `Fee` and `GatewayResponse` dataclasses mutable and were assessed as equivalent for the observable contract, with no silent suppression.

## Ledger status

| Capability | Status | Evidence |
|---|---|---|
| `fees.calculation` | `migrated` | Differential characterization and fee-boundary tests; `.migration/ledger/fees.calculation.yaml` |
| `fees.page` | `migrated` | Differential API and UI/browser-flow tests; `.migration/ledger/fees.page.yaml` |
| `integration.payment-gateway` | `migrated` | Differential gateway request/response and failure tests; `.migration/ledger/integration.payment-gateway.yaml` |

Each of the three slice entries is supported by target components and differential evidence. Their existing ledger statuses are consistent with the accepted implementation and independent audit.

## Human check — requested

Compare legacy and target side by side using the same loan data, clock/date, request, and gateway outcome. Record the observed legacy and target values/responses for each case:

1. An overdue loan: compare late-day count, fee amount in cents, and displayed dollar amount, including the legacy rounding/precision behavior.
2. A loan that is not overdue: compare the calculated fee and page/API presentation.
3. An unknown loan: compare the exact status and response body, and confirm whether either side contacts the gateway.
4. Paying a fee through the API and through the UI: compare the respective request/interaction and success response or visible page update.
5. A failed payment gateway: compare behavior for a non-200 response and an I/O/interruption failure, including the resulting status/body or UI state. The target's 502 handling follows the approved quirk ruling.

No human side-by-side check has been reported yet. The slice is awaiting that operator check; this report does not mark it passed.
