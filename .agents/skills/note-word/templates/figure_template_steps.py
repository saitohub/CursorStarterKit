"""
figure_template_steps.py — ステップ図テンプレート（D型）

横並び3〜5ステップ。Claude Codeはこれをコピーして STEPS / TITLE / PUNCH を編集して実行。

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
TITLE = "ここにタイトル"
STEPS = [
    ("STEP 1", "テーマを決める"),
    ("STEP 2", "リサーチする"),
    ("STEP 3", "本文を書く"),
    ("STEP 4", "図解を作る"),
]
PUNCH = "ここに1文のパンチライン"
BG_COLOR = (232, 244, 253)
ACCENT_COLOR = (52, 152, 219)
OUTPUT_PATH = "figure_steps.png"
# =====================

W, H = 1280, 720
BAND_H = int(H * 0.13)

img = Image.new("RGB", (W, H), color=BG_COLOR)
draw = ImageDraw.Draw(img)

# タイトル（特大）
title_font = get_japanese_font(size=72)
draw.text((40, 25), TITLE, font=title_font, fill=(30, 30, 30))

# ステップボックス
box_top = 200
n = len(STEPS)
margin = 50
gap = 40
total_gap = gap * (n - 1)
box_w = (W - margin * 2 - total_gap) // n

step_font = get_japanese_font(size=40)
desc_font = get_japanese_font(size=38)

for i, (label, desc) in enumerate(STEPS):
    x0 = margin + i * (box_w + gap)
    x1 = x0 + box_w
    # 番号丸（大）
    cx = x0 + box_w // 2
    cy = box_top + 60
    draw.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=ACCENT_COLOR)
    nf = get_japanese_font(size=72)
    n_text = str(i + 1)
    nb = draw.textbbox((0, 0), n_text, font=nf)
    draw.text((cx - (nb[2] - nb[0]) // 2, cy - (nb[3] - nb[1]) // 2 - 8),
              n_text, font=nf, fill=(255, 255, 255))
    # ラベル
    lb = draw.textbbox((0, 0), label, font=step_font)
    draw.text((cx - (lb[2] - lb[0]) // 2, cy + 90), label, font=step_font, fill=ACCENT_COLOR)
    # 説明（折返し簡易・1行最大6文字）
    d_lines = []
    cur = ""
    max_chars = 6
    for ch in desc:
        cur += ch
        if len(cur) >= max_chars:
            d_lines.append(cur); cur = ""
    if cur: d_lines.append(cur)
    for j, line in enumerate(d_lines):
        db = draw.textbbox((0, 0), line, font=desc_font)
        draw.text((cx - (db[2] - db[0]) // 2, cy + 160 + j * 50),
                  line, font=desc_font, fill=(40, 40, 40))
    # 矢印（太く）
    if i < n - 1:
        ay = cy
        ax0 = x1 + 5
        ax1 = ax0 + gap - 10
        draw.line([(ax0, ay), (ax1, ay)], fill=(120, 120, 120), width=6)
        draw.polygon([(ax1, ay - 16), (ax1 + 18, ay), (ax1, ay + 16)], fill=(120, 120, 120))

# パンチライン帯（極太）
draw.rectangle([0, H - BAND_H, W, H], fill=(255, 215, 0))
pf = get_japanese_font(size=58)
p_bbox = draw.textbbox((0, 0), PUNCH, font=pf)
px = (W - (p_bbox[2] - p_bbox[0])) // 2
py = H - BAND_H + (BAND_H - (p_bbox[3] - p_bbox[1])) // 2
draw.text((px, py), PUNCH, font=pf, fill=(0, 0, 0))

out = Path(OUTPUT_PATH)
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, "PNG")
print(f"[OK] saved: {out.resolve()} ({out.stat().st_size // 1024} KB)")
