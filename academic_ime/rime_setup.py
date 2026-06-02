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
        # Search under Program Files
        for base in [Path("C:/Program Files/Rime"), Path("C:/Program Files (x86)/Rime")]:
            if base.exists():
                for d in sorted(base.iterdir(), reverse=True):
                    exe = d / "WeaselDeployer.exe"
                    if exe.exists():
                        return str(exe)
    elif sys.platform == "darwin":
        return "/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel"
    return None


EXTENDED_DICT = """---
name: luna_pinyin.extended
version: "2026.06"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - luna_pinyin
  - academic_ime
...
"""

LUNA_SIMP_PATCH = """patch:
  translator/dictionary: luna_pinyin.extended
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


def setup_rime(dict_path: Path, dry_run: bool = False) -> list[str]:
    """Install AcademicIME dictionary and config into Rime user directory.

    Args:
        dict_path: Path to the academic_ime.dict.yaml file.
        dry_run: If True, only report what would be done.

    Returns:
        List of action descriptions.
    """
    actions: list[str] = []

    rime_dir = find_rime_dir()
    if rime_dir is None:
        actions.append("[red]未找到 Rime 用户目录，请先安装小狼毫/鼠须管[/red]")
        return actions

    actions.append(f"[green]找到 Rime 目录: {rime_dir}[/green]")

    if not dict_path.exists():
        actions.append(f"[red]词库文件不存在: {dict_path}[/red]")
        actions.append("[yellow]请先运行: academic-ime extract <语料目录> --out <输出路径>[/yellow]")
        actions.append("[yellow]再运行: academic-ime export-rime <csv路径> --out <dict路径>[/yellow]")
        return actions

    # 1. Copy dict file
    dest_dict = rime_dir / "academic_ime.dict.yaml"
    if not dry_run:
        shutil.copy2(dict_path, dest_dict)
    actions.append(f"  复制词库 → {dest_dict.name}")

    # 2. Extended dictionary
    ext_dict = rime_dir / "luna_pinyin.extended.dict.yaml"
    if not dry_run:
        ext_dict.write_text(EXTENDED_DICT, encoding="utf-8")
    actions.append(f"  创建扩展词库 → {ext_dict.name}")

    # 3. Luna pinyin patches (simp + trad both use extended dict)
    for schema in ["luna_pinyin_simp", "luna_pinyin"]:
        patch_file = rime_dir / f"{schema}.custom.yaml"
        if not dry_run:
            patch_file.write_text(LUNA_SIMP_PATCH, encoding="utf-8")
    actions.append("  配置拼音方案 → luna_pinyin_simp + luna_pinyin")

    # 4. Default schema
    default_cfg = rime_dir / "default.custom.yaml"
    if not dry_run:
        default_cfg.write_text(DEFAULT_CUSTOM, encoding="utf-8")
    actions.append(f"  设置默认方案 → {default_cfg.name}")

    # 5. Weasel theme
    weasel_cfg = rime_dir / "weasel.custom.yaml"
    if not dry_run:
        weasel_cfg.write_text(WEASEL_THEME, encoding="utf-8")
    actions.append(f"  安装线条小狗皮肤 → {weasel_cfg.name}")

    # 6. Deploy
    deployer = find_deployer(rime_dir)
    if deployer and not dry_run:
        try:
            subprocess.run([deployer, "/deploy"], capture_output=True, timeout=30)
            actions.append("[green]  已重新部署 Rime[/green]")
        except Exception as e:
            actions.append(f"[yellow]  自动部署失败: {e}[/yellow]")
            actions.append("[yellow]  请右键 Rime 托盘图标 → 重新部署[/yellow]")
    elif deployer:
        actions.append(f"  将运行: {deployer} /deploy")
    else:
        actions.append("[yellow]  未找到部署器，请手动重新部署 Rime[/yellow]")

    return actions
