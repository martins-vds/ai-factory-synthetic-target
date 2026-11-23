# Hold management plan

The slice preserves the source API contract and uses the existing loan catalog and circulation slices; it does not re-plan either. The hold capabilities form one implementation ticket, preceded by the required customer-spec ticket and a design ticket for `HoldResource.place` (CRAP 110; target threshold 30).

## Tickets and dependencies

- `HM-01` (`afs-characterizer`) owns `.migration/spec/hold-management/` and the six hold ledger entries.
- `HM-02` (`afs-planner`) designs the placement-use-case decomposition and the loan-state lookup seam. It waits for the characterized spec.
- `HM-03` (`afs-migrator`) implements all six hold capabilities. It waits for `HM-01`, `HM-02`, and `LL-02`; `LL-02` already depends on the loan catalog.

The ticket file lists the complete scope, target anchors, and cross-slice route/settings files.
