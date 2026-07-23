# Tuần 3–4 — Transformer sinh tóm tắt và thu thập dữ liệu

Module này là phần thực hành độc lập cho hai tuần giữa kỳ thực tập. Phạm vi
được giữ đúng theo kế hoạch:

- **Tuần 3:** gọi một checkpoint seq2seq đã huấn luyện sẵn (mặc định là
  `VietAI/vit5-base-vietnews-summarization`), sinh tóm tắt và đo ROUGE-1,
  ROUGE-2, ROUGE-L.
- **Tuần 4:** chuẩn hóa tối thiểu, kiểm tra chất lượng và lưu một tập dữ liệu
  thô. Module này **không fine-tune** và **không chia train/validation/test**;
  hai việc đó thuộc Tuần 5–6.

## Cấu trúc

```text
summarization/
├── src/week34_summarization/     # Module dùng chung
├── scripts/
│   ├── run_inference_and_rouge.py # Tuần 3
│   └── prepare_raw_dataset.py     # Tuần 4
├── notebooks/
│   └── week34_inference_and_data.ipynb # Chạy quy trình trên Jupyter/Colab
├── data/
│   ├── raw/                       # Dữ liệu thô đã chuẩn hóa tối thiểu
│   └── samples/                   # Mẫu nhỏ để kiểm thử pipeline
├── results/                       # Metrics và dự đoán, được gitignore
└── tests/                         # Kiểm thử không cần tải model
```

## Cài đặt

```bash
cd "tuan 3-4/summarization"
python -m pip install -e .
```

## Tuần 3 — Inference và ROUGE

Nếu muốn chạy theo notebook, mở
[`week34_inference_and_data.ipynb`](week34_inference_and_data.ipynb)
trong Jupyter hoặc VS Code, đặt `PROJECT_ROOT` ở cell đầu tiên và chạy lần lượt
từ trên xuống. Notebook gọi đúng các module bên dưới, không phải phiên bản code
riêng.

Chạy thử năm mẫu có sẵn ở thư mục gốc của workspace:

```bash
python scripts/run_inference_and_rouge.py \
  --input ../../data/summarization_samples.json \
  --max-samples 5 \
  --output results/vit5_sample_5.json
```

Script xuất một JSON có metadata lần chạy, thiết lập sinh, ROUGE (precision,
recall, F1 trên thang 0–100), tỷ lệ rút gọn và từng dự đoán. Tất cả các chỉ số
trong `results` là kết quả thực thi; không có số liệu được điền sẵn.

Các tùy chọn thường dùng:

```bash
# Chạy trên CPU; thuận tiện khi máy không có CUDA.
python scripts/run_inference_and_rouge.py --device cpu --max-samples 2

# Đổi checkpoint hoặc cột đầu vào của một CSV khác.
python scripts/run_inference_and_rouge.py \
  --model VietAI/vit5-base-vietnews-summarization \
  --input data/raw/vietnews_medical_raw_1000.csv \
  --source-column article --summary-column summary \
  --max-samples 50
```

> Mặc định script thêm tiền tố `summarize: ` cho họ T5. Có thể thay đổi bằng
> `--prefix` nếu dùng checkpoint có quy ước đầu vào khác.

## Tuần 4 — Chuẩn bị dữ liệu thô

Ví dụ dưới dùng nguồn đã có trong workspace, chỉ lấy một biến thể để tránh gộp
những bản biến đổi của cùng văn bản:

```bash
python scripts/prepare_raw_dataset.py \
  --input ../../data/vietnamese-summarization/train/bio_medicine.csv \
  --output data/raw/vietnews_medical_raw_1000.csv \
  --dataset-name vietnews-medical \
  --max-records 1000
```

Đầu ra CSV thống nhất gồm `id`, `article`, `summary`, `source_dataset`,
`source_row`. File `*_audit.json` cùng thư mục ghi rõ số dòng đầu vào/đầu ra,
cột được nhận diện, số bản ghi bị loại và thống kê độ dài. Bước này chỉ:

1. chuẩn Unicode NFC, giải mã HTML và bỏ ký tự điều khiển/zero-width;
2. chuẩn hóa khoảng trắng;
3. loại cặp rỗng, quá ngắn, hoặc có tóm tắt dài hơn văn bản nguồn;
4. phát hiện cặp trùng chính xác để báo cáo.

Không loại trùng gần, chunking hoặc split ở đây, để dữ liệu vẫn là **raw** và
không vô tình làm thay đổi dữ liệu trước khi Tuần 5–6 audit kỹ hơn.

## Hợp đồng dữ liệu

Input có thể là JSON/JSONL/CSV. Các tên cột được tự nhận diện không phân biệt
hoa thường:

| Vai trò | Tên được hỗ trợ |
|---|---|
| Văn bản nguồn | `article`, `document`, `text`, `source` |
| Tóm tắt chuẩn | `summary`, `abstract`, `target` |
| Mã bản ghi | `id`, `_id`, `index` (tùy chọn) |

Dùng `--source-column` và `--summary-column` khi tên cột không nằm trong bảng.

## Kiểm thử nhanh

```bash
python -m unittest discover -s tests -v
```

## Chuyển giao cho Tuần 5–6

`data/raw/vietnews_medical_raw_1000.csv` là đầu vào đề xuất cho pipeline làm
sạch/chia tập dữ liệu/fine-tune ở `../../tuan 5-6/sumarization`. Khi chuyển giao,
giữ lại file audit để truy vết nguồn và tiêu chí lọc ban đầu.
