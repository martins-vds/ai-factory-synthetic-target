> source: martins-vds/ai-factory-synthetic-target@563c316ed51462b08fd6e58f3781a3c8b2890453 source_sha: 563c316ed51462b08fd6e58f3781a3c8b2890453 

# Graph gate: source

- 107 nodes, 144 edges
- Edges added by harness enrichers: 69

## Required types (profile graph.require)

- node `table`: 1
- node `page`: 0
- node `endpoint`: 7
- edge `reads_from`: 5
- edge `writes_to`: 3
- edge `routes`: 7
- edge `calls`: 28

## Data paths (slice specs data_paths)

- none declared

## Entry points reaching data (for review)

- 6 of 7 pages/endpoints
  - no path: endpoint `GET /about`

## Gate

- FAIL: required node type `page` is absent

AFS-RESULT gate=graph side=source verdict=fail failures=1 entry_points=7 reaching_data=6 enriched_edges=69

# Graph check: lending-library

- Commit: `563c316ed51462b08fd6e58f3781a3c8b2890453` · analyzed 2026-11-08T16:53:32.335Z
- Languages: html, java, markdown, shell, sql, xml · frameworks: Jersey, Hibernate, H2
- 107 nodes, 144 edges, 4 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 7 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 8 | business flows → slice anchors |
| `step` | 23 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 28 | dependency resolution |
| `reads_from` | 5 | data access (read) |
| `writes_to` | 3 | data access (write) |
| `routes` | 7 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 8 | domain → flow |
| `flow_step` | 23 | flow → step |

## All node types

`method` 27, `step` 23, `function` 17, `file` 10, `flow` 8, `class` 7, `endpoint` 7, `domain` 3, `document` 2, `config` 2, `table` 1

## All edge types

`contains` 47, `calls` 28, `flow_step` 23, `depends_on` 14, `contains_flow` 8, `routes` 7, `reads_from` 5, `writes_to` 3, `cross_domain` 3, `configures` 2, `triggers` 1, `documents` 1, `related` 1, `defines_schema` 1
