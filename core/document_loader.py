"""
core/document_loader.py
Handles PDF, plain text, and image uploads.
Extracts clean text for ingestion into the vector store.
All loaders handle errors gracefully and never crash the app.
"""
import io
import pymupdf as fitz  # PyMuPDF
from PIL import Image
from pathlib import Path


def load_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF byte stream."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pages.append(page.get_text("text"))
    doc.close()
    text = "\n\n".join(pages).strip()
    if not text:
        raise ValueError("PDF appears to be scanned/image-only. Try uploading as an image for OCR.")
    return text


def load_image(file_bytes: bytes) -> str:
    """OCR an image and return extracted text."""
    try:
        import pytesseract
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image).strip()
        if not text:
            raise ValueError("No text could be extracted from the image. Ensure it contains readable text.")
        return text
    except ImportError:
        raise ImportError(
            "pytesseract is not installed or Tesseract OCR engine is not found on your system.\n"
            "Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki"
        )


def load_text(file_bytes: bytes) -> str:
    """Decode plain text or markdown file."""
    return file_bytes.decode("utf-8", errors="replace").strip()


def load_document(filename: str, file_bytes: bytes) -> str:
    """
    Dispatch to the correct loader based on file extension.

    Args:
        filename:   Original filename with extension.
        file_bytes: Raw bytes of the uploaded file.

    Returns:
        Extracted text content.

    Raises:
        ValueError: For unsupported file types or empty extraction.
    """
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return load_pdf(file_bytes)
    elif suffix in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"):
        return load_image(file_bytes)
    elif suffix in (".txt", ".md"):
        return load_text(file_bytes)
    else:
        raise ValueError(
            f"Unsupported file type: '{suffix}'. "
            "Supported: .pdf, .txt, .md, .png, .jpg, .jpeg, .webp, .bmp, .tiff"
        )


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[str]:
    """
    Split text into overlapping chunks for vector indexing.
    Reads CHUNK_SIZE and CHUNK_OVERLAP from environment if not provided.

    Args:
        text:       Full document text.
        chunk_size: Max characters per chunk (default 512).
        overlap:    Characters shared between consecutive chunks (default 64).

    Returns:
        List of non-empty text chunks.
    """
    import os
    chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", 512))
    overlap    = overlap    or int(os.getenv("CHUNK_OVERLAP", 64))

    if overlap >= chunk_size:
        overlap = chunk_size // 8

    chunks, start = [], 0
    while start < len(text):
        end   = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
