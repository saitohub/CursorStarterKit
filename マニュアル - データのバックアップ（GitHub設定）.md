# データのバックアップ（GitHub設定）

> このマニュアルでやること：このフォルダのデータをGitHubというクラウドに自動で同期させる設定。  
> PCが壊れても、間違ってファイルを消しても、いつでも復元できるようになります。
>
> **バックアップの全体方針**（3-2-1、クラウドドライブとの併用など）は [データバックアップ](マニュアル%20-%20データバックアップ.md) を参照してください。

**所要時間：20〜40分（初回のみ）**  
**難易度：★☆☆☆☆（エンジニア知識は一切不要）**

---

## 重要な前提

**10分ごとの自動バックアップは、原則として「PCが起動しており、Obsidian が動いている間」に実行されます。** 電源オフ、スリープ中、Obsidian を完全終了している間は、スケジュールされた同期は進みません。PCを閉じる前や別PCへ移る前は、手動で **Commit and push**（後述）を一度実行しておくと安全です。

---

## そもそも何をするのか

Obsidian の **Git** プラグイン（開発者名：Vinzent／旧称 Obsidian Git）が、設定した間隔で「このフォルダの変更を記録 → GitHub に送信」を自動で行います。

```
あなたのPC（Vault） → Git（履歴） → GitHub Private リポジトリ（クラウド）
```

| 項目 | 本手順での推奨 | 理由 |
| --- | --- | --- |
| GitHub の公開範囲 | **Private** | 個人メモ・業務メモ・添付が含まれる可能性があるため |
| 認証 | **HTTPS**（Git Credential Manager / macOS Keychain など） | 初心者向けの案内が多く、Obsidian Git の認証ドキュメントとも整合しやすい |
| 自動化 | **プラグインの定期 commit / push（または commit-and-sync）** | 追加サーバーや常駐スクリプトなしで運用しやすい |

一度設定してしまえば、あとは Obsidian を開いて作業するだけでバックアップが回ります。

---

## 事前準備チェック

| 確認項目 | Windows | macOS | 確認方法・備考 |
| --- | --- | --- | --- |
| GitHub アカウント | 必要 | 必要 | [github.com](https://github.com/) にサインインできること |
| Obsidian | 必要 | 必要 | バックアップしたい Vault を開けること |
| Git | 必要 | 必要 | ターミナル / Git Bash で `git --version` と打ち、バージョンが表示されること |
| Vault の保存場所 | 確認推奨 | 確認推奨 | OneDrive / iCloud Drive / Dropbox 直下だと **Git と二重同期** で競合しやすい。可能なら通常フォルダに置くか、同期ルールを決める |
| GitHub に載せたくない情報 | 確認必須 | 確認必須 | パスワード、API キー、個人番号、顧客秘密などをノートに入れていないか。入れる場合は `.gitignore` や Vault 外管理を検討 |

---

## 準備するもの

- [ ] GitHub のアカウント（なければ先に作成）
- [ ] インターネット接続

---

## 用語メモ（1分で読む）

| 用語 | 意味 |
| --- | --- |
| **commit** | 変更をローカルの履歴として記録する |
| **push** | ローカルの履歴を GitHub へ送る |
| **pull** | GitHub 側の変更をローカルへ取り込む |
| **commit-and-sync** | プラグイン上で、コミットと送受信をまとめて行う操作（表示名はバージョンで異なる場合あり） |

---

## STEP 1：GitHub アカウントを作る（すでにある人はスキップ）

1. [https://github.com](https://github.com) にアクセス
2. 「Sign up」をクリック
3. メールアドレス・パスワード・ユーザー名を設定
4. メール認証を完了する

アカウントができたらこのページを開いたままにしておいてください。

---

## STEP 2：Git をインストールする

Git は「変更履歴を記録するソフト」です。無料です。

### Mac の場合

1. ターミナルを開き（Spotlight で「ターミナル」）、次を実行：

```
git --version
```

バージョンが表示されれば **すでに導入済み**です。次の STEP に進んでください。

2. `command line developer tools` のインストールを求められた場合、または `git` が無いと言われた場合：

```
xcode-select --install
```

「インストール」をクリックし、完了まで待ちます。

> Homebrew を使っている場合は [Git 公式：macOS](https://git-scm.com/install/mac) の手順に沿って `brew install git` でも構いません。

### Windows の場合

1. [Git for Windows](https://git-scm.com/install/windows) から **x64 Setup**（ARM 版 Windows のみ ARM64）をダウンロード
2. インストーラーを実行し、基本は **既定のまま** Next（**Git Credential Manager** が有効な構成になっていることが多いです）
3. スタートメニューから **Git Bash** を開き、確認：

```
git --version
```

これ以降「ターミナル」と書いてある手順は、Windows では **Git Bash** を使ってください。

---

## STEP 3：GitHub CLI をインストールする

GitHub CLI（`gh`）は「ターミナルから GitHub を操作するツール」です。このマニュアルの **おすすめルート**では、リポジトリ作成と初回 push をまとめて行います。

### Mac の場合

ターミナルで：

```
brew install gh
```

> Homebrew が無い場合は [https://brew.sh](https://brew.sh) からインストールしてください。

### Windows の場合

1. [https://cli.github.com](https://cli.github.com) → Download for Windows
2. インストーラーを既定のまま完了

---

## STEP 4：GitHub にログインする

**Mac・Windows共通（Git Bash またはターミナル）**

```
gh auth login
```

| 質問 | 選ぶもの |
| --- | --- |
| Where do you use GitHub? | `GitHub.com` |
| What is your preferred protocol for Git operations? | `HTTPS` |
| Authenticate Git with your GitHub credentials? | `Y` |
| How would you like to authenticate GitHub CLI? | `Login with a web browser` |

ブラウザでコード認証し、「Authorize」まで完了すると、`Logged in as （ユーザー名）` のように表示されます。

---

## GitHub の HTTPS 認証（Obsidian から Push するときも使う）

GitHub の HTTPS では、**アカウントのログインパスワードをそのまま Git のパスワードとして使えません**（必要なら **Personal Access Token** をパスワードの代わりに使います）。トークンはパスワード同様に扱い、**手順書やノートに貼らない**でください。公式：[Managing personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

| OS | 推奨 | 確認・設定の例 |
| --- | --- | --- |
| Windows | Git Credential Manager | `git config --global credential.helper` で `manager` または `manager-core` が出ることが多い。未設定なら次を試す：`git config --global credential.helper manager-core`（効かない場合は `manager`） |
| macOS | Keychain | `git config --global credential.helper osxkeychain` |

Obsidian Git の認証の詳細は [Obsidian Git Documentation: Authentication](https://publish.obsidian.md/git-doc/Authentication) を参照してください。

---

## STEP 5：GitHub にプライベートリポジトリを作る（おすすめ：`gh` で一発）

「リポジトリ」＝ GitHub 上のこの Vault 用フォルダです。

ターミナルで、この **スターターキット（Vault）のフォルダ** に移動してから実行します。

**Mac：**

```
cd "このフォルダをここにドラッグ&ドロップ"
```

> `cd ` の後ろにスペースを入れ、Finder からフォルダをターミナルへドラッグするとパスが入ります。

**Windows：**

エクスプローラーでこのフォルダを開き、アドレスバーに `git bash` と入力して Enter → そのフォルダで Git Bash が開きます。

**移動できたら実行：**

```
gh repo create obsidian-vault --private --source=. --push
```

- `obsidian-vault` はリポジトリ名（好きな名前に変更可）
- 現在のデータが GitHub に送られます

> **「Name already exists」** のときは名前を変える：  
> `gh repo create obsidian-vault-2 --private --source=. --push`

### STEP 5-B（任意）：`gh` を使わず Web で空の Private リポジトリだけ作る場合

既存 Vault を後から紐づけるときは、**README / .gitignore / License を付けずに**空の Private リポジトリを作るとトラブルが少ないです（付けると初回 push で履歴が分岐することがあります）。手順は [GitHub Docs: Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) を参照。

作成後は、STEP 6 のプラグイン導入後に **Initialize a new repo**（未初期化の場合）→ **リモート origin に HTTPS URL を登録** → **初回 Commit / Push** の順で接続します。詳細は [Obsidian Git: Getting Started](https://publish.obsidian.md/git-doc/Getting+Started) を参照してください。

---

## STEP 6：Git プラグインをインストールする

Obsidian を開いてください。

> **すでに STEP 5 で `gh repo create ... --push` まで完了している場合**、Vault 内には `.git` がありリモートも登録済みです。**Git: Initialize a new repo は実行しない**でください（エラーになることがあります）。プラグインのインストールと有効化、STEP 7 の自動バックアップ設定に進めば問題ありません。

1. 左下の「設定（歯車アイコン）」
2. 「コミュニティプラグイン」→ 必要なら制限モードを解除
3. 「閲覧」→ 検索欄に `Git` または `Obsidian Git`
4. **Git**（作者：**Vinzent**）を「インストール」→「有効化」

> 検索結果は作者名 **Vinzent** で選ぶと安全です。

コマンドパレット（`Ctrl+P` / `Cmd+P`）で `Git:` と入力し、**Initialize a new repo** や **Commit-and-sync** が出れば有効化できています。

### 著者情報（初回のみ・未設定のとき）

ターミナル / Git Bash で（GitHub と同じメールや GitHub の noreply メールでも可）：

```
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

### `.gitignore` の例（不要な差分を減らす）

プラグインの **Edit .gitignore** から編集するか、Vault 直下に追記します。このキットには既に `.DS_Store` 用の設定があります。必要に応じて追加の例：

```
.trash/
.DS_Store
Thumbs.db
.obsidian/workspace.json
.obsidian/workspace-mobile.json
```

| 候補 | 目的 |
| --- | --- |
| `.trash/` | ゴミ箱をバックアップ対象から外す |
| `Thumbs.db` | Windows のサムネイルキャッシュ |
| `.obsidian/workspace.json` | 端末ごとに変わりやすいレイアウト情報（共有したい場合は入れない選択も可） |

---

## STEP 7：自動バックアップの設定をする

設定 → コミュニティプラグイン → **Git** のオプションを開きます。項目名はプラグインのバージョンで多少異なる場合があります。

| 設定項目（目安） | 推奨 | 意味 |
| --- | --- | --- |
| Vault backup interval（分） | `10` | 自動でコミットする間隔 |
| Auto push interval（分） | `10` | GitHub へ送る間隔 |
| Auto pull on startup | **オン** | 起動時にリモートの変更を取り込む（複数 PC で便利） |
| Pull before push など | **オンまたは既定** | 競合リスクを下げる |
| 自動コミットメッセージ | 例：`backup: {{date}}` | あとから履歴を追いやすくする |

> 「Vault backup interval」を `0` にすると無効になる版もあるため、**10 など正の数**になっているか確認してください。

設定後、Obsidian を一度再起動し、**10 分以上あけて** GitHub の **Commits** に新しいコミットが付くか確認します。

---

## 動作確認

### リモートが登録されているか

ターミナル / Git Bash で Vault フォルダにいて：

```
git remote -v
```

次のように `origin` と GitHub の URL が出れば成功例です。

```
origin  https://github.com/（ユーザー名）/obsidian-vault.git (fetch)
origin  https://github.com/（ユーザー名）/obsidian-vault.git (push)
```

### チェックリスト

| 確認項目 | 期待すること |
| --- | --- |
| 初回 push が成功した | GitHub のコード画面に Vault のファイルが見える |
| 約 10 分後に自動で履歴が増える | GitHub の Commits が増える（Obsidian を開いたまま） |
| 編集していないのに履歴だけ増え続ける | `.gitignore`（特に `workspace.json`）を見直す |
| 起動時にエラーが出ない | 認証・ネットワーク・リモート URL を確認 |

---

## 日常の使い方

Obsidian を開いている間、設定した間隔で自動バックアップが動きます。

**すぐ送りたいとき：** 左サイドバーのソース管理アイコンから **Commit and push**（または **Commit-and-sync**）。

**PC を閉じる前・別 PC に移る前：** 自動を待たず、手動で **Commit and push** を一度実行しておくと安心です。

---

## 困ったときは

### 「git: command not found」

→ STEP 2 をやり直す。Windows では **Git Bash** を使っているか確認。

### 「gh: command not found」

→ STEP 3 をやり直す。インストール後はターミナルを開き直す。

### Push 時に認証エラー

→ 通常パスワードではなく **PAT** を使うか、Git Credential Manager / `osxkeychain` を確認（上記「GitHub の HTTPS 認証」）。

### 「remote origin already exists」

→ プラグインまたはターミナルで `git remote -v` を確認し、URL が意図したリポジトリか確認。**Edit remotes** で修正。

### 10 分待っても GitHub に反映されない

→ Obsidian が起動しているか、プラグインが有効か、間隔が `0` になっていないか、通知に Git エラーが出ていないかを確認。

### 毎回いらない差分が大量に出る

→ `.gitignore` に `.DS_Store`、`Thumbs.db`、必要なら `.obsidian/workspace.json` を追加。

### 複数 PC で競合した

→ **Auto pull on startup** をオンにし、別 PC に行く前に手動で Commit-and-sync。

### GitHub に載せたくないファイルを push してしまった

→ ファイルを消すだけでは **履歴に残る**ことがあります。トークン類は **無効化・ローテーション** を検討し、深刻な場合は履歴の書き換えが必要になることがあります（上級者向け）。

### エラーがよく分からない

→ メッセージのスクリーンショットを Cursor に貼り、「このエラーの意味と次の一手は？」と聞いてください。

---

## バックアップから復元する方法

### パターンA：1 ファイルだけ過去に戻したい

1. GitHub 上のリポジトリでファイルを開く
2. **History** から過去版を開き、内容をコピー

または Obsidian の **ファイルリカバリー**（コアプラグイン）：

1. 設定 → コアプラグイン → ファイルリカバリーがオンか確認
2. 対象ファイルを開いた状態でコマンドパレット（`Cmd+P` / `Ctrl+P`）
3. 「ファイルリカバリー：スナップショットを表示」

### パターンB：PC を替えて Vault ごと取り戻す

1. 新しい PC に **Git** と **Obsidian** を入れ、GitHub に認証できる状態にする
2. GitHub リポジトリの **Code** から HTTPS URL（`.git` で終わるもの）をコピー
3. 保存したい場所で：

```
git clone https://github.com/ユーザー名/リポジトリ名.git
```

4. Obsidian の **Open folder as vault** で、clone したフォルダを開く

---

## 運用ルール（目安）

| テーマ | 推奨 |
| --- | --- |
| 間隔 | 基本 10 分。編集が極端に多いときは 5 分、負荷を抑えたいときは 15〜30 分 |
| 機密 | パスワード・API キー・顧客秘密はノートに書かない、または Git 対象外を徹底 |
| 添付 | 画像・PDF が膨大ならリポジトリサイズをたまに確認（大きなバイナリの頻繁な差分替えは Git に向かないこともある） |
| モバイル | Obsidian Git の公式ドキュメントでは、**モバイル版の Git 実装は不安定になり得る**旨が述べられています。本手順は **PC 版中心**の想定です |

---

## 参考リンク（公式）

| # | リンク | 内容 |
| --- | --- | --- |
| 1 | [Vinzent03/obsidian-git](https://github.com/Vinzent03/obsidian-git) | プラグイン概要・自動同期 |
| 2 | [Obsidian Git: Authentication](https://publish.obsidian.md/git-doc/Authentication) | HTTPS・Credential Manager・osxkeychain |
| 3 | [GitHub: Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) | 空リポジトリ作成・初期ファイルの注意 |
| 4 | [Git for Windows](https://git-scm.com/install/windows) | Windows 向け Git |
| 5 | [Git for macOS](https://git-scm.com/install/mac) | macOS 向け Git |
| 6 | [GitHub: Personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) | PAT の扱い |
| 7 | [Obsidian Git: Getting Started](https://publish.obsidian.md/git-doc/Getting+Started) | 初期化・空リモートへの push・clone・モバイル注意 |

---

画面や設定名は **GitHub / Git / Obsidian / プラグインのバージョン** で変わることがあります。表示が本書と違う場合は、上記公式ドキュメントで **同じ意味の項目** を選んでください。
