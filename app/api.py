"""リクエストに対するルーティング実装"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from enum import IntEnum
import os
from . import service

DETECTION_RESULTS_SAVE_DIR = "app/static/detection_results"
"""検知結果を保存するディレクトリ"""


class HttpResponseStatusCode(IntEnum):
    """HTTPレスポンスステータスコード

    値の詳細は
    [HTTP レスポンスステータスコード - HTTP | MDN]
    (https://developer.mozilla.org/ja/docs/Web/HTTP/Status)
    を参照
    """

    OK = 200
    """リクエストが成功した"""
    Bad_Request = 400
    """構文が無効であるためサーバーがリクエストを理解できない"""


api = Flask(__name__)
"""Flask apiオブジェクト"""
# レスポンスのjsonの文字コードを(asciiでなく)utf-8にする。
# これを設定しないと日本語がunicodeになる。
api.config["JSON_AS_ASCII"] = False

# CORS(Cross-Origin Resource Sharing)対応のために必要
CORS(api)

image_prosessor = service.ImageProcessing(DETECTION_RESULTS_SAVE_DIR)
"""画像処理オブジェクト"""


@api.route("/", methods=["GET"])
def index():
    return render_template("index.html"), HttpResponseStatusCode.OK


@api.route("/capture_img", methods=["POST"])
def capture_img():
    """画像データに対する処理を行う"""
    # リクエストから"img"パラメータを取得する。
    # パラメータが存在しない場合はNoneになる。
    img_base64 = request.form.get("img")
    if img_base64 is None:
        # Noneの場合はレスポンスを返して終了
        return (
            jsonify(service.make_response_dict(False, {})),
            HttpResponseStatusCode.Bad_Request,
        )
    # 画像データに対する処理を行う
    msg = image_prosessor.process(img_base64)
    return (
        jsonify(service.make_response_dict(True, msg)),
        HttpResponseStatusCode.OK,
    )


@api.route("/motion", methods=["GET"])
def motion():
    """動体検知結果のページを返す"""
    # ファイル名は"YYYYMMDD_HHMMSS_[.*].jpg"("YYYYMMDD_HHMMSS"は保存時の日付時刻)なので、
    # 先頭から15文字を取り出すことで、保存時の日付時刻を取得することができる。
    # 同一の日付時刻に3枚("current", "motion", "prev")の画像が保存されるため、
    # ファイル名から日付時刻を取得したあと、"set"関数により重複を取り除く。
    # 逆順にソートすることで日付時刻が新しい順になる。
    image_datetimes = reversed(
        sorted(set([x[0:15] for x in os.listdir(DETECTION_RESULTS_SAVE_DIR)]))
    )

    """動体検知結果の画像ファイルのリスト"""
    return (
        render_template(
            "motion_detection_result.html",
            image_datetimes=image_datetimes,
        ),
        HttpResponseStatusCode.OK,
    )
