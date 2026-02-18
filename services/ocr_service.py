"""
OCR Service — Extracts text from images using EasyOCR (pure Python, no system dependency).

Usage:
    from services.ocr_service import extract_text_from_image
    text = extract_text_from_image(uploaded_file_bytes)

Requirements:
    pip install easyocr Pillow
"""

from __future__ import annotations

import io
import logging
from typing import Union

import numpy as np
from PIL import Image, ImageFilter, ImageOps

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Lazy-loaded EasyOCR reader (heavy init — only created once)
# ──────────────────────────────────────────────────────────────
_reader_cache: dict = {}


def _get_reader(langs: list[str]):
    """Return a cached EasyOCR Reader for the requested languages."""
    key = tuple(sorted(langs))
    if key not in _reader_cache:
        import easyocr
        logger.info("Initializing EasyOCR reader for languages: %s", langs)
        _reader_cache[key] = easyocr.Reader(langs, gpu=False)  # CPU for portability
    return _reader_cache[key]


# ──────────────────────────────────────────────────────────────
# Image pre-processing helpers (improve OCR accuracy)
# ──────────────────────────────────────────────────────────────

MAX_DIMENSION = 4000  # px — resize extremely large images to save memory/time


def _preprocess_image(img: Image.Image) -> Image.Image:
    """
    Apply lightweight pre-processing to improve OCR results:
    1. Convert to RGB (handles RGBA / palette images).
    2. Auto-orient using EXIF data.
    3. Resize if very large.
    4. Convert to grayscale.
    5. Light sharpening.
    """
    # 1. Ensure RGB
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # 2. Auto-orient (phone photos may be rotated)
    img = ImageOps.exif_transpose(img)

    # 3. Resize if too large
    w, h = img.size
    if max(w, h) > MAX_DIMENSION:
        ratio = MAX_DIMENSION / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    # 4. Grayscale
    img = img.convert("L")

    # 5. Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    return img


# ──────────────────────────────────────────────────────────────
# Main extract function
# ──────────────────────────────────────────────────────────────

class OCRError(Exception):
    """Custom exception for OCR failures."""
    pass


def extract_text_from_image(
    source: Union[bytes, io.BytesIO, Image.Image, str],
    langs: list[str] | None = None,
) -> str:
    """
    Extract text from an image using EasyOCR.

    Args:
        source: Image input — raw bytes, BytesIO, PIL Image, or file path.
        langs:  List of EasyOCR language codes (default: ['en', 'fr']).
                See https://www.jaided.ai/easyocr/ for all supported languages.

    Returns:
        Extracted text (may be empty if no text is detected).

    Raises:
        OCRError: If the image cannot be loaded or OCR fails.
    """
    if langs is None:
        langs = ["en", "fr"]

    # ── Load the image ──
    try:
        if isinstance(source, Image.Image):
            img = source
        elif isinstance(source, (bytes, bytearray)):
            img = Image.open(io.BytesIO(source))
        elif isinstance(source, io.BytesIO):
            source.seek(0)
            img = Image.open(source)
        elif isinstance(source, str):
            img = Image.open(source)
        else:
            raise OCRError(f"Unsupported source type: {type(source)}")
    except OCRError:
        raise
    except Exception as exc:
        raise OCRError(f"Could not open image: {exc}") from exc

    # ── Pre-process ──
    img = _preprocess_image(img)

    # ── Convert to numpy array for EasyOCR ──
    img_array = np.array(img)

    # ── Run EasyOCR ──
    try:
        reader = _get_reader(langs)
        results = reader.readtext(img_array, detail=0, paragraph=True)
    except Exception as exc:
        raise OCRError(f"EasyOCR failed: {exc}") from exc

    # ── Join detected text blocks ──
    text = "\n".join(line.strip() for line in results if line.strip())

    logger.info("OCR extracted %d characters from image.", len(text))
    return text
