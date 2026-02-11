"""YAML loader for 履歴書 data."""

from __future__ import annotations

from pathlib import Path

import yaml

from jp_tenshoku_docs_builder.resume.models import Resume


def load_resume_yaml(
    path: str | Path,
    credential_path: str | Path,
) -> Resume:
    """Load and validate a YAML file into a Resume model.

    Args:
        path: Path to the YAML file.
        credential_path: Path to a credential YAML file.
            Its fields are merged into the resume data
            (credential values take priority).

    Returns:
        Validated Resume model instance.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    credential_path = Path(credential_path)
    with credential_path.open(encoding="utf-8") as f:
        credential_data = yaml.safe_load(f)
    if credential_data:
        data.update(credential_data)

    return Resume.model_validate(data)
