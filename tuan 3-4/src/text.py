"""Conservative Vietnamese-text normalization used before inference/audit."""

from __future__ import annotations

import html
import re
import unicodedata
from typing import Any


HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
WHITESPACE_RE = re.compile(r"\s+")
ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")


def normalize_text(value: Any) -> str:
    """Normalize harmless noise while preserving Vietnamese accents, numbers and punctuation."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFC", html.unescape(str(value)))
    text = ZERO_WIDTH_RE.sub("", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = "".join(" " if unicodedata.category(char) == "Cc" else char for char in text)
    return WHITESPACE_RE.sub(" ", text).strip()


def word_count(text: str) -> int:
    """Return a transparent whitespace-token count for reports and quality gates."""
    return len(normalize_text(text).split())


def canonical_pair_key(article: str, summary: str) -> tuple[str, str]:
    """Stable key for exact duplicate reporting without changing saved text."""
    return normalize_text(article).casefold(), normalize_text(summary).casefold()
