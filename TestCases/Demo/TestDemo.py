# coding=utf-8
import os
import ddt
import unittest
# 设置
import Settings
# 工具类
from Utils.Browser.WebBrowser import chrome
from Utils.Browser.WebBrowser import edge
from Utils.ElementUtil.Element import Element
from Utils.DataBase.Oracle import Oracle
from Utils.Report.Log import *
from Utils.Excel.readXls import *
# SQL
from TestCases import SQL
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

    def tearDown(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
        print('end')

    @ddt.data(*data)
    def test_a(self, dt):
        self._testMethodDoc = '测试参数化'
        print(dt['a'])
        self.assertEqual('ok', dt['a'])

    @ddt.data(*read_data_by_sheet_name(os.path.join(Settings.BASE_DIR, r'DS\TestDemo.xlsx'), 'Sheet1'))
    def test_b(self, ds):
        # 测试描述
        self._testMethodDoc = ds['desc']
        self.imgs = []  # 截图存储列表
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.log.info('打开网页')
        self.driver.get(ds['url'])
        # 引用页面中的常量
        self.driver.switch_to.frame(self.el.get(DemoPage.IFRAME))
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        self.el.get(DemoPage.BUTTON, ds['button']).click()
        # 等待
        self.el.wait_until_invisible(DemoPage.SQUARE)
        # 手动截图
        img = self.driver.get_screenshot_as_base64()
        self.imgs.append(img)
        # 检查点
        self.assertEquals(False, self.el.get(DemoPage.SQUARE).is_displayed(), ds['msg'])

    def test_c(self):
        self._testMethodDoc = '数据库连接测试'
        db = Oracle('zbhxzcs', 'test!60', '200.168.168.60:1523/zbhxz')
        res = db.execute_block(SQL.TuiXiuPingPiaoChaXun, str, jylx='1')
        print(res)

    def test_d(self):
        self._testMethodDoc = 'Edge'
        self.imgs = []
        self.driver = edge()
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.driver.get('https://www.baidu.com')
        self.imgs.append(self.driver.get_screenshot_as_base64())


if __name__ == '__main__':
    # 用例不在这里运行
    pass
    # unittest.main()
    # fileBase = '../..'  # 目录
    # runner = HTMLTestReportCN.HTMLTestRunner(
    #     stream=fileBase,
    #     title='{ Test Demo }',
    #     description='Test Demo',
    #     tester='ted'
    # )
    # suit = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # runner.run(suit)
