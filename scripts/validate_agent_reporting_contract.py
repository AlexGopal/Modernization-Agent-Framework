from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


SPECIALIST_REQUIRED_SNIPPETS = [
    "Guardrails enforced",
    "## Confidence Output Template",
    "Confidence Score: <0-100>",
    "Confidence Rationale: <one line>",
    "Confidence Dimensions:",
    "Evidence fidelity (35%)",
    "Traceability completeness (25%)",
    "Validation signal (25%)",
    "Risk clarity (15%)",
    "Guardrail Cap Applied: <yes|no>",
]

ORCHESTRATOR_REQUIRED_SNIPPETS = [
    "## Confidence Scoring Method",
    "If any blocking guardrail fails, cap confidence at 49.",
    "Guardrails enforced (which guardrails were checked, passed, failed, and blocked)",
    "Agent confidence scorecard (per delegated agent, score 0-100 plus one-line rationale)",
]


@dataclass
class ReportingContractResult:
    missing_by_file: Dict[Path, List[str]]

    @property
    def is_valid(self) -> bool:
        return not self.missing_by_file


def _missing_snippets(path: Path, required_snippets: List[str]) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [snippet for snippet in required_snippets if snippet not in text]


def validate_specialist_contract(agents_dir: Path) -> Dict[Path, List[str]]:
    missing: Dict[Path, List[str]] = {}
    specialist_files = sorted(agents_dir.glob("*specialist.agent.md"))

    for file_path in specialist_files:
        missing_snippets = _missing_snippets(file_path, SPECIALIST_REQUIRED_SNIPPETS)
        if missing_snippets:
            missing[file_path] = missing_snippets

    return missing


def validate_orchestrator_contract(orchestrator_file: Path) -> Dict[Path, List[str]]:
    if not orchestrator_file.exists() or not orchestrator_file.is_file():
        return {orchestrator_file: ["File is missing"]}

    missing_snippets = _missing_snippets(orchestrator_file, ORCHESTRATOR_REQUIRED_SNIPPETS)
    if not missing_snippets:
        return {}
    return {orchestrator_file: missing_snippets}


def validate_reporting_contract(repo_root: Path) -> ReportingContractResult:
    agents_dir = repo_root / ".github" / "agents"
    orchestrator_file = agents_dir / "mainframe-modernization.agent.md"

    missing_by_file: Dict[Path, List[str]] = {}
    missing_by_file.update(validate_specialist_contract(agents_dir))
    missing_by_file.update(validate_orchestrator_contract(orchestrator_file))

    return ReportingContractResult(missing_by_file=missing_by_file)


def _format_report(result: ReportingContractResult, repo_root: Path) -> str:
    if result.is_valid:
        return "[AGENT-CONTRACT] PASS - reporting contract is satisfied."

    lines = ["[AGENT-CONTRACT] FAIL - missing required snippets:"]
    for file_path in sorted(result.missing_by_file.keys()):
        rel = file_path.relative_to(repo_root).as_posix()
        lines.append(f"- {rel}")
        for snippet in result.missing_by_file[file_path]:
            lines.append(f"  - missing: {snippet}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate confidence and guardrail reporting contract across custom agent definitions."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing .github/agents.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    result = validate_reporting_contract(repo_root)
    print(_format_report(result, repo_root))
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
