# coding=utf-8
import os
import time
import ddt
import unittest
# 设置
from selenium.common.exceptions import WebDriverException

import Settings
# 工具类
from Utils.Browser.WebBrowser import chrome
from Utils.Browser.WebBrowser import edge
from Utils.Browser.WebBrowser import close_down
from Utils.ElementUtil.Element import Element
from Utils.DataBase.Oracle import Oracle
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.Report.Log import *
from Utils.Excel.readXls import *
# SQL
# from TestCases import SQL
# 页面元素
from Pages import DemoPage

data = [{'a': 'ok'}, {'a': 'ng'}, {'a': 'ok'}]


@ddt.ddt
class TestDemo(unittest.TestCase):
    # 用例组名：__module__: __name__ : __doc__
    # __module__ = '*测试示例*'
    # __name__ = '-测试示例-'
    __doc__ = '-测试示例-'

    def setUp(self):
        print('begin')
        self.imgs = []  # 截图存储列表
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.dpi = Settings.DPI

    def tearDown(self):
        close_down(self)

    @ddt.data(*read_data_by_sheet_name(os.path.join(Settings.BASE_DIR, 'DS', 'TestDemo.xlsx'), 'Sheet2'))
    def test_a(self, ds):
        self._testMethodDoc = ds['desc']
        self.log.info('打开网页')
        self.driver.get(ds['url'])
        self.el.get(DemoPage.KW).send_keys(ds['kw'])
        self.el.get(DemoPage.SEARCH).click()
        former_hds = self.driver.window_handles
        self.el.gets(DemoPage.RES)[0].click()
        self.imgs.append(self.el.catch_screen(self.dpi))
        self.el.wait_until_window_open_and_switch(former_hds)
        self.el.scroll_into_view(DemoPage.TEACHER)
        self.el.get(DemoPage.ROY)
        self.imgs.append(self.el.catch_screen(self.dpi))

    @ddt.data(*read_data_by_sheet_name(os.path.join(Settings.BASE_DIR, 'DS', 'TestDemo.xlsx'), 'Sheet1'))
    def test_b(self, ds):
        # 测试描述
        self._testMethodDoc = ds['desc']
        self.log.info('打开网页')
        # self.driver.get(ds['url'])
        self.el.open_url(ds['url'])
        # 引用页面中的常量
        # self.driver.switch_to.frame(self.el.get(DemoPage.IFRAME))
        self.el.switch_to_frame(DemoPage.IFRAME)
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        # self.el.get(DemoPage.BUTTON, ds['button']).click()
        self.el.click(DemoPage.BUTTON, ds['button'])
        # 等待
        self.el.wait_until_invisible(DemoPage.SQUARE)
        # 手动截图
        # img = self.driver.get_screenshot_as_base64()
        self.imgs.append(self.el.catch_screen(dpi=self.dpi))
        # 检查点
        self.assertEquals(False, self.el.get(DemoPage.SQUARE).is_displayed(), ds['msg'])

    @unittest.skip
    def test_c(self):
        self._testMethodDoc = '数据库连接测试'
        pass

    def test_d(self):
        self._testMethodDoc = 'Edge'
        self.driver = edge()
        self.el = Element(self.driver, self.log)
        self.driver.get('https://www.baidu.com')
        self.imgs.append(self.driver.get_screenshot_as_base64())


if __name__ == '__main__':
    # 用例不在这里运行
    pass
    # unittest.main()
    fileBase = '../../a.html'  # 目录
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fileBase,
        title='{ Test Demo }',
        description='Test Demo',
        tester='ted',
        retry=0
    )
    # suit = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    suit2 = unittest.TestSuite()
    tc = [TestDemo('test_a_1')]
    suit2.addTests(tc)
    runner.run(suit2)

