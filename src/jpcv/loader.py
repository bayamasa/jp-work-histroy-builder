"""YAML loader with Pydantic validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from jpcv.models import WorkHistory


def load_yaml(path: str | Path) -> WorkHistory:
    """Load and validate a YAML file into a WorkHistory model."""
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return WorkHistory.model_validate(data)
