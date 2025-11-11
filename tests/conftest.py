from __future__ import annotations
import os
from pathlib import Path
import pytest

# --- PDFs generieren ---------------------------------------------------------

@pytest.fixture
def make_blank_pdf(tmp_path):
    """Erzeuge ein PDF ohne Text (nur leere Seiten)."""
    try:
        from PyPDF2 import PdfMerger, PdfReader, PdfWriter
    except Exception:
        from PyPDF2 import PdfWriter  # fallback

    def _make(name="blank.pdf", pages=1):
        path = tmp_path / name
        w = PdfWriter()
        for _ in range(pages):
            w.add_blank_page(width=595, height=842)  # A4
        with open(path, "wb") as f:
            w.write(f)
        return str(path)

    return _make


@pytest.fixture
def make_text_pdf(tmp_path):
    """Erzeuge ein PDF mit einfachem Text (reportlab), damit read_pdf Text extrahieren kann."""
    reportlab = pytest.importorskip("reportlab", reason="reportlab required for text PDFs")
    from reportlab.pdfgen import canvas  # type: ignore

    def _make(name="text.pdf", base="Hello PDF", pages=2):
        path = tmp_path / name
        c = canvas.Canvas(str(path))
        for i in range(pages):
            c.drawString(72, 720, f"{base} (page {i+1})")
            c.showPage()
        c.save()
        return path

    return _make


# --- Helper-Patches ----------------------------------------------------------

@pytest.fixture
def patch_helper_noop(monkeypatch):
    """patcht helper.decrypt_pdf zu einem No-Op."""
    import core
    monkeypatch.setattr(core.helper, "decrypt_pdf", lambda reader, password: None, raising=True)


@pytest.fixture
def patch_helper_pages(monkeypatch):
    """
    Gibt eine Funktion zurück, um helper.cmd_str_pages_2_int_tuple zu patchen.
    Erwartet 0-basige, inklusive Ranges [(start, end), ...].
    """
    import core

    def _apply(ranges):
        monkeypatch.setattr(core.helper, "cmd_str_pages_2_int_tuple", lambda s: list(ranges), raising=True)

    return _apply
