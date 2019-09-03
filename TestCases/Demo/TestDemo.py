# coding=utf-8
import ddt
import unittest
import Settings
# from Utils.Report import HTMLTestReportCN
from Utils.Browser.WebBrowser import chrome
from Utils.ElementUtil.Element import Element
# from Pages.TB import AppDetailOrgEdit


data = [{'a': 'ok'}, {'a': 'ng'}, {'a': 'ok'}]


@ddt.ddt
class TestDemo(unittest.TestCase):

    def setUp(self):
        print('begin')
        self.imgs = []
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.el = Element(self.driver)

    def tearDown(self):
        # if self.driver:
        #     self.driver.close()
        #     self.driver.quit()
        print('end')

    @ddt.data(*data)
    def test_a(self, dt):
        print(dt['a'])
        self.assertEqual('ok', dt['a'])

    def test_b(self):
        self.driver.get('http://www.baidu.com')
        self.el.get('id=${kw}', val='kw').send_keys('123')
        img = self.driver.get_screenshot_as_base64()
        self.imgs.append(img)
        # self.driver.find_element_by_id('adfdff')
        # self.driver.close()
        # self.driver.quit()


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

