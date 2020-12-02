# coding=utf-8
from TestCases.Demo import TestDemoTwo
import pytest
import os
import time
import json
import Settings
from Utils.Runner.Sqlite import *

now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestDemoTwo', now)
res = pytest.main([TestDemoTwo.__file__, '--alluredir', directory + '/json'])
# for root, dirs, files in os.walk(directory + '/json'):
#     for filename in files:
#         if 'result.json' in filename:
#             with open(f'{directory}/json/{filename}', encoding='UTF-8') as result:
#                 jres = json.loads(result.read(), encoding='UTF-8')
#                 print(jres['name'])
#                 print(jres['status'])
#                 print(jres['labels'][1]['value'])
#                 print(jres['labels'][2]['value'])
# insert_result(os.path.join('TestDemoTwo', now), 'pytest+allure Demo')
allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
os.system(allure_cmd)





