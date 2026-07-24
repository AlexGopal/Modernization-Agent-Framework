# Business Rules: INQACCCU

## Metadata
- Artifact ID: BR-INQACCCU-20260724
- Agent Role: BusinessRulesAgent
- Source of Truth: program-analysis.md, COBOL and copybooks

## Rules

### BR-001 Customer Existence Gate
Account inquiry must run only when CUSTOMER-NUMBER is valid and customer lookup (INQCUST) is successful.

### BR-002 Sentinel Customer Rejection
CUSTOMER-NUMBER values 0000000000 and 9999999999 are treated as non-valid and must return no accounts.

### BR-003 Deterministic Failure Signaling
When lookup or DB2 operations fail, COMM-SUCCESS must be 'N' and COMM-FAIL-CODE must be set as:
- 1: customer not found/invalid input
- 2: DB2 cursor open failure
- 3: DB2 fetch failure
- 4: DB2 cursor close failure

### BR-004 No-Row Success
If DB2 fetch reaches SQLCODE +100 (no more rows), the transaction is a logical success and COMM-SUCCESS remains 'Y'.

### BR-005 Result Size Limit
The response can contain at most 20 account entries.

### BR-006 Sort Code Filter
Account query must use static sort code from copybook constant SORTCODE=987654 together with customer number.

### BR-007 Date Reformatting
DB2 DATE fields (ACCOUNT_OPENED, ACCOUNT_LAST_STATEMENT, ACCOUNT_NEXT_STATEMENT) must be emitted in DDMMYYYY numeric format.

### BR-008 Currency and Status Defaults
REST projection uses:
- currency='GBP'
- status='ACTIVE'
for each account row, per existing mapping assets.

### BR-009 POC Isolation
POC mode must not connect to real mainframe systems; use adapter/repository abstraction with mock/stub implementation.

## Rule Coverage Intent
Each business rule maps to functional requirements, tasks, and test cases in downstream artifacts.
