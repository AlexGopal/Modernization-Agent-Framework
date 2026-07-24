# Copilot Agents README

This document is the single entry point for Copilot custom agents and workflow in this repository.

## Scope

Use this guide to:
- Understand which agents are available and how they are intended to be used.
- Run implementation, secure review, and test automation in an orchestrator-gated sequence.
- Run optional dual-model verification and merge for higher confidence.

## Source Documents

Detailed references:
- `docs/COPILOT_CUSTOM_AGENTS.md`
- `docs/COPILOT_AGENT_WORKFLOW.md`

## Agent Visibility Model

Picker-visible:
- Mainframe modernization agent

Delegated/internal (not picker-visible):
- Legacy Analysis Specialist
- Business Rules Specialist
- Requirements and Spec Specialist
- Contract and Mapping Specialist
- Plan and Tasks Specialist
- Test and Review Specialist
- Quality Gates Specialist
- Dual Model Merge Specialist

## Authoritative Inputs

Attach these artifacts before implementation or test generation:
- `.agentic-sdlc/examples/inqacc/output/spec.md`
- `.agentic-sdlc/examples/inqacc/output/tasks.md`
- `.agentic-sdlc/examples/inqacc/output/test-spec.md`
- `.agentic-sdlc/examples/inqacc/output/openapi.yaml`

## Recommended Orchestrator-Gated Workflow

1. Run Mainframe modernization agent for a small task slice.
2. Ask it to pause after implementation summary for manual verification.
3. Resume only secure review phase and review findings manually.
4. Resume only test automation phase and review generated assets manually.
5. Run quality gates and summarize residual risks.

## Prompt Templates

Implementation:

```text
Implement <TASK_SCOPE> only using spec.md, tasks.md, test-spec.md, and openapi.yaml.
Return implemented task IDs, files changed, tests added/updated, and blockers.
```

Secure review:

```text
Review the in-scope implementation for bad practices and vulnerabilities.
Return findings by severity with impacted files, evidence, and remediations.
```

Test automation:

```text
Create manual test cases plus API automation and Playwright UI automation from spec.md, tasks.md, test-spec.md, and openapi.yaml.
Return BR/FR/AC/TASK coverage mapping and remaining gaps.
```

Dual-model double-check (optional):

```text
Run dual-model verification using primary model plus Claude, compare outputs, merge final artifacts, and summarize differences from dual-model-analysis.md.
```

## Operational Notes

- After pulling new agent definitions, run `Developer: Reload Window` in VS Code if agents do not appear.
- Keep changes scoped to requested TASK IDs.
- Preserve legacy behavior unless explicitly marked as modernization enhancement.
- Do not invent fields or endpoints not present in artifacts.
