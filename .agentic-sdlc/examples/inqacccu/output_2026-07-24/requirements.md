# Requirements: INQACCCU Modernization

## Metadata
- Artifact ID: FR-INQACCCU-20260724
- Agent Role: RequirementsAgent
- Source: business-rules.md

## Functional Requirements

### FR-001 Validate Customer Input
System shall accept a 10-digit customerId and reject sentinel invalid values 0000000000 and 9999999999.

Acceptance Criteria:
- AC-001.1: Input 0000000000 returns failure mapped to customer-not-found behavior.
- AC-001.2: Input 9999999999 returns failure mapped to customer-not-found behavior.

### FR-002 Verify Customer Existence
System shall perform customer existence check before account retrieval.

Acceptance Criteria:
- AC-002.1: If customer lookup fails, no account query is executed.
- AC-002.2: Failure result preserves legacy semantics (equivalent to COMM-FAIL-CODE 1).

### FR-003 Retrieve Accounts by Customer and Sort Code
System shall retrieve account rows filtered by customer number and static sort code 987654.

Acceptance Criteria:
- AC-003.1: Query inputs include customer number and sort code 987654.
- AC-003.2: Returned list includes only rows matching both filters.

### FR-004 Enforce Max Result Size
System shall return at most 20 account entries.

Acceptance Criteria:
- AC-004.1: If more than 20 rows are available, only first 20 are returned.

### FR-005 Preserve Date and Monetary Field Mapping
System shall map account fields and preserve date conversions and monetary values.

Acceptance Criteria:
- AC-005.1: openedDate, lastStatementDate, nextStatementDate use DDMMYYYY semantics from legacy.
- AC-005.2: availableBalance and actualBalance retain precision equivalent to DECIMAL(10,2).

### FR-006 Preserve No-Row Success
System shall return successful outcome when no accounts are found for valid customer.

Acceptance Criteria:
- AC-006.1: totalCount=0 is valid success response.
- AC-006.2: accounts array is empty in no-row scenario.

### FR-007 Preserve Failure Semantics for Data Access Stages
System shall preserve distinct failure semantics for cursor open/fetch/close equivalents.

Acceptance Criteria:
- AC-007.1: Data-open failure maps to failure code equivalent 2.
- AC-007.2: Data-read failure maps to failure code equivalent 3.
- AC-007.3: Data-close failure maps to failure code equivalent 4.

### FR-008 Return API Contract Fields
System shall return API body containing accounts[] and totalCount consistent with existing mapping assets.

Acceptance Criteria:
- AC-008.1: Each account returns accountId, accountType, currency, accountNumber, sortCode, status.
- AC-008.2: currency defaults to GBP.
- AC-008.3: status defaults to ACTIVE.

### FR-009 POC Isolation
System shall implement repository interface with mock/stub adapter and no live mainframe call in POC mode.

Acceptance Criteria:
- AC-009.1: No runtime dependency on CICS/DB2 host connectivity for test runs.

## Non-Functional Requirements
- NFR-001: Thin controllers; business logic in service layer.
- NFR-002: Structured logging with correlation id.
- NFR-003: Input validation and deterministic error model.
- NFR-004: Traceability maintained from BR to FR to TASK to TC.
