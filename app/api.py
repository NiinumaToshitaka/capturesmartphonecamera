"""リクエストに対するルーティング実装"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from . import service

api = Flask(__name__)
"""Flask apiオブジェクト"""
# レスポンスのjsonの文字コードを(asciiでなく)utf-8にする。
# これを設定しないと日本語がunicodeになる。
api.config["JSON_AS_ASCII"] = False

# CORS(Cross-Origin Resource Sharing)対応のために必要
CORS(api)

image_prosessor = service.ImageProcessing()
"""画像処理オブジェクト"""


@api.route("/", methods=["GET"])
def index():
    return render_template("index.html"), 200


@api.route("/capture_img", methods=["POST"])
def capture_img():
    """画像データを保存する"""
    # リクエストから"img"パラメータを取得する。
    # パラメータが存在しない場合はNoneになる。
    img_base64 = request.form.get("img")
    if img_base64 is None:
        # Noneの場合はレスポンスを返して終了
        return jsonify(service.make_response_dict(False, {})), 400
    # 画像データを保存
    msg = image_prosessor.process(img_base64)
    return jsonify(service.make_response_dict(True, msg)), 200
