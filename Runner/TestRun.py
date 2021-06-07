# coding=utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import time
from Settings import *
from Utils.Runner.Cmd import *
from TestCases.Demo.Demo_Web import Demo_Web
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.DataBase.models.autotest import *
from Utils.Mail.Mail import send_mail

'''
    测试用例组织与运行
    测试模块：
    测试描述：
    
    # 加载用例方法一
    # suit1 = unittest.TestLoader().loadTestsFromTestCase(Demo_Web)
    # # 加载用例方法二 使用ddt时，应加在方法名后加：_数据源序号
    # suit2 = unittest.TestSuite()
    # tc = [Demo_Web('test_a_1'), Demo_Web('test_a_2')]
    # suit2.addTests(tc)

    # 手动给用例优先级分组
    # high = [Demo_Web('test_b_1'), ]
    # middle = [Demo_Web('test_a_2'), Demo_Web('test_a_1'), ]
    # low = [Demo_Web('test_a_3'), ]
    # suit = unittest.TestSuite()
    # suit.addTests(high)
    # suit.addTests(middle)
    # suit.addTests(low)

    # 自定义前缀 加载
    # loader = unittest.TestLoader()
    # loader.testMethodPrefix = 'test_a'
    # a = loader.loadTestsFromTestCase(Demo_Web)
'''


def run_test_demo(suite, comment):
    suit3 = suite
    comment = comment

    # 报告目录
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    op_path = os.path.join('TestDemoTwo', time_stamp + '.html')
    file_path = os.path.join(Settings.BASE_DIR, 'Report', op_path)
    # 测试基本信息
    title = '{ 自动化测试示例 }'
    description = 'Test Demo'
    tester = 'ted'
    group = 'Demo'
    suite = 'Demo'
    # 使用第三方报告插件
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=file_path,
        title=title,
        description=description,
        tester=tester,
        verbosity=3,
        retry=0,  # 失败重跑次数
        comment=comment or ''
    )

    # 运行
    res = runner.run(suit3)
    print(res.result)

    # 结果写入sqlite
    if res:
        for detail in res.result:
            RunHis(group, suite, detail[1]._testMethodName or title, detail[1]._testMethodDoc or title, tester,
                   desc=description, comment=comment, report=op_path, result=str(detail[0])
                   ).save()

    # 发邮件
    if Settings.MAIL:
        # 邮件主题和内容
        subject = title
        body = '%s, %s' % (title, comment)
        send_mail(subject, body, file_path)

    return 'finished'


if __name__ == '__main__':
    # 命令行运行，根据参数加载用例
    test_suite = cmd_run(Demo_Web)
    run_test_demo(test_suite[0], test_suite[1])
    # suit3 = res[0]
    # comment = res[1]
    #
    # # 报告目录
    # time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    # op_path = os.path.join('Demo_Web', time_stamp + '.html')
    # file_path = os.path.join(Settings.BASE_DIR, 'Report', op_path)
    # # 测试基本信息
    # title = '{ 自动化测试示例 }'
    # description = 'Test Demo'
    # tester = 'ted'
    # group = 'Demo'
    # suite = 'Demo'
    # # 使用第三方报告插件
    # runner = HTMLTestReportCN.HTMLTestRunner(
    #     stream=file_path,
    #     title=title,
    #     description=description,
    #     tester=tester,
    #     verbosity=3,
    #     retry=0,  # 失败重跑次数
    #     comment=comment or ''
    # )
    #
    # # 运行
    # res = runner.run(suit3)
    # print(res.result)
    #
    # # 结果写入sqlite
    # if res:
    #     for detail in res.result:
    #         RunHis(group, suite, detail[1]._testMethodName or title, detail[1]._testMethodDoc or title, tester,
    #                desc=description, comment=comment, report=op_path, result=str(detail[0])
    #                ).save()
    #
    # # 发邮件
    # if Settings.MAIL:
    #     # 邮件主题和内容
    #     subject = title
    #     body = '%s, %s' % (title, comment)
    #     send_mail(subject, body, file_path)
