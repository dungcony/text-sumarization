# Các Thuật Ngữ Bài Toán Tóm Tắt Văn Bản (Text Summarization)

Dưới đây là bảng tổng hợp các thuật ngữ thường gặp khi làm việc với bài toán tóm tắt văn bản và huấn luyện mô hình. Bảng được chia thành các nhóm để bạn dễ dàng ôn tập và trả lời câu hỏi của thầy cô.

## 1. Phân loại bài toán (Task Types)

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Extractive Summarization** | Tóm tắt trích xuất | Phương pháp trích xuất trực tiếp các câu/cụm từ quan trọng nhất từ văn bản gốc để ghép thành bản tóm tắt. (Giống như dùng bút highlight các câu quan trọng). |
| **Abstractive Summarization** | Tóm tắt trừu tượng | Phương pháp tạo ra văn bản tóm tắt mới hoàn toàn, có thể chứa các từ ngữ không xuất hiện trong văn bản gốc. Yêu cầu mô hình phải "hiểu" ngôn ngữ giống con người. |
| **Single-document / Multi-document** | Tóm tắt đơn / đa văn bản | Tóm tắt từ 1 văn bản duy nhất hay tổng hợp thông tin từ nhiều nguồn văn bản khác nhau. |

## 2. Dữ liệu (Data & Inputs)

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Source Text / Article** | Văn bản gốc / Bài viết | Đầu vào của bài toán, văn bản cần được tóm tắt. |
| **Reference Summary / Target** | Tóm tắt tham chiếu / Mục tiêu | Bản tóm tắt chuẩn (thường do con người viết) dùng để làm nhãn (label) huấn luyện hoặc đánh giá mô hình. (Còn gọi là Ground-truth). |
| **Generated / Hypothesis Summary** | Tóm tắt do mô hình sinh ra | Kết quả đầu ra của mô hình sau khi dự đoán. |
| **Corpus / Dataset** | Tập dữ liệu | Tập hợp rất nhiều cặp (Văn bản gốc, Tóm tắt tham chiếu) dùng để train mô hình. (Ví dụ: CNN/DailyMail, XSum, VietNews). |

## 3. Kiến trúc mô hình (Model Architecture)

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Seq2Seq (Sequence-to-Sequence)** | Chuỗi sang chuỗi | Dạng bài toán nhận đầu vào là một chuỗi (văn bản) và trả ra một chuỗi khác (tóm tắt). |
| **Encoder - Decoder** | Mã hóa - Giải mã | Cấu trúc mô hình phổ biến nhất. **Encoder** đọc và nén văn bản gốc thành một vector ngữ cảnh. **Decoder** dùng vector đó để sinh ra văn bản tóm tắt từng từ một. |
| **Transformer** | - | Kiến trúc mạng nơ-ron hiện đại thay thế RNN/LSTM, xử lý toàn bộ câu cùng lúc và giải quyết tốt bài toán dài nhờ cơ chế Attention (Ví dụ: BART, T5, mBART). |
| **Attention Mechanism** | Cơ chế chú ý | Giúp mô hình tập trung vào các từ quan trọng trong văn bản gốc khi sinh ra từng từ của bản tóm tắt. |
| **Self-Attention** | Tự chú ý | Giúp các từ trong cùng một câu tìm ra mối liên hệ với nhau (đại từ này thay cho danh từ nào, ngữ cảnh xung quanh là gì). |
| **Cross-Attention** | Chú ý chéo | Xảy ra ở phần Decoder: giúp Decoder "nhìn" lại các phần quan trọng của văn bản gốc (từ Encoder) để sinh từ tiếp theo. |

## 4. Quá trình sinh văn bản (Decoding / Generation)

Khi mô hình dự đoán (inference), nó cần thuật toán để chọn ra từ tiếp theo.

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Greedy Search** | Tìm kiếm tham lam | Chọn từ có xác suất cao nhất ở mỗi bước. Nhanh nhưng có thể dẫn đến câu không tối ưu về ngữ pháp tổng thể. |
| **Beam Search** | - | Thuật toán giữ lại $K$ (Beam size) chuỗi ứng viên tốt nhất ở mỗi bước, giúp sinh ra câu văn tự nhiên và chất lượng hơn Greedy Search. (Thường hay bị thầy cô hỏi). |
| **Length Penalty** | Phạt độ dài | Thông số trong Beam Search để tránh mô hình sinh ra câu quá ngắn. Nếu penalty càng cao, mô hình có xu hướng sinh câu dài hơn. |
| **Teacher Forcing** | Ép buộc từ giáo viên | Kỹ thuật dùng trong lúc **Training**. Thay vì dùng từ do mô hình vừa dự đoán để sinh từ tiếp theo (dễ sai dây chuyền), ta đưa trực tiếp từ đúng (của Reference Summary) vào. |

## 5. Quá trình huấn luyện (Training & Optimization)

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Pre-training** | Tiền huấn luyện | Huấn luyện mô hình trên kho dữ liệu khổng lồ (vô giám sát) để nó có khả năng hiểu ngôn ngữ chung (Ví dụ BERT, GPT, T5). |
| **Fine-tuning** | Tinh chỉnh | Quá trình train lại mô hình đã pre-train bằng tập dữ liệu cụ thể của bạn (ví dụ dữ liệu tóm tắt tiếng Việt) để nó làm tốt nhiệm vụ chuyên biệt này. |
| **Epoch** | Vòng lặp / Kỷ nguyên | 1 Epoch là khi mô hình đã học qua TOÀN BỘ dữ liệu huấn luyện (Training set) đúng 1 lần. |
| **Batch Size** | Kích thước lô | Số lượng mẫu dữ liệu (cặp văn bản - tóm tắt) đưa vào mô hình trong mỗi lần cập nhật trọng số. (Ví dụ: Batch size = 16). |
| **Learning Rate** | Tốc độ học | Tham số quyết định mức độ điều chỉnh trọng số của mô hình sau mỗi lần đoán sai. Quá to thì mô hình không hội tụ, quá nhỏ thì train rất lâu. |
| **Cross-Entropy Loss** | Hàm mất mát Cross-Entropy | Hàm tính toán độ sai lệch giữa từ mô hình sinh ra và từ đúng trong Reference. Mục tiêu của Training là làm giảm Loss này. |
| **Overfitting / Underfitting** | Quá khớp / Chưa khớp | **Overfitting**: Học vẹt, train loss thấp nhưng đánh giá trên tập test thì tệ. **Underfitting**: Mô hình học quá kém, chưa tìm ra được quy luật. |
| **Optimizer** | Thuật toán tối ưu | Thuật toán dùng để cập nhật trọng số mô hình nhằm giảm Loss (Phổ biến nhất: Adam, AdamW). |

## 6. Đánh giá mô hình (Evaluation Metrics)

Thầy cô sẽ luôn hỏi: "Làm sao em biết mô hình của em tóm tắt tốt hay không?".

| Thuật ngữ tiếng Anh | Thuật ngữ tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) | - | Thước đo chuẩn nhất cho tóm tắt. Dựa trên việc đếm số từ/cụm từ trùng lặp giữa bản tóm tắt của mô hình và bản tóm tắt tham chiếu (Reference). |
| **ROUGE-N (ROUGE-1, ROUGE-2)** | - | Tính trùng lặp dựa trên N-gram (ROUGE-1 đếm từng từ đơn lẻ, ROUGE-2 đếm cụm 2 từ liền kề). |
| **ROUGE-L (LCS)** | - | Tính dựa trên chuỗi con chung dài nhất (Longest Common Subsequence). Đánh giá xem trật tự từ trong câu có tự nhiên không. |
| **BLEU** | - | Thường dùng cho Dịch máy (Machine Translation), nhưng thi thoảng vẫn dùng cho tóm tắt. Dựa trên độ chính xác (Precision) của n-gram. |
| **BERTScore** | - | Thước đo hiện đại, thay vì đếm từ trùng khớp 100%, nó dùng mô hình ngôn ngữ để so sánh độ tương đồng về mặt **ngữ nghĩa** (semantic similarity) giữa câu sinh ra và câu chuẩn. |

---

> [!TIP]
> **Một số câu hỏi thầy cô thường hay hỏi (bạn nên chuẩn bị trước):**
> 1. *Tại sao em dùng mô hình Abstractive thay vì Extractive?* (Gợi ý: Abstractive tự nhiên hơn, giống người hơn dù khó train hơn).
> 2. *ROUGE score có nhược điểm gì không?* (Gợi ý: Có, ROUGE chỉ đếm từ trùng khớp cơ học, nếu mô hình dùng từ đồng nghĩa thì ROUGE đánh giá thấp. Đó là lý do đôi khi cần thêm BERTScore hoặc đánh giá của con người).
> 3. *Em xử lý thế nào nếu văn bản đầu vào quá dài?* (Gợi ý: Các mô hình Transformer thường bị giới hạn độ dài ví dụ 512 hoặc 1024 token. Cần cắt bớt câu đầu/câu cuối, hoặc dùng các mô hình cho văn bản dài như Longformer/LED).
> 4. *Teacher Forcing là gì và tại sao lại dùng trong quá trình sinh từ?* (Gợi ý: Xem mục số 4 trong bảng).
