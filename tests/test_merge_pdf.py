# tests/test_merge_pdf.py
from __future__ import annotations
from pathlib import Path
import os
import pytest
import core

def _page_count(pdf_path: str | os.PathLike) -> int:
    try:
        from PyPDF2 import PdfMerger, PdfReader
    except Exception:
        from PyPDF2 import PdfReader  # fallback
    r = PdfReader(str(pdf_path))
    return len(r.pages)

def test_merge_happy_path(make_blank_pdf, tmp_path):
    a = make_blank_pdf("a.pdf", pages=2)
    b = make_blank_pdf("b.pdf", pages=3)
    out = str(tmp_path) +"\merged.pdf"


    print("\n Pfad datei out: " + out)
    core.merge_pdf(out , [a, b])

    assert Path(out).exists()
    assert _page_count(out) == 5

def test_merge_empty_inputs_raises(tmp_path):
    out = tmp_path / "out.pdf"
    with pytest.raises(ValueError, match="Input paths cannot be empty"):
        core.merge_pdf(str(out), [])

def test_merge_missing_file_raises(tmp_path):
    out = tmp_path / "out.pdf"
    with pytest.raises(FileNotFoundError):
        core.merge_pdf(str(out), ["does-not-exist.pdf"])

def test_merge_output_same_as_input_raises(make_blank_pdf):
    a = make_blank_pdf("a.pdf", pages=1)
    # abs paths vergleichen (Funktion macht das auch)
    with pytest.raises(ValueError, match="Output paths cannot be the same as input"):
        core.merge_pdf(str(a), [str(a)])
