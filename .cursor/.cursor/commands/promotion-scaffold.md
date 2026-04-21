# /promotion-scaffold — プロモーション全ファイル一括生成

promotion-config.md を読み込み、配信メール・LINE・特典のスケルトンファイルを一括生成するコマンド。

## なぜこのコマンドが必要か

分身AIラボでは17通のメール+LINE+特典で76ファイルを手作業で作った。URLを9ファイルで手動置換し、日付ズレを7ファイルで手動修正した。このコマンドで構造的にゼロにする。

## 前提条件

- `/product-create` の Phase 0〜6 が完了していること
- `05_Outputs/Products/{商品名}/promotion-config.md` が記入済みであること

## 使い方

**全ファイル生成:**
```
/promotion-scaffold
```
→ 商品フォルダを聞いて config を読み込み、全ファイルを生成

**商品を指定して生成:**
```
/promotion-scaffold 分身AIラボ
```

**一部だけ再生成:**
```
/promotion-scaffold 配信08〜13だけ再生成
```

---

## 実行フロー

### Step 1: Config の読み込みと検証

1. ユーザーに商品フォルダ名を確認（指定がなければ聞く）
2. `05_Outputs/Products/{商品名}/promotion-config.md` を読み込む
3. 必須項目の検証:

```
config を読み込みました。

【商品名】{product_name}
【コンセプト】{concept}
【セールス期間】{sales_start} 〜 {deadline}（{sales_days}日間）
【配信数】{schedule.length}通
【LINE】{channels.line ? "あり" : "なし"}
【代理店】{channels.agency ? "あり" : "なし"}

URL一覧:
- VSLページ: {urls.vsl_page}
- 申込リンク: {urls.signup_url || urls.vsl_page}
- YouTube: {urls.youtube_videos の一覧}

この内容で生成を開始しますか？
修正があれば先に config を更新してください。
```

### Step 2: テンプレート読み込みと変数置換

各配信エントリについて:

1. `.cursor/templates/promotion/` から `schedule[].template` に対応するテンプレートを読み込む
2. 以下の変数を config の値で置換:

| 変数 | 置換元 |
|------|--------|
| `{{product_name}}` | `product_name` |
| `{{concept}}` | `concept` |
| `{{target}}` | `target` |
| `{{date}}` | `schedule[].date` |
| `{{time}}` | `schedule[].time` |
| `{{num}}` | `schedule[].num` |
| `{{phase}}` | `schedule[].phase` |
| `{{title}}` | `schedule[].title` |
| `{{deadline}}` | `deadline` |
| `{{signup_url}}` | `urls.signup_url` or `urls.vsl_page` |
| `{{vsl_page}}` | `urls.vsl_page` |
| `{{video_url}}` | 該当する `urls.youtube_videos[].url` |
| `{{video_label}}` | 該当する `urls.youtube_videos[].label` |
| `{{days_left}}` | `deadline` から `schedule[].date` を引いた日数 |
| `{{prev_file}}` | 1つ前の配信ファイル名（Obsidianリンク形式） |
| `{{next_file}}` | 1つ後の配信ファイル名（Obsidianリンク形式） |
| `{{TODAY}}` | 実行日の日付 |

### Step 3: ファイル生成

以下の順序で生成:

#### 3-1. 配信メールファイル

config の `schedule` 配列の各エントリに対して:

**ファイル名**: `配信{num} ({phase}) - {title}.md`

- テンプレートから生成
- `title` が空の場合は `{phase}` をタイトルに使用
- `prev` / `next` の双方向リンクを自動設定

#### 3-2. LINE配信ファイル（config で `channels.line: true` の場合）

**ファイル名**: `LINE配信 - {通数}通構成.md`

- `.cursor/templates/promotion/line-messages.md` から生成
- `{{channel_context}}` は config の `channels.agency` に応じて「代理店追加者向け」or「友だち追加者向け」
- YouTube動画URL・VSLページURLを置換

#### 3-3. 特典スケルトン

config の `bonuses` セクションから:

```
セールス特典/
├── README.md
├── リストイン特典/
│   └── {特典名}.md
├── 事前教育間特典/
│   └── {特典名}.md
├── 早期申込特典/
│   └── {特典名}.md
└── 商品内特典/
    └── {特典名}.md
```

各特典ファイルは `.cursor/templates/promotion/bonus-template.md` から生成。

#### 3-4. 代理店プレゼント（config で `channels.agency: true` の場合）

```
代理店プレゼント/
└── {プレゼント名}.md
```

`.cursor/templates/promotion/agency-present.md` から生成。

#### 3-5. promotion-dashboard.md

`.cursor/templates/promotion/promotion-dashboard.md` から生成。
config の全配信エントリ・特典・LINE・代理店を反映したチェックリストを自動生成。

### Step 4: 生成完了レポート

```
✅ プロモーションファイルの生成が完了しました！

【生成ファイル一覧】

📧 配信メール（{N}通）
{各ファイル名の一覧}

📱 LINE配信
{ファイル名}

🎁 特典（{N}個）
{各ファイル名の一覧}

📊 ダッシュボード
promotion-dashboard.md

---

【次のステップ】

1. promotion-dashboard.md を開いて全体を確認
2. 各配信ファイルのテンプレートガイド（灰色のブロック）を読む
3. mailmagazine-creator / content-creator スキルで各ファイルを執筆
4. 執筆完了したらダッシュボードのチェックを更新

推奨の執筆順:
① 配信08（受付開始）← セールスの核なので最初に
② 配信07（VSL案内）← セールスへの橋渡し
③ 配信01〜06（事前教育）← 連番順に
④ 配信09〜13（セールス期間）← 連番順に
⑤ LINE・特典
```

---

## 部分再生成

ユーザーが「配信08〜13だけ再生成」等を指定した場合:

1. config を読み込む
2. 指定された配信番号のファイルだけ再生成する
3. **既存ファイルがある場合は上書き確認を取る**

```
以下のファイルが既に存在します:
- 配信08 (セールス) - 受付開始.md
- 配信09 (セールス) - よく聞かれる4つの質問.md
...

上書きしますか？（y / n / 個別に選択）
```

---

## テンプレートの選択ロジック

config の `schedule[].template` フィールドとテンプレートの対応:

| template値 | テンプレートファイル | 用途 |
|------------|---------------------|------|
| `email-pre-education` | `email-pre-education.md` | 事前教育・教育コラム・教育仕上げ |
| `email-video-announce` | `email-video-announce.md` | 動画案内 |
| `email-vsl-announce` | `email-vsl-announce.md` | VSL案内 |
| `email-sales-launch` | `email-sales-launch.md` | 受付開始 |
| `email-sales-education` | `email-sales-education.md` | セールス期間教育・FAQ・比較 |
| `email-sales-countdown` | `email-sales-countdown.md` | カウントダウン・ストーリー |
| `email-sales-final` | `email-sales-final.md` | 最終日 |

---

## カスタマイズ

### 配信通数の変更

config の `schedule` 配列にエントリを追加・削除するだけ。scaffold は配列の長さに応じて動的にファイルを生成する。

### テンプレートの追加

`.cursor/templates/promotion/` に新しいテンプレートファイルを追加し、config の `template` フィールドで指定すれば自動的に使用される。

### 変数の追加

テンプレートに `{{新しい変数}}` を追加し、config に対応するフィールドを追加すれば scaffold が自動で置換する。

---

## 参照ファイル

- `.cursor/templates/promotion/` - 全テンプレート格納先
- `.cursor/templates/promotion/promotion-config.md` - config テンプレート
- `.cursor/rules/product-launch-guide.mdc` - ローンチ設計ガイド
- `.cursor/commands/product-create.md` - 商品企画マスターコマンド（Phase 7 から接続）
