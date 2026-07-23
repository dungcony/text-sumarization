"""Small, explicit Hugging Face inference wrapper for Week 3."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .text import normalize_text


def choose_device(requested: str) -> str:
    """Resolve auto/cpu/cuda while failing clearly when CUDA is unavailable."""
    import torch

    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA không khả dụng. Dùng --device cpu hoặc --device auto.")
    return requested


def _batched(values: list[str], batch_size: int) -> Iterator[list[str]]:
    for index in range(0, len(values), batch_size):
        yield values[index : index + batch_size]


def generate_summaries(
    texts: list[str],
    *,
    model_name: str,
    device: str = "auto",
    prefix: str = "summarize: ",
    batch_size: int = 4,
    max_source_length: int = 768,
    max_new_tokens: int = 128,
    min_new_tokens: int = 20,
    num_beams: int = 4,
    no_repeat_ngram_size: int = 3,
) -> tuple[list[str], str]:
    """Load one pretrained seq2seq checkpoint and generate summaries in batches."""
    if not texts:
        return [], choose_device(device)
    if batch_size < 1:
        raise ValueError("batch_size phải lớn hơn 0.")

    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    resolved_device = choose_device(device)
    use_fast = not any(name in model_name.casefold() for name in ("vit5", "mt5", "t5"))
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=use_fast)
    model: Any = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(resolved_device)
    model.eval()

    summaries: list[str] = []
    prepared = [prefix + normalize_text(text) for text in texts]
    for batch in _batched(prepared, batch_size):
        encoded = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_source_length,
        ).to(resolved_device)
        with torch.inference_mode():
            generated = model.generate(
                **encoded,
                max_new_tokens=max_new_tokens,
                min_new_tokens=min_new_tokens,
                num_beams=num_beams,
                no_repeat_ngram_size=no_repeat_ngram_size,
                early_stopping=True,
            )
        summaries.extend(text.strip() for text in tokenizer.batch_decode(generated, skip_special_tokens=True))
    return summaries, resolved_device
