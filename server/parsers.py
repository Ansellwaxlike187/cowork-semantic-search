"""Per-format text extraction from document files."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx", ".pptx", ".csv"}


def extract_text(file_path: Path) -> list[dict]:
    """Extract text from a file, returning list of {text, metadata} dicts.

    Metadata may include page_number (PDF), slide_number (PPTX), row_number (CSV).
    """
    suffix = file_path.suffix.lower()

    match suffix:
        case ".txt" | ".md":
            text = file_path.read_text(encoding="utf-8", errors="replace")
            return [{"text": text, "metadata": {}}]
        case _:
            raise ValueError(
                f"Unsupported file type: {suffix}. "
                f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )
