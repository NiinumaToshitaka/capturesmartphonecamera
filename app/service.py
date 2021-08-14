"""リクエストに対するサービス実装"""

import base64
import numpy as np
import cv2
from app.python_modules import RingCounter, MotionDetection


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
        # デコードされた画像の保存先パス
        filepath = ImageProcessing.__SAVE_PATH.format(
            self.__counter.get_count()
        )
        # 画像を保存
        cv2.imwrite(filepath, img)
        # 画像の保存枚数カウンタを1増やす
        self.__counter.increment()
        return

    def save_img(self, img_base64: str) -> str:
        """base64にエンコードされた画像データをデコードして保存する。

        Args:
            img_base64: base64にエンコードされた画像データ

        Returns:
            レスポンスメッセージ
        """
        # binary <- string base64
        img_binary = base64.b64decode(img_base64)
        # jpg <- binary
        img_jpg = np.frombuffer(img_binary, dtype=np.uint8)
        # raw image <- jpg
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
        # 画像を保存
        self.__save_image(img)
        return "SUCCESS"

    def img_processing(self):
        """受信画像に対する処理"""
        # TODO 動体検知を行う
        return
