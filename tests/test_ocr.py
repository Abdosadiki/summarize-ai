"""
Unit tests for OCR service (EasyOCR).

Run:
    cd Stage
    python -m pytest tests/test_ocr.py -v
"""

import io
import pytest
from PIL import Image, ImageDraw

from services.ocr_service import extract_text_from_image, OCRError, _preprocess_image


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

def _make_text_image(text: str, size=(400, 100), bg="white", fg="black") -> Image.Image:
    """Create a simple image with text drawn on it."""
    img = Image.new("RGB", size, color=bg)
    draw = ImageDraw.Draw(img)
    draw.text((10, 30), text, fill=fg)
    return img


def _image_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


# ──────────────────────────────────────────────
# Tests — _preprocess_image
# ──────────────────────────────────────────────

class TestPreprocess:
    def test_converts_rgba_to_grayscale(self):
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
        result = _preprocess_image(img)
        assert result.mode == "L"

    def test_resizes_large_image(self):
        img = Image.new("RGB", (8000, 6000), "white")
        result = _preprocess_image(img)
        assert max(result.size) <= 4000

    def test_keeps_small_image_size(self):
        img = Image.new("RGB", (200, 150), "white")
        result = _preprocess_image(img)
        assert result.size == (200, 150)

    def test_output_is_grayscale(self):
        img = Image.new("RGB", (100, 100), "blue")
        result = _preprocess_image(img)
        assert result.mode == "L"


# ──────────────────────────────────────────────
# Tests — extract_text_from_image
# ──────────────────────────────────────────────

class TestExtractText:
    def test_extract_from_pil_image(self):
        """Text drawn on a white image should return a string."""
        img = _make_text_image("Hello World", size=(600, 100))
        result = extract_text_from_image(img, langs=["en"])
        assert isinstance(result, str)

    def test_extract_from_bytes(self):
        img = _make_text_image("Test 12345", size=(600, 100))
        raw = _image_to_bytes(img)
        result = extract_text_from_image(raw, langs=["en"])
        assert isinstance(result, str)

    def test_extract_from_bytesio(self):
        img = _make_text_image("BytesIO test", size=(600, 100))
        buf = io.BytesIO(_image_to_bytes(img))
        result = extract_text_from_image(buf, langs=["en"])
        assert isinstance(result, str)

    def test_blank_image_returns_empty_or_minimal(self):
        """A blank image should return empty (or near-empty) text."""
        img = Image.new("RGB", (200, 200), "white")
        result = extract_text_from_image(img, langs=["en"])
        assert len(result.strip()) < 5

    def test_invalid_source_raises_ocr_error(self):
        with pytest.raises(OCRError, match="Unsupported source type"):
            extract_text_from_image(12345)  # type: ignore

    def test_invalid_bytes_raises_ocr_error(self):
        with pytest.raises(OCRError, match="Could not open image"):
            extract_text_from_image(b"not-an-image")


# ──────────────────────────────────────────────
# Tests — edge cases
# ──────────────────────────────────────────────

class TestEdgeCases:
    def test_very_small_image(self):
        """A 1x1 image should not crash."""
        img = Image.new("RGB", (1, 1), "white")
        result = extract_text_from_image(img, langs=["en"])
        assert isinstance(result, str)

    def test_palette_mode_image(self):
        """Palette mode (P) should be handled correctly."""
        img = Image.new("P", (200, 100))
        result = extract_text_from_image(img, langs=["en"])
        assert isinstance(result, str)
