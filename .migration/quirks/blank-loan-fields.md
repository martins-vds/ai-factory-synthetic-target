# Blank loan fields are accepted

## Question
`POST /loans` rejects missing member or ISBN values but accepts empty strings and creates the loan. Preserve blank values, reject blank fields, or something else?

## Evidence
- Source: `endpoint:legacy/src/main/java/lib/LoanResource.java:POST /loans`, `legacy/src/main/java/lib/LoanResource.java:37-43`
- Characterization: tier-A characterization exercised lending with non-empty values; blank form fields were not separately exercised.
- Why it looks wrong: fields described as required can be stored empty, and the request still receives HTTP 201.

## Impact
- Ledger capabilities: `loan.lend`
- Blocks: future migration tickets implementing this capability (not yet filed)

## Options
1. Preserve exactly (empty strings are accepted; tests pin this behavior)
2. Fix (the target rejects blank fields; the divergence is recorded with this ticket as approval)
3. Other
