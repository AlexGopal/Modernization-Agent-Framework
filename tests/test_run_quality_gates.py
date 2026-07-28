from pathlib import Path
import sys
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.run_quality_gates import (  # noqa: E402
    GateResult,
    build_default_gate_commands,
    ensure_bundle_specs,
    overall_exit_code,
    summarize_results,
)


def test_build_default_gate_commands_includes_required_gates() -> None:
    commands = build_default_gate_commands(
        python_executable="python",
        generated_output="out",
        bundle_specs="specs",
    )

    names = [item.name for item in commands]
    assert names == ["tests", "agent-reporting-contract", "detail-drift"]

    contract_cmd = list(commands[1].command)
    assert "scripts/validate_agent_reporting_contract.py" in contract_cmd


def test_overall_exit_code_fails_when_any_gate_fails() -> None:
    results = [
        GateResult(name="tests", command=["python"], exit_code=0, output="ok"),
        GateResult(name="contract", command=["python"], exit_code=1, output="bad"),
    ]

    assert overall_exit_code(results) == 1


def test_summarize_results_includes_status_and_command() -> None:
    results = [
        GateResult(
            name="tests",
            command=["python", "-m", "pytest", "-q", "tests"],
            exit_code=0,
            output="10 passed",
        )
    ]

    summary = summarize_results(results)

    assert "[QUALITY-GATES] Summary" in summary
    assert "tests: PASS" in summary
    assert "python -m pytest -q tests" in summary


def test_ensure_bundle_specs_passes_when_existing(tmp_path: Path) -> None:
    (tmp_path / ".agentic-sdlc" / "spec-kit-bundles" / "current" / "specs").mkdir(parents=True)

    result = ensure_bundle_specs(
        repo_root=tmp_path,
        python_executable="python",
        generated_output=".agentic-sdlc/examples/inqacc/output",
        bundle_specs=".agentic-sdlc/spec-kit-bundles/current/specs",
    )

    assert result.name == "bundle-preflight"
    assert result.exit_code == 0
    assert "Bundle specs directory found" in result.output


def test_ensure_bundle_specs_attempts_bootstrap_when_missing(tmp_path: Path) -> None:
    with patch("scripts.run_quality_gates.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "[SPEC-KIT] Bundle ready"
        mock_run.return_value.stderr = ""

        result = ensure_bundle_specs(
            repo_root=tmp_path,
            python_executable="python",
            generated_output=".agentic-sdlc/examples/inqacc/output",
            bundle_specs=".agentic-sdlc/spec-kit-bundles/current/specs",
        )

    assert result.exit_code == 0
    assert "attempted bootstrap" in result.output
    assert "scripts/build_spec_bundle.py" in result.command
