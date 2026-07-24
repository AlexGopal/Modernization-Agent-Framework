# Test Specification: INQACCCU Modernization

## Metadata
- Artifact ID: TS-INQACCCU-20260724
- Agent Role: TestSpecAgent

## Test Cases

### TC-001 Valid Customer with Accounts
- Covers: BR-001, BR-006, FR-002, FR-003
- Input: customerId=1234567890 (exists)
- Expected:
- HTTP 200
- accounts length > 0 and <= 20
- totalCount equals accounts length

### TC-002 Valid Customer with No Accounts
- Covers: BR-004, FR-006
- Input: existing customer with zero matching rows
- Expected:
- HTTP 200
- accounts=[]
- totalCount=0

### TC-003 Sentinel Zero Customer
- Covers: BR-002, FR-001
- Input: customerId=0000000000
- Expected:
- Not-found semantic outcome (legacy fail equivalent code 1)

### TC-004 Sentinel Nines Customer
- Covers: BR-002, FR-001
- Input: customerId=9999999999
- Expected:
- Not-found semantic outcome (legacy fail equivalent code 1)

### TC-005 Customer Not Found by Repository
- Covers: BR-001, FR-002
- Input: syntactically valid non-existing customerId
- Expected:
- Service returns not-found semantic outcome
- Account repository call is skipped

### TC-006 Query Uses Static Sort Code
- Covers: BR-006, FR-003
- Input: valid existing customerId
- Expected:
- Repository invoked with sortCode 987654

### TC-007 Result Capped to 20
- Covers: BR-005, FR-004
- Input: dataset with >20 rows
- Expected:
- only first 20 mapped and returned

### TC-008 Field Mapping and Defaults
- Covers: BR-007, BR-008, FR-005, FR-008
- Expected per account:
- accountId/accountNumber from COMM-ACCNO
- accountType from COMM-ACC-TYPE
- sortCode from COMM-SCODE
- currency=GBP
- status=ACTIVE

### TC-009 Open Stage Failure Mapping
- Covers: BR-003, FR-007
- Setup: repository throws open-stage error
- Expected:
- fail semantic equivalent code 2

### TC-010 Read Stage Failure Mapping
- Covers: BR-003, FR-007
- Setup: repository throws read-stage error
- Expected:
- fail semantic equivalent code 3

### TC-011 Close Stage Failure Mapping
- Covers: BR-003, FR-007
- Setup: repository throws close-stage error
- Expected:
- fail semantic equivalent code 4

### TC-012 Contract Validation
- Covers: FR-008
- Expected:
- response schema matches openapi.yaml
