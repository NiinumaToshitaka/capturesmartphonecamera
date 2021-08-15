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

    def __init__(self, detection_result_save_dir: str):
        self.__counter = RingCounter.RingCounter(
            ImageProcessing.__SAVE_COUNT_MAX
        )
        """画像の保存枚数カウンタ"""
        self.__motion_detector = MotionDetection.MotionDetection()
        """動体検知オブジェクト"""
        self.__prev_image: np.ndarray = None
        """前フレーム画像"""
        self.__detection_result_save_dir = detection_result_save_dir
        """動体検知結果の保存先ディレクトリ"""

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
        current_image = ImageProcessing.__decode_image(img_base64)
        """画像"""
        # 画像を保存
        self.__save_image(current_image)
        # 動体検知を行う
        detection_result = self.__motion_detector.detect(current_image)
        response = ImageProcessing.__make_response(detection_result)
        # 動体検知結果が空でなければ検知結果を保存
        if detection_result.size():
            MotionDetection.MotionDetectionResultProcessing.save(
                detection_result,
                current_image,
                self.__prev_image,
                self.__detection_result_save_dir,
            )
        # 現在のフレームを前フレームとして格納
        self.__prev_image = current_image.copy()
        return response
