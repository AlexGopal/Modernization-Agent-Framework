# Copilot Custom Agents (Workspace)

This repo now includes workspace custom agents under `.github/agents/`.

## Available Agents

- `SpecKit Orchestrator`
- `Legacy Analysis Specialist`
- `Business Rules Specialist`
- `Requirements and Spec Specialist`
- `Contract and Mapping Specialist`
- `Plan and Tasks Specialist`
- `Test and Review Specialist`
- `Quality Gates Specialist`
- `Spec Implementation Specialist` (manual)
- `Secure Code Review Specialist` (manual)
- `Test Automation Specialist` (manual)

## How to Use in VS Code Copilot

1. Open Copilot Chat.
2. Switch to Agent mode.
3. Pick `SpecKit Orchestrator` from the agent picker.
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
Use SpecKit Orchestrator for this feature slice.
1) Implement code from spec.md, tasks.md, test-spec.md, and openapi.yaml.
2) Run secure code review for bad practices and vulnerabilities and generate a report.
3) Create manual tests plus API and UI automation tests (Playwright) from the same artifacts.
4) Run quality gates and return traceability and risk summary.
```

Manual checkpoint flow (separate calls):

1. Run `Spec Implementation Specialist` for requested TASK scope.
2. Manually verify code changes.
3. Run `Secure Code Review Specialist` for bad practices and vulnerabilities.
4. Manually verify and resolve findings.
5. Run `Test Automation Specialist` to create manual, API, and Playwright UI tests.
6. Manually verify generated test assets before running quality gates.

## Quality Gate Commands

Use these in `Quality Gates Specialist` when needed:

- `python -m pytest -q tests`
- `python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output --bundle-specs .agentic-sdlc/spec-kit-bundles/current/specs`

## Notes

- Most specialist agents are `user-invocable: false` and designed for orchestrated delegation.
- `Spec Implementation Specialist`, `Secure Code Review Specialist`, and `Test Automation Specialist` are picker-visible for manual gated execution.
- After pulling new agent definitions, run VS Code `Developer: Reload Window` if the picker does not update immediately.
- Dual-model compare and merge is delegated internally through `Dual Model Merge Specialist` when you request double-check mode.
- You can still request orchestrated execution, but manual step-by-step invocation is recommended when you need checkpoint approvals.
