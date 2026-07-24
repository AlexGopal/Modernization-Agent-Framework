# QA Review Checklist: INQACCCU

## Metadata
- Artifact ID: QA-INQACCCU-20260724
- Agent Role: QAReviewAgent

## Functional Parity Checks
- [ ] BR-001 customer existence gate preserved
- [ ] BR-002 sentinel values rejected
- [ ] BR-003 fail-code semantics preserved
- [ ] BR-004 no-row success preserved
- [ ] BR-005 max 20 result cap preserved
- [ ] BR-006 static sort code filter preserved
- [ ] BR-007 date conversion semantics preserved
- [ ] BR-008 GBP/ACTIVE projection preserved

## Architecture and Design Checks
- [ ] Controller has no business logic
- [ ] Service layer contains orchestration logic
- [ ] Repository interfaces isolate legacy access
- [ ] POC mode avoids real mainframe connectivity

## API and Contract Checks
- [ ] Endpoint matches GET /customers/{customerId}/accounts
- [ ] Response schema matches openapi.yaml
- [ ] Error schema consistent for 4xx/5xx

## Test Coverage Checks
- [ ] TC-001..TC-012 implemented
- [ ] Edge cases covered (sentinel ids, zero rows, >20 rows)
- [ ] Failure stage mapping tests cover open/read/close

## Operational Checks
- [ ] Structured logs with correlation id
- [ ] No hardcoded secrets
- [ ] Error messages do not leak sensitive internals
