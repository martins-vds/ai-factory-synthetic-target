# Restart resets loan data

## Question
At every application startup, the source creates an in-memory H2 database with a `drop-and-create` schema and reloads the three seed loans. Preserve this reset-on-restart behavior, make loans persistent, or something else?

## Evidence
- Source: `config:legacy/src/main/resources/META-INF/persistence.xml`, `legacy/src/main/resources/META-INF/persistence.xml:6-10`
- Characterization: tier A confirms startup connects to in-memory H2, the seed loans are served, and a new loan can be created; restart persistence was not separately exercised.
- Why it looks wrong: loans added or returned while the app runs are discarded when it restarts, despite the interface allowing users to create and update loans.

## Impact
- Ledger capabilities: `data.loan-storage`, `data.seed-records`, `application.startup`
- Blocks: future migration tickets implementing these capabilities (not yet filed)

## Options
1. Preserve exactly (the target resets its data on startup; tests pin this behavior)
2. Fix (the target persists loan data; the divergence is recorded with this ticket as approval)
3. Other
