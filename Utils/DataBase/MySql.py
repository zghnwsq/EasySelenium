import pymysql


class Mysql:

    def __init__(self, url, port, user_name, password, db_name):
        self.url = url
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.con = None
        self.cursor = None

    def connect(self):
        self.con = pymysql.connect(host=self.url, port=self.port, database=self.db_name, user=self.user_name,
                                   password=self.password)
        self.cursor = self.con.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except pymysql.Error:
            self.con.rollback()

    def fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetchone(self, sql):
        self.cursor.execute(sql)
        cols = self.cursor.description
        res = self.cursor.fetchone()
        res_dict = dict(zip(cols, res))
        # for i, col in enumerate(cols):
        #     res_dict[col[0]] = res[i]
        return res_dict

    def close(self):
        self.con.close()







