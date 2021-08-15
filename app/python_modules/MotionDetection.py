"""MotionDetectionクラス実装"""

import numpy as np
import cv2
from datetime import datetime
import os

# tuple型の型アノテーションに使用
from typing import Tuple, List


# TODO 単純に動体検知結果のデータ型を"List[Tuple[int, int, int, int]]"として定義したいのなら、
#      [Type aliases]
#      (https://docs.python.org/3/library/typing.html#type-aliases)
#      のほうが素直
class MotionDetectionResult:
    """動体検知結果"""

    def __init__(self, detected_area: List[Tuple[int, int, int, int]]):
        """コンストラクタ

        Args:
            detected_area: 検知した動体の位置
                画像に対して、(x, y, width, height)の順
        """
        self.detected_area = detected_area
        """検知した動体の位置"""

    def size(self) -> int:
        """検知した動体の個数を返す

        Returns:
            検知した動体の個数
        """
        return len(self.detected_area)

    def get(self) -> List[Tuple[int, int, int, int]]:
        return self.detected_area.copy()


class MotionDetection:
    """画像からの動体検知を扱う

    Note:
        [Python+OpenCVとWebカメラを使って動体検知する話 - EnsekiTT Blog]
        (https://ensekitt.hatenablog.com/entry/2018/06/11/200000)のコードを実装した。
    """

    __AREA_LIMIT_MIN = 1000
    """動体とみなす検知結果面積の最小値[pixel]"""
    __AREA_LIMIT_MAX = 10000
    """動体とみなす検知結果面積の最大値[pixel]"""
    __ACCUMULATION_WEIGHT = 0.5
    """前フレームとの移動平均の重み"""

    def __init__(self):
        self.__before_frame = None
        """前フレーム"""

    def detect(self, frame: np.ndarray) -> MotionDetectionResult:
        """動体検知を実行

        Args:
            frame: 画像データ

        Returns:
            動体検知結果
        """
        # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """グレイスケール化した画像"""
        if self.__before_frame is None:
            # 初めてフレームを取得した場合は、前フレームをセットして終了
            # print("before frame is None")
            self.__before_frame = gray.copy().astype("float")
            return MotionDetectionResult([])
        # 現フレームと前フレームの加重平均を使うと良いらしい
        cv2.accumulateWeighted(
            gray, self.__before_frame, MotionDetection.__ACCUMULATION_WEIGHT
        )
        mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(self.__before_frame))
        """動いているところが明るい画像"""

        # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する
        THRESHOLD = 3
        """しきい値"""
        MAXVAL = 255
        """2値化したときにしきい値以上の画素に与える値。
        中途半端な色にする理由は特にないので真っ黒にする。
        """
        thresh = cv2.threshold(
            mdframe,
            THRESHOLD,
            MAXVAL,
            cv2.THRESH_BINARY,
        )[1]
        """2値化画像"""
        # 輪郭データに変換してくれるfindContours
        # RETR_EXTERNAL: 一番外側の輪郭を出力する
        # CHAIN_APPROX_SIMPLE: 輪郭を出力するときに、省略できる検出点は省略する
        contours, hierarchy = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        """検出した輪郭のリスト, 検出した輪郭の階層情報"""

        # 輪郭を検出できなかった場合、前フレームと現フレームとの
        # 差分が存在しないため、動体が存在しない。
        if 0 == len(contours):
            # print("detect no motion")
            return MotionDetectionResult([])

        # 面積が規定の範囲にある輪郭を取り出す
        valid_contours = [
            cnt
            for cnt in contours
            if MotionDetection.__AREA_LIMIT_MIN
            < cv2.contourArea(cnt)
            < MotionDetection.__AREA_LIMIT_MAX
        ]

        # 動体検知結果オブジェクトを返す
        if 0 == len(valid_contours):
            # 検知できなかった場合
            return MotionDetectionResult([])
        else:
            detected_area = []
            """検知した矩形"""
            # 検知できた場合
            # 諸般の事情で矩形検出とした。
            for cnt in valid_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                """動体の位置(矩形左上のx座標, y座標, 矩形の幅, 高さ)"""
                detected_area.append((x, y, w, h))
            return MotionDetectionResult(detected_area)


class MotionDetectionResultProcessing:
    """動体検知結果を扱うクラス"""

    def __write_image(basename: str, image: np.ndarray, save_dir: str) -> None:
        """画像データをファイルに保存する

        Args:
            basename: ファイル名
            image: 画像データ
            save_dir: 画像の保存先ディレクトリ
        """
        # ファイルパスを生成
        filepath = os.path.join(save_dir, basename)
        # 画像をファイルに保存
        cv2.imwrite(filepath, image)
        return

    def save(
        detection_result: MotionDetectionResult,
        current_frame: np.ndarray,
        prev_frame: np.ndarray,
        save_dir: str,
    ) -> None:
        """検知結果を保存する

        以下の画像を保存する。
        - 現フレーム
        - 前フレーム
        - 現フレームに検知結果矩形を描画した画像

        Args:
            detection_result: 動体検知結果
            current_frame: 現フレーム
            prev_frame: 前フレーム
            save_dir: 画像の保存先ディレクトリ
        """
        # 現フレームを、矩形を描画する画像としてコピー
        canvas = current_frame.copy()
        """現フレーム"""
        # 検知結果の矩形を描画
        for rect in detection_result.get():
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
        basename_motion = "{}_motion.jpg".format(now_str)
        # 画像を保存
        MotionDetectionResultProcessing.__write_image(
            basename_current_frame, current_frame, save_dir
        )
        MotionDetectionResultProcessing.__write_image(
            basename_prev_frame, prev_frame, save_dir
        )
        MotionDetectionResultProcessing.__write_image(
            basename_motion, canvas, save_dir
        )
