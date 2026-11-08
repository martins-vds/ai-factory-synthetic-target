# Loan export does not escape field delimiters

## Question
The source joins raw loan fields with semicolons and newlines without escaping them. Preserve this format, escape values, or something else?

## Evidence
- Source: `method:legacy/src/main/java/lib/LoanResource.java:LoanResource.line`, `legacy/src/main/java/lib/LoanResource.java:52-55`; format contract: `legacy/docs/export-csv.md:1-4`
- Characterization: tier-A characterization exercised the documented export with seeded values; delimiter-containing fields were not separately exercised.
- Why it looks wrong: accepted member or ISBN values containing `;` or a line break make the documented one-loan-per-line export ambiguous.

## Impact
- Ledger capabilities: `loan.text-export`, `loan.lend`
- Blocks: future migration tickets implementing these capabilities (not yet filed)

## Options
1. Preserve exactly (raw fields remain unescaped; tests pin this behavior)
2. Fix (the target escapes or rejects delimiter-containing fields; the divergence is recorded with this ticket as approval)
3. Other
