"""PDF generation for 履歴書 (JIS standard resume) using ReportLab Canvas API.

Layout based on yaml_cv (https://github.com/kaityo256/yaml_cv) style.txt.
A4 page, coordinate system: origin at bottom-left, units in mm.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as canvas_module

from jp_tenshoku_docs_builder.fonts import FontConfig, register_fonts
from jp_tenshoku_docs_builder.resume.models import HistoryEntry, Resume

# A4 dimensions in mm
_PW = 210  # page width
_PH = 297  # page height
_MX = 16   # left margin x
_MY = 20   # bottom margin y (for content area origin offset)

# Content area width/height (matching yaml_cv: 177mm usable)
_CW = 177  # content width

# Font sizes
_FS_TITLE = 14
_FS_LARGE = 12
_FS_NORMAL = 9
_FS_SMALL = 8

# Row height for history tables
_ROW_H = 7


def _x(v: float) -> float:
    """Convert content-relative x (mm) to absolute page x (points)."""
    return (_MX + v) * mm


def _y(v: float) -> float:
    """Convert content-relative y (mm) to absolute page y (points)."""
    return v * mm


def _draw_string(c: canvas_module.Canvas, x_mm: float, y_mm: float, text: str,
                 font_size: float = _FS_NORMAL, font_name: str | None = None) -> None:
    """Draw a string at content-relative coordinates."""
    if font_name:
        c.setFont(font_name, font_size)
    else:
        c.setFontSize(font_size)
    c.drawString(_x(x_mm), _y(y_mm), text)


def _draw_line(c: canvas_module.Canvas, x1: float, y1: float, x2: float, y2: float,
               dashed: bool = False, line_width: float = 0.5) -> None:
    """Draw a line at content-relative coordinates."""
    c.setLineWidth(line_width)
    if dashed:
        c.setDash(3, 3)
    else:
        c.setDash()
    c.line(_x(x1), _y(y1), _x(x2), _y(y2))


def _draw_box(c: canvas_module.Canvas, x: float, y: float, w: float, h: float,
              line_width: float = 0.5) -> None:
    """Draw a rectangle. (x, y) is bottom-left corner."""
    c.setLineWidth(line_width)
    c.setDash()
    c.rect(_x(x), _y(y), w * mm, h * mm)


def _draw_textbox(c: canvas_module.Canvas, x: float, y: float, w: float, h: float,
                  text: str, font_size: float = _FS_LARGE, font_name: str | None = None) -> None:
    """Draw multi-line text within a box area (top-down)."""
    if font_name:
        c.setFont(font_name, font_size)
    else:
        c.setFontSize(font_size)
    leading = font_size * 1.5
    lines = text.strip().split("\n")
    cur_y = y
    for line in lines:
        if cur_y < (y - h):
            break
        c.drawString(_x(x), _y(cur_y), line.strip())
        cur_y -= leading / mm


def _draw_history_rows(c: canvas_module.Canvas, entries: list[HistoryEntry],
                       start_y: float, max_rows: int, row_h: float,
                       year_center_x: float, month_center_x: float, value_x: float,
                       font_size: float = _FS_LARGE,
                       font_name: str | None = None) -> None:
    """Draw history entries (year/month/value) in table rows.

    year_center_x / month_center_x are column center positions for centered text.
    """
    if font_name:
        c.setFont(font_name, font_size)
    else:
        c.setFontSize(font_size)
    for i, entry in enumerate(entries[:max_rows]):
        y = start_y - i * row_h
        if entry.year:
            c.drawCentredString(_x(year_center_x), _y(y), str(entry.year))
        if entry.month:
            c.drawCentredString(_x(month_center_x), _y(y), str(entry.month))
        c.drawString(_x(value_x), _y(y), entry.value)


def _draw_page1(c: canvas_module.Canvas, data: Resume, fonts: FontConfig) -> None:
    """Draw page 1: header, personal info, address, education/experience table."""

    # ── ヘッダー ──
    c.setFont(fonts.gothic, _FS_TITLE)
    c.drawString(_x(5), _y(247), "履　歴　書")
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(110), _y(245), data.date)

    # ── 写真エリア ──
    c.setDash(3, 3)
    c.setLineWidth(0.5)
    c.rect(_x(145), _y(204), 30 * mm, 40 * mm)
    c.setDash()
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(148), _y(240), "写真を貼る位置")
    c.setFontSize(_FS_SMALL)
    c.drawString(_x(147), _y(233), "1. 縦36〜40 mm")
    c.drawString(_x(150), _y(230), "横24〜30 mm")
    c.drawString(_x(147), _y(227), "2. 本人単身胸から上")
    c.drawString(_x(147), _y(224), "3. 裏面にのりづけ")
    c.drawString(_x(147), _y(221), "4. 裏面に氏名記入")

    # Insert photo if specified
    if data.photo:
        photo_path = Path(data.photo)
        if photo_path.exists():
            c.drawImage(str(photo_path), _x(145), _y(204), 30 * mm, 40 * mm,
                        preserveAspectRatio=True)

    # ── 外枠 (L字型フレーム) ──
    # 氏名エリア(139mm幅) + 住所エリア(177mm幅) を一体の枠で描画
    c.setLineWidth(2.0)
    c.setDash()
    p = c.beginPath()
    p.moveTo(_x(0), _y(240))
    p.lineTo(_x(139), _y(240))
    p.lineTo(_x(139), _y(199))
    p.lineTo(_x(_CW), _y(199))
    p.lineTo(_x(_CW), _y(146))
    p.lineTo(_x(0), _y(146))
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(0.5)

    # ── 氏名エリア内部線 ──
    _draw_line(c, 0, 233, 139, 233, dashed=True)   # ふりがな区切り
    _draw_line(c, 0, 218, 139, 218)                 # 氏名/生年月日
    _draw_line(c, 0, 205, 139, 205)                 # 生年月日/電話
    _draw_line(c, 0, 199, 139, 199)                 # 電話/住所 (内部区切り)

    # 生年月日エリア縦線
    _draw_line(c, 15, 218, 15, 205)
    _draw_line(c, 110, 218, 110, 205)

    # 携帯電話・E-MAIL エリア縦線
    _draw_line(c, 23, 205, 23, 199, dashed=True)
    _draw_line(c, 56, 205, 56, 199)
    _draw_line(c, 71, 205, 71, 199, dashed=True)

    # ── 住所エリア内部線 ──
    _draw_line(c, 0, 192, 139, 192, dashed=True)   # 現住所ふりがな
    _draw_line(c, 0, 173, _CW, 173)                 # 現住所/連絡先
    _draw_line(c, 0, 166, 139, 166, dashed=True)   # 連絡先ふりがな

    # 電話FAX列
    _draw_line(c, 139, 199, 139, 146)               # 左境界(縦)
    _draw_line(c, 139, 186, _CW, 186, dashed=True)  # 現住所 TEL/FAX
    _draw_line(c, 139, 160, _CW, 160, dashed=True)  # 連絡先 TEL/FAX

    # ── テキスト: ふりがな・氏名 ──
    # ふりがな row: y=240〜233 (7mm), vertically centered
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(235), "ふりがな")
    c.drawString(_x(30), _y(235), data.name_kana)
    c.drawString(_x(2), _y(228), "氏　　名")
    # 氏名データ: 行 y=233〜218 (15mm), 14ptフォントで垂直中央
    c.setFont(fonts.mincho, _FS_TITLE)
    c.drawString(_x(30), _y(224), data.name)

    # ── テキスト: 生年月日・性別 ──
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(1.5), _y(210), "生年月日")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(30), _y(210), data.birth_day)
    c.drawString(_x(121), _y(210), data.gender)

    # ── テキスト: 携帯電話・E-MAIL ──
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawCentredString(_x(11.5), _y(201), "携帯電話番号")
    c.drawString(_x(25), _y(201), data.cell_phone)
    c.drawCentredString(_x(63.5), _y(201), "E-MAIL")
    c.drawString(_x(75), _y(201), data.email)

    # ── テキスト: 現住所 ──
    # ふりがな row: y=199〜192 (7mm), vertically centered
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(194), "ふりがな")
    c.drawString(_x(20), _y(194), data.address_kana)
    c.drawString(_x(2), _y(188), "現住所 〒")
    c.drawString(_x(16), _y(188), data.address_zip)
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(15), _y(182), data.address)

    # ── テキスト: 連絡先 ──
    # ふりがな row: y=173〜166 (7mm), vertically centered
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(168), "ふりがな")
    c.drawString(_x(20), _y(168), data.address_kana2)
    c.drawString(_x(2), _y(162), "連絡先 〒")
    c.drawString(_x(16), _y(162), data.address_zip2)
    c.setFont(fonts.mincho, _FS_SMALL)
    c.drawRightString(_x(137), _y(162), "（現住所以外に連絡を希望する場合のみ記入）")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(15), _y(156), data.address2)

    # ── テキスト: 電話・FAX（右側） ──
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(141), _y(195), "電話")
    c.drawString(_x(143), _y(190), data.tel)
    c.drawString(_x(141), _y(182), "FAX")
    c.drawString(_x(143), _y(177), data.fax)
    c.drawString(_x(141), _y(169), "電話")
    c.drawString(_x(143), _y(164), data.tel2)
    c.drawString(_x(141), _y(156), "FAX")
    c.drawString(_x(143), _y(151), data.fax2)

    # ── 学歴・職歴テーブル ──
    table_top = 136
    table_bottom = 17
    table_h = table_top - table_bottom  # 119mm
    num_rows = 16

    _draw_box(c, 0, table_bottom, _CW, table_h, line_width=2.0)

    # Vertical lines: year | month | content
    _draw_line(c, 19, table_top, 19, table_bottom)
    _draw_line(c, 31, table_top, 31, table_bottom)

    # Horizontal row lines
    for i in range(num_rows + 1):
        y = table_top - i * _ROW_H
        if i == 0:
            continue  # top border already drawn
        _draw_line(c, 0, y, _CW, y)

    # Column headers (center-aligned, vertically centered in 7mm row)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawCentredString(_x(9.5), _y(table_top - 5), "年")
    c.drawCentredString(_x(25), _y(table_top - 5), "月")
    c.drawString(_x(77), _y(table_top - 5), "学歴・職歴（各項目ごとにまとめて書く）")

    # Merge education + experience with section headers
    entries: list[HistoryEntry] = []
    # 「学歴」header
    entries.append(HistoryEntry(value="学　歴"))
    entries.extend(data.education)
    # 「職歴」header
    entries.append(HistoryEntry(value="職　歴"))
    entries.extend(data.experience)

    row_start_y = table_top - _ROW_H - 5  # first data row (font_size=12: ascent ~3.5mm)
    _draw_history_rows(c, entries, row_start_y, num_rows - 1,
                       _ROW_H, 9.5, 25, 35,
                       font_size=_FS_LARGE, font_name=fonts.mincho)

    # Footer note (テーブル下端 y=17 から少しマージンを空ける)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(1), _y(12), "記入上の注意")
    c.drawString(_x(22), _y(12), "数字はアラビア数字で、文字はくずさず正確に書く。")


def _draw_page2(c: canvas_module.Canvas, data: Resume, fonts: FontConfig) -> None:
    """Draw page 2: licences, commuting/dependents, hobby, motivation, request."""

    # ── 免許・資格テーブル ──
    table_top = 239
    table_bottom = 190
    table_h = table_top - table_bottom  # 49mm
    num_rows = 6

    _draw_box(c, 0, table_bottom, _CW, table_h, line_width=2.0)

    # Vertical lines
    _draw_line(c, 19, table_top, 19, table_bottom)
    _draw_line(c, 31, table_top, 31, table_bottom)

    # Horizontal row lines
    for i in range(num_rows + 1):
        y = table_top - i * _ROW_H
        if i == 0:
            continue
        _draw_line(c, 0, y, _CW, y)

    # Headers (center-aligned, vertically centered in 7mm row)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawCentredString(_x(9.5), _y(table_top - 5), "年")
    c.drawCentredString(_x(25), _y(table_top - 5), "月")
    c.drawString(_x(90), _y(table_top - 5), "免許・資格")

    # Licence entries
    row_start_y = table_top - _ROW_H - 5
    _draw_history_rows(c, data.licences, row_start_y, num_rows - 1,
                       _ROW_H, 9.5, 25, 35,
                       font_size=_FS_LARGE, font_name=fonts.mincho)

    # ── 通勤時間・扶養家族・配偶者 ──
    box_top = 182
    box_bottom = 167
    box_h = box_top - box_bottom  # 15mm

    _draw_box(c, 0, box_bottom, _CW, box_h, line_width=2.0)
    _draw_line(c, 57, box_bottom, 57, box_top)
    _draw_line(c, 97, box_bottom, 97, box_top)
    _draw_line(c, 137, box_bottom, 137, box_top)

    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(178), "通勤時間")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(5), _y(171), data.commuting_time)

    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(59), _y(178), "扶養家族")
    c.drawString(_x(59), _y(171), "(配偶者を除く)")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(85), _y(171), data.dependents)

    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(99), _y(178), "配偶者")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(116), _y(171), data.spouse)

    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(139), _y(178), "配偶者の扶養義務")
    c.setFont(fonts.mincho, _FS_LARGE)
    c.drawString(_x(155), _y(171), data.supporting_spouse)

    # ── 趣味・特技 ── (box: y=120 to 160)
    _draw_box(c, 0, 120, _CW, 40, line_width=2.0)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(156), "趣味・特技")
    _draw_textbox(c, 2, 150, 173, 28, data.hobby,
                  font_size=_FS_LARGE, font_name=fonts.mincho)

    # ── 志望動機 ── (box: y=73 to 113)
    _draw_box(c, 0, 73, _CW, 40, line_width=2.0)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(109), "志望動機")
    _draw_textbox(c, 2, 103, 173, 28, data.motivation,
                  font_size=_FS_LARGE, font_name=fonts.mincho)

    # ── 本人希望記入欄 ── (box: y=26 to 66)
    _draw_box(c, 0, 26, _CW, 40, line_width=2.0)
    c.setFont(fonts.mincho, _FS_NORMAL)
    c.drawString(_x(2), _y(62), "本人希望記入欄")
    _draw_textbox(c, 2, 56, 173, 28, data.request,
                  font_size=_FS_LARGE, font_name=fonts.mincho)


def build_resume_pdf(
    data: Resume,
    output: str | Path,
    font_dir: str | Path | None = None,
) -> Path:
    """Generate the 履歴書 PDF.

    Args:
        data: Validated Resume data.
        output: Output PDF file path.
        font_dir: Optional directory containing Japanese fonts.

    Returns:
        Path to the generated PDF.
    """
    output = Path(output)
    fonts = register_fonts(font_dir)

    c = canvas_module.Canvas(str(output), pagesize=A4)

    # Page 1
    _draw_page1(c, data, fonts)
    c.showPage()

    # Page 2
    _draw_page2(c, data, fonts)
    c.showPage()

    c.save()
    return output
