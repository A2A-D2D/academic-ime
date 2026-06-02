"""Export lexicon entries to Rime dict.yaml format."""

from __future__ import annotations

from pathlib import Path


RIME_HEADER = """# Rime dictionary
# encoding: utf-8
---
name: academic_ime
version: "0.1"
sort: by_weight
use_preset_vocabulary: false
...

"""


def export_rime(
    entries: list[dict[str, str | int]],
    output_path: Path,
) -> None:
    """Export enabled entries to a Rime-compatible dict.yaml file.

    Only exports entries with enabled=1.
    Format: term<TAB>pinyin<TAB>weight
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enabled = [e for e in entries if e["enabled"] == 1]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(RIME_HEADER)
        for entry in enabled:
            term = entry["term"]
            pinyin = entry["pinyin"]
            weight = entry["weight"]
            f.write(f"{term}\t{pinyin}\t{weight}\n")
