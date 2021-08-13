"""httpsサーバを起動する"""

from app.api import api
import ssl

"""証明書ファイル"""
CERT_FILE = "keys/cert.pem"
"""秘密鍵ファイル"""
KEY_FILE = "keys/key.pem"
"""待ち受けアドレス"""
HOST = "192.168.10.103"
"""待ち受けポート番号"""
PORT = 8081


def main():
    """アプリケーションメイン処理"""
    # https通信を有効にする
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    api.run(host=HOST, port=PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
