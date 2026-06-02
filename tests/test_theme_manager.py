"""Tests for theme_manager.py."""

from __future__ import annotations

import tempfile
from pathlib import Path

from academic_ime.theme_manager import (
    list_themes,
    install_theme,
    preview_theme,
    THEME_META,
    THEMES_DIR,
)


def test_list_themes() -> None:
    """list_themes returns all 3 built-in themes."""
    themes = list_themes()
    assert len(themes) == 3
    slugs = {t["slug"] for t in themes}
    assert slugs == {"cute-dog", "academic-blue", "minimal-dark"}


def test_theme_meta_has_names() -> None:
    """Each theme has a name, slug, and description."""
    for slug, meta in THEME_META.items():
        assert meta["name"]
        assert meta["slug"] == slug
        assert meta["description"]


def test_theme_files_exist() -> None:
    """Each theme directory contains a weasel.custom.yaml file."""
    for slug in THEME_META:
        yaml_path = THEMES_DIR / slug / "weasel.custom.yaml"
        assert yaml_path.exists(), f"Missing: {yaml_path}"


def test_install_to_temp_dir() -> None:
    """install_theme copies weasel.custom.yaml to target directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        code = install_theme("cute-dog", rime_dir=tmpdir)
        assert code == 0

        dest = Path(tmpdir) / "weasel.custom.yaml"
        assert dest.exists()

        content = dest.read_text(encoding="utf-8")
        assert "cute_dog" in content
        assert "🐾" in content
        assert "🐶" in content
        assert "线条小狗" in content


def test_install_backup_existing() -> None:
    """install_theme backs up existing weasel.custom.yaml before overwriting."""
    with tempfile.TemporaryDirectory() as tmpdir:
        existing = Path(tmpdir) / "weasel.custom.yaml"
        existing.write_text("# existing config", encoding="utf-8")

        code = install_theme("cute-dog", rime_dir=tmpdir)
        assert code == 0

        # Original should be backed up
        backups = list(Path(tmpdir).glob("weasel.custom.yaml.bak.*"))
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "# existing config"

        # Current file should be the theme
        assert "cute_dog" in existing.read_text(encoding="utf-8")


def test_install_unknown_theme() -> None:
    """install_theme returns non-zero for unknown theme."""
    code = install_theme("nonexistent", rime_dir="/tmp")
    assert code == 1


def test_preview_known_theme() -> None:
    """preview_theme returns 0 for valid theme."""
    code = preview_theme("cute-dog")
    assert code == 0


def test_preview_unknown_theme() -> None:
    """preview_theme returns 1 for unknown theme."""
    code = preview_theme("nonexistent")
    assert code == 1


def test_academic_blue_theme_contents() -> None:
    """academic-blue theme has expected color scheme."""
    yaml_path = THEMES_DIR / "academic-blue" / "weasel.custom.yaml"
    content = yaml_path.read_text(encoding="utf-8")
    assert "academic_blue" in content
    assert "学术蓝" in content


def test_minimal_dark_theme_contents() -> None:
    """minimal-dark theme has expected color scheme."""
    yaml_path = THEMES_DIR / "minimal-dark" / "weasel.custom.yaml"
    content = yaml_path.read_text(encoding="utf-8")
    assert "minimal_dark" in content
    assert "极简暗色" in content
