> target_commit: 4f4bb689a7b8998a352921816dd7bb3c39556582 tree.src: 785e3232b0ffcce762b6bab45340887a2b7936d0 tree.templates: ae3ec611a9f633a95e12f9a34bc318adb53813c8 

# Graph gate: target

- 147 nodes, 219 edges
- Edges added by harness enrichers: 106

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 13
- edge `reads_from`: 7
- edge `writes_to`: 1
- edge `routes`: 28
- edge `calls`: 44

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/<str:loan_id>**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `fees-payments` **endpoint=POST /payments/<str:loan_id>**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `fees-payments` **endpoint=GET /ui/fees/<str:loan_id>/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `fees-payments` **endpoint=POST /ui/payments/<str:loan_id>/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-catalog` **endpoint=GET /loans**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-circulation` **endpoint=POST /loans/<str:loan_id>/return**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-circulation` **endpoint=POST /ui/loans/new/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `loan-circulation` **endpoint=POST /ui/loans/<str:loan_id>/return/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 13 owned, 0 not owned

## Entry points reaching data (for review)

- 4 of 23 pages/endpoints
  - no path: page `templates/fees/detail.html`
  - no path: page `templates/fees/payment-status.html`
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/detail.html`
  - no path: page `templates/loans/loan-created.html`
  - no path: page `templates/loans/return-status.html`
  - no path: endpoint `GET /fees/<str:loan_id>`
  - no path: endpoint `POST /payments/<str:loan_id>`
  - no path: endpoint `GET /ui/fees/<str:loan_id>/`
  - no path: endpoint `POST /ui/payments/<str:loan_id>/`
  - no path: endpoint `GET /loans`
  - no path: endpoint `POST /loans`
  - no path: endpoint `POST /loans/<str:loan_id>/return`
  - no path: endpoint `/loans/<str:loan_id>`
  - no path: endpoint `GET /ui/loans/new/`
  - no path: endpoint `POST /ui/loans/new/`
  - no path: endpoint `POST /ui/loans/<str:loan_id>/return/`
  - no path: page `templates/base.html`
  - no path: page `templates/fees/payment-form.html`

## Gate

- FAIL: slice fees-payments: data path from `endpoint=GET /fees/<str:loan_id>`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice fees-payments: data path from `endpoint=POST /payments/<str:loan_id>`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice fees-payments: data path from `endpoint=GET /ui/fees/<str:loan_id>/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice fees-payments: data path from `endpoint=POST /ui/payments/<str:loan_id>/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-catalog: data path from `endpoint=GET /loans`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-catalog: data path from `endpoint=/loans/<str:loan_id>`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /loans`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /loans/<str:loan_id>/return`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /ui/loans/new/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice loan-circulation: data path from `endpoint=POST /ui/loans/<str:loan_id>/return/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)

AFS-RESULT gate=graph side=target verdict=fail failures=10 entry_points=23 reaching_data=4 enriched_edges=106

# Graph check: analyze

- Commit: `4f4bb689a7b8998a352921816dd7bb3c39556582` · analyzed 2026-11-10T17:04:51.770Z
- Languages: html, python · frameworks: Django
- 147 nodes, 219 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 13 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 10 | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 2 | bounded contexts |
| `flow` | 5 | business flows → slice anchors |
| `step` | 18 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 44 | dependency resolution |
| `reads_from` | 7 | data access (read) |
| `writes_to` | 1 | data access (write) |
| `routes` | 28 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 5 | domain → flow |
| `flow_step` | 18 | flow → step |

## All node types

`file` 31, `method` 28, `class` 20, `function` 19, `step` 18, `endpoint` 13, `page` 10, `flow` 5, `domain` 2, `table` 1

## All edge types

`contains` 74, `calls` 44, `routes` 28, `imports` 19, `flow_step` 18, `exports` 12, `reads_from` 7, `depends_on` 5, `contains_flow` 5, `related` 4, `defines_schema` 1, `writes_to` 1, `cross_domain` 1
