# coding=utf-8
import json
# import Settings
from Utils.DataBase.models.autotest import *


def check_col(obj, typ, mi=-99, ma=-99):
    """
    入库前检查字段是否符合表定义
    :param obj: 输入
    :param typ: 期望类型
    :param mi: 最小长度
    :param ma: 最大长度
    :return: 符合则返回真
    """
    if not isinstance(obj, typ):
        raise Exception('Wrong type!')
    if mi != -99 and len(obj) < mi:
        raise Exception('Wrong length! Expect min: %d' % mi)
    if ma != -99 and len(obj) > ma:
        raise Exception('Wrong length! Expect max: %d' % ma)
    return True

