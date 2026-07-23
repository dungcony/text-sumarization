#!/usr/bin/env python3
"""Week 4: create one auditable raw Vietnamese document-summary dataset."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from week34_summarization.data import records_from_rows, read_rows, write_json, write_records_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chuẩn hóa tối thiểu và audit một bộ dữ liệu tóm tắt thô.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input", type=Path, required=True, help="Nguồn CSV, JSON hoặc JSONL.")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "data/raw/vietnews_medical_raw_1000.csv")
    parser.add_argument("--dataset-name", default="", help="Nhãn nguồn được lưu cùng từng bản ghi.")
    parser.add_argument("--source-column", help="Tên cột văn bản nguồn nếu không tự nhận diện được.")
    parser.add_argument("--summary-column", help="Tên cột tóm tắt chuẩn nếu không tự nhận diện được.")
    parser.add_argument("--id-column", help="Tên cột mã bản ghi nếu có.")
    parser.add_argument("--min-article-words", type=int, default=10)
    parser.add_argument("--min-summary-words", type=int, default=3)
    parser.add_argument("--max-records", type=int, default=1000, help="0 để giữ toàn bộ bản ghi đạt điều kiện.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_records < 0:
        raise ValueError("--max-records phải là 0 hoặc số nguyên dương.")
    records, audit = records_from_rows(
        read_rows(args.input),
        source_column=args.source_column,
        summary_column=args.summary_column,
        id_column=args.id_column,
        dataset_name=args.dataset_name,
        min_article_words=args.min_article_words,
        min_summary_words=args.min_summary_words,
        keep_at_most=args.max_records or None,
    )
    write_records_csv(records, args.output)
    audit.update(
        {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "input_path": str(args.input),
            "output_path": str(args.output),
            "scope": "Week 4 raw-data acquisition; no train/validation/test split or chunking applied.",
        }
    )
    audit_path = args.output.with_name(f"{args.output.stem}_audit.json")
    write_json(audit_path, audit)
    print(f"Đã lưu {len(records)} cặp dữ liệu thô: {args.output}")
    print(f"Báo cáo audit: {audit_path}")
    print(f"Bản ghi bị loại: {audit['rejected_rows']}")


if __name__ == "__main__":
    main()
