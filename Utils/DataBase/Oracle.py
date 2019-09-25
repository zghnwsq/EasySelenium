# coding=utf-8

import cx_Oracle


class Oracle:

    def __init__(self, user: str, pwd: str, link: str, ip='', port='', sid=''):
        if not user or not (link or (ip and port and sid)):
            raise Exception('user or ip or sid should not be None')
        # self.connect = cx_Oracle.connect(user, pwd or '', '%s:%s/%s' % (ip, port, sid))
        self.connect = cx_Oracle.connect(user, pwd or '', link, encoding='UTF-8')
        self.cursor = self.connect.cursor()

    def query(self, sql: str, limit=10, *args, **kwargs):
        if sql:
            if limit == 1:
                result = self.cursor.execute(sql, *args, **kwargs).fetchone()
            else:
                result = self.cursor.execute(sql, *args, **kwargs).fetchmany(limit)
            # 查询结束后自动关闭连接
            # self.close()
            return result
        else:
            raise Exception('SQL should not be None')

    def execute(self, sql: str, *args, **kwargs):
        # cur.execute("insert into MyTable values (:idbv, :nmbv)", [1, "Fredico"])
        if sql:
            result = self.cursor.execute(sql, *args, **kwargs)
            self.connect.commit()
            # 查询结束后自动关闭连接
            # self.close()
            return result
        else:
            raise Exception('SQL should not be None')

    def execute_block(self, sql: str, out_type, *args, **kwargs):
        if sql:
            if out_type:
                var = self.cursor.var(out_type)
                self.cursor.execute(sql, *args, out_var=var, **kwargs)
                # 查询结束后自动关闭连接
                self.close()
                return var.getvalue()
            else:
                result = self.cursor.execute(sql, *args, **kwargs)
                self.connect.commit()
                # 查询结束后自动关闭连接
                self.close()
                return result
        else:
            raise Exception('SQL should not be None')

    def close(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as e:
            print(e)
