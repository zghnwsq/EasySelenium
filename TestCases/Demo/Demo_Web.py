# coding=utf-8
import os
import ddt
import unittest
# 设置
# from selenium.common.exceptions import WebDriverException
import Settings
# 工具类
from Utils.Browser.WebBrowser import chrome
from Utils.Browser.WebBrowser import edge
from Utils.Browser.WebBrowser import close_down
from Utils.ElementUtil.Element import Element
# from Utils.DataBase.Oracle import Oracle
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.Report.Log import *
from Utils.Excel.readXls import *
# SQL
# from TestCases import SQL
# 页面元素
from Pages.DemoPage import DemoPage

data_source = os.path.join(Settings.BASE_DIR, 'DS', 'Demo_Web', 'TestDemo.xlsx')


@ddt.ddt
class Demo_Web(unittest.TestCase):
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
        # self.demo_page = DemoPage(self.driver, self.log)
        self.dpi = Settings.DPI

    def tearDown(self):
        close_down(self)

    @ddt.data(*read_data_by_sheet_name(data_source, 'test_a'))
    def test_a(self, ds):
        demo_page = DemoPage(self.driver, self.log)
        self._testMethodDoc = ds['desc']
        self.log.info('打开网页')
        self.driver.get(ds['url'])
        demo_page.get(demo_page.KW).send_keys(ds['kw'])
        demo_page.get(demo_page.SEARCH).click()
        former_hds = self.driver.window_handles
        demo_page.get(demo_page.RES, ds['kw']).click()
        self.imgs.append(demo_page.catch_screen(self.dpi))
        demo_page.wait_until_window_open_and_switch(former_hds)
        demo_page.scroll_into_view(demo_page.TEACHER)
        demo_page.get(demo_page.ROY)
        self.imgs.append(demo_page.catch_screen(self.dpi))
        # self.driver.find_element_by_xpath('').location_once_scrolled_into_view

    @ddt.data(*read_data_by_sheet_name(data_source, 'test_b'))
    def test_b(self, ds):
        demo_page = DemoPage(self.driver, self.log)
        # 测试描述
        self._testMethodDoc = ds['desc']
        self.log.info('打开网页')
        demo_page.open_url(ds['url'])
        # 引用页面中的常量
        # demo_page.switch_to_frame(demo_page.IFRAME)
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        # demo_page.click(demo_page.BUTTON, ds['button'])
        click_at = demo_page.click_by_img_recognition('D:/20211105133533.png', threshold=0.9, img_type='base64')
        self.imgs.append(click_at)
        # self.imgs.append(demo_page.catch_screen(dpi=self.dpi))
        demo_page.switch_to_frame(demo_page.IFRAME)
        # 等待
        demo_page.wait_until_invisible(demo_page.SQUARE)
        # 手动截图
        # img = self.driver.get_screenshot_as_base64()
        self.imgs.append(demo_page.catch_screen(dpi=self.dpi))
        # 检查点
        self.assertEqual(False, demo_page.get(demo_page.SQUARE).is_displayed(), ds['msg'])

    def test_d(self):
        self._testMethodDoc = 'Edge'
        self.driver = edge()
        self.el = Element(self.driver, self.log)
        self.driver.get('https://www.baidu.com')
        self.imgs.append(self.el.catch_screen(dpi=self.dpi))


if __name__ == '__main__':
    # 用例不在这里运行
    # pass
    # unittest.main()
    fileBase = '../../a.html'  # 目录
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fileBase,
        title='{ Test Demo }',
        description='Test Demo',
        tester='ted',
        retry=0
    )
    # suit = unittest.TestLoader().loadTestsFromTestCase(Demo_Web)
    # print(suit.countTestCases())
    suit = unittest.TestSuite()
    tc = [Demo_Web('test_b_1')]
    suit.addTests(tc)
    runner.run(suit)

