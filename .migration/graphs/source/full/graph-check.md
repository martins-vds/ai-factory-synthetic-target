> source: martins-vds/ai-factory-synthetic-target@563c316ed51462b08fd6e58f3781a3c8b2890453 source_sha: 563c316ed51462b08fd6e58f3781a3c8b2890453 

# Graph gate: source

- 96 nodes, 148 edges
- Edges added by harness enrichers: 65

## Required types (profile graph.require)

- node `table`: 2
- node `page`: 0
- node `endpoint`: 7
- edge `reads_from`: 4
- edge `writes_to`: 2
- edge `routes`: 7
- edge `calls`: 25

## Data paths (slice specs data_paths)

- none declared

## Entry points reaching data (for review)

- 6 of 7 pages/endpoints
  - no path: endpoint `GET /about`

## Gate

- FAIL: required node type `page` is absent

AFS-RESULT gate=graph side=source verdict=fail failures=1 entry_points=7 reaching_data=6 enriched_edges=65

# Graph check: lending-library

- Commit: `563c316ed51462b08fd6e58f3781a3c8b2890453` · analyzed 2026-11-08T16:54:52.214Z
- Languages: html, java, markdown, shell, sql, xml · frameworks: Jersey, Hibernate, Maven
- 96 nodes, 148 edges, 4 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 7 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | 2 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 22 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 25 | dependency resolution |
| `reads_from` | 4 | data access (read) |
| `writes_to` | 2 | data access (write) |
| `routes` | 7 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 22 | flow → step |

## All node types

`method` 27, `step` 22, `file` 9, `function` 8, `class` 7, `endpoint` 7, `flow` 7, `domain` 3, `document` 2, `config` 2, `table` 2

## All edge types

`contains` 42, `calls` 25, `flow_step` 22, `exports` 14, `depends_on` 13, `routes` 7, `contains_flow` 7, `related` 4, `reads_from` 4, `configures` 2, `documents` 2, `writes_to` 2, `cross_domain` 2, `deploys` 1, `defines_schema` 1
