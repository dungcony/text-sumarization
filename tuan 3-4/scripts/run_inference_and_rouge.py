#!/usr/bin/env python3
"""Week 3: run pretrained Vietnamese summarization and calculate ROUGE."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from data import records_from_rows, read_rows
from metrics import compression_statistics, compute_rouge
from model import generate_summaries


DEFAULT_MODEL = "VietAI/vit5-base-vietnews-summarization"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Suy luận bằng checkpoint seq2seq có sẵn và tính ROUGE.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT.parent.parent / "data/summarization_samples.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "results/vit5_evaluation.json")
    parser.add_argument("--source-column")
    parser.add_argument("--summary-column")
    parser.add_argument("--id-column")
    parser.add_argument("--max-samples", type=int, default=10)
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto")
    parser.add_argument("--prefix", default="summarize: ")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-source-length", type=int, default=768)
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--min-new-tokens", type=int, default=20)
    parser.add_argument("--num-beams", type=int, default=4)
    parser.add_argument("--no-repeat-ngram-size", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_samples < 1:
        raise ValueError("--max-samples phải lớn hơn 0.")
    records, input_audit = records_from_rows(
        read_rows(args.input),
        source_column=args.source_column,
        summary_column=args.summary_column,
        id_column=args.id_column,
        keep_at_most=args.max_samples,
    )
    articles = [record.article for record in records]
    references = [record.summary for record in records]
    started = perf_counter()
    predictions, device = generate_summaries(
        articles,
        model_name=args.model,
        device=args.device,
        prefix=args.prefix,
        batch_size=args.batch_size,
        max_source_length=args.max_source_length,
        max_new_tokens=args.max_new_tokens,
        min_new_tokens=args.min_new_tokens,
        num_beams=args.num_beams,
        no_repeat_ngram_size=args.no_repeat_ngram_size,
    )
    elapsed_seconds = round(perf_counter() - started, 2)
    payload = {
        "run": {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "model": args.model,
            "device": device,
            "input_path": str(args.input),
            "number_of_examples": len(records),
            "elapsed_seconds": elapsed_seconds,
            "seconds_per_example": round(elapsed_seconds / len(records), 2),
        },
        "generation": {
            "prefix": args.prefix,
            "batch_size": args.batch_size,
            "max_source_length": args.max_source_length,
            "max_new_tokens": args.max_new_tokens,
            "min_new_tokens": args.min_new_tokens,
            "num_beams": args.num_beams,
            "no_repeat_ngram_size": args.no_repeat_ngram_size,
        },
        "input_audit": input_audit,
        "metrics": {
            "rouge": compute_rouge(predictions, references),
            "compression": compression_statistics(articles, predictions),
        },
        "predictions": [
            {"id": record.id, "article": record.article, "reference": record.summary, "prediction": prediction}
            for record, prediction in zip(records, predictions)
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rouge = payload["metrics"]["rouge"]
    print(f"Đã đánh giá {len(records)} mẫu bằng {args.model} trên {device}.")
    print(f"ROUGE-1 F1: {rouge['rouge1']['f1']:.2f}")
    print(f"ROUGE-2 F1: {rouge['rouge2']['f1']:.2f}")
    print(f"ROUGE-L F1: {rouge['rougeL']['f1']:.2f}")
    print(f"Kết quả chi tiết: {args.output}")


if __name__ == "__main__":
    main()
