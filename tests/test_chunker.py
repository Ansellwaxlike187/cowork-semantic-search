from pathlib import Path

from server.chunker import chunk_document


def test_chunk_short_text():
    """Text shorter than chunk_size returns a single chunk."""
    parts = [{"text": "Short text.", "metadata": {}}]
    chunks = chunk_document(parts, Path("/fake/doc.txt"))
    assert len(chunks) == 1
    assert chunks[0]["text"] == "Short text."
    assert chunks[0]["source_file"] == "/fake/doc.txt"
    assert chunks[0]["file_name"] == "doc.txt"
    assert chunks[0]["file_type"] == ".txt"


def test_chunk_long_text():
    """Text longer than chunk_size returns multiple chunks."""
    long_text = "Word " * 200  # ~1000 chars, well over 400 chunk_size
    parts = [{"text": long_text, "metadata": {}}]
    chunks = chunk_document(parts, Path("/fake/long.md"))
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk["source_file"] == "/fake/long.md"


def test_chunk_preserves_metadata():
    """Page number metadata carries through to chunks."""
    parts = [{"text": "Content on page 5. " * 30, "metadata": {"page_number": 5}}]
    chunks = chunk_document(parts, Path("/fake/report.pdf"))
    for chunk in chunks:
        assert chunk["page_number"] == 5
        assert chunk["file_type"] == ".pdf"


def test_chunk_multiple_parts():
    """Multiple extracted parts produce chunks with correct metadata per part."""
    parts = [
        {"text": "Page one content. " * 20, "metadata": {"page_number": 1}},
        {"text": "Page two content. " * 20, "metadata": {"page_number": 2}},
    ]
    chunks = chunk_document(parts, Path("/fake/multi.pdf"))
    page_numbers = {c["page_number"] for c in chunks}
    assert 1 in page_numbers
    assert 2 in page_numbers


def test_chunk_empty_text_skipped():
    """Empty text parts produce no chunks."""
    parts = [{"text": "", "metadata": {}}, {"text": "   ", "metadata": {}}]
    chunks = chunk_document(parts, Path("/fake/empty.txt"))
    assert len(chunks) == 0


def test_chunk_has_id_and_index():
    """Each chunk has an id and chunk_index."""
    parts = [{"text": "Some content here.", "metadata": {}}]
    chunks = chunk_document(parts, Path("/fake/doc.txt"))
    assert "id" in chunks[0]
    assert chunks[0]["chunk_index"] == 0


def test_chunk_ids_are_unique():
    """Chunk IDs are unique across parts."""
    parts = [
        {"text": "First part content. " * 30, "metadata": {"page_number": 1}},
        {"text": "Second part content. " * 30, "metadata": {"page_number": 2}},
    ]
    chunks = chunk_document(parts, Path("/fake/doc.pdf"))
    ids = [c["id"] for c in chunks]
    assert len(ids) == len(set(ids))
