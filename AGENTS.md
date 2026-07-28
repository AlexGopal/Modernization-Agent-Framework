# Agent Catalog

## Purpose

Defines each framework (Python pipeline) agent role and when to use it.

This file documents agents implemented under `.agentic-sdlc/agents/`.
Copilot custom agents are documented separately in `docs/COPILOT_AGENTS_README.md`.

## Agents

1. LegacyAnalysisAgent
- Use when onboarding COBOL/copybook assets.
- Produces program-analysis.md.

2. BusinessRulesAgent
- Use after legacy analysis.
- Produces business-rules.md.

3. SystemIntentAgent
- Use after business rules to capture intended target architecture and constraints.
- Produces intended-system.md.

4. RequirementsAgent
- Use after business rules are drafted.
- Produces requirements.md.

5. SpecAgent
- Use when requirements are stable enough for design.
- Produces spec.md.

6. PlanAgent
- Use to define phased delivery path.
- Produces plan.md.

7. TaskAgent
- Use to create engineering backlog slices.
- Produces tasks.md.

8. MappingMatrixAgent
- Use to map legacy elements and maintain traceability.
- Produces mapping-matrix.md and traceability-matrix.md.

9. TestSpecAgent
- Use to define test strategy from rules and spec.
- Produces test-spec.md.

10. OpenApiAgent
- Use to create API contract starter.
- Produces openapi.yaml.

11. CopilotPromptAgent
- Use to generate Copilot implementation prompts.
- Produces copilot-build-prompt.md.

12. QAReviewAgent
- Use before and after implementation iterations.
- Produces qa-review-checklist.md.

13. CodeReviewAgent
- Use during PR review and architecture checks.
- Produces code-review-checklist.md.

14. ReportAgent
- Use at iteration close or milestone review.
- Produces modernization-report.md.

## Copilot Custom Agents

Copilot custom agents are workspace chat agents in `.github/agents/` and are not Python pipeline agents.

- Picker-visible entrypoint: Mainframe modernization agent
- Delegated specialists: Legacy Analysis Specialist, Business Rules Specialist, Requirements and Spec Specialist, Contract and Mapping Specialist, Plan and Tasks Specialist, Spec Implementation Specialist, Secure Code Review Specialist, Test and Review Specialist, Test Automation Specialist, Quality Gates Specialist, Dual Model Merge Specialist

See:
- docs/COPILOT_AGENTS_README.md
- docs/COPILOT_CUSTOM_AGENTS.md
