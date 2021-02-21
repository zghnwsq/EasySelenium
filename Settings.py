# coding:utf-8

import os
# 浏览器驱动路径
DRIVER_PATH = {
    'chrome': r'C:\Soft\Driver\chromedriver.exe',
    'ie': r'C:\Soft\Driver\IEDriverServer.exe'
}
# 工程根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 自动化结果存储db
Sqlite = os.path.join(BASE_DIR, 'autotest.db')
# MyWeb db
# MyWebDb = r'D:\PythonProject\MyWeb\db.sqlite3'
MyWebDb = r'W:\myweb.sqlite3'
# 从节点参数(弃用)
Node1 = {
    'hub': '192.168.0.118:48000',
    'platform': 'WINDOWS',
    'version': '10',
    'user_dir': r'C:\Users\tedv\AppData\Local\Google\Chrome\User Data',
    'grid_dir': r'C:\Soft\selenium'
    }
# RPCServer
RPC_Server = '192.168.0.150'
RPC_Server_Port = 8888
# 上传文件路径
FILE_DIR = os.path.join(BASE_DIR, 'Upload')
# 显示器DPI缩放
DPI = 1.25
# 邮箱配置
MAIL = False
SENDER = 'tedwang@sina.cn'
SENDER_NAME = 'Ted'
SMTP_CODE = ''
RECEIVERS = ['tedwang@sina.cn', ]
# 更新脚本路径
UPDATE_BAT_DIR = os.path.join(BASE_DIR, 'Utils', 'RPC')


