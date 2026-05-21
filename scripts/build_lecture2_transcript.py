#!/usr/bin/env python3
"""第2講文字起こし：キャプション行を段落化し、見出しを挿入して md に反映する。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(__file__).parent / "lecture2_raw.txt"
OUT = (
    ROOT
    / "01_Notes/AI分身ラボ/第2項 - なぜこのフォルダー構成なのか、基礎用語と設計の意図と企画について"
    / "第2講 - 文字起こし - 基礎用語とフォルダ設計と企画.md"
)

MARKERS = [
    ("まず前回の動画で全体像の話をしましたね", "## 前回とのつながり・今回の位置づけ"),
    ("軽く一つ目がAIのモデルですね", "## 基礎用語 — AIモデル"),
    ("2つ目がここが結構重要な概念で", "## 基礎用語 — API"),
    ("3つ目がマークダウン", "## 基礎用語 — マークダウン"),
    ("4つ目がボルトです", "## 基礎用語 — Vault（ボルト）"),
    ("5つ目がクレジットですね", "## 基礎用語 — クレジット"),
    ("基礎用語解説次がカーソルとオブシリア", "## カーソルとオブシディアンの役割分担"),
    ("はいで次4番ですね", "## フォルダ構成（01〜07）"),
    ("はい各フォルダについてもっと詳しく話します", "## 各フォルダの詳細"),
    ("この情報の流れが一方通行で決まっているんですよ", "## 情報の流れ（一方通行）"),
    ("ドットカーソルフォルダーイコールAIの脳みそですと", "## ドットカーソル — AIの脳みそ"),
    ("一つ目がこのルール社則とか就業規則のことです", "## ルール（社則・就業規則）"),
    ("スキルは業務の手順書です", "## スキル（業務手順書）"),
    ("スキル図とルール図の違いの整理をしたくて", "## ルールとスキルの違い"),
    ("はいでコマンズコマンドとはワンクリックの指示書のことです", "## コマンド（ワンクリック指示書）"),
    ("テンプレートはひな形の保管庫で", "## テンプレート・リファレンス"),
    ("整理するとこんな感じです", "## カーソルフォルダ全体の整理"),
    ("企画を揃えるところの本当の理由", "## 企画を揃える（命名規則）"),
    ("はいようやく終わりですよ", "## 最終まとめ"),
    ("はいでは次の動画でお会いしましょう", "## クロージング"),
]


def normalize(text: str) -> str:
    lines = text.splitlines()
    parts: list[str] = []
    buf: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            if buf:
                parts.append("".join(buf))
                buf = []
        else:
            buf.append(s)
    if buf:
        parts.append("".join(buf))
    return "\n\n".join(parts)


def add_sections(text: str) -> str:
    for needle, header in reversed(MARKERS):
        idx = text.find(needle)
        if idx >= 0:
            text = text[:idx] + "\n\n---\n\n" + header + "\n\n" + text[idx:]
    if not text.lstrip().startswith("##"):
        text = "## オープニング\n\n" + text
    return text


def main() -> None:
    raw = RAW.read_text(encoding="utf-8")
    body = add_sections(normalize(raw))
    template = OUT.read_text(encoding="utf-8")
    OUT.write_text(template.replace("<!-- TRANSCRIPT_BODY -->", body), encoding="utf-8")
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
