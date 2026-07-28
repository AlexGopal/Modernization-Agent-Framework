from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

BUSINESS_RULES_ARTIFACT = "business-rules.md"
REQUIREMENTS_ARTIFACT = "requirements.md"
SPEC_ARTIFACT = "spec.md"
TASKS_ARTIFACT = "tasks.md"
TEST_SPEC_ARTIFACT = "test-spec.md"

DEFAULT_ARTIFACTS = [
    BUSINESS_RULES_ARTIFACT,
    REQUIREMENTS_ARTIFACT,
    SPEC_ARTIFACT,
    TASKS_ARTIFACT,
    TEST_SPEC_ARTIFACT,
    "openapi.yaml",
]

TOKEN_PATTERN = re.compile(r"\b(?P<prefix>FR|BR|NFR|AC|TC|TASK)-(?P<number>\d+)\b", re.IGNORECASE)

REQUIRED_CONTENT_MARKERS: Dict[str, List[str]] = {
    BUSINESS_RULES_ARTIFACT: ["#", "br-"],
    REQUIREMENTS_ARTIFACT: ["#", "fr-", "ac-"],
    SPEC_ARTIFACT: ["#", "fr-", "ac-"],
    TASKS_ARTIFACT: ["#", "task-"],
    TEST_SPEC_ARTIFACT: ["#", "tc-"],
    "openapi.yaml": ["openapi:", "paths:"],
}


@dataclass
class ArtifactMetrics:
    chars: int
    headings: int
    table_rows: int
    ids: int
    unique_ids: int = 0
    duplicate_ids: int = 0
    missing_required_markers: int = 0


@dataclass
class ValidationThresholds:
    min_char_ratio: float
    max_char_ratio: float
    min_heading_ratio: float
    max_heading_ratio: float
    min_id_ratio: float
    max_id_ratio: float


@dataclass
class ArtifactValidationResult:
    artifact: str
    status: str
    reasons: List[str]
    baseline: ArtifactMetrics
    generated: ArtifactMetrics


@dataclass
class CrossArtifactIssue:
    status: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate generated artifact detail level against Spec Kit baseline to "
            "detect under-specification and over-specification drift."
        )
    )
    parser.add_argument(
        "--generated-output",
        default=".agentic-sdlc/examples/inqacc/output",
        help="Generated artifact folder to validate.",
    )
    parser.add_argument(
        "--bundle-specs",
        default=".agentic-sdlc/spec-kit-bundles/current/specs",
        help="Spec Kit specs folder used as baseline.",
    )
    parser.add_argument(
        "--artifacts",
        default=",".join(DEFAULT_ARTIFACTS),
        help="Comma-separated list of artifacts to validate.",
    )
    parser.add_argument("--min-char-ratio", type=float, default=0.75)
    parser.add_argument("--max-char-ratio", type=float, default=1.35)
    parser.add_argument("--min-heading-ratio", type=float, default=0.70)
    parser.add_argument("--max-heading-ratio", type=float, default=1.60)
    parser.add_argument("--min-id-ratio", type=float, default=0.70)
    parser.add_argument("--max-id-ratio", type=float, default=1.60)
    parser.add_argument(
        "--report-file",
        default="detail-drift-report.md",
        help="Report filename written under generated output folder.",
    )
    return parser.parse_args()


def _safe_ratio(value: int, baseline: int) -> float | None:
    if baseline <= 0:
        return None
    return value / baseline


def _ratio_text(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def _metric_status(
    *,
    name: str,
    ratio: float | None,
    min_ratio: float,
    max_ratio: float,
) -> Tuple[bool, str | None]:
    if ratio is None:
        return True, None
    if ratio < min_ratio:
        return False, f"{name} ratio too low ({ratio:.2f} < {min_ratio:.2f})"
    if ratio > max_ratio:
        return False, f"{name} ratio too high ({ratio:.2f} > {max_ratio:.2f})"
    return True, None


def collect_metrics(path: Path) -> ArtifactMetrics:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    ids = [match.group(0).upper() for match in TOKEN_PATTERN.finditer(text)]
    unique_ids = set(ids)
    return ArtifactMetrics(
        chars=len(text),
        headings=sum(1 for line in lines if line.lstrip().startswith("#")),
        table_rows=sum(1 for line in lines if "|" in line),
        ids=len(ids),
        unique_ids=len(unique_ids),
        duplicate_ids=max(0, len(ids) - len(unique_ids)),
    )


def _find_missing_required_markers(artifact: str, text: str) -> List[str]:
    markers = REQUIRED_CONTENT_MARKERS.get(artifact.lower(), [])
    lowered = text.lower()
    return [marker for marker in markers if marker not in lowered]


def _collect_ids_by_prefix(text: str) -> Dict[str, Set[int]]:
    per_prefix: Dict[str, Set[int]] = {}
    for match in TOKEN_PATTERN.finditer(text):
        prefix = match.group("prefix").upper()
        number = int(match.group("number"))
        per_prefix.setdefault(prefix, set()).add(number)
    return per_prefix


def _missing_sequence_values(values: Set[int]) -> List[int]:
    if len(values) < 3:
        return []

    minimum = min(values)
    maximum = max(values)
    return [value for value in range(minimum, maximum + 1) if value not in values]


def _format_gap_message(prefix: str, missing: List[int]) -> str:
    preview = ", ".join(str(value) for value in missing[:5])
    suffix = "..." if len(missing) > 5 else ""
    return f"ID continuity gap for {prefix}: missing {preview}{suffix}"


def _find_id_gaps(text: str) -> List[str]:
    gaps: List[str] = []
    for prefix, values in _collect_ids_by_prefix(text).items():
        missing = _missing_sequence_values(values)
        if missing:
            gaps.append(_format_gap_message(prefix, missing))
    return gaps


def _collect_semantic_reasons(artifact: str, generated_path: Path, generated: ArtifactMetrics) -> List[str]:
    reasons: List[str] = []
    generated_text = generated_path.read_text(encoding="utf-8", errors="ignore")

    missing_markers = _find_missing_required_markers(artifact, generated_text)
    generated.missing_required_markers = len(missing_markers)
    if missing_markers:
        if artifact.lower() == "openapi.yaml" and "status: dry run" in generated_text.lower():
            reasons.append(
                "Dry-run OpenAPI scaffold missing required content markers: "
                + ", ".join(missing_markers)
            )
        else:
            reasons.append(
                "Missing required content markers: " + ", ".join(missing_markers)
            )

    # Duplicate IDs are a quality signal rather than a hard failure, but they are surfaced.
    if generated.duplicate_ids > 0:
        reasons.append(
            f"Non-unique ID occurrences detected ({generated.duplicate_ids} duplicate mentions)"
        )

    reasons.extend(_find_id_gaps(generated_text))
    return reasons


def _classify_reasons(reasons: List[str]) -> Tuple[List[str], List[str]]:
    warn_prefixes = (
        "Non-unique ID occurrences",
        "ID continuity gap",
        "Dry-run OpenAPI scaffold missing required content markers",
    )
    blocking: List[str] = []
    warnings: List[str] = []
    for reason in reasons:
        if reason.startswith(warn_prefixes):
            warnings.append(reason)
        else:
            blocking.append(reason)
    return blocking, warnings


def _status_from_reasons(
    *,
    baseline: ArtifactMetrics,
    blocking_reasons: List[str],
    all_reasons: List[str],
) -> str:
    if baseline.headings == 0 and baseline.ids == 0:
        return "pass" if not blocking_reasons else "fail"

    if blocking_reasons:
        return "fail"
    if all_reasons:
        return "warn"
    return "pass"


def validate_artifact(
    *,
    artifact: str,
    baseline_dir: Path,
    generated_dir: Path,
    thresholds: ValidationThresholds,
) -> ArtifactValidationResult:
    baseline_path = baseline_dir / artifact
    generated_path = generated_dir / artifact

    if not baseline_path.exists() or not baseline_path.is_file():
        return ArtifactValidationResult(
            artifact=artifact,
            status="warn",
            reasons=["Baseline artifact is missing, skipped."],
            baseline=ArtifactMetrics(0, 0, 0, 0),
            generated=ArtifactMetrics(0, 0, 0, 0),
        )

    if not generated_path.exists() or not generated_path.is_file():
        baseline = collect_metrics(baseline_path)
        return ArtifactValidationResult(
            artifact=artifact,
            status="fail",
            reasons=["Generated artifact is missing."],
            baseline=baseline,
            generated=ArtifactMetrics(0, 0, 0, 0),
        )

    baseline = collect_metrics(baseline_path)
    generated = collect_metrics(generated_path)
    char_ratio = _safe_ratio(generated.chars, baseline.chars)
    heading_ratio = _safe_ratio(generated.headings, baseline.headings)
    id_ratio = _safe_ratio(generated.ids, baseline.ids)

    checks = [
        _metric_status(
            name="chars",
            ratio=char_ratio,
            min_ratio=thresholds.min_char_ratio,
            max_ratio=thresholds.max_char_ratio,
        ),
        _metric_status(
            name="headings",
            ratio=heading_ratio,
            min_ratio=thresholds.min_heading_ratio,
            max_ratio=thresholds.max_heading_ratio,
        ),
        _metric_status(
            name="ids",
            ratio=id_ratio,
            min_ratio=thresholds.min_id_ratio,
            max_ratio=thresholds.max_id_ratio,
        ),
    ]
    reasons = [message for passed, message in checks if not passed and message]
    reasons.extend(_collect_semantic_reasons(artifact, generated_path, generated))

    blocking_reasons, _warning_reasons = _classify_reasons(reasons)
    status = _status_from_reasons(
        baseline=baseline,
        blocking_reasons=blocking_reasons,
        all_reasons=reasons,
    )

    return ArtifactValidationResult(
        artifact=artifact,
        status=status,
        reasons=reasons,
        baseline=baseline,
        generated=generated,
    )


def build_report(
    *,
    results: List[ArtifactValidationResult],
    thresholds: ValidationThresholds,
    cross_issues: List[CrossArtifactIssue] | None = None,
) -> str:
    cross_issues = cross_issues or []
    fails = [item for item in results if item.status == "fail"]
    warns = [item for item in results if item.status == "warn"]
    cross_fails = [item for item in cross_issues if item.status == "fail"]
    cross_warns = [item for item in cross_issues if item.status == "warn"]

    lines = [
        "# Detail Drift Validation Report",
        "",
        "Compares generated artifacts against the Spec Kit baseline to catch under- and over-detail drift.",
        "",
        "## Thresholds",
        "",
        f"- Char ratio: {thresholds.min_char_ratio:.2f} to {thresholds.max_char_ratio:.2f}",
        f"- Heading ratio: {thresholds.min_heading_ratio:.2f} to {thresholds.max_heading_ratio:.2f}",
        f"- ID ratio: {thresholds.min_id_ratio:.2f} to {thresholds.max_id_ratio:.2f}",
        "",
        (
            "## Summary\n\n"
            f"- Pass: {len(results) - len(fails) - len(warns)}\n"
            f"- Warn: {len(warns)}\n"
            f"- Fail: {len(fails)}\n"
            f"- Cross-check warn: {len(cross_warns)}\n"
            f"- Cross-check fail: {len(cross_fails)}"
        ),
        "",
        "## Results",
        "",
        "| Artifact | Status | Baseline chars | Generated chars | Char ratio | Heading ratio | ID ratio | Unique IDs | Duplicate mentions | Notes |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]

    for item in results:
        char_ratio = _ratio_text(_safe_ratio(item.generated.chars, item.baseline.chars))
        heading_ratio = _ratio_text(_safe_ratio(item.generated.headings, item.baseline.headings))
        id_ratio = _ratio_text(_safe_ratio(item.generated.ids, item.baseline.ids))
        notes = "; ".join(item.reasons) if item.reasons else "within thresholds"
        lines.append(
            f"| {item.artifact} | {item.status} | {item.baseline.chars} | {item.generated.chars} | "
            f"{char_ratio} | {heading_ratio} | {id_ratio} | {item.generated.unique_ids} | "
            f"{item.generated.duplicate_ids} | {notes} |"
        )

    lines.append("")
    if cross_issues:
        lines.extend(
            [
                "## Cross-Artifact Consistency",
                "",
                "| Status | Issue |",
                "|---|---|",
            ]
        )
        for issue in cross_issues:
            lines.append(f"| {issue.status} | {issue.message} |")
        lines.append("")

    if fails or cross_fails:
        lines.append("Validation failed because at least one artifact drifted outside configured thresholds.")
    else:
        lines.append("Validation passed.")

    lines.append("")
    return "\n".join(lines)


def _ids_with_prefix(ids: Set[str], prefix: str) -> Set[str]:
    return {value for value in ids if value.startswith(f"{prefix}-")}


def _collect_artifact_ids(generated_dir: Path, artifacts: List[str]) -> Dict[str, Set[str]]:
    artifact_ids: Dict[str, Set[str]] = {}
    for artifact in artifacts:
        path = generated_dir / artifact
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        artifact_ids[artifact] = {match.group(0).upper() for match in TOKEN_PATTERN.finditer(text)}
    return artifact_ids


def validate_cross_artifact_consistency(
    artifact_ids: Dict[str, Set[str]],
) -> List[CrossArtifactIssue]:
    issues: List[CrossArtifactIssue] = []

    requirements_ids = artifact_ids.get(REQUIREMENTS_ARTIFACT, set())
    spec_ids = artifact_ids.get(SPEC_ARTIFACT, set())
    rules_ids = artifact_ids.get(BUSINESS_RULES_ARTIFACT, set())
    tasks_ids = artifact_ids.get(TASKS_ARTIFACT, set())
    test_spec_ids = artifact_ids.get(TEST_SPEC_ARTIFACT, set())

    fr_missing = _ids_with_prefix(requirements_ids, "FR") - _ids_with_prefix(spec_ids, "FR")
    if fr_missing:
        issues.append(
            CrossArtifactIssue(
                status="fail",
                message=(
                    f"FR IDs exist in {REQUIREMENTS_ARTIFACT} but not in {SPEC_ARTIFACT}: "
                    + ", ".join(sorted(fr_missing)[:10])
                ),
            )
        )

    ac_missing = _ids_with_prefix(requirements_ids, "AC") - _ids_with_prefix(spec_ids, "AC")
    if ac_missing:
        issues.append(
            CrossArtifactIssue(
                status="fail",
                message=(
                    f"AC IDs exist in {REQUIREMENTS_ARTIFACT} but not in {SPEC_ARTIFACT}: "
                    + ", ".join(sorted(ac_missing)[:10])
                ),
            )
        )

    br_referenced = _ids_with_prefix(requirements_ids, "BR") | _ids_with_prefix(spec_ids, "BR")
    br_unmapped = _ids_with_prefix(rules_ids, "BR") - br_referenced
    if br_unmapped:
        issues.append(
            CrossArtifactIssue(
                status="fail",
                message=(
                    f"BR IDs exist in {BUSINESS_RULES_ARTIFACT} without reference in "
                    f"{REQUIREMENTS_ARTIFACT} or {SPEC_ARTIFACT}: "
                    + ", ".join(sorted(br_unmapped)[:10])
                ),
            )
        )

    task_uncovered = _ids_with_prefix(tasks_ids, "TASK") - _ids_with_prefix(test_spec_ids, "TASK")
    if task_uncovered:
        issues.append(
            CrossArtifactIssue(
                status="fail",
                message=(
                    f"TASK IDs exist in {TASKS_ARTIFACT} without mention in {TEST_SPEC_ARTIFACT}: "
                    + ", ".join(sorted(task_uncovered)[:10])
                ),
            )
        )

    return issues


def main() -> int:
    args = parse_args()

    generated_dir = Path(args.generated_output).resolve()
    baseline_dir = Path(args.bundle_specs).resolve()
    artifacts = [name.strip() for name in args.artifacts.split(",") if name.strip()]

    if not generated_dir.exists() or not generated_dir.is_dir():
        raise FileNotFoundError(f"Generated output folder not found: {generated_dir}")
    if not baseline_dir.exists() or not baseline_dir.is_dir():
        raise FileNotFoundError(f"Bundle specs folder not found: {baseline_dir}")

    thresholds = ValidationThresholds(
        min_char_ratio=args.min_char_ratio,
        max_char_ratio=args.max_char_ratio,
        min_heading_ratio=args.min_heading_ratio,
        max_heading_ratio=args.max_heading_ratio,
        min_id_ratio=args.min_id_ratio,
        max_id_ratio=args.max_id_ratio,
    )

    results = [
        validate_artifact(
            artifact=artifact,
            baseline_dir=baseline_dir,
            generated_dir=generated_dir,
            thresholds=thresholds,
        )
        for artifact in artifacts
    ]

    artifact_ids = _collect_artifact_ids(generated_dir, artifacts)
    cross_issues = validate_cross_artifact_consistency(artifact_ids)

    report = build_report(results=results, thresholds=thresholds, cross_issues=cross_issues)
    report_path = generated_dir / args.report_file
    report_path.write_text(report, encoding="utf-8")

    fail_count = sum(1 for item in results if item.status == "fail")
    warn_count = sum(1 for item in results if item.status == "warn")
    cross_fail_count = sum(1 for item in cross_issues if item.status == "fail")
    cross_warn_count = sum(1 for item in cross_issues if item.status == "warn")
    print(f"[DETAIL-DRIFT] Report: {report_path}")
    print(
        "[DETAIL-DRIFT] "
        f"Pass={len(results) - fail_count - warn_count} "
        f"Warn={warn_count} Fail={fail_count} "
        f"CrossWarn={cross_warn_count} CrossFail={cross_fail_count}"
    )

    return 1 if (fail_count + cross_fail_count) > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
