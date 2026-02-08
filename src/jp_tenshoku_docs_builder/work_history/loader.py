"""YAML loader with Pydantic validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from jp_tenshoku_docs_builder.work_history.models import StandardWorkHistory, StarWorkHistory, _WorkHistoryBase


def load_yaml(path: str | Path, content_format: str = "standard") -> _WorkHistoryBase:
    """Load and validate a YAML file into a WorkHistory model.

    Args:
        path: Path to the YAML file.
        content_format: Project content format ("standard" or "star").

    Returns:
        Validated WorkHistory model instance.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if content_format == "star":
        return StarWorkHistory.model_validate(data)
    return StandardWorkHistory.model_validate(data)
