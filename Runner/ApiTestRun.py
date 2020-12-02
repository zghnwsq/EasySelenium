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


def run_api_test_demo(suite, comment):
    suit3 = suite
    comment = comment

    # 报告目录
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    op_path = os.path.join('TestApi', time_stamp + '.html')
    file_path = os.path.join(Settings.BASE_DIR, 'Report', op_path)
    # 测试基本信息
    title = '{ 自动化测试示例 }'
    description = 'Test Api'
    tester = 'ted'
    group = 'Demo'
    suite = 'API Demo'
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
