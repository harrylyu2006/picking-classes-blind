import json
from pathlib import Path

import pytest

from picking_classes_blind.cli import main
from picking_classes_blind.locking import freeze_methods, verify_methods


def test_freeze_detects_changes_and_refuses_replacement(tmp_path):
    project = tmp_path / "project"
    (project / "docs").mkdir(parents=True)
    (project / "docs/methodology.md").write_text("Locked rules")
    manifest = project / "methods-lock.json"
    freeze_methods(project, manifest, paths=["docs/methodology.md"])
    verify_methods(project, manifest)
    with pytest.raises(FileExistsError):
        freeze_methods(project, manifest, paths=["docs/methodology.md"])
    (project / "docs/methodology.md").write_text("Changed rules")
    with pytest.raises(ValueError, match="changed"):
        verify_methods(project, manifest)


def test_demo_end_to_end_and_existing_output_refused(tmp_path):
    output = tmp_path / "demo"
    assert main(["demo", "--output", str(output)]) == 0
    report = json.loads((output / "qa_report.json").read_text())
    assert report["data_kind"] == "synthetic"
    assert report["balanced"] is True
    assert report["raw_rows"] == report["analysis_rows"] + report["excluded_rows"]
    assert len(report["input_sha256"]) == 64
    assert (output / "public/index.html").exists()
    for file in (output / "public").iterdir():
        if file.suffix == ".csv":
            assert "ResponseId" not in file.read_text()
            assert "SYN_" not in file.read_text()
    assert main(["demo", "--output", str(output)]) == 2


def test_real_run_needs_unchanged_methods_lock_before_output(tmp_path):
    output = tmp_path / "real"
    assert (
        main(
            [
                "run",
                "missing.csv",
                "--output",
                str(output),
                "--lock",
                str(tmp_path / "missing.json"),
            ]
        )
        == 2
    )
    assert not output.exists()


def test_lock_file_cannot_escape_project(tmp_path):
    manifest = tmp_path / "bad-lock.json"
    manifest.write_text(json.dumps({"files": {"../outside": "a" * 64}}))
    with pytest.raises(ValueError, match="outside"):
        verify_methods(tmp_path, manifest)


def test_runtime_must_match_locked_project(tmp_path, capsys):
    from picking_classes_blind.locking import METHOD_FILES

    project = Path(__file__).resolve().parents[1]
    other = tmp_path / "other"
    for name in METHOD_FILES:
        target = other / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((project / name).read_bytes())
    cleaning = other / "src/picking_classes_blind/cleaning.py"
    cleaning.write_text(cleaning.read_text().replace("< 90", "< 900"))
    manifest = other / "methods-lock.json"
    freeze_methods(other, manifest)
    assert (
        main(
            [
                "run",
                "missing.csv",
                "--output",
                str(tmp_path / "out"),
                "--project",
                str(other),
                "--lock",
                str(manifest),
            ]
        )
        == 2
    )
    assert "runtime" in capsys.readouterr().err.lower()


def test_participant_command_with_generated_fixture_and_exact_input_hash(tmp_path):
    import hashlib

    from picking_classes_blind.cleaning import clean_responses
    from picking_classes_blind.synthetic import make_synthetic

    # Temporary generated fixture exercises the real-data code path; these are not real responses.
    frame = clean_responses(make_synthetic()).analysis
    frame["ResponseId"] = [f"FIXTURE_ROW_{i}" for i in range(len(frame))]
    frame["P2"] = frame["P2"].apply(lambda values: ",".join(map(str, values)))
    input_path = tmp_path / "fixture.csv"
    frame.to_csv(input_path, index=False)
    project = Path(__file__).resolve().parents[1]
    manifest = tmp_path / "test-lock.json"
    freeze_methods(project, manifest)
    out = tmp_path / "participant-code-path"
    assert (
        main(
            [
                "run",
                str(input_path),
                "--output",
                str(out),
                "--project",
                str(project),
                "--lock",
                str(manifest),
            ]
        )
        == 0
    )
    report = json.loads((out / "qa_report.json").read_text())
    assert report["analysis_rows"] == 50
    assert report["input_sha256"] == hashlib.sha256(input_path.read_bytes()).hexdigest()
    assert report["metadata_rows_skipped"] == 0
    assert report["data_kind"] == "participant"
    assert "FIXTURE_ROW_" not in (out / "public/index.html").read_text()


def test_synthetic_records_cannot_be_presented_as_participant_data(tmp_path, capsys):
    from picking_classes_blind.synthetic import make_synthetic

    project = Path(__file__).resolve().parents[1]
    manifest = tmp_path / "test-lock.json"
    freeze_methods(project, manifest)
    source = tmp_path / "synthetic.csv"
    make_synthetic().to_csv(source, index=False)
    output = tmp_path / "out"
    assert (
        main(
            [
                "run",
                str(source),
                "--output",
                str(output),
                "--project",
                str(project),
                "--lock",
                str(manifest),
            ]
        )
        == 2
    )
    assert "synthetic" in capsys.readouterr().err.lower()
    assert not output.exists()
