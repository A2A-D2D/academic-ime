"""CLI commands for AcademicIME."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from academic_ime.corpus_loader import load_directory
from academic_ime.term_extractor import extract_from_corpus
from academic_ime.lexicon import build_lexicon, write_csv, read_csv
from academic_ime.rime_exporter import export_rime
from academic_ime.rime_setup import setup_rime
from academic_ime.theme_manager import (
    list_themes,
    print_theme_list,
    install_theme,
    preview_theme,
    show_theme,
    uninstall_theme,
)
from academic_ime.pinyin_utils import term_to_pinyin

app = typer.Typer(
    name="academic-ime",
    help="学术联想输入法 - 面向科研写作的中文输入法增强工具",
)
console = Console()

INIT_FILES = {
    "user_terms.csv": "term,pinyin,weight,source_count,term_type,enabled\n",
    "academic_ime_config.toml": (
        "# AcademicIME 配置文件\n"
        "# 更多配置选项将在后续版本中添加\n"
        '[extract]\n'
        'min_freq = 2\n'
        'max_terms = 5000\n'
    ),
}


@app.command()
def init() -> None:
    """初始化项目配置，创建 data/ output/ 目录和配置文件。"""
    console.print("[bold blue]初始化 AcademicIME 项目...[/bold blue]")
    created: list[str] = []

    for dirname in ["data", "output"]:
        d = Path(dirname)
        if not d.exists():
            d.mkdir(parents=True)
            created.append(f"  + {dirname}/")

    for filename, content in INIT_FILES.items():
        p = Path(filename)
        if not p.exists():
            p.write_text(content, encoding="utf-8")
            created.append(f"  + {filename}")

    if created:
        for item in created:
            console.print(f"  {item}")
        console.print("[green]初始化完成[/green]")
    else:
        console.print("[yellow]项目已初始化，跳过[/yellow]")


@app.command()
def extract(
    input_dir: str = typer.Argument(..., help="输入语料目录路径"),
    out: str = typer.Option("output/candidates.csv", help="输出 CSV 文件路径"),
) -> None:
    """导入语料并提取候选词。"""
    root = Path(input_dir)
    if not root.exists():
        console.print(f"[red]错误: 路径不存在: {input_dir}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold blue]正在读取语料: {input_dir}[/bold blue]")
    file_contents = load_directory(root)

    if not file_contents:
        console.print("[red]错误: 未找到支持的文件[/red]")
        raise typer.Exit(code=1)

    console.print(f"  读取了 {len(file_contents)} 个文件")

    console.print("[bold blue]正在提取术语...[/bold blue]")
    term_freq, term_sources = extract_from_corpus(file_contents)

    console.print(f"  提取了 {len(term_freq)} 个候选词")

    console.print("[bold blue]正在计算权重...[/bold blue]")
    entries = build_lexicon(term_freq, term_sources)

    out_path = Path(out)
    write_csv(entries, out_path)
    console.print(f"[green]已导出 {len(entries)} 个候选词到 {out}[/green]")


@app.command()
def review(
    csv_path: str = typer.Argument(..., help="候选词 CSV 文件路径"),
    limit: int = typer.Option(100, help="显示前 N 个候选词"),
) -> None:
    """查看候选词列表，按权重排序。"""
    path = Path(csv_path)
    if not path.exists():
        console.print(f"[red]错误: 文件不存在: {csv_path}[/red]")
        raise typer.Exit(code=1)

    entries = read_csv(path)
    entries.sort(key=lambda e: e["weight"], reverse=True)
    display_entries = entries[:limit]

    table = Table(title=f"候选词列表 (前 {min(limit, len(entries))} / {len(entries)} 条)")
    table.add_column("#", style="dim", width=5)
    table.add_column("词条", style="cyan")
    table.add_column("拼音", style="green")
    table.add_column("权重", justify="right", style="yellow")
    table.add_column("来源数", justify="right", style="dim")
    table.add_column("类型", justify="center", width=8)
    table.add_column("启用", justify="center", width=5)

    type_colors = {"zh": "blue", "en": "magenta", "mixed": "red", "phrase": "yellow"}

    for i, entry in enumerate(display_entries, 1):
        ttype = str(entry["term_type"])
        tcolor = type_colors.get(ttype, "white")
        enabled_mark = "Y" if entry["enabled"] else "N"
        table.add_row(
            str(i),
            str(entry["term"]),
            str(entry["pinyin"]),
            str(entry["weight"]),
            str(entry["source_count"]),
            f"[{tcolor}]{ttype}[/{tcolor}]",
            enabled_mark,
        )

    console.print(table)


@app.command(name="export-rime")
def export_rime_cmd(
    csv_path: str = typer.Argument(..., help="候选词 CSV 文件路径"),
    out: str = typer.Option("output/academic_ime.dict.yaml", help="输出 YAML 文件路径"),
) -> None:
    """导出 Rime 词库 dict.yaml 文件。"""
    path = Path(csv_path)
    if not path.exists():
        console.print(f"[red]错误: 文件不存在: {csv_path}[/red]")
        raise typer.Exit(code=1)

    entries = read_csv(path)
    enabled_count = sum(1 for e in entries if e["enabled"] == 1)

    out_path = Path(out)
    export_rime(entries, out_path)
    console.print(
        f"[green]已导出 {enabled_count} 个词条到 {out}[/green]"
    )


@app.command()
def stats(
    csv_path: str = typer.Argument(..., help="候选词 CSV 文件路径"),
) -> None:
    """显示项目统计信息。"""
    path = Path(csv_path)
    if not path.exists():
        console.print(f"[red]错误: 文件不存在: {csv_path}[/red]")
        raise typer.Exit(code=1)

    entries = read_csv(path)

    total = len(entries)
    by_type: dict[str, int] = {}
    for e in entries:
        t = str(e["term_type"])
        by_type[t] = by_type.get(t, 0) + 1

    enabled = sum(1 for e in entries if e["enabled"] == 1)
    max_weight = max(e["weight"] for e in entries) if entries else 0
    min_weight = min(e["weight"] for e in entries) if entries else 0

    console.print("[bold blue]== 项目统计 ==[/bold blue]\n")

    table = Table(title="汇总")
    table.add_column("指标", style="cyan")
    table.add_column("数值", justify="right", style="green")
    table.add_row("总词条数", str(total))
    table.add_row("已启用词条数", str(enabled))
    table.add_row("最高权重", str(max_weight))
    table.add_row("最低权重", str(min_weight))
    for ttype, count in sorted(by_type.items()):
        table.add_row(f"  {ttype} 类型", str(count))
    console.print(table)

    # Top 20
    sorted_entries = sorted(entries, key=lambda e: e["weight"], reverse=True)
    top_table = Table(title="Top 20 高频词")
    top_table.add_column("#", style="dim", width=4)
    top_table.add_column("词条", style="cyan")
    top_table.add_column("权重", justify="right", style="yellow")
    top_table.add_column("类型", justify="center", style="green")

    for i, e in enumerate(sorted_entries[:20], 1):
        top_table.add_row(str(i), str(e["term"]), str(e["weight"]), str(e["term_type"]))

    console.print()
    console.print(top_table)


@app.command(name="setup-rime")
def setup_rime_cmd(
    dict_path: str = typer.Argument(
        "output/academic_ime.dict.yaml", help="词库 dict.yaml 路径"
    ),
) -> None:
    """一键部署到 Rime：复制词库、配置方案、应用皮肤、重新部署。"""
    path = Path(dict_path)
    console.print("[bold blue]== 一键部署 Rime ==[/bold blue]\n")
    actions = setup_rime(path)
    for action in actions:
        console.print(action)
    if any("red" in a for a in actions):
        raise typer.Exit(code=1)


theme_app = typer.Typer(help="主题/皮肤管理")
app.add_typer(theme_app, name="theme")


@theme_app.command(name="list")
def theme_list() -> None:
    """列出所有内置主题。"""
    print_theme_list()


@theme_app.command(name="install")
def theme_install(
    theme_name: str = typer.Argument(..., help="主题名称，如 cute-dog"),
    rime_dir: Optional[str] = typer.Option(
        None, "--rime-dir", help="Rime 用户目录路径，默认自动检测"
    ),
) -> None:
    """安装主题到小狼毫：备份原配置 → 写入新皮肤 → 提示部署。"""
    code = install_theme(theme_name, rime_dir=rime_dir)
    if code != 0:
        raise typer.Exit(code=code)


@theme_app.command(name="preview")
def theme_preview(
    theme_name: str = typer.Argument(..., help="主题名称，如 cute-dog"),
) -> None:
    """预览主题的 weasel.custom.yaml 内容。"""
    code = preview_theme(theme_name)
    if code != 0:
        raise typer.Exit(code=code)


@theme_app.command(name="show")
def theme_show(
    theme_name: str = typer.Argument(..., help="主题名称，如 line-puppy"),
) -> None:
    """展示主题详情：名称、说明、推荐字体、颜色色块、YAML 配置。"""
    code = show_theme(theme_name)
    if code != 0:
        raise typer.Exit(code=code)


@theme_app.command(name="uninstall")
def theme_uninstall(
    theme_name: str = typer.Argument(..., help="主题名称，如 line-puppy"),
    rime_dir: Optional[str] = typer.Option(
        None, "--rime-dir", help="Rime 用户目录路径，默认自动检测"
    ),
) -> None:
    """卸载主题：恢复备份或移除主题相关配置。"""
    code = uninstall_theme(theme_name, rime_dir=rime_dir)
    if code != 0:
        raise typer.Exit(code=code)


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
