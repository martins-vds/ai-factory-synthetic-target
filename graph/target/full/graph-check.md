> target_commit: 9bf7ed19f5ad7536598923af0eb1b4277f4cc173 tree.src: 1bc2e8bd54c267473db993f018958e87a044028b tree.templates: 6b84672cc62e3cce89b41b562c7f10562d2caa58 

# Graph gate: target

- 282 nodes, 529 edges
- Edges added by harness enrichers: 295

## Required types (profile graph.require)

- node `table`: 2
- node `endpoint`: 18
- edge `reads_from`: 13
- edge `writes_to`: 2
- edge `routes`: 36
- edge `calls`: 146

## Data paths (slice specs data_paths)

- `fees-payments` **endpoint=GET /fees/<str:loan_id>**: `GET /fees/<str:loan_id>` →routes `fee_detail` →calls `fee_or_404` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan` — reaches 2 data node(s): holds_hold, loans_loan
- `fees-payments` **endpoint=POST /payments/<str:loan_id>**: `POST /payments/<str:loan_id>` →routes `payment` →calls `gateway_result` →calls `FeeApplication.pay` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan` — reaches 2 data node(s): holds_hold, loans_loan
- `fees-payments` **endpoint=GET /ui/fees/<str:loan_id>/**: `GET /ui/fees/<str:loan_id>/` →routes `fee_page` →calls `fee_or_404` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan` — reaches 2 data node(s): holds_hold, loans_loan
- `fees-payments` **endpoint=POST /ui/payments/<str:loan_id>/**: `POST /ui/payments/<str:loan_id>/` →routes `payment_page` →calls `FeeApplication.fee_for` →calls `DjangoFeeLoanRepository.find` →reads_from `loans_loan` — reaches 2 data node(s): holds_hold, loans_loan
- `hold-management` **endpoint=GET /holds**: `GET /holds` →routes `hold_collection` →calls `HoldApplication.place` →calls `DjangoHoldRepository.create` →writes_to `holds_hold` — reaches 2 data node(s): holds_hold, loans_loan
- `hold-management` **endpoint=POST /holds**: `POST /holds` →routes `hold_collection` →calls `HoldApplication.place` →calls `DjangoHoldRepository.create` →writes_to `holds_hold` — reaches 2 data node(s): holds_hold, loans_loan
- `hold-management` **endpoint=POST /holds/<str:hold_id>/cancel**: `POST /holds/<str:hold_id>/cancel` →routes `hold_cancel` →calls `HoldApplication.cancel` →calls `DjangoHoldRepository.find` →reads_from `holds_hold` — reaches 2 data node(s): holds_hold, loans_loan
- `loan-catalog` **endpoint=GET /loans**: `GET /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/loans/<str:loan_id>**: `/loans/<str:loan_id>` →routes `loan_detail` →calls `LoanApplication.get_loan_text` →calls `DjangoLoanRepository.find` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/**: `/ui/loans/` →routes `loan_catalog` →reads_from `loans_loan`
- `loan-catalog` **endpoint=/ui/loans/<str:loan_id>/**: `/ui/loans/<str:loan_id>/` →routes `loan_catalog_detail` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans**: `POST /loans` →routes `loan_collection` →calls `LoanApplication.list_loans_text` →calls `DjangoLoanRepository.all` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /loans/<str:loan_id>/return**: `POST /loans/<str:loan_id>/return` →routes `loan_return` →calls `LoanApplication.return_loan` →calls `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/new/**: `POST /ui/loans/new/` →routes `loan_lend_page` →calls `LoanApplication.lend` →calls `DjangoLoanRepository.create` →writes_to `loans_loan`
- `loan-circulation` **endpoint=POST /ui/loans/<str:loan_id>/return/**: `POST /ui/loans/<str:loan_id>/return/` →routes `loan_return_page` →calls `LoanApplication.return_loan` →calls `DjangoLoanRepository.mark_returned` →reads_from `loans_loan`
- `monthly-report` **command=monthly_report**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)

## Entry points owned by a slice (ADR-0026)

- 19 owned, 0 not owned

## Entry points reaching data (for review)

- 21 of 30 pages/endpoints
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

- FAIL: slice monthly-report: data path from `command=monthly_report`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)

AFS-RESULT gate=graph side=target verdict=fail failures=1 entry_points=30 reaching_data=21 enriched_edges=295

# Graph check: analyze

- Commit: `9bf7ed19f5ad7536598923af0eb1b4277f4cc173` · analyzed 2026-11-24T04:46:11.741Z
- Languages: html, python · frameworks: Django
- 282 nodes, 529 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 18 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 12 | UI pages (alternative to screen) |
| `table` | 2 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 5 | bounded contexts |
| `flow` | 10 | business flows → slice anchors |
| `step` | 36 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 146 | dependency resolution |
| `reads_from` | 13 | data access (read) |
| `writes_to` | 2 | data access (write) |
| `routes` | 36 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 10 | domain → flow |
| `flow_step` | 36 | flow → step |

## All node types

`method` 68, `file` 54, `class` 43, `step` 36, `function` 33, `endpoint` 18, `page` 12, `flow` 10, `domain` 5, `table` 2, `command` 1

## All edge types

`calls` 146, `contains` 132, `exports` 53, `implements` 44, `imports` 36, `routes` 36, `flow_step` 36, `depends_on` 13, `reads_from` 13, `contains_flow` 10, `cross_domain` 4, `related` 2, `defines_schema` 2, `writes_to` 2
