# Loan circulation — acceptance

- Slice: `loan-circulation` (#60)
- Acceptance run: [42752283868, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42752283868), passed on commit `70fef8e7bc822092770b04b1bf9b5288e04d8bb6`
- Archived result: `.migration/evidence/acceptance-runs/42752283868-1.json` (artifact retained through 2026-12-10)
- Acceptance journal: `.migration/evidence/runs/LC-ACCEPT.md`

No acceptance gates or mutation runs were repeated for this report. The archived result and previously verified artifact record the following:

| Result | Outcome |
|---|---|
| Source graph | Pass; 8 entry points, 6 reaching data |
| Target graph | Pass; 16 entry points, 12 reaching data |
| Build, idiom, and behavior | All steps passed |
| CRAP | Maximum 7.0; threshold 30 |
| Full mutation | 0.920; 126 killed, 11 survived; threshold 0.8 |

## Verification and audit history

| Work | Evidence | Outcome |
|---|---|---|
| Initial LL-02 verification | #78, PR #79; `.migration/returns/LL-02.afs-verifier.yaml` at that landing | `changes-required`; application use cases were coupled to Django and the concrete ORM repository |
| Follow-up LL-02 verification | #84, PR #85; `.migration/returns/LL-02.afs-verifier.yaml` | `pass`; ports remediation and the lending/return behavior were verified |
| Initial circulation audit | #94, PR #95; `.migration/returns/LC-AUDIT.afs-auditor.yaml` at that landing | `gaps-remain`; `loan.lend` and `loan.return-date` had misplaced target references |
| Re-audit | #100, PR #101, after ledger fix PR #98; current `.migration/returns/LC-AUDIT.afs-auditor.yaml` | `complete`; all three circulation ledger entries name existing implementation components |

## Circulation ledger

| Entry | Status | Evidence |
|---|---|---|
| `loan.lend` | `migrated` | Tier-A characterization and LL-02 tests cover required fields, 14-day due date, delimiter escaping, API lending, and the new-loan UI |
| `loan.return` | `migrated` | Tier-A characterization and LL-02 tests cover successful return, missing loans, repeat-return `409`, and browser/HTMX return |
| `loan.return-date` | `migrated` | Tier-A characterization and LL-02 tests verify the first return date is saved and repeat returns leave it unchanged |

The final audit found no capability gaps. It noted one target-graph path inconsistency: the accepted graph maps `POST /loans` through the listing/read path, while the inspected view branches to lending and tests verify loan creation. This was reported as a graph-path inconsistency, not as a missing capability. The full mutation run had 11 survivors; the final audit reviewed the route, method-guard, and form-model cases against behavior tests.

## Human check — requested

Compare legacy and target side by side:

1. **Lending through the API:** required member and ISBN fields, the 14-day due date, and delimiter escaping in the resulting loan record.
2. **Returning:** the first return succeeds and saves its date; a repeat return answers `409` and leaves the saved date unchanged.
3. **Forms:** the `/ui/loans/new/` lending form and `/ui/loans/{id}/return/` return form, including their success and validation/error behavior.

Human check is requested and remains pending; no pass or approval is recorded here.
