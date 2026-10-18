# 💖 いたずら＆デートプランナー (Zoeira & Date Matcher)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/対応言語-日本語%20%7C%20英語%20%7C%20ポルトガル語%20%7C%20スペイン語-E11D48?style=for-the-badge" alt="Languages" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <a href="README.md">English</a> | <b>日本語 (N3レベル・わかりやすい解説)</b>
</p>

---

## 📖 はじめに（どんなアプリ？）

**「いたずら＆デートプランナー」**は、友達と笑い合ったり、好きな人をスマートにデートに誘ったりできるWebアプリケーションです。

一番のポイントは、**「いいえ」を押そうとしてもボタンが逃げてしまい、最後はいたずら子猫がボタンを盗んでしまう**ことです！そのため、相手は絶対に**「はい」**しか選べなくなります🐱💨

このアプリには、大きく分けて**2つのモード**があります：

1. **😂 友達へのいたずらモード**：
   面白い質問（例：「私にご飯をおごってくれますか？」）を作って友達に送るモードです。何回「いいえ」を押そうとしたかをカウントして、最後に楽しいお祝い画面を表示します。
2. **💖 ロマンチックデートモード**：
   好きな人の名前を入れた専用リンクを作り、相手に空いている日（カレンダー）と時間帯（夜、昼、朝）を選んでもらうモードです。LINEやWhatsAppですぐにメッセージを送ることができます。

---

## ✨ 主な機能

### 🐱 1. 逃げるボタンといたずら子猫のアニメーション
- **パソコンでもスマホでもきれいに動く**：
  スマートフォンの画面をタップしたとき、イベントが重なってアニメーションが一瞬で消えてしまう問題を解決しました（タッチ防止ロック機能）。
- **かわいい劇的なアニメーション**：
  1. 1回目：「いいえ」ボタンが別の場所に逃げます。
  2. 2回目：いたずら子猫（`🐈`）が上から飛び降りてきます。「『いいえ』はボクがもらったにゃ！🐾」というセリフを表示し、ボタンを抱えて足跡（`🐾`）を残しながら画面を走り去ります。
  3. ボタンが消えたあと、「はい！❤️」ボタンが大きくなってピカピカ光り、思わず押したくなります。

### 📅 2. カレンダーと時間帯の選択
- 相手は30日先までの空いている日をカレンダーで見ることができます。
- 「🌙 夜（19時〜）」「☀️ 午後（14時〜）」「☕ 昼 / ランチ」の3つの時間帯から選べます。
- **Googleカレンダーにワンタップで登録**できる便利なボタンも自動で作られます。

### 🟢 3. LINEやSNSとのスマートな連携
- **1つのボタンで完結するスマートなLINE機能**：
  デートの日程が決まったあと、「🟢 〇〇とLINEで連絡する」ボタンを押すと：
  1. デートの日程を書いたメッセージが自動でスマホのクリップボードにコピーされます。
     > *「〇〇さん、こんにちは！デートのお誘いOKです！2026-10-25（夜）にしましょう！✨🥂」*
  2. 画面に「メッセージをコピーしました！」という通知が出ます。
  3. あなたのLINE追加画面（`https://line.me/ti/p/~あなたのID`）が開き、相手は「友だち追加」をしてトークに貼るだけで返信できます。
- **WhatsApp・Facebook Messengerにも対応**しています。

### 🌐 4. 4つの言語にいつでも切り替え可能
- 画面右上のマークから、いつでも言葉を変えられます：
  - 🇯🇵 **日本語** (`ja`)
  - 🇺🇸 **英語** (`en`)
  - 🇧🇷 **ポルトガル語** (`pt`)
  - 🇪🇸 **スペイン語** (`es`)
- 相手のスマホの言語に合わせて自動で表示されます。

### 📊 5. リアルタイム回答ダッシュボード
- 作ったリンクに誰かがアクセスした回数や、「いいえ」から逃げた回数がリアルタイムで見られます。
- 相手が日程を選んで「確定」を押すと、画面を更新しなくてもポンッと画面にお知らせが届きます（WebSocket機能）。

---

## 🛠️ どうやって作ったの？（技術構成）

このアプリは、シンプルで軽く、そして早く動くように設計されています。

- **バックエンド（サーバー側）**：
  - **Python 3.12**：最新の安定したPythonを使用。
  - **FastAPI**：とても高速でモダンなWebフレームワーク。
  - **Uvicorn**：非同期処理（ASGI）を動かすサーバー。
  - **SQLAlchemy & SQLite**：作ったリンクや回答を保存する軽量データベース。
- **フロントエンド（見た目と動き）**：
  - **HTML5 & Jinja2テンプレート**：サーバーから動的に画面を生成。
  - **Tailwind CSS**：デザインが崩れず、スマホでもパソコンでも綺麗に見えるデザイン。
  - **Vanilla JavaScript（ピュアJavaScript）**：重いライブラリを使わず、軽快に動くアニメーションとクリップボード操作。
  - **Canvas Confetti**：画面いっぱいに紙吹雪を飛ばすお祝いエフェクト。

---

## 📁 フォルダ構成

```
├── app/
│   ├── routes/
│   │   ├── api.py                 # リンク作成やデータ処理の窓口（API）
│   │   ├── web.py                 # 各ページ（トップ、いたずら、デート、管理画面）の表示
│   │   └── auth_google.py         # Googleカレンダー連携機能
│   ├── services/
│   │   ├── i18n_service.py        # 4言語の翻訳データと自動判定ロジック
│   │   ├── notification_dispatcher.py  # ボット通知機能
│   │   └── google_calendar.py     # カレンダーの空き時間チェック
│   ├── static/                    # CSS（スタイル）やアイコン
│   ├── templates/                 # 画面のHTMLファイル
│   │   ├── index.html             # リンクを作るトップ画面（タブ切り替え式）
│   │   ├── prank_view.html        # 友達へのいたずら画面
│   │   ├── date_view.html         # 子猫とカレンダー付きのデート画面
│   │   └── dashboard.html         # リアルタイム管理画面
│   ├── config.py                  # 設定ファイル（ポート番号など）
│   ├── database.py                # データベースの接続設定
│   └── models.py                  # データの設計図
├── .env.example                   # 設定のサンプルファイル
├── .gitignore                     # GitHubにアップロードしないファイルの設定
├── requirements.txt               # 必要なPythonライブラリの一覧
├── run.py                         # アプリを起動するメインファイル（ポート8050）
├── start_site.bat                 # Windowsで1クリック起動するバッチファイル
└── README.md                      # 英語の詳しい説明書
```

---

## 🚀 自分のパソコンで動かす方法

### 必要なもの
- **Python 3.10以上**（Python 3.12をおすすめします）

### 手順

1. **このリポジトリをダウンロード（クローン）します**：
   ```bash
   git clone https://github.com/あなたのユーザー名/zoeira-date-matcher.git
   cd zoeira-date-matcher
   ```

2. **仮想環境（venv）を作って有効化します**：
   ```bash
   # Windowsの場合
   python -m venv venv
   venv\Scripts\activate

   # Mac / Linuxの場合
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **必要なライブラリをインストールします**：
   ```bash
   pip install -r requirements.txt
   ```

4. **アプリを起動します**：
   ```bash
   python run.py
   ```
   ターミナルに表示された **`http://localhost:8050`** をブラウザで開くと、アプリが動きます！

---

## 🌐 24時間いつでもネット上に公開する方法

自分のパソコンを消しても、友達や好きな人がいつでもアクセスできるようにクラウドサーバー（無料〜低価格）に公開する方法です。

### おすすめ：Render.com を使う方法（簡単・無料枠あり）
1. このプロジェクトをご自身のGitHubアカウントにアップロード（プッシュ）します。
2. [Render.com](https://render.com) にアクセスしてアカウントを作ります（GitHub連携でログインできます）。
3. **「New +」** から **「Web Service」** を選び、GitHubのリポジトリを選択します。
4. 設定を以下のように入力します：
   - **Environment**：`Python`
   - **Build Command**：`pip install -r requirements.txt`
   - **Start Command**：`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **「Deploy Web Service」** をクリックします。数分待つと、全世界からアクセスできる無料のURL（例：`https://your-app.onrender.com`）が手に入ります！

### 自宅PCから今すぐ一時的に公開したい場合：Cloudflare Tunnel
パソコンに `cloudflared` がある場合、以下のコマンドを打つだけで無料かつ安全に公開URLが発行されます：
```bash
cloudflared tunnel --url http://localhost:8050
```

---

## 📄 ライセンス

このプロジェクトは **[MIT License](LICENSE)** のもとで公開されています。自由に改造して使ってください！

---

<p align="center">
  みんなの笑顔と素敵なご縁のために作られました ❤️
</p>
