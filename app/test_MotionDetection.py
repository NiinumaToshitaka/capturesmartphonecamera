"""MotionDetectionクラスによる動体検知のテスト

プロジェクトのルートディレクトリで実行すること。
`python app/[this_module].py`
"""

import cv2
import service


def test_motion_detection():
    """MotionDetectionクラスによる動体検知のテスト"""
    SAVE_PATH = "images/img{:05d}.jpg"
    """画像の保存先パス"""
    WINDOW_NAME = "motion detection result"
    """検知結果を表示するウィンドウ名"""
    motion_detector = service.MotionDetection()
    """動体検知オブジェクト"""

    # 画像ファイルパスを生成
    filepath_0 = SAVE_PATH.format(0)
    """画像ファイルパス"""
    print("filepath_0 = " + filepath_0)
    # 画像読み込み
    frame_0 = cv2.imread(filepath_0)
    """画像データ"""

    # 画像を表示
    cv2.imshow(WINDOW_NAME, frame_0)
    # キー入力を待つ
    cv2.waitKey(0)

    # 動体検知
    status, detected_area = motion_detector.detect(frame_0)
    # 初回実行時は比較するべき前フレームが存在しないので、
    # 検知結果が必ずFalseになる
    assert status is False

    # 画像ファイルパスを生成
    filepath_1 = SAVE_PATH.format(1)
    """画像ファイルパス"""
    print("filepath_1 = " + filepath_1)
    # 画像読み込み
    frame_1 = cv2.imread(filepath_1)
    """画像データ"""

    # 画像を表示
    cv2.imshow(WINDOW_NAME, frame_1)
    # キー入力を待つ
    cv2.waitKey(0)

    # 動体検知
    status, detected_area = motion_detector.detect(frame_1)
    """検知結果、検知した動体の位置"""
    print("frame_1 status = {}".format(status))
    if status is True:
        # 検知した動体の位置に矩形を描画
        print("detected_area = {}".format(detected_area))
        # 現フレームをコピー
        img = frame_1.copy()
        RECT_COLOR = (0, 255, 0)
        """矩形の描画色"""
        RECT_THICKNESS = 2
        """矩形の線の太さ"""
        cv2.rectangle(
            img,
            (detected_area[0], detected_area[1]),
            (
                detected_area[0] + detected_area[2],
                detected_area[1] + detected_area[3],
            ),
            RECT_COLOR,
            RECT_THICKNESS,
        )
        # 画像を表示
        cv2.imshow(WINDOW_NAME, img)
        # キー入力を待つ
        cv2.waitKey(0)


if __name__ == "__main__":
    test_motion_detection()
