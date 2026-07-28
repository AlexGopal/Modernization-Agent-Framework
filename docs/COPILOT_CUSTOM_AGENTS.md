# Copilot Custom Agents (Workspace)

This repo now includes workspace custom agents under `.github/agents/`.

## Available Agents

- `Mainframe modernization agent`
- `Legacy Analysis Specialist`
- `Business Rules Specialist`
- `Requirements and Spec Specialist`
- `Contract and Mapping Specialist`
- `Plan and Tasks Specialist`
- `Spec Implementation Specialist` (delegated)
- `Secure Code Review Specialist` (delegated)
- `Test Automation Specialist` (delegated)
- `Test and Review Specialist`
- `Quality Gates Specialist`
- `Dual Model Merge Specialist`

## Visibility Model

- Picker-visible: `Mainframe modernization agent`
- Delegated/internal: all specialists listed above

Specialists are configured as `user-invocable: false`, so they are run by orchestration, not direct picker selection.

## Agent Responsibilities (Quick Map)

- `Mainframe modernization agent`: phased orchestration and final summary
- `Legacy Analysis Specialist`: legacy behavior and dependency evidence
- `Business Rules Specialist`: BR extraction, IDs, traceable evidence
- `Requirements and Spec Specialist`: FR/NFR/AC artifacts
- `Contract and Mapping Specialist`: OpenAPI plus mapping and traceability matrices
- `Plan and Tasks Specialist`: implementation plan and task decomposition
- `Spec Implementation Specialist`: scoped code implementation from artifacts
- `Secure Code Review Specialist`: vulnerability and bad-practice findings
- `Test and Review Specialist`: test spec plus QA/code-review checklists
- `Test Automation Specialist`: manual tests + API automation + Playwright UI automation
- `Quality Gates Specialist`: tests, drift/alignment checks, readiness verdict
- `Dual Model Merge Specialist`: two-model compare/merge and reconciliation report

## How to Use in VS Code Copilot

1. Open Copilot Chat.
2. Switch to Agent mode.
3. Pick `Mainframe modernization agent` from the agent picker.
4. Give one input prompt with scope, for example:

```text
Generate modernization artifacts for INQACC account inquiry.
Use legacy assets from .agentic-sdlc/examples/inqacc/legacy.
Write outputs to .agentic-sdlc/examples/inqacc/output.
Run quality gates and return readiness summary.
```

The orchestrator delegates internally to specialist agents.

For double-check mode, ask the orchestrator to run dual-model verification so outputs are compared and merged.

Example request:

```text
Generate modernization artifacts for INQACC account inquiry.
Then run dual-model verification using primary model plus Claude,
compare outputs, merge final artifacts, and summarize differences from dual-model-analysis.md.
```

Full delivery request example:

```text
Use Mainframe modernization agent for this feature slice.
1) Implement code from spec.md, tasks.md, test-spec.md, and openapi.yaml.
2) Run secure code review for bad practices and vulnerabilities and generate a report.
3) Create manual tests plus API and UI automation tests (Playwright) from the same artifacts.
4) Run quality gates and return traceability and risk summary.
```

Manual checkpoint flow (single orchestrator call with gated phases):

1. Run `Mainframe modernization agent` with explicit phase gates.
2. Ask it to stop after implementation summary for manual verification.
3. Continue with secure review phase only after approval.
4. Continue with test automation phase only after approval.
5. Run quality gates after final manual sign-off.

## Recommended Usage Patterns

Implementation slice:

```text
Implement TASK-001 to TASK-003 only.
Use spec.md, tasks.md, test-spec.md, and openapi.yaml as authority.
Return task IDs implemented, files changed, tests updated, blockers.
```

Security checkpoint:

```text
Run secure review for the in-scope changes and report findings by severity
with impacted files, evidence, and remediations.
```

Test automation checkpoint:

```text
Generate manual test cases plus API automation and Playwright UI automation
for the in-scope feature slice and return BR/FR/AC/TASK coverage gaps.
```

Quality gate checkpoint:

```text
Run quality gates now and return command log, pass/fail by gate,
top issues, and release-readiness verdict.
```

## Quality Gate Commands

Use these in `Quality Gates Specialist` when needed:

- `python -m pytest -q tests`
- `python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output --bundle-specs .agentic-sdlc/spec-kit-bundles/current/specs`

## Notes

- Most specialist agents are `user-invocable: false` and designed for orchestrated delegation.
- `Mainframe modernization agent` is the only picker-visible entry point.
- After pulling new agent definitions, run VS Code `Developer: Reload Window` if the picker does not update immediately.
- Dual-model compare and merge is delegated internally through `Dual Model Merge Specialist` when you request double-check mode.
- Use phase-gated orchestrator prompts when you need manual checkpoint approvals.
