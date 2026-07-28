from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass(frozen=True)
class GateCommand:
    name: str
    command: Sequence[str]


@dataclass(frozen=True)
class GateResult:
    name: str
    command: Sequence[str]
    exit_code: int
    output: str

    @property
    def status(self) -> str:
        return "PASS" if self.exit_code == 0 else "FAIL"


def _join_output(*parts: str) -> str:
    return "\n".join(part for part in (value.strip() for value in parts) if part)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run project quality gates and emit a deterministic pass/fail summary."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root to run commands in.")
    parser.add_argument(
        "--python-executable",
        default=sys.executable,
        help="Python executable used to run gate scripts.",
    )
    parser.add_argument(
        "--generated-output",
        default=".agentic-sdlc/examples/inqacc/output",
        help="Generated artifact folder used by detail drift validator.",
    )
    parser.add_argument(
        "--bundle-specs",
        default=".agentic-sdlc/spec-kit-bundles/current/specs",
        help="Spec bundle folder used by detail drift validator.",
    )
    return parser.parse_args()


def build_default_gate_commands(
    *,
    python_executable: str,
    generated_output: str,
    bundle_specs: str,
) -> List[GateCommand]:
    return [
        GateCommand(
            name="tests",
            command=[python_executable, "-m", "pytest", "-q", "tests"],
        ),
        GateCommand(
            name="agent-reporting-contract",
            command=[
                python_executable,
                "scripts/validate_agent_reporting_contract.py",
                "--repo-root",
                ".",
            ],
        ),
        GateCommand(
            name="detail-drift",
            command=[
                python_executable,
                "scripts/validate_detail_drift.py",
                "--generated-output",
                generated_output,
                "--bundle-specs",
                bundle_specs,
            ],
        ),
    ]


def _bundle_dir_from_specs(bundle_specs: str) -> str:
    bundle_specs_path = Path(bundle_specs)
    if bundle_specs_path.name.lower() == "specs":
        return str(bundle_specs_path.parent).replace("\\", "/")
    return str(bundle_specs_path).replace("\\", "/")


def ensure_bundle_specs(
    *,
    repo_root: Path,
    python_executable: str,
    generated_output: str,
    bundle_specs: str,
) -> GateResult:
    bundle_specs_path = (repo_root / bundle_specs).resolve()
    check_command = ["bundle-check", bundle_specs]

    if bundle_specs_path.exists() and bundle_specs_path.is_dir():
        return GateResult(
            name="bundle-preflight",
            command=check_command,
            exit_code=0,
            output=f"Bundle specs directory found: {bundle_specs_path}",
        )

    build_command = [
        python_executable,
        "scripts/build_spec_bundle.py",
        "--source-output",
        generated_output,
        "--bundle-dir",
        _bundle_dir_from_specs(bundle_specs),
    ]
    completed = subprocess.run(
        build_command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    output = _join_output(
        f"Bundle specs missing, attempted bootstrap at: {bundle_specs_path}",
        completed.stdout,
        completed.stderr,
    )
    return GateResult(
        name="bundle-preflight",
        command=build_command,
        exit_code=completed.returncode,
        output=output,
    )


def run_gate(command: GateCommand, *, cwd: Path) -> GateResult:
    completed = subprocess.run(
        command.command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    output = _join_output(completed.stdout, completed.stderr)
    return GateResult(
        name=command.name,
        command=command.command,
        exit_code=completed.returncode,
        output=output,
    )


def summarize_results(results: Sequence[GateResult]) -> str:
    lines = ["[QUALITY-GATES] Summary"]
    for result in results:
        rendered = " ".join(shlex.quote(token) for token in result.command)
        lines.append(f"- {result.name}: {result.status} (exit={result.exit_code})")
        lines.append(f"  command: {rendered}")
        if result.output:
            output_lines = result.output.splitlines()
            if result.exit_code == 0:
                preview = output_lines[:3]
                truncated = len(output_lines) > len(preview)
            else:
                preview = output_lines[-12:]
                truncated = len(output_lines) > len(preview)
            lines.append("  output:")
            for line in preview:
                lines.append(f"    {line}")
            if truncated:
                lines.append("    ...")
    return "\n".join(lines)


def overall_exit_code(results: Sequence[GateResult]) -> int:
    return 1 if any(result.exit_code != 0 for result in results) else 0


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    commands = build_default_gate_commands(
        python_executable=args.python_executable,
        generated_output=args.generated_output,
        bundle_specs=args.bundle_specs,
    )
    results: List[GateResult] = []
    # Run deterministic gates first.
    for command in commands[:2]:
        results.append(run_gate(command, cwd=repo_root))

    preflight = ensure_bundle_specs(
        repo_root=repo_root,
        python_executable=args.python_executable,
        generated_output=args.generated_output,
        bundle_specs=args.bundle_specs,
    )
    results.append(preflight)

    if preflight.exit_code == 0:
        results.append(run_gate(commands[2], cwd=repo_root))
    else:
        results.append(
            GateResult(
                name="detail-drift",
                command=commands[2].command,
                exit_code=1,
                output="Skipped because bundle preflight failed.",
            )
        )

    print(summarize_results(results))
    return overall_exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
