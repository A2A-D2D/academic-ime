"""Theme management for Rime Weasel (小狼毫).

Handles listing, installing (with backup), and previewing themes.
Themes are weasel.custom.yaml patch files stored under academic_ime/themes/.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

THEMES_DIR = Path(__file__).parent / "themes"

THEME_META: dict[str, dict[str, str]] = {
    "cute-dog": {
        "name": "线条小狗",
        "slug": "cute-dog",
        "description": "奶油白背景、浅棕边框、粉色高亮、[paw]标签、[dog]选中标记、圆角阴影",
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
}


def list_themes() -> list[dict[str, str]]:
    """Return metadata for all built-in themes."""
    result: list[dict[str, str]] = []
    for slug, meta in THEME_META.items():
        theme_dir = THEMES_DIR / slug
        yaml_path = theme_dir / "weasel.custom.yaml"
        meta["installed"] = str(yaml_path.exists())
        result.append(meta)
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


def find_rime_dir(user_dir: str | None = None) -> Path | None:
    """Find the Rime user directory. Respects --rime-dir if given."""
    if user_dir:
        p = Path(user_dir)
        if p.exists():
            return p
        return None

    import sys
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


def install_theme(
    theme_slug: str,
    rime_dir: str | None = None,
    dry_run: bool = False,
) -> int:
    """Install a theme to the Rime user directory.

    Args:
        theme_slug: Theme identifier (e.g. 'cute-dog').
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

    theme_dir = THEMES_DIR / theme_slug
    src_yaml = theme_dir / "weasel.custom.yaml"
    if not src_yaml.exists():
        console.print(f"[red]主题文件缺失: {src_yaml}[/red]")
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
        console.print(f"  源文件: {src_yaml}")
        console.print(f"  目标:   {dest_yaml}")

        content = src_yaml.read_text(encoding="utf-8")
        preview = content[:500] + ("…" if len(content) > 500 else "")
        console.print(Panel(preview, title="预览"))
        return 0

    # Backup existing config
    if dest_yaml.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = dest_dir / f"weasel.custom.yaml.bak.{timestamp}"
        shutil.copy2(dest_yaml, backup_path)
        console.print(f"[yellow]已备份 → {backup_path.name}[/yellow]")

    # Install theme
    shutil.copy2(src_yaml, dest_yaml)
    console.print(f"[green]已安装 {THEME_META[theme_slug]['name']} → {dest_yaml}[/green]")

    # Redeploy hint
    console.print("\n[yellow]请重新部署小狼毫使主题生效：[/yellow]")
    console.print("  右键小狼毫托盘图标 → 重新部署")

    return 0


def preview_theme(theme_slug: str) -> int:
    """Print a preview of a theme's weasel.custom.yaml content."""
    if theme_slug not in THEME_META:
        console.print(f"[red]未知主题: {theme_slug}[/red]")
        console.print(f"可用主题: {', '.join(THEME_META.keys())}")
        return 1

    meta = THEME_META[theme_slug]
    theme_dir = THEMES_DIR / theme_slug
    src_yaml = theme_dir / "weasel.custom.yaml"

    if not src_yaml.exists():
        console.print(f"[red]主题文件缺失: {src_yaml}[/red]")
        return 1

    content = src_yaml.read_text(encoding="utf-8")
    console.print(f"[bold]{meta['name']} / {meta['slug']}[/bold]")
    console.print(f"[dim]{meta['description']}[/dim]\n")
    console.print(Panel(content, title="weasel.custom.yaml"))
    return 0
