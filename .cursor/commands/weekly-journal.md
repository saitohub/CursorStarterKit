# /weekly-journal コマンド

## 説明
直近1週間のジャーナルを振り返り、フィードバックと03_Knowledge候補の抽出を行う。
結果は `06_Reflections/Weekly/` に保存される。

## 実行方法
Cursorのチャットで以下のように入力する：
```
/weekly-journal
```

## このコマンドがやること

1. `04_Journals/` から直近7日分のファイルを読み込む
2. 週次フィードバックを生成する（成長・パターン・問いかけ）
3. 03_Knowledge に入れる候補（Story/Logic/Evidence/Claim）を抽出し、深掘り質問を添える
4. 深掘り質問への回答を受け取る（任意）
5. `06_Reflections/Weekly/Reflection - YYYY-WW週.md` として保存する
6. 答えてもらった候補は `03_Knowledge/` 配下にファイルを自動作成する

## スキルの呼び出し

以下のスキルを `timeframe: weekly` で実行する：
`.cursor/skills/journal-crystallizer/SKILL.md`
