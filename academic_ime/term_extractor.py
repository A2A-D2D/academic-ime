"""Term extraction: Chinese words, English terms, mixed phrases, n-gram phrases."""

from __future__ import annotations

import re
from collections import Counter

import jieba

from academic_ime.config import (
    STOPWORDS,
    MIN_ZH_WORD_LEN,
    MAX_PHRASE_LEN,
    MIN_PHRASE_LEN,
    MIN_NGRAM,
    MAX_NGRAM,
    MAX_MIXED_CHINESE_CHARS,
)

# Pattern for English/international terms
_RE_ENGLISH = re.compile(
    r"\b(?:"
    r"[A-Z]{2,}(?:/[A-Z]{2,})*[a-z]*\d*(?:nm|um|mm|cm|km|hz|khz|mhz|ghz|bit|byte|bytes)?"
    r"|"
    r"[a-z]+[A-Z][a-zA-Z]*\d*"
    r"|"
    r"[A-Z][a-z]+(?:[A-Z][a-z]*)*\d*"
    r"|"
    r"[A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)*\d*"
    r")\b"
)

_RE_MIXED = re.compile(r"[A-Za-z][A-Za-z0-9\-/]*[一-鿿]+")


def _is_pure_number(s: str) -> bool:
    return bool(re.match(r"^[\d.,万万千百万亿\s]+$", s))


def extract_chinese_words(text: str) -> list[str]:
    """Extract Chinese words using jieba segmentation.

    Filters: length >= 2, non-stopword, non-pure-number.
    """
    words = jieba.lcut(text)
    result: list[str] = []
    for w in words:
        w = w.strip()
        if len(w) < MIN_ZH_WORD_LEN:
            continue
        if w in STOPWORDS:
            continue
        if _is_pure_number(w):
            continue
        # Must contain at least one Chinese character
        if not re.search(r"[一-鿿]", w):
            continue
        result.append(w)
    return result


def extract_english_terms(text: str) -> list[str]:
    """Extract English/acronym terms like NTT, ffSampling, SMIC40nm, FPU/FFT."""
    matches = _RE_ENGLISH.findall(text)
    return [m.strip() for m in matches if len(m.strip()) >= 2]


def extract_mixed_phrases(text: str, english_terms: list[str]) -> list[str]:
    """Extract mixed Chinese-English phrases.

    Uses English terms as anchors and looks for surrounding Chinese text
    to form mixed phrases like 'Falcon签名', 'NTT模块', 'SamplerZ输出'.
    """
    if not english_terms:
        return []

    results: list[str] = []
    seen: set[str] = set()

    for term in english_terms:
        # Find occurrences of this term in text
        for m in re.finditer(re.escape(term), text):
            start = m.start()
            # Look at surrounding Chinese chars (up to MAX_MIXED_CHINESE_CHARS chars)
            # Before: skip non-CJK, non-ASCII whitespace/punctuation
            pre_chars = ""
            i = start - 1
            while i >= 0 and len(pre_chars) < MAX_MIXED_CHINESE_CHARS:
                ch = text[i]
                if "一" <= ch <= "鿿":
                    pre_chars = ch + pre_chars
                    i -= 1
                elif ch.isspace() or (ch.isascii() and not ch.isalnum()):
                    i -= 1  # skip whitespace/punctuation between en and zh
                else:
                    break

            # After: skip non-CJK, non-ASCII whitespace/punctuation
            end = m.end()
            post_chars = ""
            j = end
            while j < len(text) and len(post_chars) < MAX_MIXED_CHINESE_CHARS:
                ch = text[j]
                if "一" <= ch <= "鿿":
                    post_chars += ch
                    j += 1
                elif ch.isspace() or (ch.isascii() and not ch.isalnum()):
                    j += 1  # skip whitespace/punctuation
                else:
                    break

            # Build mixed phrases of varying lengths
            for pre_len in range(0, len(pre_chars) + 1):
                pre_part = pre_chars[-pre_len:] if pre_len > 0 else ""
                for post_len in range(0, len(post_chars) + 1):
                    post_part = post_chars[:post_len] if post_len > 0 else ""
                    # At least 2 Chinese chars total
                    if pre_len + post_len < 2:
                        continue
                    phrase = f"{pre_part}{term}{post_part}"
                    phrase = phrase.strip()
                    if MIN_PHRASE_LEN <= len(phrase) <= MAX_PHRASE_LEN:
                        if phrase not in seen:
                            seen.add(phrase)
                            results.append(phrase)

    return results


def extract_ngram_phrases(words: list[str]) -> list[str]:
    """Generate 2-gram, 3-gram, 4-gram phrases from a token list.

    Filters: length 3-20 chars, not start/end with stopword, not too much punctuation.
    """
    results: list[str] = []
    seen: set[str] = set()

    for n in range(MIN_NGRAM, MAX_NGRAM + 1):
        for i in range(len(words) - n + 1):
            gram = words[i : i + n]
            phrase = "".join(gram).strip()

            if len(phrase) < MIN_PHRASE_LEN or len(phrase) > MAX_PHRASE_LEN:
                continue
            if gram[0] in STOPWORDS or gram[-1] in STOPWORDS:
                continue
            # Must have at least some Chinese or be mixed
            if not re.search(r"[一-鿿]", phrase):
                continue
            # Reject phrases that are mostly punctuation
            punct_ratio = sum(1 for c in phrase if c in "，。；：！？、（）\"\"''《》【】…—·")
            if punct_ratio / len(phrase) > 0.3:
                continue
            if phrase not in seen:
                seen.add(phrase)
                results.append(phrase)

    return results


def extract_english_anchored_phrases(
    text: str,
    english_terms: list[str],
    max_following: int = 6,
    min_zh: int = 2,
    max_zh: int = 5,
) -> list[str]:
    """Generate联想词 phrases anchored on English terms.

    For each English term, finds the following Chinese words in the text
    and creates combined phrases like 'Falcon签名', 'FPU/FFT精度'.
    This enables English-to-Chinese联想 when typing English terms.
    """
    if not english_terms:
        return []

    results: list[str] = []
    seen: set[str] = set()

    for term in english_terms:
        for m in re.finditer(re.escape(term), text):
            end = m.end()
            # Collect Chinese chars from following text
            zh_chars = ""
            j = end
            while j < len(text) and len(zh_chars) < max_following:
                ch = text[j]
                if "一" <= ch <= "鿿":
                    zh_chars += ch
                elif ch.isspace() or (ch.isascii() and not ch.isalnum()):
                    pass  # Skip whitespace/punctuation
                else:
                    break
                j += 1

            if len(zh_chars) < min_zh:
                continue

            # Generate phrases: term + N zh chars (2-5 chars works best)
            for n in range(min_zh, min(len(zh_chars) + 1, max_zh + 1)):
                zh_part = zh_chars[:n]
                phrase = f"{term}{zh_part}".strip()
                if MIN_PHRASE_LEN <= len(phrase) <= MAX_PHRASE_LEN:
                    if phrase not in seen:
                        seen.add(phrase)
                        results.append(phrase)

    return results


def classify_term(term: str) -> str:
    """Classify a term as 'zh', 'en', 'mixed', or 'phrase'.

    - 'zh': pure Chinese
    - 'en': pure English/international
    - 'mixed': contains both Chinese and English
    - 'phrase': Chinese but multi-word phrase (3+ chars)
    """
    has_cjk = bool(re.search(r"[一-鿿]", term))
    has_eng = bool(re.search(r"[A-Za-z]", term))

    if has_cjk and has_eng:
        return "mixed"
    if has_cjk:
        return "zh"
    return "en"


def extract_terms(text: str, filename: str = "") -> Counter:
    """Extract all candidate terms from a text corpus.

    Returns a Counter of term → frequency pairs.
    The filename is used for source tracking.
    """
    results: Counter = Counter()

    # 1. English terms (these are high-priority)
    eng_terms = extract_english_terms(text)
    results.update(eng_terms)

    # 2. Mixed Chinese-English phrases
    mixed = extract_mixed_phrases(text, eng_terms)
    results.update(mixed)

    # 3. Chinese word segmentation
    zh_words = extract_chinese_words(text)
    results.update(zh_words)

    # 4. N-gram phrases from segmented words
    phrases = extract_ngram_phrases(zh_words)
    results.update(phrases)

    # 5. English-anchored phrases (联想词 for English terms)
    eng_anchored = extract_english_anchored_phrases(text, eng_terms)
    results.update(eng_anchored)

    return results


def extract_from_corpus(file_contents: list[tuple[str, str]]) -> tuple[Counter, Counter]:
    """Extract terms from multiple files.

    Args:
        file_contents: list of (filename, text) tuples.

    Returns:
        (term_freq_counter, term_source_counter)
        term_freq_counter: term → total frequency
        term_source_counter: term → number of files containing it
    """
    term_freq: Counter = Counter()
    term_sources: Counter = Counter()

    for filename, text in file_contents:
        file_terms = extract_terms(text, filename)
        term_freq.update(file_terms)
        for term in set(file_terms.keys()):
            term_sources[term] += 1

    return term_freq, term_sources
