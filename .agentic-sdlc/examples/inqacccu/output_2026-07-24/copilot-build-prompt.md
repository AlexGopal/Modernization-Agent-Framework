# Copilot Build Prompt: INQACCCU

Implement INQACCCU modernization using these authoritative artifacts:
- spec.md
- tasks.md
- test-spec.md
- openapi.yaml
- mapping-matrix.md
- traceability-matrix.md

## Rules
- Do not invent fields not present in copybooks/specs.
- Preserve legacy behavior unless enhancement is explicitly flagged.
- Keep controllers thin and business logic in services.
- Use repository interfaces for legacy adapters.
- Do not connect to real mainframe systems in POC mode.

## Required Task Scope
- Implement TASK-001 through TASK-008 in task order.
- Add tests for each acceptance criterion.
- Maintain traceability IDs in code comments or test names.

## Technical Expectations
- Input validation for 10-digit customerId.
- Sentinel rejection for 0000000000 and 9999999999.
- Static sort code filter 987654.
- Max 20 account outputs.
- Preserve semantic fail mapping equivalent to legacy fail codes 1/2/3/4.
- Contract compatibility with openapi.yaml.

## Completion Output
Provide:
1. Implemented task IDs
2. Files changed
3. Tests added/updated
4. Remaining tasks not implemented
