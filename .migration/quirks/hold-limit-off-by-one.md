# Hold limit permits a fourth active hold

## Question
The source rejects a new hold only when the member already has more than three active holds, so a member with three can place a fourth. Preserve, fix, or something else?

## Evidence
- Source: `method:legacy/src/main/java/lib/HoldResource.java:HoldResource.place`, `legacy/src/main/java/lib/HoldResource.java:52-54`
- Characterization: with three active holds, the `activeFor(...) > MAX_ACTIVE_HOLDS` check is false and an otherwise eligible `POST /holds` creates a hold and returns 201.
- Why it looks wrong: the domain graph states an active hold limit of three.

## Impact
- Ledger capabilities: `hold.place`
- Blocks: the future hold-placement migration ticket (not yet planned)

## Options
1. Preserve exactly (the target reproduces the quirk; a test pins it)
2. Fix (the target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
