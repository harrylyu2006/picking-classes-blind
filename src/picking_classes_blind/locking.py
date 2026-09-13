"""Record prospective methods and reject accidental analysis-rule changes."""

import hashlib
import importlib
import json
from datetime import UTC, datetime
from pathlib import Path

METHOD_FILES = [
    "docs/methodology.md",
    "docs/survey-instrument.md",
    "survey/qualtrics-import.txt",
    "docs/data-dictionary.csv",
    "docs/launch-record.md",
    "src/picking_classes_blind/schema.py",
    "src/picking_classes_blind/ingestion.py",
    "src/picking_classes_blind/cleaning.py",
    "src/picking_classes_blind/reporting.py",
    "src/picking_classes_blind/cli.py",
    "src/picking_classes_blind/locking.py",
    "src/picking_classes_blind/rendering.py",
    "pyproject.toml",
    "uv.lock",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _within(project: Path, relative: str) -> Path:
    path = (project / relative).resolve()
    if not path.is_relative_to(project.resolve()):
        raise ValueError("Methods manifest references a path outside the project.")
    return path


def freeze_methods(project: Path, manifest: Path, paths: list[str] | None = None) -> None:
    files = METHOD_FILES if paths is None else paths
    payload = {
        "format_version": 1,
        "created_utc": datetime.now(UTC).isoformat(),
        "status": "prospective; no participant responses analyzed",
        "files": {name: sha256(_within(project, name)) for name in files},
    }
    with manifest.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def verify_methods(project: Path, manifest: Path) -> dict:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(payload.get("files"), dict) or not payload["files"]:
        raise ValueError("Methods manifest must contain a nonempty files mapping.")
    for name, digest in payload["files"].items():
        path = _within(project, name)
        if not path.is_file() or sha256(path) != digest:
            raise ValueError(
                f"Locked method changed: {name}. Record an amendment before proceeding."
            )
    return payload


def verify_runtime(project: Path) -> None:
    """Prevent a lock from one checkout authenticating code executed from another."""
    for name in METHOD_FILES:
        if not name.startswith("src/picking_classes_blind/") or not name.endswith(".py"):
            continue
        module = importlib.import_module("picking_classes_blind." + Path(name).stem)
        if Path(module.__file__).resolve() != _within(project, name):
            raise ValueError(
                "Runtime package does not come from the locked project. "
                "Run uv sync --frozen and uv run pcb from that project directory."
            )
