"""PDF generation using ReportLab Platypus."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from jb_workhistory.fonts import register_fonts
from jb_workhistory.work_history.models import (
    SideCompany,
    SideProject,
    StandardCompany,
    StandardProject,
    StarCompany,
    StarProject,
    _CompanyBase,
    _ProjectBase,
    _WorkHistoryBase,
)
from jb_workhistory.work_history.styles import (
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    MARGIN_TOP,
    build_styles,
)

# Table column widths
CONTENT_WIDTH = 170 * mm  # total usable width

# For experience table: period | content | environment | team
COL_PERIOD = 18 * mm
COL_CONTENT = 117 * mm
COL_ENV = 21 * mm
COL_TEAM = 14 * mm

# For company info row: info | employment_type
COL_COMPANY_INFO = 135 * mm
COL_EMPLOYMENT = 35 * mm

# For skill table
COL_SKILL_CAT = 25 * mm
COL_SKILL_NAME = 45 * mm
COL_SKILL_PERIOD = 35 * mm
COL_SKILL_LEVEL = 65 * mm

# For qualification table
COL_QUAL_NAME = 110 * mm
COL_QUAL_DATE = 60 * mm

# Grid style constants
_GRID_STYLE = [
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
]


def _escape(text: str) -> str:
    """Escape text for ReportLab Paragraph XML."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _build_header(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build the header section: title, date, name."""
    elements = []
    elements.append(Paragraph("職 務 経 歴 書", styles["title"]))
    elements.append(Paragraph(_escape(data.date), styles["date"]))
    elements.append(Paragraph(_escape(data.name), styles["name"]))
    return elements


def _build_summary(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build 職務要約 section."""
    if not data.summary:
        return []
    elements = []
    elements.append(Paragraph("■職務要約", styles["section_header"]))
    text = _escape(data.summary.strip()).replace("\n", "<br/>")
    elements.append(Paragraph(text, styles["body"]))
    return elements


def _build_highlights(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build 活かせる経験・知識・技術 section."""
    if not data.highlights:
        return []
    elements = []
    elements.append(Paragraph("■活かせる経験・知識・技術", styles["section_header"]))
    for h in data.highlights:
        elements.append(Paragraph(f"・{_escape(h)}", styles["bullet"]))
    elements.append(Spacer(1, 2 * mm))
    return elements


def _build_env_cell(project: _ProjectBase, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Build the environment column content for a project row."""
    parts = []
    env = project.environment
    categories = [
        ("言語", env.languages),
        ("OS", env.os),
        ("DB", env.db),
        ("FW", env.frameworks),
        ("ツール", env.tools),
        ("その他", env.other),
    ]
    for label, items in categories:
        if items:
            parts.append(f"◆ {label}<br/>" + "<br/>".join(_escape(i) for i in items))
    return Paragraph("<br/>".join(parts), styles["cell"])


def _build_period_cell(project: _ProjectBase, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Build the period column for a project row.

    Splits on ～ into three lines: start / ～ / end.
    """
    text = _escape(project.period)
    if "～" in text:
        start, end = text.split("～", 1)
        text = f"{start}<br/>～<br/>{end}"
    return Paragraph(text, styles["cell"])


def _build_project_content(project: StandardProject, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Build the main content column for a standard project row."""
    parts = []

    # Industry / project name (period is now in separate column)
    header_parts = []
    if project.industry:
        header_parts.append(_escape(project.industry))
    header_parts.append(_escape(project.name))
    header_line = " / ".join(header_parts) if project.industry else _escape(project.name)
    parts.append(f"<b>{header_line}</b>")

    if project.overview:
        parts.append(f"◆ プロジェクト概要<br/>{_escape(project.overview.strip()).replace(chr(10), '<br/>')}")

    if project.phases:
        parts.append(f"◆ 担当フェーズ<br/>{_escape(project.phases)}")

    if project.responsibilities:
        items = "<br/>".join(f"・{_escape(r)}" for r in project.responsibilities)
        parts.append(f"◆ 業務内容<br/>{items}")

    if project.achievements:
        items = "<br/>".join(f"・{_escape(a)}" for a in project.achievements)
        parts.append(f"◆ 実績・取り組み<br/>{items}")

    return Paragraph("<br/><br/>".join(parts), styles["cell"])


def _build_project_content_star(project: StarProject, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Build the main content column for a STAR project row."""
    parts = []

    # Industry / project name
    header_parts = []
    if project.industry:
        header_parts.append(_escape(project.industry))
    header_parts.append(_escape(project.name))
    header_line = " / ".join(header_parts) if project.industry else _escape(project.name)
    parts.append(f"<b>{header_line}</b>")

    if project.situation:
        text = _escape(project.situation.strip()).replace(chr(10), "<br/>")
        parts.append(f"◆ 状況（Situation）<br/>{text}")

    if project.task:
        text = _escape(project.task.strip()).replace(chr(10), "<br/>")
        parts.append(f"◆ 課題（Task）<br/>{text}")

    if project.action:
        items = "<br/>".join(f"・{_escape(a)}" for a in project.action)
        parts.append(f"◆ 行動（Action）<br/>{items}")

    if project.result:
        items = "<br/>".join(f"・{_escape(r)}" for r in project.result)
        parts.append(f"◆ 結果（Result）<br/>{items}")

    return Paragraph("<br/><br/>".join(parts), styles["cell"])


def _build_team_cell(project: _ProjectBase, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Build the team size / role column."""
    parts = []
    if project.team_size:
        parts.append(_escape(project.team_size))
    if project.role:
        parts.append(_escape(project.role))
    return Paragraph("<br/>".join(parts), styles["cell"])


def _build_experience(
    data: _WorkHistoryBase,
    styles: dict[str, ParagraphStyle],
    content_format: str = "standard",
) -> list:
    """Build 職務経歴 section with company and project tables."""
    if not data.experience:
        return []
    elements = []
    elements.append(Paragraph("■職務経歴", styles["section_header"]))

    for company in data.experience:
        elements.extend(_build_company_table(company, styles, content_format))
        elements.append(Spacer(1, 3 * mm))

    return elements


def _build_company_table(
    company: _CompanyBase,
    styles: dict[str, ParagraphStyle],
    content_format: str = "standard",
) -> list:
    """Build a single company's table (header + info + projects)."""
    elements = []

    # Company header row: period + company name (full width)
    header_text = f"{_escape(company.period)}　{_escape(company.company)}"
    header_para = Paragraph(header_text, styles["company_header"])

    header_table = Table(
        [[header_para]],
        colWidths=[CONTENT_WIDTH],
    )
    header_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.92, 0.92, 0.92)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(header_table)

    # Company info row: details | employment type
    info_parts = []
    if company.business:
        info_parts.append(f"事業内容：{_escape(company.business)}")
    finance_parts = []
    if company.capital:
        finance_parts.append(f"資本金：{_escape(company.capital)}")
    if company.revenue:
        finance_parts.append(f"売上高：{_escape(company.revenue)}")
    if finance_parts:
        info_parts.append("　".join(finance_parts))
    size_parts = []
    if company.employees:
        size_parts.append(f"従業員数：{_escape(company.employees)}")
    if company.listing:
        size_parts.append(f"上場：{_escape(company.listing)}")
    if size_parts:
        info_parts.append("　".join(size_parts))

    info_text = "<br/>".join(info_parts)
    info_para = Paragraph(info_text, styles["cell"])
    emp_para = Paragraph(_escape(company.employment_type), styles["cell"])

    info_table = Table(
        [[info_para, emp_para]],
        colWidths=[COL_COMPANY_INFO, COL_EMPLOYMENT],
    )
    info_table.setStyle(TableStyle([
        *_GRID_STYLE,
    ]))
    elements.append(info_table)

    # Project rows
    if company.projects:
        # Column headers
        col_headers = [
            Paragraph("<b>期間</b>", styles["cell_gothic"]),
            Paragraph("<b>内容</b>", styles["cell_gothic"]),
            Paragraph("<b>開発環境</b>", styles["cell_gothic"]),
            Paragraph("<b>規模</b>", styles["cell_gothic"]),
        ]

        table_data = [col_headers]

        for project in company.projects:
            period_cell = _build_period_cell(project, styles)
            if content_format == "star":
                content_cell = _build_project_content_star(project, styles)
            else:
                content_cell = _build_project_content(project, styles)
            env_cell = _build_env_cell(project, styles)
            team_cell = _build_team_cell(project, styles)
            table_data.append([period_cell, content_cell, env_cell, team_cell])

        project_table = Table(
            table_data,
            colWidths=[COL_PERIOD, COL_CONTENT, COL_ENV, COL_TEAM],
        )
        project_style = TableStyle([
            *_GRID_STYLE,
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.95, 0.95, 0.95)),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ])
        project_table.setStyle(project_style)
        elements.append(project_table)

    return elements


def _build_side_project_content(
    project: SideProject,
    styles: dict[str, ParagraphStyle],
) -> Paragraph:
    """Build the content column for a side project row."""
    parts = []
    parts.append(f"<b>{_escape(project.name)}</b>")
    if project.description:
        text = _escape(project.description.strip()).replace(chr(10), "<br/>")
        parts.append(text)
    return Paragraph("<br/>".join(parts), styles["cell"])


def _build_side_experience(
    data: _WorkHistoryBase,
    styles: dict[str, ParagraphStyle],
) -> list:
    """Build 副業・その他経歴 section."""
    if not data.side_experience:
        return []
    elements = []
    elements.append(Paragraph("■副業・その他経歴", styles["section_header"]))

    for company in data.side_experience:
        # Company header row: period + company name (grey background)
        header_text = f"{_escape(company.period)}　{_escape(company.company)}"
        if company.employment_type:
            header_text += f"（{_escape(company.employment_type)}）"
        header_para = Paragraph(header_text, styles["company_header"])

        header_table = Table(
            [[header_para]],
            colWidths=[CONTENT_WIDTH],
        )
        header_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.92, 0.92, 0.92)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(header_table)

        # Project rows
        if company.projects:
            col_headers = [
                Paragraph("<b>期間</b>", styles["cell_gothic"]),
                Paragraph("<b>内容</b>", styles["cell_gothic"]),
                Paragraph("<b>開発環境</b>", styles["cell_gothic"]),
                Paragraph("<b>規模</b>", styles["cell_gothic"]),
            ]
            table_data = [col_headers]

            for project in company.projects:
                period_cell = Paragraph(
                    _escape(project.period).replace("～", "<br/>～<br/>"),
                    styles["cell"],
                )
                content_cell = _build_side_project_content(project, styles)
                env_cell = _build_env_cell(project, styles)
                team_cell = _build_team_cell(project, styles)
                table_data.append([period_cell, content_cell, env_cell, team_cell])

            project_table = Table(
                table_data,
                colWidths=[COL_PERIOD, COL_CONTENT, COL_ENV, COL_TEAM],
            )
            project_table.setStyle(TableStyle([
                *_GRID_STYLE,
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.95, 0.95, 0.95)),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ]))
            elements.append(project_table)

        elements.append(Spacer(1, 3 * mm))

    return elements


def _build_technical_skills(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build テクニカルスキル section."""
    if not data.technical_skills:
        return []
    elements = []
    elements.append(Paragraph("■テクニカルスキル", styles["section_header"]))

    # Header row
    table_data = [[
        Paragraph("<b>種類</b>", styles["cell_gothic"]),
        Paragraph("<b>名称</b>", styles["cell_gothic"]),
        Paragraph("<b>使用期間</b>", styles["cell_gothic"]),
        Paragraph("<b>レベル</b>", styles["cell_gothic"]),
    ]]

    span_commands = []
    row_idx = 1

    for cat in data.technical_skills:
        cat_start = row_idx
        for item in cat.items:
            table_data.append([
                Paragraph(_escape(cat.category), styles["cell_gothic"]),
                Paragraph(_escape(item.name), styles["cell"]),
                Paragraph(_escape(item.period), styles["cell"]),
                Paragraph(_escape(item.level), styles["cell"]),
            ])
            row_idx += 1

        if len(cat.items) > 1:
            span_commands.append(("SPAN", (0, cat_start), (0, row_idx - 1)))

    skill_table = Table(
        table_data,
        colWidths=[COL_SKILL_CAT, COL_SKILL_NAME, COL_SKILL_PERIOD, COL_SKILL_LEVEL],
    )
    skill_style = TableStyle([
        *_GRID_STYLE,
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.95, 0.95, 0.95)),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        *span_commands,
    ])
    skill_table.setStyle(skill_style)
    elements.append(skill_table)
    elements.append(Spacer(1, 2 * mm))

    return elements


def _build_qualifications(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build 資格 section."""
    if not data.qualifications:
        return []
    elements = []
    elements.append(Paragraph("■資格", styles["section_header"]))

    table_data = []
    for q in data.qualifications:
        table_data.append([
            Paragraph(_escape(q.name), styles["cell"]),
            Paragraph(_escape(q.date), styles["cell"]),
        ])

    qual_table = Table(
        table_data,
        colWidths=[COL_QUAL_NAME, COL_QUAL_DATE],
    )
    qual_table.setStyle(TableStyle(_GRID_STYLE))
    elements.append(qual_table)
    elements.append(Spacer(1, 2 * mm))

    return elements


def _build_self_pr(data: _WorkHistoryBase, styles: dict[str, ParagraphStyle]) -> list:
    """Build 自己PR section."""
    if not data.self_pr:
        return []
    elements = []
    elements.append(Paragraph("■自己PR", styles["section_header"]))

    for pr in data.self_pr:
        title_text = f"＜{_escape(pr.title)}＞"
        elements.append(Paragraph(title_text, styles["section_header"]))
        content = _escape(pr.content.strip()).replace("\n", "<br/>")
        elements.append(Paragraph(content, styles["body"]))

    return elements


class _PageNumCanvas:
    """Mixin to draw page numbers on each page."""

    def __init__(self, font_name: str):
        self.font_name = font_name

    def on_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font_name, 8)
        page_num = canvas.getPageNumber()
        text = f"{page_num} / {{total_pages}}"
        canvas.drawRightString(
            A4[0] - MARGIN_RIGHT,
            MARGIN_BOTTOM - 5 * mm,
            text,
        )
        canvas.restoreState()

    def on_page_final(self, canvas, doc):
        """Called after all pages are known, to fill in total pages."""
        canvas.saveState()
        canvas.setFont(self.font_name, 8)
        page_num = canvas.getPageNumber()
        total = doc.page
        text = f"{page_num} / {total}"
        canvas.drawRightString(
            A4[0] - MARGIN_RIGHT,
            MARGIN_BOTTOM - 5 * mm,
            text,
        )
        canvas.restoreState()


def _build_elements(
    data: _WorkHistoryBase,
    styles: dict[str, ParagraphStyle],
    content_format: str = "standard",
) -> list:
    """Build all flowable elements for the PDF."""
    elements = []
    elements.extend(_build_header(data, styles))
    elements.extend(_build_summary(data, styles))
    elements.extend(_build_highlights(data, styles))
    elements.extend(_build_experience(data, styles, content_format))
    elements.extend(_build_side_experience(data, styles))
    elements.extend(_build_technical_skills(data, styles))
    elements.extend(_build_qualifications(data, styles))
    elements.extend(_build_self_pr(data, styles))
    elements.append(Paragraph("以上", styles["right"]))
    return elements


def build_pdf(
    data: _WorkHistoryBase,
    output: str | Path,
    font_dir: str | Path | None = None,
    content_format: str = "standard",
) -> Path:
    """Generate the 職務経歴書 PDF.

    Args:
        data: Validated WorkHistory data.
        output: Output PDF file path.
        font_dir: Optional directory containing Japanese fonts.
        content_format: Project content format ("standard" or "star").

    Returns:
        Path to the generated PDF.
    """
    output = Path(output)
    fonts = register_fonts(font_dir)
    styles = build_styles(fonts)

    # Collect all flowable elements
    elements = _build_elements(data, styles, content_format)

    # Build the document with page numbers
    page_num_handler = _PageNumCanvas(fonts.mincho)

    frame = Frame(
        MARGIN_LEFT,
        MARGIN_BOTTOM,
        A4[0] - MARGIN_LEFT - MARGIN_RIGHT,
        A4[1] - MARGIN_TOP - MARGIN_BOTTOM,
        id="main",
    )

    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    page_template = PageTemplate(
        id="main",
        frames=[frame],
        onPage=page_num_handler.on_page,
    )
    doc.addPageTemplates([page_template])

    # First pass: build to get total pages
    doc.build(elements)

    # Now we know total pages, rebuild with correct page numbers
    total_pages = doc.page

    def on_page_with_total(canvas, doc):
        canvas.saveState()
        canvas.setFont(fonts.mincho, 8)
        page_num = canvas.getPageNumber()
        text = f"{page_num} / {total_pages}"
        canvas.drawRightString(
            A4[0] - MARGIN_RIGHT,
            MARGIN_BOTTOM - 5 * mm,
            text,
        )
        canvas.restoreState()

    doc2 = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    page_template2 = PageTemplate(
        id="main",
        frames=[Frame(
            MARGIN_LEFT,
            MARGIN_BOTTOM,
            A4[0] - MARGIN_LEFT - MARGIN_RIGHT,
            A4[1] - MARGIN_TOP - MARGIN_BOTTOM,
            id="main",
        )],
        onPage=on_page_with_total,
    )
    doc2.addPageTemplates([page_template2])

    # Rebuild elements (Platypus consumes them)
    elements2 = _build_elements(data, styles, content_format)

    doc2.build(elements2)

    return output
