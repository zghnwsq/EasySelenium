# coding=utf-8

import sqlite3


class Sqlite:

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cursor = None

    def connect(self):
        self.cursor = self.con.cursor()

    def execute(self, sql):
        res = self.cursor.execute(sql)
        self.con.commit()
        if res:
            return res






