"""リクエストに対するルーティング実装"""

from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from . import service

api = Flask(__name__)
"""Flask apiオブジェクト"""

# CORS(Cross-Origin Resource Sharing)対応のために必要
CORS(api)

image_prosessor = service.ImageProcessing()
"""画像処理オブジェクト"""


@api.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@api.route("/capture_img", methods=["POST"])
def capture_img():
    """画像データを保存する"""
    # リクエストから"img"パラメータを取得する。
    # パラメータが存在しない場合はNoneになる。
    img_base64 = request.form.get("img")
    if img_base64 is None:
        # Noneの場合はレスポンスを返して終了
        return make_response("FAILURE")
    # 画像データを保存
    msg = image_prosessor.save_img(img_base64)
    # 画像に対する処理を実行
    image_prosessor.img_processing()
    return make_response(msg)
