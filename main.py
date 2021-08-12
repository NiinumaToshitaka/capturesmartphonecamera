#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""JSONデータサーバ

[[python3] 簡易サーバでJSONデータ受け渡し　[POST] - Qiita]
(https://qiita.com/tkj/items/1338ad081038fa64cef8)
のコードをベースに実装

通信確認には以下のコマンドを使用する。

```bash
# --tlsv1.2: TLS1.2で通信
# --insecure: 自己署名証明書でも通信する。デフォルトだと怪しそうな証明書の場合は通信しない。
# -v: 通信時の情報を出力
# -X POST: POST通信する。実際にはこのオプションは自動的に推測されるようなので要らないかもしれない。
# -H: リクエストヘッダ
# -d: リクエストボディ
curl --tlsv1.2 --insecure -v -X POST -H "Content-Type: application/json" \
'https://[ip_address]:[port]' -d '{ "question": "今日の天気は" }'
```
"""

import http.server as s
import ssl
import json
from urllib.parse import parse_qs, urlparse


"""待ち受けアドレス"""
HOST = "192.168.10.103"
"""待ち受けポート番号"""
PORT = 8081
"""証明書"""
CERTFILE = "keys/cert.pem"
"""秘密鍵"""
KEYFILE = "keys/key.pem"


class MyHandler(s.BaseHTTPRequestHandler):
    """サーバに到着したリクエストを処理する

    `http.server.BaseHTTPRequestHandler`クラスを継承。
    HTTPリクエストを処理するには、適切な`do_*()`を実装する。
    """

    def do_POST(self):
        """'POST'型のHTTP要求に対するサービスを行う

        Note:
            CGI でない url に対して POST を試みた場合、
            出力は Error 501, "Can only POST to CGI scripts" になります。
        """

        # リクエスト取得
        content_len = int(self.headers.get("content-length"))
        body = json.loads(self.rfile.read(content_len).decode("utf-8"))

        # レスポンス処理
        body["answer"] = "晴れです。"
        self.send_response(200)
        self.send_header("Content-type", "application/json;charset=utf-8")
        self.end_headers()
        body_json = json.dumps(
            body, sort_keys=False, indent=4, ensure_ascii=False
        )
        self.wfile.write(body_json.encode("utf-8"))

    def do_GET(self):
        """'GET'型のHTTP要求に対するサービスを行う

        適当にメッセージを返す
        """
        print("path = {}".format(self.path))

        # クエリに含まれるパラメータをパース
        parsed_path = urlparse(self.path)
        print(
            "parsed: path = {}, query = {}".format(
                parsed_path.path, parse_qs(parsed_path.query)
            )
        )

        # クエリのヘッダ情報を表示
        print("headers\r\n-----\r\n{}-----".format(self.headers))

        # レスポンスを返す
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Hello from do_GET")


def main():
    """サーバ起動"""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # 証明書読み込み
    context.load_cert_chain(CERTFILE, keyfile=KEYFILE)
    # httpsサーバ起動
    httpd = s.HTTPServer((HOST, PORT), MyHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Server Starts - %s:%s" % (HOST, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        # "ctrl + c"で終了
        pass
    print("Server Stops - %s:%s" % (HOST, PORT))


if __name__ == "__main__":
    main()
