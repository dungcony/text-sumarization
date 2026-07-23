"""ROUGE computation and concise evaluation summaries."""

from __future__ import annotations

from statistics import mean

from rouge_score import rouge_scorer

from .text import normalize_text, word_count


def compute_rouge(predictions: list[str], references: list[str]) -> dict[str, dict[str, float]]:
    """Compute mean ROUGE P/R/F1 on a 0–100 scale for aligned predictions."""
    if len(predictions) != len(references):
        raise ValueError("predictions và references phải có cùng số phần tử.")
    if not predictions:
        raise ValueError("Cần tối thiểu một dự đoán để tính ROUGE.")
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    scores = [scorer.score(normalize_text(reference), normalize_text(prediction)) for prediction, reference in zip(predictions, references)]
    return {
        metric: {
            "precision": round(mean(score[metric].precision for score in scores) * 100, 2),
            "recall": round(mean(score[metric].recall for score in scores) * 100, 2),
            "f1": round(mean(score[metric].fmeasure for score in scores) * 100, 2),
        }
        for metric in ("rouge1", "rouge2", "rougeL")
    }


def compression_statistics(articles: list[str], predictions: list[str]) -> dict[str, float]:
    """Report transparent whitespace-token compression statistics."""
    source_lengths = [word_count(article) for article in articles]
    generated_lengths = [word_count(prediction) for prediction in predictions]
    if not source_lengths:
        return {"source_words_mean": 0.0, "summary_words_mean": 0.0, "compression_percent": 0.0}
    source_mean = mean(source_lengths)
    summary_mean = mean(generated_lengths)
    return {
        "source_words_mean": round(source_mean, 2),
        "summary_words_mean": round(summary_mean, 2),
        "compression_percent": round((1 - summary_mean / source_mean) * 100, 2) if source_mean else 0.0,
    }
