# Các tham số học máy

## dropout: số lượng bị bịt mắt

    Hãy tưởng tượng bạn có 100 học sinh (tương đương 100 nơ-ron thần kinh trong mô hình AI) cùng nhau giải 1 bài toán. Nếu ngày nào 100 học sinh này cũng làm chung, sẽ có hiện tượng "ỷ lại": một vài học sinh giỏi sẽ làm hết, những học sinh khác chỉ chép bài. Dẫn đến khi đi thi thật, học sinh giỏi làm bài sai thì cả lớp sai theo (thuật ngữ gọi là Overfitting - Học vẹt).

    Giải pháp (Dropout): Trong lúc học ở nhà (Training), thỉnh thoảng thầy giáo sẽ ngẫu nhiên bịt mắt 10% số học sinh (Dropout = 0.1). Bọn trẻ không được phép nhìn bài nhau nữa, bắt buộc những đứa học sinh lười cũng phải tự động não suy nghĩ. Nhờ vậy, khi ra chiến trường (Test), cả đội hình sẽ mạnh mẽ và chống chịu tốt hơn rất nhiều.

## LoRA - Low-Rank Adaptation

### định nghĩa

    Là kỹ thuật thuộc nhóm PEFT(parameter-efficient Fine-Turning)
    Được sử dụng để tinh chỉnh(Fine-Turn) các LLM hiệu quả

### Hoạt động

- LoRA  không cập nhật toàn bộ hàng tỷ tham số của mô hình gốc:
- **Đóng băng mô hình gốc:** Toàn bộ trọng số ban đầu được giữ
- **Thêm ma trận nhỏ:** Thêm các ma trận nhỏ - ma trận phân hạng (rank decomposition matries) bên cạnh các lớp của mô hình(lớp attention)
- **Chỉ huấn luyện ma trận ảo:** Chỉ cập nhật các ma trận nhỏ này khi Fine-Turn
-
