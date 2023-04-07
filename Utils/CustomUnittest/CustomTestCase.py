"""
@Time ： 2023/4/6 15:13
@Auth ： Ted
@File ：CustomTestCase.py
@IDE ：PyCharm
"""
import time
import unittest
import Settings


class CustomTestCase(unittest.TestCase):
    """
    重写setUp和tearDown方法，自动初始化截图列表,屏幕dpi,记录开始结束时间，计算用例执行持续时间
    """
    imgs = None
    dpi = 1.0
    logger = None  # 等待HTMLTestRunner注入
    beg = None

    def setUp(self) -> None:
        """
        初始化截图列表，屏幕dpi，记录开始时间
        :return: None
        """
        super(CustomTestCase, self).setUp()
        self.imgs = []  # 截图存储列表
        self.dpi = Settings.DPI
        self.beg = time.time()

    def tearDown(self) -> None:
        """
        记录结束时间，计算用例执行持续时间
        :return: None
        """
        super(CustomTestCase, self).setUp()
        if hasattr(self, 'beg'):
            end = time.time()
            delta = end - self.beg
            m, s = divmod(delta, 60)
            h, m = divmod(m, 60)
            print(f'Last {h:0>2.0f}:{m:0>2.0f}:{s:.3f}')
