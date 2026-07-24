# Tasks: INQACCCU Modernization Backlog

## Metadata
- Artifact ID: TASK-INQACCCU-20260724
- Agent Role: TaskAgent

## Task List

### TASK-001 Build Contract and DTO Models
- Requirement Links: FR-008, FR-005
- Scope:
- Define API DTOs for accounts and totalCount
- Enforce schema constraints from openapi.yaml
- Done When:
- DTO tests validate required fields and formats

### TASK-002 Implement Input Validation and Sentinel Checks
- Requirement Links: FR-001
- Scope:
- Validate 10-digit customerId
- Reject 0000000000 and 9999999999 with legacy-equivalent not-found semantics
- Done When:
- Unit tests cover valid and invalid/sentinel inputs

### TASK-003 Implement Customer Existence Gate
- Requirement Links: FR-002
- Scope:
- Add customer repository interface and service check before account query
- Done When:
- Tests verify account repository is not called when customer check fails

### TASK-004 Implement Account Retrieval Service
- Requirement Links: FR-003, FR-004, FR-006
- Scope:
- Query by customerId and sortCode 987654
- Limit records to 20
- Preserve success semantics for zero rows
- Done When:
- Tests validate filters, cap, and zero-row success

### TASK-005 Implement Failure Stage Mapping
- Requirement Links: FR-007
- Scope:
- Map open/read/close stage failures to equivalent legacy fail codes 2/3/4
- Done When:
- Tests assert deterministic error mapping

### TASK-006 Implement Field Mapping and Defaults
- Requirement Links: FR-005, FR-008
- Scope:
- Map COMM-* values to account response fields
- Apply currency=GBP and status=ACTIVE defaults
- Done When:
- Mapping tests verify each output field

### TASK-007 Implement POC Repository Adapters
- Requirement Links: FR-009
- Scope:
- Provide mock repository implementations for customer and account data
- Done When:
- Service tests run without mainframe access

### TASK-008 Add Contract and Integration Tests
- Requirement Links: FR-001..FR-009
- Scope:
- Add endpoint tests for 200/4xx/5xx and payload shape
- Done When:
- Test-spec coverage matrix fully green
