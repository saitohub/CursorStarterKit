"""
figure_template_compare.py — 比較表テンプレート（F型）

2列の比較表。Claude Codeはこれをコピーして TITLE / LEFT / RIGHT / ROWS を編集して実行。

依存: Pillow のみ
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def find_dist_root(start: Path) -> Path:
    p = start
    for _ in range(8):
        if (p / "skill" / "note-word" / "scripts" / "_fontutil.py").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise FileNotFoundError("配布ルートが見つかりません")

DIST_ROOT = find_dist_root(HERE)
sys.path.insert(0, str(DIST_ROOT / "skill" / "note-word" / "scripts"))

from _fontutil import get_japanese_font  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

# ===== ここを編集 =====
TITLE = "ここに比較タイトル"
LEFT_LABEL = "従来の方法"
RIGHT_LABEL = "新しい方法"
ROWS = [
    ("速度", "遅い", "速い"),
    ("コスト", "高い", "低い"),
    ("難易度", "難しい", "簡単"),
    ("再現性", "低い", "高い"),
]
PUNCH = "ここに1文のパンチライン"
BG_COLOR = (253, 240, 240)
LEFT_COLOR = (192, 57, 43)
RIGHT_COLOR = (39, 174, 96)
OUTPUT_PATH = "figure_compare.png"
# =====================

W, H = 1280, 720
BAND_H = int(H * 0.13)

img = Image.new("RGB", (W, H), color=BG_COLOR)
draw = ImageDraw.Draw(img)

# タイトル（特大）
title_font = get_japanese_font(size=64)
tb = draw.textbbox((0, 0), TITLE, font=title_font)
draw.text(((W - (tb[2] - tb[0])) // 2, 25), TITLE, font=title_font, fill=(30, 30, 30))

# 表領域
table_top = 140
table_h = H - BAND_H - table_top - 30
col1_w = 280
col2_w = (W - col1_w - 80) // 2
col1_x = 40
col2_x = col1_x + col1_w + 10
col3_x = col2_x + col2_w + 10

header_h = 90
row_h = (table_h - header_h) // len(ROWS)

# ヘッダー
draw.rectangle([col1_x, table_top, col1_x + col1_w, table_top + header_h], fill=(200, 200, 200))
draw.rectangle([col2_x, table_top, col2_x + col2_w, table_top + header_h], fill=LEFT_COLOR)
draw.rectangle([col3_x, table_top, col3_x + col2_w, table_top + header_h], fill=RIGHT_COLOR)

hf = get_japanese_font(size=42)
def draw_centered(txt, x, y, w, h, font, fill):
    b = draw.textbbox((0, 0), txt, font=font)
    draw.text((x + (w - (b[2] - b[0])) // 2, y + (h - (b[3] - b[1])) // 2 - 4),
              txt, font=font, fill=fill)

draw_centered("項目", col1_x, table_top, col1_w, header_h, hf, (40, 40, 40))
draw_centered(LEFT_LABEL, col2_x, table_top, col2_w, header_h, hf, (255, 255, 255))
draw_centered(RIGHT_LABEL, col3_x, table_top, col2_w, header_h, hf, (255, 255, 255))

# 各行（特大）
rf = get_japanese_font(size=44)
for i, (item, left, right) in enumerate(ROWS):
    y0 = table_top + header_h + i * row_h
    bg = (250, 250, 250) if i % 2 == 0 else (240, 240, 240)
    draw.rectangle([col1_x, y0, col1_x + col1_w, y0 + row_h], fill=bg)
    draw.rectangle([col2_x, y0, col2_x + col2_w, y0 + row_h], fill=(255, 235, 235))
    draw.rectangle([col3_x, y0, col3_x + col2_w, y0 + row_h], fill=(235, 250, 240))
    draw_centered(item, col1_x, y0, col1_w, row_h, rf, (40, 40, 40))
    draw_centered(left, col2_x, y0, col2_w, row_h, rf, LEFT_COLOR)
    draw_centered(right, col3_x, y0, col2_w, row_h, rf, RIGHT_COLOR)

# パンチライン帯
draw.rectangle([0, H - BAND_H, W, H], fill=(255, 215, 0))
pf = get_japanese_font(size=44)
pb = draw.textbbox((0, 0), PUNCH, font=pf)
draw.text(((W - (pb[2] - pb[0])) // 2,
           H - BAND_H + (BAND_H - (pb[3] - pb[1])) // 2),
          PUNCH, font=pf, fill=(0, 0, 0))

out = Path(OUTPUT_PATH)
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, "PNG")
print(f"[OK] saved: {out.resolve()} ({out.stat().st_size // 1024} KB)")
