import os
import unittest
import Settings
from Utils.DataBase.MySql import Mysql
from Utils.Runner.Cmd import get_range


def load_suite(test_class, mtd=None, rg=None):
    suite = unittest.TestSuite()
    if hasattr(test_class, 'Test_Group') and hasattr(test_class, 'Test_Suite'):
        case_count = unittest.TestLoader().loadTestsFromTestCase(test_class).countTestCases()
        test_group = test_class.Test_Group
        test_suite = test_class.Test_Suite
        update_suite_count(test_group, test_suite, case_count)
    if not mtd and not rg:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    elif 'all' in mtd:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    elif mtd and rg:
        li = get_range(rg)
        count = unittest.TestLoader().loadTestsFromTestCase(test_class).countTestCases()
        formatter = f'test_%s_%0{len(str(count))}d'
        for i in li:
            suite.addTest(test_class(formatter % (mtd, i)))
    elif mtd:
        suite.addTest(test_class(f'test_{mtd}'))
    else:
        raise Exception('Input args required: Test Method')
    return suite


def update_suite_count(test_group: str, test_suite: str, case_count: int):
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



