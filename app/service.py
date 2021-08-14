"""リクエストに対するサービス実装"""

import base64
import numpy as np
import cv2
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

    def __save_image(self, img):
        """画像データをファイルに保存する

        Args:
            img (numpy.ndarray): 画像データ
        """
        filepath = ImageProcessing.__SAVE_PATH.format(
            self.__counter.get_count()
        )
        """デコードされた画像の保存先パス"""
        # 画像を保存
        cv2.imwrite(filepath, img)
        # 画像の保存枚数カウンタを1増やす
        self.__counter.increment()
        return

    def __make_response(
        self, detection_result: MotionDetection.MotionDetectionResult
    ) -> dict:
        """動体検知結果を格納した辞書型を作成する

        Args:
            detection_result: 動体検知結果

        Returns:
            動体検知結果を格納した辞書型
        """
        response = dict.fromkeys(["detection_status", "detected_area"])
        response["detection_status"] = detection_result.has_detect
        response["detected_area"] = str(detection_result.detected_area)
        return response

    def save_img(self, img_base64: str) -> dict:
        """base64にエンコードされた画像データをデコードして保存する。

        Args:
            img_base64: base64にエンコードされた画像データ

        Returns:
            動体検知結果
        """
        # binary <- string base64
        img_binary = base64.b64decode(img_base64)
        # jpg <- binary
        img_jpg = np.frombuffer(img_binary, dtype=np.uint8)
        # raw image <- jpg
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
        # 画像を保存
        self.__save_image(img)

        # 動体検知を行う
        detection_result = self.__motion_detector.detect(img)
        response = self.__make_response(detection_result)
        return response
