"""リクエストに対するサービス実装"""

import base64
import numpy as np
import cv2
from datetime import datetime
import os
from app.python_modules import RingCounter, MotionDetection


def make_response_dict(
    request_status: bool, motion_detection_result: dict
) -> dict:
    """レスポンスのjsonを生成するもととなる辞書型を生成する

    Args:
        request_status: リクエストステータス。
            True: リクエストパラメータが正常
            False: リクエストパラメータが不正
        motion_detection_result: 動体検知結果

    Returns:
        レスポンスのjsonを生成するもととなる辞書型
    """
    response = dict.fromkeys(["request_status", "detection_result"])
    response["request_status"] = request_status
    response["detection_result"] = motion_detection_result
    return response


class MotionDetectionResultProcessing:
    """動体検知結果を扱うクラス"""

    __SAVE_DIR = "detection_results/"
    """検知結果の保存先ディレクトリ"""

    def save(
        detection_result: MotionDetection.MotionDetectionResult,
        current_frame: np.ndarray,
        prev_frame: np.ndarray,
    ) -> None:
        """検知結果を保存する

        Args:
            detection_result: 動体検知結果
            current_frame: 現フレーム
            prev_frame: 前フレーム
        """
        # 現フレームを、矩形を描画する画像としてコピー
        canvas = current_frame.copy()
        """現フレーム"""
        res = detection_result.get()
        """検知結果"""

        # 検知結果の矩形を描画
        for rect in res:
            top_left = (rect[0], rect[1])
            bottom_right = (rect[0] + rect[2], rect[1] + rect[3])
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(canvas, top_left, bottom_right, color, thickness)

        now = datetime.now()
        """現在時刻"""
        # 現在時刻を文字列に変換
        # フォーマットは、2021/08/15 11:52:14の場合、"20210815_115214"となる。
        now_str = now.strftime("%Y%m%d_%H%M%S")
        """現在時刻の文字列表現"""
        # 画像ファイルパス生成
        basename_current_frame = "{}_current.jpg".format(now_str)
        basename_prev_frame = "{}_prev.jpg".format(now_str)
        filepath_current_frame = os.path.join(
            MotionDetectionResultProcessing.__SAVE_DIR,
            basename_current_frame,
        )
        filepath_prev_frame = os.path.join(
            MotionDetectionResultProcessing.__SAVE_DIR,
            basename_prev_frame,
        )
        # 画像を保存
        cv2.imwrite(
            filepath_current_frame,
            canvas,
        )
        cv2.imwrite(filepath_prev_frame, prev_frame)


class ImageProcessing:
    """画像処理を扱うクラス"""

    __SAVE_PATH = "images/img{:05d}.jpg"
    """画像の保存先パス"""
    __SAVE_COUNT_MAX = 10
    """画像を保存する最大枚数"""

    def __init__(self):
        self.__counter = RingCounter.RingCounter(
            ImageProcessing.__SAVE_COUNT_MAX
        )
        """画像の保存枚数カウンタ"""
        self.__motion_detector = MotionDetection.MotionDetection()
        """動体検知オブジェクト"""
        self.__prev_image: np.ndarray = None
        """前フレーム画像"""

    def __save_image(self, img: np.ndarray) -> None:
        """画像データをファイルに保存する

        Args:
            img: 画像データ
        """
        filepath = ImageProcessing.__SAVE_PATH.format(
            self.__counter.get_count()
        )
        """画像の保存先パス"""
        # 画像を保存
        cv2.imwrite(filepath, img)
        # 画像の保存枚数カウンタを1増やす
        self.__counter.increment()

    def __make_response(
        detection_result: MotionDetection.MotionDetectionResult,
    ) -> dict:
        """動体検知結果を格納した辞書型を作成する

        Args:
            detection_result: 動体検知結果

        Returns:
            動体検知結果を格納した辞書型
        """
        response = dict.fromkeys(["detected_area"])
        response["detected_area"] = detection_result.detected_area
        return response

    def __decode_image(img_base64: str) -> np.ndarray:
        """base64にエンコードされた画像データをデコードする

        Args:
            img_base64: base64にエンコードされた画像データ

        Returns:
            画像
        """
        # binary <- string base64
        img_binary = base64.b64decode(img_base64)
        # jpg <- binary
        img_jpg = np.frombuffer(img_binary, dtype=np.uint8)
        # raw image <- jpg
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
        return img

    def process(self, img_base64: str) -> dict:
        """base64にエンコードされた画像データに対して動体検知を行う

        Args:
            img_base64: base64にエンコードされた画像データ

        Returns:
            動体検知結果
        """
        # 画像データをデコード
        img = ImageProcessing.__decode_image(img_base64)
        """画像"""
        # 画像を保存
        self.__save_image(img)
        # 動体検知を行う
        detection_result = self.__motion_detector.detect(img)
        response = ImageProcessing.__make_response(detection_result)
        print("detection_result.size() = {}".format(detection_result.size()))
        # 動体検知結果が空でなければ検知結果を保存
        if detection_result.size():
            MotionDetectionResultProcessing.save(
                detection_result, img, self.__prev_image
            )
        # 現在のフレームを前フレームとして格納
        self.__prev_image = img.copy()
        return response
