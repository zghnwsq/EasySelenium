# coding=utf-8
from Runner import RunByPytest
from TestCases.Demo import TestApiMZ
import pytest
import os
import time
import json
import Settings
# from Utils.Runner.Sqlite import *
import TestCases.Demo.TestApiMZ as TestApiMZ

# print(TestApiMZ.__file__)
# now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestTXYJS', now)
# res = pytest.main([TestApiMZ.__file__+'::TestMZ::test_GH1018Q1_invalid', '--alluredir', directory + '/json'])
# insert_result(os.path.join('TestTXYJS', now), 'pytest+allure API Demo')
# allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
# os.system(allure_cmd)

res = RunByPytest.run(py_file=TestApiMZ, py_class='TestMZ',
                      comment='comment', tester='TED')
