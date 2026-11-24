# Hold management plan

The slice preserves the source API contract and uses the existing loan catalog and circulation slices; it does not re-plan either. The hold capabilities form one implementation ticket, preceded by the required customer-spec ticket and a design ticket for `HoldResource.place` (CRAP 110; target threshold 30).

## Tickets and dependencies

- `HM-01` (`afs-characterizer`) owns `.migration/spec/hold-management/` and the six hold ledger entries.
- `HM-02` (`afs-planner`) designs the placement-use-case decomposition and the loan-state lookup seam. It waits for the characterized spec.
- `HM-03` (`afs-migrator`) implements all six hold capabilities. It waits for `HM-01`, `HM-02`, and `LL-02`; `LL-02` already depends on the loan catalog.

The ticket file lists the complete scope, target anchors, and cross-slice route/settings files.

## HM-02 design: placement decomposition and loan lookup

Keep `POST /holds` as a thin HTTP adapter: parse the request, call the hold application, and map its result to the characterized status, content type, and body. The application sequences these separately testable policy steps, returning the first rejection in the characterized order:

1. Validate the required member and ISBN values.
2. Ask whether the ISBN has an active loan; reject an available book or one already borrowed by this member.
3. Reject an existing active hold for the same member and ISBN.
4. Check the member's active-hold count. Preserve the ruled quirk exactly: reject only when the count is greater than three, so a fourth hold is allowed and a fifth is refused.
5. On success, obtain the next identifier and today's date from the injected repository and clock, create the hold, and persist it.

Keep each policy step at no more than four independent decision points (CCN ≤ 4; worst-case CRAP 20 even at 0% coverage). Run the checks lazily in sequence and short-circuit on the first rejection, so the placement orchestrator stays at CCN ≤ 3 instead of accumulating one branch per rule. If implementation pushes a policy step above its budget, split it before adding more branches. Test each step's rejection and success paths at its interface, and retain the characterized end-to-end cases as the authority for check precedence and exact HTTP responses. The view must not duplicate policy or reorder checks.

The hold application owns a `LoanStateLookup` Protocol in `src/holds/services.py`; its read-only ISBN query returns no active loan or the active loan's borrower identity. Inject this port into the hold application. Wire the existing loan application as its adapter in `src/holds/composition.py`; add a corresponding public query to `LoanApplication` and keep any storage query inside the loans context. Do not have holds import loan models or repositories, query Django storage, parse the loans text endpoint, or expose a new HTTP endpoint for this internal question.

Layering contracts:

- Hold policy, placement orchestration, and the lookup/repository/clock Protocols stay in `src/holds/services.py`, independent of Django, HTTP, and storage models.
- Django views translate HTTP only; Django repositories and the system clock are outer adapters, assembled with the loan application in `src/holds/composition.py`.
- The hold application depends on its own ports. Its only cross-context dependency is the loans application's read interface; loan persistence details remain owned by loans.
- Exercise the application through injected ports in focused tests; prove repository and endpoint behavior through the existing PostgreSQL-backed tests and the immutable hold-management customer spec.

## HM-03 scope prerequisite

The current HM-03 file list does not include the loans-side query needed by this design. Before HM-03 starts, amend its declared scope to include `src/loans/services.py`, `src/loans/repository.py`, `tests/loans/test_services.py`, and `tests/loans/test_catalog.py` (and retain the existing hold files). This is a required scope correction, not permission to reach around the loan application into its storage. The HM-02 ticket does not include the ticket file, so the Orchestrator must make that correction.
