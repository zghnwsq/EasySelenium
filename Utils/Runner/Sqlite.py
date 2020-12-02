import json
import os

from Utils.DataBase.models.autotest import RunHis


def insert_result(res_dir, title, tester=None, desc=None, comment=None):
    for root, dirs, files in os.walk(res_dir):
        for filename in files:
            if 'result.json' in filename:
                with open(os.path.join(res_dir, 'json', filename), encoding='UTF-8') as result:
                    jres = json.loads(result.read(), encoding='UTF-8')
                    test_case = jres['name']
                    if 'pass' in jres['status']:
                        result = '1'
                    else:
                        result = '0'
                    group = jres['labels'][1]['value']
                    suite = jres['labels'][2]['value']
                    host = jres['labels'][3]['value']
                    report = os.path.join(res_dir, 'html', 'index.html')
                    RunHis(group, suite, test_case, title, tester or host,
                           desc=desc, comment=comment, report=report, result=result
                           ).save()






