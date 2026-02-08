"""YAML loader for 履歴書 data."""

from __future__ import annotations

from pathlib import Path

import yaml

from jp_tenshoku_docs_builder.resume.models import Resume


def load_resume_yaml(path: str | Path) -> Resume:
    """Load and validate a YAML file into a Resume model.

    Args:
        path: Path to the YAML file.

    Returns:
        Validated Resume model instance.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Resume.model_validate(data)
