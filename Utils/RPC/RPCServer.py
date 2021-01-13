import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import socket
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary
from socketserver import ThreadingMixIn
import traceback
# 引入测试相关
import Settings
from TestCases.Demo.TestDemo import TestDemo
from TestCases.Demo.TestTXYJS import TestTXYJS
from Utils.RPC.LoadSuite import load_suite
import TestCases.Demo.TestApiMZ as TestApiMZ
import Runner.RunByHtmlRunner as RunByHtmlRunner
import Runner.RunByPytest as RunByPytest
from Utils.DataBase.Sqlite import *
import Utils.FileUtil.Zip.Zip as ZipUtil
import time
import Utils.FileUtil.FileUtil as FileUtil


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


class RegisterFunctions:

    def __init__(self):
        pass

    @staticmethod
    def is_alive():
        return 'alive'

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

    @staticmethod
    def Demo_Web(kw):
        try:
            suite = load_suite(TestDemo, kw['mtd'], kw['rg'])
            # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Web', tester=kw['tester'] or '',
            #                           comment=kw['comment'] or '')
            res = RunByHtmlRunner.run_and_return(suite, test_group='Demo', suite_name='Web', tester=kw['tester'] or '',
                                                 comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def Demo_Api(kw):
        try:
            suite = load_suite(TestTXYJS, kw['mtd'], kw['rg'])
            # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Api', tester=kw['tester'] or '',
            #                           comment=kw['comment'] or '')
            res = RunByHtmlRunner.run_and_return(suite, test_group='Demo', suite_name='Api', tester=kw['tester'] or '',
                                                 comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def Demo_Api_GH1018Q1(kw):
        try:
            if kw['mtd'] == 'all':
                mtd = None
            else:
                mtd = kw['mtd']
            if 'rg' not in kw.keys():
                dsrange = None
            else:
                dsrange = kw['rg']
            res = RunByPytest.run_and_return('TestApi', py_file=TestApiMZ, py_class='TestMZ', py_method=mtd,
                                             dsrange=dsrange, title='Api_GH1018Q1', comment=kw['comment'],
                                             tester=kw['tester'])
        except Exception as e:
            print(e.args)
            msg = traceback.format_exc()
            return str(msg)[:256]
        return res

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
    ip_port = host_ip + ":" + str(Settings.RPC_Server_Port)
    # print(is_exists)
    if not is_exists:
        sql = r"insert into autotest_node(%s) values(%s)" % (
            r"'ip_port', 'tag', 'status'",
            "'" + ip_port + r"', '" + tag + "', 'on'")
        # print(sql)
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
    server = ThreadXMLRPCServer((host, Settings.RPC_Server_Port), allow_none=True)
    funcs = RegisterFunctions()
    print(funcs.methods())
    for method_name in funcs.methods():
        method = getattr(funcs, method_name)
        server.register_function(method, method_name)
    server.register_function(getattr(funcs, 'is_alive'), 'is_alive')
    server.register_function(getattr(funcs, 'get_report_file'), 'get_report_file')
    # server.register_function(funcs.web_demo, 'web_demo')
    print('listen for client')
    register_node(host, '虚拟机', funcs.methods())
    server.serve_forever()
