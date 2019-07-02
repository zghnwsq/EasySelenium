# coding=utf-8
from TestCases.Demo.TestDemo import TestDemo
import unittest
# from Utils.Report import HTMLTestReportCN
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN

'''
    测试用例组织与运行
    测试模块：
    测试描述：
'''

if __name__ == '__main__':
    # 使用第三方报告插件
    fileBase = '../Report'  # 报告的目录
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fileBase,
        title='{ Test Demo }',
        description='Test Demo',
        tester='ted',
        retry=0
    )
    # 加载用例方法一
    suit1 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # 加载用例方法二 使用ddt时，应加在方法后加：_数据源序号
    # suit2 = unittest.TestSuite()
    # tc = [TestDemo('test_something_1'), TestDemo('test_something_2')]
    # suit2.addTests(tc)
    # 运行
    runner.run(suit1)

