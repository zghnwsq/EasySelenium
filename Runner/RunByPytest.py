# coding=utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import pytest
import time
from Utils.Runner.Sqlite import *


def __prepare_cmd(py_file, py_class, py_method, marker=None, dsrange=None):
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
    # cmd_list.extend(['--alluredir', directory + '/json'])
    return cmd_list


def run(report_dictory, py_file=None, py_class=None, py_method=None, marker=None, dsrange=None, title=None, tester=None,
        desc=None, comment=None):
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', report_dictory, now)
    cmd_list = __prepare_cmd(py_file, py_class, py_method, marker=marker, dsrange=dsrange)
    cmd_list.extend(['--alluredir', directory + '/json'])
    pytest.main(cmd_list)
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)
    insert_result(os.path.join(report_dictory, now), title or 'pytest+allure API Demo', tester=tester, desc=desc,
                  comment=comment)
    return 'finish'


def run_and_return(report_dictory, py_file=None, py_class=None, py_method=None, marker=None, dsrange=None, title=None,
                   tester=None, desc=None, comment=None):
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', report_dictory, now)
    cmd_list = __prepare_cmd(py_file, py_class, py_method, marker=marker, dsrange=dsrange)
    cmd_list.extend(['--alluredir', directory + '/json'])
    pytest.main(cmd_list)
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)
    # insert_result(os.path.join(report_dictory, now), title or 'pytest+allure API Demo', tester=tester, desc=desc,
    #               comment=comment)
    res_dir = os.path.join(report_dictory, now)
    case_result = []
    test_group = ''
    suite_name = ''
    for root, dirs, files in os.walk(os.path.join(Settings.BASE_DIR, 'Report', res_dir)):
        for filename in files:
            if 'result.json' in filename:
                with open(os.path.join(root, filename), encoding='UTF-8') as result:
                    jres = json.loads(result.read(), encoding='UTF-8')
                    test_case = jres['name']
                    if 'pass' in jres['status']:
                        result = '0'
                    elif 'skiped' in jres['status']:
                        result = '3'
                    else:
                        result = '1'
                    group = jres['labels'][1]['value']
                    test_group = group
                    suite = jres['labels'][2]['value']
                    suite_name = suite
                    host = jres['labels'][3]['value']
                    report = os.path.join(res_dir, 'html')
                    finish_time = str(jres['stop'])[:10]
                    case_result.append(
                        {'group': group, 'suite': suite, 'case': test_case, 'title': title, 'tester': tester or host,
                         'desc': desc, 'comment': comment, 'report': report, 'result': result,
                         'finish_time': finish_time})
    result = {'test_group': test_group, 'test_suite': suite_name, 'title': title, 'tester': tester, 'description': desc,
              'comment': comment, 'report': os.path.join(directory, 'html'), 'result': case_result}
    return result


