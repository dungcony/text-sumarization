"""Utilities for the Week 3–4 Vietnamese summarization deliverables."""

from .metrics import compute_rouge
from .text import normalize_text

__all__ = ["compute_rouge", "normalize_text"]
