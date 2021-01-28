# coding:utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import socket
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary
from socketserver import ThreadingMixIn
import threading
# 引入测试相关
import Settings
from Utils.DataBase.Sqlite import *
import Utils.FileUtil.Zip.Zip as ZipUtil
import time
import Utils.FileUtil.FileUtil as FileUtil
from Utils.RPC.TestSuiteFunctions import *


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


class NodeService(threading.Thread):

    def __init__(self, ip, port, test_suite_obj):
        super().__init__()
        self.ip = ip
        self.port = port
        self.test_suite_obj = test_suite_obj
        self.server = ThreadXMLRPCServer((self.ip, self.port), allow_none=True)
        self.server.register_function(getattr(self, 'is_on'), 'is_alive')
        self.server.register_function(getattr(self, 'start_server'), 'start_server')
        self.server.register_function(getattr(self, 'stop_server'), 'stop_server')
        self.server.register_function(getattr(self, 'update_node'), 'update_node')
        self.server.register_instance(test_suite_obj)

    @staticmethod
    def is_on():
        return 'alive'

    def update_node(self):
        self.stop_server()
        UpdateNodeThread().start()
        # self.server.server_close()
        return 'Node Service Starting...'

    def start_server(self):
        register_node(self.ip, os.environ.get("COMPUTERNAME"), self.test_suite_obj.methods())
        self.server.serve_forever()
        print('success')
        return 'running'

    def stop_server(self):
        ip_port = f'{self.ip}:{self.port}'
        update_node_off(ip_port)
        self.server.shutdown()
        ClearNodeThread().start()
        # self.server.server_close()
        return 'stopped'

    def run(self):
        self.start_server()


class UpdateNodeThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        res = os.popen(
            f'cd {Settings.UPDATE_BAT_DIR} && start "" cmd  /k call update.bat && taskkill /F /pid {os.getpid()}').read()
        print(res)


class ClearNodeThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        res = os.popen(
            f'cd {Settings.UPDATE_BAT_DIR} && taskkill /F /FI "WINDOWTITLE eq Node Server..."').read()
        print(res)


class RegisterFunctions:

    def __init__(self):
        pass

    @staticmethod
    def get_report_file(file_path):
        # 新建压缩包路径
        zip_path = os.path.abspath(os.path.join(file_path, '..', 'zip'))
        if not os.path.exists(zip_path):
            os.mkdir(zip_path)
        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            if '.html' in file_path:
                ZipUtil.zip_file(file_path, os.path.join(zip_path, f'{timestamp}.zip'))
                FileUtil.remove(file_path)
                with open(os.path.join(zip_path, f'{timestamp}.zip'), 'rb') as report:
                    bin_data = Binary(report.read())
                FileUtil.remove(zip_path)
            else:
                ZipUtil.zip_dir(file_path, os.path.join(zip_path, f'{timestamp}.zip'))
                FileUtil.remove(file_path)
                with open(os.path.join(zip_path, f'{timestamp}.zip'), 'rb') as report:
                    bin_data = Binary(report.read())
                FileUtil.remove(os.path.abspath(os.path.join(file_path, '..')))
            return bin_data
        else:
            return None

    def methods(self):
        return (list(filter(
            lambda m: not m.startswith("__") and not m.endswith("__") and not m.startswith(
                "is_alive") and not m.startswith("methods") and not m.startswith("get_report") and callable(
                getattr(self, m)), dir(self))
        ))


def register_node(host_ip, tag, func=None):
    db = Sqlite(Settings.MyWebDb)
    db.connect()
    sql = "select * from autotest_node where ip_port like '%s'" % (host_ip + r"%")
    is_exists = db.execute(sql).fetchone()
    ip_port = str(host_ip) + ":" + str(Settings.RPC_Server_Port)
    # print(is_exists)
    if not is_exists:
        sql = r"insert into autotest_node(%s) values(%s)" % (
            r"'ip_port', 'tag', 'status'",
            "'" + ip_port + r"', '" + tag + "', 'on'")
        db.execute(sql)
    else:
        sql = r"update autotest_node set status='on' where ip_port like '%s'" % (host_ip + r"%")
        db.execute(sql)
    if func:
        for mthd_name in func:
            if mthd_name.strip():
                sql = "select * from autotest_registerfunction where function = '%s'  and node = '%s'" % (
                    mthd_name, ip_port)
                is_exists = db.execute(sql).fetchone()
                if not is_exists:
                    split_mthd_name = mthd_name.split('_')
                    group = split_mthd_name[0]
                    suite_name = split_mthd_name[1]
                    sql = r"insert into autotest_registerfunction('group', 'suite', 'function', 'node') values ('%s', '%s', '%s', '%s')" % (
                        group, suite_name, mthd_name, ip_port)
                    # print(sql)
                    db.execute(sql)


def update_node_off(host_ip):
    db = Sqlite(Settings.MyWebDb)
    db.connect()
    sql = r"update autotest_node set status='off' where ip_port like '%s'" % (host_ip + r"%")
    db.execute(sql)


def get_host_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s:
            s.close()
    return ip


if __name__ == '__main__':
    print(get_host_ip())
    host = get_host_ip()
    # server = ThreadXMLRPCServer((host, Settings.RPC_Server_Port), allow_none=True)
    funcs = TestSuiteFunctions()
    print(funcs.methods())
    # for method_name in funcs.methods():
    #     method = getattr(funcs, method_name)
    #     server.register_function(method, method_name)
    # server.register_function(getattr(funcs, 'is_alive'), 'is_alive')
    # server.register_function(getattr(funcs, 'get_report_file'), 'get_report_file')
    # print('listen for client')
    # register_node(host, os.environ.get("COMPUTERNAME"), funcs.methods())
    # server.serve_forever()
    node_service = NodeService(host, Settings.RPC_Server_Port, funcs)
    node_service.start()
    # time.sleep(30)
    # node_service.stop_server()
    # node_service.join()

