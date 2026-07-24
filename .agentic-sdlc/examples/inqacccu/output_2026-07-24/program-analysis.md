# Program Analysis: INQACCCU

## Metadata
- Artifact ID: PA-INQACCCU-20260724
- Agent Role: LegacyAnalysisAgent
- Source Program: INQACCCU
- Source Repository: https://github.com/IBM/Bank-of-Z
- Analysis Date: 2026-07-24

## Inputs
- legacy/cobol/INQACCCU.cbl
- legacy/copybooks/INQACCCU.cpy
- legacy/copybooks/INQACCCZ.cpy
- legacy/copybooks/INQCUSTZ.cpy
- legacy/copybooks/ACCDB2.cpy
- legacy/copybooks/ACCOUNT.cpy
- legacy/copybooks/CUSTOMER.cpy
- legacy/copybooks/ABNDINFO.cpy
- legacy/copybooks/SORTCODE.cpy
- legacy/supporting/api/request.yaml
- legacy/supporting/api/response_200.yaml
- legacy/supporting/api/response_mapping.yaml

## Program Purpose
INQACCCU receives a customer number in COMMAREA, validates customer existence by linking to INQCUST, then reads up to 20 account rows from DB2 ACCOUNT table for that customer and sort code. It returns account details and status indicators in COMMAREA.

## Interface Summary

### Input COMMAREA fields
- CUSTOMER-NUMBER (PIC 9(10))

### Output control fields
- COMM-SUCCESS (Y/N)
- COMM-FAIL-CODE (0,1,2,3,4 observed)
- CUSTOMER-FOUND (Y/N)
- NUMBER-OF-ACCOUNTS (0..20)

### Output account repeating fields (OCCURS 1 TO 20)
- COMM-EYE
- COMM-CUSTNO
- COMM-SCODE
- COMM-ACCNO
- COMM-ACC-TYPE
- COMM-INT-RATE
- COMM-OPENED (derived from DB2 DATE)
- COMM-OVERDRAFT
- COMM-LAST-STMT-DT (derived from DB2 DATE)
- COMM-NEXT-STMT-DT (derived from DB2 DATE)
- COMM-AVAIL-BAL
- COMM-ACTUAL-BAL

## Observed Legacy Flow
1. Initialize COMM-SUCCESS='N', COMM-FAIL-CODE='0'.
2. Register CICS HANDLE ABEND for custom ABEND handling section.
3. Run CUSTOMER-CHECK:
- If CUSTOMER-NUMBER is 0 or 9999999999, set CUSTOMER-FOUND='N' and return with 0 accounts.
- Else LINK to INQCUST and set CUSTOMER-FOUND based on INQCUST-INQ-SUCCESS.
4. If CUSTOMER-FOUND='N', set COMM-FAIL-CODE='1' and return.
5. For valid customer, open DB2 cursor filtered by CUSTOMER-NUMBER and static SORTCODE.
6. FETCH loop copies DB2 columns into COMMAREA account array.
7. If SQLCODE +100, stop fetch loop and return success with collected rows.
8. Cursor close executed after fetch loop.
9. For SQL failures on OPEN/FETCH/CLOSE, set fail codes 2/3/4 respectively, issue SYNCPOINT ROLLBACK, and return failure.
10. On rollback failure, populate ABNDINFO and ABEND with code HROL.

## Legacy Behavioral Rules Captured
- BR-001: Customer must be valid and found via INQCUST before account retrieval.
- BR-002: CUSTOMER-NUMBER values 0000000000 and 9999999999 are rejected.
- BR-003: Max 20 accounts returned even if more exist.
- BR-004: SQLCODE +100 is treated as normal completion (not failure).
- BR-005: COMM-FAIL-CODE mapping is deterministic: 1 customer check failure, 2 cursor open failure, 3 fetch failure, 4 cursor close failure.
- BR-006: DB2 dates are reformatted from YYYY-MM-DD to DDMMYYYY in output fields.
- BR-007: Sort code filter is fixed from copybook constant SORTCODE=987654.

## Risks and Unknowns
- RISK-001: COMM-SUCCESS='Y' may coexist with zero accounts when no DB2 rows are found; clients must not assume non-empty list.
- RISK-002: Potential data truncation/format expectations if modern API changes numeric field formats.
- RISK-003: Storm drain handling is operationally significant; modern system should preserve failure semantics even if exact CICS ABEND behavior differs.
- RISK-004: COMM-PCB-POINTER is present but not used by modern REST mapping.

## Modernization Implications
- Preserve observable success/failure semantics and fail-code behavior.
- Keep controller thin and encapsulate customer validation and account retrieval in service layer.
- Use repository interface for legacy adapter strategy and mock implementation in POC mode.
- Expose deterministic REST response consistent with existing response_200 mapping (accounts, totalCount, GBP currency, ACTIVE status template).
