"""YAML loader with Pydantic validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from jp_tenshoku_docs_builder.work_history.models import StandardWorkHistory, StarWorkHistory, _WorkHistoryBase


def load_yaml(
    path: str | Path,
    content_format: str = "standard",
    credential_path: str | Path | None = None,
) -> _WorkHistoryBase:
    """Load and validate a YAML file into a WorkHistory model.

    Args:
        path: Path to the YAML file.
        content_format: Project content format ("standard" or "star").
        credential_path: Optional path to a credential YAML file.
            When provided, its fields are merged into the data
            (credential values take priority).

    Returns:
        Validated WorkHistory model instance.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if credential_path is not None:
        credential_path = Path(credential_path)
        with credential_path.open(encoding="utf-8") as f:
            credential_data = yaml.safe_load(f)
        if credential_data:
            data.update(credential_data)

    if content_format == "star":
        return StarWorkHistory.model_validate(data)
    return StandardWorkHistory.model_validate(data)
