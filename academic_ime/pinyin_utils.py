"""Pinyin conversion for Chinese, English, and mixed terms."""

from __future__ import annotations

import re
from pypinyin import lazy_pinyin


def _is_chinese(ch: str) -> bool:
    """Check if a character is a Chinese character."""
    return "一" <= ch <= "鿿"


def _segment_text(text: str) -> list[tuple[str, bool]]:
    """Split text into (segment, is_chinese) alternations.

    English parts include letters, digits, hyphens, slashes, dots.
    Chinese parts are CJK characters.
    """
    result: list[tuple[str, bool]] = []
    if not text:
        return result

    # Build regex: runs of CJK chars, runs of non-CJK
    current_is_cjk = _is_chinese(text[0])
    start = 0
    for i, ch in enumerate(text):
        ch_is_cjk = _is_chinese(ch)
        if ch_is_cjk != current_is_cjk:
            result.append((text[start:i], current_is_cjk))
            start = i
            current_is_cjk = ch_is_cjk
    result.append((text[start:], current_is_cjk))
    return result


def term_to_pinyin(term: str) -> str:
    """Convert a term to its pinyin representation.

    Chinese parts → space-separated pinyin.
    Non-Chinese parts → lowercased, preserved as-is.

    Examples:
        Falcon签名流程 → falcon qian ming liu cheng
        NTT模块 → ntt mo kuai
        SMIC40nm工艺 → smic40nm gong yi
        ffSampling模块 → ffsampling mo kuai
        ML-KEM算法 → ml-kem suan fa
        FPU/FFT精度 → fpu/fft jing du
        trade-off → trade-off
    """
    segments = _segment_text(term)
    parts: list[str] = []
    for seg, is_cjk in segments:
        if is_cjk:
            pinyins = lazy_pinyin(seg)
            parts.extend(pinyins)
        else:
            # Lowercase and strip, keep hyphens/slashes
            cleaned = seg.lower().strip()
            if cleaned:
                parts.append(cleaned)
    return " ".join(part for part in parts if part)


def english_prefix_codes(word: str, min_len: int = 3) -> list[str]:
    """Generate prefix codes for English word auto-completion.

    Example: 'history' → ['his', 'hist', 'histo', 'histor', 'history']
    Prefixes shorter than min_len are skipped to avoid noise (too many
    candidates from very short prefixes like 'h', 'hi').
    """
    word_lower = word.lower()
    if len(word_lower) <= min_len:
        return [word_lower]
    return [word_lower[:i] for i in range(min_len, len(word_lower) + 1)]


def chunk_to_pinyin(chunks: list[str]) -> str:
    """Convert a list of chunks (from jieba) into a combined pinyin string."""
    result_parts: list[str] = []
    for chunk in chunks:
        result_parts.append(term_to_pinyin(chunk))
    return " ".join(result_parts)
