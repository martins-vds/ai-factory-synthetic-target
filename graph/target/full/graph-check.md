> target_commit: 88605f51a9b919dd3aba3aad04bbaa307b2f24d2 tree.src: 4e5319104dc4b07b3ecf6ff5b91d220b56e7d6b7 tree.templates: c7bee2d26ae6043b6437290dc24cb4db0a97314f 

# Graph gate: target

- 66 nodes, 90 edges
- Edges added by harness enrichers: 21

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 4
- edge `reads_from`: 4
- edge `writes_to`: 1
- edge `routes`: 6
- edge `calls`: 10

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /payments/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=GET /ui/fees/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /ui/payments/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `loan-catalog` **endpoint=/loans**: `/loans` →routes `loan_list` →calls `list_loans_text` →calls `LoanRepository` →contains `LoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: `/loans/<str:loan_id>` →routes `loan_detail` →calls `get_loan_text` →calls `LoanRepository` →contains `LoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /loans/{id}/return**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /ui/loans/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `loan-circulation` **endpoint=POST /ui/loans/{id}/return/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-02 open)_
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 4 owned, 0 not owned

## Entry points reaching data (for review)

- 4 of 7 pages/endpoints
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/detail.html`
  - no path: page `templates/base.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=4 enriched_edges=21

# Graph check: analyze

- Commit: `88605f51a9b919dd3aba3aad04bbaa307b2f24d2` · analyzed 2026-11-09T22:47:45.123Z
- Languages: html, python · frameworks: Django
- 66 nodes, 90 edges, 5 layers

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
| `step` | 17 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 10 | dependency resolution |
| `reads_from` | 4 | data access (read) |
| `writes_to` | 1 | data access (write) |
| `routes` | 6 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 6 | domain → flow |
| `flow_step` | 17 | flow → step |

## All node types

`step` 17, `file` 14, `function` 12, `flow` 6, `method` 4, `endpoint` 4, `class` 3, `page` 3, `domain` 2, `table` 1

## All edge types

`contains` 18, `flow_step` 17, `calls` 10, `depends_on` 8, `exports` 7, `routes` 6, `contains_flow` 6, `imports` 5, `related` 5, `reads_from` 4, `migrates` 1, `defines_schema` 1, `writes_to` 1, `cross_domain` 1
