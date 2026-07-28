from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_detail_drift import (  # noqa: E402
    ValidationThresholds,
    build_report,
    validate_cross_artifact_consistency,
    validate_artifact,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_validate_artifact_passes_when_within_thresholds(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "bundle" / "specs"
    generated_dir = tmp_path / "output"

    baseline = "# Spec\n\n## Requirements\n- FR-001\n- AC-001\n"
    generated = "# Spec\n\n## Requirements\n- FR-001\n- AC-001\n- TASK-001\n"
    _write(baseline_dir / "spec.md", baseline)
    _write(generated_dir / "spec.md", generated)

    thresholds = ValidationThresholds(
        min_char_ratio=0.75,
        max_char_ratio=1.5,
        min_heading_ratio=0.6,
        max_heading_ratio=1.6,
        min_id_ratio=0.5,
        max_id_ratio=2.0,
    )

    result = validate_artifact(
        artifact="spec.md",
        baseline_dir=baseline_dir,
        generated_dir=generated_dir,
        thresholds=thresholds,
    )

    assert result.status == "pass"
    assert result.reasons == []


def test_validate_artifact_fails_when_too_short(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "bundle" / "specs"
    generated_dir = tmp_path / "output"

    baseline = "# Spec\n\n## Rules\n- FR-001\n- AC-001\n- TC-001\n"
    generated = "# Spec\n"
    _write(baseline_dir / "spec.md", baseline)
    _write(generated_dir / "spec.md", generated)

    thresholds = ValidationThresholds(
        min_char_ratio=0.8,
        max_char_ratio=1.4,
        min_heading_ratio=0.8,
        max_heading_ratio=1.4,
        min_id_ratio=0.8,
        max_id_ratio=1.4,
    )

    result = validate_artifact(
        artifact="spec.md",
        baseline_dir=baseline_dir,
        generated_dir=generated_dir,
        thresholds=thresholds,
    )

    assert result.status == "fail"
    assert any("chars ratio too low" in reason for reason in result.reasons)


def test_build_report_contains_summary() -> None:
    thresholds = ValidationThresholds(
        min_char_ratio=0.75,
        max_char_ratio=1.35,
        min_heading_ratio=0.7,
        max_heading_ratio=1.6,
        min_id_ratio=0.7,
        max_id_ratio=1.6,
    )

    report = build_report(results=[], thresholds=thresholds)

    assert "Detail Drift Validation Report" in report
    assert "Summary" in report


def test_validate_artifact_warns_for_id_continuity_gaps(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "bundle" / "specs"
    generated_dir = tmp_path / "output"

    baseline = "# Spec\n\n## Requirements\n- FR-001\n- FR-002\n- FR-003\n- AC-001\n"
    generated = "# Spec\n\n## Requirements\n- FR-001\n- FR-003\n- FR-004\n- AC-001\n"
    _write(baseline_dir / "spec.md", baseline)
    _write(generated_dir / "spec.md", generated)

    thresholds = ValidationThresholds(
        min_char_ratio=0.70,
        max_char_ratio=1.35,
        min_heading_ratio=0.70,
        max_heading_ratio=1.60,
        min_id_ratio=0.60,
        max_id_ratio=1.10,
    )

    result = validate_artifact(
        artifact="spec.md",
        baseline_dir=baseline_dir,
        generated_dir=generated_dir,
        thresholds=thresholds,
    )

    assert result.status == "warn"
    assert any("ID continuity gap" in reason for reason in result.reasons)


def test_validate_cross_artifact_consistency_flags_missing_links() -> None:
    artifact_ids = {
        "business-rules.md": {"BR-001", "BR-002"},
        "requirements.md": {"FR-001", "AC-001", "BR-001"},
        "spec.md": {"FR-001"},
        "tasks.md": {"TASK-001"},
        "test-spec.md": {"TC-001"},
    }

    issues = validate_cross_artifact_consistency(artifact_ids)

    assert issues
    assert any("AC IDs exist in requirements.md but not in spec.md" in issue.message for issue in issues)
    assert any("BR IDs exist in business-rules.md" in issue.message for issue in issues)
    assert any("TASK IDs exist in tasks.md" in issue.message for issue in issues)


def test_validate_artifact_warns_for_dry_run_openapi_marker_gaps(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "bundle" / "specs"
    generated_dir = tmp_path / "output"

    baseline = "openapi: 3.0.3\npaths:\n  /health:\n    get: {}\n"
    generated = "# openapi.yaml\n\nStatus: DRY RUN\n\n## Prompt Template\n"
    _write(baseline_dir / "openapi.yaml", baseline)
    _write(generated_dir / "openapi.yaml", generated)

    thresholds = ValidationThresholds(
        min_char_ratio=0.10,
        max_char_ratio=5.00,
        min_heading_ratio=0.0,
        max_heading_ratio=10.0,
        min_id_ratio=0.0,
        max_id_ratio=10.0,
    )

    result = validate_artifact(
        artifact="openapi.yaml",
        baseline_dir=baseline_dir,
        generated_dir=generated_dir,
        thresholds=thresholds,
    )

    assert result.status == "pass"
    assert any(
        "Dry-run OpenAPI scaffold missing required content markers" in reason
        for reason in result.reasons
    )
