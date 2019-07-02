# coding=utf-8
import ddt
import unittest
# from Utils.Report import HTMLTestReportCN
from Utils.Browser.WebBrowser import chrome


data = [{'a': 'ok'}, {'a': 'ng'}]


@ddt.ddt
class TestDemo(unittest.TestCase):

    def setUp(self):
        print('begin')

    def tearDown(self):
        print('end')

    @ddt.data(*data)
    def test_a(self, dt):
        print(dt['a'])
        self.assertEqual('ok', dt['a'])

    def test_b(self):
        self.driver = chrome(path='D:\\Driver\\chromedriver.exe')
        self.driver.get('http://www.baidu.com')
        self.driver.find_element_by_id('adfdff')
        self.driver.close()
        self.driver.quit()


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

