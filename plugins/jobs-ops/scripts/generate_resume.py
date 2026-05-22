#!/usr/bin/env python3
"""
Generate a single-page ATS-optimized PDF resume.

Usage:
    python3 scripts/generate_resume.py <html_data_json> <output_pdf_path> [--format=letter|a4]

The html_data_json is a path to a JSON file with all resume content sections.
See modes/resume.md for the content schema Claude must produce before calling this script.
"""

import os
import sys
import subprocess
import json
import argparse

# -- Venv bootstrap (never pollute system Python) --------------------------------
if not os.environ.get("VIRTUAL_ENV"):
    venv_path = os.path.join(os.getcwd(), ".venv")
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    python = os.path.join(venv_path, "bin", "python")
    os.execv(python, [python] + sys.argv)

for pkg in ["reportlab", "pypdf"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

# -- Imports after bootstrap -----------------------------------------------------
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, pt
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from pypdf import PdfReader

# -- Colours ---------------------------------------------------------------------
ACCENT_CYAN   = colors.HexColor("#1a7f8f")
ACCENT_PURPLE = colors.HexColor("#6b3fa0")
LIGHT_GRAY    = colors.HexColor("#cccccc")
BLACK         = colors.black

# -- Page constants --------------------------------------------------------------
PAGE_SIZES = {"letter": letter, "a4": A4}
SIDE_MARGIN   = 0.5 * inch
TOP_MARGIN    = 0.4 * inch
BOTTOM_MARGIN = 0.4 * inch


def build_styles(body_size=9.2, header_size=10.5, contact_size=9.0):
    """Return a dict of ParagraphStyles at the given font sizes."""
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "name":    S("name",    fontName="Helvetica-Bold", fontSize=18,          leading=22,          alignment=TA_CENTER, textColor=BLACK),
        "contact": S("contact", fontName="Helvetica",      fontSize=contact_size, leading=contact_size+2, alignment=TA_CENTER, textColor=BLACK),
        "section": S("section", fontName="Helvetica-Bold", fontSize=header_size,  leading=header_size+2, textColor=ACCENT_CYAN, spaceAfter=1),
        "job_co":  S("job_co",  fontName="Helvetica-Bold", fontSize=body_size,    leading=body_size+2,  textColor=ACCENT_PURPLE),
        "job_ttl": S("job_ttl", fontName="Helvetica",      fontSize=body_size,    leading=body_size+2),
        "bullet":  S("bullet",  fontName="Helvetica",      fontSize=body_size,    leading=body_size+2.3, leftIndent=10, spaceAfter=1.5, bulletIndent=0),
        "tech":    S("tech",    fontName="Helvetica-Bold", fontSize=body_size-0.7, leading=body_size+1, spaceAfter=1.5),
        "skill":   S("skill",   fontName="Helvetica",      fontSize=body_size,    leading=body_size+2,  spaceAfter=1.5),
    }


def section_header(title, styles):
    """Return flowables for a section header with HR divider."""
    return [
        Paragraph(title.upper(), styles["section"]),
        HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=3),
    ]


def date_row(left_text, right_text, styles, col_split=0.78):
    """Return a Table with left-aligned institution/company and right-aligned date."""
    page_width = 540  # points, fixed for both letter and a4 after margins
    left_w  = page_width * col_split
    right_w = page_width * (1 - col_split)
    right_style = ParagraphStyle(
        "date_right", fontName="Helvetica", fontSize=9.0, leading=11,
        alignment=TA_RIGHT, textColor=BLACK
    )
    t = Table(
        [[Paragraph(left_text, styles["job_co"]), Paragraph(right_text, right_style)]],
        colWidths=[left_w, right_w],
        hAlign="LEFT",
    )
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0)]))
    return t


def build_story(data: dict, styles: dict, section_space_before: int = 8) -> list:
    """Build the full list of flowables from resume data."""
    story = []

    # -- Header ------------------------------------------------------------------
    story.append(Paragraph(data["name"], styles["name"]))
    story.append(Spacer(1, 8))                          # MANDATORY: prevents overlap
    story.append(Paragraph(data["contact"], styles["contact"]))
    story.append(Spacer(1, 4))                          # MANDATORY
    story.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT_CYAN))
    story.append(Spacer(1, 6))                          # MANDATORY: before first section

    # -- Professional Summary ----------------------------------------------------
    story += section_header("Professional Summary", styles)
    story.append(Paragraph(data["summary"], styles["bullet"]))
    story.append(Spacer(1, section_space_before))

    # -- Education ---------------------------------------------------------------
    story += section_header("Education", styles)
    for edu in data["education"]:
        story.append(date_row(
            f'<b>{edu["school"]}</b> - {edu["degree"]}',
            edu["dates"], styles
        ))
        if edu.get("gpa"):
            story.append(Paragraph(f'GPA: {edu["gpa"]}', styles["job_ttl"]))
        if edu.get("coursework"):
            story.append(Paragraph(f'Coursework: {edu["coursework"]}', styles["skill"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, section_space_before - 3))

    # -- Work Experience ---------------------------------------------------------
    story += section_header("Work Experience", styles)
    for job in data["experience"]:
        story.append(Spacer(1, 5))
        story.append(date_row(
            f'<b><font color="#{ACCENT_PURPLE.hexval()[2:]}">  {job["company"]}</font></b>',
            job["dates"], styles
        ))
        story.append(Paragraph(job["title"], styles["job_ttl"]))
        for bullet in job["bullets"]:
            story.append(Paragraph(f"• {bullet}", styles["bullet"]))
    story.append(Spacer(1, section_space_before))

    # -- Projects ----------------------------------------------------------------
    story += section_header("Projects", styles)
    for proj in data["projects"]:
        story.append(Spacer(1, 5))
        story.append(Paragraph(f'<b>{proj["name"]}</b>', styles["job_co"]))
        story.append(Paragraph(f'Technologies: {proj["tech"]}', styles["tech"]))
        for bullet in proj["bullets"]:
            story.append(Paragraph(f"• {bullet}", styles["bullet"]))
    story.append(Spacer(1, section_space_before))

    # -- Technical Skills --------------------------------------------------------
    story += section_header("Technical Skills", styles)
    for skill_line in data["skills"]:
        story.append(Paragraph(
            f'<b>{skill_line["category"]}:</b> {skill_line["items"]}',
            styles["skill"]
        ))

    return story


def measure_height(story, page_width, available_height):
    """Rough height measurement: sum leading * line_count for each flowable."""
    total = 0
    for item in story:
        w, h = item.wrap(page_width, available_height)
        total += h
    return total


def generate(data_path: str, output_path: str, page_format: str = "letter"):
    with open(data_path) as f:
        data = json.load(f)

    page_size    = PAGE_SIZES.get(page_format, letter)
    page_width   = page_size[0] - 2 * SIDE_MARGIN
    page_height  = page_size[1]
    avail_height = page_height - TOP_MARGIN - BOTTOM_MARGIN

    # -- Pass 1: measure at default sizes ----------------------------------------
    styles = build_styles()
    story  = build_story(data, styles)
    total_h = measure_height(story, page_width, avail_height)

    section_space_before = 8
    body_size   = 9.2
    header_size = 10.5
    contact_size = 9.0

    if total_h > avail_height:
        # Scale down proportionally
        ratio = (avail_height / total_h) * 0.97
        body_size    = max(8.8, body_size * ratio)
        header_size  = max(10.0, header_size * ratio)
        contact_size = max(8.5, contact_size * ratio)
        styles  = build_styles(body_size, header_size, contact_size)
        story   = build_story(data, styles)
        total_h = measure_height(story, page_width, avail_height)
    elif (avail_height - total_h) > avail_height * 0.12:
        # Distribute extra space into section gaps
        slack  = avail_height - total_h
        # Count how many section gaps there are (rough: number of sections)
        n_gaps = len(data["experience"]) + len(data["projects"]) + 3
        section_space_before = int(8 + slack / max(n_gaps, 1))
        section_space_before = min(section_space_before, 20)
        styles = build_styles(body_size, header_size, contact_size)
        story  = build_story(data, styles, section_space_before)

    # -- Pass 2: build final PDF -------------------------------------------------
    doc = SimpleDocTemplate(
        output_path,
        pagesize=page_size,
        leftMargin=SIDE_MARGIN, rightMargin=SIDE_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    )
    doc.build(story)

    # -- Verify page count (informational, no regeneration) ----------------------
    reader = PdfReader(output_path)
    n_pages = len(reader.pages)
    if n_pages != 1:
        print(f"WARNING: PDF is {n_pages} pages (expected 1). Review font sizes.", file=sys.stderr)
    else:
        print(f"OK: 1-page PDF written to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_json",   help="Path to resume content JSON file")
    parser.add_argument("output_pdf",  help="Output PDF path")
    parser.add_argument("--format",    default="letter", choices=["letter", "a4"])
    args = parser.parse_args()
    generate(args.data_json, args.output_pdf, args.format)
