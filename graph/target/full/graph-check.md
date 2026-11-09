> target_commit: 008507cf59e92b055c00daf6cdd426d8aca4674a tree.src: 4e5319104dc4b07b3ecf6ff5b91d220b56e7d6b7 tree.templates: c7bee2d26ae6043b6437290dc24cb4db0a97314f 

# Graph gate: target

- 64 nodes, 82 edges
- Edges added by harness enrichers: 20

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 4
- edge `reads_from`: 6
- edge `writes_to`: 3
- edge `routes`: 10
- edge `calls`: 9

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /payments/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=GET /ui/fees/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /ui/payments/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `loan-catalog` **endpoint=GET /loans**: no matching node (match a node's name, or the end of its file path or id)
- `loan-catalog` **endpoint=GET /loans/{id}**: no matching node (match a node's name, or the end of its file path or id)
- `loan-catalog` **endpoint=GET /ui/loans/**: no matching node (match a node's name, or the end of its file path or id)
- `loan-catalog` **endpoint=GET /ui/loans/{id}/**: no matching node (match a node's name, or the end of its file path or id)
- `loan-circulation` **endpoint=POST /loans**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /loans/{id}/return**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /ui/loans/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /ui/loans/{id}/return/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 0 owned, 4 not owned
  - endpoint=/loans (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it
  - endpoint=/loans/<str:loan_id> (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it
  - endpoint=/ui/loans/ (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it
  - endpoint=/ui/loans/<str:loan_id>/ (src/loans/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it
  - slice library-info: entry_points.target `endpoint=GET /about` matches no node
  - slice library-info: entry_points.target `endpoint=GET /ui/about/` matches no node
  - slice loan-circulation: entry_points.target `endpoint=GET /ui/loans/new/` matches no node

## Entry points reaching data (for review)

- 3 of 7 pages/endpoints
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/detail.html`
  - no path: endpoint `/ui/loans/<str:loan_id>/`
  - no path: page `templates/base.html`

## Gate

- FAIL: slice loan-catalog: data path from `endpoint=GET /loans`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-catalog: data path from `endpoint=GET /loans/{id}`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-catalog: data path from `endpoint=GET /ui/loans/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice loan-catalog: data path from `endpoint=GET /ui/loans/{id}/`: no matching node (match a node's name, or the end of its file path or id)

AFS-RESULT gate=graph side=target verdict=fail failures=4 entry_points=7 reaching_data=3 enriched_edges=20

# Graph check: analyze

- Commit: `008507cf59e92b055c00daf6cdd426d8aca4674a` · analyzed 2026-11-09T21:22:38.041Z
- Languages: html, python · frameworks: Django
- 64 nodes, 82 edges, 4 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 4 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 3 | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 2 | bounded contexts |
| `flow` | 6 | business flows → slice anchors |
| `step` | 18 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 9 | dependency resolution |
| `reads_from` | 6 | data access (read) |
| `writes_to` | 3 | data access (write) |
| `routes` | 10 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 6 | domain → flow |
| `flow_step` | 18 | flow → step |

## All node types

`step` 18, `file` 14, `function` 9, `flow` 6, `method` 4, `endpoint` 4, `class` 3, `page` 3, `domain` 2, `table` 1

## All edge types

`contains` 18, `flow_step` 18, `routes` 10, `calls` 9, `reads_from` 6, `contains_flow` 6, `imports` 5, `depends_on` 4, `writes_to` 3, `defines_schema` 2, `cross_domain` 1
