# Specification: INQACCCU Account Inquiry Service

## Metadata
- Artifact ID: SPEC-INQACCCU-20260724
- Agent Role: SpecAgent
- Inputs: requirements.md, business-rules.md, legacy mappings

## 1. API Behavior
- Endpoint: GET /customers/{customerId}/accounts
- Path parameter:
- customerId: string, exactly 10 numeric digits
- Success response (200):
- accounts: array
- totalCount: integer

## 2. Domain Model

### 2.1 AccountSummary
- accountId: string (from COMM-ACCNO)
- accountType: string (from COMM-ACC-TYPE)
- currency: string constant GBP
- accountNumber: string (from COMM-ACCNO)
- sortCode: string (from COMM-SCODE)
- status: string constant ACTIVE

### 2.2 Internal LegacyResult (service boundary)
- successFlag: Y/N equivalent
- failCode: 0/1/2/3/4 equivalent
- customerFound: Y/N equivalent
- numberOfAccounts: integer 0..20
- accountDetails: list of up to 20 records

## 3. Service Workflow
1. Validate customerId format and sentinel values.
2. Execute customer lookup through customer repository contract.
3. If customer missing, return not-found semantic outcome.
4. Execute account query through account repository contract with filters:
- customerNumber=customerId
- sortCode=987654
5. Limit result to max 20 records.
6. Map output model and defaults (GBP, ACTIVE).
7. Return 200 with accounts and totalCount for successful logical completion (including zero rows).

## 4. Error Model
- E-001 (legacy equivalent failCode 1): Customer invalid/not found.
- E-002 (legacy equivalent failCode 2): Data-open stage failure.
- E-003 (legacy equivalent failCode 3): Data-read stage failure.
- E-004 (legacy equivalent failCode 4): Data-close stage failure.

## 5. Legacy Compatibility Rules
- C-001: Preserve no-row success behavior.
- C-002: Preserve max 20 account cap.
- C-003: Preserve field-level mapping names and value semantics.
- C-004: Preserve date conversion semantics (DDMMYYYY representation).

## 6. Component Responsibilities
- Controller:
- Parse/validate path param
- Delegate to service
- Return HTTP response model
- Service:
- Business rule orchestration and failure mapping
- Repository interface calls
- Output shaping
- Repository interfaces:
- CustomerRepository.exists(customerId)
- AccountRepository.findByCustomerAndSortCode(customerId, sortCode, limit)

## 7. Testability Hooks
- Repository interfaces are mockable.
- Service returns explicit error codes for deterministic tests.
- Contract tests validate OpenAPI schema for 200/4xx/5xx.
