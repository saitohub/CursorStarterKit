# /weekly-journal コマンド

## 説明

直近1週間のジャーナルを振り返り、フィードバックと03_Knowledge候補の抽出を行う。
結果は `06_Reflections/Weekly/` に保存される。

## 実行方法

Cursorのチャットで以下のように入力する：

```text
/weekly-journal
```

## 実行条件

- 対象期間: 今日を終了日とする直近7日間
- 収集元: `04_Journals/YYYY-MM-DD.md`
- 振り返り保存先: `06_Reflections/Weekly/Reflection - YYYY-WW週.md`
- Knowledge保存先: `03_Knowledge/`

## Cursor 3 以降の運用

週次は対象量が少ないため、基本は直列で進める。
ただし、対象ファイル確認・既存Knowledge重複チェック・過去振り返りとの比較は、必要に応じて `/multitask` や async subagents で並列化してよい。

## このコマンドがやること

1. `04_Journals/` から直近7日分のファイルを読み込む
2. 週次フィードバックを生成する（成長・パターン・問いかけ）
3. 気づきをジャーナルに追記する
4. ここで一度停止し、「Step 3（Knowledgeの深掘り抽出）に進みますか？」と確認する
5. ユーザーが進行を許可した場合のみ、03_Knowledge に入れる候補（Story/Logic/Evidence/Claim）を抽出し、深掘り質問を添える
6. 深掘り質問への回答を受け取る（任意）
7. `06_Reflections/Weekly/Reflection - YYYY-WW週.md` として保存する
8. 答えてもらった候補は `03_Knowledge/` 配下にファイルを作成する

## スキルの呼び出し

以下のスキルを `timeframe: weekly` で実行する：
`.cursor/skills/journal-crystallizer/SKILL.md`

## 最重要

- 原文を要約しない
- 感情タグの派生タグを作らない
- チェックボックス番号はファイル全体の最大番号の次から採番する
- 保存・新規作成の前には必ず確認を取る
