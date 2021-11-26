# coding:utf-8

import os
import win32con
import win32gui
import win32print

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
# MyWebDb = r'W:\myweb.sqlite3'
MyWebDb = '8.136.125.0'  # 8.136.125.0
MyWebDbPort = 9306
MyWebDbName = 'myweb'
# MyWeb服务器
MyWebService = '192.168,0,150'
MyWebServicePort = 8000
NodeUser = 'node'
NodePwd = 'xkj2ei9dx9q0s9jfjkehvn'
# 从节点参数(弃用)
# Node1 = {
#     'hub': '192.168.0.118:48000',
#     'platform': 'WINDOWS',
#     'version': '10',
#     'user_dir': r'C:\Users\tedv\AppData\Local\Google\Chrome\User Data',
#     'grid_dir': r'C:\Soft\selenium'
#     }
# RPCServer
# RPC_Server = '192.168.0.150' # 废弃 自动获取
RPC_Server_Port = 8888
# 上传文件路径
FILE_DIR = os.path.join(BASE_DIR, 'Upload')
# 显示器DPI缩放
# DPI = 1.25
# DPI改自动获取
hDC = win32gui.GetDC(0)
DEFAULT_DPI = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)/win32print.GetDeviceCaps(hDC, win32con.HORZRES)
ADVANCED_DPI = win32print.GetDeviceCaps(hDC, win32con.LOGPIXELSX)/0.96/100
DPI = DEFAULT_DPI if ADVANCED_DPI == 1.0 else ADVANCED_DPI
# 邮箱配置
MAIL = False
SENDER = 'tedwang@sina.cn'
SENDER_NAME = 'Ted'
SMTP_CODE = ''
RECEIVERS = ['tedwang@sina.cn', ]
# 更新脚本路径
UPDATE_BAT_DIR = os.path.join(BASE_DIR, 'Utils', 'RPC')
# 注册测试集配置文件
RPC_SERVER_SUITES = ['register.yaml']
# yaml
# - MODULE: 'TestCases.Demo.Demo_Web' py文件模块
# CLASS: 'Demo_Web' 类名
# NAME: 'Demo_Web' RPC调用名, '_'分割, 用例组_用例集_用例子集
#                  unittest用例按 用例组/用例集 创建报告目录, 数据源按NAME查找目录
#                  pytest用例 按NAME创建报告目录, 数据源按NAME查找目录
# TYPE: 'unittest' 测试框架类型
# DS_FILE_NAME: 'TestDemo.xlsx' 数据源文件名
