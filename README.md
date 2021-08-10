# README

- [README](#readme)
  - [参考資料](#参考資料)
  - [開発環境](#開発環境)
    - [サーバ](#サーバ)
    - [クライアント](#クライアント)
  - [使用手順](#使用手順)
    - [Node.jsをインストール](#nodejsをインストール)
    - [http-serverインストール](#http-serverインストール)
    - [wsl2上のhttpsサーバに外部から接続](#wsl2上のhttpsサーバに外部から接続)
      - [wsl2側の設定](#wsl2側の設定)
      - [windows側の設定](#windows側の設定)
    - [ルータに接続したデバイス間の通信](#ルータに接続したデバイス間の通信)
    - [クライアントをサーバと同じネットワークに接続する](#クライアントをサーバと同じネットワークに接続する)
  - [メモ](#メモ)
    - [powershellのコマンド履歴を取得](#powershellのコマンド履歴を取得)
      - [現在のセッションの履歴を取得](#現在のセッションの履歴を取得)
      - [以前のセッションの履歴まで含めて取得](#以前のセッションの履歴まで含めて取得)

## 参考資料

- [スマフォカメラにブラウザからアクセス - Qiita](https://qiita.com/tkyko13/items/1871d906736ac88a1f35)

## 開発環境

### サーバ

- OS: *ubuntu 18.04* on *wsl2* on *windows 10 home*

### クライアント

- モデル：ASUS_Z017DA
- ビルド番号：OPR1.170623.026.JP_Phone-15.0410.1807.75
- OS: Android 8.0.0
- ブラウザ：Chrome 92.0.4515.131

## 使用手順

基本的に参考資料の通りに進める

### Node.jsをインストール

参考文献：[WSL 2 上で Node.jis を設定する | Microsoft Docs](https://docs.microsoft.com/ja-jp/windows/dev-environment/javascript/nodejs-on-wsl)

基本的に参考文献に従う。

1. `sudo apt install curl`を使用して`cURL`をインストールする(コマンドラインでインターネットからコンテンツをダウンロードするために使用するツール)。ただし`wget`が使えるなら`cURL`は不要。
1. <https://github.com/nvm-sh/nvm#install--update-script>のコマンドを実行する
1. 端末を閉じて再度開く
1. インストールを確認するには、`command -v nvm`を入力する。これによって`nvm`が返される。
   1. シェルにzshを使用している場合、インストールスクリプトで`~/.zshrc`へ追記できず、上記コマンドで何も返ってこない場合がある。この場合は、`~/.bashrc`に以下のようなnvmの環境変数設定などが追加されているので、これを`~/.zshrc`にコピーし、`source ~/.zshrc`で変更を適用する

      ```bash
      # ~/.bashrc
      # この通りに追加されているとは限らないので、
      # ファイルを確認すること
      export NVM_DIR="$HOME/.nvm"
      [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
      [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
      ```

1. 現在インストールされている Node のバージョンを一覧表示します (この時点では何もないはずです): `nvm ls`
1. Node.js の最新の安定した LTS リリースをインストールします (推奨): `nvm install --lts`
   1. 参考文献では現在のリリースをインストールする手順も記載されているが、バージョンを切り替える必要が出たときにやればよい
1. インストールされている Node のバージョンを一覧表示します: `nvm ls`。インストールしたバージョン（以下では`v14.17.4`）が表示されることを確認する。

    ```zsh
    ✗ nvm ls
    ->     v14.17.4
            system
    default -> lts/* (-> v14.17.4)
    iojs -> N/A (default)
    unstable -> N/A (default)
    node -> stable (-> v14.17.4) (default)
    stable -> 14.17 (-> v14.17.4) (default)
    lts/* -> lts/fermium (-> v14.17.4)
    lts/argon -> v4.9.1 (-> N/A)
    lts/boron -> v6.17.1 (-> N/A)
    lts/carbon -> v8.17.0 (-> N/A)
    lts/dubnium -> v10.24.1 (-> N/A)
    lts/erbium -> v12.22.4 (-> N/A)
    lts/fermium -> v14.17.4
    ```

1. Node.js がインストールされており、現在の既定のバージョンであることを確認します: `node --version`を使用。次に、`npm`があることも確認します: `npm --version`を使用。
1. プロジェクトに使用する Node.js のバージョンを変更するには、`mkdir NodeTest`（ディレクトリ名は例）で新しいプロジェクトディレクトリを作成し、`cd NodeTest`でディレクトリを移動する。次に`nvm use node`を入力して現在のバージョンに切り替えるか、または`nvm use --lts`を入力して LTS のバージョンに切り替えます。また、`nvm use v8.2.1`のように、インストールした追加のバージョンに固有の番号を使用することもできます (使用可能な Node.js のバージョンをすべて一覧表示するには、コマンド`nvm ls-remote`を使用します)。
1. プロジェクトのルートディレクトリで`npm init`を実行し、npmの管理下に置く。
1. vscodeで拡張機能*Node Extension Pack*(拡張機能ID: `swellaby.node-pack`)をインストールする。

### http-serverインストール

手早くwebサーバを立てるのに使う。

```bash
# よくわからないがローカルではなくグローバルにインストールしないと実行できない
npm install -g http-server
```

### wsl2上のhttpsサーバに外部から接続

windowsとwsl2は別ホストとして扱われるため，wsl2上でhttpsサーバを起動しても，そのままでは外部からwsl2のhttpsサーバにアクセスできない。このため，windows側でポートフォワーディングを設定する必要がある。

#### wsl2側の設定

```bash
# sshサービスを起動
sudo service ssh restart

# ipアドレスを取得
# wsl2のipアドレスはwindowsが再起動するたびに変わるので，
# 毎回取得する必要がある。
$ ip addr show dev eth0 | grep -w inet
# この場合は`172.27.48.40`がipアドレス。
# このアドレスが`ip_addr_of_wsl2`になる。
inet 172.27.48.40/20 brd 172.27.63.255 scope global eth0

# httpサーバを起動
# 今回は使用しない。
$ http-server

# httpsサーバを起動
# スマホのブラウザでカメラを利用するには
# httpsである必要があるので，こちらを使用する。
$ http-server -S -C cert.pem
```

windows側のブラウザで`https://[ip_addr_of_wsl2]:8080`にアクセスし，ページを開けることを確認する。

#### windows側の設定

wsl2のlocalhostフォワーディングを有効にする。
`localhost`でwsl2にアクセスしない場合はやらなくてもいい。
`c:\Users\<ユーザ名>\.wslconfig`に以下のように記述する。

```ini
localhostForwarding=True
```

管理者権限で以下のコマンドを実行すること。
アドレスとポート番号は適宜変更すること。

参考：[wsl2でsshサーバを起動し、外部からそこに接続 - Qiita](https://qiita.com/yabeenico/items/15532c703974dc40a7f5)

```powershell
# Windowsのポート8080(listenport)に来たパケットをwsl2(connectaddress)のポート8080に転送する
netsh.exe interface portproxy add v4tov4 listenport=8080 connectaddress=[ip_addr_of_wsl2]

# ポートフォワーディングを動作させるために，`IP Helper`サービスを起動する
# 以下の2つのコマンドは，一度実行すれば
# 以降はwindowsを再起動しても有効になっているので，
# 再度入力する必要はない。
# ブート時の自動起動設定
sc.exe config iphlpsvc start=auto
# サービスの起動
sc.exe start iphlpsvc

# 以上のコマンドを発行した時点で、ポートフォワーディングが有効になる(再起動不要)。
# 設定確認
# Portの列が8080の行が追加されていればよい。
> netsh.exe interface portproxy show v4tov4

ipv4 をリッスンする:         ipv4 に接続する:

Address         Port        Address           Port
--------------- ----------  ----------------- ----------
*               8080        [ip_addr_of_wsl2] 8080
localhost       22          172.27.48.1       22

# 設定削除
# 間違えて設定してしまったときに使用する。
# `listenport`と`listenaddress`で削除する条件を指定できる。
netsh.exe interface portproxy delete v4tov4 listenport=22
```

なお，windows側の設定は，再起動するたびにpowershellで以下を実行するバッチを用意すれば，上記の設定を自動化できる。

```powershell
# `Ubuntu`の部分はwslディストリビューション名
$IP = wsl -d Ubuntu exec hostname -I
netsh.exe interface portproxy delete v4tov4 listenport=8080
netsh.exe interface portproxy add    v4tov4 listenport=8080 connectaddress=$IP
```

### ルータに接続したデバイス間の通信

ルータの設定によっては，接続しているデバイス間で通信できない。
ルータの設定を確認すること。

### クライアントをサーバと同じネットワークに接続する

ここでは簡単のためにandroid端末をWi-Fiでwindowsマシンへ接続するものとする。

**サーバとなるwindowsマシンから，クライアントとなるandroid端末にpingが通ったとしても，同じネットワークに接続していないとwebアプリケーションへアクセスできない。**
android端末のipアドレスを見て，windowsマシンと同じネットワークに接続していることを必ず確認すること。
android端末のipアドレスは，今回使用するモデルの場合は
設定アプリ -> 無線とネットワーク -> Wi-Fi -> 右上のハンバーガーボタン -> Wi-Fi詳細
から見られる。

## メモ

### powershellのコマンド履歴を取得

参考：[PowerShellのコマンド実行履歴を取得する方法](https://zenn.dev/unsoluble_sugar/articles/ec7f052e36181c2f33be)

#### 現在のセッションの履歴を取得

```powershell
> Get-History
```

#### 以前のセッションの履歴まで含めて取得

```powershell
# コマンドの実行ログが記録されたファイルのパスが表示される
> (Get-PSReadlineOption).HistorySavePath
C:\Users\toshi\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```
