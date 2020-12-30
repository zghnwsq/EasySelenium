# coding=utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import time
from Settings import *
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.DataBase.models.autotest import *
from Utils.Mail.Mail import send_mail


def run(test_suite, test_group: str = 'Demo', suite_name: str = 'Demo', retry: int = 0, tester: str = '',
        title: str = '{ 自动化测试报告 }', description: str = '', comment=None):
    suit3 = test_suite
    comment = comment

    # 报告目录
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not os.path.exists(os.path.join(Settings.BASE_DIR, 'Report', test_group)):
        os.mkdir(os.path.join(Settings.BASE_DIR, 'Report', test_group))
    if not os.path.exists(os.path.join(Settings.BASE_DIR, 'Report', test_group, suite_name)):
        os.mkdir(os.path.join(Settings.BASE_DIR, 'Report', test_group, suite_name))
    op_path = os.path.join(test_group, suite_name, time_stamp + '.html')
    file_path = os.path.join(Settings.BASE_DIR, 'Report', op_path)
    # 测试基本信息
    title = title
    description = description
    tester = tester
    group = test_group
    test_suite = suite_name
    # 使用第三方报告插件
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=file_path,
        title=title,
        description=description,
        tester=tester,
        verbosity=3,
        retry=retry,  # 失败重跑次数
        comment=comment or ''
    )

    # 运行
    res = runner.run(suit3)
    print(res.result)

    # 结果写入sqlite
    if res:
        for detail in res.result:
            RunHis(group, test_suite, detail[1]._testMethodName or title, detail[1]._testMethodDoc or title, tester,
                   desc=description, comment=comment, report=op_path, result=str(detail[0])
                   ).save()

    # 发邮件
    if Settings.MAIL:
        # 邮件主题和内容
        subject = title
        body = '%s, %s' % (title, comment)
        send_mail(subject, body, file_path)

    return 'finished'
