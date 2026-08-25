#!/usr/bin/env python3
"""Create clean, beginner-friendly figures for Chapters 1 and 2."""

from __future__ import annotations

import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path("bao-cao/figures_chapter2")
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

WHITE = "#FFFFFF"
INK = "#17212B"
MUTED = "#52606D"
NAVY = "#234E70"
BLUE = "#4C78A8"
TEAL = "#1F8A70"
GREEN = "#55A868"
GOLD = "#D69E2E"
ORANGE = "#E07A3F"
RED = "#C44E52"
PURPLE = "#7663A7"
LIGHT_BLUE = "#EAF3F8"
LIGHT_TEAL = "#E9F6F2"
LIGHT_GOLD = "#FFF7DD"
LIGHT_RED = "#FDEEEE"
LIGHT_GRAY = "#F4F6F8"
BORDER = "#C8D2DC"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    width: int,
    line_gap: int = 10,
    align: str = "left",
) -> int:
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    line_height = fnt.size + line_gap
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        line_width = bbox[2] - bbox[0]
        line_x = x
        if align == "center":
            line_x = x + (width - line_width) // 2
        elif align == "right":
            line_x = x + width - line_width
        draw.text((line_x, y), line, font=fnt, fill=fill)
        y += line_height
    return y


def rounded_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    outline: str = BORDER,
    width: int = 3,
    radius: int = 16,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str = TEAL,
    width: int = 8,
) -> None:
    draw.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 22
    left = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon((end, left, right), fill=color)


def title(draw: ImageDraw.ImageDraw, text: str, subtitle: str | None = None) -> None:
    draw.text((70, 48), text, font=font(50, True), fill=INK)
    if subtitle:
        draw.text((72, 112), subtitle, font=font(27), fill=MUTED)


def save(image: Image.Image, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUT_DIR / name, dpi=(180, 180), optimize=True)


def chapter1_taxonomy_figure() -> None:
    image = Image.new("RGB", (1800, 980), WHITE)
    draw = ImageDraw.Draw(image)
    title(
        draw,
        "Ba góc nhìn để phân loại bài toán tóm tắt",
        "Một hệ thống có thể đồng thời thuộc một nhánh ở mỗi cột",
    )

    columns = [
        (
            "THEO CÁCH TẠO",
            [
                ("Trích xuất", "Chọn lại câu có sẵn"),
                ("Trừu tượng", "Viết câu mới từ nội dung nguồn"),
                ("Kết hợp", "Chọn lọc rồi biên tập lại"),
            ],
            BLUE,
            LIGHT_BLUE,
        ),
        (
            "THEO SỐ ĐẦU VÀO",
            [
                ("Một tài liệu", "Tóm tắt một văn bản"),
                ("Nhiều tài liệu", "Tổng hợp nhiều nguồn cùng chủ đề"),
            ],
            TEAL,
            LIGHT_TEAL,
        ),
        (
            "THEO MỤC TIÊU",
            [
                ("Tổng quát", "Giữ các ý chính toàn văn bản"),
                ("Theo truy vấn", "Ưu tiên thông tin người đọc hỏi"),
                ("Theo lĩnh vực", "Giữ chi tiết quan trọng của miền"),
            ],
            GOLD,
            LIGHT_GOLD,
        ),
    ]

    for index, (heading, items, accent, fill) in enumerate(columns):
        x1 = 80 + index * 570
        x2 = x1 + 520
        rounded_box(draw, (x1, 190, x2, 890), "#FAFBFC", accent, 4, 14)
        draw.rectangle((x1, 190, x2, 275), fill=accent)
        heading_box = draw.textbbox((0, 0), heading, font=font(28, True))
        draw.text(
            (x1 + (520 - (heading_box[2] - heading_box[0])) / 2, 215),
            heading,
            font=font(28, True),
            fill=WHITE,
        )

        box_height = 155 if len(items) == 3 else 205
        gap = 38
        start_y = 320
        for item_index, (label, description) in enumerate(items):
            y1 = start_y + item_index * (box_height + gap)
            rounded_box(draw, (x1 + 35, y1, x2 - 35, y1 + box_height), fill, accent, 3, 12)
            draw.text((x1 + 62, y1 + 24), label, font=font(29, True), fill=accent)
            draw_wrapped(
                draw,
                (x1 + 62, y1 + 73),
                description,
                font(23),
                INK,
                395,
                8,
            )

    save(image, "chapter1_taxonomy.png")


def chapter1_timeline_figure() -> None:
    image = Image.new("RGB", (1800, 860), WHITE)
    draw = ImageDraw.Draw(image)
    title(
        draw,
        "Từ đếm từ đến mô hình sinh tạo",
        "Các mốc tiêu biểu được sử dụng để tổ chức phần tổng quan nghiên cứu",
    )

    milestones = [
        ("1958", "Luhn", "Tần suất từ", NAVY, LIGHT_GRAY),
        ("2004", "TextRank", "Xếp hạng đồ thị", BLUE, LIGHT_BLUE),
        ("2015", "Rush và cộng sự", "Sinh tóm tắt với Attention", PURPLE, "#F3EEFA"),
        ("2017", "Pointer-Generator\n& Transformer", "Sao chép có kiểm soát; Self-Attention", ORANGE, LIGHT_GOLD),
        ("2020", "BART, T5, PhoBERT", "Tiền huấn luyện quy mô lớn", TEAL, LIGHT_TEAL),
        ("2022", "ViT5", "Sinh văn bản tiếng Việt", RED, LIGHT_RED),
    ]

    line_y = 390
    draw.line((130, line_y, 1670, line_y), fill=BORDER, width=12)
    for index, (year, name, contribution, accent, fill) in enumerate(milestones):
        x = 165 + index * 285
        draw.ellipse((x - 24, line_y - 24, x + 24, line_y + 24), fill=accent, outline=WHITE, width=5)
        box_top = 180 if index % 2 == 0 else 475
        box_bottom = box_top + 240
        rounded_box(draw, (x - 125, box_top, x + 205, box_bottom), fill, accent, 3, 12)
        draw.text((x - 95, box_top + 20), year, font=font(30, True), fill=accent)
        draw_wrapped(draw, (x - 95, box_top + 70), name, font(25, True), INK, 270, 6)
        draw_wrapped(draw, (x - 95, box_top + 145), contribution, font(21), MUTED, 270, 6)
        connector_start = box_bottom if index % 2 == 0 else box_top
        draw.line((x, connector_start, x, line_y), fill=accent, width=4)

    draw.text(
        (90, 790),
        "Dòng thời gian mang tính khái quát; mỗi mốc đại diện cho một thay đổi đáng chú ý trong phương pháp tiếp cận.",
        font=font(23),
        fill=MUTED,
    )
    save(image, "chapter1_timeline.png")


def pipeline_figure() -> None:
    image = Image.new("RGB", (1800, 760), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "Toàn cảnh quy trình tóm tắt văn bản", "Mỗi khối trả lời một câu hỏi đơn giản của người đọc")

    items = [
        ("1", "Văn bản thô", "Máy nhận bài báo, báo cáo hoặc bệnh án", LIGHT_GRAY, NAVY),
        ("2", "Tiền xử lý", "Làm sạch, tách câu, tách từ tiếng Việt", LIGHT_BLUE, BLUE),
        ("3", "Biểu diễn số", "Đổi câu chữ thành vector để máy tính so sánh", LIGHT_GOLD, GOLD),
        ("4", "Tóm tắt", "Xếp hạng, gom cụm hoặc sinh câu mới", LIGHT_TEAL, TEAL),
        ("5", "Đánh giá", "So với bản chuẩn bằng ROUGE và kiểm tra thủ công", LIGHT_RED, RED),
    ]
    start_x = 65
    box_w, box_h, gap = 290, 260, 55
    y1 = 200
    for index, (number, heading, body, fill, accent) in enumerate(items):
        x1 = start_x + index * (box_w + gap)
        x2 = x1 + box_w
        rounded_box(draw, (x1, y1, x2, y1 + box_h), fill, accent, 4)
        draw.ellipse((x1 + 20, y1 + 22, x1 + 80, y1 + 82), fill=accent)
        number_bbox = draw.textbbox((0, 0), number, font=font(30, True))
        draw.text(
            (x1 + 50 - (number_bbox[2] - number_bbox[0]) / 2, y1 + 31),
            number,
            font=font(30, True),
            fill=WHITE,
        )
        draw.text((x1 + 22, y1 + 105), heading, font=font(31, True), fill=INK)
        draw_wrapped(draw, (x1 + 22, y1 + 158), body, font(24), MUTED, box_w - 44, 10)
        if index < len(items) - 1:
            arrow(draw, (x2 + 10, y1 + box_h // 2), (x2 + gap - 10, y1 + box_h // 2), NAVY, 7)

    rounded_box(draw, (120, 520, 1680, 690), "#FAFBFC", BORDER, 3, 12)
    draw.text((155, 552), "Ví dụ xuyên suốt", font=font(28, True), fill=TEAL)
    draw_wrapped(
        draw,
        (155, 602),
        "Bài báo 5 câu về khu cấp cứu mới → làm sạch và tách từ → tạo vector → chọn hoặc sinh câu tóm tắt → đối chiếu với bản tóm tắt của con người.",
        font(26),
        INK,
        1470,
        9,
    )
    save(image, "chapter2_pipeline.png")


def preprocessing_figure() -> None:
    image = Image.new("RGB", (1800, 980), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "Từ văn bản thô đến các từ máy có thể xử lý", "Một ví dụ tiếng Việt trước và sau từng công đoạn")

    stages = [
        (
            "DỮ LIỆU THÔ",
            '<p>  Bệnh viện A khai trương khu cấp cứu mới!!!  Xem tại https://bv-a.vn  </p>',
            LIGHT_RED,
            RED,
        ),
        (
            "SAU KHI LÀM SẠCH",
            "Bệnh viện A khai trương khu cấp cứu mới!",
            LIGHT_GOLD,
            GOLD,
        ),
        (
            "SAU KHI TÁCH TỪ",
            "bệnh_viện / A / khai_trương / khu / cấp_cứu / mới",
            LIGHT_TEAL,
            TEAL,
        ),
    ]
    y_positions = [185, 400, 615]
    for i, ((label, body, fill, accent), y) in enumerate(zip(stages, y_positions)):
        rounded_box(draw, (130, y, 1670, y + 155), fill, accent, 4, 12)
        draw.text((170, y + 24), label, font=font(28, True), fill=accent)
        draw_wrapped(draw, (170, y + 75), body, font(29), INK, 1440, 10)
        if i < len(stages) - 1:
            arrow(draw, (900, y + 164), (900, y + 205), NAVY, 7)

    rounded_box(draw, (180, 825, 1620, 930), LIGHT_BLUE, BLUE, 3, 10)
    draw.text((220, 850), "Nhãn biên minh họa:", font=font(25, True), fill=BLUE)
    draw.text(
        (520, 850),
        "Bệnh(B)  viện(I)   |   cấp(B)  cứu(I)   →   bệnh_viện, cấp_cứu",
        font=font(25),
        fill=INK,
    )
    save(image, "chapter2_preprocessing.png")


def representation_figure() -> None:
    image = Image.new("RGB", (1800, 1030), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "Bốn cách biến chữ thành số", "Càng về sau, biểu diễn càng giữ được nhiều thông tin ngữ cảnh")

    cards = [
        (
            "BoW",
            "Đếm từ",
            "cấp_cứu: 2\nbệnh_viện: 1",
            "Không biết trật tự từ",
            LIGHT_GRAY,
            NAVY,
        ),
        (
            "TF-IDF",
            "Đếm có trọng số",
            "Từ hiếm trong toàn tập\nđược ưu tiên hơn",
            "Vẫn khó hiểu từ đồng nghĩa",
            LIGHT_GOLD,
            GOLD,
        ),
        (
            "Word2Vec",
            "Vector nghĩa tĩnh",
            "bác_sĩ ↔ y_tá\nnằm gần nhau",
            "Một từ chỉ có một vector",
            LIGHT_BLUE,
            BLUE,
        ),
        (
            "PhoBERT",
            "Vector theo ngữ cảnh",
            "đường phố ≠ đường cát\n≠ đường lối",
            "Hiểu tốt hơn nhưng tốn tài nguyên",
            LIGHT_TEAL,
            TEAL,
        ),
    ]
    start_x, y1, card_w, card_h, gap = 60, 205, 385, 620, 45
    for i, (name, tagline, example, limitation, fill, accent) in enumerate(cards):
        x1 = start_x + i * (card_w + gap)
        rounded_box(draw, (x1, y1, x1 + card_w, y1 + card_h), fill, accent, 4, 14)
        draw.text((x1 + 28, y1 + 28), name, font=font(38, True), fill=accent)
        draw.text((x1 + 28, y1 + 88), tagline, font=font(27, True), fill=INK)
        draw.line((x1 + 28, y1 + 145, x1 + card_w - 28, y1 + 145), fill=accent, width=3)
        draw.text((x1 + 28, y1 + 180), "Ví dụ", font=font(24, True), fill=MUTED)
        yy = y1 + 225
        for line in example.split("\n"):
            yy = draw_wrapped(draw, (x1 + 28, yy), line, font(26), INK, card_w - 56, 9) + 8
        draw.text((x1 + 28, y1 + 430), "Điểm cần nhớ", font=font(24, True), fill=MUTED)
        draw_wrapped(draw, (x1 + 28, y1 + 477), limitation, font(25), INK, card_w - 56, 9)

    arrow(draw, (235, 885), (1550, 885), TEAL, 8)
    draw.text((645, 910), "Mức độ giữ ngữ cảnh tăng dần", font=font(28, True), fill=TEAL)
    save(image, "chapter2_representation.png")


def textrank_figure() -> None:
    image = Image.new("RGB", (1800, 1080), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "TextRank: câu quan trọng nằm ở vị trí kết nối tốt", "Ví dụ gồm 5 câu; đường nối dày biểu thị mức tương đồng cao")

    rounded_box(draw, (65, 180, 590, 950), LIGHT_GRAY, BORDER, 3, 12)
    draw.text((95, 210), "VĂN BẢN ĐẦU VÀO", font=font(29, True), fill=NAVY)
    sentences = [
        ("S1", "Bệnh viện A khai trương khu cấp cứu mới."),
        ("S2", "Khu cấp cứu có 30 giường, hoạt động 24/7."),
        ("S3", "Bệnh viện bổ sung 12 bác sĩ và 20 điều dưỡng."),
        ("S4", "Khu vực chờ được trang trí màu xanh."),
        ("S5", "Cơ sở mới dự kiến giảm thời gian chờ."),
    ]
    y = 275
    for sid, sentence in sentences:
        draw.text((95, y), sid, font=font(25, True), fill=TEAL if sid in {"S1", "S2", "S5"} else MUTED)
        y = draw_wrapped(draw, (155, y), sentence, font(23), INK, 390, 8) + 28

    draw.text((705, 205), "ĐỒ THỊ TƯƠNG ĐỒNG", font=font(29, True), fill=NAVY)
    nodes = {
        "S1": (940, 350),
        "S2": (1260, 370),
        "S3": (1220, 690),
        "S4": (790, 760),
        "S5": (900, 610),
    }
    edges = [
        ("S1", "S2", 12),
        ("S1", "S5", 11),
        ("S2", "S5", 10),
        ("S2", "S3", 7),
        ("S3", "S5", 5),
        ("S4", "S5", 2),
    ]
    for a, b, thickness in edges:
        draw.line((nodes[a], nodes[b]), fill="#9AA8B5", width=thickness)
    scores = {"S1": 0.27, "S2": 0.25, "S3": 0.16, "S4": 0.08, "S5": 0.24}
    for sid, (x, y) in nodes.items():
        radius = 68 if sid in {"S1", "S2", "S5"} else 54
        fill = TEAL if sid in {"S1", "S2", "S5"} else BLUE if sid == "S3" else "#A7B0B8"
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill, outline=WHITE, width=5)
        bbox = draw.textbbox((0, 0), sid, font=font(30, True))
        draw.text((x - (bbox[2] - bbox[0]) / 2, y - 34), sid, font=font(30, True), fill=WHITE)
        score_text = f"{scores[sid]:.2f}"
        score_bbox = draw.textbbox((0, 0), score_text, font=font(22))
        draw.text((x - (score_bbox[2] - score_bbox[0]) / 2, y + 4), score_text, font=font(22), fill=WHITE)

    rounded_box(draw, (1375, 180, 1735, 950), LIGHT_TEAL, TEAL, 4, 12)
    draw.text((1410, 215), "XẾP HẠNG", font=font(29, True), fill=TEAL)
    rankings = [("1", "S1", "0.27"), ("2", "S2", "0.25"), ("3", "S5", "0.24"), ("4", "S3", "0.16"), ("5", "S4", "0.08")]
    y = 300
    for rank, sid, score in rankings:
        fill = TEAL if int(rank) <= 2 else WHITE
        text_fill = WHITE if int(rank) <= 2 else INK
        rounded_box(draw, (1410, y, 1700, y + 78), fill, TEAL, 2, 9)
        draw.text((1432, y + 19), rank, font=font(25, True), fill=text_fill)
        draw.text((1490, y + 19), sid, font=font(25, True), fill=text_fill)
        draw.text((1600, y + 19), score, font=font(25), fill=text_fill)
        y += 100
    draw_wrapped(draw, (1410, 820), "Giữ 30% ≈ 2 câu; sau đó đưa câu về thứ tự gốc.", font(22), INK, 290, 7)
    save(image, "chapter2_textrank.png")


def clustering_figure() -> None:
    image = Image.new("RGB", (1800, 1080), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "PhoBERT + phân cụm: gom các câu cùng chủ đề", "Mỗi chấm là một câu đã được đổi thành vector 768 chiều; hình chỉ chiếu xuống 2 chiều để minh họa")

    panels = [
        (80, 200, 850, 890, "K-MEANS", "Chia mọi câu vào đúng K cụm", BLUE, LIGHT_BLUE),
        (950, 200, 1720, 890, "DBSCAN", "Tạo cụm theo mật độ và có thể loại nhiễu", TEAL, LIGHT_TEAL),
    ]
    for x1, y1, x2, y2, heading, subtitle, accent, fill in panels:
        rounded_box(draw, (x1, y1, x2, y2), fill, accent, 4, 14)
        draw.text((x1 + 35, y1 + 30), heading, font=font(34, True), fill=accent)
        draw.text((x1 + 35, y1 + 84), subtitle, font=font(24), fill=INK)
        draw.line((x1 + 40, y2 - 90, x2 - 40, y2 - 90), fill="#8795A1", width=3)
        draw.line((x1 + 70, y1 + 160, x1 + 70, y2 - 60), fill="#8795A1", width=3)

    k_points = [
        (230, 405, BLUE), (285, 355, BLUE), (335, 425, BLUE), (260, 480, BLUE),
        (560, 405, GOLD), (620, 350, GOLD), (670, 430, GOLD), (600, 485, GOLD),
        (390, 650, PURPLE), (455, 600, PURPLE), (520, 670, PURPLE), (450, 735, PURPLE),
    ]
    for x, y, color in k_points:
        draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=color, outline=WHITE, width=3)
    for x, y, color in [(280, 415, BLUE), (615, 420, GOLD), (455, 660, PURPLE)]:
        draw.ellipse((x - 25, y - 25, x + 25, y + 25), outline=INK, width=6)
        draw.line((x - 18, y, x + 18, y), fill=INK, width=4)
        draw.line((x, y - 18, x, y + 18), fill=INK, width=4)
    draw.text((145, 815), "Chọn trước K; lấy câu gần tâm mỗi cụm.", font=font(23), fill=INK)

    d_points = [
        (1110, 395, TEAL), (1160, 350, TEAL), (1210, 420, TEAL), (1150, 470, TEAL),
        (1440, 405, ORANGE), (1500, 355, ORANGE), (1555, 430, ORANGE), (1490, 485, ORANGE),
    ]
    for x, y, color in d_points:
        draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=color, outline=WHITE, width=3)
    draw.ellipse((1110 - 105, 410 - 105, 1110 + 170, 410 + 135), outline=TEAL, width=4)
    draw.ellipse((1485 - 115, 415 - 110, 1485 + 125, 415 + 135), outline=ORANGE, width=4)
    for x, y in [(1280, 690), (1620, 690), (1035, 650)]:
        draw.line((x - 15, y - 15, x + 15, y + 15), fill=RED, width=6)
        draw.line((x - 15, y + 15, x + 15, y - 15), fill=RED, width=6)
    draw.text((1015, 815), "Câu thưa thớt có thể mang nhãn -1 (nhiễu).", font=font(23), fill=INK)

    rounded_box(draw, (240, 935, 1560, 1025), LIGHT_GOLD, GOLD, 3, 10)
    draw.text((285, 958), "Điểm mấu chốt:", font=font(25, True), fill=GOLD)
    draw.text((540, 958), "K-Means luôn gán cụm; DBSCAN phụ thuộc mạnh vào eps và MinPts.", font=font(25), fill=INK)
    save(image, "chapter2_clustering.png")


def vit5_figure() -> None:
    image = Image.new("RGB", (1800, 1070), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "ViT5: đọc toàn bài và viết lại bản tóm tắt", "Khác với TextRank, đầu ra có thể là câu mới không xuất hiện nguyên văn trong nguồn")

    rounded_box(draw, (70, 190, 470, 440), LIGHT_GRAY, BORDER, 3, 12)
    draw.text((105, 220), "VĂN BẢN GỐC", font=font(28, True), fill=NAVY)
    draw_wrapped(
        draw,
        (105, 275),
        "Bệnh viện A mở khu cấp cứu 30 giường, hoạt động 24/7 và bổ sung nhân sự.",
        font(24),
        INK,
        330,
        9,
    )

    rounded_box(draw, (600, 190, 1010, 440), LIGHT_BLUE, BLUE, 4, 12)
    draw.text((675, 220), "ENCODER", font=font(32, True), fill=BLUE)
    draw_wrapped(draw, (640, 285), "Mã hóa quan hệ giữa mọi token bằng self-attention", font(25), INK, 330, 9, "center")

    rounded_box(draw, (1140, 190, 1570, 440), LIGHT_TEAL, TEAL, 4, 12)
    draw.text((1220, 220), "DECODER", font=font(32, True), fill=TEAL)
    draw_wrapped(draw, (1180, 285), "Sinh lần lượt từng token của bản tóm tắt", font(25), INK, 350, 9, "center")
    arrow(draw, (485, 315), (585, 315), NAVY, 8)
    arrow(draw, (1025, 315), (1125, 315), NAVY, 8)

    rounded_box(draw, (130, 510, 1670, 960), "#FAFBFC", BORDER, 3, 12)
    draw.text((175, 545), "BEAM SEARCH (minh họa Beam Width = 4)", font=font(30, True), fill=PURPLE)
    draw.text((175, 600), "Mô hình giữ đồng thời bốn hướng viết tốt nhất thay vì chốt ngay một từ.", font=font(24), fill=INK)

    root = (300, 720)
    draw.ellipse((root[0] - 62, root[1] - 35, root[0] + 62, root[1] + 35), fill=NAVY)
    draw.text((250, 701), "Bệnh viện", font=font(22, True), fill=WHITE)
    candidates = [
        ("mở", "0.42", 600, 660, TEAL),
        ("đưa", "0.31", 600, 755, BLUE),
        ("khai trương", "0.18", 600, 850, GOLD),
        ("vận hành", "0.09", 600, 930, RED),
    ]
    for word, prob, x, y, color in candidates:
        arrow(draw, (365, 720), (x - 85, y), color, 5)
        rounded_box(draw, (x - 75, y - 36, x + 220, y + 36), WHITE, color, 4, 10)
        word_font = font(19, True) if word == "khai trương" else font(21, True)
        draw.text((x - 52, y - 24), word, font=word_font, fill=color)
        draw.text((x + 145, y - 23), prob, font=font(20), fill=MUTED)

    rounded_box(draw, (950, 670, 1575, 885), LIGHT_TEAL, TEAL, 4, 12)
    draw.text((995, 705), "ĐẦU RA ĐƯỢC CHỌN", font=font(27, True), fill=TEAL)
    draw_wrapped(
        draw,
        (995, 760),
        "Bệnh viện A đưa vào hoạt động khu cấp cứu 30 giường, phục vụ liên tục 24/7.",
        font(24),
        INK,
        530,
        9,
    )
    save(image, "chapter2_vit5.png")


def rouge_figure() -> None:
    image = Image.new("RGB", (1800, 1000), WHITE)
    draw = ImageDraw.Draw(image)
    title(draw, "ROUGE: đếm phần nội dung trùng với bản chuẩn", "Các token màu xanh xuất hiện ở cả bản chuẩn và bản máy")

    draw.text((90, 200), "BẢN CHUẨN", font=font(28, True), fill=NAVY)
    ref = [("bệnh_viện", True), ("mở", False), ("khu", True), ("cấp_cứu", True), ("mới", False)]
    cand = [("bệnh_viện", True), ("khai_trương", False), ("khu", True), ("cấp_cứu", True)]

    def tokens(y: int, values: list[tuple[str, bool]]) -> None:
        x = 330
        for token, matched in values:
            token_width = draw.textbbox((0, 0), token, font=font(25, True))[2] + 46
            fill = LIGHT_TEAL if matched else LIGHT_RED
            outline = TEAL if matched else RED
            rounded_box(draw, (x, y, x + token_width, y + 70), fill, outline, 3, 9)
            draw.text((x + 22, y + 18), token, font=font(25, True), fill=outline)
            x += token_width + 20

    tokens(175, ref)
    draw.text((90, 325), "BẢN MÁY", font=font(28, True), fill=NAVY)
    tokens(300, cand)

    rounded_box(draw, (90, 445, 830, 885), LIGHT_BLUE, BLUE, 4, 12)
    draw.text((130, 480), "ROUGE-1", font=font(34, True), fill=BLUE)
    draw.text((130, 545), "Số token trùng = 3", font=font(27), fill=INK)
    draw.text((130, 605), "Recall = 3 / 5 = 0.60", font=font(27), fill=INK)
    draw.text((130, 665), "Precision = 3 / 4 = 0.75", font=font(27), fill=INK)
    draw.text((130, 725), "F1 = 0.67", font=font(30, True), fill=BLUE)
    draw_wrapped(draw, (130, 790), "Bản máy khớp 60% số token trong bản chuẩn.", font(24), MUTED, 640, 8)

    rounded_box(draw, (970, 445, 1710, 885), LIGHT_GOLD, GOLD, 4, 12)
    draw.text((1010, 480), "ROUGE-2 & ROUGE-L", font=font(34, True), fill=GOLD)
    draw.text((1010, 545), "Bigram trùng: khu → cấp_cứu", font=font(26), fill=INK)
    draw.text((1010, 605), "ROUGE-2 F1 ≈ 0.29", font=font(28, True), fill=GOLD)
    draw.text((1010, 675), "Chuỗi chung dài nhất:", font=font(26), fill=INK)
    draw.text((1010, 725), "bệnh_viện → khu → cấp_cứu", font=font(25, True), fill=TEAL)
    draw.text((1010, 785), "ROUGE-L F1 = 0.67", font=font(28, True), fill=GOLD)

    draw.text((255, 925), "ROUGE đo mức trùng lặp; không tự phát hiện câu sai sự thật hoặc câu khó đọc.", font=font(27, True), fill=RED)
    save(image, "chapter2_rouge.png")


def main() -> None:
    chapter1_taxonomy_figure()
    chapter1_timeline_figure()
    pipeline_figure()
    preprocessing_figure()
    representation_figure()
    textrank_figure()
    clustering_figure()
    vit5_figure()
    rouge_figure()
    for path in sorted(OUT_DIR.glob("*.png")):
        print(path)


if __name__ == "__main__":
    main()
