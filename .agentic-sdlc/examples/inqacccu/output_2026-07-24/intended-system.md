# Intended System: INQACCCU Modernized Service

## Metadata
- Artifact ID: IS-INQACCCU-20260724
- Agent Role: SystemIntentAgent

## Product Goal
Expose INQACCCU account inquiry as a modern REST capability while preserving legacy observable behavior and error semantics.

## Target Architecture
- Backend: Java 21 + Spring Boot 3.x
- API Contract: OpenAPI 3.0.3
- Layering:
- Controller (transport, validation only)
- Service (business rules and orchestration)
- Repository interface (legacy adapter boundary)
- Adapter implementation:
- POC: in-memory/mock implementation
- Future: CICS/DB2-backed adapter (out of current scope)

## Functional Scope
- Endpoint equivalent: GET /customers/{customerId}/accounts
- Input: customerId path parameter (10-digit customer number)
- Output: accounts array and totalCount
- Preserve max result size of 20

## Non-Functional Constraints
- Preserve fail-code semantics from legacy.
- No direct mainframe connectivity in POC mode.
- Structured logs with correlation id.
- Standardized error responses for 4xx/5xx.

## Security Baseline
- JWT bearer auth at API gateway or service boundary.
- Role check for account inquiry endpoint.
- Input validation and safe error handling.

## Legacy-Compatibility Commitments
- Keep customer validation gate before account retrieval.
- Keep sentinel input behavior (0000000000, 9999999999).
- Keep no-row success behavior.
- Keep deterministic fail mappings.

## Out of Scope for This Slice
- Real-time CICS transaction invocation.
- Production DB2 bind/runtime setup.
- UI rework beyond contract compatibility.
