# AI Factory Swarm — synthetic target

A deliberately small migration target for [AI Factory Swarm](https://github.com/martins-vds/ai-factory-swarm)
(ADR-0037). `legacy/` is the Lending Library, a Java 17 app built so that a migration produces the harness
paths the real pilot may never reach. `legacy/SCENARIOS.yaml` lists them. Everything under `.migration/`
is written by the harness and its role sessions, never by hand.
