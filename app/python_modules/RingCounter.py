"""RingCounterクラス実装"""


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
