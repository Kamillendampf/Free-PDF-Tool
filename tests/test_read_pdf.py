from __future__ import annotations
import pytest
import core



def test_read_all_pages(make_text_pdf, patch_helper_noop):
    pdf = make_text_pdf("t.pdf", base="Hallo Welt", pages=2)
    text = core.read_pdf(str(pdf), raw_selected_pages=None, password=None)
    assert "Hallo Welt (page 1)" in text
    assert "Hallo Welt (page 2)" in text

def test_read_selected_range(make_text_pdf, patch_helper_noop, patch_helper_pages):
    pdf = make_text_pdf("t.pdf", base="RANGE", pages=3)
    # Wir simulieren: "2-3" -> [(1, 2)] als 0-basiger inkl. Bereich
    patch_helper_pages(ranges=[(1, 2)])
    text = core.read_pdf(str(pdf), raw_selected_pages="2-3", password=None)
    assert "RANGE (page 1)" not in text
    assert "RANGE (page 2)" in text and "RANGE (page 3)" in text

def test_read_invalid_range_raises(make_text_pdf, patch_helper_noop, patch_helper_pages):
    pdf = make_text_pdf("t.pdf", base="X", pages=2)
    # Ungültig: verweist auf Seite 5 (index 4)
    patch_helper_pages(ranges=[(4, 4)])
    with pytest.raises(ValueError, match="Invalide PDF pages"):
        core.read_pdf(str(pdf), raw_selected_pages="5", password=None)
