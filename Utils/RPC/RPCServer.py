import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
# 引入测试相关
import Settings
from TestCases.Demo.TestDemo import TestDemo
from Utils.DataBase.models.autotest import RunHis
from Utils.Mail.Mail import send_mail
from Utils.RPC.LoadSuite import load_suite
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def test_run_remote(mtd='all', rg=None, comment=None):
    suite = load_suite(TestDemo, mtd, rg)
    # 报告目录
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    op_path = os.path.join('TestDemo', time_stamp + '.html')
    file_path = os.path.join(Settings.BASE_DIR, 'Report', op_path)
    # 测试基本信息
    title = '{ 自动化测试示例 }'
    description = 'Test Demo'
    tester = 'ted'
    group = 'Demo'
    suite_name = 'Demo'
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
    res = runner.run(suite)
    print(res.result)
    # 结果写入sqlite
    if res:
        for detail in res.result:
            RunHis(group, suite_name, detail[1]._testMethodName or title, detail[1]._testMethodDoc or title, tester,
                   desc=description, comment=comment, report=op_path, result=str(detail[0])
                   ).save()
    # 发邮件
    if Settings.MAIL:
        # 邮件主题和内容
        subject = title
        body = '%s, %s' % (title, comment)
        send_mail(subject, body, file_path)
    return 'finish'


if __name__ == '__main__':
    server = ThreadXMLRPCServer((Settings.RPC_Server, Settings.RPC_Server_Port))
    server.register_function(test_run_remote, 'test_run_remote')
    print('listen for client')
    server.serve_forever()


