from docx import Document
from fpdf import FPDF
import os
from config import EXPORT_DIR


def _clean(text: str) -> str:
    return text.encode("latin-1", "replace").decode("latin-1")


def export_txt(title, transcript, summary):
    path = os.path.join(EXPORT_DIR, f"{title}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n")
        f.write("=== SUMMARY ===\n")
        f.write(summary.get("executive_summary", "") + "\n\n")
        f.write("=== ACTION ITEMS ===\n")
        for item in summary.get("action_items", []):
            f.write(f"- {item.get('task')} (Owner: {item.get('owner')})\n")
        f.write("\n=== FULL TRANSCRIPT ===\n")
        f.write(transcript)
    return path


def export_docx(title, transcript, summary):
    path = os.path.join(EXPORT_DIR, f"{title}.docx")
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_heading("Executive Summary", level=2)
    doc.add_paragraph(summary.get("executive_summary", ""))
    doc.add_heading("Key Highlights", level=2)
    for h in summary.get("key_highlights", []):
        doc.add_paragraph(h, style="List Bullet")
    doc.add_heading("Action Items", level=2)
    for item in summary.get("action_items", []):
        doc.add_paragraph(f"{item.get('task')} — Owner: {item.get('owner')}", style="List Bullet")
    doc.add_heading("Full Transcript", level=2)
    doc.add_paragraph(transcript)
    doc.save(path)
    return path


def export_pdf(title, transcript, summary):
    path = os.path.join(EXPORT_DIR, f"{title}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, _clean(title))
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 8, "Executive Summary")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, _clean(summary.get("executive_summary", "")))
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 8, "Action Items")
    pdf.set_font("Helvetica", "", 11)
    for item in summary.get("action_items", []):
        pdf.multi_cell(0, 6, _clean(f"- {item.get('task')} (Owner: {item.get('owner')})"))
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 8, "Full Transcript")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, _clean(transcript))
    pdf.output(path)
    return path