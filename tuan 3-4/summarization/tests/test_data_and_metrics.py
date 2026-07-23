from __future__ import annotations

import unittest

from week34_summarization.data import records_from_rows
from week34_summarization.metrics import compute_rouge
from week34_summarization.text import normalize_text


class DataAndMetricsTests(unittest.TestCase):
    def test_normalize_preserves_vietnamese_numbers(self) -> None:
        self.assertEqual(normalize_text("  Liều\u200b 500mg &amp; ngày 2. "), "Liều 500mg & ngày 2.")

    def test_records_resolve_document_summary_and_filter_duplicate(self) -> None:
        rows = [
            {"Document": "Một văn bản tiếng Việt có đủ số lượng từ để được chấp nhận.", "Summary": "Tóm tắt đủ ba từ."},
            {"Document": "Một văn bản tiếng Việt có đủ số lượng từ để được chấp nhận.", "Summary": "Tóm tắt đủ ba từ."},
        ]
        records, audit = records_from_rows(rows, min_article_words=5, min_summary_words=3)
        self.assertEqual(len(records), 1)
        self.assertEqual(audit["rejected_by_reason"]["exact_duplicate_pair"], 1)

    def test_rouge_identical_text_is_100(self) -> None:
        scores = compute_rouge(["Việt Nam phát triển công nghệ"], ["Việt Nam phát triển công nghệ"])
        self.assertEqual(scores["rouge1"]["f1"], 100.0)
        self.assertEqual(scores["rouge2"]["f1"], 100.0)
        self.assertEqual(scores["rougeL"]["f1"], 100.0)


if __name__ == "__main__":
    unittest.main()
