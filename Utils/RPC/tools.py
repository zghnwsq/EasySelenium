import os
import socket
import warnings
import requests
from requests.auth import HTTPBasicAuth
import Settings
from Utils.DataBase.MySql import *


def register_node(host_ip, tag, func: dict = None):
    """
       向数据库注册节点或更新节点状态, 并将RPC Server注册的测试方法插入数据库
       *数据库由sqlite改为mysql
    :param host_ip: 节点ip
    :param tag: 标签
    :param func: 字典{测试集注册名:tests列表(","连接的字符串)}, 即RPC Client调用的suite_name列表和可供选择的mtd
    :return: None
    """
    warnings.warn("register_node is deprecated, replace it with register_node_to_server", DeprecationWarning)
    # db = Sqlite(Settings.MyWebDb)
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PWD')
    db = Mysql(Settings.MyWebDb, Settings.MyWebDbPort, user, pwd, Settings.MyWebDbName)
    db.connect()
    sql = "select * from autotest_node where ip_port like '%s'" % (host_ip + r"%")
    is_exists = db.fetchall(sql)
    ip_port = str(host_ip) + ":" + str(Settings.RPC_Server_Port)
    if not is_exists:
        sql = r"insert into autotest_node(%s) values(%s)" % (
            r"ip_port, tag, status",
            "'" + ip_port + r"', '" + tag + "', 'on'")
        db.execute(sql)
    else:
        sql = r"update autotest_node set status='on' where ip_port like '%s'" % (host_ip + r"%")
        db.execute(sql)
    if func:
        for mthd_name in func.keys():
            if mthd_name.strip():
                sql = "select * from autotest_registerfunction where func = '%s'  and node = '%s'" % (
                    mthd_name, ip_port)
                is_exists = db.fetchall(sql)
                if not is_exists:
                    split_mthd_name = mthd_name.split('_')
                    group = split_mthd_name[0]
                    suite_name = split_mthd_name[1]
                    sql = r"insert into autotest_registerfunction(`group`, suite, func, node, tests) values ('%s', '%s', '%s', '%s', '%s')" % (
                        group, suite_name, mthd_name, ip_port, func[mthd_name])
                    # print(sql)
                else:
                    sql = r"update autotest_registerfunction set tests='%s' where func = '%s'  and node = '%s'" % (
                        func[mthd_name], mthd_name, ip_port)
                db.execute(sql)
    db.close()


def register_node_to_server(host_ip, tag, func: dict = None):
    session = requests.session()
    url = f'http://{Settings.MyWebService}:{Settings.MyWebServicePort}/autotest/node/register/'
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(Settings.NodeUser, Settings.NodePwd)
    body = {'type': 'update', 'host_ip': f'{host_ip}:{Settings.RPC_Server_Port}', 'tag': tag, 'func': func}
    response = session.post(url, headers=headers, auth=auth, json=body)
    session.close()
    return response.text


def update_node_off(host_ip):
    """
       更新节点状态为off
    :param host_ip: 节点ip
    :return: None
    """
    warnings.warn("update_node_off is deprecated, replace it with update_node_off_to_server", DeprecationWarning)
    # db = Sqlite(Settings.MyWebDb)
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PWD')
    db = Mysql(Settings.MyWebDb, Settings.MyWebDbPort, user, pwd, Settings.MyWebDbName)
    db.connect()
    sql = r"update autotest_node set status='off' where ip_port like '%s'" % (host_ip + r"%")
    db.execute(sql)
    db.close()


def update_node_off_to_server(host_ip):
    session = requests.session()
    url = f'http://{Settings.MyWebService}:{Settings.MyWebServicePort}/autotest/node/register/'
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(Settings.NodeUser, Settings.NodePwd)
    body = {'type': 'node_off', 'host_ip': f'{host_ip}:{Settings.RPC_Server_Port}', 'tag': '', 'func': ''}
    response = session.post(url, headers=headers, auth=auth, json=body)
    session.close()
    return response.text


def get_host_ip():
    """
       获取本节点ip地址
    :return: 本节点ip地址
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s:
            s.close()
    return ip
