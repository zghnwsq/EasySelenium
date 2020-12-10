# coding=utf-8
from TestCases.Demo import TestApiMZ
import pytest
import os
import time
import json
import Settings
from Utils.Runner.Sqlite import *

now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestApi', now)
res = pytest.main([TestApiMZ.__file__, '--alluredir', directory + '/json'])
insert_result(os.path.join('TestApi', now), 'pytest+allure API Demo')
allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
os.system(allure_cmd)





