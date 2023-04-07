# coding:utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import Settings
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
# 引入测试相关
from RPC.tools import get_host_ip, register_node_to_server, update_node_off_to_server
from RPC.TestSuiteFunctions import TestSuiteInstance


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """
       多线程的SimpleXMLRPCServer
    """
    pass


class NodeService(threading.Thread):

    def __init__(self, ip, port, test_suite_obj):
        """
           执行节点服务,多线程
        :param ip: 节点ip
        :param port: 节点端口
        :param test_suite_obj: 注册测试套件对象
        """
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
        """
           另起线程，更新节点
        :return: 提示
        """
        self.stop_server()
        UpdateNodeThread().start()
        # self.server.server_close()
        return 'Node Service Starting...'

    def start_server(self):
        """
           注册节点，启动节点服务
        :return: 提示
        """
        # register_node(self.ip, os.environ.get("COMPUTERNAME"), self.test_suite_obj.methods())
        register_node_to_server(self.ip, os.environ.get("COMPUTERNAME"), self.test_suite_obj.methods())
        self.server.serve_forever()
        print('success')
        return 'running'

    def stop_server(self):
        """
           另起线程停止节点，更新节点状态
        :return: 提示
        """
        ip_port = f'{self.ip}:{self.port}'
        # update_node_off(ip_port)
        update_node_off_to_server(ip_port)
        self.server.shutdown()
        ClearNodeThread().start()
        # self.server.server_close()
        return 'stopped'

    def run(self):
        """
           启动节点服务线程
        :return: None
        """
        self.start_server()


class UpdateNodeThread(threading.Thread):

    def __init__(self):
        """
           更新节点线程
        """
        super().__init__()

    def run(self):
        """
           调用bat脚本更新节点并重启节点
        :return: None
        """
        res = os.popen(
            f'cd {Settings.UPDATE_BAT_DIR} && start "" cmd  /k call update.bat && taskkill /F /pid {os.getpid()}').read()
        print(res)


class ClearNodeThread(threading.Thread):

    def __init__(self):
        """
           清理节点线程
        """
        super().__init__()

    def run(self):
        """
           调用bat脚本清理节点服务窗口
        :return: None
        """
        res = os.popen(
            f'cd {Settings.UPDATE_BAT_DIR} && taskkill /F /FI "WINDOWTITLE eq Node Server..."').read()
        print(res)


if __name__ == '__main__':
    print(get_host_ip())
    host = get_host_ip()
    funcs = TestSuiteInstance()
    print(funcs.methods())
    node_service = NodeService(host, Settings.RPC_Server_Port, funcs)
    node_service.start()

