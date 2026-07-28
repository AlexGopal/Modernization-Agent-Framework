# Copilot Agents README

This document is the single entry point for Copilot custom agents and usage in this repository.

## What Changed

This guide now reflects the full current custom-agent set under `.github/agents/`, including:
- implementation delegation
- secure review delegation
- test automation delegation
- quality-gate delegation
- dual-model compare and merge delegation

## Agent Inventory

### Picker-visible entry point

- Mainframe modernization agent

### Delegated specialists (not picker-visible)

- Legacy Analysis Specialist
- Business Rules Specialist
- Requirements and Spec Specialist
- Contract and Mapping Specialist
- Plan and Tasks Specialist
- Spec Implementation Specialist
- Secure Code Review Specialist
- Test and Review Specialist
- Test Automation Specialist
- Quality Gates Specialist
- Dual Model Merge Specialist

## What Each Agent Is For

- Mainframe modernization agent: orchestrates phased work and delegates specialists in dependency order.
- Legacy Analysis Specialist: extracts evidence-first legacy behavior and dependencies.
- Business Rules Specialist: builds BR catalog with evidence and risk context.
- Requirements and Spec Specialist: produces FR/NFR/AC artifacts with stable IDs.
- Contract and Mapping Specialist: aligns OpenAPI and mapping/traceability artifacts.
- Plan and Tasks Specialist: produces implementation plan and scoped task backlog.
- Spec Implementation Specialist: implements requested task scope from approved artifacts.
- Secure Code Review Specialist: reports bad practices and vulnerabilities with severity.
- Test and Review Specialist: builds test spec and review checklists with coverage intent.
- Test Automation Specialist: creates manual tests plus API and Playwright automation.
- Quality Gates Specialist: runs tests, review, drift checks, and readiness verdict.
- Dual Model Merge Specialist: runs compare/merge pass and summarizes reconciliation evidence.

## How To Use In VS Code

1. Open Copilot Chat and switch to Agent mode.
2. Select Mainframe modernization agent from the picker.
3. Attach authoritative artifacts:
	- `.agentic-sdlc/examples/inqacc/output/spec.md`
	- `.agentic-sdlc/examples/inqacc/output/tasks.md`
	- `.agentic-sdlc/examples/inqacc/output/test-spec.md`
	- `.agentic-sdlc/examples/inqacc/output/openapi.yaml`
4. Request only the scope you want (for example TASK-001 to TASK-003).
5. Ask for gated phases when needed: implementation -> secure review -> test automation -> quality gates.
6. Optionally request dual-model verification at the end.

## Recommended Prompt Patterns

Implementation only:

```text
Implement TASK-001 to TASK-003 only using spec.md, tasks.md, test-spec.md, and openapi.yaml.
Return implemented task IDs, files changed, tests added or updated, and blockers.
```

Implementation + secure review + test automation + gates:

```text
Implement <TASK_SCOPE> only from spec.md, tasks.md, test-spec.md, and openapi.yaml.
Then run secure code review and return findings by severity with evidence.
Then create manual tests plus API and Playwright UI automation tests.
Then run quality gates and return pass or fail plus residual risks.
```

Dual-model verification:

```text
Run dual-model verification using primary model plus Claude,
compare outputs, merge final artifacts, and summarize differences from dual-model-analysis.md.
```

## Visibility And Invocation Rules

- Only Mainframe modernization agent is user-invocable in the picker.
- All specialists are orchestrator-delegated and intentionally hidden from picker selection.
- If new agent files are pulled and the picker does not update, run Developer: Reload Window.

## Relationship To Framework Agents

Copilot custom agents orchestrate workflow in chat. The Python framework agents produce pipeline artifacts.
For the Python framework catalog, see AGENTS.md.

## Related Docs

- docs/COPILOT_CUSTOM_AGENTS.md
- docs/COPILOT_AGENT_WORKFLOW.md
- AGENTS.md
