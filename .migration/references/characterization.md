# Characterization evidence

## Source and environment

- Source: `martins-vds/ai-factory-synthetic-target`, commit `563c316ed51462b08fd6e58f3781a3c8b2890453`, path `legacy`.
- Verified the pinned and checked-out `legacy/` trees are identical: both resolve to tree `1e683e0091beb079121c2ab6d223573ae29186ae`.
- Runtime: OpenJDK 17.0.21, Maven 3.10.0.
- Source stack from `legacy/pom.xml`: Java 17, Maven, Jersey/JAX-RS 3.1.5, Hibernate ORM 6.4.4.Final, H2 2.2.224. Source files are ASCII (UTF-8-compatible).

## Commands and observations

The initial invocation `./run.sh` from the repository root failed with exit 127 because the script is in `legacy/`. The corrected run was:

```sh
cd /home/runner/work/ai-factory-synthetic-target/ai-factory-synthetic-target/legacy
./run.sh
```

`run.sh` ran `mvn -q -B package -DskipTests` successfully, then started `lib.App` on port 8080. Hibernate connected to the in-memory H2 database and Grizzly reported `Lending Library listening on 8080`. Jersey logged warnings that its registered resource classes were ignored as providers, but the probes below all reached the expected endpoints.

With the server running, these commands returned:

| Command | Result |
|---|---|
| `curl -i --max-time 5 http://localhost:8080/loans` | HTTP 200; three seeded loan rows (`L1`, `L2`, `L3`) in semicolon-separated form. |
| `curl -i --max-time 5 http://localhost:8080/fees/L3` | HTTP 200; `Fee: $4.75` and `19 day(s) late`. |
| `curl -i --max-time 5 -X POST http://localhost:8080/payments/L3` | HTTP 502; body `payment gateway unavailable`. |
| `curl -i --max-time 5 http://localhost:8080/about` | HTTP 200; HTML title and heading identify the Lending Library. |
| `curl -i --max-time 5 -X POST -d member=dee -d isbn=123 http://localhost:8080/loans` | HTTP 201; body `L4;dee;123;2026-11-08;2026-11-22;`. |

These observations establish characterization tier A: the pinned source can be built, run, and exercised through its HTTP interface. No source files were changed.
