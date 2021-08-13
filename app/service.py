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


class MotionDetection:
    """画像からの動体検知を扱う

    Note:
        [Python+OpenCVとWebカメラを使って動体検知する話 - EnsekiTT Blog]
        (https://ensekitt.hatenablog.com/entry/2018/06/11/200000)のコードを実装した。
    """

    def __init__(self):
        self.__before_frame = None
        """前フレーム"""

    def detect(self, frame) -> (bool, tuple):
        """動体検知を実行

        Args:
            frame (numpy.ndarray): 画像データ

        Returns:
            bool: 動体を検知したか。True: 検知した。False: 検知しなかった。
            tuple: 動体を検知した場合、検知した動体の位置。画像に対して、(x, y, width, height)の順。
                   動体を検知しなかった場合は空のtuple。
        """
        # 加工なし画像を表示する
        cv2.imshow("Raw Frame", frame)
        # キー入力を待つ
        cv2.waitKey(0)

        # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """グレイスケール化した画像"""
        if self.__before_frame is None:
            # 初めてフレームを取得した場合は、前フレームをセットして終了
            print("before frame is None")
            self.__before_frame = gray.copy().astype("float")
            return (False, ())
        # 現フレームと前フレームの加重平均を使うと良いらしい
        cv2.accumulateWeighted(gray, self.__before_frame, 0.5)
        mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(self.__before_frame))

        # 動いているところが明るい画像を表示する
        cv2.imshow("MotionDetected Frame", mdframe)
        # キー入力を待つ
        cv2.waitKey(0)

        # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する
        thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]
        """2値化画像"""

        cv2.imshow("threshold Frame", thresh)
        # キー入力を待つ
        cv2.waitKey(0)

        # 輪郭データに変換してくれるfindContours
        # RETR_EXTERNAL: 一番外側の輪郭を出力する
        # CHAIN_APPROX_SIMPLE: 輪郭を出力するときに、省略できる検出点は省略する
        contours, hierarchy = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # 輪郭を検出できなかった場合、前フレームと現フレームとの
        # 差分が存在しないため、動体が存在しない。
        if 0 == len(contours):
            print("detect no motion")
            return (False, ())

        """検出した輪郭のリスト, 検出した輪郭の階層情報"""
        max_area = 0
        """輪郭の面積の最大値"""
        target = contours[0]
        """面積が最も大きい輪郭"""
        AREA_LIMIT_MIN = 1000
        """動体とみなす面積の最小値"""
        AREA_LIMIT_MAX = 10000
        """動体とみなす面積の最大値"""

        # 検出した輪郭のうち、面積が最大のものを求める
        for cnt in contours:
            # 輪郭の面積を求めてくれるcontourArea
            area = cv2.contourArea(cnt)
            if max_area < area and AREA_LIMIT_MIN < area < AREA_LIMIT_MAX:
                max_area = area
                target = cnt

        # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
        if max_area <= AREA_LIMIT_MIN:
            # 検知できなかった場合
            areaframe = frame
            cv2.putText(
                areaframe,
                "not detected",
                (0, 50),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 255, 0),
                3,
                cv2.LINE_AA,
            )
            cv2.imshow("MotionDetected Area Frame", areaframe)
            # キー入力を待つ
            cv2.waitKey(0)
            return (False, ())
        else:
            # 諸般の事情で矩形検出とした。
            x, y, w, h = cv2.boundingRect(target)
            areaframe = cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 255, 0), 2
            )
            cv2.imshow("MotionDetected Area Frame", areaframe)
            # キー入力を待つ
            cv2.waitKey(0)
            detected_area = (x, y, w, h)
            """動体の位置"""
            return (True, detected_area)


class ImageProcessing:
    """画像処理を扱うクラス"""

    __SAVE_PATH = "images/img{:05d}.jpg"
    """画像の保存先パス"""
    __SAVE_COUNT_MAX = 10
    """画像を保存する最大枚数"""

    def __init__(self):
        self.__counter = RingCounter(ImageProcessing.__SAVE_COUNT_MAX)
        """画像の保存枚数カウンタ"""
        self.__motion_detector = MotionDetection()
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
