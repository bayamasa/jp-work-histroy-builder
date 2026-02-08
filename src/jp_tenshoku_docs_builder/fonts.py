"""Font registration and discovery for Japanese PDF generation."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font search candidates: (file_name, family_name, subfont_index or None)
# Ordered by preference. subfont_index is needed for .ttc files.
_GOTHIC_CANDIDATES = [
    ("ipaexg.ttf", "IPAexGothic", None),
    ("NotoSansJP-Regular.ttf", "NotoSansJP", None),
    ("NotoSansCJKjp-Regular.ttf", "NotoSansCJKjp", None),
    # macOS fallbacks (TrueType outline, ReportLab compatible)
    ("AppleGothic.ttf", "AppleGothic", None),
]

_MINCHO_CANDIDATES = [
    ("ipaexm.ttf", "IPAexMincho", None),
    ("NotoSerifJP-Regular.ttf", "NotoSerifJP", None),
    ("NotoSerifCJKjp-Regular.ttf", "NotoSerifCJKjp", None),
    # macOS fallback (Korean Myungjo, but supports Japanese kanji)
    ("AppleMyungjo.ttf", "AppleMyungjo", None),
]


def _system_font_dirs() -> list[Path]:
    """Return platform-specific system font directories."""
    dirs: list[Path] = []
    if sys.platform == "darwin":
        dirs.extend([
            Path.home() / "Library" / "Fonts",
            Path("/Library/Fonts"),
            Path("/System/Library/Fonts"),
        ])
    elif sys.platform == "linux":
        dirs.extend([
            Path.home() / ".local" / "share" / "fonts",
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
        ])
    elif sys.platform == "win32":
        dirs.append(Path("C:/Windows/Fonts"))
    return [d for d in dirs if d.is_dir()]


def _find_font(
    candidates: list[tuple[str, str, int | None]],
    search_dirs: list[Path],
) -> tuple[Path, str, int | None] | None:
    """Find the first available font from candidates in search directories."""
    for font_file, family_name, subfont_idx in candidates:
        for d in search_dirs:
            path = d / font_file
            if path.exists():
                return path, family_name, subfont_idx
            # Also check subdirectories one level deep
            try:
                for sub in d.iterdir():
                    if sub.is_dir():
                        path = sub / font_file
                        if path.exists():
                            return path, family_name, subfont_idx
            except PermissionError:
                continue
    return None


def _register_font(name: str, path: Path, subfont_index: int | None) -> None:
    """Register a single font with ReportLab."""
    if subfont_index is not None:
        pdfmetrics.registerFont(TTFont(name, str(path), subfontIndex=subfont_index))
    else:
        pdfmetrics.registerFont(TTFont(name, str(path)))
    addMapping(name, 0, 0, name)


@dataclass
class FontConfig:
    """Registered font configuration."""

    gothic: str  # Font name for headings (gothic/sans-serif)
    mincho: str  # Font name for body text (mincho/serif)


def register_fonts(font_dir: str | Path | None = None) -> FontConfig:
    """Discover and register Japanese fonts. Returns FontConfig with registered names.

    Search order:
    1. Specified font_dir (if provided)
    2. Project's fonts/ directory
    3. System font directories
    """
    search_dirs: list[Path] = []

    if font_dir:
        search_dirs.append(Path(font_dir))

    # Project fonts directory
    search_dirs.append(Path("fonts"))

    # System fonts
    search_dirs.extend(_system_font_dirs())

    # Find and register gothic font
    gothic_result = _find_font(_GOTHIC_CANDIDATES, search_dirs)
    if gothic_result:
        path, _family, subfont_idx = gothic_result
        gothic_name = "Gothic"
        _register_font(gothic_name, path, subfont_idx)
    else:
        gothic_name = "Helvetica"

    # Find and register mincho font
    mincho_result = _find_font(_MINCHO_CANDIDATES, search_dirs)
    if mincho_result:
        path, _family, subfont_idx = mincho_result
        mincho_name = "Mincho"
        _register_font(mincho_name, path, subfont_idx)
    else:
        # Fall back to gothic if available, otherwise Helvetica
        mincho_name = gothic_name

    if gothic_name == "Helvetica" and mincho_name == "Helvetica":
        print(
            "WARNING: No Japanese fonts found. "
            "Please install IPAex fonts or specify --font-dir. "
            "See fonts/README.md for details."
        )

    return FontConfig(gothic=gothic_name, mincho=mincho_name)
