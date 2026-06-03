"""Tests for theme_manager.py."""

from __future__ import annotations

import tempfile
from pathlib import Path

from academic_ime.theme_manager import (
    list_themes,
    install_theme,
    preview_theme,
    show_theme,
    uninstall_theme,
    THEME_META,
    THEMES_DIR,
    _get_theme_yaml,
    _backup_existing,
)


def test_list_themes() -> None:
    """list_themes returns all 4 built-in themes."""
    themes = list_themes()
    assert len(themes) == 4
    slugs = {t["slug"] for t in themes}
    assert slugs == {"cute-dog", "academic-blue", "minimal-dark", "line-puppy"}


def test_theme_meta_has_names() -> None:
    """Each theme has a name, slug, and description."""
    for slug, meta in THEME_META.items():
        assert meta["name"]
        assert meta["slug"] == slug
        assert meta["description"]


def test_theme_files_exist() -> None:
    """Each theme directory contains a weasel.custom.yaml file."""
    for slug in THEME_META:
        yaml_path = _get_theme_yaml(slug)
        assert yaml_path.exists(), f"Missing: {yaml_path}"


def test_install_to_temp_dir() -> None:
    """install_theme copies weasel.custom.yaml to target directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        code = install_theme("line-puppy", rime_dir=tmpdir)
        assert code == 0

        dest = Path(tmpdir) / "weasel.custom.yaml"
        assert dest.exists()

        content = dest.read_text(encoding="utf-8")
        assert "line_puppy" in content
        assert "线条小狗" in content
        assert "F8F3E8" in content


def test_install_backup_existing() -> None:
    """install_theme backs up existing config with .bak.academic-ime suffix."""
    with tempfile.TemporaryDirectory() as tmpdir:
        existing = Path(tmpdir) / "weasel.custom.yaml"
        existing.write_text("# existing config", encoding="utf-8")

        code = install_theme("line-puppy", rime_dir=tmpdir)
        assert code == 0

        # Backup should exist with new naming convention
        backup = Path(tmpdir) / "weasel.custom.yaml.bak.academic-ime"
        assert backup.exists()
        assert backup.read_text(encoding="utf-8") == "# existing config"

        # Current file should be the theme
        assert "line_puppy" in existing.read_text(encoding="utf-8")


def test_install_unknown_theme() -> None:
    """install_theme returns 1 for unknown theme."""
    code = install_theme("nonexistent", rime_dir="/tmp")
    assert code == 1


def test_preview_known_theme() -> None:
    """preview_theme returns 0 for valid theme."""
    code = preview_theme("line-puppy")
    assert code == 0


def test_preview_unknown_theme() -> None:
    """preview_theme returns 1 for unknown theme."""
    code = preview_theme("nonexistent")
    assert code == 1


def test_show_known_theme() -> None:
    """show_theme returns 0 for valid theme."""
    code = show_theme("line-puppy")
    assert code == 0


def test_show_unknown_theme() -> None:
    """show_theme returns 1 for unknown theme."""
    code = show_theme("nonexistent")
    assert code == 1


def test_uninstall_restores_backup() -> None:
    """uninstall_theme restores backup if .bak.academic-ime exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Pre-create backup
        backup = Path(tmpdir) / "weasel.custom.yaml.bak.academic-ime"
        backup.write_text("# original user config", encoding="utf-8")

        # Create current config (as if theme was installed)
        current = Path(tmpdir) / "weasel.custom.yaml"
        current.write_text("patch:\n  style/color_scheme: line_puppy\n", encoding="utf-8")

        code = uninstall_theme("line-puppy", rime_dir=tmpdir)
        assert code == 0

        # Should restore the backup
        assert current.read_text(encoding="utf-8") == "# original user config"
        # Backup should be deleted after restore
        assert not backup.exists()


def test_uninstall_no_backup() -> None:
    """uninstall_theme without backup removes theme lines gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        current = Path(tmpdir) / "weasel.custom.yaml"
        original = 'patch:\n  "style/font_face": "Microsoft YaHei"\n  "style/color_scheme": line_puppy\n'
        current.write_text(original, encoding="utf-8")

        code = uninstall_theme("line-puppy", rime_dir=tmpdir)
        assert code == 0

        content = current.read_text(encoding="utf-8")
        assert "line_puppy" not in content
        assert "font_face" in content  # Other config preserved


def test_uninstall_unknown_theme() -> None:
    """uninstall_theme returns 1 for unknown theme."""
    code = uninstall_theme("nonexistent", rime_dir="/tmp")
    assert code == 1


def test_uninstall_no_rime_dir() -> None:
    """uninstall_theme returns 1 when no Rime dir found."""
    code = uninstall_theme("line-puppy", rime_dir="/nonexistent/path")
    assert code == 1


def test_line_puppy_theme_contents() -> None:
    """line-puppy theme has expected color scheme and layout."""
    yaml_path = _get_theme_yaml("line-puppy")
    content = yaml_path.read_text(encoding="utf-8")

    # Color scheme
    assert "line_puppy" in content
    assert "线条小狗" in content
    assert "Line Puppy" in content

    # Colors
    assert "F8F3E8" in content  # back_color
    assert "D8C7AE" in content  # border_color
    assert "F2E2B8" in content  # hilited_back_color
    assert "5A4636" in content  # text_color

    # Layout
    assert "corner_radius: 10" in content
    assert "border_width: 1" in content
    assert "margin_x: 12" in content


def test_line_puppy_no_emoji() -> None:
    """line-puppy theme uses pure color styling, no emoji or images."""
    yaml_path = _get_theme_yaml("line-puppy")
    content = yaml_path.read_text(encoding="utf-8")

    # Should NOT contain emoji or image references
    import re

    # No emoji (common emoji ranges)
    assert not re.search(r"[\U0001F300-\U0001F9FF]", content)
    # No PNG/SVG references
    assert ".png" not in content
    assert ".svg" not in content


def test_missing_rime_dir_hint() -> None:
    """install_theme returns 1 when given a non-existent directory."""
    code = install_theme("line-puppy", rime_dir="/nonexistent/path/to/rime")
    assert code == 1


class TestBackupExisting:
    """Tests for _backup_existing helper."""

    def test_no_existing_no_backup(self) -> None:
        """_backup_existing returns None when no file to back up."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "weasel.custom.yaml"
            result = _backup_existing(dest)
            assert result is None

    def test_existing_creates_backup(self) -> None:
        """_backup_existing creates .bak.academic-ime backup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "weasel.custom.yaml"
            dest.write_text("# test config", encoding="utf-8")
            result = _backup_existing(dest)
            assert result is not None
            assert result.exists()
            assert result.name == "weasel.custom.yaml.bak.academic-ime"
            assert result.read_text(encoding="utf-8") == "# test config"
