"""utils/report_gen.py — ReportLab PDF report for a SignLang AI session."""

import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ── Color palette matching the UI ─────────────────────────────
NAVY      = colors.HexColor("#0D1117")
PURPLE    = colors.HexColor("#7C3AED")
PURPLE_LT = colors.HexColor("#EDE9FE")
TEAL      = colors.HexColor("#0F6E56")
TEAL_LT   = colors.HexColor("#CCFBF1")
GRAY_LT   = colors.HexColor("#F8FAFC")
GRAY      = colors.HexColor("#94A3B8")
WHITE     = colors.white


def generate_pdf(user_name: str, user_email: str, session_data: dict) -> str:
    """
    Generate a PDF session report.
    Returns the path to the generated PDF file.
    """
    path = os.path.join(tempfile.gettempdir(), f"signlang_report_{abs(hash(user_email + str(datetime.now())))}.pdf")
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    story  = []

    # ── Header bar ────────────────────────────────────────────
    header_data = [["SignLang AI — Session Report"]]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 18),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Subtitle ──────────────────────────────────────────────
    sub_style = ParagraphStyle("sub", fontSize=10, textColor=GRAY,
                               alignment=TA_CENTER, spaceAfter=12)
    story.append(Paragraph("Real-Time Indian Sign Language Recognition — Session Summary", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=16))

    # ── User + Session info ───────────────────────────────────
    label_style = ParagraphStyle("label", fontSize=10, textColor=TEAL,
                                 fontName="Helvetica-Bold")
    val_style   = ParagraphStyle("val",   fontSize=10, textColor=NAVY)

    info_data = [
        [Paragraph("Name", label_style),       Paragraph(user_name, val_style),
         Paragraph("Date", label_style),        Paragraph(str(session_data.get("date", "—")), val_style)],
        [Paragraph("Email", label_style),      Paragraph(user_email, val_style),
         Paragraph("Time", label_style),        Paragraph(str(session_data.get("time", "—")), val_style)],
        [Paragraph("Words recognized", label_style), Paragraph(str(session_data.get("word_count", "0")), val_style),
         Paragraph("Report generated", label_style), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"), val_style)],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GRAY_LT),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [GRAY_LT, WHITE]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    # ── Full sentence ─────────────────────────────────────────
    sent_label = ParagraphStyle("sl", fontSize=11, textColor=NAVY,
                                fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)
    sent_body  = ParagraphStyle("sb", fontSize=12, textColor=PURPLE,
                                fontName="Helvetica-Bold", spaceAfter=12,
                                backColor=PURPLE_LT, borderPad=8)
    story.append(Paragraph("Full Sentence Recognized", sent_label))
    sentence = session_data.get("sentence") or session_data.get("words") or "—"
    story.append(Paragraph(sentence, sent_body))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=12))

    # ── Words table ───────────────────────────────────────────
    story.append(Paragraph("Words Recognized in This Session", sent_label))
    story.append(Spacer(1, 0.2*cm))

    words_raw = session_data.get("words", "")
    words     = [w.strip() for w in words_raw.split(",") if w.strip()] if words_raw else []

    if words:
        col_count = 4
        rows_data = [["#", "Word", "#", "Word"]]
        for i in range(0, len(words), 2):
            row = [str(i + 1), words[i]]
            if i + 1 < len(words):
                row += [str(i + 2), words[i + 1]]
            else:
                row += ["", ""]
            rows_data.append(row)

        words_table = Table(rows_data, colWidths=[1.5*cm, 7*cm, 1.5*cm, 7*cm])
        words_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0),  10),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GRAY_LT]),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
            ("ALIGN",         (2, 0), (2, -1),  "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ]))
        story.append(words_table)
    else:
        story.append(Paragraph("No words recorded in this session.", val_style))

    story.append(Spacer(1, 1*cm))

    # ── Footer ────────────────────────────────────────────────
    footer_style = ParagraphStyle("footer", fontSize=8, textColor=GRAY,
                                  alignment=TA_CENTER)
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY, spaceAfter=8))
    story.append(Paragraph(
        f"SignLang AI — Indian Sign Language Recognition | Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | NIELIT IIT Ropar — 2026",
        footer_style
    ))

    doc.build(story)
    return path
