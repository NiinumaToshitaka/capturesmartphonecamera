"""RingCounterクラスのテストケース"""

import unittest
from python_modules import RingCounter


class TestRingCounter(unittest.TestCase):
    """RingCounterクラスのテストケース"""

    __COUNT_LIMIT = 10
    """カウンタの最大値"""

    def test_increment(self):
        """カウントする"""
        counter = RingCounter.RingCounter(TestRingCounter.__COUNT_LIMIT)
        """カウンタ"""
        # カウントする
        counter.increment()
        current_count = counter.get_count()
        """現在のカウンタの値"""
        EXPECT_COUNT = 1
        """期待するカウンタの値"""
        self.assertEqual(EXPECT_COUNT, current_count)

    def test_count_limit(self):
        """規定回数カウントしたら、カウンタが0に戻る"""
        counter = RingCounter.RingCounter(TestRingCounter.__COUNT_LIMIT)
        """カウンタ"""
        # 規定回数カウント
        for i in range(0, TestRingCounter.__COUNT_LIMIT):
            counter.increment()
        current_count = counter.get_count()
        """現在のカウンタの値"""
        EXPECT_COUNT = 0
        """期待するカウンタの値"""
        self.assertEqual(EXPECT_COUNT, current_count)
