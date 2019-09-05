# coding=utf-8
import sys
import os
# print(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
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
        title='{ 自动化测试示例 }',
        description='Test Demo',
        tester='ted',
        # verbosity=2,
        retry=0
    )
    # 加载用例方法一
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # # 加载用例方法二 使用ddt时，应加在方法后加：_数据源序号
    # suit2 = unittest.TestSuite()
    # tc = [TestDemo('test_a_1'), TestDemo('test_a_2')]
    # suit2.addTests(tc)

    # 手动管理用例优先级
    high = [TestDemo('test_c'),]
    middle = [TestDemo('test_a_2'), TestDemo('test_a_1'), ]
    low = [TestDemo('test_a_3'), ]
    suit3 = unittest.TestSuite()
    suit3.addTests(high)
    # suit3.addTests(middle)
    # suit3.addTests(low)

    # 运行
    runner.run(suit3)

