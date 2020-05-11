# coding:utf-8

import os

DRIVER_PATH = {
    'chrome': r'C:\Soft\Driver\chromedriver.exe',
    'ie': r'C:\Soft\Driver\IEDriverServer.exe'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Sqlite = os.path.join(BASE_DIR, 'autotest.db')

Node1 = {
    'hub': '192.168.0.118:48000',
    'platform': 'WINDOWS',
    'version': '10',
    'user_dir': r'C:\Users\tedv\AppData\Local\Google\Chrome\User Data',
    'grid_dir': r'C:\Soft\selenium'
    }

FILE_DIR = os.path.join(BASE_DIR, 'Upload')

MAIL = False
SENDER = 'tedwang@sina.cn'
SENDER_NAME = 'Ted'
SMTP_CODE = ''
RECEIVERS = ['tedwang@sina.cn', ]


