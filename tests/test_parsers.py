from pathlib import Path

import pytest

from server.parsers import extract_text, SUPPORTED_EXTENSIONS


@pytest.fixture
def tmp_files(tmp_path):
    """Create test files for parser tests."""
    (tmp_path / "hello.txt").write_text("Hello, world!", encoding="utf-8")
    (tmp_path / "notes.md").write_text(
        "# Notes\n\nSome markdown content.\n\n## Section 2\n\nMore text.",
        encoding="utf-8",
    )
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    (tmp_path / "german.md").write_text(
        "# Quartalsbericht\n\nDer Umsatz stieg um 23%.", encoding="utf-8"
    )
    (tmp_path / "utf8.txt").write_bytes("Sch\u00f6ne Gr\u00fc\u00dfe \u2014 test".encode("utf-8"))
    return tmp_path


def test_supported_extensions_include_txt_and_md():
    assert ".txt" in SUPPORTED_EXTENSIONS
    assert ".md" in SUPPORTED_EXTENSIONS


def test_parse_txt(tmp_files):
    result = extract_text(tmp_files / "hello.txt")
    assert len(result) == 1
    assert result[0]["text"] == "Hello, world!"
    assert result[0]["metadata"] == {}


def test_parse_md(tmp_files):
    result = extract_text(tmp_files / "notes.md")
    assert len(result) == 1
    assert "# Notes" in result[0]["text"]
    assert "Section 2" in result[0]["text"]


def test_parse_empty_txt(tmp_files):
    result = extract_text(tmp_files / "empty.txt")
    assert len(result) == 1
    assert result[0]["text"] == ""


def test_parse_german_md(tmp_files):
    result = extract_text(tmp_files / "german.md")
    assert "Quartalsbericht" in result[0]["text"]
    assert "23%" in result[0]["text"]


def test_parse_utf8(tmp_files):
    result = extract_text(tmp_files / "utf8.txt")
    assert "Sch\u00f6ne" in result[0]["text"]
    assert "\u2014" in result[0]["text"]


def test_parse_unsupported_extension(tmp_path):
    bad_file = tmp_path / "data.xyz"
    bad_file.write_text("some data")
    with pytest.raises(ValueError, match="Unsupported"):
        extract_text(bad_file)
