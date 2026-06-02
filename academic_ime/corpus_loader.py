"""Load text content from txt, md, docx, and pdf files."""

from __future__ import annotations

from pathlib import Path


def _read_txt(path: Path) -> str:
    """Read a plain text file, trying UTF-8 then GBK."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="gbk")


def _read_md(path: Path) -> str:
    """Read a Markdown file."""
    return _read_txt(path)


def _read_docx(path: Path) -> str:
    """Read a .docx file."""
    from docx import Document

    doc = Document(str(path))
    paragraphs: list[str] = []
    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text.strip())
    return "\n".join(paragraphs)


def _read_pdf(path: Path) -> str:
    """Read a .pdf file."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


READERS = {
    ".txt": _read_txt,
    ".md": _read_md,
    ".docx": _read_docx,
    ".pdf": _read_pdf,
}


def load_file(path: Path) -> str:
    """Load text content from a single file based on extension."""
    ext = path.suffix.lower()
    if ext not in READERS:
        raise ValueError(f"不支持的文件格式: {ext}")
    return READERS[ext](path)


def load_directory(root: Path) -> list[tuple[str, str]]:
    """Recursively load all supported files from a directory.

    Returns list of (filename, content) tuples.
    """
    results: list[tuple[str, str]] = []
    if not root.exists():
        raise FileNotFoundError(f"路径不存在: {root}")
    if root.is_file():
        content = load_file(root)
        results.append((root.name, content))
        return results

    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in READERS:
            try:
                content = load_file(path)
                results.append((path.name, content))
            except Exception as e:
                print(f"  警告: 跳过 {path.name}: {e}")
    return results
