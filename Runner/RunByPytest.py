# coding=utf-8
# import sys
import io
import os
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
import sys
from Runner.TestResult import CaseResult, SummaryResult
from Utils.Constant.Constant import ResultCode
from Utils.Runner.LoadSuite import update_suite_count_to_server
from Utils.Mail.Mail import send_mail
import warnings
import pytest
import time
import re
import Settings
import json
from Utils.DataBase.models.autotest import RunHis


def __prepare_cmd(py_file, py_class, py_method, marker=None, dsrange=None):
    cmd_list = []
    cmd_tmp = ''
    if py_file and py_class and py_method:
        cmd_tmp = '{0}::{1}::{2}'.format(py_file.__file__, py_class, 'test_' + py_method)  # 2021.5.26自动添加test_头
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


def run(py_file=None, py_class=None, py_method=None, marker=None, dsrange=None, title=None, tester=None,
        desc=None, comment=None):
    warnings.warn("run is deprecated, replace it with run_and_return", DeprecationWarning)
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    report_dictory = py_file.Test_Group
    directory = os.path.join(Settings.BASE_DIR, 'Report', report_dictory, now)
    cmd_list = __prepare_cmd(py_file, py_class, py_method, marker=marker, dsrange=dsrange)
    cmd_list.extend(['--alluredir', directory + '/json'])
    pytest.main(cmd_list)
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)
    insert_pytest_result(os.path.join(report_dictory, now), title or 'pytest+allure API Demo', tester=tester, desc=desc,
                         comment=comment)
    return 'finish'


def insert_pytest_result(res_dir, title, tester=None, desc=None, comment=None):
    warnings.warn("insert_pytest_result is deprecated, replace it with run_and_return", DeprecationWarning)
    for root, dirs, files in os.walk(os.path.join(Settings.BASE_DIR, 'Report', res_dir)):
        for filename in files:
            if 'result.json' in str(filename):
                with open(os.path.join(root, filename), encoding='UTF-8') as result:
                    jres = json.loads(result.read(), encoding='UTF-8')
                    test_case = jres['name']
                    if 'pass' in jres['status']:
                        result = ResultCode.PASS
                    elif 'skip' in jres['status']:
                        result = ResultCode.SKIP
                    else:
                        result = ResultCode.FAIL
                    group = jres['labels'][1]['value']
                    suite = jres['labels'][2]['value']
                    host = jres['labels'][3]['value']
                    report = os.path.join(res_dir, 'html')
                    finish_time = str(jres['stop'])[:10]
                    RunHis(group, suite, test_case, title, tester or host,
                           desc=desc, comment=comment, report=report, result=result, create_time=finish_time
                           ).save_with_time()


def get_method_and_dsrange(kw):
    if kw['mtd'] == 'all':
        mtd = None
    else:
        mtd = kw['mtd']
    if 'rg' not in kw.keys():
        dsrange = None
    else:
        dsrange = kw['rg']
    return mtd, dsrange


def collect_case_count(py_file=None, name=None):
    out = sys.stdout
    redirect = io.StringIO()
    sys.stdout = redirect
    pytest.main(['--collect-only', py_file.__file__])
    res = sys.stdout.getvalue()
    sys.stdout = out
    match = re.search('collected\\s*?(\\d+?)\\s*?items', res)
    case_count = int(match.group(1)) if match else 0
    # if hasattr(py_file, 'Case_Count'):
    #     case_count = py_file.Case_Count
    # else:
    #     pass
    name = name.split('_')
    test_group = name[0]
    test_suite = '_'.join((name[1], name[2]))
    update_suite_count_to_server(test_group, test_suite, case_count)


def read_pytest_result(res_json_dir, title):
    case_result = []
    # ../EasySelenium/Report/suite_meta['NAME']/%Y%m%d_%H%M%S/json/
    for root, dirs, files in os.walk(res_json_dir):
        for filename in files:
            if 'result.json' in str(filename):
                with open(os.path.join(root, filename), encoding='UTF-8') as result_file:
                    jres = json.loads(result_file.read(), encoding='UTF-8')
                    test_case = jres['name']
                    if 'pass' in jres['status']:
                        result = ResultCode.PASS
                    elif 'skip' in jres['status']:
                        # pytest skip用作跳过非dsrange选择场景,暂不统计进结果
                        continue
                        # result = ResultCode.SKIP
                    else:
                        result = ResultCode.FAIL
                    # host = jres['labels'][3]['value']
                    # report = html_dir
                    finish_time = str(jres['stop'])[:10]
                    param = jres['parameters'][0]['value']
                    # desc参数用作用例标题
                    if 'desc' in param:
                        span = re.findall(r'desc\':[\s]*[\'\"](.+?)[\'\"],', param)[0]
                        title = span or title
                    case_result.append(
                        CaseResult(test_case, title, result,
                                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(finish_time)))).values
                    )
    return case_result


def run_and_return(py_file=None, py_class=None, py_method=None, marker=None, dsrange=None, title='',
                   tester=None, desc=None, comment=None, report_dictory='None', suite_meta=None):
    """
       执行pytest用例组，生成html报告，发送邮件，并返回json结果
    :param report_dictory: 报告存放文件夹名
    :param py_file: 测试用例所在py文件
    :param py_class: 测试用例所在类
    :param py_method: 指定执行的测试方法
    :param marker: pytest marker参数
    :param dsrange: 选择数据源范围
    :param title: 报告标题
    :param tester: 测试人
    :param desc: 描述
    :param comment: 备注
    :param suite_meta: 测试集信息，来自yaml配置文件
    :return: json格式结果 ：{'group_name': group_name, 'test_suite': suite_name, 'title': title, 'tester': tester, 'description': desc,
              'comment': comment, 'report': os.path.join(directory, 'html'), 'result': case_result}
    """
    # run by pytest
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    if suite_meta:
        if py_class is None:
            py_class = suite_meta['CLASS']
        if not title:
            title = suite_meta['NAME']
        if report_dictory == 'None':
            report_dictory = suite_meta['NAME']
    test_group = suite_meta['NAME'].split('_')[0]
    suite_name = '_'.join(suite_meta['NAME'].split('_')[1:])
    # report_dictory = py_file.Test_Group
    # directory: ../EasySelenium/Report/suite_meta['NAME']/%Y%m%d_%H%M%S/
    directory = os.path.join(Settings.BASE_DIR, 'Report', report_dictory, now)
    cmd_list = __prepare_cmd(py_file, py_class, py_method, marker=marker, dsrange=dsrange)
    # ../EasySelenium/Report/suite_meta['NAME']/%Y%m%d_%H%M%S/json/
    json_dir = os.path.join(directory, 'json')
    cmd_list.extend(['--alluredir', json_dir])
    os.makedirs(json_dir)
    print(cmd_list)
    # 运行时所有异常应当捕获, 并返回服务器错误信息
    try:
        pytest.main(cmd_list)
        # generate report by allure
        # ../EasySelenium/Report/suite_meta['NAME']/%Y%m%d_%H%M%S/html/
        html_dir = os.path.join(directory, 'html')
        os.makedirs(html_dir)
        allure_cmd = f'allure generate -o  {html_dir}  {json_dir}'
        os.system(allure_cmd)
        # read json result and insert into database
        case_result = read_pytest_result(json_dir, title)
        # ../EasySelenium/Report/suite_meta['NAME']/%Y%m%d_%H%M%S/html/
        result = SummaryResult(test_group, suite_name, title, tester, desc, comment, os.path.join(directory, 'html'),
                               case_result).values
    except Exception:
        result = SummaryResult(test_group, suite_name, title, tester, desc, comment, os.path.join(directory, 'html'),
                               []).values
    # insert_result(os.path.join(report_dictory, now), title or 'pytest+allure API Demo', tester=tester, desc=desc,
    #               comment=comment)
    # 发邮件
    if Settings.MAIL:
        # 邮件主题和内容
        subject = title
        body = '%s, %s' % (title, comment)
        if os.path.isfile(f'{directory}{os.sep}html'):
            file_path = f'{directory}{os.sep}html'
        else:
            file_path = None
        send_mail(subject, body, file_path)
    return result
