# README

## 参考資料

* [スマフォカメラにブラウザからアクセス - Qiita](https://qiita.com/tkyko13/items/1871d906736ac88a1f35)

## 開発環境

* OS: <u>ubuntu 18.04</u> on <u>wsl2</u> on <u>windows 10 home</u>

## 使用手順

基本的に参考資料の通りに進める

### wslにnode.jsをインストールする手順

[WSL 2 上で Node.jis を設定する | Microsoft Docs](https://docs.microsoft.com/ja-jp/windows/dev-environment/javascript/nodejs-on-wsl)

### wsl2上のhttpsサーバに外部から接続

windowsとwsl2は別ホストとして扱われるため，wsl2上でhttpsサーバを起動しても，そのままでは外部からwsl2のhttpsサーバにアクセスできない。このため，windows側でポートフォワーディングを設定する必要がある。

参考：[wsl2でsshサーバを起動し、外部からそこに接続 - Qiita](https://qiita.com/yabeenico/items/15532c703974dc40a7f5)

管理者権限で以下のコマンドを実行すること。
アドレスとポート番号は適宜変更すること。

```powershell
# Windows(listenaddress)のポート22(listenport)に来たパケットをwsl2(connectaddress)のポート22(connectport)に転送する
# なお，listenaddress, connectportは省略可能
netsh.exe interface portproxy add v4tov4 listenaddress=localhost listenport=22 connectaddress=[ip_addr_of_wsl2] connectport=22

# ポートフォワーディングを動作させるために，IP Helperサービスを起動する
# ブート時の自動起動設定
sc.exe config iphlpsvc start=auto
# サービスの起動
sc.exe start iphlpsvc

# 以上のコマンドを発行した時点で、ポートフォワーディングが有効になる(再起動不要)。
# 設定確認
netsh.exe interface portproxy show v4tov4

# 設定削除
netsh.exe interface portproxy delete v4tov4 listenport=22
```

### ルータに接続したデバイス間の通信

ルータの設定によっては，接続しているデバイス間で通信できない。
ルータの設定を確認すること。
