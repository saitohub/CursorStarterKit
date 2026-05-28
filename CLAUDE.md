# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリについて

Obsidian Vault と Python スクリプトを組み合わせた、コンテンツ制作・知識管理のための個人ワークスペース。発信者ハンドルは**サイジム**。

## スクリプトの実行方法

`scripts/` 以下に Gmail API を使った2つのスクリプトがある。実行はリポジトリルートから行う。

```bash
# イチゼミ・アカデミア・イチトレ・イチヘリのメールを収集 → ichimaiworks_list.csv
python scripts/fetch_ichimaiworks.py

# イチラボのメールを収集 → lecture_list.csv
python scripts/fetch_ichilabo.py
```

**認証ファイルの場所：** `client_secret_*.json` を `~/secrets/gmail_api/` に置く。初回実行時にブラウザ認証が走り、`~/secrets/gmail_api/token.json` が生成される。以降は自動更新。認証ファイルはVault外に保管するためGitには含まれない。

依存ライブラリ: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`

## フォルダ構成と役割

| フォルダ | 役割 |
|---------|------|
| `01_Notes/` | 一次置き場。メモ・アイデア・下書き |
| `02_Configs/Templates/` | Obsidianテンプレート（編集不要） |
| `03_Knowledge/` | 自分の知識資産（Story / Logic / Evidence / Claim） |
| `04_Journals/` | 日々のジャーナル（ファイル名：`YYYY-MM-DD.md`） |
| `05_Outputs/` | 完成コンテンツ。noteは `05_Outputs/note/` 以下に保存 |
| `06_Reflections/` | 週次・月次振り返り（Weekly / Monthly） |
| `07_Swipe/` | **他人の**事例ライブラリ（構造参考のみ） |
| `.cursor/rules/` | AIへの永続指示（my-business.mdc が中心） |
| `.cursor/commands/` | Cursorスラッシュコマンドの定義 |
| `scripts/` | Gmail APIスクリプト |

## コンテンツ制作の重要ルール

### 07_Swipe は「構造の教科書」

`07_Swipe/` の中身は**全て他人の実績・文章・事例**。コンテンツ素材は必ず `03_Knowledge/`（自分の知識資産）から引く。Swipeの数字・ストーリー・文章を自分のものとして使わない。

### note原稿の保存場所

note の記事・原稿は `05_Outputs/note/` 以下に保存する（`05_Outputs/` 直下には置かない）。ファイル名プレフィックス: `note-記事-` / `note貼り付け用-` / `note原稿-` / `note-有料-`

### ターゲット読者（健一さん）

有料note・無料noteは**田中健一さん（47歳・多忙な会社員）**に語りかける形で書く。冒頭3行で「誰向け・何が残る・開発者向けではない」を示す。煽り・月収断定・根拠なき断言は禁止。

### 文体の原則

話し言葉ベース・短文・「事実と根拠」が主軸、感情は補助。構造パターン：体験 → 気づき → 教訓 → **次の一行**。

## .cursor/rules の主要ファイル

Claude Code で作業する際も、これらのルールを同様に適用する。

- `my-business.mdc` — ビジネス設計・ターゲット・文体・禁止事項が集約。全会話に適用
- `swipe-guard.mdc` — 07_Swipe 内ファイルへのアクセス時に適用
- `file-save-confirmation.mdc` — ファイル保存前の確認ルール
- `journal-frontmatter.mdc` — ジャーナルファイルのフロントマター形式
- `read-discipline.mdc` — ファイル読み込み時の規律

## note-word スキルの使い方

`簡易型Note作成くん` スキルを使って note 記事を生成できる。スキルは Vault の `.claude/skills/note-word/` に配置済み。

### 実行方法

Claude Code の作業ディレクトリを **このVault（CursorStarterKit）** にした状態で呼び出す：

```
note-wordスキルで「〇〇」の記事を書いて
```

### 出力先ルール

生成された記事フォルダ（`YYYYMMDD_slug/`）は必ず **`05_Outputs/note/`** に保存する。
ツール側の `output/articles/` に出力された場合も、完成後に `05_Outputs/note/` へ移動すること。

### 依存ライブラリ（初回のみ）

```bash
pip install -r .claude/skills/note-word/requirements.txt
playwright install chromium
```

## 利用可能なコマンド（Cursor commands → Claude Codeでの代替）

| コマンド | 内容 |
|---------|------|
| `/weekly-journal` | 週次振り返り生成 |
| `/monthly-journal` | 月次振り返り生成 |
| `/journal-fix` | ジャーナル修正 |
| `/product-create` | 商品企画の壁打ち |
| `/promotion-scaffold` | プロモーション配信メール一括生成 |
| `/setup-target` | ターゲット設計インタビュー（my-business.mdc更新） |
| `/setup-character` | キャラクター設計インタビュー（my-business.mdc更新） |
