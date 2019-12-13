# coding=utf-8
import sys
import os
import time
import unittest
# print(os.path.abspath(os.path.join(os.getcwd(), "..")))
import Settings
from Utils.Runner.Cmd import *
from Utils.Mail import *
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
    suit3 = unittest.TestSuite()
    if len(sys.argv) < 2:  # python   xxx.py
        suit3 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    if len(sys.argv) > 1:  # python  xxx.py   qlc  [1]
        method = sys.argv[1].strip()
        if 'all' in method:
            suit3 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
        else:
            if len(sys.argv) > 2:
                ds_range = sys.argv[2]
                li = get_range(ds_range)
                for i in li:
                    suit3.addTest(TestDemo('test_%s_%s' % (method, str(i))))
    else:
        raise Exception('Input args required: Test Method  [Data Source Range]')
    if len(sys.argv) > 3:  # python  xxx.py    qlc    111    调试
        comment = sys.argv[3].strip()
    else:
        comment = ''
    # 使用第三方报告插件
    fileBase = os.path.join(Settings.BASE_DIR, 'Report')  # 报告的目录
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    file_path = fileBase + '/' + time_stamp + '.html'
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=file_path,
        title='{ 自动化测试示例 }',
        description='Test Demo',
        tester='ted',
        # verbosity=2,
        retry=0  # 失败重跑次数
    )
    subject = runner.title
    body = '%s, %s' % (runner.title, runner.comment)
    # 加载用例方法一
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # # 加载用例方法二 使用ddt时，应加在方法名后加：_数据源序号
    # suit2 = unittest.TestSuite()
    # tc = [TestDemo('test_a_1'), TestDemo('test_a_2')]
    # suit2.addTests(tc)

    # 手动给用例优先级分组
    high = [TestDemo('test_b_1'), ]
    # middle = [TestDemo('test_a_2'), TestDemo('test_a_1'), ]
    # low = [TestDemo('test_a_3'), ]
    suit = unittest.TestSuite()
    suit.addTests(high)
    # suit.addTests(middle)
    # suit.addTests(low)

    # 自定义前缀 加载
    # loader = unittest.TestLoader()
    # loader.testMethodPrefix = 'test_a'
    # a = loader.loadTestsFromTestCase(TestDemo)

    # 运行
    runner.run(suit)

    # 发邮件
    send_mail(subject, body, file_path)

