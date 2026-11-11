> target_commit: 7d4b249e342a94e7176ebf3e1d370f81d7156b16 tree.src: 304c585502c55c196ab27dbc31f71b6204043fa6 tree.templates: 9659173daf2010f59ffc9f84131337c9b13f07b8 

# Graph gate: target

- 162 nodes, 292 edges
- Edges added by harness enrichers: 146

## Required types (profile graph.require)

- node `table`: 1
- node `endpoint`: 15
- edge `reads_from`: 7
- edge `writes_to`: 1
- edge `routes`: 32
- edge `calls`: 69

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/<str:loan_id>**: `GET /fees/<str:loan_id>` →routes `fee_detail` →calls `_fee_or_404` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan`
- `fees-payments` **endpoint=POST /payments/<str:loan_id>**: `POST /payments/<str:loan_id>` →routes `payment` →calls `_gateway_result` →calls `FeeApplication.pay` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan`
- `fees-payments` **endpoint=GET /ui/fees/<str:loan_id>/**: `GET /ui/fees/<str:loan_id>/` →routes `fee_page` →calls `_fee_or_404` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan`
- `fees-payments` **endpoint=POST /ui/payments/<str:loan_id>/**: `POST /ui/payments/<str:loan_id>/` →routes `payment_page` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=GET /loans**: `GET /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: `/loans/<str:loan_id>` →routes `loan_detail` →calls `LoanApplication.get_loan_text` →calls `DjangoLoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: `POST /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans/<str:loan_id>/return**: `POST /loans/<str:loan_id>/return` →routes `loan_return` →calls `LoanApplication.return_loan` →calls `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/new/**: `POST /ui/loans/new/` →routes `loan_lend_page` →calls `LoanApplication.lend` →calls `DjangoLoanRepository.create` →writes_to `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/<str:loan_id>/return/**: `POST /ui/loans/<str:loan_id>/return/` →routes `loan_return_page` →calls `LoanApplication.return_loan` →calls `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `monthly-report` **command=monthly_report**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: LL-05 open)_

## Entry points owned by a slice (ADR-0026)

- 15 owned, 0 not owned

## Entry points reaching data (for review)

- 18 of 27 pages/endpoints
  - no path: page `templates/fees/payment-status.html`
  - no path: page `templates/library_info/legacy_about.html`
  - no path: page `templates/library_info/about.html`
  - no path: page `templates/loans/list.html`
  - no path: page `templates/loans/loan-created.html`
  - no path: page `templates/loans/return-status.html`
  - no path: endpoint `GET /about`
  - no path: endpoint `GET /ui/about/`
  - no path: page `templates/base.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=146

# Graph check: analyze

- Commit: `7d4b249e342a94e7176ebf3e1d370f81d7156b16` · analyzed 2026-11-11T01:26:58.257Z
- Languages: html, python · frameworks: Django
- 162 nodes, 292 edges, 6 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 15 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 12 | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 6 | business flows → slice anchors |
| `step` | 20 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 69 | dependency resolution |
| `reads_from` | 7 | data access (read) |
| `writes_to` | 1 | data access (write) |
| `routes` | 32 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 6 | domain → flow |
| `flow_step` | 20 | flow → step |

## All node types

`file` 36, `method` 28, `function` 21, `class` 20, `step` 20, `endpoint` 15, `page` 12, `flow` 6, `domain` 3, `table` 1

## All edge types

`contains` 77, `calls` 69, `routes` 32, `exports` 31, `imports` 20, `flow_step` 20, `implements` 16, `depends_on` 9, `reads_from` 7, `contains_flow` 6, `related` 2, `defines_schema` 1, `writes_to` 1, `cross_domain` 1
