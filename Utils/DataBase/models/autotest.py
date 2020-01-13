# coding=utf-8
# import time

from Utils.DataBase.Utils import check
from Utils.DataBase.Sqlite import *
import Settings


class Autotest:

    def __init__(self, cls, title, tester, desc=None,  comment=None, report=None, result=None):
        if not cls:
            raise Exception('Class must not null!')
        if not title:
            raise Exception('Title must not null!')
        if not tester:
            raise Exception('Tester must not null!')
        check(cls, str, 1, 32)
        check(title, str, 1, 64)
        check(tester, str, 1, 32)
        if desc:
            check(desc, str, 1, 200)
        if comment:
            check(comment, str, 1, 200)
        if report:
            check(report, str, 1, 100)
        if result:
            check(result, str, 1, 1)
        self.__cls = cls
        self.__title = title
        self.__tester = tester
        self.__desc = desc
        self.__comment = comment
        self.__report = report
        self.__result = result

    def save(self):
        keys = 'class, title, tester'
        params = r"'%s', '%s', '%s'" % (self.__cls, self.__title, self.__tester)
        if self.__desc:
            keys = keys + r', desc'
            params = params + r", '%s'" % self.__desc
        if self.__comment:
            keys = keys + r', comment'
            params = params + r", '%s'" % self.__comment
        if self.__report:
            keys = keys + r', report'
            params = params + r", '%s'" % self.__report
        if self.__result:
            keys = keys + r', result'
            params = params + r", '%s'" % self.__result
        keys = keys + r', create_time'
        params = params + r", datetime('now', 'localtime')"
        sql = r"insert into run_his(%s) values(%s)" % (keys, params)
        db = Sqlite(Settings.DB)
        db.connect()
        db.execute(sql)


