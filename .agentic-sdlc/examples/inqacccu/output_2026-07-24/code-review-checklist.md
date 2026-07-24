# Code Review Checklist: INQACCCU

## Metadata
- Artifact ID: CR-INQACCCU-20260724
- Agent Role: CodeReviewAgent

## Correctness
- [ ] Input validation enforces 10-digit numeric customerId
- [ ] Sentinel inputs map to not-found semantic result
- [ ] Customer existence check precedes account query
- [ ] Account query uses customerId + sortCode 987654
- [ ] Response list capped at 20

## Compatibility
- [ ] Legacy-equivalent fail-code mapping (1,2,3,4) is deterministic
- [ ] No-row scenario returns successful empty result
- [ ] Mapping preserves required fields from copybook data

## Maintainability
- [ ] Controller/service/repository layering respected
- [ ] Business rules encapsulated in service methods
- [ ] Clear naming and test IDs aligned to FR/TC

## Security
- [ ] AuthZ checks enforced at endpoint
- [ ] No plaintext secrets or credentials
- [ ] Error handling avoids stack trace exposure

## Testing
- [ ] Unit tests for all rules and acceptance criteria
- [ ] Contract tests for OpenAPI response shapes
- [ ] Regression tests for sentinel and fail-stage behavior
