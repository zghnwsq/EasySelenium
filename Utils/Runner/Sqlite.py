import json
import os
import Settings
from Utils.DataBase.models.autotest import RunHis


def insert_result(res_dir, title, tester=None, desc=None, comment=None):
    for root, dirs, files in os.walk(os.path.join(Settings.BASE_DIR, 'Report', res_dir)):
        for filename in files:
            if 'result.json' in filename:
                with open(os.path.join(root, filename), encoding='UTF-8') as result:
                    jres = json.loads(result.read(), encoding='UTF-8')
                    test_case = jres['name']
                    if 'pass' in jres['status']:
                        result = '0'
                    elif 'skiped' in jres['status']:
                        result = '3'
                    else:
                        result = '1'
                    group = jres['labels'][1]['value']
                    suite = jres['labels'][2]['value']
                    host = jres['labels'][3]['value']
                    report = os.path.join(res_dir, 'html')
                    finish_time = str(jres['stop'])[:10]
                    RunHis(group, suite, test_case, title, tester or host,
                           desc=desc, comment=comment, report=report, result=result, create_time=finish_time
                           ).save_with_time()






