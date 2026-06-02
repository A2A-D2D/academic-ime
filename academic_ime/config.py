"""Global constants for AcademicIME."""

from __future__ import annotations

STOPWORDS: set[str] = {
    "的", "了", "和", "是", "在", "对", "与", "及", "进行", "一个",
    "通过", "可以", "也", "都", "但", "被", "从", "到", "中", "上",
    "下", "着", "过", "之", "而", "或", "其", "这", "那", "等",
    "有", "不", "为", "以", "就", "要", "会", "能", "将", "向",
    "前", "后", "所", "更", "已", "还", "又", "再", "最", "至",
    "于", "并", "如", "每", "各", "该", "此", "则", "且", "让",
    "把", "用", "很", "非常", "更", "比较", "较", "相对", "基本",
    "主要", "相关", "相应", "一般", "通常", "一种", "一些", "一些",
    "针对", "结合", "同时", "根据", "按照", "通过", "采用",
    "个", "些", "种", "样", "项", "条", "篇", "次", "点",
    "什么", "怎样", "如何", "为何", "哪里", "哪", "谁",
}

# Minimum / maximum lengths for extracted terms
MIN_ZH_WORD_LEN = 2
MAX_PHRASE_LEN = 20
MIN_PHRASE_LEN = 3
MIN_NGRAM = 2
MAX_NGRAM = 4
MAX_MIXED_CHINESE_CHARS = 6

# Weight constants
BASE_WEIGHT = 10000
FREQ_MULTIPLIER = 1000
BONUS_MIXED = 20000
BONUS_PHRASE = 10000
BONUS_UPPER_ABBR = 8000
BONUS_LENGTH_OPTIMAL = 5000
BONUS_MULTI_SOURCE = 2000
MIN_WEIGHT = 1000
MAX_WEIGHT = 100000

# Regex patterns
RE_ENGLISH_TERM = r"([A-Z]+(?:/[A-Z]+)*[a-z]*\d*(?:nm|um|mm|cm|km|hz|khz|mhz|ghz|bit|byte|bytes|b|kb|mb|gb)?|[a-z]+[A-Z][a-zA-Z]*\d*|[A-Z]+-[A-Z]+[a-z]*)"
