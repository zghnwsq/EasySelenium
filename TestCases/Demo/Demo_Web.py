# coding=utf-8
import logging
import os
import ddt
import unittest
# 设置
# from selenium.common.exceptions import WebDriverException
import Settings
# 工具类
from Utils.Browser.WebBrowser import init_chrome_browser
from Utils.Browser.WebBrowser import edge
from Utils.Browser.WebBrowser import close_down
from Utils.ElementUtil.Element import Element
# from Utils.DataBase.Oracle import Oracle
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.Report import HTMLTestRunnerThreading
from Utils.Report.Decorators import group_name, case_name
# from Utils.Report.Log import *
from Utils.Excel.readXls import *
# SQL
# from TestCases import SQL
# 页面元素
from Pages.DemoPage import DemoPage

data_source = os.path.join(Settings.BASE_DIR, 'DS', 'Demo_Web', 'TestDemo.xlsx')


@ddt.ddt
@group_name('-测试示例-')
class Demo_Web(unittest.TestCase):
    # 用例组名：__module__: __name__ : __doc__
    # __module__ = '*测试示例*'
    # __name__ = '-测试示例-'
    # __doc__ = '-测试示例-'
    log = None

    def setUp(self):
        print('begin')
        # self.imgs = []  # 截图存储列表
        # self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        # self.log = logger('info')
        # # self.el = Element(self.driver, self.log)
        # self.dpi = Settings.DPI
        init_chrome_browser(self)

    def tearDown(self):
        close_down(self)

    @ddt.data(*read_data_by_sheet_name(data_source, 'test_a'))
    @case_name('百度')
    def test_a(self, ds):
        demo_page = DemoPage(self.driver, imgs=self.imgs)
        # self._testMethodDoc = ds['desc']
        demo_page.logger.info('打开网页')
        demo_page.open_url(ds['url'])
        demo_page.get(demo_page.KW).send_keys(ds['kw'])
        # demo_page.get(demo_page.SEARCH).click()
        target = os.path.join(Settings.BASE_DIR, 'TestCases', 'Demo', 'baidu.png')
        click_at = demo_page.click_by_templ_matching(target, threshold=0.9, img_type='base64')
        self.imgs.append(click_at)
        former_hds = self.driver.window_handles
        # demo_page.get(demo_page.RES, ds['kw']).click()
        target = os.path.join(Settings.BASE_DIR, 'TestCases', 'Demo', 'testing.png')
        click_at = demo_page.click_by_templ_matching(target, threshold=0.9, img_type='base64')
        self.imgs.append(click_at)
        # self.imgs.append(demo_page.catch_screen(self.dpi))
        demo_page.wait_until_window_open_and_switch(former_hds)
        demo_page.scroll_into_view(demo_page.TEACHER)
        demo_page.get(demo_page.ROY)
        demo_page.catch_screen(self.dpi, imgs=self.imgs)
        # self.driver.find_element_by_xpath('').location_once_scrolled_into_view

    @ddt.data(*read_data_by_sheet_name(data_source, 'test_b'))
    @case_name('矩形淡出')
    def test_b(self, ds):
        demo_page = DemoPage(self.driver, imgs=self.imgs, logger=self.log)
        # 测试描述
        # self._testMethodDoc = ds['desc']
        demo_page.logger.info('打开网页')
        demo_page.open_url(ds['url'])
        # 引用页面中的常量
        # demo_page.switch_to_frame(demo_page.IFRAME)
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        # demo_page.click('xpath=//div[@id="djdjdj"]')
        # click_at = demo_page.click_by_templ_matching('./clickhere.png', threshold=0.9, img_type='base64')
        click_at = demo_page.click_by_featrue_matching('./clickhere.png', img_type='base64')
        demo_page.imgs.append({'img': click_at, 'desc': '点击处'})
        # self.imgs.append(demo_page.catch_screen(dpi=self.dpi))
        demo_page.switch_to_frame(demo_page.IFRAME)
        # 等待
        demo_page.wait_until_invisible(demo_page.SQUARE)
        # 手动截图
        # img = self.driver.get_screenshot_as_base64()
        demo_page.catch_screen(dpi=self.dpi, imgs=self.imgs, info='方块消失')
        # 检查点
        self.assertEqual(False, demo_page.get(demo_page.SQUARE).is_displayed(), ds['msg'])

    def test_d(self):
        self._testMethodDoc = 'Edge'
        self.driver = edge()
        self.el = Element(self.driver)
        self.driver.get('https://www.baidu.com')
        self.imgs.append(self.el.catch_screen(dpi=self.dpi))


if __name__ == '__main__':
    # 用例不在这里运行
    # pass
    # unittest.main()
    fileBase = '../../a.html'  # 目录
    runner = HTMLTestRunnerThreading.HTMLTestRunner(
        stream=fileBase,
        is_thread=True,
        threads=4,
        title='{ Test Demo }',
        description='Test Demo',
        tester='ted',
        retry=1
    )
    # suit = unittest.TestLoader().loadTestsFromTestCase(Demo_Web)
    # print(suit.countTestCases())
    suit = unittest.TestSuite()
    tc = [Demo_Web('test_b_1'), Demo_Web('test_b_2'), Demo_Web('test_b_3'), Demo_Web('test_b_4')]
    suit.addTests(tc)
    runner.run(suit)
