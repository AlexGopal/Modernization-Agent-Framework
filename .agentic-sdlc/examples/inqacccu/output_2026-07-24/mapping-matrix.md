# Mapping Matrix: Legacy to Modern Components

## Metadata
- Artifact ID: MAP-INQACCCU-20260724
- Agent Role: MappingMatrixAgent

## Component Mapping
| Legacy Asset | Legacy Element | Modern Component | Notes |
|---|---|---|---|
| INQACCCU.cbl | PREMIERE, CUSTOMER-CHECK, READ-ACCOUNT-DB2, FETCH-DATA | AccountInquiryService | Business flow orchestration |
| INQACCCU.cpy | CUSTOMER-NUMBER input | AccountInquiryController | GET path param customerId |
| INQACCCU.cpy | ACCOUNT-DETAILS OCCURS 1..20 | AccountSummary DTO list | Max 20 preserved |
| INQCUSTZ.cpy | INQCUST-INQ-SUCCESS | CustomerRepository.exists() | Customer validation gate |
| ACCDB2.cpy | ACCOUNT table columns | AccountRepository model | Source data fields |
| SORTCODE.cpy | SORTCODE=987654 | Service constant/config | Static filter |
| ABNDINFO.cpy | ABEND diagnostics | Error/log telemetry model | Operational diagnostics only |
| supporting/api/response_200.yaml | body.accounts, totalCount | OpenAPI response schema | Contract alignment |

## Field-Level Mapping
| Legacy Field | Modern Field | Rule |
|---|---|---|
| COMM-ACCNO | accountId | Direct string map |
| COMM-ACCNO | accountNumber | Direct string map |
| COMM-ACC-TYPE | accountType | Direct string map |
| COMM-SCODE | sortCode | Direct string map |
| N/A | currency | Constant GBP |
| N/A | status | Constant ACTIVE |
| ACCOUNT-DETAILS count | totalCount | size(accounts) |

## Failure Mapping
| Legacy Signal | Modern Semantic Error |
|---|---|
| COMM-FAIL-CODE 1 | customerNotFound |
| COMM-FAIL-CODE 2 | dataOpenFailure |
| COMM-FAIL-CODE 3 | dataReadFailure |
| COMM-FAIL-CODE 4 | dataCloseFailure |
