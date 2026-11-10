> target_commit: 740c4466373f0d5fd0c355c251627accbd90cb3c tree.src: 0b9e1a708283d0b16665418a08833c1c03f7cded tree.templates: eb7d8e47aa813f26b8c57f87b8c8d936370b63a4 

# Graph gate: target

- 116 nodes, 161 edges
- Edges added by harness enrichers: 68

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 9
- edge `reads_from`: 8
- edge `writes_to`: 1
- edge `routes`: 20
- edge `calls`: 24

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /payments/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=GET /ui/fees/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /ui/payments/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `loan-catalog` **endpoint=/loans**: no matching node (match a node's name, or the end of its file path or id)
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-circulation` **endpoint=POST /loans/{id}/return**: no matching node (match a node's name, or the end of its file path or id)
- `loan-circulation` **endpoint=POST /ui/loans/**: no matching node (match a node's name, or the end of its file path or id)
- `loan-circulation` **endpoint=POST /ui/loans/{id}/return/**: no matching node (match a node's name, or the end of its file path or id)
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 7 owned, 2 not owned
  - endpoint=GET /loans (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it
  - endpoint=POST /ui/loans/new/ (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it

## Entry points reaching data (for review)

- 4 of 16 pages/endpoints
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/detail.html`
  - no path: page `templates/loans/loan-created.html`
  - no path: page `templates/loans/return-status.html`
  - no path: endpoint `GET /loans`
  - no path: endpoint `POST /loans`
  - no path: endpoint `POST /loans/<str:loan_id>/return`
  - no path: endpoint `/loans/<str:loan_id>`
  - no path: endpoint `GET /ui/loans/new/`
  - no path: endpoint `POST /ui/loans/new/`
  - no path: endpoint `POST /ui/loans/<str:loan_id>/return/`
  - no path: page `templates/base.html`

## Gate

- FAIL: slice loan-catalog: data path from `endpoint=/loans`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-catalog: data path from `endpoint=/loans/<str:loan_id>`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /loans`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /loans/{id}/return`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-circulation: data path from `endpoint=POST /ui/loans/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-circulation: data path from `endpoint=POST /ui/loans/{id}/return/`: no matching node (match a node's name, or the end of its file path or id)

AFS-RESULT gate=graph side=target verdict=fail failures=6 entry_points=16 reaching_data=4 enriched_edges=68

# Graph check: analyze

- Commit: `740c4466373f0d5fd0c355c251627accbd90cb3c` · analyzed 2026-11-10T01:58:02.140Z
- Languages: html, python · frameworks: Django
- 116 nodes, 161 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 9 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 7 | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 24 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 24 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 1 | data access (write) |
| `routes` | 20 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 24 | flow → step |

## All node types

`step` 24, `file` 21, `method` 18, `function` 16, `class` 9, `endpoint` 9, `page` 7, `flow` 7, `domain` 4, `table` 1

## All edge types

`contains` 42, `calls` 24, `flow_step` 24, `routes` 20, `imports` 11, `reads_from` 8, `depends_on` 7, `serves` 7, `contains_flow` 7, `cross_domain` 4, `implements` 2, `validates` 2, `migrates` 1, `defines_schema` 1, `writes_to` 1
