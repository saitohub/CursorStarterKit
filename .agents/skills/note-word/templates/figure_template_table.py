"""
figure_template_table.py — 汎用テーブル図解テンプレート（3〜5列対応）

note.com はマークダウン表を描画しないため、表データは必ず画像化する。
Claude Codeはこれをコピーして TITLE / HEADERS / ROWS を編集して実行。

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
TITLE = "ここに表タイトル"
HEADERS = ["プラットフォーム", "特徴", "向いている人"]
ROWS = [
    ["Amazon", "最大規模・信頼度高", "安定収益狙い"],
    ["メルカリ", "手軽・回転速い", "初心者向け"],
    ["ヤフオク", "オークション形式", "希少品扱い"],
    ["eBay", "海外市場・高利益", "グローバル狙い"],
    ["楽天", "ブランド力強い", "独自ブランド育成"],
]
PUNCH = "ここに1文のパンチライン"
BG_COLOR = (248, 250, 253)
HEADER_COLOR = (52, 73, 94)
ACCENT_COLOR = (52, 152, 219)
OUTPUT_PATH = "figure_table.png"
# =====================

W, H = 1280, 720
BAND_H = int(H * 0.13)

img = Image.new("RGB", (W, H), color=BG_COLOR)
draw = ImageDraw.Draw(img)

# タイトル（中央・特大）
title_font = get_japanese_font(size=58)
tb = draw.textbbox((0, 0), TITLE, font=title_font)
draw.text(((W - (tb[2] - tb[0])) // 2, 25), TITLE, font=title_font, fill=(30, 30, 30))

# 表領域
table_top = 130
table_h = H - BAND_H - table_top - 30
n_cols = len(HEADERS)
n_rows = len(ROWS)

margin = 40
total_w = W - margin * 2
col_w = total_w // n_cols

header_h = 80
row_h = (table_h - header_h) // max(n_rows, 1)

# フォント自動調整（列数・文字数に応じて）
max_text_len = max(
    [len(s) for s in HEADERS] +
    [len(c) for r in ROWS for c in r]
)
if max_text_len <= 6:
    cell_size = 38
elif max_text_len <= 9:
    cell_size = 32
elif max_text_len <= 12:
    cell_size = 28
else:
    cell_size = 24

hf = get_japanese_font(size=max(cell_size + 4, 32))
rf = get_japanese_font(size=cell_size)

def draw_centered(txt, x, y, w, h, font, fill):
    # 折返し（最大2行）
    max_chars_per_line = max(1, int(w / (cell_size * 0.7)))
    lines = []
    cur = ""
    for ch in txt:
        cur += ch
        if len(cur) >= max_chars_per_line:
            lines.append(cur); cur = ""
        if len(lines) >= 2:
            break
    if cur and len(lines) < 2:
        lines.append(cur)
    line_h = font.size + 4 if hasattr(font, 'size') else cell_size + 4
    total_h = line_h * len(lines)
    sy = y + (h - total_h) // 2
    for i, line in enumerate(lines):
        b = draw.textbbox((0, 0), line, font=font)
        sx = x + (w - (b[2] - b[0])) // 2
        draw.text((sx, sy + i * line_h), line, font=font, fill=fill)

# ヘッダー
for i, header in enumerate(HEADERS):
    x0 = margin + i * col_w
    draw.rectangle([x0, table_top, x0 + col_w, table_top + header_h], fill=HEADER_COLOR)
    draw_centered(header, x0, table_top, col_w, header_h, hf, (255, 255, 255))

# 各行
for r, row in enumerate(ROWS):
    y0 = table_top + header_h + r * row_h
    bg = (255, 255, 255) if r % 2 == 0 else (240, 245, 250)
    draw.rectangle([margin, y0, margin + col_w * n_cols, y0 + row_h], fill=bg)
    for c, cell in enumerate(row):
        x0 = margin + c * col_w
        # 1列目はアクセント色
        text_color = ACCENT_COLOR if c == 0 else (50, 50, 50)
        draw_centered(str(cell), x0, y0, col_w, row_h, rf, text_color)

# 罫線
for i in range(n_cols + 1):
    x = margin + i * col_w
    draw.line([(x, table_top), (x, table_top + header_h + row_h * n_rows)], fill=(180, 180, 180), width=1)
draw.line([(margin, table_top + header_h), (margin + col_w * n_cols, table_top + header_h)],
          fill=(180, 180, 180), width=2)

# パンチライン帯
draw.rectangle([0, H - BAND_H, W, H], fill=(255, 215, 0))
pf = get_japanese_font(size=52)
pb = draw.textbbox((0, 0), PUNCH, font=pf)
draw.text(((W - (pb[2] - pb[0])) // 2,
           H - BAND_H + (BAND_H - (pb[3] - pb[1])) // 2),
          PUNCH, font=pf, fill=(0, 0, 0))

out = Path(OUTPUT_PATH)
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, "PNG")
print(f"[OK] saved: {out.resolve()} ({out.stat().st_size // 1024} KB)")
