"""リクエストに対するサービス実装"""

import base64
import numpy as np
import cv2


class RingCounter:
    """0から指定した値まで循環して数えるカウンタ"""

    def __init__(self, count_limit: int):
        """コンストラクタ

        Args:
            count_limit: カウンタの最大値
        """
        self.__count = 0
        """カウンタ"""
        self.__count_limit = count_limit
        """カウンタの最大値"""

    def increment(self):
        """カウンタを1増やす"""
        self.__count += 1
        # カウンタが最大値に達した場合は0に戻る
        if self.__count_limit <= self.__count:
            self.__count = 0

    def get_count(self) -> int:
        """現在のカウンタの値を取得する

        Returns:
            現在のカウンタの値
        """
        return self.__count


class ImageProcessing:
    """画像処理を扱うクラス"""

    __SAVE_DIR = "images/"
    """画像の保存先パス"""
    __SAVE_COUNT_MAX = 10
    """画像を保存する最大枚数"""

    def __init__(self):
        self.__counter = RingCounter(ImageProcessing.__SAVE_COUNT_MAX)
        """画像の保存枚数カウンタ"""

    def __save_image(self, img):
        """画像データをファイルに保存する

        Args:
            img (numpy.ndarray): 画像データ
        """
        # デコードされた画像の保存先パス
        filepath = "{0}/img{1:05d}.jpg".format(
            ImageProcessing.__SAVE_DIR, self.__counter.get_count()
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
        print(type(img))
        # 画像を保存
        self.__save_image(img)
        return "SUCCESS"

    def img_processing(self):
        """受信画像に対する処理"""
        return
