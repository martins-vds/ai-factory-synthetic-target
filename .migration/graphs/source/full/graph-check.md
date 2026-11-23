> source: martins-vds/ai-factory-synthetic-target@96d50b85a9a456d9c0a58f080414b3badb501e59 source_sha: 96d50b85a9a456d9c0a58f080414b3badb501e59 

# Graph gate: source

- 167 nodes, 248 edges
- Edges added by harness enrichers: 125

## Required types (profile graph.require)

- node `table`: 4
- node `page`: 1
- node `endpoint`: 10
- edge `reads_from`: 8
- edge `writes_to`: 4
- edge `routes`: 11
- edge `calls`: 48

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/{id}**: `GET /fees/{id}` →routes `LateFeeView.page` →calls `LoanRepository.find` →reads_from `LOAN`
- `fees-payments` **endpoint=POST /payments/{id}**: `POST /payments/{id}` →routes `FinePayments.pay` →calls `LoanRepository.find` →reads_from `LOAN`
- `loan-catalog` **endpoint=GET /loans**: `GET /loans` →routes `LoanResource.list` →calls `LoanRepository.all` →reads_from `LOAN`
- `loan-catalog` **endpoint=GET /loans/{id}**: `GET /loans/{id}` →routes `LoanResource.one` →calls `LoanRepository.find` →reads_from `LOAN`
- `loan-circulation` **endpoint=POST /loans**: `POST /loans` →routes `LoanResource.lend` →calls `LoanRepository.lend` →reads_from `LOAN`
- `loan-circulation` **endpoint=POST /loans/{id}/return**: `POST /loans/{id}/return` →routes `LoanResource.giveBack` →calls `LoanRepository.markReturned` →reads_from `LOAN`

## Entry points reaching data (for review)

- 9 of 11 pages/endpoints
  - no path: endpoint `GET /about`
  - no path: page `legacy/src/main/resources/static/about.html`

## Gate

- PASS

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=11 reaching_data=9 enriched_edges=125

# Graph check: lending-library

- Commit: `96d50b85a9a456d9c0a58f080414b3badb501e59` · analyzed 2026-11-23T05:18:00.145Z
- Languages: html, java, markdown, shell, sql, xml · frameworks: Jersey, Hibernate, H2, Maven
- 167 nodes, 248 edges, 4 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 10 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 1 | UI pages (alternative to screen) |
| `table` | 4 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 5 | bounded contexts |
| `flow` | 10 | business flows → slice anchors |
| `step` | 31 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 48 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 4 | data access (write) |
| `routes` | 11 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 12 | domain → flow |
| `flow_step` | 31 | flow → step |

## All node types

`method` 51, `step` 31, `function` 29, `file` 12, `class` 10, `endpoint` 10, `flow` 10, `domain` 5, `table` 4, `document` 2, `config` 2, `page` 1

## All edge types

`contains` 91, `calls` 48, `flow_step` 31, `depends_on` 21, `contains_flow` 12, `routes` 11, `exports` 10, `reads_from` 8, `defines_schema` 4, `writes_to` 4, `configures` 3, `documents` 2, `cross_domain` 2, `deploys` 1
