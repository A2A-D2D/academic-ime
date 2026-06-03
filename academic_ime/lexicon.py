"""Weight calculation and CSV I/O for candidate terms."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

from academic_ime.config import (
    BASE_WEIGHT,
    FREQ_MULTIPLIER,
    BONUS_MIXED,
    BONUS_PHRASE,
    BONUS_UPPER_ABBR,
    BONUS_LENGTH_OPTIMAL,
    BONUS_MULTI_SOURCE,
    MIN_WEIGHT,
    MAX_WEIGHT,
)
from academic_ime.pinyin_utils import term_to_pinyin, english_prefix_codes
from academic_ime.term_extractor import classify_term


def calculate_weight(
    term: str,
    freq: int,
    source_count: int,
    term_type: str | None = None,
) -> int:
    """Calculate the weight for a candidate term.

    Formula:
        weight = BASE + freq * FREQ_MULTIPLIER + bonuses

    Bonuses:
        - mixed term: +20000
        - phrase term: +10000
        - contains uppercase acronym: +8000
        - length 4-12: +5000
        - multi-source: +source_count * 2000
    """
    if term_type is None:
        term_type = classify_term(term)

    weight = BASE_WEIGHT + freq * FREQ_MULTIPLIER

    if term_type == "mixed":
        weight += BONUS_MIXED
    elif term_type == "phrase":
        weight += BONUS_PHRASE

    if re.search(r"[A-Z]{2,}", term):
        weight += BONUS_UPPER_ABBR

    if 4 <= len(term) <= 12:
        weight += BONUS_LENGTH_OPTIMAL

    weight += source_count * BONUS_MULTI_SOURCE

    return max(MIN_WEIGHT, min(MAX_WEIGHT, weight))


def build_lexicon(
    term_freq: Counter,
    term_sources: Counter,
    include_common_en: bool = True,
) -> list[dict[str, str | int]]:
    """Build the candidate lexicon from frequency and source counters.

    Args:
        term_freq: term → frequency counter from corpus extraction.
        term_sources: term → number of source files.
        include_common_en: if True, merge built-in common English word list.

    Returns a list of dicts with keys: term, pinyin, weight, source_count, term_type, enabled.
    """
    entries: list[dict[str, str | int]] = []
    seen: set[str] = set()
    seen_prefix: set[tuple[str, str]] = set()  # (term_lower, prefix_code) dedup

    for term, freq in term_freq.items():
        source_count = term_sources.get(term, 1)
        term_type = classify_term(term)
        pinyin = term_to_pinyin(term)
        weight = calculate_weight(term, freq, source_count, term_type)

        entries.append({
            "term": term,
            "pinyin": pinyin,
            "weight": weight,
            "source_count": source_count,
            "term_type": term_type,
            "enabled": 1,
        })
        seen.add(term.lower())

        # Generate prefix entries for English terms (auto-completion)
        if term_type == "en" and len(term) >= 4:
            for prefix_code in english_prefix_codes(term):
                if prefix_code == pinyin:
                    continue  # Skip the full-length code (already the main entry)
                key = (term.lower(), prefix_code)
                if key in seen_prefix:
                    continue
                seen_prefix.add(key)
                entries.append({
                    "term": term,
                    "pinyin": prefix_code,
                    "weight": weight - 1000,  # Slightly lower than exact match
                    "source_count": source_count,
                    "term_type": term_type,
                    "enabled": 1,
                })

    # Merge common English words (lower weight, as baseline vocabulary)
    if include_common_en:
        from academic_ime.wordlist import COMMON_ENGLISH

        for word, rank in COMMON_ENGLISH:
            if word.lower() in seen:
                continue
            weight = max(1000, 5000 - rank * 4)
            entries.append({
                "term": word,
                "pinyin": word.lower(),
                "weight": weight,
                "source_count": 0,
                "term_type": "en",
                "enabled": 1,
            })
            seen.add(word.lower())

            # Generate prefix entries for auto-completion
            if len(word) >= 4:
                for prefix_code in english_prefix_codes(word):
                    if prefix_code == word.lower():
                        continue
                    key = (word.lower(), prefix_code)
                    if key in seen_prefix:
                        continue
                    seen_prefix.add(key)
                    entries.append({
                        "term": word,
                        "pinyin": prefix_code,
                        "weight": weight - 500,
                        "source_count": 0,
                        "term_type": "en",
                        "enabled": 1,
                    })

    entries.sort(key=lambda e: e["weight"], reverse=True)
    return entries


CSV_FIELDS = ["term", "pinyin", "weight", "source_count", "term_type", "enabled"]


def write_csv(entries: list[dict[str, str | int]], path: Path) -> None:
    """Write lexicon entries to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(entries)


def read_csv(path: Path) -> list[dict[str, str | int]]:
    """Read lexicon entries from a CSV file."""
    entries: list[dict[str, str | int]] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["weight"] = int(row["weight"])
            row["source_count"] = int(row["source_count"])
            row["enabled"] = int(row["enabled"])
            entries.append(row)
    return entries
