"""Tests for rime_exporter.py."""

import tempfile
from pathlib import Path

from academic_ime.rime_exporter import export_rime


def test_export_rime_yaml() -> None:
    """Export should produce a valid Rime dict.yaml file."""
    entries = [
        {"term": "Falcon签名流程", "pinyin": "falcon qian ming liu cheng", "weight": 100000, "enabled": 1},
        {"term": "范数溢出", "pinyin": "fan shu yi chu", "weight": 95000, "enabled": 1},
        {"term": "disabled_term", "pinyin": "disabled", "weight": 5000, "enabled": 0},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "academic_ime.dict.yaml"
        export_rime(entries, out_path)

        content = out_path.read_text(encoding="utf-8")

        # Check YAML header
        assert "name: academic_ime" in content
        assert 'version: "0.1"' in content
        assert "sort: by_weight" in content
        assert "use_preset_vocabulary: true" in content
        assert "..." in content

        # Check entries (tab-separated)
        assert "Falcon签名流程\tfalcon qian ming liu cheng\t100000" in content
        assert "范数溢出\tfan shu yi chu\t95000" in content

        # Disabled entry should NOT appear
        assert "disabled_term" not in content


def test_export_rime_empty() -> None:
    """Export with no enabled entries should produce header only."""
    entries = [
        {"term": "x", "pinyin": "x", "weight": 1000, "enabled": 0},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "empty.dict.yaml"
        export_rime(entries, out_path)

        content = out_path.read_text(encoding="utf-8")
        assert "name: academic_ime" in content
        # No data lines after header
        lines = content.strip().split("\n")
        # Should just be the 8 header lines
        assert len(lines) == 8
