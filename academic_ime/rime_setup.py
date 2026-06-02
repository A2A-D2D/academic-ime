"""Auto-detect Rime directory and install dictionary + config."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def find_rime_dir() -> Path | None:
    """Auto-detect the Rime user directory."""
    if sys.platform == "win32":
        appdata = Path.home() / "AppData" / "Roaming" / "Rime"
        if appdata.exists():
            return appdata
    elif sys.platform == "darwin":
        mac_dir = Path.home() / "Library" / "Rime"
        if mac_dir.exists():
            return mac_dir
    else:
        for candidate in [
            Path.home() / ".config" / "ibus" / "rime",
            Path.home() / ".config" / "fcitx" / "rime",
        ]:
            if candidate.exists():
                return candidate
    return None


def find_deployer(rime_dir: Path) -> str | None:
    """Find the Rime deployer executable."""
    if sys.platform == "win32":
        for base in [Path("C:/Program Files/Rime"), Path("C:/Program Files (x86)/Rime")]:
            if base.exists():
                for d in sorted(base.iterdir(), reverse=True):
                    exe = d / "WeaselDeployer.exe"
                    if exe.exists():
                        return str(exe)
    elif sys.platform == "darwin":
        return "/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel"
    return None


def find_shared_data() -> Path | None:
    """Find Rime shared data directory."""
    if sys.platform == "win32":
        for base in [Path("C:/Program Files/Rime"), Path("C:/Program Files (x86)/Rime")]:
            if base.exists():
                for d in sorted(base.iterdir(), reverse=True):
                    data = d / "data"
                    if data.exists():
                        return data


MERGE_HEADER = """# Rime dictionary
# encoding: utf-8
---
name: luna_pinyin_plus
version: "2026.06"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - luna_pinyin
...

"""

LUNA_SIMP_PATCH = """patch:
  translator/dictionary: luna_pinyin_plus
"""

DEFAULT_CUSTOM = """patch:
  schema_list:
    - schema: luna_pinyin_simp
  switcher:
    hotkeys:
      - Control+grave
"""

WEASEL_THEME = """patch:
  "style/font_face": "Microsoft YaHei"
  "style/font_point": 16
  "style/label_format": "%s"
  "style/color_scheme": puppy
  "style/horizontal": true
  "preset_color_schemes/puppy":
    name: 线条小狗
    author: AcademicIME
    back_color: 0xFFF8F0
    border_color: 0xC8956C
    text_color: 0x4A3728
    candidate_text_color: 0x6B4C3B
    hilited_text_color: 0xFFFFFF
    hilited_back_color: 0xE8A87C
    hilited_candidate_text_color: 0xFFFFFF
    hilited_candidate_back_color: 0xD4956B
    comment_text_color: 0xB8956E
    label_color: 0xC8956C
    hilited_label_color: 0xFFFFFF
"""


def build_merged_dict(dict_path: Path, rime_dir: Path) -> Path | None:
    """Build a merged dictionary that imports luna_pinyin and appends our terms.

    We avoid import_tables issues by creating a raw merge: our entries are
    appended directly after the header (luna_pinyin is still imported).
    """
    merged = rime_dir / "luna_pinyin_plus.dict.yaml"

    # Copy our academic dict to Rime dir
    academic_dest = rime_dir / "academic_ime.dict.yaml"
    shutil.copy2(dict_path, academic_dest)

    # Create wrapper that imports luna_pinyin
    merged.write_text(MERGE_HEADER, encoding="utf-8")
    return merged


def setup_rime(dict_path: Path, dry_run: bool = False) -> list[str]:
    """Install AcademicIME dictionary and config into Rime user directory."""
    actions: list[str] = []

    rime_dir = find_rime_dir()
    if rime_dir is None:
        actions.append("[red]未找到 Rime 用户目录，请先安装小狼毫/鼠须管[/red]")
        return actions
    actions.append(f"[green]找到 Rime 目录: {rime_dir}[/green]")

    if not dict_path.exists():
        actions.append(f"[red]词库文件不存在: {dict_path}[/red]")
        actions.append("[yellow]请先运行: academic-ime extract <语料> && academic-ime export-rime[/yellow]")
        return actions

    # 1. Copy academic dict & build merged wrapper
    merged_path = build_merged_dict(dict_path, rime_dir)
    actions.append("  创建合并词库 → luna_pinyin_plus.dict.yaml (luna_pinyin + academic_ime)")

    # 2. Patch luna_pinyin_simp + luna_pinyin to use merged dict
    for schema in ["luna_pinyin_simp", "luna_pinyin"]:
        patch_file = rime_dir / f"{schema}.custom.yaml"
        if not dry_run:
            patch_file.write_text(LUNA_SIMP_PATCH, encoding="utf-8")
    actions.append("  配置拼音方案 → 使用 luna_pinyin_plus")

    # 3. Default schema
    default_cfg = rime_dir / "default.custom.yaml"
    if not dry_run:
        default_cfg.write_text(DEFAULT_CUSTOM, encoding="utf-8")
    actions.append("  设置默认方案 → luna_pinyin_simp")

    # 4. Theme
    weasel_cfg = rime_dir / "weasel.custom.yaml"
    if not dry_run:
        weasel_cfg.write_text(WEASEL_THEME, encoding="utf-8")
    actions.append("  安装线条小狗皮肤")

    # 5. Force rebuild
    # Remove compiled extended files to force clean build
    for f in rime_dir.glob("build/luna_pinyin_plus.*"):
        if not dry_run:
            f.unlink()

    deployer = find_deployer(rime_dir)
    if deployer and not dry_run:
        try:
            subprocess.run([deployer, "/deploy"], capture_output=True, timeout=60)
            actions.append("[green]  已重新部署 Rime[/green]")
        except Exception as e:
            actions.append(f"[yellow]  自动部署失败: {e}[/yellow]")
            actions.append("[yellow]  请右键 Rime 托盘图标 → 重新部署[/yellow]")
    elif deployer:
        actions.append(f"  将运行: {deployer} /deploy")
    else:
        actions.append("[yellow]  未找到部署器，请手动重新部署 Rime[/yellow]")

    return actions
