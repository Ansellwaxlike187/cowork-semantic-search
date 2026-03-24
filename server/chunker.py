"""Text chunking with metadata preservation."""

import hashlib
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def chunk_document(extracted_parts: list[dict], file_path: Path) -> list[dict]:
    """Split extracted text into chunks, preserving per-part metadata."""
    chunks = []
    for part in extracted_parts:
        text = part["text"]
        if not text.strip():
            continue
        splits = splitter.split_text(text)
        page_or_section = part.get("metadata", {}).get("page_number", 0)
        for chunk_idx, chunk_text in enumerate(splits):
            chunks.append({
                "id": f"{_short_hash(str(file_path))}_{page_or_section}_{chunk_idx}",
                "text": chunk_text,
                "source_file": str(file_path),
                "file_name": file_path.name,
                "file_type": file_path.suffix.lower(),
                "folder_path": str(file_path.parent),
                "chunk_index": chunk_idx,
                **part.get("metadata", {}),
            })
    return chunks
