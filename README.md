# AcademicIME · 学术联想输入法

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Test](https://github.com/A2A-D2D/academic-ime/actions/workflows/test.yml/badge.svg)](https://github.com/A2A-D2D/academic-ime/actions/workflows/test.yml)

面向科研写作的中文输入法增强工具。分析论文、周报、笔记、代码注释等个人语料，自动提取学术高频词、专业短语、中英混合术语，**一键生成 Rime 输入法词库**。

> 纯本地运行 · 无需联网 · 不依赖大模型

## 安装

### 从 GitHub Releases 安装（推荐）

去 [Releases](https://github.com/A2A-D2D/academic-ime/releases) 下载最新的 `.whl` 文件，然后：

```bash
pip install academic_ime-0.1.0-py3-none-any.whl
```

### 从源码安装

```bash
git clone https://github.com/A2A-D2D/academic-ime.git
cd academic-ime
pip install -e .
```

## 使用指南

### 场景一：刚安装，上传最近的文档建词库

把最近写的论文、周报、笔记放到一个文件夹里，一行命令搞定：

```bash
# 把文档放到 data/ 目录
# 支持格式：.txt .md .docx .pdf
cp ~/Documents/本周周报.md data/
cp ~/Documents/芯片验证笔记.txt data/

# 提取术语 → 导出词库 → 一键部署
academic-ime extract data/ --out output/candidates.csv
academic-ime export-rime output/candidates.csv
academic-ime setup-rime output/academic_ime.dict.yaml
```

之后写新文档时把新文件丢进 `data/`，重新跑一次即可增量更新词库。

> 文档越多，覆盖越全。建议至少放 3-5 篇代表性的论文或周报。

### 场景二：已有词库，提高某些词的优先级

如果已经生成过 `output/candidates.csv`，想手动调整某些词的权重：

```bash
# 1. 查看当前词库
academic-ime review output/candidates.csv

# 2. 用 Excel / VS Code 打开 candidates.csv
#    - 把想优先出现的词 weight 调高（最大值 100000）
#    - 不想出现的词 enabled 改为 0
#    - 词条类型：zh=中文 en=英文 mixed=中英混合 phrase=短语

# 3. 重新导出 & 部署
academic-ime export-rime output/candidates.csv
academic-ime setup-rime output/academic_ime.dict.yaml
```

> 每次修改 CSV 后重新 export + setup-rime 即可生效，Rime 会自动重建索引。

### 快速试用

项目自带一篇示例语料，可以立即体验效果：

```bash
academic-ime init
academic-ime extract examples --out output/candidates.csv
academic-ime stats output/candidates.csv
academic-ime setup-rime output/academic_ime.dict.yaml
```

## CLI 命令

| 命令 | 作用 |
|------|------|
| `academic-ime init` | 初始化项目目录和配置文件 |
| `academic-ime extract <dir>` | 从语料目录提取候选词 → CSV |
| `academic-ime review <csv>` | 终端表格预览候选词（按权重排序） |
| `academic-ime export-rime <csv>` | 导出 Rime dict.yaml 词库 |
| `academic-ime stats <csv>` | 显示词库统计和 Top 20 |
| `academic-ime setup-rime <dict>` | **一键部署到 Rime**（复制+配置+皮肤+部署） |
| `academic-ime theme list` | 列出内置主题 |
| `academic-ime theme show <name>` | 展示主题详情（含颜色预览色块） |
| `academic-ime theme preview <name>` | 预览皮肤 YAML 内容 |
| `academic-ime theme install <name>` | 安装皮肤（自动备份原配置） |
| `academic-ime theme uninstall <name>` | 卸载皮肤（恢复备份或移除配置） |

### 主题 / 皮肤

内置 4 款小狼毫皮肤：

| 主题 | 命令 | 说明 |
|------|------|------|
| 线条小狗 | `cute-dog` | 奶油白背景、浅棕边框、粉色高亮、🐾 标签、🐶 选中标记、圆角阴影 |
| 线条小狗 | `line-puppy` | 浅米白背景、浅奶黄高亮、棕色文字、细圆角手账风，纯配色实现 |
| 学术蓝 | `academic-blue` | 浅蓝灰背景、蓝色高亮，清爽专业 |
| 极简暗色 | `minimal-dark` | 深色背景、低对比度，适合夜间 |

```bash
# 列出所有主题
academic-ime theme list

# 查看主题详情（含颜色色块预览）
academic-ime theme show line-puppy

# 预览 YAML 配置
academic-ime theme preview line-puppy

# 安装主题（自动备份原有 weasel.custom.yaml → .bak.academic-ime）
academic-ime theme install line-puppy

# 卸载主题（自动恢复备份或移除相关配置）
academic-ime theme uninstall line-puppy
```

安装后需要：右键小狼毫托盘图标 → 重新部署

> 小狼毫原生皮肤主要支持颜色、字体、布局、圆角等，不支持直接在候选框插入 PNG/SVG 图片。所有主题均使用纯配色 + 布局实现，不依赖任何外部素材。

### CSV 字段

| 字段 | 说明 |
|------|------|
| term | 词条原文 |
| pinyin | 拼音（英文部分保留原文） |
| weight | 权重 1000-100000 |
| source_count | 来源文件数 |
| term_type | zh / en / mixed / phrase |
| enabled | 1=启用，0=禁用（可手动编辑 CSV 筛选） |

## 提取能力

| 类型 | 示例 | 说明 |
|------|------|------|
| 中文词 | 范数溢出、综合数据 | jieba 分词 + 停用词过滤 |
| 英文缩写 | `FPU`, `NTT`, `FPU/FFT` | 大写缩写、斜杠组合 |
| 驼峰术语 | `ffSampling`, `SamplerZ` | 代码中常见的驼峰命名 |
| 连字符术语 | `trade-off`, `ML-KEM` | 学术论文常见写法 |
| 中英混合 | `Falcon签名`, `NTT模块` | 英文术语 + 中文上下文 |
| N-gram 短语 | `签名流程联调` | 2-4 gram 学术短语 |

## 技术栈

python 3.8+ · typer · rich · jieba · pypinyin · python-docx · pypdf · pytest

## 后续规划

- [ ] 交互式词条筛选 TUI
- [ ] 自定义停用词表
- [ ] 学术领域模板（芯片/算法/生物等）
- [ ] 增量语料导入
- [ ] LaTeX 文件支持
- [ ] 更多输出格式
