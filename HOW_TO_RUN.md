# How to Run

## 0. Execution Modes

- Deterministic mode: no LLM calls, fastest for scaffolding.
- Single-model AI mode: one provider run into output.
- Dual-model mode: primary + Claude compare and merge.
- Demo dual-model mode: non-AI run that still executes primary, claude, and merge phases.

## 1. Environment Files (Push-Safe)

```powershell
# Keep key values empty in .env before commit/push
# Put actual keys only in .env.local
```

Use this precedence order:

1. Process environment variables (highest)
2. `.env.local` (local secrets, git-ignored)
3. `.env` (committed defaults, no secrets)

Rules:

- Keep `AGENTIC_AI_API_KEY=` blank in `.env` before commit/push.
- Keep `AGENTIC_CLAUDE_API_KEY=` blank in `.env` before commit/push.
- Put real keys only in `.env.local`.

Suggested `.env.local` content:

```dotenv
AGENTIC_AI_API_KEY=<YOUR_OPENAI_KEY>
AGENTIC_CLAUDE_API_KEY=<YOUR_CLAUDE_KEY>
```

## 2. Prerequisites

- Python 3.11+
- Node.js 18+ (for React dashboard)
- VS Code with GitHub Copilot

## 3. Install Dependencies

Optional if using run.py auto-install:

```powershell
python -m pip install -r requirements.txt
```

For dashboard UI:

```powershell
cd agent-visual-ui
npm install
```

## 4. Prepare Input Files

- .agentic-sdlc/examples/inqacc/legacy/cobol
- .agentic-sdlc/examples/inqacc/legacy/copybooks

## 5. Deterministic Run (No AI)

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --dry-run
```

## 6. Single-Model AI Run (OpenAI-Compatible)

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --ai-provider openai --ai-model gpt-4o-mini --ai-base-url https://api.openai.com --ai-api-key <YOUR_KEY>
```

Optional system intent input:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --system-intent .agentic-sdlc/examples/inqacc/legacy/system-intent.md --use-ai --ai-provider openai --ai-model gpt-4o-mini --ai-base-url https://api.openai.com --ai-api-key <YOUR_KEY>
```

## 7. Dual-Model Verification (OpenAI + Claude)

Verify Claude first:

```powershell
python test_claude_api.py
```

Run dual-model compare + merge:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --system-intent .agentic-sdlc/examples/inqacc/legacy/system-intent.md --use-ai --ai-provider openai --ai-model gpt-4o-mini --ai-base-url https://api.openai.com --ai-api-key <PRIMARY_KEY> --compare-with-claude --claude-model claude-haiku-4-5-20251001 --claude-api-key <CLAUDE_KEY>
```

Requirements for dual-model mode:

- `AGENTIC_AI_API_KEY` must be set (primary OpenAI-compatible run).
- `AGENTIC_CLAUDE_API_KEY` must be set (secondary Claude run).
- If either key is missing, the run fails fast with an explicit error.

Generated folders/files in dual mode:

- .agentic-sdlc/examples/inqacc/output_primary
- .agentic-sdlc/examples/inqacc/output_claude
- .agentic-sdlc/examples/inqacc/output
- .agentic-sdlc/examples/inqacc/output/dual-model-analysis.md

Parallel execution option:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --compare-with-claude --parallel-dual-run
```

Sequential fallback:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --compare-with-claude --no-parallel-dual-run
```

Token optimization options:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --optimize-tokens --token-max-sources 12 --token-preview-chars 1400
```

Enable strict Spec Kit alignment gate:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --align-to-speckit --speckit-baseline .agentic-sdlc/spec-kit-bundles/current/specs --require-baseline-alignment --baseline-alignment-threshold 0.78
```

Auto-tune token settings (single-model AI mode):

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --auto-tune-tokens
```

Optional quality threshold override:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --auto-tune-tokens --auto-tune-quality-threshold 0.95
```

Auto-tune outputs:

- Candidate folders: `<output>_autotune_*`
- Selected best artifacts copied into configured output folder
- Report: `token-optimization-report.md`

Auto-tune constraints:

- Requires `--use-ai`
- Single-model mode only (do not combine with `--compare-with-claude`)
- Cannot be combined with `--dry-run` or `--demo-mode`

Add output token caps:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --optimize-tokens --token-max-sources 10 --token-preview-chars 1000 --ai-max-output-tokens 1600
```

Dual-run with explicit Claude cap:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --use-ai --compare-with-claude --parallel-dual-run --ai-max-output-tokens 1800 --claude-max-output-tokens 1200
```

Output cap precedence:

- Primary provider: `--ai-max-output-tokens` -> `AGENTIC_AI_MAX_OUTPUT_TOKENS`
- Claude in dual mode: `--claude-max-output-tokens` -> `AGENTIC_CLAUDE_MAX_OUTPUT_TOKENS` -> `AGENTIC_AI_MAX_OUTPUT_TOKENS`

Token cost model:

- Estimated cost = `(prompt_tokens / 1000 * prompt_rate) + (completion_tokens / 1000 * completion_rate)`
- Completion tokens are typically the largest variable cost and should be tuned first.

Suggested optimization workflow:

1. Start with balanced settings: max sources 8-10, preview chars 900-1200, output cap 1400-1800.
2. Run a representative sample input set and capture token usage.
3. Reduce output cap first in 200-token steps until quality drops.
4. Reduce preview chars next in 100-200 char steps.
5. Reduce max sources last in 1-2 source steps.
6. Promote dual-run to checkpoint validation only.
7. Keep the best settings as your project baseline.

## 8. Demo Mode (Non-AI, Full Dual Flow)

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output --demo-mode --parallel-dual-run
```

Demo mode behavior:

- No API keys required.
- Runs primary and claude phases in dry-run mode.
- Executes merge phase and writes final output.
- Emits full phase events for realistic dashboard visualization.

## 9. Run with Visual Dashboard (API + React)

Fastest start (Windows PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-dashboard.ps1
```

Optional custom ports:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-dashboard.ps1 -ApiPort 8010 -UiPort 5175
```

Manual start:

Start backend API:

```powershell
python -m uvicorn agent_visual_api:app --reload --port 8000
```

Start React UI:

```powershell
cd agent-visual-ui
npm run dev
```

Open `http://localhost:5173`.

UI run behavior:

- `Use OpenAI = off` runs deterministic mode without keys.
- `Use OpenAI = on` requires `AGENTIC_AI_API_KEY`.
- `Use Claude = on` also requires `AGENTIC_CLAUDE_API_KEY`.
- `Demo Mode = on` runs full non-AI primary/claude/merge flow.
- `Run OpenAI + Claude in Parallel` controls dual-run concurrency.
- `Optimize Token Usage` enables compact prompt context.
- In dual mode, the execution map shows OpenAI/Claude flows converging to `Merge + Compare`, then `Final Output`.
- Run controls display resolved model names for OpenAI and Claude.
- Header shows elapsed run timer.
- Theme toggle switches between Classic and Neon UI.

## 10. Expected Artifacts

- program-analysis.md
- business-rules.md
- intended-system.md
- requirements.md
- spec.md
- plan.md
- tasks.md
- mapping-matrix.md
- traceability-matrix.md
- test-spec.md
- openapi.yaml
- copilot-build-prompt.md
- qa-review-checklist.md
- code-review-checklist.md
- modernization-report.md
- dual-model-analysis.md (dual mode)

## 11. Tests

```powershell
python -m pytest -q tests
```

## 11.1 Unified Quality Gates (CI-Parity Local Check)

Run this as the primary local readiness check:

```powershell
python scripts/run_quality_gates.py --repo-root .
```

Gate stages:

1. `tests`
2. `agent-reporting-contract`
3. `bundle-preflight`
4. `detail-drift`

Bundle preflight behavior:

- If `.agentic-sdlc/spec-kit-bundles/current/specs` is missing, the gate runner auto-builds the baseline with `scripts/build_spec_bundle.py`.

Detail drift behavior:

- Runs structural and semantic checks.
- Runs cross-artifact consistency checks across BR/FR/AC/TASK references.
- Writes report to `<generated-output>/detail-drift-report.md`.
- Dry-run OpenAPI marker mismatches are warning-class findings (non-blocking for deterministic scaffold output).

## 12. Validate Detail Drift Against Spec Kit Baseline

Use this after implementation to catch artifacts that are too thin or too verbose compared to your Spec Kit source of truth.

Imported Spec Kit baseline:

```powershell
python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output --bundle-specs <SPEC_KIT_IMPORT_PATH>/specs
```

Local bundle baseline:

```powershell
python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output --bundle-specs .agentic-sdlc/spec-kit-bundles/current/specs
```

The command writes `detail-drift-report.md` in the generated output folder and exits non-zero on failure.

## 12.1 Validate AI Artifacts (Optional CI Lane Reproduction)

Use this to reproduce the optional GitHub Actions AI artifact validation lane locally.

Generate AI artifacts:

```powershell
python run_pipeline.py --pipeline mainframe_modernization --input .agentic-sdlc/examples/inqacc/legacy --output .agentic-sdlc/examples/inqacc/output_ai_ci --use-ai --ai-provider openai --ai-model gpt-4o-mini --ai-base-url https://api.openai.com
```

Validate generated AI artifacts with CI-aligned relaxed thresholds:

```powershell
python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output_ai_ci --bundle-specs .agentic-sdlc/spec-kit-bundles/current/specs --min-char-ratio 0.20 --max-char-ratio 5.00 --min-heading-ratio 0.20 --max-heading-ratio 5.00 --min-id-ratio 0.20 --max-id-ratio 5.00
```

Expected CI gate condition:

- GitHub Actions runs this lane only when `AGENTIC_AI_API_KEY` is configured as a repository secret.

## 13. Fast Troubleshooting

- Error: `AGENTIC_AI_API_KEY is required for provider=openai`
	- Cause: AI mode enabled without primary key.
	- Fix: Set key in `.env.local` or pass `--ai-api-key`.

- Error: `Claude API key is required for dual-model mode`
	- Cause: compare mode enabled without Claude key.
	- Fix: Set `AGENTIC_CLAUDE_API_KEY` in `.env.local`.

- If deterministic mode is enough for demo:
	- Set `Use AI = off` in UI or use `--dry-run` in CLI.

- If dual mode is too slow:
	- Keep `--parallel-dual-run` enabled.
	- Enable `--optimize-tokens` and tune source/preview limits.
	- Set `--ai-max-output-tokens` and `--claude-max-output-tokens` to constrain completion spend.
	- Use smaller/faster models where acceptable.

## 14. Copilot Custom Agent Quickstart (VS Code)

1. Generate/refresh artifacts first using one of:
	- `pipeline:generate:default`
	- `pipeline:dual:compare`
2. Open Copilot Chat and switch to Agent mode.
3. Select `Mainframe modernization agent` from the agent picker.
4. Attach authoritative artifacts:
	- `.agentic-sdlc/examples/inqacc/output/spec.md`
	- `.agentic-sdlc/examples/inqacc/output/tasks.md`
	- `.agentic-sdlc/examples/inqacc/output/test-spec.md`
	- `.agentic-sdlc/examples/inqacc/output/openapi.yaml`
5. Request explicit task scope (for example TASK-001 to TASK-003).
6. Optionally request gated phases: implementation -> secure review -> test automation -> quality gates.
7. Optionally request dual-model verification and merged summary from `dual-model-analysis.md`.

Notes:

- `Mainframe modernization agent` is the only picker-visible custom agent.
- Specialist agents are delegated internally by the orchestrator.
- If agent definitions do not appear after pull, run VS Code command `Developer: Reload Window`.

References:

- `docs/COPILOT_AGENTS_README.md`
- `docs/COPILOT_CUSTOM_AGENTS.md`
- `docs/COPILOT_AGENT_WORKFLOW.md`

