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

## Reporting Contract

All custom agents now include two mandatory report elements in their output format:
- Guardrails enforced: checks performed, pass/fail status, and any blocking guardrail.
- Confidence score: 0 to 100, plus one-line rationale grounded in evidence.

For orchestrated runs, `Mainframe modernization agent` must return an agent confidence scorecard summarizing confidence per delegated specialist.

## Confidence Rubric (v1)

Use the same weighted rubric for every agent so confidence is comparable across phases:

| Dimension | Weight | Scoring intent |
|---|---:|---|
| Evidence fidelity | 35% | Are claims backed by artifacts, code, and command output? |
| Traceability completeness | 25% | Are BR/FR/AC/TASK/TC/API links present and consistent? |
| Validation signal | 25% | Did relevant tests/checks pass with deterministic evidence? |
| Risk clarity | 15% | Are assumptions, blockers, and residual risks explicit? |

Formula:
- `confidence = round(0.35*evidence + 0.25*traceability + 0.25*validation + 0.15*risk)`

Guardrail rule:
- If any blocking guardrail fails, cap confidence at `49`.

Recommended score bands:
- `90-100`: High confidence, no blocking guardrails, strong validation signal.
- `70-89`: Good confidence, minor non-blocking gaps or warnings.
- `50-69`: Moderate confidence, meaningful validation or traceability gaps.
- `0-49`: Low confidence, blocking guardrail failed or evidence is insufficient.

## Sample Orchestrator Output

Use this shape for `Mainframe modernization agent` final summaries:

```text
Phase summary and delegated agents used:
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

Guardrails enforced:
- No invented fields: PASS
- Dependency order preserved: PASS
- Scope bounded to requested TASK IDs: PASS
- Traceability chain complete (BR->FR->AC->TASK->TC->API): PASS
- Blocking review findings (critical/high): NONE
- Release readiness gate: PASS

Agent confidence scorecard:
- Legacy Analysis Specialist: 92
	- Evidence fidelity: 95
	- Traceability completeness: 90
	- Validation signal: 90
	- Risk clarity: 92
	- Guardrail cap applied: no
- Business Rules Specialist: 89
	- Evidence fidelity: 91
	- Traceability completeness: 88
	- Validation signal: 87
	- Risk clarity: 90
	- Guardrail cap applied: no
- Requirements and Spec Specialist: 86
	- Evidence fidelity: 88
	- Traceability completeness: 86
	- Validation signal: 84
	- Risk clarity: 88
	- Guardrail cap applied: no
- Quality Gates Specialist: 93
	- Evidence fidelity: 94
	- Traceability completeness: 92
	- Validation signal: 95
	- Risk clarity: 90
	- Guardrail cap applied: no

Remaining assumptions requiring SME validation:
- ASSUMP-004: confirm final error-code taxonomy for downstream channel integrations.
```

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
