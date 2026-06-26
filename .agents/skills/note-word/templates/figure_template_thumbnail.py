"""
figure_template_thumbnail.py — サムネイル生成テンプレート（A型/J型対応）

Claude Code はこのファイルをコピーして以下を編集してから実行する:
  1. TITLE / SUBTITLE / PUNCH を記事内容に合わせて書き換え
  2. BG_COLOR / ACCENT_COLOR をテーマに合わせて選択
  3. OUTPUT_PATH を実際の保存先に変更（絶対パス推奨）

使い方:
  python figure_template_thumbnail.py

依存: Pillow のみ
"""

import sys
from pathlib import Path

# _fontutil への絶対パス解決（このファイルがどこに置かれても動く）
HERE = Path(__file__).resolve().parent
# 配布ルート探索（HEREから上に向かって ".codex/skills/note-word/scripts/_fontutil.py" を探す）
def find_dist_root(start: Path) -> Path:
    p = start
    for _ in range(8):
        candidate = p / "skill" / "note-word" / "scripts" / "_fontutil.py"
        if candidate.exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise FileNotFoundError("配布ルート（_fontutil.py を含む）が見つかりません")

DIST_ROOT = find_dist_root(HERE)
sys.path.insert(0, str(DIST_ROOT / "skill" / "note-word" / "scripts"))

from _fontutil import get_japanese_font  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

# ===== ここを編集 =====
TITLE = "ここにメインタイトル"
SUBTITLE = "ここに補足キャッチ"
PUNCH = "ここに1文のパンチライン"
BG_COLOR = (255, 248, 231)        # パステルクリーム
ACCENT_COLOR = (231, 76, 60)      # アクセント（赤系）
OUTPUT_PATH = "thumbnail.png"     # 絶対パス推奨
# =====================

W, H = 1280, 720
BAND_H = int(H * 0.13)

img = Image.new("RGB", (W, H), color=BG_COLOR)
draw = ImageDraw.Draw(img)

# タイトル（中央配置・極大）
title_font = get_japanese_font(size=110)
sub_font = get_japanese_font(size=44)

t_bbox = draw.textbbox((0, 0), TITLE, font=title_font)
tx = (W - (t_bbox[2] - t_bbox[0])) // 2
ty = int(H * 0.18)
draw.text((tx, ty), TITLE, font=title_font, fill=(40, 40, 40))

s_bbox = draw.textbbox((0, 0), SUBTITLE, font=sub_font)
sx = (W - (s_bbox[2] - s_bbox[0])) // 2
sy = ty + (t_bbox[3] - t_bbox[1]) + 40
draw.text((sx, sy), SUBTITLE, font=sub_font, fill=ACCENT_COLOR)

# 装飾アクセント（右下に小円）
draw.ellipse([W - 200, sy + 100, W - 80, sy + 220], fill=ACCENT_COLOR)

# パンチライン帯（黄・極太）
draw.rectangle([0, H - BAND_H, W, H], fill=(255, 215, 0))
pf = get_japanese_font(size=60)
p_bbox = draw.textbbox((0, 0), PUNCH, font=pf)
px = (W - (p_bbox[2] - p_bbox[0])) // 2
py = H - BAND_H + (BAND_H - (p_bbox[3] - p_bbox[1])) // 2
draw.text((px, py), PUNCH, font=pf, fill=(0, 0, 0))

out = Path(OUTPUT_PATH)
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, "PNG")
print(f"[OK] saved: {out.resolve()} ({out.stat().st_size // 1024} KB)")
