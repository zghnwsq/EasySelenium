# coding=utf-8
import unittest
import sys
import pytest


def get_range(rg):
    res = []
    # 1-3 类型
    if rg.find('-') != -1:
        li = rg.strip().split('-')
        for i in range(int(li[0]), int(li[1])+1, 1):
            res.append(i)
    # 2,3,4 or 2 类型
    elif rg.find(',') != -1:
        li = rg.strip().split(',')
        for i in li:
            res.append(int(i))
    elif len(rg) == 1:
        res.append(int(rg.strip()))
    else:
        raise Exception('Error data range! Correct format: "2" or "1-3" or "2,3,5"')
    return res


def cmd_run(test_class):
    suit3 = unittest.TestSuite()
    comment = ''
    if len(sys.argv) < 2:  # python   xxx.py
        suit3 = unittest.TestLoader().loadTestsFromTestCase(test_class)
    if len(sys.argv) > 1:  # python  xxx.py   qlc  [1]
        method = sys.argv[1].strip()
        if 'all' in method:
            suit3 = unittest.TestLoader().loadTestsFromTestCase(test_class)
        else:
            if len(sys.argv) > 2:
                ds_range = sys.argv[2]
                li = get_range(ds_range)
                for i in li:
                    suit3.addTest(test_class('test_%s_%s' % (method, str(i))))
            else:
                raise Exception('Input args required: Test Method  [Data Source Range]')
    if len(sys.argv) > 3:  # python  xxx.py    qlc    111    调试
        comment = sys.argv[3].strip()
    return [suit3, comment]


def choose_case(data, dsrange):
    if dsrange.strip() != 'all':
        rg = get_range(dsrange)
        if int(data['no']) not in rg:
            pytest.skip('Not be choosen to run, then skip.')
