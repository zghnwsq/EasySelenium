# coding=utf-8
import ddt
import unittest
# 设置
import Settings
# 工具类
from Utils.Browser.WebBrowser import chrome
from Utils.ElementUtil.Element import Element
from Utils.DataBase.Oracle import Oracle
from Utils.Report.Log import *
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

    def test_b(self):
        # 用例名： __class__._testMethodName : _testMethodDoc *verbosity>1时显示
        # self._testMethodName = '测试1'
        # 测试描述
        self._testMethodDoc = '自动化测试示例'
        self.imgs = []  # 截图存储列表
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.log.info('打开网页')
        self.driver.get('https://www.w3school.com.cn/tiy/t.asp?f=jquery_fadeout')
        # 引用页面中的常量
        self.driver.switch_to.frame(self.el.get(DemoPage.IFRAME))
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        self.el.get(DemoPage.BUTTON, '点击这里，使三个矩形淡出').click()
        # 等待
        self.el.wait_until_invisible(DemoPage.SQUARE)
        # 手动截图
        img = self.driver.get_screenshot_as_base64()
        self.imgs.append(img)
        # 检查点
        self.assertEquals(False, self.el.get(DemoPage.SQUARE).is_displayed(), '方块不应显示')

    def test_c(self):
        self._testMethodDoc = '数据库连接测试'
        db = Oracle('zbhxzcs', 'test!60', '200.168.168.60:1523/zbhxz')
        res = db.execute_block(SQL.TuiXiuPingPiaoChaXun, str, jylx='1')
        print(res)


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

