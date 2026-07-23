"""Input/output and audit helpers for the Week 4 raw dataset."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

from .text import canonical_pair_key, normalize_text, word_count


SOURCE_ALIASES = ("article", "document", "text", "source")
SUMMARY_ALIASES = ("summary", "abstract", "target")
ID_ALIASES = ("id", "_id", "index")


@dataclass(frozen=True)
class Record:
    """A normalized document/reference pair used in inference and raw storage."""

    id: str
    article: str
    summary: str
    source_dataset: str = ""
    source_row: int = 0


def _find_column(fieldnames: Iterable[str], aliases: tuple[str, ...], explicit: str | None) -> str:
    columns = list(fieldnames)
    if explicit:
        if explicit not in columns:
            raise ValueError(f"Không tìm thấy cột '{explicit}'. Cột có sẵn: {columns}")
        return explicit
    mapping = {column.casefold(): column for column in columns}
    for alias in aliases:
        if alias in mapping:
            return mapping[alias]
    raise ValueError(f"Không nhận diện được cột trong {aliases}. Cột có sẵn: {columns}")


def _read_json(path: Path) -> list[dict[str, Any]]:
    if path.suffix.casefold() == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("data", payload.get("records", []))
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise ValueError("JSON phải là một mảng bản ghi hoặc object có khóa data/records.")
    return payload


def read_rows(path: str | Path) -> list[dict[str, Any]]:
    """Read CSV, JSON, or JSONL into row dictionaries with UTF-8 handling."""
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy input: {input_path}")
    suffix = input_path.suffix.casefold()
    if suffix in {".json", ".jsonl"}:
        return _read_json(input_path)
    if suffix == ".csv":
        with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise ValueError("Chỉ hỗ trợ .csv, .json và .jsonl")


def records_from_rows(
    rows: list[dict[str, Any]],
    *,
    source_column: str | None = None,
    summary_column: str | None = None,
    id_column: str | None = None,
    dataset_name: str = "",
    min_article_words: int = 10,
    min_summary_words: int = 3,
    keep_at_most: int | None = None,
) -> tuple[list[Record], dict[str, Any]]:
    """Normalize/filter rows and return a transparent audit dictionary."""
    if not rows:
        raise ValueError("Input không có bản ghi.")
    fieldnames = list(rows[0])
    source_name = _find_column(fieldnames, SOURCE_ALIASES, source_column)
    summary_name = _find_column(fieldnames, SUMMARY_ALIASES, summary_column)
    id_name = _find_column(fieldnames, ID_ALIASES, id_column) if id_column else None
    rejected: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()
    output: list[Record] = []

    for row_number, row in enumerate(rows, start=1):
        article = normalize_text(row.get(source_name, ""))
        summary = normalize_text(row.get(summary_name, ""))
        if not article or not summary:
            rejected["empty"] += 1
            continue
        article_words = word_count(article)
        summary_words = word_count(summary)
        if article_words < min_article_words:
            rejected["article_too_short"] += 1
            continue
        if summary_words < min_summary_words:
            rejected["summary_too_short"] += 1
            continue
        if summary_words >= article_words:
            rejected["summary_not_shorter_than_article"] += 1
            continue
        pair_key = canonical_pair_key(article, summary)
        if pair_key in seen:
            rejected["exact_duplicate_pair"] += 1
            continue
        seen.add(pair_key)
        record_id = normalize_text(row.get(id_name, "")) if id_name else ""
        output.append(
            Record(
                id=record_id or str(row_number),
                article=article,
                summary=summary,
                source_dataset=dataset_name or normalize_text(row.get("Dataset", "")),
                source_row=row_number,
            )
        )
        if keep_at_most and len(output) >= keep_at_most:
            break

    article_lengths = [word_count(record.article) for record in output]
    summary_lengths = [word_count(record.summary) for record in output]
    audit = {
        "input_rows": len(rows),
        "accepted_rows": len(output),
        "rejected_rows": sum(rejected.values()),
        "rejected_by_reason": dict(sorted(rejected.items())),
        "columns": {"article": source_name, "summary": summary_name, "id": id_name},
        "filters": {
            "min_article_words": min_article_words,
            "min_summary_words": min_summary_words,
            "requires_summary_shorter_than_article": True,
            "deduplicate": "exact article-summary pair",
        },
        "length_statistics_words": {
            "article_mean": round(mean(article_lengths), 2) if article_lengths else 0,
            "article_min": min(article_lengths, default=0),
            "article_max": max(article_lengths, default=0),
            "summary_mean": round(mean(summary_lengths), 2) if summary_lengths else 0,
            "summary_min": min(summary_lengths, default=0),
            "summary_max": max(summary_lengths, default=0),
        },
    }
    return output, audit


def write_records_csv(records: list[Record], path: str | Path) -> None:
    """Save standard raw-data CSV without mutating its source file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "article", "summary", "source_dataset", "source_row"])
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
