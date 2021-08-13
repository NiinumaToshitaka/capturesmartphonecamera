"""リクエストに対するサービス実装"""

import base64
import numpy as np
import cv2

SAVE_DIR = "images/img0000.jpg"
"""デコードされた画像の保存先パス"""


def save_img(img_base64: str) -> str:
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
    # デコードされた画像の保存先パス
    image_file = SAVE_DIR
    # 画像を保存
    cv2.imwrite(image_file, img)
    return "SUCCESS"
