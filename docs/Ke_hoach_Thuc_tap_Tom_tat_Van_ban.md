# KẾ HOẠCH VÀ ĐỀ CƯƠNG CHI TIẾT: BÀI TOÁN TÓM TẮT NỘI DUNG VĂN BẢN TIẾNG VIỆT

## 🎯 Mục Tiêu Tổng Quan

Chuyển đổi yêu cầu thực tập từ dạng khái quát thành một lộ trình kỹ thuật cụ thể. Mục tiêu cốt lõi của kỳ thực tập là **hiểu sâu sắc sự tiến hóa của các mô hình NLP trong bài toán Tóm tắt văn bản (Text Summarization)**, từ đó xây dựng một **ứng dụng thực tế** có khả năng tự động xử lý và tóm tắt văn bản tiếng Việt dựa trên dữ liệu thu thập được.

---

## 📚 MẢNG 1: NGHIÊN CỨU & THỬ NGHIỆM MÔ HÌNH HỌC MÁY

Bài toán tóm tắt văn bản được chia thành hai nhánh tiếp cận chính: **Extractive (Trích xuất)** và **Abstractive (Trừu tượng)**. Bạn cần nghiên cứu và chạy thử nghiệm (Hands-on) qua 5 thế hệ mô hình sau đây để đánh giá sự thay đổi về mặt công nghệ:

### 1. Hệ thống 5 mô hình nghiên cứu theo dòng lịch sử

#### Thế hệ 1: Phương pháp Thống kê & Đồ thị (Dựa trên luật - Rule-based / Không giám sát)

* **Mô hình tiêu biểu:** **TextRank** hoặc **LexRank**.
* **Cơ chế:** Coi văn bản là một đồ thị, trong đó mỗi câu là một nút (node), mối quan hệ giữa các câu dựa trên mức độ trùng lặp từ vựng (Cosine Similarity / TF-IDF). Thuật toán xếp hạng câu quan trọng nhất (tương tự PageRank của Google).
* **Tính chất:** Trích xuất (Extractive).
* **Thư viện chạy thử:** `gensim`, `networkx` hoặc `spacy`.

#### Thế hệ 2: Mạng Nơ-ron Hồi quy (Deep Learning truyền thống)

* **Mô hình tiêu biểu:** **Sequence-to-Sequence (Seq2Seq) kết hợp LSTM/GRU và cơ chế Attention**.
* **Cơ chế:** Mã hóa (Encoder) toàn bộ văn bản đầu vào thành một vector ngữ cảnh cố định, sau đó giải mã (Decoder) để sinh ra từng từ của bản tóm tắt.
* **Tính chất:** Trừu tượng (Abstractive).
* **Hạn chế:** Bị suy giảm hiệu năng nghiêm trọng khi xử lý các văn bản dài (vấn đề Vanishing Gradient).

#### Thế hệ 3: Kỷ nguyên Transformer & Mô hình ngôn ngữ lớn Pre-trained (Encoder-only)

* **Mô hình tiêu biểu:** **BERT / PhoBERT** (Phiên bản BERT tối ưu riêng cho tiếng Việt).
* **Cơ chế:** Sử dụng cơ chế Self-Attention đa đầu để hiểu ngữ cảnh hai chiều của toàn bộ văn bản một cách đồng thời.
* **Ứng dụng trong tóm tắt:** Thường được cấu hình làm **BERT-based Extractor** (Xếp hạng và trích xuất các câu có trọng số ngữ cảnh cao nhất).

#### Thế hệ 4: Mô hình Sequence-to-Sequence chuyên dụng cho sinh văn bản (Encoder-Decoder)

* **Mô hình tiêu biểu:** **BART (mBART-50) hoặc T5 (ViT5 / mT5)**.
* **Cơ chế:** Được tiền huấn luyện (Pre-trained) trên các tác vụ phá hủy văn bản (Text infilling, sentence shuffling) và khôi phục lại văn bản gốc. Đây là các mô hình tối ưu nhất cho bài toán Abstractive Summarization trước kỷ nguyên LLM.
* **Cách tiếp cận:** Tải pre-trained weights từ HuggingFace và thiết lập mã nguồn để thực hiện Inference (Dự đoán).

#### Thế hệ 5: Mô hình ngôn ngữ lớn hiện đại (Generative LLMs)

* **Mô hình tiêu biểu:** **LLaMA 3 (hoặc các phiên bản tinh chỉnh cho tiếng Việt như SeaLLaMA, VinaLlama), GPT-4o-mini**.
* **Cơ chế:** Tận dụng khả năng Zero-shot/Few-shot learning thông qua kỹ thuật Prompt Engineering để yêu cầu mô hình tóm tắt văn bản theo các tiêu chí phức tạp (độ dài mong muốn, văn phong, định dạng).

### 2. Tiêu chí đánh giá hệ thống mô hình

Khi chạy thử nghiệm các mô hình trên, bạn không chỉ nhìn bằng mắt mà phải lượng hóa bằng số liệu cụ thể thông qua **Thang đo ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**:

* **ROUGE-1:** Đo mức độ trùng lặp của các từ đơn (unigram).
* **ROUGE-2:** Đo mức độ trùng lặp của các cặp từ đi liền nhau (bigram).
* **ROUGE-L:** Đo chuỗi con chung dài nhất (Longest Common Subsequence), đánh giá tính mạch lạc và thứ tự của câu.

---

## 🛠️ MẢNG 2: XÂY DỰNG ỨNG DỤNG & THU THẬP DỮ LIỆU

Mục tiêu là hiện thực hóa lý thuyết thành một sản phẩm cụ thể. Bạn sẽ chọn một trong các mô hình mạnh ở Mảng 1 để phát triển một ứng dụng thực tế.

### 1. Quy trình xử lý dữ liệu (Data Pipeline)

Để huấn luyện (Fine-tune) hoặc đánh giá một mô hình tóm tắt, dữ liệu bắt buộc phải tồn tại dưới dạng cặp: `{"document": "Văn bản gốc dài", "summary": "Bản tóm tắt chuẩn"}`.

* **Thu thập dữ liệu (Crawling):** * *Nguồn gợi ý:* Các trang báo điện tử lớn (VnExpress, Tuổi Trẻ, Dân Trí).
  * *Kỹ thuật:* Sử dụng Python với thư viện `BeautifulSoup` hoặc `Selenium`. Cào nội dung chi tiết của bài báo làm `document`, cào phần Sapo (đoạn tóm tắt in đậm đầu bài) hoặc tự tổng hợp tiêu đề làm `summary`.
  * *Giải pháp thay thế:* Sử dụng các bộ dữ liệu có sẵn trên GitHub/HuggingFace như *VietNews* hoặc dữ liệu văn bản hành chính công khai để tiết kiệm thời gian.
* **Tiền xử lý dữ liệu (Preprocessing):**
  * Làm sạch HTML, loại bỏ các ký tự rác, quảng cáo, liên kết ẩn.
  * Tách từ tiếng Việt (Word Segmentation) bằng các công cụ như `PyVi` hoặc `Underthesea`.
  * *Kỹ thuật nâng cao:* Đối với văn bản quá dài vượt ngưỡng giới hạn token của mô hình (ví dụ 1024 tokens của mBART), cần áp dụng kỹ thuật **Text Chunking** (chia nhỏ văn bản thành các đoạn hợp lý, tóm tắt từng đoạn rồi tổng hợp lại).
* **Phân chia dữ liệu:** Chia tập dữ liệu thu thập được thành 2 phần độc lập theo tỷ lệ chuẩn:
  * **Tập Train (80%):** Dùng để huấn luyện/tinh chỉnh mô hình.
  * **Tập Test (20%):** Giữ nguyên không cho mô hình biết trước, dùng để chạy kiểm thử và tính điểm ROUGE.

### 2. Phát triển ứng dụng hoàn chỉnh

* **Lõi xử lý (Backend):** Viết bằng Python (sử dụng Framework như FastAPI hoặc Flask) để tải mô hình đã huấn luyện lên, tiếp nhận văn bản dài từ người dùng và trả về kết quả tóm tắt.
* **Giao diện người dùng (Frontend/Demo):** Sử dụng **Streamlit** hoặc **Gradio** (hai công cụ tạo giao diện nhanh bằng Python cực kỳ phổ biến trong ngành AI/Data) để tạo một trang web đơn giản:
  * Một ô lớn để người dùng dán (paste) văn bản dài vào.
  * Một nút bấm "Tóm tắt ngay".
  * Một ô hiển thị kết quả văn bản rút gọn kèm theo thời gian xử lý và các chỉ số thống kê (độ dài giảm bao nhiêu %, số lượng từ,...).

---

## 📅 LỘ TRÌNH TRIỂN KHAI CHI TIẾT 07 TUẦN

Dưới đây là bảng phân rã công việc theo từng tuần giúp bạn quản lý tiến độ và báo cáo với mentor:

| Tuần | Mục tiêu chính | Công việc cụ thể | Sản phẩm đầu ra (Deliverables) |
| :--- | :--- | :--- | :--- |
| **Tuần 1** | **Tổng quan & Đồ thị** | - Đọc hiểu bài toán Summarization (Extractive vs Abstractive).<br>- Cài đặt môi trường Python, HuggingFace.<br>- Chạy thử nghiệm thuật toán **TextRank** với thư viện `gensim`. | - Báo cáo lý thuyết tổng quan.<br>- Script Python chạy thử TextRank trên 10 văn bản mẫu. |
| **Tuần 2** | **Deep Learning & BERT** | - Nghiên cứu mô hình Seq2Seq (Lý thuyết).<br>- Tìm hiểu cơ chế Attention và kiến trúc Transformer.<br>- Chạy thử nghiệm trích xuất câu bằng **PhoBERT**. | - Script Python thực hiện inference với PhoBERT làm nhiệm vụ Extractive. |
| **Tuần 3** | **Generative Models** | - Nghiên cứu các mô hình sinh chuyên dụng: **mBART, ViT5**.<br>- Tìm hiểu thang đo **ROUGE score** và cách cài đặt bằng code. | - Mã nguồn gọi các mô hình mBART/ViT5 sinh văn bản tóm tắt.<br>- Kết quả chấm điểm ROUGE thử nghiệm. |
| **Tuần 4** | **Thu thập dữ liệu** | - Xác định chủ đề ứng dụng (Ví dụ: Tóm tắt tin tức thời sự).<br>- Viết script cào dữ liệu tự động hoặc tải và làm sạch các bộ dữ liệu tiếng Việt có sẵn. | - Dataset thô gồm ít nhất 1,000 - 2,000 cặp `[Văn bản - Tóm tắt]`. |
| **Tuần 5** | **Tiền xử lý & Chunking** | - Thực hiện làm sạch dữ liệu (loại bỏ nhiễu, chuẩn hóa font chữ).<br>- Viết module tách từ và thuật toán **Text Chunking** cho văn bản dài. | - Dataset sạch đã được phân tách thành 2 file: `train.json` và `test.json`. |
| **Tuần 6** | **Huấn luyện & Tối ưu** | - Tiến hành **Fine-tune** mô hình (khuyến khích chọn mBART hoặc ViT5) trên tập dữ liệu Train đã chuẩn bị ở tuần trước. | - File lưu trữ trọng số mô hình (Model Checkpoint) sau khi huấn luyện xong. |
| **Tuần 7** | **Đóng gói & Báo cáo** | - Đánh giá mô hình trên tập Test bằng ROUGE score.<br>- Xây dựng giao diện Web Demo bằng **Streamlit**.<br>- Viết báo cáo thực tập tổng kết. | - Ứng dụng Web chạy nội bộ (Localhost).<br>- File báo cáo thực tập hoàn chỉnh (Word/PDF). |

---

## 💡 Gợi ý tư duy làm sản phẩm (Để đạt điểm cao)

Thay vì làm một ứng dụng tóm tắt tin tức chung chung giống mọi người, bạn có thể hướng sản phẩm của mình vào một ngách cụ thể để tạo điểm nhấn lớn trong báo cáo:

1. **Ứng dụng tóm tắt văn bản học thuật/Đề án tuyển sinh:** Giúp học sinh nhanh chóng nắm bắt các thông tin cốt lõi (chỉ tiêu, khối thi, quy chế) từ các tài liệu tuyển sinh dài hàng chục trang.
2. **Ứng dụng tóm tắt biên bản cuộc họp/Văn bản pháp luật:** Tập trung lọc ra các điều khoản quan trọng, các mốc thời gian và hành động cần thực hiện (Action items).
