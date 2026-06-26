---
name: note-word
description: >
  テーマを渡すだけで note.com 用の記事ドラフト（本文 Markdown + 図解 +
  サムネイル）を生成し、Word (.docx) ファイルに1本化する簡易スキル。
  認証キー不要・完全ローカル動作。
---

# note-word — note記事 → Word化 簡易スキル

このスキルは **「記事の原稿と図解を作り、1つの Word ファイルにまとめる」** ところまでが責任範囲です。
note.com への自動投稿は行いません（手動コピペで運用）。

---

## 実行フロー（必ずこの順で行うこと）

### Phase 1. 入力整理

ユーザーから受け取る情報：
- **記事テーマ**（必須）
- ターゲット読者（任意。なければ「note読者一般」と仮置き）
- トーン（任意。指定なければ「個人体験ベース・カジュアル丁寧体」）
- 希望図解数（任意。指定なければ 2枚 + サムネ1枚）

#### 1-1. 記事スタイルの選択（必須質問・最初に1回・AskUserQuestion）

テーマを受け取ったら、**まず最初に** 記事スタイルを確認する：

```
質問: 記事のスタイルはどちらにしますか？
  [1] 有料記事向け（購買意欲を高める、感情に訴えるコピー）
  [2] 無料記事・読み物（有益情報をわかりやすく届ける通常スタイル）
  [3] その他（ここに独自の回答を入力してください）
```

選択結果を `metadata.json` の `article_style` に保存：
- `[1]` → `"sales"`
- `[2]` → `"info"`
- `[3]` → `"custom"`（自由入力テキストを `style_notes` に保存）

執筆フェーズでは **必ず `.codex/skills/note-word/references/style-guide.md` を Read** し、
選択スタイルの該当セクションを唯一の根拠として書く。

#### 1-2. 文字数の選択（必須質問・AskUserQuestion）

続けて文字数を質問：

```
質問: 記事の文字数はどのくらいにしますか？
  [1] 3,000文字（短め・スマホで読み切れる量）
  [2] 10,000文字（長文・SEOと網羅性重視）
  [3] 自由入力（数値で指定）
```

選択された文字数を `target_chars` として記録（`metadata.json` にも保存）。
許容範囲は **±10%**（例: 3000指定 → 2700〜3300字を合格、10000指定 → 9000〜11000字）。

その他の不足項目は仮置きで走り出す（Dejiina流：まず実行、後で確認）。

---

### Phase 1.5. リサーチ徹底（必須・憶測禁止）

**配布ルール**: 推測・憶測で本文を書くことは禁止。必ず一次情報を集めて
`research.md` に保存し、それを唯一の根拠として執筆する。

#### 1.5-1. リサーチ手段の選択（自動判定）

以下の優先順位で利用可能なものを使う（不足時は次へフォールバック）：

| 優先度 | 手段 | 判定 |
|--------|------|------|
| 1 | Skillツール `/research-free`（APIキー不要） | グローバルスキルに存在すれば使用 |
| 2 | Skillツール `/research`（標準） | 同上 |
| 3 | WebSearch + WebFetch（Codex 標準ツール） | 上記スキルが無い場合のフォールバック |

> 配布先の Codex 環境に `/research-free` が無い可能性もあるため、
> WebSearch+WebFetch でも同等の品質が出せるよう設計している。

#### 1.5-2. リサーチ実行

選んだ手段で以下を収集：
- 主要な事実・数値（**出典URL付き必須**）
- 具体例・ケーススタディ **3つ以上**
- 反対意見・注意点 **1つ以上**
- 関連キーワード・SEO候補語

#### 1.5-3. 保存先

`output/articles/{YYYYMMDD}_{slug}/research.md` に以下フォーマットで保存：

```markdown
# リサーチ結果: [記事テーマ]

## 1. 主要事実・数値
- [事実1] — 出典: <URL>
- [事実2] — 出典: <URL>

## 2. 具体例・ケーススタディ
### 例1: [タイトル]
...

## 3. 反対意見・注意点
...

## 4. 関連キーワード
- ...
```

#### 1.5-4. 品質ゲート（合格まで進めない）

- 出典URLが **3個以上** あるか確認
- 数値・固有名詞が **5個以上** あるか確認
- 不足ならリサーチ追加実行（最大3回）

このフェーズの成果物を **本文執筆の唯一の根拠とする**（憶測禁止）。

---

### Phase 2. 記事フォルダ作成

記事スラッグを英小文字ハイフン区切りで決定し、以下のフォルダを作成する：

```
output/articles/{YYYYMMDD}_{slug}/
├── images/
└── metadata.json
```

- `{YYYYMMDD}`: 今日の日付（例 `20260423`）
- `{slug}`: 記事テーマから生成する英小文字スラッグ（例 `Codex-note-automation`）

`metadata.json` の雛形（`templates/metadata_template.json` をコピーして使う）：

```json
{
  "title": "",
  "slug": "",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "tags": [],
  "target_reader": "",
  "tone": "",
  "article_style": "sales | info | custom",
  "style_notes": "",
  "target_chars": 3000,
  "actual_chars": 0,
  "image_mode": {
    "thumbnail": "placeholder",
    "figure_01": "placeholder",
    "figure_02": "placeholder"
  },
  "research_path": "research.md",
  "notes": ""
}
```

- `article_style` は Phase 1-1 の選択結果を保存
- `image_mode` の各値は `nanobanana` / `Codex` / `placeholder` / `manual` のいずれか
- `image_mode` は Phase 4 で画像ごとに確定する（混在可）

---

### Phase 3. 本文 Markdown 作成

#### 3-0. スタイルガイドの読み込み（必須）

執筆開始前に **必ず** 以下を実行：

1. `.codex/skills/note-word/references/style-guide.md` を Read
2. `metadata.json` の `article_style` の値（`sales` / `info` / `custom`）に応じて
   該当セクション（A / B / C）を **唯一の根拠** とする
3. `target_chars` に応じたセクション別文字数配分（style-guide.md 末尾の表）に従う

スタイルガイドに書かれていない流儀で書くことは禁止。

#### 3-1. 標準テンプレート

`output/articles/{YYYYMMDD}_{slug}/article.md` に以下の構造で執筆する。
ただし、**スタイル `sales` の場合は style-guide.md の A-2 構成（5セクション）を優先**：

```markdown
---
title: "記事タイトル"
tags: ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"]
---

（冒頭フック：個人体験・共感から始める。1〜2段落）

![サムネイル](images/thumbnail.png)

## 大見出し1

### 小見出し1-1

本文…

![図解1：〇〇のイメージ](images/figure_01.png)

### 小見出し1-2

本文…

## 大見出し2

### 小見出し2-1

本文…

![図解2：△△の流れ](images/figure_02.png)

## まとめ

（要点を3〜5個の箇条書き + 次のアクション）
```

**必ず守ること：**
- frontmatter に `title` と `tags`（3〜5個）を入れる
- H2大見出しは 3〜5個
- 各H2に H3小見出しが2個以上
- 図解プレースホルダを本文中に最低2枚
- 文末に「## まとめ」セクション
- 箇条書き・引用ブロック（`> `）・太字を適切に使用

#### 3-2. ⚠️ note.com 互換ルール（厳守）

note.com のエディタは **以下の Markdown 記法を描画しない**。配布版で確認済み：

| 記法 | note での挙動 | 対応 |
|------|--------------|------|
| **テーブル** `\| col1 \| col2 \|` | パイプ記号がそのまま生表示される | **絶対禁止 → 図解画像に変換** |
| HTML タグ `<table>` 等 | 多くは無視またはエスケープ | 禁止 |
| 脚注 `[^1]` | 反映されない | 本文に直接書く |
| 定義リスト `term : def` | 反映されない | 箇条書きに変換 |
| インライン HTML | 反映されない | 禁止 |

**特に重要なルール：表データは必ず図解化する**

- 比較表（2-3列） → `figure_template_compare.py` で画像化
- 一般的な表データ → `figure_template_table.py` で画像化
- 本文中で `| ... | ... |` の構文を **絶対に書かない**
- 表データを本文に書きそうになったら、その瞬間に図解として画像追加へ切り替える

例：
```markdown
❌ NG（noteで崩れる）
| プラットフォーム | 特徴 | 向いている人 |
| --- | --- | --- |
| Amazon | 最大規模 | 安定収益狙い |
| メルカリ | 手軽 | 初心者 |

✅ OK（画像で表現）
代表的なプラットフォームを比較しました。

![プラットフォーム比較](images/figure_compare.png)
```

詳細は `ARTICLE_CHECKLIST.md` の B7 を参照。

---

### Phase 3.5. 図解生成エンジン準備（HTML+Playwright 一本・質問しない）

> ⛔ **絶対ルール**: 自動フローでは **Gemini / nanobanana を使わない**。
> ブラウザログイン要求などユーザー作業が発生するため。
> 図解は `templates/html/*.html` を **Playwright で 1280x720 PNG にスクショする一択**。

#### 3.5-1. Playwright 存在チェック

```bash
python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('playwright') else 1)"
```

#### 3.5-2. 未インストールなら自動セットアップ（質問しない・進捗だけ表示）

exit code が非0だった場合、以下を **無音で実行**（ユーザーに聞かない）：

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

> Chromium は約200MB のダウンロード。配布物は軽量を維持し、初回実行時に自動取得する設計。
> インストール失敗時のみ Phase 4-B-FALLBACK（PIL テンプレ）に降りる。

#### 3.5-3. Chromium 動作確認

```bash
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); b.close()
print('PLAYWRIGHT_OK')
"
```

`PLAYWRIGHT_OK` 出力 → Phase 4 へ。失敗 → PIL フォールバック。

#### 3.5-4. 必ず生成する成果物（質問なし・固定）

- `images/thumbnail.png`（サムネ・必須）
- `images/figure_01.png`（図解1・必須・ステップ or ロードマップ）
- `images/figure_02.png`（図解2・必須・比較カード）
- 本文中の表は Phase 4.5 で `images/figure_table_NN.png` に自動変換

`metadata.json` の `image_mode` は固定値 `"playwright-html"` を書き込む（聞かない）。

---

### Phase 4-A. ⚠️ 自動フローでは使用しない（参考のみ）

`.codex/skills/nanobanana-deji/` フォルダは同梱しているが、**自動フローでは呼ばない**。
理由: Gemini API キー設定 / ブラウザログイン等のユーザー作業が発生し、配布版の自動化原則に反するため。

ユーザーが明示的に `nanobanana-deji を使って` と指示した場合のみ起動可。
通常は **Phase 4-B（HTML+Playwright）一本** で完結させる。

---

### Phase 4-B. 図解生成本体（HTML+Playwright 一本）

**APIキー不要・完全ローカル・質問なし**。配布フォルダ同梱の HTML テンプレを Playwright で PNG 化する。

- **本系統**: `templates/html/*.html` を編集 → `scripts/html_to_png.py` で 1280x720 PNG
- **緊急フォールバック**: Playwright が動かないときのみ `templates/figure_template_*.py`（PIL）を使用

> Phase 3.5 で Playwright のセットアップ済み。通常はこの段階で必ず動く。

#### 4-B-1. 必読資料

実行前に **必ず** Read：
1. `.codex/skills/note-word/references/figure-patterns.md` — 共通設計原則・禁止事項
2. B1ルート利用時：`.codex/skills/note-word/templates/html/*.html` の対象テンプレ
3. B2ルート利用時：`.codex/skills/note-word/templates/figure_template_*.py` の対象テンプレ

#### 4-B-2. Playwright 検出と分岐

```bash
python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('playwright') else 1)"
```

- exit 0 → **B1ルート**（HTML+Playwright）
- exit 1 → **B2ルート**（PIL テンプレ）

> 配布版に Playwright は同梱しない（200MB超になるため）。
> ユーザーが任意で `pip install -r requirements-html.txt && playwright install chromium` を実行した場合のみ B1 が使える。

#### 4-B-3. テンプレ対応表

| 画像 | B1: HTML テンプレ | B2: PIL テンプレ | 用途 |
|------|------------------|------------------|------|
| `thumbnail.png` | `templates/html/thumbnail_light.html` | `templates/figure_template_thumbnail.py` | サムネ・キャッチコピー |
| `figure_01.png` | `templates/html/steps_roadmap_light.html` | `templates/figure_template_steps.py` | ステップ・ロードマップ |
| `figure_02.png` | `templates/html/compare_card_light.html` | `templates/figure_template_compare.py` | 比較カード Before/After |
| 表データ | `templates/html/table_light.html` | `templates/figure_template_table.py` | 一覧・比較表（Phase 4.5 で自動使用） |

> **必ずサムネも生成すること**。サムネ無しはNG。

#### 4-B-4. B1ルート（HTML+Playwright）実行手順

各画像について：

```bash
# 1. HTML テンプレを記事フォルダにコピー（同じディレクトリでないと _base.css が読まれないため
#    そのまま元のテンプレ位置で編集→生成→削除のフローを使う）
cp ".codex/skills/note-word/templates/html/thumbnail_light.html" \
   ".codex/skills/note-word/templates/html/_gen_thumbnail.html"

# 2. Edit ツールで _gen_thumbnail.html の中身を記事内容に合わせて書き換える
#    - <div class="head">…</div> をタイトルに
#    - 本文要素・KPIカード・ステップなどを記事の要点に
#    - 文字数は figure-patterns.md の上限内に収める

# 3. Playwright で PNG 化
python .codex/skills/note-word/scripts/html_to_png.py \
  --html ".codex/skills/note-word/templates/html/_gen_thumbnail.html" \
  --output "output/articles/{YYYYMMDD}_{slug}/images/thumbnail.png" \
  --width 1280 --height 720 --scale 2

# 4. 確認・後始末
ls -la "output/articles/{YYYYMMDD}_{slug}/images/thumbnail.png"
rm ".codex/skills/note-word/templates/html/_gen_thumbnail.html"
```

3画像（thumbnail / figure_01 / figure_02）について繰り返す。

#### 4-B-5. B2ルート（PILテンプレ）実行手順

各画像について：

```bash
# 1. PILテンプレを記事フォルダにコピー
cp ".codex/skills/note-word/templates/figure_template_thumbnail.py" \
   "output/articles/{YYYYMMDD}_{slug}/_gen_thumbnail.py"

# 2. Edit ツールで TITLE / SUBTITLE / PUNCH / OUTPUT_PATH を書き換え
# 3. 実行
python "output/articles/{YYYYMMDD}_{slug}/_gen_thumbnail.py"
# 4. 確認
ls -la "output/articles/{YYYYMMDD}_{slug}/images/thumbnail.png"
```

スクリプトはあえて残す（後でユーザーが再調整できるように）。

#### 4-B-6. テンプレ拡張時の禁止事項

テンプレを基盤として差し替えるのは可だが、以下は **絶対に変更しない**：
- `find_dist_root()` のパス解決ロジック
- `_fontutil.get_japanese_font()` の使用（B2）
- 配色・フォントサイズ規約（figure-patterns.md 準拠）
- 出力ディレクトリ作成・保存ロジック

#### 4-B-7. 失敗時の挙動

- B1で `playwright._impl._api_types.Error` 系 → 同じ画像を B2 で再生成
- B1/B2 とも失敗 → プレースホルダにフォールバック
- フォント読込失敗 → デフォルトフォントで続行（要警告）
- PIL未インストール → `pip install -r requirements.txt` を案内して停止

---

### Phase 4-C. プレースホルダルート（image_mode=placeholder）

何もしない。`build_docx.py` が後段で自動的にプレースホルダ画像を生成する。

サムネイル設計の参考は `.codex/skills/note-word/THUMBNAIL_GUIDE.md`。

---

### Phase 4.5. テーブル自動変換（必須・全モード共通）

**理由**: note.com はマークダウン表（`| col1 | col2 |`）を描画しない。
パイプ記号がそのまま生表示されてしまう。

#### 4.5-1. 自動変換実行

選択した image_mode に関わらず **必ず実行**：

```bash
python .codex/skills/note-word/scripts/auto_convert_tables.py \
  --input "output/articles/{YYYYMMDD}_{slug}/article.md" \
  --punch "重要ポイントを一目で"
```

このスクリプトは：
1. article.md 内のマークダウン表をすべて検出
2. 各表を `images/figure_table_NN.png` として描画
   - **Playwright あり**: `templates/html/table_light.html` を流し込み高品質カラフル画像
   - **Playwright なし**: `figure_template_table.py` 同等の PIL 描画（追加依存なし）
3. 本文中の表記法を `![alt](images/figure_table_NN.png)` に置換
4. 元の article.md は `article.md.bak` としてバックアップ

#### 4.5-2. 検証

```bash
# バックアップが存在するなら変換が走っている
ls "output/articles/{YYYYMMDD}_{slug}/article.md.bak"
# 表の生記法が残っていないか確認
grep -n "^|.*|" "output/articles/{YYYYMMDD}_{slug}/article.md" || echo "[OK] 表記法残存なし"
```

#### 4.5-3. 注意

- このフェーズは **絶対にスキップしない**。表が残ったまま納品すると note 投稿時に崩れる
- ユーザー確認は不要（自動・無音）。バックアップがあるので元に戻せる

---

### Phase 4.6. ⛔ 絶対禁止ルール（最終成果物に中間ファイルを残さない）

以下は **絶対にやらない**：

| 禁止 | 理由 |
|------|------|
| HTML ファイルを最終成果物として `output/articles/` に残し「ブラウザで開いてスクショしてください」と案内 | ユーザーに余計な作業を強いる。配布版の自動化原則に反する |
| Mermaid / PlantUML / Graphviz の中間記法 | note でも Word でも描画されない |
| SVG ファイル単体出力 | note にアップ不可 |
| 表データを本文に `\| col \| col \|` のまま残す | note で生表示される（Phase 4.5 で必ず画像化） |

**画像は必ず PNG として `images/` 配下に保存** すること。
Phase 4-A/4-B/4-C/4.5 のいずれかで完結させる。

> 補足: Phase 4-B の **B1ルート（HTML+Playwright）は OK**。これはユーザーに HTML を渡すのではなく、
> Playwright が裏でスクショして PNG を `images/` に保存するため、最終成果物は PNG のみ。
> 中間 HTML（`_gen_*.html`）は生成直後に削除する（Phase 4-B-4 の手順4）。

---

### Phase 5. 品質チェック（文量チェック必須）

#### 5-1. 文量チェック（必須・自動）

専用スクリプトで本文文字数を計測し、`metadata.json` の `actual_chars` を更新＆判定：

```bash
python .codex/skills/note-word/scripts/count_chars.py \
  --input "output/articles/{YYYYMMDD}_{slug}/article.md" \
  --metadata "output/articles/{YYYYMMDD}_{slug}/metadata.json"
```

出力例:
```
actual_chars=2876
[OK] metadata.json を更新: ...
target_chars=3000  range=[2700, 3300]  verdict=OK
```

verdict が `OK` 以外なら以下を実行：

| 判定 | アクション |
|------|----------|
| 範囲内（±10%） | OK → Phase 5-2 へ |
| 不足（−10%超） | **追記必須**。リサーチ結果（`research.md`）から具体例・数値・事例を引用して各H2を厚くする |
| 超過（+10%超） | 冗長部分を整理。意味のある削減のみ（情報密度を下げない） |

修正したら 5-1 を再実行（最大3回まで）。

#### 5-2. 内容品質チェック

`ARTICLE_CHECKLIST.md` に沿って自己レビュー。
NG 項目があれば `article.md` を修正してから次のフェーズへ進む。

#### 5-3. リサーチ反映チェック

- `research.md` の出典URLが本文に **3個以上** 引用されているか
- リサーチで得た固有名詞・数値が本文に **5個以上** 含まれるか
- 不足ならリサーチ未活用とみなし追記

#### 5-4. スタイル準拠チェック（必須）

`metadata.json` の `article_style` に応じて `style-guide.md` の該当セクションを再読し、
以下を実測・判定する：

**`sales` 型の場合（style-guide.md A-1 / A-3 / A-5）**
- [ ] 疑問形語尾の比率が 20〜35% に収まっているか（実測）
- [ ] 短文（1〜15字）の比率が 42〜55% に収まっているか
- [ ] 1文1行の比率が 85% 以上か
- [ ] 恐怖→希望サイクルが本文全体で5回以上あるか
- [ ] 冒頭100字以内に具体的数値（端数含む）があるか
- [ ] P.S. セクションが存在するか
- [ ] 時間的希少性表現がクロージングにあるか
- [ ] キラーワード密度が style-guide.md A-5 の目安内か

**`info` 型の場合（style-guide.md B-1 / B-3 / B-4）**
- [ ] 冒頭が個人体験・共感から始まっているか（営業色ゼロ）
- [ ] H2大見出し3〜5個、各H2にH3小見出し2個以上
- [ ] 「## まとめ」セクションが存在するか
- [ ] 過度な煽り表現を避けているか

**`custom` 型の場合**
- [ ] `style_notes` に書かれたユーザー指示を満たしているか

不適合があれば該当箇所を書き直し（最大3回）。

---

### Phase 5.5. 画像生成検証ゲート（突破必須・無音）

**完成報告の前に必ず実行**。1枚でも欠けていたら Phase 4 を強制再実行する。

```bash
python -c "
import sys, pathlib
slug_dir = pathlib.Path(r'output/articles/{YYYYMMDD}_{slug}')
required = ['images/thumbnail.png', 'images/figure_01.png', 'images/figure_02.png']
missing = [p for p in required if not (slug_dir / p).exists() or (slug_dir / p).stat().st_size < 5000]
if missing:
    print('MISSING_IMAGES=' + ','.join(missing))
    sys.exit(1)
else:
    print('IMAGES_OK')
"
```

- `IMAGES_OK` → Phase 6 へ進む
- `MISSING_IMAGES=...` → 該当画像のみ Phase 4-B（HTML or PIL）で **再生成**。最大3周。
  - 3周しても欠ける場合のみプレースホルダで埋め、Phase 7 で「自動生成失敗：手動差し替え推奨」と明記する

> このゲートを **絶対にスキップしない**。
> 「図解は後で作りますね」「サムネは省略しました」と言って完成報告するのは禁止。

---

### Phase 6. Word 変換

Bash ツールで以下を実行：

```bash
python .codex/skills/note-word/scripts/build_docx.py \
  --input "output/articles/{YYYYMMDD}_{slug}/article.md" \
  --output "output/articles/{YYYYMMDD}_{slug}/article.docx"
```

スクリプトは以下を自動処理：
- frontmatter からタイトル・タグを取り出して Word の表紙・見出しに反映
- Markdown の H1/H2/H3/箇条書き/引用/太字/コードを Word スタイルにマッピング
- `![alt](images/xxx.png)` を検出し、画像を本文に埋め込み
- 画像ファイルが存在しない場合はプレースホルダ画像を自動生成

---

### Phase 7. 完成報告

ユーザーに以下をまとめて提示：

1. 生成された成果物のフルパス
   - `article.md`（本文・note貼付推奨）
   - `article.docx`（オフライン参照・配布用）
   - `images/` 配下の画像とその状態（自動生成 / プレースホルダ / 手動配置）
   - `research.md`（リサーチ結果・出典）
2. 記事タイトル・タグ一覧 / `actual_chars` と `target_chars` の判定結果
3. **note.com への貼り付け方（推奨手順）**
   - **方式A（推奨）**: `article.md` を直接 note エディタにコピペ → 画像は `images/` から1枚ずつドラッグ&ドロップで挿入
     （Word→noteのコピペは画像が欠落することがあるため）
   - **方式B**: `article.docx` を開いてコピペ → 画像はnote側で再挿入
4. 次のアクション候補（プレースホルダ画像の差し替え、タグ調整、本文の人間レビュー 等）

---

## 絶対にやらないこと

- 認証キーの要求（本スキルは無認証）
- 外部APIへの自動送信（note.com投稿、クラウド保存等）
- ユーザー確認なしの上書き（同名記事フォルダがあれば確認する）
- **HTML ファイルでの図解出力**（必ず PNG で `images/` に保存。中間 HTML は生成直後に削除）
- **マークダウン表（`\| ... \|`）を本文に残す**（必ず Phase 4.5 で画像化）
- **「ブラウザで開いてスクショして」「Puppeteerで変換して」等の案内**（配布版の自動化原則違反）
- **🚫 画像生成について「どうしますか？」と質問すること**
  - Phase 3.5 は質問せず自動判定・自動実行
  - Phase 4.5 も自動・無音
  - 「APIキー設定しますか？」も聞かない（無ければ HTML or PIL で粛々と生成）
- **🚫 図解・サムネ無しで完成報告すること**
  - Phase 5.5 のゲートを必ず通過させる
  - 失敗時は最大3周リトライ、それでも駄目ならプレースホルダ＋警告明記
