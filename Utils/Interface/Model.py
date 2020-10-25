# coding:utf-8
from Utils.Interface.Field import *


class Model:

    def __init__(self):
        pass

    def get(self):
        print(list(filter(lambda v: not v.startswith("__") and not v.endswith("__"), vars(self.__class__))))


class A(Model):
    integer = IntField(False, ge=1, lt=2)
    number = FloatField(False, 1, gt='1.0', le='1.1')
    name = CharField(True, '13829302938', min_length=11, max_length=11, reg='^1[0-9]{10}$')
    bank = CollectionField(True, [1.0, 8.2, 10.0], float)
    create_time = DatetimeField(False, '%Y-%m-%d %H:%M:%S', ge='2019-12-31 23:59:59', lt='2020-01-01 00:00:00')


a = A()
a.get()
a.create_time.generate()
print(a.create_time.valid_list)
print(a.create_time.invalid_list)




