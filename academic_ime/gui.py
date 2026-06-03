"""Web GUI for AcademicIME - configure domain priorities and deploy."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path
from typing import Optional

from flask import Flask, request, jsonify, render_template_string

from academic_ime.corpus_loader import load_directory
from academic_ime.term_extractor import extract_from_corpus
from academic_ime.lexicon import build_lexicon, write_csv
from academic_ime.rime_exporter import export_rime
from academic_ime.rime_setup import setup_rime
from academic_ime.domain_profiles import (
    get_domain_list,
    build_domain_lexicon,
    DOMAINS,
)

gui_app = Flask(__name__)

GUI_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AcademicIME · 学术联想输入法</title>
<style>
  :root {
    --bg: #faf8f5; --card-bg: #fff; --border: #e0d8cc;
    --text: #3d3226; --sub: #8a7b68; --accent: #b8956c;
    --accent-hover: #a07850; --green: #6b9b6b; --red: #c47a7a;
    --radius: 12px; --shadow: 0 1px 3px rgba(0,0,0,.06);
    --font: "Microsoft YaHei","PingFang SC","Helvetica Neue",sans-serif;
  }
  * { box-sizing:border-box; margin:0; padding:0 }
  body { font-family:var(--font); background:var(--bg); color:var(--text);
         line-height:1.6; padding:24px; max-width:960px; margin:0 auto }
  header { text-align:center; margin-bottom:32px }
  h1 { font-size:1.6rem; font-weight:600; color:var(--accent) }
  header p { color:var(--sub); font-size:.9rem; margin-top:4px }
  .section { background:var(--card-bg); border:1px solid var(--border);
             border-radius:var(--radius); padding:20px; margin-bottom:20px;
             box-shadow:var(--shadow) }
  .section h2 { font-size:1.05rem; margin-bottom:12px; color:var(--text);
                display:flex; align-items:center; gap:8px }
  .domains { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
             gap:12px }
  .card { background:var(--card-bg); border:1px solid var(--border);
          border-radius:var(--radius); padding:14px; cursor:pointer;
          transition:all .15s; position:relative; box-shadow:var(--shadow) }
  .card:hover { border-color:var(--accent); transform:translateY(-1px) }
  .card.active { border-color:var(--accent); background:#fdf8f0; box-shadow:0 2px 8px rgba(0,0,0,.08) }
  .card-header { display:flex; align-items:center; gap:8px; margin-bottom:6px }
  .card-icon { font-size:1.4rem }
  .card-name { font-weight:600; font-size:.95rem }
  .card-rank { position:absolute; top:10px; right:12px; font-size:.75rem;
               color:var(--accent); font-weight:700; background:#f5ede0;
               padding:2px 8px; border-radius:10px }
  .card-rank.disabled { background:#eee; color:#bbb }
  .card-desc { font-size:.78rem; color:var(--sub); line-height:1.4;
               display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
               overflow:hidden }
  .card-mult { font-size:.75rem; color:var(--accent); margin-top:6px; font-weight:500 }
  .card-mult.disabled { color:#ccc }
  .form-row { display:flex; gap:10px; align-items:center; flex-wrap:wrap }
  .form-row input { flex:1; min-width:240px; padding:10px 14px; border:1px solid var(--border);
                    border-radius:8px; font-size:.9rem; font-family:inherit; outline:none }
  .form-row input:focus { border-color:var(--accent) }
  .btn { padding:10px 24px; border:none; border-radius:8px; font-size:.9rem;
         cursor:pointer; font-weight:600; font-family:inherit; transition:all .15s }
  .btn-primary { background:var(--accent); color:#fff }
  .btn-primary:hover { background:var(--accent-hover) }
  .btn-primary:disabled { background:#e0d8cc; cursor:not-allowed }
  .btn-secondary { background:#f5ede0; color:var(--accent); border:1px solid var(--accent) }
  .btn-secondary:hover { background:#efe4d2 }
  .status { margin-top:12px; padding:10px 16px; border-radius:8px; font-size:.85rem }
  .status.info { background:#f0f4f8; color:#6b8299 }
  .status.ok { background:#e8f4e8; color:var(--green) }
  .status.err { background:#fce8e8; color:var(--red) }
  .tip { font-size:.78rem; color:var(--sub); margin-top:6px }
  .hidden { display:none }
</style>
</head>
<body>

<header>
  <h1>📚 AcademicIME · 学术联想输入法</h1>
  <p>选择学术领域并按优先级排序，一键生成专属 Rime 词库</p>
</header>

<div class="section">
  <h2>🔬 选择领域并排序优先级 <span class="tip">（点击卡片激活，激活顺序=优先级）</span></h2>
  <div class="domains" id="domains"></div>
  <div class="tip" style="margin-top:10px">
    点击卡片切换激活状态，激活顺序决定权重倍率：
    第1位 <b>3.0x</b> · 第2位 <b>2.0x</b> · 第3位 <b>1.5x</b> ·
    第4位 <b>1.3x</b> · 第5位 <b>1.1x</b> · 其余 <b>1.0x</b>
  </div>
</div>

<div class="section">
  <h2>📁 语料目录</h2>
  <div class="form-row">
    <input type="text" id="dataDir" placeholder="输入语料目录路径，如 C:\Users\me\Documents\论文" value="data">
    <button class="btn btn-primary" id="btnBuild">🚀 一键构建 & 部署到 Rime</button>
  </div>
  <div class="tip">支持 .txt .md .docx .pdf，可从论文/周报/笔记中提取专业术语</div>
  <div id="status" class="status hidden"></div>
</div>

<script>
const domains = {{ domains|tojson }};

let active = [];
let allDomains = [];

function render() {
  const container = document.getElementById('domains');
  container.innerHTML = '';
  allDomains.forEach((d, i) => {
    const rank = active.indexOf(d.id);
    const isActive = rank >= 0;
    const mult = getMultiplier(rank);
    const div = document.createElement('div');
    div.className = 'card' + (isActive ? ' active' : '');
    div.onclick = () => toggle(d.id);
    div.innerHTML =
      '<div class="card-header">' +
        '<span class="card-icon">' + d.icon + '</span>' +
        '<span class="card-name">' + d.name + '</span>' +
      '</div>' +
      '<div class="card-desc">' + d.description + '</div>' +
      (isActive
        ? '<div class="card-rank">#' + (rank+1) + ' · ' + mult.toFixed(1) + 'x</div>'
        : '<div class="card-rank disabled">未激活</div>') +
      (isActive
        ? '<div class="card-mult">' + d.word_count + ' 个专业词汇</div>'
        : '<div class="card-mult disabled">' + d.word_count + ' 个专业词汇</div>');
    container.appendChild(div);
  });
  document.getElementById('btnBuild').disabled = active.length === 0;
}

function getMultiplier(rank) {
  if (rank === 0) return 3.0;
  if (rank === 1) return 2.0;
  if (rank === 2) return 1.5;
  if (rank === 3) return 1.3;
  if (rank === 4) return 1.1;
  return 1.0;
}

function toggle(id) {
  const idx = active.indexOf(id);
  if (idx >= 0) {
    active.splice(idx, 1);
  } else {
    active.push(id);
  }
  render();
}

async function loadDomains() {
  const resp = await fetch('/api/domains');
  const data = await resp.json();
  allDomains = data;
  active = [];
  render();
}

async function build() {
  const dir = document.getElementById('dataDir').value.trim();
  if (!dir) { showStatus('请输入语料目录路径', 'err'); return; }
  if (active.length === 0) { showStatus('请至少选择一个领域', 'err'); return; }

  const btn = document.getElementById('btnBuild');
  btn.disabled = true;
  btn.textContent = '⏳ 正在构建...';
  showStatus('正在提取术语、构建词库...', 'info');

  try {
    const resp = await fetch('/api/build', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({data_dir: dir, domains: active})
    });
    const result = await resp.json();
    if (result.ok) {
      showStatus(result.message, 'ok');
    } else {
      showStatus(result.message, 'err');
    }
  } catch(e) {
    showStatus('构建失败: ' + e.message, 'err');
  }
  btn.disabled = false;
  btn.textContent = '🚀 一键构建 & 部署到 Rime';
}

function showStatus(msg, cls) {
  const el = document.getElementById('status');
  el.className = 'status ' + cls;
  el.textContent = msg;
  el.classList.remove('hidden');
}

document.getElementById('btnBuild').addEventListener('click', build);
loadDomains();
</script>
</body>
</html>"""


@gui_app.route("/")
def index():
    return render_template_string(GUI_HTML, domains=json.dumps(_get_domain_data()))


def _get_domain_data() -> list[dict]:
    """Return domain list with word counts for the frontend."""
    result = []
    for d in get_domain_list():
        d_copy = dict(d)
        d_copy["word_count"] = len(DOMAINS[d["id"]]["words"])
        result.append(d_copy)
    return result


@gui_app.route("/api/domains")
def api_domains():
    return jsonify(_get_domain_data())


@gui_app.route("/api/build", methods=["POST"])
def api_build():
    data = request.get_json()
    data_dir = data.get("data_dir", "data")
    domain_ids = data.get("domains", [])

    if not domain_ids:
        return jsonify({"ok": False, "message": "请至少选择一个领域"})

    try:
        root = Path(data_dir)
        if not root.exists():
            return jsonify({"ok": False, "message": f"语料目录不存在: {data_dir}"})

        # 1. Extract from corpus
        file_contents = load_directory(root)
        corpus_msg = ""
        term_freq = {}
        term_sources = {}
        if file_contents:
            from collections import Counter
            term_freq, term_sources = extract_from_corpus(file_contents)
            corpus_msg = f"从 {len(file_contents)} 个文件中提取了 {len(term_freq)} 个候选词"
        else:
            from collections import Counter
            term_freq, term_sources = Counter(), Counter()
            corpus_msg = "语料目录为空，仅使用领域词库"

        # 2. Build domain lexicon with priorities
        domain_priorities = [(did, i + 1) for i, did in enumerate(domain_ids)]
        domain_entries = build_domain_lexicon(domain_priorities)

        # 3. Merge domain entries into term_freq
        from collections import Counter as Ctr
        combined_freq = Ctr(term_freq)
        combined_sources = Ctr(term_sources)
        for word, _, _ in domain_entries:
            combined_freq[word] = max(combined_freq.get(word, 0), 1)
            combined_sources[word] += 1

        # 4. Build lexicon
        entries = build_lexicon(combined_freq, combined_sources, include_common_en=True)

        # Apply domain weight multipliers
        domain_weight_map: dict[str, float] = {}
        for did, rank in domain_priorities:
            domain_weight_map[did] = get_domain_weight_multiplier(did, rank)

        # Boost weights for domain words
        domain_words_set: set[str] = set()
        for did in domain_ids:
            for word, _ in DOMAINS[did]["words"]:
                domain_words_set.add(word.lower())

        for entry in entries:
            if entry["term"].lower() in domain_words_set:
                # Find which domain and apply its multiplier
                for did in domain_ids:
                    for word, _ in DOMAINS[did]["words"]:
                        if word.lower() == entry["term"].lower():
                            mult = domain_weight_map.get(did, 1.0)
                            entry["weight"] = min(100000, int(entry["weight"] * mult))
                            break

        # 5. Write CSV
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        csv_path = out_dir / "candidates.csv"
        write_csv(entries, csv_path)

        # 6. Export Rime dict
        rime_path = out_dir / "academic_ime.dict.yaml"
        export_rime(entries, rime_path)

        # 7. Deploy to Rime
        deploy_msgs = setup_rime(rime_path)
        deploy_ok = not any("red" in m for m in deploy_msgs)

        domain_names = ", ".join(
            DOMAINS[did]["name"] for did in domain_ids if did in DOMAINS
        )

        msg = (
            f"✅ 构建完成！\n"
            f"{corpus_msg}\n"
            f"领域词库: {domain_names} ({len(domain_entries)} 词)\n"
            f"总计: {len(entries)} 个词条\n"
            f"已部署到 Rime → {rime_path}\n\n"
            f"⚠️ 请右键小狼毫托盘图标 → 重新部署 使词库生效"
        )
        return jsonify({"ok": True, "message": msg})

    except Exception as e:
        return jsonify({"ok": False, "message": f"构建失败: {str(e)}"})


def get_domain_weight_multiplier(domain_id: str, priority_rank: int | None = None) -> float:
    """Re-export from domain_profiles for use in gui module."""
    from academic_ime.domain_profiles import get_domain_weight_multiplier as _fn
    return _fn(domain_id, priority_rank)


def start_gui(port: int = 5278, open_browser: bool = True) -> None:
    """Start the AcademicIME GUI web server.

    Args:
        port: Port to listen on (default 5278).
        open_browser: Whether to automatically open the browser.
    """
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()

    print(f"\n  AcademicIME GUI 已启动 → http://127.0.0.1:{port}")
    print(f"  按 Ctrl+C 停止服务器\n")

    gui_app.run(host="127.0.0.1", port=port, debug=False)
