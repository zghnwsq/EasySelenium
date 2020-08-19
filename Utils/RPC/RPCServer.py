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
from Utils.RPC.LoadSuite import load_suite
from Runner.TestRun import run_test_demo
from Utils.DataBase.Sqlite import *


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


class RegisterFunctions:

    def __init__(self):
        pass

    @staticmethod
    def test_run_remote(mtd='all', rg=None, comment=None):
        try:
            suite = load_suite(TestDemo, mtd, rg)
            res = run_test_demo(suite, comment)
        except Exception as e:
            return str(e)[:256]
        return res

    def methods(self):
        return (list(filter(
            lambda m: not m.startswith("__") and not m.endswith("__") and not m.startswith("methods") and callable(
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
                sql = "select * from autotest_registerfunction where function = '%s'  and node = '%s'" % (mthd_name, ip_port)
                is_exists = db.execute(sql).fetchone()
                if not is_exists:
                    sql = r"insert into autotest_registerfunction('group', 'suite', 'function', 'node') values ('%s', '%s', '%s', '%s')" % (
                        'default', 'default', mthd_name, ip_port)
                    # print(sql)
                    db.execute(sql)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s in locals():
            s.close()
    return ip


if __name__ == '__main__':
    print(get_host_ip())
    host = get_host_ip()
    server = ThreadXMLRPCServer((host, Settings.RPC_Server_Port))
    funcs = RegisterFunctions()
    print(funcs.methods())
    for method_name in funcs.methods():
        method = getattr(funcs, method_name)
        server.register_function(method, method_name)
    # server.register_function(funcs.test_run_remote, 'test_run_remote')
    print('listen for client')
    register_node(host, '虚拟机', funcs.methods())
    server.serve_forever()
