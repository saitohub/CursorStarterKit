# 振り返りファイルの構成テンプレート

journal-crystallizer スキルが 06_Reflections に保存するファイルの構成。
実際のファイルはこの構成に従ってAIが生成する。

---

## ファイルの構成

```markdown
---
date: YYYY-WW（週次）または YYYY-MM（月次）
type: weekly-reflection（または monthly-reflection）
period: YYYY-MM-DD 〜 YYYY-MM-DD
journal_count: X件
---

## 今期のあなたへ

（フェーズ2で生成した全体フィードバック・①〜④を記載）

---

## 03_Knowledge 候補

### 作成済み（X件）

（深掘り質問に答えてもらい、Knowledgeファイルを作成したものをリスト化）
- [[Story - 〇〇]]
- [[Logic - 〇〇]]

### 未作成・候補リスト（X件）

（深掘り質問に答えなかった候補をリスト化。後から手動でファイル化できる）

**📖 Story候補｜「〇〇」**
> ジャーナル YYYY-MM-DD より
> 一言：〇〇
> 深掘り質問（未回答）：「〇〇」

**🧠 Logic候補｜「〇〇」**
> ジャーナル YYYY-MM-DD より
> 一言：〇〇
> 深掘り質問（未回答）：「〇〇」

---

## メモ・補足

（ユーザーが答えてくれた深掘り回答をそのまま引用して残す）
```

---

## 保存先のルール

- 週次：`06_Reflections/Weekly/Reflection - YYYY-WW週.md`
  - 例：`Reflection - 2026-W13週.md`
- 月次：`06_Reflections/Monthly/Reflection - YYYY-MM.md`
  - 例：`Reflection - 2026-03.md`
