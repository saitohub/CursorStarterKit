---
tags:
  - promotion
  - dashboard
  - {{product_name}}
status: active
created: {{TODAY}}
updated: {{TODAY}}
---
# {{product_name}} プロモーション ダッシュボード

> `/promotion-scaffold` が自動生成。進捗管理・URL一覧・振り返りを1ファイルに集約。

---

## 基本情報

| 項目 | 値 |
|------|-----|
| 商品名 | {{product_name}} |
| コンセプト | {{concept}} |
| セールス期間 | {{sales_start}} 〜 {{deadline}} |
| VSLページ | {{vsl_page}} |
| 申込リンク | {{signup_url}} |

---

## 配信スケジュール＆進捗

| # | 日付 | 時間 | フェーズ | タイトル | ステータス |
|---|------|------|----------|---------|-----------|
{{#each schedule}}
| {{num}} | {{date}} | {{time}} | {{phase}} | [[配信{{num}} ({{phase}}) - {{title}}]] | ⬜ 未着手 |
{{/each}}

**ステータス凡例**: ⬜ 未着手 → ✏️ 執筆中 → 📝 レビュー待ち → ✅ 完成 → 📤 配信済み

---

## URL一覧

### ページ

| 用途 | URL |
|------|-----|
| VSLページ | {{vsl_page}} |
| 申込リンク | {{signup_url}} |

### YouTube動画

| ラベル | URL | 非公開予定日 |
|--------|-----|-------------|
{{#each youtube_videos}}
| {{label}} | {{url}} | {{private_date}} |
{{/each}}

### ブログ記事

| タイトル | URL |
|---------|-----|
{{#each blog_articles}}
| {{label}} | {{url}} |
{{/each}}

---

## 特典チェックリスト

### リストイン特典
{{#each bonuses.リストイン特典}}
- [ ] {{name}}（{{format}}）
{{/each}}

### 事前教育間特典
{{#each bonuses.事前教育間特典}}
- [ ] {{name}}（{{format}}）
{{/each}}

### 早期申込特典
{{#each bonuses.早期申込特典}}
- [ ] {{name}}（{{format}}）
{{/each}}

### 商品内特典
{{#each bonuses.商品内特典}}
- [ ] {{name}}（{{format}}）
{{/each}}

---

## チャネル別チェックリスト

### LINE配信
{{#if channels.line}}
- [ ] LINE配信メッセージ（{{channels.line_messages}}通）作成
- [ ] 垢BANチェックリスト確認
- [ ] LINE公式に設定
{{else}}
（このプロモーションではLINE配信なし）
{{/if}}

### 代理店
{{#if channels.agency}}
- [ ] 代理店プレゼント（{{channels.agency_presents}}個）作成
- [ ] 代理店への案内資料準備
- [ ] 報酬設計の確定
{{else}}
（このプロモーションでは代理店チャネルなし）
{{/if}}

---

## ローンチ前チェックリスト

### コンテンツ
- [ ] 全配信メール完成
- [ ] 件名（ボレット）確定
- [ ] 全メールのCTAリンク確認
- [ ] 日付・曜日の整合性確認
- [ ] prev/next リンクの整合性確認

### インフラ
- [ ] Utage にメール設定済み
- [ ] VSLページ公開済み
- [ ] 申込フォーム動作確認
- [ ] 決済テスト完了
- [ ] YouTube動画公開済み

### LINE（該当する場合）
- [ ] LINE公式にメッセージ設定済み
- [ ] 自動応答テスト完了

---

## ポストプロモーション振り返り

> プロモーション完了後に記入する。次回の改善に直結する。

### 数字の記録

| 指標 | 値 |
|------|-----|
| リスト数（配信開始時） | |
| 開封率（平均） | |
| クリック率（平均） | |
| VSL視聴数 | |
| 申込数 | |
| 成約率 | |
| 売上（合計） | |

### 最も反応が良かったメール（TOP 3）

1. 配信__: 理由 →
2. 配信__: 理由 →
3. 配信__: 理由 →

### 改善点

1. 
2. 
3. 

### 次回への申し送り

- 
- 
- 

---

## 参照

- [[Course - {{product_name}} 企画書]]
- [[promotion-config]]
- `.cursor/rules/product-launch-guide.mdc`
