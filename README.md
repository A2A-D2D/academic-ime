# AcademicIME · 学术联想输入法

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Test](https://github.com/A2A-D2D/academic-ime/actions/workflows/test.yml/badge.svg)](https://github.com/A2A-D2D/academic-ime/actions/workflows/test.yml)

面向科研写作的中文输入法增强工具。分析论文、周报、笔记、代码注释等个人语料，自动提取学术高频词、专业短语、中英混合术语，**一键生成 Rime 输入法词库**。

> 纯本地运行 · 无需联网 · 不依赖大模型

---

## 📦 下载安装

### Windows 用户：下载 EXE（推荐）

无需装 Python，一个文件即可使用：

1. 打开 [http://39.105.75.142](http://39.105.75.142) 下载 `academic-ime.exe`（54 MB）
2. 把 EXE 放到任意目录
3. 终端运行 `./academic-ime.exe init` 初始化

> 或从 [GitHub Releases](https://github.com/A2A-D2D/academic-ime/releases/latest) 下载 EXE

### macOS / Linux 用户：pip 安装

```bash
# 从 GitHub Releases 下载 .whl 后：
pip install academic_ime-0.2.0-py3-none-any.whl

# 或从源码安装：
git clone https://github.com/A2A-D2D/academic-ime.git
cd academic-ime
pip install -e .
```

---

## 核心特性

| 🎯 | 能力 |
|-----|------|
| 📚 **14 个专业领域** | 外交、法律、芯片、医学、金融、会计、教育、建筑、机械、化学、环境、游戏、日常、学术，每个 ~120 个专业词汇 |
| 🖥️ **Web 图形界面** | 浏览器里点卡片选领域、排优先级，一键构建部署到 Rime |
| 🔤 **英文联想 + 补全** | 输入 `his` → 联想 `history`；输入 `Falcon` → 联想 `Falcon签名流程` |
| 📄 **多格式语料** | 支持 `.txt` `.md` `.docx` `.pdf`，从论文/周报/笔记中自动提取专业术语 |
| 🎨 **4 款原创皮肤** | 线条小狗、学术蓝、极简暗色，纯配色实现 |
| 📦 **单文件 EXE** | Windows 用户下载即用，无需 Python 环境 |

---

## 📋 前提条件

- **需要安装小狼毫输入法**（[Weasel](https://rime.im/download/)）并至少运行过一次
- EXE 版本无需 Python；pip 版本需要 Python 3.8+

---

## 💡 选择你的使用方式

- **我下载了 EXE** → 跳到 [🖥️ Web 界面](#web-界面) 或 [⌨️ 命令行使用](#命令行使用)
- **我懒得记命令** → 跳到 [🖥️ Web 界面](#web-界面)
- **我愿意敲命令** → 跳到 [⌨️ 命令行使用](#命令行使用)
- **我想看效果再决定** → 跳到 [🚀 30 秒快速试用](#30-秒快速试用)

---

## 🖥️ Web 界面

浏览器里点一点就能配好词库，不用记任何命令。

### 第 1 步：安装

- **EXE 用户**：下载后直接使用，跳过此步
- **pip 用户**：`pip install academic_ime-0.2.0-py3-none-any.whl`

### 第 2 步：启动

```bash
academic-ime gui
# EXE 用户用：./academic-ime.exe gui
```

浏览器会自动打开一个面板 👇

### 第 3 步：在浏览器里操作

1. **选领域** — 页面上有 14 个领域卡片（外交、法律、芯片、医学、金融、会计、教育、建筑、机械、化学、环境、游戏、日常、学术），点击卡片激活你需要的领域

2. **排优先级** — 先点的领域排在最前面，权重最高（第 1 位 = 3.0 倍权重，第 2 位 = 2.0 倍 ... 第 5 位及以后 = 1.0 倍）

   > 比如你是会计专业，先点「会计/审计」再点「日常用语」再点「金融/经济」，这样会计术语会优先出现在候选词最前面

3. **选语料目录** — 在输入框里填你的文档目录（论文、周报、笔记所在的文件夹），支持 `.txt` `.md` `.docx` `.pdf`

4. **点「一键构建 & 部署」** 按钮

5. **右键小狼毫托盘图标 → 重新部署**

完成！现在打字试试，你选的领域词汇会优先出现。

> 💡 如果语料目录留空或没有文档，系统会只使用你选的领域词库，也能用。

---

## ⌨️ 命令行使用

适合习惯终端操作的用户。

### 第 1 步：安装

- **EXE 用户**：下载 `academic-ime.exe` 后直接使用，注意命令前面加 `./`
- **pip 用户**：`pip install academic_ime-0.2.0-py3-none-any.whl`

### 第 2 步：准备文档

把你的论文、周报、笔记放到一个文件夹里，比如 `data/`：

```
data/
├── 本周周报.md
├── 芯片验证笔记.txt
├── 论文初稿.docx
└── 参考文献.pdf
```

> 支持格式：`.txt` `.md` `.docx` `.pdf` · 建议至少放 3-5 篇

### 第 3 步：三条命令部署

```bash
# ① 提取术语 → 生成候选词 CSV
academic-ime extract data/ --out output/candidates.csv

# ② 导出 Rime 词库文件
academic-ime export-rime output/candidates.csv

# ③ 一键部署到小狼毫
academic-ime setup-rime output/academic_ime.dict.yaml
```

### 第 4 步：重新部署 Rime

右键小狼毫托盘图标 → **重新部署**。完成！

> 💡 以后有了新文档，丢进 `data/` 目录再跑一遍第 3 步的三条命令即可增量更新。

---

## 🔧 高级技巧

### 手动调整词条权重

如果你对自动生成的词库不满意，可以手动编辑 CSV：

```bash
# 先看看当前词库长什么样
academic-ime review output/candidates.csv

# 用 Excel / VS Code 打开 output/candidates.csv
```

| 字段 | 含义 | 怎么改 |
|------|------|--------|
| `weight` | 权重，越大越靠前 | 调高想要的词（最大 100000） |
| `enabled` | 1=启用 0=禁用 | 不想出现的词改成 0 |
| `term_type` | zh/en/mixed/phrase | 不用改 |

改完 CSV 后：
```bash
academic-ime export-rime output/candidates.csv
academic-ime setup-rime output/academic_ime.dict.yaml
# 右键 Rime → 重新部署
```

### 查看词库统计

```bash
academic-ime stats output/candidates.csv
# 显示总词条数、启用数、各类型分布、Top 20
```

---

## 🚀 30 秒快速试用

项目自带一篇芯片验证示例，不用准备文档就能体验：

```bash
academic-ime init                           # 初始化目录
academic-ime extract examples --out output/candidates.csv   # 提取
academic-ime stats output/candidates.csv    # 看看提取了啥
academic-ime setup-rime output/academic_ime.dict.yaml       # 部署
```

示例输出：

```
Falcon签名流程    falcon qian ming liu cheng    38000
FPU/FFT精度       fpu/fft jing du              46000
SamplerZ输出      samplerz shu chu             38000
范数溢出          fan shu yi chu               18000
性能面积trade-off  xing neng mian ji trade-off  33000
```

## 内置领域词库（14 个）

每个领域约 120 个专业词汇，共 ~1680 词。在 GUI 中选择领域并排序，系统自动加权匹配。

| 领域 | 图标 | 覆盖范围 |
|------|------|----------|
| 外交/国际关系 | 🌐 | 联合国、条约、多边机制、地缘政治 |
| 法律/政策 | ⚖️ | 司法程序、知识产权、合规监管 |
| 计算机/芯片 | 💻 | 半导体、处理器架构、EDA、RISC-V |
| 医学/生物 | 🧬 | 临床医学、基因编辑、药物研发 |
| 金融/经济 | 📈 | 宏观经济、证券交易、风险管理 |
| 会计/审计 | 🧾 | 财务报告、审计核查、税务筹划 |
| 教育/心理 | 🎓 | 课程设计、认知科学、心理健康 |
| 建筑/土木 | 🏗️ | 结构设计、岩土工程、城市规划 |
| 机械/汽车 | ⚙️ | 机械设计、新能源汽车、制造工艺 |
| 化学/材料 | 🧪 | 合成催化、材料表征、化工工艺 |
| 环境/能源 | 🌱 | 碳中和、可再生能源、ESG |
| 游戏/娱乐 | 🎮 | 游戏设计、电竞、二次元 |
| 日常用语 | 📝 | 办公沟通、邮件、日程、出行 |
| 学术通用 | 📚 | 论文写作、研究方法、发表流程 |

## CLI 命令参考

| 命令 | 作用 |
|------|------|
| `academic-ime gui` | **🖥️ 启动 Web 界面**（推荐） |
| `academic-ime init` | 初始化项目目录 |
| `academic-ime extract <dir>` | 从语料提取候选词 → CSV |
| `academic-ime review <csv>` | 表格预览候选词 |
| `academic-ime export-rime <csv>` | 导出 Rime dict.yaml |
| `academic-ime stats <csv>` | 词库统计 + Top 20 |
| `academic-ime setup-rime <dict>` | **一键部署到 Rime** |
| `academic-ime theme list` | 列出内置皮肤 |
| `academic-ime theme show <name>` | 皮肤详情 + 颜色预览 |
| `academic-ime theme install <name>` | 安装皮肤（自动备份） |
| `academic-ime theme uninstall <name>` | 卸载皮肤（恢复备份） |

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

- [x] Web 图形界面 + 14 个领域词库
- [x] 英文前缀补全（his → history）
- [x] 英文联想词（Falcon → Falcon签名流程）
- [ ] 自定义停用词表
- [ ] 增量语料导入（不重复处理已有文档）
- [ ] LaTeX 文件支持（`.tex`）
- [ ] 更多输出格式（搜狗、百度、QQ 拼音）
- [ ] 领域词库社区贡献机制
