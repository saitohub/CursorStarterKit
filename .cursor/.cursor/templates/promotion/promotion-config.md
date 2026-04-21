---
tags:
  - promotion
  - config
status: draft
created: {{TODAY}}
updated: {{TODAY}}
---
# プロモーション設定

> **このファイルについて**
> プロモーション全体の「変数」を一元管理する設定ファイル。
> `/promotion-scaffold` コマンドがこのファイルを読み込み、全配信ファイルを自動生成する。
> 日付・URL・商品名を変更するときはここだけ書き換えればOK。

---

## 商品情報

```yaml
product_name: ""           # 例: 分身AIラボ
concept: ""                # 一文コンセプト
target: ""                 # ターゲット一文
```

## プラン

```yaml
plans:
  - name: "分身AIラボ"
    price: "税込 55,000円"
    limit: ""              # 空欄 = 人数制限なし
```

## 日程

```yaml
pre_education_start: "YYYY-MM-DD"   # 事前教育メール配信開始日
video1_date: "YYYY-MM-DD"           # 動画①配信日
video2_date: "YYYY-MM-DD"           # 動画②配信日
vsl_date: "YYYY-MM-DD"              # VSL配信日
sales_start: "YYYY-MM-DD"           # セールス開始日（受付開始メール）
deadline: "YYYY-MM-DD"              # 受付最終日（23:59締切）
sales_days: 5                       # セールス期間の日数
```

## URL

```yaml
urls:
  vsl_page: ""             # VSLページ（申し込みリンク兼用）例: https://utage-system.com/p/xxxxx
  signup_url: ""           # 申込リンク（VSLページと同じなら空欄）
  youtube_videos:
    - label: "事前教育①"
      url: ""
      private_date: ""     # 非公開にする日（空欄 = 非公開にしない）
    - label: "事前教育②"
      url: ""
      private_date: ""
    - label: "VSL動画"
      url: ""
      private_date: ""
  blog_articles:
    - label: ""            # 記事タイトル
      url: ""              # 公開URL
```

## 配信スケジュール

> 配信番号・日付・時間帯・フェーズ・仮タイトルを定義する。
> scaffold はこの表をもとに全ファイルを生成する。

```yaml
schedule:
  # --- 事前教育期間 ---
  - num: "01"
    date: ""
    time: "AM"
    phase: "事前教育"
    title: ""
    template: "email-pre-education"
  - num: "02"
    date: ""
    time: "AM"
    phase: "事前教育"
    title: ""
    template: "email-pre-education"
  - num: "03"
    date: ""
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-pre-education"
  - num: "04"
    date: ""
    time: "AM"
    phase: "動画①案内"
    title: ""
    template: "email-video-announce"
  - num: "05"
    date: ""
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-pre-education"
  - num: "06"
    date: ""
    time: "AM"
    phase: "動画②案内"
    title: ""
    template: "email-video-announce"
  # --- 企画案内 ---
  - num: "07"
    date: ""
    time: "18:00"
    phase: "VSL案内"
    title: ""
    template: "email-vsl-announce"
  - num: "07b"
    date: ""
    time: "21:00"
    phase: "教育仕上げ"
    title: ""
    template: "email-pre-education"
  # --- セールス期間 ---
  - num: "08"
    date: ""
    time: "AM"
    phase: "セールス"
    title: "受付開始"
    template: "email-sales-launch"
  - num: "09"
    date: ""
    time: "PM"
    phase: "セールス"
    title: ""
    template: "email-sales-education"
  - num: "09b"
    date: ""
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-sales-education"
  - num: "10"
    date: ""
    time: "AM"
    phase: "セールス"
    title: ""
    template: "email-sales-education"
  - num: "10b"
    date: ""
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-sales-education"
  - num: "11"
    date: ""
    time: "AM"
    phase: "セールス"
    title: ""
    template: "email-sales-countdown"
  - num: "12"
    date: ""
    time: "PM"
    phase: "セールス"
    title: ""
    template: "email-sales-countdown"
  - num: "12b"
    date: ""
    time: "AM"
    phase: "ストーリー"
    title: ""
    template: "email-sales-countdown"
  - num: "13"
    date: ""
    time: "PM"
    phase: "セールス"
    title: "本日最終日"
    template: "email-sales-final"
```

## 特典

```yaml
bonuses:
  リストイン特典:
    - name: ""
      format: ""           # チェックリスト / 電子書籍 / 診断ツール 等
  事前教育間特典:
    - name: ""
      format: ""
  早期申込特典:
    - name: ""
      format: ""
  商品内特典:
    - name: ""
      format: ""
```

## チャネル設定

```yaml
channels:
  email: true
  line: false              # LINE配信を行うか
  line_messages: 5         # LINE配信の通数
  agency: false            # 代理店チャネルを使うか
  agency_presents: 3       # 代理店プレゼントの数
```

## メモ

（このプロモーション固有の注意事項・方針をここに記述）
