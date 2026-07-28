from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_agent_reporting_contract import (  # noqa: E402
    ORCHESTRATOR_REQUIRED_SNIPPETS,
    SPECIALIST_REQUIRED_SNIPPETS,
    validate_orchestrator_contract,
    validate_reporting_contract,
    validate_specialist_contract,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_validate_specialist_contract_detects_missing_snippets(tmp_path: Path) -> None:
    agents_dir = tmp_path / ".github" / "agents"
    specialist_file = agents_dir / "demo-specialist.agent.md"
    _write(specialist_file, "## Output Format\n1. Files changed\n")

    missing = validate_specialist_contract(agents_dir)

    assert specialist_file in missing
    assert "## Confidence Output Template" in missing[specialist_file]


def test_validate_orchestrator_contract_detects_missing_snippets(tmp_path: Path) -> None:
    orchestrator_file = tmp_path / ".github" / "agents" / "mainframe-modernization.agent.md"
    _write(orchestrator_file, "# Mainframe modernization agent\n")

    missing = validate_orchestrator_contract(orchestrator_file)

    assert orchestrator_file in missing
    assert ORCHESTRATOR_REQUIRED_SNIPPETS[0] in missing[orchestrator_file]


def test_validate_reporting_contract_passes_for_current_repo() -> None:
    result = validate_reporting_contract(REPO_ROOT)

    assert result.is_valid, result.missing_by_file


def test_required_snippet_lists_are_non_empty() -> None:
    assert SPECIALIST_REQUIRED_SNIPPETS
    assert ORCHESTRATOR_REQUIRED_SNIPPETS
