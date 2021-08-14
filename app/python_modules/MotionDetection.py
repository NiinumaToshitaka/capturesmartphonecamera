"""MotionDetectionクラス実装"""

import cv2


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

    def detect(self, frame) -> (bool, tuple(int, int, int, int)):
        """動体検知を実行

        Args:
            frame (numpy.ndarray): 画像データ

        Returns:
            bool: 動体を検知したか。
                  True: 検知した。
                  False: 検知しなかった。
            tuple: 動体を検知した場合、検知した動体の位置。
                   画像に対して、(x, y, width, height)の順。
                   動体を検知しなかった場合は空のtuple。
        """
        # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """グレイスケール化した画像"""
        if self.__before_frame is None:
            # 初めてフレームを取得した場合は、前フレームをセットして終了
            print("before frame is None")
            self.__before_frame = gray.copy().astype("float")
            return (False, ())
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
            print("detect no motion")
            return (False, ())

        max_area = 0
        """輪郭の面積の最大値"""
        target = contours[0]
        """面積が最も大きい輪郭"""

        # 検出した輪郭のうち、面積が最大のものを求める
        for cnt in contours:
            # 輪郭の面積を求めてくれるcontourArea
            area = cv2.contourArea(cnt)
            if (max_area < area) and (
                MotionDetection.__AREA_LIMIT_MIN
                < area
                < MotionDetection.__AREA_LIMIT_MAX
            ):
                max_area = area
                target = cnt

        # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
        if max_area <= MotionDetection.__AREA_LIMIT_MIN:
            # 検知できなかった場合
            return (False, ())
        else:
            # 検知できた場合
            # 諸般の事情で矩形検出とした。
            x, y, w, h = cv2.boundingRect(target)
            """動体の位置(矩形左上のx座標, y座標, 矩形の幅, 高さ)"""
            return (True, (x, y, w, h))
