# coding=utf-8
import sys
import os
import unittest
# print(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from TestCases.Demo.TestDemo import TestDemo
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
        title='{ 自动化测试示例 }',
        description='Test Demo',
        tester='ted',
        # verbosity=2,
        retry=0  # 失败重跑次数
    )
    # 加载用例方法一
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # # 加载用例方法二 使用ddt时，应加在方法名后加：_数据源序号
    # suit2 = unittest.TestSuite()
    # tc = [TestDemo('test_a_1'), TestDemo('test_a_2')]
    # suit2.addTests(tc)

    # 手动给用例优先级分组
    high = [TestDemo('test_d'), ]
    # middle = [TestDemo('test_a_2'), TestDemo('test_a_1'), ]
    # low = [TestDemo('test_a_3'), ]
    suit = unittest.TestSuite()
    suit.addTests(high)
    # suit.addTests(middle)
    # suit.addTests(low)

    # 自定义前缀 加载
    loader = unittest.TestLoader()
    loader.testMethodPrefix = 'test_a'
    a = loader.loadTestsFromTestCase(TestDemo)

    # 运行
    runner.run(suit)

