# データのバックアップ（GitHub設定）

> このマニュアルでやること：このフォルダのデータをGitHubというクラウドに自動で同期させる設定。  
> PCが壊れても、間違ってファイルを消しても、いつでも復元できるようになります。

**所要時間：20〜30分（初回のみ）**  
**難易度：★☆☆☆☆（エンジニア知識は一切不要）**

---

## そもそも何をするのか

Obsidian Git というプラグインが、10分おきに「このフォルダの変更を記録 → GitHubに送信」を自動でやってくれます。

```
あなたのPC → （10分ごとに自動送信）→ GitHub（クラウド）
```

一度設定してしまえば、あとは何もしなくていいです。

---

## 準備するもの

- [ ] GitHubのアカウント（持っていない場合は最初に作る）
- [ ] インターネット接続

---

## STEP 1：GitHubアカウントを作る（すでにある人はスキップ）

1. [https://github.com](https://github.com) にアクセス
2. 「Sign up」をクリック
3. メールアドレス・パスワード・ユーザー名を設定
4. メール認証を完了する

アカウントができたらこのページを開いたままにしておいてください。

---

## STEP 2：Git をインストールする

Gitは「変更履歴を記録するソフト」です。無料です。

### Macの場合

ターミナルを開いて（Spotlight検索で「ターミナル」と入力）、以下を貼り付けてEnter：

```
xcode-select --install
```

「インストール」ボタンが出たらクリック。完了まで数分待ちます。

> すでにインストール済みの場合は「already installed」と表示されます。そのまま次に進んでOKです。

### Windowsの場合

1. [https://git-scm.com/download/win](https://git-scm.com/download/win) にアクセス
2. 「Click here to download」をクリック
3. ダウンロードされたインストーラーを実行
4. 途中の選択肢はすべてデフォルト（そのまま「Next」を押し続ける）でOK
5. 「Finish」で完了

インストール後、スタートメニューに「Git Bash」が追加されます。これ以降「ターミナル」と書いてある手順は、Windowsの場合はこの「Git Bash」を使ってください。

---

## STEP 3：GitHub CLI をインストールする

GitHub CLI は「ターミナルからGitHubを操作するツール」です。

### Macの場合

ターミナルで以下を実行：

```
brew install gh
```

> Homebrewが入っていない場合は先に [https://brew.sh](https://brew.sh) からインストールしてください（ページの指示に従うだけ）。

### Windowsの場合

1. [https://cli.github.com](https://cli.github.com) にアクセス
2. 「Download for Windows」をクリック
3. ダウンロードされたインストーラーを実行
4. デフォルト設定のまま「Next」→「Install」→「Finish」

---

## STEP 4：GitHubにログインする

**Mac・Windows共通（Git BashまたはターミナルでOK）**

以下を実行：

```
gh auth login
```

いくつか質問されます：

| 質問 | 選ぶもの |
|-----|---------|
| Where do you use GitHub? | `GitHub.com` |
| What is your preferred protocol for Git operations? | `HTTPS` |
| Authenticate Git with your GitHub credentials? | `Y` を押してEnter |
| How would you like to authenticate GitHub CLI? | `Login with a web browser` |

「Login with a web browser」を選ぶと：
1. ターミナルに8桁のコード（例：`XXXX-XXXX`）が表示される
2. ブラウザが開く
3. コードを入力してGitHubにログイン
4. 「Authorize」をクリック

ターミナルに「Logged in as （ユーザー名）」と表示されたら成功です。

---

## STEP 5：GitHubにプライベートリポジトリを作る

「リポジトリ」＝「GitHubのクラウド上のフォルダ」のことです。

ターミナルで以下を実行（このフォルダのパスを指定します）：

**Macの場合：**

```
cd "このフォルダをここにドラッグ&ドロップ"
```

> ターミナルに `cd ` と入力した後（スペースあり）、Finderからこのフォルダ（スターターキット）をターミナルにドラッグすると自動でパスが入ります。Enterを押してください。

**Windowsの場合：**

エクスプローラーでこのフォルダを開き、アドレスバーに `git bash` と入力してEnterを押すと、そのフォルダを開いた状態でGit Bashが起動します。

---

フォルダに移動できたら、以下を実行：

```
gh repo create obsidian-vault --private --source=. --push
```

これで：
- `obsidian-vault` という名前のプライベートリポジトリがGitHub上に作成される
- 現在のデータが全部GitHubに送られる

完了すると「✓ Created repository（ユーザー名）/obsidian-vault on GitHub」と表示されます。

> **「Name already exists」と表示された場合：**  
> すでに同じ名前のリポジトリがある場合です。以下のように別の名前で作ってください：  
> `gh repo create obsidian-vault-2 --private --source=. --push`

---

## STEP 6：Obsidian Git プラグインをインストールする

Obsidianを開いてください。

1. 左下の「設定（歯車アイコン）」をクリック
2. 左メニューの「コミュニティプラグイン」をクリック
3. 「コミュニティプラグインを有効化」が出たら「有効化」をクリック
4. 「閲覧」ボタンをクリック
5. 検索欄に「Obsidian Git」と入力
6. 「Obsidian Git」が表示されたら「インストール」→「有効化」

---

## STEP 7：自動バックアップの設定をする

プラグインをインストールしたら、設定を変更します。

1. 設定画面の左メニューに「Obsidian Git」が追加されているのでクリック
2. 以下の項目を変更：

| 設定項目 | 変更後の値 |
|---------|----------|
| Vault backup interval (minutes) | `10` |
| Auto push interval (minutes) | `10` |

> 「Vault backup interval」は自動コミット（変更を記録）する間隔。  
> 「Auto push interval」はGitHubに送信する間隔。どちらも10分ごとに設定します。

3. 設定を閉じる

---

## 動作確認

設定が正しくできているか確認します。

ターミナルで以下を実行：

```
git remote -v
```

以下のように表示されれば成功です：

```
origin  https://github.com/（ユーザー名）/obsidian-vault.git (fetch)
origin  https://github.com/（ユーザー名）/obsidian-vault.git (push)
```

10分後、GitHubのページ（[https://github.com/（ユーザー名）/obsidian-vault](https://github.com)）を開くと、ファイルが反映されているはずです。

---

## 日常の使い方

**何もしなくていいです。**

Obsidianを開いている間、10分ごとに自動でバックアップが取られます。

手動でいますぐバックアップしたい場合は：

- Obsidianの左サイドバーにある「ソースコントロール」アイコン（分岐した線のマーク）をクリック
- 「Commit and push」ボタンをクリック

---

## 困ったときは

### 「git: command not found」と表示される

→ STEP 2のGitのインストールからやり直してください。Windowsの場合はGit Bashを使っているか確認してください。

### 「gh: command not found」と表示される

→ STEP 3のGitHub CLIのインストールからやり直してください。インストール後はターミナルを一度閉じて開き直してください。

### 10分待ってもGitHubに反映されない

→ Obsidianの設定でObsidian Gitプラグインが「有効」になっているか確認してください。

### エラーが出てよくわからない

→ エラーメッセージをスクリーンショットに撮って、Cursorのチャットに貼り付けて「このエラーはどういう意味ですか？」と聞いてください。

---

## バックアップから復元する方法

間違ってファイルを消した・内容を戻したいという場合：

1. [https://github.com/（ユーザー名）/obsidian-vault](https://github.com) を開く
2. 目的のファイルを探してクリック
3. 「History」をクリックすると過去のバージョン一覧が表示される
4. 戻したいバージョンをクリックして内容をコピー

または、Obsidianの「ファイルリカバリー」プラグイン（デフォルトで入っています）を使う：

1. 設定 → 「コアプラグイン」→「ファイルリカバリー」が有効になっているか確認
2. 復元したいファイルを開いた状態で、コマンドパレット（`Cmd+P` / `Ctrl+P`）を開く
3. 「ファイルリカバリー：スナップショットを表示」で過去のバージョン一覧が表示される
