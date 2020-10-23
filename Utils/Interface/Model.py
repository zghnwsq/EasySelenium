# coding:utf-8

class Model:

    def __init__(self):
        pass

    def get(self):
        print(list(filter(lambda v: not v.startswith("__") and not v.endswith("__"), vars(self.__class__))))


class A(Model):
    idno = 'aaaaa'


a = A()
a.get()




