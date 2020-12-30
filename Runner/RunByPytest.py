# coding=utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import pytest
import time
from Utils.Runner.Sqlite import *


def run(report_dictory, py_file=None, py_class=None, py_method=None, marker=None, dsrange=None, title=None, tester=None,
        desc=None, comment=None):
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', report_dictory, now)
    cmd_list = []
    cmd_tmp = ''
    if py_file and py_class and py_method:
        cmd_tmp = '{0}::{1}::{2}'.format(py_file.__file__, py_class, py_method)
    elif py_file and py_class:
        cmd_tmp = '{0}::{1}'.format(py_file.__file__, py_class)
    elif py_file:
        cmd_tmp = '{0}'.format(py_file.__file__)
    else:
        pass
    cmd_list.append(cmd_tmp)
    if marker:
        cmd_list = cmd_list + ['-m', marker]
    if dsrange:
        cmd_list = cmd_list + ['--dsrange', dsrange]
    cmd_list.extend(['--alluredir', directory + '/json'])
    pytest.main(cmd_list)
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)
    insert_result(os.path.join(report_dictory, now), title or 'pytest+allure API Demo', tester=tester, desc=desc,
                  comment=comment)
    return 'finish'

