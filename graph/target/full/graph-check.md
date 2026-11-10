> target_commit: 70fef8e7bc822092770b04b1bf9b5288e04d8bb6 tree.src: 0b9e1a708283d0b16665418a08833c1c03f7cded tree.templates: eb7d8e47aa813f26b8c57f87b8c8d936370b63a4 

# Graph gate: target

- 98 nodes, 165 edges
- Edges added by harness enrichers: 77

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 9
- edge `reads_from`: 9
- edge `writes_to`: 2
- edge `routes`: 20
- edge `calls`: 30

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /payments/{id}**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=GET /ui/fees/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `fees-payments` **endpoint=POST /ui/payments/{id}/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-03 open)_
- `loan-catalog` **endpoint=GET /loans**: `GET /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `LoanRepository.all` ←implements `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: `/loans/<str:loan_id>` →routes `loan_detail` →calls `LoanApplication.get_loan_text` →calls `LoanRepository.find` ←implements `DjangoLoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: `POST /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `LoanRepository.all` ←implements `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans/<str:loan_id>/return**: `POST /loans/<str:loan_id>/return` →routes `loan_return` →calls `LoanApplication.return_loan` →calls `LoanRepository.mark_returned` ←implements `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/new/**: `POST /ui/loans/new/` →routes `loan_lend_page` →calls `LoanApplication.lend` →calls `LoanRepository.create` ←implements `DjangoLoanRepository.create` →writes_to `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/<str:loan_id>/return/**: `POST /ui/loans/<str:loan_id>/return/` →routes `loan_return_page` →calls `LoanApplication.return_loan` →calls `LoanRepository.mark_returned` ←implements `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 9 owned, 0 not owned

## Entry points reaching data (for review)

- 12 of 16 pages/endpoints
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/loan-created.html`
  - no path: page `templates/loans/return-status.html`
  - no path: page `templates/base.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=16 reaching_data=12 enriched_edges=77

# Graph check: analyze

- Commit: `70fef8e7bc822092770b04b1bf9b5288e04d8bb6` · analyzed 2026-11-10T03:55:27.847Z
- Languages: python, html · frameworks: Django
- 98 nodes, 165 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 9 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 7 | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 4 | business flows → slice anchors |
| `step` | 15 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 30 | dependency resolution |
| `reads_from` | 9 | data access (read) |
| `writes_to` | 2 | data access (write) |
| `routes` | 20 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 4 | domain → flow |
| `flow_step` | 15 | flow → step |

## All node types

`file` 21, `method` 18, `step` 15, `function` 12, `endpoint` 9, `class` 8, `page` 7, `flow` 4, `domain` 3, `table` 1

## All edge types

`contains` 46, `calls` 30, `routes` 20, `flow_step` 15, `depends_on` 14, `imports` 10, `reads_from` 9, `implements` 8, `contains_flow` 4, `cross_domain` 3, `writes_to` 2, `validates` 2, `migrates` 1, `defines_schema` 1
