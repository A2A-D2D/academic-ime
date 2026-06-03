"""Theme management for Rime Weasel (小狼毫).

Handles listing, showing, installing (with backup), and uninstalling themes.
Themes are weasel.custom.yaml patch files stored under academic_ime/themes/.
"""

from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

THEMES_DIR = Path(__file__).parent / "themes"

THEME_META: dict[str, dict[str, str]] = {
    "cute-dog": {
        "name": "线条小狗",
        "slug": "cute-dog",
        "description": "奶油白背景、浅棕边框、粉色高亮、paw标签、dog选中标记、圆角阴影",
        "has_dark": "true",
    },
    "academic-blue": {
        "name": "学术蓝",
        "slug": "academic-blue",
        "description": "浅蓝灰背景、蓝色高亮，清爽专业，适合长时间写作",
        "has_dark": "false",
    },
    "minimal-dark": {
        "name": "极简暗色",
        "slug": "minimal-dark",
        "description": "深色背景、低对比度，适合夜间使用",
        "has_dark": "false",
    },
    "line-puppy": {
        "name": "线条小狗",
        "slug": "line-puppy",
        "description": "浅米白背景、浅奶黄高亮、棕色文字，圆角手账风，简洁线稿小狗风格",
        "has_dark": "false",
    },
}


def _get_theme_dir(slug: str) -> Path:
    """Resolve theme directory for a given slug."""
    return THEMES_DIR / slug


def _get_theme_yaml(slug: str) -> Path:
    """Resolve weasel.custom.yaml path for a theme."""
    return _get_theme_dir(slug) / "weasel.custom.yaml"


def list_themes() -> list[dict[str, str]]:
    """Return metadata for all built-in themes."""
    result: list[dict[str, str]] = []
    for slug, meta in THEME_META.items():
        yaml_path = _get_theme_yaml(slug)
        meta_copy = dict(meta)
        meta_copy["installed"] = str(yaml_path.exists())
        result.append(meta_copy)
    return result


def print_theme_list() -> None:
    """Print a rich table of available themes."""
    table = Table(title="内置主题")
    table.add_column("名称", style="cyan")
    table.add_column("命令", style="green")
    table.add_column("说明")
    table.add_column("夜间模式", justify="center")

    for slug, meta in THEME_META.items():
        table.add_row(
            meta["name"],
            slug,
            meta["description"],
            "Y" if meta["has_dark"] == "true" else "-",
        )

    console.print(table)
    console.print("\n[dim]安装: academic-ime theme install <名称>[/dim]")
    console.print("[dim]卸载: academic-ime theme uninstall <名称>[/dim]")


def find_rime_dir(user_dir: str | None = None) -> Path | None:
    """Find the Rime user directory. Respects --rime-dir if given."""
    if user_dir:
        p = Path(user_dir)
        if p.exists():
            return p
        return None

    if sys.platform == "win32":
        appdata = Path.home() / "AppData" / "Roaming" / "Rime"
        if appdata.exists():
            return appdata
    elif sys.platform == "darwin":
        p = Path.home() / "Library" / "Rime"
        if p.exists():
            return p
    else:
        for candidate in [
            Path.home() / ".config" / "ibus" / "rime",
            Path.home() / ".config" / "fcitx" / "rime",
        ]:
            if candidate.exists():
                return candidate
    return None


def _backup_existing(dest_yaml: Path) -> Path | None:
    """Create a backup of an existing weasel.custom.yaml.

    Uses the naming convention: weasel.custom.yaml.bak.academic-ime
    Returns the backup path, or None if no backup was needed.
    """
    if not dest_yaml.exists():
        return None

    backup_path = dest_yaml.parent / f"{dest_yaml.name}.bak.academic-ime"
    shutil.copy2(dest_yaml, backup_path)
    console.print(f"[yellow]已备份 → {backup_path.name}[/yellow]")
    return backup_path


def show_theme(theme_slug: str) -> int:
    """Show theme details with color swatches and YAML preview.

    Args:
        theme_slug: Theme identifier (e.g. 'line-puppy').

    Returns:
        0 on success, 1 if theme not found.
    """
    if theme_slug not in THEME_META:
        console.print(f"[red]未知主题: {theme_slug}[/red]")
        console.print(f"可用主题: {', '.join(THEME_META.keys())}")
        return 1

    meta = THEME_META[theme_slug]
    yaml_path = _get_theme_yaml(theme_slug)

    if not yaml_path.exists():
        console.print(f"[red]主题文件缺失: {yaml_path}[/red]")
        return 1

    # Header
    console.print(f"\n[bold]{meta['name']} / {meta['slug']}[/bold]")
    console.print(f"[dim]{meta['description']}[/dim]")
    console.print(f"[dim]推荐字体: Microsoft YaHei / LXGW WenKai / Sarasa UI SC[/dim]")
    console.print(f"[dim]夜间模式: {'Y' if meta['has_dark'] == 'true' else '—'}[/dim]\n")

    # Parse YAML content to extract color values
    content = yaml_path.read_text(encoding="utf-8")
    _print_color_swatches(content)

    # YAML preview
    console.print(Panel(content.strip(), title="weasel.custom.yaml", border_style="dim"))
    return 0


def _print_color_swatches(yaml_content: str) -> None:
    """Parse color values from YAML and print swatches using rich."""
    import re

    color_map: dict[str, str] = {}
    for line in yaml_content.splitlines():
        m = re.match(r"\s+(\w+):\s*(0x[0-9A-Fa-f]{6,8})\b", line)
        if m:
            name = m.group(1)
            hex_val = m.group(2)
            # Convert 0xRRGGBBAA → RRGGBB (raw hex without alpha)
            if len(hex_val) == 10:  # 0x + 8 hex digits
                hex_val = hex_val[2:8]
            else:
                hex_val = hex_val[2:]
            color_map[name] = hex_val

    if not color_map:
        return

    console.print("[bold]颜色预览:[/bold]")
    for name, hex_val in color_map.items():
        display_name = name.replace("_", " ").replace("hilited", "选中")
        # Use rich's Style to create a colored swatch
        from rich.style import Style
        from rich.text import Text

        swatch = Text("  ", style=Style(bgcolor=f"#{hex_val}"))
        label = Text(f"  {display_name}  #{hex_val}")
        console.print(swatch + label)
    console.print()


def install_theme(
    theme_slug: str,
    rime_dir: str | None = None,
    dry_run: bool = False,
) -> int:
    """Install a theme to the Rime user directory.

    Args:
        theme_slug: Theme identifier (e.g. 'line-puppy').
        rime_dir: Path to Rime user directory. Auto-detected if None.
        dry_run: If True, preview only, don't write files.

    Returns:
        0 on success, 1 on error.
    """
    # Validate theme
    if theme_slug not in THEME_META:
        console.print(f"[red]未知主题: {theme_slug}[/red]")
        console.print(f"可用主题: {', '.join(THEME_META.keys())}")
        return 1

    yaml_path = _get_theme_yaml(theme_slug)
    if not yaml_path.exists():
        console.print(f"[red]主题文件缺失: {yaml_path}[/red]")
        return 1

    # Find Rime directory
    dest_dir = find_rime_dir(rime_dir)
    if dest_dir is None:
        if rime_dir:
            console.print(f"[red]Rime 目录不存在: {rime_dir}[/red]")
        else:
            console.print("[red]未找到 Rime 用户目录，请用 --rime-dir 指定[/red]")
        return 1

    dest_yaml = dest_dir / "weasel.custom.yaml"

    if dry_run:
        console.print(f"[bold blue]预览安装 {THEME_META[theme_slug]['name']}[/bold blue]")
        console.print(f"  源文件: {yaml_path}")
        console.print(f"  目标:   {dest_yaml}")
        content = yaml_path.read_text(encoding="utf-8")
        preview = content[:500] + ("…" if len(content) > 500 else "")
        console.print(Panel(preview, title="预览"))
        return 0

    # Backup existing config
    _backup_existing(dest_yaml)

    # Install theme
    shutil.copy2(yaml_path, dest_yaml)
    console.print(f"[green]已安装 {THEME_META[theme_slug]['name']} → {dest_yaml}[/green]")

    _print_deploy_hint()
    return 0


def uninstall_theme(theme_slug: str, rime_dir: str | None = None) -> int:
    """Uninstall a theme from the Rime user directory.

    If a backup file (weasel.custom.yaml.bak.academic-ime) exists, restores it.
    Otherwise removes only the theme's color scheme from the config.

    Args:
        theme_slug: Theme identifier (e.g. 'line-puppy').
        rime_dir: Path to Rime user directory. Auto-detected if None.

    Returns:
        0 on success, 1 on error.
    """
    if theme_slug not in THEME_META:
        console.print(f"[red]未知主题: {theme_slug}[/red]")
        console.print(f"可用主题: {', '.join(THEME_META.keys())}")
        return 1

    dest_dir = find_rime_dir(rime_dir)
    if dest_dir is None:
        console.print("[red]未找到 Rime 用户目录[/red]")
        return 1

    dest_yaml = dest_dir / "weasel.custom.yaml"
    backup_path = dest_dir / "weasel.custom.yaml.bak.academic-ime"

    if backup_path.exists():
        console.print(f"[yellow]发现备份文件: {backup_path.name}[/yellow]")
        shutil.copy2(backup_path, dest_yaml)
        backup_path.unlink()
        console.print(f"[green]已恢复原有配置，删除备份[/green]")
        _print_deploy_hint()
        return 0

    # No backup — try to remove the theme's color scheme from current config
    if not dest_yaml.exists():
        console.print("[yellow]未找到 weasel.custom.yaml，无需卸载[/yellow]")
        return 0

    _remove_color_scheme(dest_yaml, theme_slug)
    _print_deploy_hint()
    return 0


def _remove_color_scheme(dest_yaml: Path, theme_slug: str) -> None:
    """Remove a theme's color_scheme block and related style entries.

    Only touches lines related to the target scheme; preserves all other config.
    """
    scheme_key = theme_slug.replace("-", "_")

    lines = dest_yaml.read_text(encoding="utf-8").splitlines(True)
    result: list[str] = []
    skip_block = False
    block_indent: Optional[str] = None

    for line in lines:
        # Detect start of the target preset_color_schemes block
        if f'"preset_color_schemes/{scheme_key}":' in line:
            skip_block = True
            # Determine indentation of the block (2 spaces past current indent)
            stripped = line.lstrip()
            block_indent = line[: len(line) - len(stripped)] + "  "
            continue

        # Also check for old-style color_scheme reference
        if skip_block:
            if line.strip() == "" and block_indent is not None:
                # Empty line within block — skip
                continue
            if block_indent is not None and line.startswith(block_indent):
                # Still inside the block
                continue
            # End of block
            skip_block = False
            block_indent = None
            continue

        # Remove style/color_scheme reference
        if scheme_key in line and "style/color_scheme" in line:
            continue

        result.append(line)

    dest_yaml.write_text("".join(result), encoding="utf-8")
    console.print(f"[green]已从配置中移除 {theme_slug} 相关设置[/green]")


def preview_theme(theme_slug: str) -> int:
    """Print a preview of a theme's weasel.custom.yaml content."""
    if theme_slug not in THEME_META:
        console.print(f"[red]未知主题: {theme_slug}[/red]")
        console.print(f"可用主题: {', '.join(THEME_META.keys())}")
        return 1

    meta = THEME_META[theme_slug]
    yaml_path = _get_theme_yaml(theme_slug)

    if not yaml_path.exists():
        console.print(f"[red]主题文件缺失: {yaml_path}[/red]")
        return 1

    content = yaml_path.read_text(encoding="utf-8")
    console.print(f"[bold]{meta['name']} / {meta['slug']}[/bold]")
    console.print(f"[dim]{meta['description']}[/dim]\n")
    console.print(Panel(content, title="weasel.custom.yaml"))
    return 0


def _print_deploy_hint() -> None:
    """Print a reminder to re-deploy Rime."""
    console.print("\n[yellow]请重新部署小狼毫使主题生效：[/yellow]")
    console.print("  右键小狼毫托盘图标 → 重新部署")
    console.print("[dim]  如果未生效，可尝试重启小狼毫算法服务[/dim]")
