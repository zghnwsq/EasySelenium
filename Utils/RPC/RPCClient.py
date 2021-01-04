from xmlrpc.client import ServerProxy
import Settings
import os
import time
import Utils.Zip.zip as zip_util
from Utils.DataBase.models.autotest import RunHis

if __name__ == '__main__':
    server = ServerProxy("http://%s:%d" % (Settings.RPC_Server, Settings.RPC_Server_Port), allow_none=True)  # 初始化服务器
    try:
        # ConnectionRefusedError
        # is_alive = server.is_alive()
        # print(is_alive)
        # ret = server.Demo_Web({'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'})  # 调用函数1并传参
        # ret = server.Demo_Api({'mtd': 'auth_valid_case', 'rg': '1', 'comment': '', 'tester': 'TED'})  # 调用函数并传参
        ret = server.Demo_Api_GH1018Q1({'mtd': 'all', 'comment': None, 'tester': 'TED'})
        print(ret)
        # 压缩前文件名或文件夹
        if '.html' in ret['report']:
            file_name = ret['report'].split(os.sep)[-1]
        else:
            file_name = ''
        file_binary = server.get_report_file(ret['report']).data
        time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # 解压缩文件夹
        report_file_path = os.path.join(r'D:\PythonProject\MyWeb\Report', ret['test_group'], ret['test_suite'],
                                        time_stamp)
        # zip文件路径
        zip_file_path = report_file_path + '.zip'
        os.makedirs(report_file_path, exist_ok=True)
        # binary数据写入zip
        with open(zip_file_path, 'wb') as handle:
            handle.write(file_binary)
        # 解压缩zip到文件夹
        zip_util.unzip_file(zip_file_path, report_file_path)
        # 写入数据库的相对路径
        op_path = os.path.join(ret['test_group'], ret['test_suite'], time_stamp, file_name)
        # 写入MyWeb数据库
        for res in ret['result']:
            RunHis(res['group'], res['suite'], res['case'], res['title'], res['tester'], desc=res['desc'],
                   comment=res['comment'], report=op_path, result=res['result']
                   ).save()
    except TimeoutError as time_out:
        print(time_out)
    except ConnectionRefusedError as e:
        print(e)



