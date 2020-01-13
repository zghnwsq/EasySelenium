# coding=utf-8


def check_col(obj, typ, mi=-99, ma=-99):

    if not isinstance(obj, typ):
        raise Exception('Wrong type!')
    if mi != -99 and len(obj) < mi:
        raise Exception('Wrong length! Expect min: %d' % mi)
    if ma != -99 and len(obj) > ma:
        raise Exception('Wrong length! Expect max: %d' % ma)
    return True

