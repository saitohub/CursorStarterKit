---
tags:
  - promotion
  - config
status: draft
created: 2026-04-20
updated: 2026-04-20
---
# プロモーション設定

> **このファイルについて**
> `/promotion-scaffold` の動作確認用サンプルです。本番の商品ではないので、試し終わったらフォルダごと削除して構いません。

---

## 商品情報

```yaml
product_name: "動作確認サンプル"
concept: "スキャフォールドのテスト用ダミー商品です"
target: "動作確認をする自分"
```

## プラン

```yaml
plans:
  - name: "通常プラン"
    price: "税込 55,000円"
    limit: ""
  - name: "個別コンサル付きプラン"
    price: "税込 500,000円"
    limit: "5名限定・埋まり次第終了"
```

## 日程

```yaml
pre_education_start: "2026-06-02"
video1_date: "2026-06-09"
video2_date: "2026-06-11"
vsl_date: "2026-06-13"
sales_start: "2026-06-15"
deadline: "2026-06-19"
sales_days: 5
```

## URL

```yaml
urls:
  vsl_page: "https://example.com/vsl-test"
  signup_url: ""
  youtube_videos:
    - label: "事前教育①"
      url: "https://www.youtube.com/watch?v=XXXXXXXXXXX"
      private_date: ""
    - label: "事前教育②"
      url: "https://www.youtube.com/watch?v=YYYYYYYYYYY"
      private_date: ""
    - label: "VSL動画"
      url: "https://www.youtube.com/watch?v=ZZZZZZZZZZZ"
      private_date: ""
  blog_articles:
    - label: "（動作確認用）サンプル記事"
      url: "https://example.com/article-test"
```

## 配信スケジュール

```yaml
schedule:
  - num: "01"
    date: "2026-06-02"
    time: "AM"
    phase: "事前教育"
    title: "動作確認01"
    template: "email-pre-education"
  - num: "02"
    date: "2026-06-03"
    time: "AM"
    phase: "事前教育"
    title: ""
    template: "email-pre-education"
  - num: "03"
    date: "2026-06-04"
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-pre-education"
  - num: "04"
    date: "2026-06-05"
    time: "AM"
    phase: "動画①案内"
    title: ""
    template: "email-video-announce"
  - num: "05"
    date: "2026-06-06"
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-pre-education"
  - num: "06"
    date: "2026-06-07"
    time: "AM"
    phase: "動画②案内"
    title: ""
    template: "email-video-announce"
  - num: "07"
    date: "2026-06-08"
    time: "18:00"
    phase: "VSL案内"
    title: ""
    template: "email-vsl-announce"
  - num: "07b"
    date: "2026-06-08"
    time: "21:00"
    phase: "教育仕上げ"
    title: ""
    template: "email-pre-education"
  - num: "08"
    date: "2026-06-09"
    time: "AM"
    phase: "セールス"
    title: "受付開始"
    template: "email-sales-launch"
  - num: "09"
    date: "2026-06-10"
    time: "PM"
    phase: "セールス"
    title: ""
    template: "email-sales-education"
  - num: "09b"
    date: "2026-06-10"
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-sales-education"
  - num: "10"
    date: "2026-06-11"
    time: "AM"
    phase: "セールス"
    title: ""
    template: "email-sales-education"
  - num: "10b"
    date: "2026-06-11"
    time: "PM"
    phase: "教育コラム"
    title: ""
    template: "email-sales-education"
  - num: "11"
    date: "2026-06-12"
    time: "AM"
    phase: "セールス"
    title: ""
    template: "email-sales-countdown"
  - num: "12"
    date: "2026-06-13"
    time: "PM"
    phase: "セールス"
    title: ""
    template: "email-sales-countdown"
  - num: "12b"
    date: "2026-06-14"
    time: "AM"
    phase: "ストーリー"
    title: ""
    template: "email-sales-countdown"
  - num: "13"
    date: "2026-06-15"
    time: "PM"
    phase: "セールス"
    title: "本日最終日"
    template: "email-sales-final"
```

## 特典

```yaml
bonuses:
  リストイン特典:
    - name: "動作確認チェックリスト"
      format: "チェックリスト"
  事前教育間特典:
    - name: "動作確認PDF"
      format: "電子書籍"
  早期申込特典:
    - name: "動作確認ボーナス"
      format: "テンプレート"
  商品内特典:
    - name: "動作確認コミュニティ"
      format: "コミュニティ"
```

## チャネル設定

```yaml
channels:
  email: true
  line: false
  line_messages: 5
  agency: false
  agency_presents: 3
```

## メモ

動作確認用。`/promotion-scaffold 動作確認サンプル` で生成テストできます。
