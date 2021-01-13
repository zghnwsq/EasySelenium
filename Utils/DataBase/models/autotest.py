# coding=utf-8
# import time

from Utils.DataBase.Utils import check_col
from Utils.DataBase.Sqlite import *
import Settings


class RunHis:
    """
        自动化执行历史表模型
    """

    def __init__(self, group, suite, case, title, tester, desc=None, comment=None, report=None, result=None, create_time=None):
        if not group:
            raise Exception('Group must not null!')
        if not suite:
            raise Exception('Suite must not null!')
        if not case:
            raise Exception('Case must not null!')
        if not title:
            raise Exception('Title must not null!')
        if not tester:
            raise Exception('Tester must not null!')
        check_col(group, str, 1, 32)
        check_col(suite, str, 1, 32)
        check_col(case, str, 1, 32)
        check_col(title, str, 1, 64)
        check_col(tester, str, 1, 32)
        if desc:
            check_col(desc, str, 1, 200)
        if comment:
            check_col(comment, str, 1, 200)
        if report:
            check_col(report, str, 1, 100)
        if result:
            check_col(result, str, 1, 1)
        self.__group = group
        self.__suite = suite
        self.__case = case
        self.__title = title
        self.__tester = tester
        self.__desc = desc
        self.__comment = comment
        self.__report = report
        self.__result = result
        self.__create_time = create_time

    def save(self):
        keys = r"'group', 'suite', 'case', 'title', 'tester'"
        values = r"'%s', '%s', '%s', '%s', '%s'" % (self.__group, self.__suite, self.__case, self.__title, self.__tester)
        if self.__desc:
            keys = keys + r", 'desc'"
            values = values + r", '%s'" % self.__desc
        if self.__comment:
            keys = keys + r", 'comment'"
            values = values + r", '%s'" % self.__comment
        if self.__report:
            keys = keys + r", 'report'"
            values = values + r", '%s'" % self.__report
        if self.__result:
            keys = keys + r", 'result'"
            values = values + r", '%s'" % self.__result
        keys = keys + r", 'create_time'"
        values = values + r", datetime('now', 'localtime')"
        sql = r"insert into run_his(%s) values(%s)" % (keys, values)
        db = Sqlite(Settings.MyWebDb)
        db.connect()
        db.execute(sql)

    def save_with_time(self):
        keys = r"'group', 'suite', 'case', 'title', 'tester'"
        values = r"'%s', '%s', '%s', '%s', '%s'" % (self.__group, self.__suite, self.__case, self.__title, self.__tester)
        if self.__desc:
            keys = keys + r", 'desc'"
            values = values + r", '%s'" % self.__desc
        if self.__comment:
            keys = keys + r", 'comment'"
            values = values + r", '%s'" % self.__comment
        if self.__report:
            keys = keys + r", 'report'"
            values = values + r", '%s'" % self.__report
        if self.__result:
            keys = keys + r", 'result'"
            values = values + r", '%s'" % self.__result
        keys = keys + r", 'create_time'"
        values = values + f", datetime({self.__create_time}, 'unixepoch', 'localtime')"
        sql = r"insert into run_his(%s) values(%s)" % (keys, values)
        db = Sqlite(Settings.MyWebDb)
        db.connect()
        db.execute(sql)


