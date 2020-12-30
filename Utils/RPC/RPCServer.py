# import time
import os
import socket
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
# 引入测试相关
import Settings
from TestCases.Demo.TestDemo import TestDemo
from TestCases.Demo.TestApi import TestApi
from Utils.RPC.LoadSuite import load_suite
import TestCases.Demo.TestApiMZ as TestApiMZ
# from Runner.TestRun import run_test_demo
# from Runner.ApiTestRun import run_api_test_demo
import Runner.RunByHtmlRunner as RunByHtmlRunner
import Runner.RunByPytest as RunByPytest
from Utils.DataBase.Sqlite import *


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


class RegisterFunctions:

    def __init__(self):
        pass

    @staticmethod
    def is_alive():
        return 'alive'

    @staticmethod
    def Demo_Web(kw):
        try:
            suite = load_suite(TestDemo, kw['mtd'], kw['rg'])
            res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Web', tester=kw['tester'] or '',
                                      comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def Demo_Api(kw):
        try:
            suite = load_suite(TestApi, kw['mtd'], kw['rg'])
            res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Api', tester=kw['tester'] or '',
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
            res = RunByPytest.run('TestApi', py_file=TestApiMZ, py_class='TestAPI', py_method=mtd, dsrange=kw['rg'],
                                  title='Api_GH1018Q1', comment=kw['comment'], tester=kw['tester'])
        except Exception as e:
            return str(e)[:256]
        return res

    def methods(self):
        return (list(filter(
            lambda m: not m.startswith("__") and not m.endswith("__") and not m.startswith(
                "is_alive") and not m.startswith("methods") and callable(getattr(self, m)), dir(self))
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
    # server.register_function(funcs.web_demo, 'web_demo')
    print('listen for client')
    register_node(host, '虚拟机', funcs.methods())
    server.serve_forever()
