# coding=utf-8
# import time
import os
from Utils.DataBase.Utils import check_col
from Utils.DataBase.Sqlite import *
from Utils.DataBase.MySql import *
import Settings


class RunHis:
    """
        自动化测试执行历史表模型
    """

    def __init__(self, group, suite, case, title, tester, desc=None, comment=None, report=None, result=None, create_time=None):
        """
           自动化测试执行历史表模型, 检查数据并初始化
        :param group: 测试组
        :param suite: 测试套件名
        :param case: 测试用例名
        :param title: 标题
        :param tester: 测试人
        :param desc: 描述
        :param comment: 备注
        :param report: 报告uri
        :param result: 结果, 0-通过,1-失败,2-错误,3-跳过,
        :param create_time: 创建时间
        """
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

    def __prepare_sql(self):
        """
           准备入库insert sql的keys和values, create_time除外
        :return: keys, values
        """
        keys = r"'group', 'suite', 'case', 'title', 'tester'"
        values = r"'%s', '%s', '%s', '%s', '%s'" % (self.__group, self.__suite, self.__case, self.__title, self.__tester)
        if self.__desc:
            keys = keys + r", 'description'"
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
        return keys, values

    @staticmethod
    def __insert_into_db(sql):
        """
           连接数据库,执行insert sql
        :param sql: insert sql
        :return: None
        """
        # db = Sqlite(Settings.MyWebDb)
        user = os.getenv('MYSQL_USER')
        pwd = os.getenv('MYSQL_PWD')
        db = Mysql(Settings.MyWebDb, Settings.MyWebDbPort, user, pwd, Settings.MyWebDbName)
        db.connect()
        db.execute(sql)
        db.close()

    def save(self):
        """
           保存自动化测试执行数据到数据库,创建时间使用插入时间
        :return: None
        """
        keys, values = self.__prepare_sql()
        keys = keys + r", 'create_time'"
        values = values + r", datetime('now', 'localtime')"
        sql = r"insert into run_his(%s) values(%s)" % (keys, values)
        self.__insert_into_db(sql)

    def save_with_time(self):
        """
           保存自动化测试执行数据到数据库,创建时间使用报告时间
        :return: None
        """
        keys, values = self.__prepare_sql()
        keys = keys + r", 'create_time'"
        values = values + f", datetime({self.__create_time}, 'unixepoch', 'localtime')"
        sql = r"insert into run_his(%s) values(%s)" % (keys, values)
        self.__insert_into_db(sql)


