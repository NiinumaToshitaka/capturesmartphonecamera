#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""JSONデータサーバ

[[python3] 簡易サーバでJSONデータ受け渡し　[POST] - Qiita]
(https://qiita.com/tkj/items/1338ad081038fa64cef8)
のコードを実装
"""

import http.server as s
import json


"""待ち受けアドレス"""
HOST = "192.168.10.103"
"""待ち受けポート番号"""
PORT = 8081


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


def main():
    """サーバ起動"""
    httpd = s.HTTPServer((HOST, PORT), MyHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
