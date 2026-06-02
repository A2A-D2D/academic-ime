# AcademicIME · 学术联想输入法

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Test](https://github.com/你的用户名/academic-ime/actions/workflows/test.yml/badge.svg)](https://github.com/你的用户名/academic-ime/actions/workflows/test.yml)

面向科研写作的中文输入法增强工具。分析论文、周报、笔记、代码注释等个人语料，自动提取学术高频词、专业短语、中英混合术语，**一键生成 Rime 输入法词库**。

> 纯本地运行 · 无需联网 · 不依赖大模型

## 安装

### 从 GitHub Releases 安装（推荐）

去 [Releases](https://github.com/你的用户名/academic-ime/releases) 下载最新的 `.whl` 文件，然后：

```bash
pip install academic_ime-0.1.0-py3-none-any.whl
```

### 从源码安装

```bash
git clone https://github.com/你的用户名/academic-ime.git
cd academic-ime
pip install -e .
```

## 三步上手

```bash
# 1. 分析你的语料，提取候选词
academic-ime extract ~/我的论文 --out output/candidates.csv

# 2. 预览 & 导出 Rime 词库
academic-ime review output/candidates.csv
academic-ime export-rime output/candidates.csv

# 3. 一键部署到 Rime（自动复制 + 配置 + 部署）
academic-ime setup-rime output/academic_ime.dict.yaml
```

> 第 3 步会自动完成：复制词库、创建扩展词典、配置简繁体方案、应用皮肤、重新部署。无需手动操作 Rime 配置。

完成！切换到小狼毫/鼠须管，正常打字，学术词汇自动出现在候选词前列。

## 试用内置示例

```bash
academic-ime init
academic-ime extract examples --out output/candidates.csv
academic-ime stats output/candidates.csv
academic-ime setup-rime output/academic_ime.dict.yaml
```

示例输出（`academic_ime.dict.yaml`）：

```
Falcon签名流程    falcon qian ming liu cheng    38000
FPU/FFT精度       fpu/fft jing du              46000
SamplerZ输出      samplerz shu chu             38000
ffSampling之间    ffsampling zhi jian          38000
范数溢出          fan shu yi chu               18000
综合数据          zong he shu ju               18000
性能面积trade-off  xing neng mian ji trade-off  33000
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
