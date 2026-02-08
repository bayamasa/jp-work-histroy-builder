"""ReportLab style definitions for 職務経歴書."""

from __future__ import annotations

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm

from jpcv.fonts import FontConfig

# Page settings (A4)
PAGE_WIDTH = 210 * mm
PAGE_HEIGHT = 297 * mm
MARGIN_LEFT = 20 * mm
MARGIN_RIGHT = 20 * mm
MARGIN_TOP = 15 * mm
MARGIN_BOTTOM = 15 * mm

# Font sizes
TITLE_SIZE = 16
SECTION_HEADER_SIZE = 11
BODY_SIZE = 9
SMALL_SIZE = 8
TABLE_SIZE = 8


def build_styles(fonts: FontConfig) -> dict[str, ParagraphStyle]:
    """Build all paragraph styles using the given font configuration."""
    base = getSampleStyleSheet()

    styles: dict[str, ParagraphStyle] = {}

    styles["title"] = ParagraphStyle(
        "CVTitle",
        parent=base["Normal"],
        fontName=fonts.gothic,
        fontSize=TITLE_SIZE,
        alignment=TA_CENTER,
        spaceAfter=2 * mm,
        leading=TITLE_SIZE * 1.4,
    )

    styles["date"] = ParagraphStyle(
        "CVDate",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=BODY_SIZE,
        alignment=TA_RIGHT,
        spaceAfter=1 * mm,
    )

    styles["name"] = ParagraphStyle(
        "CVName",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=BODY_SIZE,
        alignment=TA_RIGHT,
        spaceAfter=3 * mm,
    )

    styles["section_header"] = ParagraphStyle(
        "SectionHeader",
        parent=base["Normal"],
        fontName=fonts.gothic,
        fontSize=SECTION_HEADER_SIZE,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
        leading=SECTION_HEADER_SIZE * 1.4,
    )

    styles["body"] = ParagraphStyle(
        "CVBody",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=BODY_SIZE,
        leading=BODY_SIZE * 1.8,
        spaceAfter=2 * mm,
    )

    styles["bullet"] = ParagraphStyle(
        "CVBullet",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=BODY_SIZE,
        leading=BODY_SIZE * 1.8,
        leftIndent=4 * mm,
    )

    styles["cell"] = ParagraphStyle(
        "CVCell",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=TABLE_SIZE,
        leading=TABLE_SIZE * 1.6,
    )

    styles["cell_gothic"] = ParagraphStyle(
        "CVCellGothic",
        parent=base["Normal"],
        fontName=fonts.gothic,
        fontSize=TABLE_SIZE,
        leading=TABLE_SIZE * 1.6,
    )

    styles["cell_small"] = ParagraphStyle(
        "CVCellSmall",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=SMALL_SIZE,
        leading=SMALL_SIZE * 1.5,
    )

    styles["right"] = ParagraphStyle(
        "CVRight",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=BODY_SIZE,
        alignment=TA_RIGHT,
        spaceBefore=4 * mm,
    )

    styles["page_number"] = ParagraphStyle(
        "PageNumber",
        parent=base["Normal"],
        fontName=fonts.mincho,
        fontSize=SMALL_SIZE,
        alignment=TA_RIGHT,
    )

    styles["company_header"] = ParagraphStyle(
        "CompanyHeader",
        parent=base["Normal"],
        fontName=fonts.gothic,
        fontSize=BODY_SIZE,
        leading=BODY_SIZE * 1.6,
    )

    styles["cell_label"] = ParagraphStyle(
        "CVCellLabel",
        parent=base["Normal"],
        fontName=fonts.gothic,
        fontSize=TABLE_SIZE,
        leading=TABLE_SIZE * 1.6,
        textColor="black",
    )

    return styles
