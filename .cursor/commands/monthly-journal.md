# /monthly-journal コマンド

## 説明
直近1ヶ月のジャーナルを振り返り、フィードバックと03_Knowledge候補の抽出を行う。
結果は `06_Reflections/Monthly/` に保存される。

## 実行方法
Cursorのチャットで以下のように入力する：
```
/monthly-journal
```

## このコマンドがやること

1. `04_Journals/` から直近30日分のファイルを読み込む
2. 月次フィードバックを生成する（成長・パターン・テーマ・次月への問いかけ）
3. 03_Knowledge に入れる候補（Story/Logic/Evidence/Claim）を抽出し、深掘り質問を添える
4. 深掘り質問への回答を受け取る（任意）
5. `06_Reflections/Monthly/Reflection - YYYY-MM.md` として保存する
6. 答えてもらった候補は `03_Knowledge/` 配下にファイルを自動作成する

## 月次ならではの視点

月次では週次に加えて以下も見る：
- 1ヶ月を通じて変化したことがあるか
- 繰り返し出てきたテーマの変化・深化
- 来月に持ち越したい問いや課題

## スキルの呼び出し

以下のスキルを `timeframe: monthly` で実行する：
`.cursor/skills/journal-crystallizer/SKILL.md`
