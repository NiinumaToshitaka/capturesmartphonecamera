"""MotionDetectionクラスのテスト"""

import cv2
import service


def main():
    __SAVE_PATH = "images/img{:05d}.jpg"
    """画像の保存先パス"""

    motion_detector = service.MotionDetection()
    """動体検知オブジェクト"""
    filepath_0 = __SAVE_PATH.format(0)
    print("filepath_0 = " + filepath_0)
    """画像ファイルパス"""
    # 画像読み込み
    frame_0 = cv2.imread(filepath_0)
    # 動体検知
    motion_detector.detect(frame_0)

    filepath_1 = __SAVE_PATH.format(1)
    print("filepath_1 = " + filepath_1)
    # 画像読み込み
    frame_1 = cv2.imread(filepath_1)
    # 動体検知
    motion_detector.detect(frame_1)


if __name__ == "__main__":
    main()
