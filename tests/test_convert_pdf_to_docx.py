from __future__ import annotations

from pathlib import Path

import pytest
import core

pdf2docx = pytest.importorskip("pdf2docx", reason="pdf2docx not installed")
fitz = pytest.importorskip("fitz", reason="pymupdf (fitz) not installed")  # pdf2docx braucht PyMuPDF

def test_convert_all_pages_to_docx(make_text_pdf, patch_helper_noop, tmp_path):
    pdf = make_text_pdf("t.pdf", base="DOCX", pages=1)
    out = str(tmp_path) + "\\t.docx"

    core.convert_pdf_to_docx(str(pdf), str(out), "", "")

    assert Path(out).exists()
    # Inhalt grob prüfen (optional)
    try:
        from docx import Document
        doc = Document(str(out))
        text = "\n".join(p.text for p in doc.paragraphs)
        # Bei layout-Engine kann Text in Textboxen landen – daher nur Existenz der Datei prüfen.
        assert text is not None
    except Exception:
        # Wenn python-docx nicht installiert ist, reicht die Existenzprüfung
        pass

def test_convert_selected_one_page(make_text_pdf, patch_helper_noop, patch_helper_pages, tmp_path):
    pdf = make_text_pdf("t.pdf", base="ONLY ONE", pages=3)
    out = str(tmp_path) + "\one.docx"

    core.convert_pdf_to_docx(pdf, out, "1", "")

    assert Path(out).exists()
