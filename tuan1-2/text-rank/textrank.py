"""
các bước thực hiện:
1. chia văn bản thành các câu 
2. phân tách câu bằng phuơng pháp phân đoạn từ tiếng việt (underthesea)
3. vector hóa câu sử dụng TF-IDF
4. xây dựng ma trận tương đồng cosine giữa các câu
5. xây dựng đồ thị và áp dụng pageRank để xếp hạng các câu
6. chọn các câu có điểm số cao nhất để tạo tóm tắt
"""

import re
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_tokenize


# ============================================================
# Vietnamese Stopwords
# ============================================================
VIETNAMESE_STOPWORDS = {
    "và", "của", "là", "có", "trong", "cho", "các", "được", "này",
    "với", "không", "một", "những", "đã", "để", "từ", "theo", "trên",
    "về", "khi", "đến", "tại", "cũng", "như", "hay", "nhưng", "hoặc",
    "nếu", "thì", "do", "vì", "bởi", "mà", "rằng", "sẽ", "đang",
    "còn", "nên", "vẫn", "ra", "lại", "đó", "đây", "bị", "phải",
    "rất", "hơn", "nhiều", "ít", "thì", "qua", "sau", "trước",
}


# ============================================================
# Tiền xử lý 
# ============================================================
def split_into_sentences(text: str) -> list[str]:
    # chuẩn hóa khoảng trắng và loại bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text.strip())
    
    # tách văn bản thành các câu dựa trên dấu chấm, chấm than, chấm hỏi
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # loại bỏ các câu trống và loại bỏ dấu chấm cuối cùng
    sentences = [s.strip().rstrip('.').strip() for s in sentences if s.strip()]
    
    # loại bỏ các câu ngắn (có ít hơn 5 ký tự) để tránh các câu không có ý nghĩa
    sentences = [s for s in sentences if len(s) >= 5]
    return sentences


def tokenize_vietnamese(text: str) -> str:
    tokens = word_tokenize(text, format="text").lower().split()
    tokens = [t for t in tokens if t not in VIETNAMESE_STOPWORDS and len(t) > 1]
    return " ".join(tokens)


# ============================================================
# TextRank Summarizer
# ============================================================
class TextRankSummarizer:
    # ratio : float : số lượng phần trăm câu được chọn để tạo tóm tắt (mặc định là 0.3, tức là 30% số câu)
    
    def __init__(self, ratio: float = 0.3):
        self.ratio = ratio

    def _build_similarity_matrix(self, tfidf_vectors) -> np.ndarray:
        return cosine_similarity(tfidf_vectors)

    def _rank_sentences(self, similarity_matrix: np.ndarray) -> dict:
        """s
        xây dựng đồ thị từ ma trận tương đông và áp dụng PageRank.
        trả về 1 dict ánh xạ chỉ số câu -> điểm số
        """
        graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(graph, max_iter=200)
        return scores

    def summarize(self, text: str, ratio: float | None = None) -> str:

        #Tóm tắt văn bản tiếng Việt bằng phương pháp TextRank.

        ratio = ratio if ratio is not None else self.ratio

        # buwoisc 1: chia văn bản thành các câu
        sentences = split_into_sentences(text)
        if len(sentences) <= 1:
            return text.strip()

        # bước 2: phân tách câu bằng phương pháp phân đoạn từ tiếng việt (underthesea)
        tokenized = [tokenize_vietnamese(s) for s in sentences]

        # bước 3: vector hóa câu sử dụng TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(tokenized)

        # bước 4: xây dựng ma trận tương đồng
        sim_matrix = self._build_similarity_matrix(tfidf_matrix)

        # bước 5: xếp hạng câu sử dụng PageRank
        scores = self._rank_sentences(sim_matrix)

        # bước 6: chọn các câu hàng đầu (giữ nguyên thứ tự gốc)
        n_select = max(1, round(len(sentences) * ratio))
        ranked_indices = sorted(scores, key=scores.get, reverse=True)[:n_select]
        # Sắp xếp theo vị trí gốc để duy trì thứ tự đọc
        ranked_indices.sort()

        summary = ". ".join(sentences[i] for i in ranked_indices) + "."
        return summary
