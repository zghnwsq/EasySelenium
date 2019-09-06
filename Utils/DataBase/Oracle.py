# coding=utf-8

import cx_Oracle


class Oracle:

    def __init__(self, user: str, pwd: str, ip: str, port:str, sid: str):
        if not user or not ip or not port or not sid:
            raise Exception('user or ip or sid should not be None')
        self.connect = cx_Oracle.connect(user, pwd or '', '%s:%s/%s' % (ip, port, sid))
        self.cursor = self.connect.cursor()

    def query(self, sql: str, limit=10):
        if sql:
            if limit == 1:
                result = self.cursor.execute(sql).fetchone()
            else:
                result = self.cursor.execute(sql).fetchmany(limit)
            return result
        else:
            raise Exception('SQL should not be None')

    def execute(self, sql: str):
        # cur.execute("insert into MyTable values (:idbv, :nmbv)", [1, "Fredico"])
        if sql:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        else:
            raise Exception('SQL should not be None')

    def close(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as e:
            print(e)
