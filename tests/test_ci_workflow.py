from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_ci_uses_unified_quality_gate_command() -> None:
    workflow_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    content = workflow_path.read_text(encoding="utf-8")

    assert "- name: Run quality gates" in content
    assert "python scripts/run_quality_gates.py --repo-root ." in content


def test_ci_has_secret_gated_ai_artifact_validation_job() -> None:
    workflow_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    content = workflow_path.read_text(encoding="utf-8")

    assert "artifact-validation-ai:" in content
    assert "if: ${{ secrets.AGENTIC_AI_API_KEY != '' }}" in content
    assert "python run_pipeline.py" in content
    assert "--use-ai --ai-provider openai --ai-model gpt-4o-mini --ai-base-url https://api.openai.com" in content
    assert "python scripts/validate_detail_drift.py --generated-output .agentic-sdlc/examples/inqacc/output_ai_ci" in content
