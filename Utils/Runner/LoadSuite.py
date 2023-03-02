import os
import unittest
import warnings
import requests
from requests.auth import HTTPBasicAuth
import Settings
from Utils.DataBase.MySql import Mysql
from Utils.Runner.Cmd import get_range


def load_suite(test_class, mtd=None, rg=None, test_group=None, suite_name=None):
    suite = unittest.TestSuite()
    # if hasattr(test_class, 'Test_Group') and hasattr(test_class, 'Test_Suite'):
    if test_group and suite_name:
        case_count = unittest.TestLoader().loadTestsFromTestCase(test_class).countTestCases()
        update_suite_count_to_server(test_group, suite_name, case_count)
    if not mtd and not rg:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    elif 'all' in mtd:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    # elif mtd and rg:
    #     li = get_range(rg)
    #     count = unittest.TestLoader().loadTestsFromTestCase(test_class).countTestCases()
    #     formatter = f'test_%s_%0{len(str(count))}d'
    #     for i in li:
    #         suite.addTest(test_class(formatter % (mtd, i)))
    elif mtd:
        # bug: 只有mtd，但有多个场景，是test_mtd_1格式
        loader = unittest.TestLoader()
        # # 测试方法名后加几位数取决于整个类的用例数位数
        # class_case_count = loader.loadTestsFromTestCase(test_class).countTestCases()
        # 指定方法,加载所有场景
        loader.testMethodPrefix = f'test_{mtd}'
        # 该方法场景数
        this_case_count = loader.loadTestsFromTestCase(test_class).countTestCases()
        if rg:
            # 按需加载
            formatter = f'test_%s_%0{len(str(this_case_count))}d'
            li = get_range(rg)
            for i in li:
                suite.addTest(test_class(formatter % (mtd, i)))
        else:
            # 加载所有
            suite = loader.loadTestsFromTestCase(test_class)
        # suite.addTest(test_class(f'test_{mtd}'))
    else:
        raise Exception('Input args required: Test Method')
    return suite


def update_suite_count(test_group: str, test_suite: str, case_count: int):
    warnings.warn("update_suite_count is deprecated, replace it with update_suite_count_to_server", DeprecationWarning)
    print(f"group: {test_group}, suite: {test_suite}, count: {case_count}")
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PWD')
    db = Mysql(Settings.MyWebDb, Settings.MyWebDbPort, user, pwd, Settings.MyWebDbName)
    db.connect()
    sql = f"select * from autotest_suitecount where `group`='{test_group}' and suite='{test_suite}'"
    is_exists = db.fetchall(sql)
    if not is_exists:
        sql = f"insert into autotest_suitecount(`group`, suite, count) values ('{test_group}', '{test_suite}', {case_count})"
        db.execute(sql)
    else:
        sql = f"update autotest_suitecount set count={case_count} where `group`='{test_group}' and suite='{test_suite}'"
        db.execute(sql)
    db.close()


def update_suite_count_to_server(test_group: str, test_suite: str, case_count: int):
    print(f"Update_suite_count_to_server: group: {test_group}, suite: {test_suite}, count: {case_count}")
    session = requests.session()
    url = f'http://{Settings.MyWebService}:{Settings.MyWebServicePort}/autotest/suite/count/'
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(Settings.NodeUser, Settings.NodePwd)
    body = {'group_name': test_group, 'test_suite': test_suite, 'case_count': case_count}
    response = session.post(url, headers=headers, auth=auth, json=body)
    session.close()
    return response.text

