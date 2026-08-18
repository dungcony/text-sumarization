# BỘ CÂU HỎI ÔN BẢO VỆ BÁO CÁO THỰC TẬP

**Đề tài:** Bài toán tóm tắt văn bản y khoa tiếng Việt  
**Sinh viên:** Lường Tiến Dũng - B22DCCN128

Tài liệu này tổng hợp các câu hỏi giảng viên có thể đặt ra dựa trên báo cáo tổng hợp. Mỗi câu có một gợi ý ngắn để ôn tập. Khi trả lời, nên theo cấu trúc: **khẳng định chính → giải thích kỹ thuật → liên hệ thí nghiệm của đề tài → nêu hạn chế**.

---

## I. Câu hỏi mở đầu và tổng quan đề tài

### 1. Em hãy trình bày đề tài của mình trong khoảng hai phút.

**Gợi ý:** Bài toán, lý do chọn miền y khoa, ba hướng đã thử nghiệm, dữ liệu, kết quả ViT5 cuối cùng và sản phẩm Streamlit.

### 2. Mục tiêu chính của đề tài là gì?

**Gợi ý:** Nghiên cứu và thực nghiệm tóm tắt văn bản tiếng Việt; xây dựng pipeline từ dữ liệu, huấn luyện, đánh giá đến triển khai; tập trung vào dữ liệu y khoa.

### 3. Bài toán đầu vào và đầu ra của hệ thống là gì?

**Gợi ý:** Đầu vào là một văn bản tiếng Việt; đầu ra là bản tóm tắt ngắn hơn nhưng phải giữ thông tin cốt lõi và hạn chế sai lệch.

### 4. Vì sao em chọn miền dữ liệu y khoa?

**Gợi ý:** Văn bản dài, nhiều thuật ngữ, nhu cầu rút gọn cao; đồng thời đây là miền yêu cầu độ chính xác đặc biệt đối với tên bệnh, thuốc, liều lượng và thời gian.

### 5. Khó khăn lớn nhất của đề tài là gì?

**Gợi ý:** Văn bản dài hơn giới hạn đầu vào, dữ liệu chuyên ngành hạn chế, GPU 16 GB, đánh giá tính đúng sự thật và nguy cơ hallucination.

### 6. Đóng góp thực tế của em trong đề tài là gì?

**Gợi ý:** Cài đặt và so sánh nhiều thế hệ phương pháp; chuẩn hóa dữ liệu; xây dựng pipeline fine-tuning ViT5 hai giai đoạn; đánh giá trên tập độc lập; triển khai Web Demo.

### 7. Điểm mới hoặc điểm khác biệt của đề tài so với việc chỉ gọi một mô hình có sẵn là gì?

**Gợi ý:** Không chỉ inference; có xử lý dữ liệu, chia tập, fine-tuning theo miền, tối ưu GPU, quản lý cấu hình/checkpoint, đánh giá trước và sau thích nghi miền, rồi tích hợp ứng dụng.

### 8. Quy trình thực hiện đề tài gồm những giai đoạn nào?

**Gợi ý:** TextRank → Seq2Seq LSTM + Attention → thử ViT5 gốc → chuẩn bị dữ liệu → Phase 1 dữ liệu tổng quát → Phase 2 dữ liệu y khoa → đánh giá → Streamlit.

### 9. Vì sao em không dừng lại ở TextRank hoặc LSTM mà chuyển sang ViT5?

**Gợi ý:** TextRank giữ nguyên câu nên thiếu mạch lạc; LSTM huấn luyện từ đầu khó xử lý văn bản dài và thiếu tri thức tiếng Việt; ViT5 là Transformer encoder-decoder đã được pre-train cho tiếng Việt.

### 10. Nếu chỉ được giữ lại một kết quả quan trọng nhất của đề tài, em sẽ chọn kết quả nào?

**Gợi ý:** Trên cùng tập test y khoa 871 mẫu, Phase 2 đạt ROUGE-1/2/L = 54,75/26,13/36,55, tăng lần lượt 8,45/3,88/7,61 điểm so với checkpoint Phase 1.

---

## II. Cơ sở về tóm tắt văn bản và NLP

### 11. Tóm tắt trích xuất và tóm tắt trừu tượng khác nhau như thế nào?

**Gợi ý:** Trích xuất chọn câu/cụm có sẵn; trừu tượng sinh cách diễn đạt mới. Trích xuất thường trung thực hơn nhưng kém mạch lạc; trừu tượng tự nhiên hơn nhưng có nguy cơ hallucination.

### 12. Đề tài của em thuộc single-document hay multi-document summarization?

**Gợi ý:** Chủ yếu là single-document summarization vì mỗi lần hệ thống nhận một bài viết nguồn.

### 13. Generic summarization và query-focused summarization khác nhau thế nào?

**Gợi ý:** Generic giữ nội dung chính toàn bài; query-focused chỉ tóm tắt phần liên quan đến truy vấn/chủ đề của người dùng.

### 14. Tại sao xử lý tiếng Việt khó hơn việc đơn giản tách chuỗi theo dấu cách?

**Gợi ý:** Dấu cách trong tiếng Việt thường phân tách âm tiết, không luôn phân tách từ; nhiều từ gồm nhiều tiếng như “viêm phổi”, “học máy”.

### 15. Tokenization và word segmentation có giống nhau không?

**Gợi ý:** Không hoàn toàn. Word segmentation xác định ranh giới từ tiếng Việt; tokenizer của ViT5 dùng SentencePiece để chia thành subword/token theo từ vựng mô hình.

### 16. Tại sao khi làm sạch dữ liệu y khoa phải giữ lại chữ số?

**Gợi ý:** Chữ số có thể biểu diễn liều lượng, tuổi, thời gian, chỉ số xét nghiệm; xóa chúng có thể làm thay đổi ý nghĩa y khoa.

### 17. Bag of Words, TF-IDF và contextual embedding khác nhau thế nào?

**Gợi ý:** BoW đếm từ; TF-IDF thêm trọng số theo độ hiếm; contextual embedding biểu diễn token phụ thuộc ngữ cảnh và giữ nhiều thông tin ngữ nghĩa hơn.

### 18. Tại sao một từ cần vector khác nhau trong những ngữ cảnh khác nhau?

**Gợi ý:** Từ có thể đa nghĩa; contextual embedding giúp mô hình biểu diễn nghĩa phù hợp với câu hiện tại.

### 19. Pre-training và fine-tuning khác nhau như thế nào?

**Gợi ý:** Pre-training học tri thức ngôn ngữ tổng quát trên dữ liệu lớn; fine-tuning tiếp tục cập nhật mô hình trên nhiệm vụ hoặc miền dữ liệu cụ thể.

### 20. Hallucination trong tóm tắt văn bản là gì và vì sao đặc biệt nguy hiểm trong y khoa?

**Gợi ý:** Mô hình sinh chi tiết không được hỗ trợ bởi văn bản nguồn; thông tin sai về chẩn đoán, thuốc hoặc liều lượng có thể gây hậu quả nghiêm trọng.

---

## III. TextRank

### 21. TextRank thuộc tóm tắt trích xuất hay trừu tượng?

**Gợi ý:** Trích xuất, vì thuật toán chọn lại các câu từ văn bản nguồn.

### 22. TextRank biểu diễn văn bản dưới dạng đồ thị như thế nào?

**Gợi ý:** Mỗi câu là một đỉnh; cạnh và trọng số cạnh biểu diễn mức tương đồng giữa hai câu.

### 23. Độ tương đồng giữa các câu có thể được tính bằng cách nào?

**Gợi ý:** TF-IDF cosine similarity hoặc embedding cosine similarity; cần nêu đúng cách đã cài đặt nếu được hỏi về mã nguồn.

### 24. PageRank có vai trò gì trong TextRank?

**Gợi ý:** Lan truyền độ quan trọng trên đồ thị để xếp hạng câu; câu liên kết mạnh với nhiều câu quan trọng khác sẽ có điểm cao.

### 25. TextRank có cần dữ liệu gán nhãn để huấn luyện không?

**Gợi ý:** Không; đây là phương pháp không giám sát.

### 26. Ưu điểm chính của TextRank là gì?

**Gợi ý:** Đơn giản, nhanh, không cần dữ liệu huấn luyện, ít bịa thông tin vì dùng nguyên câu nguồn.

### 27. Nhược điểm chính của TextRank là gì?

**Gợi ý:** Các câu được chọn có thể lặp ý, rời rạc hoặc thiếu liên kết; khó diễn đạt cô đọng bằng câu mới.

### 28. Sau khi chọn các câu có điểm cao, tại sao thường phải sắp xếp lại theo vị trí gốc?

**Gợi ý:** Để giữ trình tự diễn biến và tăng tính mạch lạc thay vì sắp theo điểm quan trọng.

### 29. Nếu hai câu gần như giống nhau đều có điểm cao, em xử lý thế nào?

**Gợi ý:** Dùng ngưỡng tương đồng, Maximal Marginal Relevance hoặc kiểm tra trùng lặp để tăng tính đa dạng.

### 30. Trong miền y khoa, khi nào TextRank có thể an toàn hơn ViT5?

**Gợi ý:** Khi yêu cầu ưu tiên tuyệt đối việc không tạo thông tin mới và có thể chấp nhận bản tóm tắt kém tự nhiên hơn.

---

## IV. Seq2Seq, LSTM và Attention

### 31. Kiến trúc Seq2Seq gồm những phần nào?

**Gợi ý:** Encoder nhận chuỗi nguồn và tạo biểu diễn; Decoder sinh chuỗi đích từng bước.

### 32. Vai trò của Encoder và Decoder trong mô hình LSTM của em là gì?

**Gợi ý:** Encoder mã hóa văn bản; Decoder sử dụng trạng thái và ngữ cảnh Attention để dự đoán token tiếp theo.

### 33. Tại sao cần các token SOS, EOS, UNK và PAD?

**Gợi ý:** SOS bắt đầu giải mã; EOS kết thúc; UNK đại diện token ngoài từ điển; PAD làm các chuỗi trong batch có cùng chiều dài.

### 34. RNN gặp vấn đề gì với chuỗi dài?

**Gợi ý:** Khó truyền thông tin qua nhiều bước, dễ vanishing/exploding gradient và phải xử lý tuần tự.

### 35. LSTM cải thiện RNN bằng cách nào?

**Gợi ý:** Cell state và các cổng input/forget/output giúp điều khiển luồng thông tin; giảm nhưng không loại bỏ hoàn toàn khó khăn với chuỗi rất dài.

### 36. Attention trong Seq2Seq giải quyết vấn đề gì?

**Gợi ý:** Cho Decoder truy cập trực tiếp các trạng thái Encoder thay vì phụ thuộc vào một vector ngữ cảnh cố định.

### 37. Attention Masking dùng để làm gì?

**Gợi ý:** Loại vị trí PAD khỏi phép tính Attention để mô hình không phân bổ trọng số cho dữ liệu rỗng.

### 38. Teacher Forcing là gì và tại sao báo cáo dùng tỷ lệ 50%?

**Gợi ý:** Khi train, dùng token đích đúng ở bước trước làm đầu vào Decoder; giúp hội tụ nhanh. Tỷ lệ 50% cân bằng giữa hướng dẫn bằng nhãn và làm quen với dự đoán của mô hình.

### 39. Nhược điểm của Teacher Forcing là gì?

**Gợi ý:** Exposure bias: lúc train mô hình thường nhìn token đúng, nhưng lúc inference phải dùng token tự dự đoán nên lỗi có thể tích lũy.

### 40. Vì sao LSTM trong đề tài chỉ đạt ROUGE-1 khoảng 0,21?

**Gợi ý:** Huấn luyện từ đầu, chỉ khoảng 3.182 mẫu thực sự dùng để train, từ vựng nhỏ, văn bản y khoa dài và không có tri thức tiếng Việt được pre-train.

### 41. Hàm loss giảm có đủ để kết luận mô hình tốt không?

**Gợi ý:** Không. Phải kiểm tra validation/test, ROUGE, chất lượng định tính và khả năng tổng quát hóa; loss train giảm vẫn có thể đi kèm overfitting.

### 42. Khi inference, vì sao không còn Teacher Forcing?

**Gợi ý:** Không có đáp án chuẩn; Decoder phải dùng token vừa dự đoán để sinh token tiếp theo.

---

## V. Attention, Transformer và ViT5

### 43. Attention và Transformer khác nhau thế nào?

**Gợi ý:** Attention là một cơ chế tính mức liên quan; Transformer là kiến trúc hoàn chỉnh sử dụng Attention cùng feed-forward, residual connection, layer normalization và thông tin vị trí.

### 44. ViT5 có bỏ Attention không?

**Gợi ý:** Không. Attention là thành phần trung tâm của ViT5; mô hình bỏ cấu trúc hồi quy LSTM chứ không bỏ Attention.

### 45. Self-Attention là gì?

**Gợi ý:** Mỗi token tạo truy vấn để tính mức liên quan với các token trong cùng chuỗi, từ đó tổng hợp biểu diễn theo ngữ cảnh.

### 46. Query, Key và Value có vai trò gì trong Attention?

**Gợi ý:** Query là thông tin đang cần tìm; Key dùng để so độ liên quan; Value là nội dung được tổng hợp theo trọng số Attention.

### 47. Công thức Scaled Dot-Product Attention là gì?

**Gợi ý:** `softmax(QKᵀ/√d_k)V`; chia cho căn bậc hai của số chiều key để logits không quá lớn và softmax ổn định hơn.

### 48. Multi-Head Attention có lợi ích gì?

**Gợi ý:** Nhiều head có thể học các quan hệ khác nhau song song, chẳng hạn quan hệ cú pháp, chủ thể, tên bệnh, thuốc và liều lượng.

### 49. Transformer cần Positional Encoding để làm gì?

**Gợi ý:** Self-Attention tự thân không biết thứ tự token; thông tin vị trí giúp phân biệt các trật tự khác nhau.

### 50. Encoder Self-Attention, Decoder Masked Self-Attention và Cross-Attention khác nhau thế nào?

**Gợi ý:** Encoder nhìn toàn bộ nguồn; Decoder chỉ nhìn các token đích đã sinh; Cross-Attention giúp Decoder truy cập biểu diễn nguồn từ Encoder.

### 51. Tại sao Decoder phải dùng causal mask?

**Gợi ý:** Ngăn mô hình nhìn token tương lai của bản tóm tắt trong lúc huấn luyện.

### 52. Transformer có ưu thế gì so với LSTM?

**Gợi ý:** Đường truyền thông tin giữa token ngắn hơn, xử lý song song khi train và mô hình hóa phụ thuộc xa tốt hơn; tuy nhiên Attention tốn bộ nhớ theo độ dài chuỗi.

### 53. Độ phức tạp `O(N²)` của Self-Attention có ý nghĩa gì?

**Gợi ý:** Ma trận Attention có kích thước theo bình phương số token; khi chuỗi dài gấp đôi, chi phí phần Attention có thể tăng khoảng bốn lần.

### 54. ViT5 là gì và tại sao phù hợp với đề tài?

**Gợi ý:** Mô hình text-to-text encoder-decoder dựa trên T5, được pre-train cho tiếng Việt; phù hợp với tác vụ nhận văn bản và sinh bản tóm tắt.

### 55. Vì sao không chọn PhoBERT làm mô hình sinh tóm tắt chính?

**Gợi ý:** PhoBERT chủ yếu là encoder-only, phù hợp bài toán hiểu/trích xuất; muốn sinh văn bản cần thêm Decoder. ViT5 có sẵn kiến trúc encoder-decoder sinh chuỗi.

### 56. Tiền tố `summarize:` trong dữ liệu ViT5 dùng để làm gì?

**Gợi ý:** T5 biểu diễn nhiều nhiệm vụ theo dạng text-to-text; prefix chỉ rõ nhiệm vụ và phải nhất quán giữa train và inference.

### 57. ViT5 có phải lúc nào cũng tốt hơn TextRank không?

**Gợi ý:** Không. ViT5 có khả năng diễn đạt tốt hơn nhưng tốn tài nguyên và có nguy cơ hallucination; lựa chọn phụ thuộc yêu cầu trung thực, tốc độ và phần cứng.

### 58. Có nên gọi ViT5-base là “LLM tiên tiến nhất” không?

**Gợi ý:** Nên diễn đạt thận trọng: đây là mô hình Transformer text-to-text được pre-train cho tiếng Việt và phù hợp với đề tài; “tiên tiến nhất” cần benchmark và mốc thời gian để chứng minh.

---

## VI. Dữ liệu và tiền xử lý

### 59. Dữ liệu của đề tài đến từ đâu và có bao nhiêu mẫu?

**Gợi ý:** Phải phân biệt các giai đoạn: khoảng 7.000 bài ở thử nghiệm LSTM; 1.000 bản ghi thu thập ở tuần 3-4; nguồn y khoa hơn 10.600 văn bản ở giai đoạn sau; Phase 2 cuối có 6.909 train, 859 validation và 871 test.

### 60. Tại sao các con số 1.000, 7.000 và 10.600 cùng xuất hiện trong báo cáo?

**Gợi ý:** Đây là các nguồn/giai đoạn thí nghiệm khác nhau, không phải cùng một tập. Khi bảo vệ phải nói rõ nguồn nào dùng cho mô hình nào và sau lọc còn bao nhiêu mẫu.

### 61. Một mẫu dữ liệu huấn luyện tóm tắt gồm những trường nào?

**Gợi ý:** Tối thiểu gồm văn bản nguồn và bản tóm tắt tham chiếu; có thể có ID/metadata để truy vết và chia tập theo bài gốc.

### 62. Tại sao phải chia train, validation và test?

**Gợi ý:** Train cập nhật trọng số; validation chọn siêu tham số/checkpoint; test chỉ dùng đánh giá cuối để ước lượng khả năng tổng quát hóa.

### 63. Data leakage là gì?

**Gợi ý:** Thông tin từ validation/test lọt vào train, khiến điểm đánh giá cao giả tạo.

### 64. Khi dùng sliding window, làm sao tránh leakage?

**Gợi ý:** Chia tập theo ID bài viết gốc trước hoặc đảm bảo mọi chunk của cùng một bài chỉ nằm trong một split; không chia ngẫu nhiên từng chunk độc lập.

### 65. Nếu gán cùng bản tóm tắt toàn bài cho mọi chunk thì có vấn đề gì?

**Gợi ý:** Một chunk có thể không chứa thông tin tương ứng với toàn bộ summary, tạo cặp nguồn-nhãn sai. Cần summary theo chunk, chọn chunk liên quan hoặc dùng chiến lược tổng hợp nhiều chunk.

### 66. Text chunking bằng sliding window hoạt động như thế nào?

**Gợi ý:** Chia văn bản dài thành các đoạn token có độ dài giới hạn và phần chồng lấn để giảm mất ngữ cảnh tại biên.

### 67. Chunking khác truncation như thế nào?

**Gợi ý:** Truncation bỏ phần vượt giới hạn; chunking giữ nhiều phần của văn bản nhưng phải giải quyết việc tổng hợp kết quả giữa các chunk.

### 68. Vì sao chọn `max_source_length = 768`?

**Gợi ý:** Cân bằng mức bao phủ nội dung với VRAM/thời gian; cần nói đây là lựa chọn thực nghiệm theo tokenizer và GPU, không phải độ dài tối ưu tuyệt đối.

### 69. K-Means được dùng vào mục đích gì trong dữ liệu?

**Gợi ý:** Nhóm các mẫu có biểu diễn tương tự để phân tích phân bố và chọn các mẫu đại diện, giảm trùng lặp nhưng vẫn giữ tính đa dạng.

### 70. Trước khi chạy K-Means, văn bản được biểu diễn thành vector bằng cách nào?

**Gợi ý:** Đây là câu phải trả lời theo mã nguồn/thí nghiệm thực tế. Không nói K-Means chạy trực tiếp trên chuỗi; cần nêu rõ TF-IDF hay embedding, cách chuẩn hóa và số chiều.

### 71. Chọn số cụm K dựa trên tiêu chí nào?

**Gợi ý:** Có thể dựa trên elbow, silhouette, ngân sách coreset và kiểm tra phân bố chủ đề. Báo cáo hiện chưa trình bày rõ nên cần chuẩn bị bằng chứng từ mã nguồn.

### 72. Herding là gì và được dùng sau K-Means như thế nào?

**Gợi ý:** Chọn tuần tự các mẫu sao cho trung bình embedding của tập được chọn xấp xỉ trung bình phân bố/nhóm; mục tiêu là tạo coreset đại diện.

### 73. Làm sao chứng minh K-Means và Herding thực sự giúp giảm overfitting?

**Gợi ý:** Cần thí nghiệm đối chứng có/không có chọn mẫu trên cùng split, cùng ngân sách huấn luyện và nhiều seed; chỉ mô tả trực giác chưa phải bằng chứng.

### 74. Vì sao lưu Phase 1 dưới Parquet và Phase 2 dưới CSV?

**Gợi ý:** Parquet nén tốt, giữ schema và đọc theo cột hiệu quả; CSV đơn giản, dễ kiểm tra và trao đổi nhưng lớn hơn và yếu về kiểu dữ liệu.

---

## VII. Fine-tuning và tối ưu GPU

### 75. Tại sao huấn luyện theo hai giai đoạn Phase 1 và Phase 2?

**Gợi ý:** Phase 1 thích nghi tác vụ tóm tắt tổng quát; Phase 2 tiếp tục thích nghi miền y khoa. Cần so sánh trên cùng dữ liệu Phase 2 để đo đóng góp của bước thích nghi miền.

### 76. Fine-tuning toàn bộ và LoRA khác nhau như thế nào?

**Gợi ý:** Full fine-tuning cập nhật toàn bộ trọng số, tốn VRAM và lưu trữ hơn; LoRA đóng băng trọng số gốc và học các ma trận hạng thấp ở một số lớp. Cấu hình cuối của đề tài tắt LoRA.

### 77. Learning rate có vai trò gì?

**Gợi ý:** Quyết định độ lớn bước cập nhật trọng số; quá cao dễ mất ổn định/catastrophic forgetting, quá thấp hội tụ chậm hoặc không thích nghi đủ.

### 78. Tại sao Phase 2 dùng learning rate nhỏ hơn Phase 1?

**Gợi ý:** Checkpoint đã học tác vụ tổng quát; Phase 2 chỉ cần điều chỉnh nhẹ sang miền y khoa và hạn chế phá hỏng tri thức đã có. Cấu hình chạy cuối ghi nhận `5e-6`.

### 79. Batch size và gradient accumulation liên hệ thế nào?

**Gợi ý:** Effective batch trên một GPU xấp xỉ `per_device_batch_size × gradient_accumulation_steps`; nếu nhiều GPU còn nhân số GPU.

### 80. Gradient accumulation có làm giảm bộ nhớ giống hệt tăng batch vật lý không?

**Gợi ý:** Nó giả lập gradient của batch lớn qua nhiều micro-batch, giảm VRAM cho dữ liệu/kích hoạt; nhưng thời gian tăng và một số hành vi phụ thuộc batch có thể không hoàn toàn giống.

### 81. Mixed Precision fp16 giúp gì và có rủi ro gì?

**Gợi ý:** Giảm VRAM, có thể tăng tốc trên GPU phù hợp; rủi ro underflow/overflow nên thường cần loss scaling và kiểm tra NaN.

### 82. Gradient Checkpointing hoạt động như thế nào?

**Gợi ý:** Không lưu toàn bộ activation ở forward; tính lại một phần khi backward để đổi thêm thời gian tính toán lấy giảm VRAM.

### 83. Adafactor khác AdamW ở điểm nào?

**Gợi ý:** Adafactor factor hóa thống kê moment bậc hai của ma trận, giảm bộ nhớ optimizer; phù hợp mô hình T5 lớn nhưng vẫn cần cấu hình learning rate cẩn thận.

### 84. Warmup và cosine scheduler có tác dụng gì?

**Gợi ý:** Warmup tăng learning rate từ thấp để ổn định đầu quá trình; cosine decay giảm dần learning rate để tinh chỉnh nhẹ hơn về cuối.

### 85. Weight decay dùng để làm gì?

**Gợi ý:** Regularization trọng số, giúp hạn chế trọng số quá lớn và có thể giảm overfitting; không nên áp dụng máy móc cho mọi tham số như bias/norm.

### 86. Label smoothing là gì?

**Gợi ý:** Phân phối một phần xác suất khỏi nhãn đúng tuyệt đối để giảm overconfidence; quá lớn có thể làm giảm khả năng học token chính xác.

### 87. Early stopping hoạt động dựa trên chỉ số nào trong đề tài?

**Gợi ý:** Theo dõi ROUGE-L validation; dừng sau số lần đánh giá liên tiếp không cải thiện theo patience đã đặt.

### 88. Tại sao chọn checkpoint tốt nhất theo ROUGE-L thay vì train loss?

**Gợi ý:** Mục tiêu cuối là chất lượng bản tóm tắt trên dữ liệu chưa thấy; loss token-level không luôn tương quan trực tiếp với chất lượng chuỗi sinh.

### 89. Seed 42 có bảo đảm thí nghiệm tái lập hoàn toàn không?

**Gợi ý:** Không tuyệt đối; còn phiên bản thư viện, CUDA, thuật toán không deterministic, phần cứng, thứ tự dữ liệu và cấu hình môi trường.

### 90. Catastrophic forgetting có thể xảy ra ở Phase 2 không?

**Gợi ý:** Có; fine-tuning miền hẹp có thể làm giảm năng lực tổng quát. Có thể kiểm tra lại trên tập Phase 1 và dùng LR nhỏ, trộn dữ liệu hoặc regularization.

---

## VIII. Quá trình sinh văn bản

### 91. Greedy Search và Beam Search khác nhau thế nào?

**Gợi ý:** Greedy chọn token tốt nhất tại mỗi bước; Beam Search giữ nhiều chuỗi ứng viên và chọn theo điểm toàn chuỗi, tốn tính toán hơn.

### 92. Tăng `num_beams` có luôn làm kết quả tốt hơn không?

**Gợi ý:** Không. Beam lớn tăng thời gian/bộ nhớ, đôi khi làm câu chung chung hoặc quá ưu tiên chuỗi xác suất cao; phải đánh giá thực nghiệm.

### 93. `length_penalty` dùng để làm gì?

**Gợi ý:** Điều chỉnh cách điểm của Beam Search ưu tiên chuỗi theo độ dài; cần kiểm thử vì tác động cụ thể phụ thuộc cách thư viện chuẩn hóa điểm.

### 94. `min_length` và `max_length` có tác dụng gì?

**Gợi ý:** Giới hạn độ dài đầu ra; tránh summary quá ngắn hoặc quá dài, nhưng có thể cắt câu hoặc ép mô hình sinh thêm nếu đặt không phù hợp.

### 95. `no_repeat_ngram_size = 3` có ý nghĩa gì?

**Gợi ý:** Ngăn mô hình tạo lại một trigram đã xuất hiện trong cùng chuỗi; giảm lặp nhưng có thể làm khó các cụm thuật ngữ buộc phải lặp.

### 96. Tỷ lệ nén được tính như thế nào?

**Gợi ý:** Phải nói rõ quy ước. Thông thường mức giảm là `1 - độ dài tóm tắt/độ dài nguồn`; cần thống nhất đơn vị token hay từ.

### 97. Nếu văn bản gồm nhiều chunk, em tổng hợp các bản tóm tắt chunk như thế nào?

**Gợi ý:** Có thể dùng map-reduce summarization: tóm tắt từng chunk rồi tóm tắt lần hai; cần kiểm soát trùng lặp và mất liên kết toàn văn bản.

---

## IX. Đánh giá ROUGE và phân tích kết quả

### 98. ROUGE-1, ROUGE-2 và ROUGE-L đo điều gì?

**Gợi ý:** Mức trùng unigram, bigram và chuỗi con chung dài nhất giữa candidate với reference.

### 99. Precision, Recall và F1 trong ROUGE khác nhau thế nào?

**Gợi ý:** Precision đo phần candidate khớp reference; Recall đo phần reference được candidate bao phủ; F1 là trung bình điều hòa cân bằng hai phía.

### 100. Vì sao trong báo cáo sử dụng F1 thay vì chỉ Recall?

**Gợi ý:** Chỉ Recall có thể được tăng bằng cách sinh bản rất dài; F1 cân bằng độ bao phủ và độ cô đọng/chính xác.

### 101. Kết quả cuối cùng của mô hình là bao nhiêu?

**Gợi ý:** Test 871 mẫu: loss 2,0192; ROUGE-1 54,75; ROUGE-2 26,13; ROUGE-L 36,55; độ dài sinh trung bình 38,6 token theo file kết quả.

### 102. Kết quả Phase 2 cải thiện bao nhiêu so với Phase 1 trên cùng tập test?

**Gợi ý:** Phase 1: 46,30/22,25/28,94; Phase 2: 54,75/26,13/36,55. Mức tăng: +8,45 ROUGE-1, +3,88 ROUGE-2, +7,61 ROUGE-L; loss giảm khoảng 1,0718.

### 103. Vì sao phải so sánh hai mô hình trên cùng một tập test và cùng cấu hình sinh?

**Gợi ý:** Nếu dữ liệu hoặc decoding khác nhau thì chênh lệch có thể đến từ điều kiện đánh giá, không phải từ fine-tuning.

### 104. Tại sao kết quả ViT5 gốc trên 5 mẫu là ROUGE-1 66,01 nhưng mô hình cuối chỉ đạt 54,75?

**Gợi ý:** Hai số không thể so trực tiếp: 66,01 chỉ là smoke test trên 5 mẫu ngẫu nhiên, còn 54,75 là test độc lập 871 mẫu và có thể khác dữ liệu/cấu hình. So sánh hợp lệ là Phase 1 46,30 với Phase 2 54,75 trên cùng 871 mẫu.

### 105. ROUGE-2 tăng có chứng minh mô hình không hallucination không?

**Gợi ý:** Không. Nó chỉ cho thấy bigram trùng reference nhiều hơn. Phải đánh giá factual consistency bằng kiểm tra thực thể/số liệu, entailment, thước đo chuyên biệt và đánh giá con người.

### 106. ROUGE cao có đồng nghĩa bản tóm tắt tốt không?

**Gợi ý:** Không hoàn toàn. ROUGE phụ thuộc trùng từ và reference, chưa đo đầy đủ tính đúng sự thật, mạch lạc, mức hữu ích hay khả năng diễn đạt tương đương bằng từ khác.

### 107. Vì sao cần đánh giá định tính bên cạnh ROUGE?

**Gợi ý:** Để kiểm tra tính đúng, mạch lạc, không lặp, giữ thực thể y khoa và phát hiện lỗi mà độ trùng n-gram bỏ sót.

### 108. Có thể bổ sung thước đo nào ngoài ROUGE?

**Gợi ý:** BERTScore/semantic similarity, factual consistency, entity/number accuracy, compression ratio và đánh giá của người có chuyên môn y khoa.

### 109. BERTScore khắc phục hạn chế nào của ROUGE?

**Gợi ý:** So sánh embedding theo ngữ nghĩa, nên nhận biết các cách diễn đạt khác từ nhưng gần nghĩa; tuy vậy vẫn không tự động bảo đảm factuality.

### 110. Validation và test có điểm gần nhau đã đủ chứng minh không overfitting chưa?

**Gợi ý:** Chưa đủ. Đây là tín hiệu tích cực nhưng cần đường cong train/validation, nhiều checkpoint, nhiều seed và xác nhận split không leakage.

### 111. Test loss 2,019 có thể diễn giải trực tiếp là “sai 2%” không?

**Gợi ý:** Không. Đây thường là cross-entropy trung bình theo token; không phải tỷ lệ phần trăm lỗi và không so được tùy ý giữa tokenizer/dataset khác nhau.

### 112. Tại sao ROUGE-L được dùng chọn best checkpoint?

**Gợi ý:** Nó xem xét chuỗi con chung theo thứ tự, phù hợp để phản ánh một phần cấu trúc bản tóm tắt; đây vẫn là lựa chọn thiết kế cần kết hợp đánh giá khác.

### 113. Nếu có nhiều bản tóm tắt tham chiếu cho một văn bản thì đánh giá thế nào?

**Gợi ý:** Tính với nhiều reference theo chính sách của thư viện, chẳng hạn lấy max hoặc tổng hợp; phải ghi rõ cách làm để kết quả tái lập.

### 114. Em có kiểm định ý nghĩa thống kê của mức tăng ROUGE không?

**Gợi ý:** Báo cáo chưa thể hiện. Có thể dùng bootstrap confidence interval hoặc paired bootstrap trên cùng các mẫu test để xác định mức tăng có ổn định hay không.

---

## X. Streamlit và triển khai sản phẩm

### 115. Luồng xử lý của Web Demo diễn ra như thế nào?

**Gợi ý:** Nhận văn bản → kiểm tra đầu vào → thêm prefix/tokenize → model.generate → decode → hiển thị summary và tỷ lệ nén.

### 116. Tại sao chọn Streamlit?

**Gợi ý:** Phù hợp tạo demo ML nhanh bằng Python, dễ tích hợp model và widget; không nhất thiết là lựa chọn tối ưu cho hệ thống production tải lớn.

### 117. Làm sao tránh tải lại mô hình sau mỗi lần người dùng tương tác?

**Gợi ý:** Dùng cơ chế cache tài nguyên của Streamlit, khởi tạo model/tokenizer một lần và tái sử dụng.

### 118. Ứng dụng chạy trên CPU được không?

**Gợi ý:** Có thể nhưng chậm hơn; cần chọn device động, giới hạn độ dài/beam và thông báo thời gian chờ.

### 119. Nếu người dùng nhập văn bản dài hơn 768 token thì hệ thống làm gì?

**Gợi ý:** Không nên âm thầm cắt mất nội dung; cần thông báo, chunking rồi tổng hợp, hoặc từ chối có hướng dẫn tùy thiết kế.

### 120. Những kiểm tra đầu vào nào cần có?

**Gợi ý:** Văn bản rỗng/quá ngắn/quá dài, ngôn ngữ không phù hợp, ký tự bất thường, giới hạn tài nguyên và nội dung nhạy cảm.

### 121. Vì sao bản demo chưa thể được xem là công cụ hỗ trợ quyết định y khoa?

**Gợi ý:** Chưa có thẩm định lâm sàng, factuality đầy đủ, giám sát chuyên gia, quản lý rủi ro và các yêu cầu pháp lý/bảo mật cần thiết.

### 122. Nếu triển khai production, em sẽ cải tiến kiến trúc như thế nào?

**Gợi ý:** Tách frontend/API/model service, batching/queue, cache, logging và monitoring, xác thực, rate limit, container hóa và quản lý phiên bản model.

---

## XI. Hạn chế, hướng phát triển và câu hỏi phản biện

### 123. Hạn chế lớn nhất của hệ thống hiện tại là gì?

**Gợi ý:** Đầu vào hữu hạn, đánh giá chủ yếu bằng ROUGE, chưa có đánh giá chuyên gia y khoa/factuality, thử nghiệm siêu tham số và kiểm định thống kê còn hạn chế.

### 124. Tại sao RAG có thể hỗ trợ bài toán và có rủi ro gì?

**Gợi ý:** Retrieval có thể tìm đoạn liên quan trước khi tóm tắt; nhưng lấy kiến thức ngoài nguồn có thể làm bản tóm tắt lẫn thông tin không thuộc văn bản. Cần xác định rõ mục tiêu là tóm tắt nguồn hay trả lời có bổ sung kiến thức.

### 125. Nếu tiếp tục đề tài, thí nghiệm quan trọng nhất em sẽ làm là gì?

**Gợi ý:** Đánh giá factuality và đánh giá mù bởi người có chuyên môn; đồng thời ablation pipeline dữ liệu/chunking và so sánh baseline công bằng.

### 126. Ablation study là gì và đề tài có thể ablation những thành phần nào?

**Gợi ý:** Loại/thay từng thành phần để đo đóng góp: K-Means/Herding, Phase 1, chunking, beam size, gradient checkpointing hoặc tập dữ liệu chuyên ngành.

### 127. Nếu ROUGE tăng nhưng chuyên gia đánh giá chất lượng giảm thì em tin kết quả nào?

**Gợi ý:** Với ứng dụng y khoa, ưu tiên tiêu chí gắn với mục tiêu sử dụng và đánh giá chuyên gia được thiết kế tốt; phân tích vì sao metric tự động lệch thay vì chọn một con số máy móc.

### 128. Làm thế nào để kiểm tra mô hình giữ đúng tên thuốc, liều lượng và con số?

**Gợi ý:** Trích xuất thực thể/số từ nguồn và summary, đo precision/recall, kiểm tra quan hệ thực thể-giá trị và lấy mẫu đánh giá thủ công.

### 129. Nếu reference cũng có lỗi thì ROUGE phản ánh điều gì?

**Gợi ý:** Mô hình có thể bị phạt khi đúng hoặc được thưởng khi lặp lỗi; cần kiểm soát chất lượng nhãn, nhiều reference và đánh giá nguồn-grounded.

### 130. Em làm gì để bảo đảm khả năng tái lập thí nghiệm?

**Gợi ý:** Lưu YAML và `resolved_config.json`, seed, phiên bản code/dữ liệu/thư viện, checkpoint, log, cách split và lệnh chạy; cấu hình thực chạy phải là nguồn sự thật cuối cùng.

### 131. Vì sao cấu hình trong báo cáo và file cấu hình có thể không giống nhau?

**Gợi ý:** YAML có thể là bản dự kiến, còn tham số bị override khi chạy. Phải dùng `resolved_config.json` và log của run sinh kết quả để báo cáo, đồng thời sửa bảng để tránh mâu thuẫn.

### 132. Cấu hình thực chạy Phase 2 trong `resolved_config.json` là gì?

**Gợi ý:** LR `5e-6`, batch/device 8, accumulation 2, fp16, Adafactor, gradient checkpointing tắt, beam 2. Các điểm này khác một số mô tả/bảng trong PDF nên cần chủ động xác minh trước khi bảo vệ.

### 133. Nếu giảng viên nói “em chỉ dùng mô hình có sẵn”, em trả lời thế nào?

**Gợi ý:** Thừa nhận dùng checkpoint pre-trained là thực hành chuẩn của transfer learning; đóng góp nằm ở thiết kế dữ liệu, pipeline hai phase, chiến lược tối ưu, đánh giá công bằng và triển khai. Không nhận là tự thiết kế ViT5.

### 134. Nếu giảng viên yêu cầu chứng minh mô hình hiểu ngữ nghĩa, em làm gì?

**Gợi ý:** ROUGE chưa đủ. Trình bày ví dụ diễn đạt lại đúng nghĩa, bộ ca kiểm thử đối nghịch, BERTScore/factuality và đánh giá con người.

### 135. Tại sao không được tuyên bố mô hình “giải quyết triệt để hallucination”?

**Gợi ý:** Không có mô hình sinh nào được bảo đảm chỉ từ ROUGE; phải nói “giảm lỗi quan sát được trên tập đánh giá” và nêu phương pháp kiểm tra cụ thể.

---

## XII. Mười câu cần học kỹ nhất trước khi bảo vệ

1. Trình bày đề tài trong hai phút và nêu đóng góp cá nhân.
2. So sánh TextRank, LSTM + Attention và ViT5.
3. Phân biệt Attention với Transformer; giải thích ba loại Attention trong ViT5.
4. Giải thích vì sao chọn ViT5 thay vì PhoBERT.
5. Trình bày nguồn dữ liệu và giải thích các con số 1.000, 7.000, 10.600 và bộ split cuối.
6. Giải thích chunking, nguy cơ leakage và cách ghép kết quả nhiều chunk.
7. Trình bày Phase 1, Phase 2 và cấu hình thực chạy.
8. Giải thích ROUGE-1/2/L, kết quả cuối và mức cải thiện trên cùng tập test.
9. Giải thích vì sao ROUGE-1 66,01 của smoke test không mâu thuẫn trực tiếp với 54,75 của test cuối.
10. Thừa nhận đúng các hạn chế: ROUGE không chứng minh hết chất lượng hoặc hallucination; chưa đủ cơ sở để sử dụng cho quyết định y khoa.

---

## XIII. Mẫu trả lời tổng quan ngắn

> Đề tài của em nghiên cứu bài toán tóm tắt văn bản tiếng Việt trong miền y khoa. Em lần lượt khảo sát TextRank, Seq2Seq LSTM kết hợp Attention và ViT5. TextRank nhanh và ít bịa thông tin nhưng bản tóm tắt có thể rời rạc. LSTM có khả năng sinh văn bản mới nhưng mô hình huấn luyện từ đầu trên dữ liệu nhỏ chỉ đạt ROUGE-1 khoảng 0,21. Vì vậy, em chuyển sang ViT5, một mô hình Transformer encoder-decoder đã được pre-train cho tiếng Việt.
>
> Em xây dựng pipeline xử lý dữ liệu, chia tập để tránh leakage, huấn luyện theo hai giai đoạn và tối ưu cho GPU giới hạn bằng fp16, gradient accumulation và Adafactor. Trên cùng tập test y khoa 871 mẫu, checkpoint Phase 1 đạt ROUGE-1/2/L là 46,30/22,25/28,94; sau Phase 2 đạt 54,75/26,13/36,55. Cuối cùng, em tích hợp checkpoint tốt nhất vào Web Demo Streamlit.
>
> Hạn chế của đề tài là độ dài đầu vào còn giới hạn, đánh giá chủ yếu dựa trên ROUGE và chưa có đánh giá đầy đủ bởi chuyên gia y khoa. Vì vậy, sản phẩm hiện là bản demo nghiên cứu, chưa phải công cụ hỗ trợ quyết định lâm sàng.

