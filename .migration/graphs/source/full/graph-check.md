> source: martins-vds/ai-factory-synthetic-target@563c316ed51462b08fd6e58f3781a3c8b2890453 source_sha: 563c316ed51462b08fd6e58f3781a3c8b2890453 

# Graph gate: source

- 86 nodes, 119 edges
- Edges added by harness enrichers: 67

## Required types (profile graph.require)

- node `table`: 2
- node `page`: 1
- node `endpoint`: 7
- edge `reads_from`: 6
- edge `writes_to`: 3
- edge `routes`: 8
- edge `calls`: 24

## Data paths (slice specs data_paths)

- none declared

## Entry points reaching data (for review)

- 6 of 8 pages/endpoints
  - no path: endpoint `GET /about`
  - no path: page `legacy/src/main/resources/static/about.html`

## Gate

- PASS

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=8 reaching_data=6 enriched_edges=67

# Graph check: lending-library

- Commit: `563c316ed51462b08fd6e58f3781a3c8b2890453` · analyzed 2026-11-08T17:23:45.202Z
- Languages: java, shell, sql, html, xml, markdown · frameworks: Jersey, Hibernate, Maven
- 86 nodes, 119 edges, 4 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 7 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 1 | UI pages (alternative to screen) |
| `table` | 2 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 6 | business flows → slice anchors |
| `step` | 18 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 24 | dependency resolution |
| `reads_from` | 6 | data access (read) |
| `writes_to` | 3 | data access (write) |
| `routes` | 8 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 6 | domain → flow |
| `flow_step` | 18 | flow → step |

## All node types

`method` 27, `step` 18, `file` 9, `class` 7, `endpoint` 7, `flow` 6, `domain` 3, `document` 2, `config` 2, `function` 2, `table` 2, `page` 1

## All edge types

`contains` 33, `calls` 24, `flow_step` 18, `depends_on` 12, `routes` 8, `reads_from` 6, `contains_flow` 6, `writes_to` 3, `configures` 3, `defines_schema` 2, `triggers` 1, `documents` 1, `related` 1, `cross_domain` 1
