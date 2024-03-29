# coding=utf-8

import cx_Oracle


class Oracle:
    """
        Oracle数据库连接及语句执行
    """

    def __init__(self, user: str, pwd: str, link: str = '', ip='', port='', sid=''):
        """
        初始化连接
        :param user: 用户名
        :param pwd: 密码
        :param link: 连接串 ip:port/sid
        :param ip: ip
        :param port: port
        :param sid: sid
        """
        self.__cursor = None
        self.__connect = None
        if not user or not (link or (ip and port and sid)):
            raise Exception('user or ip or sid should not be None')
        # self.connect = cx_Oracle.connect(user, pwd or '', '%s:%s/%s' % (ip, port, sid))
        self.__user = user
        self.__pwd = pwd
        self.__link = '%s:%s/%s' % (ip, port, sid) if not link and ip and port and sid else link

    def connect(self):
        self.__connect = cx_Oracle.connect(self.__user, self.__pwd or '', self.__link, encoding='UTF-8')
        self.__cursor = self.__connect.cursor()

    def query(self, sql: str, limit=10, *args, **kwargs):
        """
        数据库查询
        :param sql:查询sql
        :param limit: 行数限制
        :param args: 不定参数，用于绑定参数
            sql = '''insert into departments (department_id, department_name)
                    values (:dept_id, :dept_name)'''
            __cursor.execute(sql, [280, "Facility"])
        :param kwargs: 不定参数，用于绑定参数
            __cursor.execute('''
                insert into departments (department_id, department_name)
                values (:dept_id, :dept_name)''', dept_id=280, dept_name="Facility")
        :return:Query result
        """
        if sql:
            self.connect()
            if limit == 1:
                result = self.__cursor.execute(sql, *args, **kwargs).fetchone()
            else:
                result = self.__cursor.execute(sql, *args, **kwargs).fetchmany(limit)
            # 查询结束后自动关闭连接
            self.close()
            return result
        else:
            raise Exception('SQL should not be None')

    def execute(self, sql: str, *args, **kwargs):
        """
        执行DML，执行后commit
        :param sql: DML
        :param args:不定参数，用于绑定参数
            sql = '''insert into departments (department_id, department_name)
                    values (:dept_id, :dept_name)'''
            __cursor.execute(sql, [280, "Facility"])
        :param kwargs:不定参数，用于绑定参数
            __cursor.execute('''
                insert into departments (department_id, department_name)
                values (:dept_id, :dept_name)''', dept_id=280, dept_name="Facility")
        :return: Execute result
        """
        # cur.execute("insert into MyTable values (:idbv, :nmbv)", [1, "Fredico"])
        if sql:
            self.connect()
            result = self.__cursor.execute(sql, *args, **kwargs)
            self.__connect.commit()
            # 查询结束后自动关闭连接
            self.close()
            return result
        else:
            raise Exception('SQL should not be None')

    def execute_block(self, sql: str, out_type, *args, **kwargs):
        """
        执行匿名块
        :param sql: 匿名块
        :param out_type:输出参数类型
        :param args:定参数，用于绑定参数
            sql = '''insert into departments (department_id, department_name)
                    values (:dept_id, :dept_name)'''
            __cursor.execute(sql, [280, "Facility"])
        :param kwargs:不定参数，用于绑定参数
            __cursor.execute('''
                insert into departments (department_id, department_name)
                values (:dept_id, :dept_name)''', dept_id=280, dept_name="Facility")
        :return: Query Result
        """
        if sql:
            self.connect()
            if out_type:
                var = self.__cursor.var(out_type)
                self.__cursor.execute(sql, *args, out_var=var, **kwargs)
                # 查询结束后自动关闭连接
                self.close()
                return var.getvalue()
            else:
                result = self.__cursor.execute(sql, *args, **kwargs)
                self.__connect.commit()
                # 查询结束后自动关闭连接
                self.close()
                return result
        else:
            raise Exception('SQL should not be None')

    def execute_func(self, func: str, out_type, *args, **kwargs):
        """
        执行匿名块
        :param func: 存储过程
        :param out_type:输出参数类型
        :param args:定参数，用于绑定参数
            sql = '''insert into departments (department_id, department_name)
                    values (:dept_id, :dept_name)'''
            __cursor.execute(sql, [280, "Facility"])
        :param kwargs:不定参数，用于绑定参数
            __cursor.execute('''
                insert into departments (department_id, department_name)
                values (:dept_id, :dept_name)''', dept_id=280, dept_name="Facility")
        :return: Query Result
        """
        if func:
            self.connect()
            if out_type:
                return_val = self.__cursor.callfunc(func, out_type, *args, **kwargs)
                # 查询结束后自动关闭连接
                self.close()
                return return_val
            else:
                self.__cursor.callfunc(func, *args, **kwargs)
                # 查询结束后自动关闭连接
                self.close()
                return None
        else:
            raise Exception('Function name should not be None')

    def close(self):
        """
        关闭数据连接
        :return: None
        """
        try:
            self.__cursor.close()
            self.__connect.close()
        except Exception as e:
            print(e)
