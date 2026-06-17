# Voice Input App 実装プラン

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ホットキーをトグルして録音し、Whisper API でテキスト変換後、カーソル位置に自動ペーストする macOS 向け Python スクリプトを作る

**Architecture:** pynput でグローバルホットキーを監視するスレッドと、tkinter のメインループを別スレッドで動かす。ホットキーをトグルするたびに録音開始・終了を切り替え、停止時に Whisper API へ送信して自動ペーストする。

**Tech Stack:** Python 3.9+, pynput, sounddevice, scipy, openai>=1.0.0, pyperclip, pyautogui, tkinter, python-dotenv

---

## ファイル構成

```
voice-input/
├── main.py           # 全ロジック（このファイルだけ起動すれば動く）
├── .env              # OPENAI_API_KEY=sk-... （Git管理外）
├── .env.example      # キーのテンプレート
├── requirements.txt  # pip install 用
├── .gitignore
├── log.txt           # 変換成功テキストの履歴（自動生成）
└── recordings/       # APIエラー時の音声保存先（自動生成）
```

---

## Task 1: プロジェクトのセットアップ

**Files:**
- Create: `voice-input/requirements.txt`
- Create: `voice-input/.env.example`
- Create: `voice-input/.gitignore`

- [ ] **Step 1: ディレクトリを作成する**

```bash
mkdir -p ~/voice-input
cd ~/voice-input
```

- [ ] **Step 2: requirements.txt を作成する**

ファイル `~/voice-input/requirements.txt` を作成し、以下を書く：

```
openai>=1.0.0
pynput
sounddevice
scipy
numpy
pyperclip
pyautogui
python-dotenv
```

- [ ] **Step 3: .env.example を作成する**

ファイル `~/voice-input/.env.example` を作成し、以下を書く：

```
OPENAI_API_KEY=sk-ここにAPIキーを貼る
HOTKEY=<cmd>+<shift>+<space>
```

- [ ] **Step 4: .gitignore を作成する**

ファイル `~/voice-input/.gitignore` を作成し、以下を書く：

```
.env
recordings/
log.txt
__pycache__/
*.pyc
```

- [ ] **Step 5: .env を作成する**

ファイル `~/voice-input/.env` を作成し、自分の OpenAI API キーを書く：

```
OPENAI_API_KEY=sk-ここに自分のAPIキーを貼る
HOTKEY=<cmd>+<shift>+<space>
```

OpenAI API キーは https://platform.openai.com/api-keys から取得する。

- [ ] **Step 6: ライブラリをインストールする**

```bash
cd ~/voice-input
pip install -r requirements.txt
```

期待する出力：最後に `Successfully installed ...` が出ればOK。エラーが出た場合は `pip3` で試す。

- [ ] **Step 7: コミット**

```bash
cd ~/voice-input
git init
git add requirements.txt .env.example .gitignore
git commit -m "feat: project setup"
```

---

## Task 2: 設定読み込みと起動チェック

**Files:**
- Create: `voice-input/main.py`

- [ ] **Step 1: main.py を新規作成する**

ファイル `~/voice-input/main.py` を作成し、以下を書く：

```python
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HOTKEY = os.getenv("HOTKEY", "<cmd>+<shift>+<space>")
SAMPLE_RATE = 16000


def check_config():
    if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
        print("エラー: .env に OPENAI_API_KEY が設定されていません。")
        print(".env.example を参考に .env ファイルを作成してください。")
        sys.exit(1)


if __name__ == "__main__":
    check_config()
    print("設定OK。起動します...")
```

- [ ] **Step 2: 動作確認する**

```bash
cd ~/voice-input
python main.py
```

期待する出力：`設定OK。起動します...`

.env の API キーが間違っている場合は：`エラー: .env に OPENAI_API_KEY が設定されていません。`

- [ ] **Step 3: コミット**

```bash
git add main.py
git commit -m "feat: config loading and startup check"
```

---

## Task 3: テキストログと音声ファイル保存

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py にログ関数を追加する**

`check_config()` 関数の下に以下を追記する：

```python
import datetime
from pathlib import Path

LOG_FILE = Path("log.txt")
RECORDINGS_DIR = Path("recordings")


def append_log(text: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")


def save_error_recording(audio_data, sample_rate: int):
    RECORDINGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = RECORDINGS_DIR / f"{timestamp}.wav"
    import scipy.io.wavfile as wavfile
    import numpy as np
    wavfile.write(str(filepath), sample_rate, audio_data.astype(np.float32))
    print(f"音声を保存しました: {filepath}")
    return filepath
```

- [ ] **Step 2: 動作確認する**

```bash
cd ~/voice-input
python -c "from main import append_log; append_log('テスト'); print(open('log.txt').read())"
```

期待する出力：`[2026-06-17 14:32:10] テスト` のような行が表示される。

- [ ] **Step 3: コミット**

```bash
git add main.py
git commit -m "feat: add logger and error recording saver"
```

---

## Task 4: 音声録音

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py に録音クラスを追加する**

`save_error_recording()` の下に以下を追記する：

```python
import numpy as np
import sounddevice as sd
import threading


class AudioRecorder:
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        self.sample_rate = sample_rate
        self._frames = []
        self._is_recording = False
        self._lock = threading.Lock()

    def _callback(self, indata, frames, time, status):
        if self._is_recording:
            with self._lock:
                self._frames.append(indata.copy())

    def start(self):
        self._frames = []
        self._is_recording = True
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self):
        self._is_recording = False
        self._stream.stop()
        self._stream.close()
        with self._lock:
            if not self._frames:
                return None
            return np.concatenate(self._frames, axis=0)
```

- [ ] **Step 2: マイク権限を確認する**

```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

期待する出力：マイクデバイスの一覧が表示される。エラーが出た場合は「システム環境設定 → プライバシーとセキュリティ → マイク」で Python にマイクへのアクセスを許可する。

- [ ] **Step 3: 録音の動作確認をする**

```bash
python -c "
import time
from main import AudioRecorder
r = AudioRecorder()
r.start()
print('3秒録音します...')
time.sleep(3)
data = r.stop()
print(f'録音完了: {len(data)} フレーム取得')
"
```

期待する出力：`録音完了: 48000 フレーム取得`（3秒 × 16000Hz = 48000）

- [ ] **Step 4: コミット**

```bash
git add main.py
git commit -m "feat: add audio recorder"
```

---

## Task 5: Whisper API 文字起こし

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py に Whisper クライアントを追加する**

`AudioRecorder` クラスの下に以下を追記する：

```python
import io
import scipy.io.wavfile as wavfile
from openai import OpenAI

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe(audio_data: np.ndarray, sample_rate: int = SAMPLE_RATE) -> str:
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, audio_data.astype(np.float32))
    buffer.seek(0)
    buffer.name = "recording.wav"

    response = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=buffer,
        language="ja",
    )
    return response.text.strip()
```

- [ ] **Step 2: 動作確認する（録音して文字起こしまで）**

```bash
python -c "
import time
import numpy as np
from main import AudioRecorder, transcribe
r = AudioRecorder()
r.start()
print('「こんにちは、テストです」と喋ってください（3秒）')
time.sleep(3)
data = r.stop()
text = transcribe(data)
print(f'文字起こし結果: {text}')
"
```

期待する出力：喋った内容がテキストで表示される。

- [ ] **Step 3: コミット**

```bash
git add main.py
git commit -m "feat: add whisper transcription"
```

---

## Task 6: 自動ペースト

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py に自動ペースト関数を追加する**

`transcribe()` 関数の下に以下を追記する：

```python
import time
import pyperclip
import pyautogui

pyautogui.FAILSAFE = False


def paste_text(text: str):
    pyperclip.copy(text)
    time.sleep(0.15)
    pyautogui.hotkey("command", "v")
```

- [ ] **Step 2: アクセシビリティ権限を確認する**

「システム環境設定 → プライバシーとセキュリティ → アクセシビリティ」で Terminal（またはスクリプトを動かすアプリ）にアクセス権を与える。これがないと `pyautogui` がキー操作を実行できない。

- [ ] **Step 3: 動作確認する**

テキストエディタ（メモ帳、VSCode など）を開いてカーソルを置いた状態で：

```bash
python -c "from main import paste_text; paste_text('ペーストのテスト')"
```

期待する動作：エディタに「ペーストのテスト」と入力される。

- [ ] **Step 4: コミット**

```bash
git add main.py
git commit -m "feat: add auto-paste"
```

---

## Task 7: フローティングインジケーターウィンドウ

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py にインジケータークラスを追加する**

`paste_text()` の下に以下を追記する：

```python
import tkinter as tk


class IndicatorWindow:
    def __init__(self):
        self._root = None
        self._label = None
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        time.sleep(0.3)  # tkinter の初期化待ち

    def _run(self):
        self._root = tk.Tk()
        self._root.withdraw()
        self._root.overrideredirect(True)
        self._root.attributes("-topmost", True)
        self._root.attributes("-alpha", 0.88)

        frame = tk.Frame(self._root, bg="#1a1a1a", padx=18, pady=10)
        frame.pack()
        self._label = tk.Label(
            frame,
            text="",
            font=("Helvetica", 15),
            fg="white",
            bg="#1a1a1a",
        )
        self._label.pack()

        screen_w = self._root.winfo_screenwidth()
        screen_h = self._root.winfo_screenheight()
        self._root.geometry(f"+{screen_w - 220}+{screen_h - 120}")
        self._root.mainloop()

    def _update(self, text: str):
        if self._root:
            self._label.config(text=text)
            self._root.deiconify()

    def show_recording(self):
        if self._root:
            self._root.after(0, lambda: self._update("🎙  録音中..."))

    def show_processing(self):
        if self._root:
            self._root.after(0, lambda: self._update("⏳  変換中..."))

    def hide(self):
        if self._root:
            self._root.after(0, self._root.withdraw)
```

- [ ] **Step 2: 動作確認する**

```bash
python -c "
import time
from main import IndicatorWindow
w = IndicatorWindow()
time.sleep(0.5)
w.show_recording()
time.sleep(2)
w.show_processing()
time.sleep(1)
w.hide()
time.sleep(1)
print('インジケーターテスト完了')
"
```

期待する動作：画面右下に「🎙 録音中...」→「⏳ 変換中...」が表示されて消える。

- [ ] **Step 3: コミット**

```bash
git add main.py
git commit -m "feat: add floating indicator window"
```

---

## Task 8: ホットキー制御（トグル）

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py にホットキーコントローラーを追加する**

`IndicatorWindow` クラスの下に以下を追記する：

```python
from pynput import keyboard


class HotkeyController:
    def __init__(self, hotkey_str: str, on_toggle):
        self._on_toggle = on_toggle
        self._hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(hotkey_str),
            self._on_toggle,
        )
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )

    def _on_press(self, key):
        self._hotkey.press(self._listener.canonical(key))

    def _on_release(self, key):
        self._hotkey.release(self._listener.canonical(key))

    def start(self):
        self._listener.start()

    def join(self):
        self._listener.join()
```

- [ ] **Step 2: コミット**

```bash
git add main.py
git commit -m "feat: add hotkey controller"
```

---

## Task 9: 全体を組み合わせる main() 関数

**Files:**
- Modify: `voice-input/main.py`

- [ ] **Step 1: main.py の `if __name__ == "__main__":` ブロックを置き換える**

既存の：
```python
if __name__ == "__main__":
    check_config()
    print("設定OK。起動します...")
```

を以下に置き換える：

```python
def run():
    indicator = IndicatorWindow()
    recorder = AudioRecorder(sample_rate=SAMPLE_RATE)
    is_recording = threading.Event()

    def on_toggle():
        if not is_recording.is_set():
            is_recording.set()
            recorder.start()
            indicator.show_recording()
            print("録音開始")
        else:
            is_recording.clear()
            indicator.show_processing()
            print("録音停止 → 変換中...")

            audio_data = recorder.stop()

            if audio_data is None or len(audio_data) < SAMPLE_RATE * 0.3:
                print("録音が短すぎます。スキップします。")
                indicator.hide()
                return

            def process():
                try:
                    text = transcribe(audio_data)
                    print(f"変換結果: {text}")
                    append_log(text)
                    paste_text(text)
                except Exception as e:
                    print(f"変換エラー: {e}")
                    save_error_recording(audio_data, SAMPLE_RATE)
                finally:
                    indicator.hide()

            threading.Thread(target=process, daemon=True).start()

    controller = HotkeyController(HOTKEY, on_toggle)
    controller.start()
    print(f"起動しました。ホットキー: {HOTKEY}")
    print("Ctrl+C で終了")
    try:
        controller.join()
    except KeyboardInterrupt:
        print("\n終了します。")


if __name__ == "__main__":
    check_config()
    run()
```

- [ ] **Step 2: 動作確認する**

```bash
cd ~/voice-input
python main.py
```

期待する出力：`起動しました。ホットキー: <cmd>+<shift>+<space>`

ターミナルを起動したまま、テキストエディタにカーソルを置き：
1. `Cmd+Shift+Space` を押す → 「🎙 録音中...」が出る
2. 喋る
3. もう一度 `Cmd+Shift+Space` を押す → 「⏳ 変換中...」→ テキストが自動ペーストされる

- [ ] **Step 3: コミット**

```bash
git add main.py
git commit -m "feat: wire all components in main()"
```

---

## Task 10: ログイン時に自動起動する設定（オプション）

毎回ターミナルを開かなくても起動するようにする。

**Files:**
- Create: `~/Library/LaunchAgents/com.voice-input.plist`

- [ ] **Step 1: Python のフルパスを確認する**

```bash
which python3
```

出力（例）：`/usr/local/bin/python3` または `/opt/homebrew/bin/python3`

- [ ] **Step 2: plist ファイルを作成する**

`~/Library/LaunchAgents/com.voice-input.plist` を作成し、以下を書く（パスは Step 1 の出力に合わせる）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.voice-input</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/python3</string>
    <string>/Users/あなたのユーザー名/voice-input/main.py</string>
  </array>
  <key>WorkingDirectory</key>
  <string>/Users/あなたのユーザー名/voice-input</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/あなたのユーザー名/voice-input/stdout.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/あなたのユーザー名/voice-input/stderr.log</string>
</dict>
</plist>
```

`あなたのユーザー名` は `echo $USER` で確認する。

- [ ] **Step 3: 自動起動を登録する**

```bash
launchctl load ~/Library/LaunchAgents/com.voice-input.plist
```

- [ ] **Step 4: 動作確認する**

```bash
launchctl list | grep voice-input
```

期待する出力：`com.voice-input` が表示されればOK。

停止したい場合：
```bash
launchctl unload ~/Library/LaunchAgents/com.voice-input.plist
```

---

## 完成後のフォルダ構成

```
~/voice-input/
├── main.py
├── .env              # APIキー（Git管理外）
├── .env.example
├── requirements.txt
├── .gitignore
├── log.txt           # 自動生成される
└── recordings/       # エラー時に自動生成される
    └── 2026-06-17_14-32-10.wav
```

## コスト確認

- Whisper API: $0.006/分
- 月7時間11分（431分）使うと：約 **$2.59/月**
- 現在の Typeless $12/月 と比べて **約78%削減**
