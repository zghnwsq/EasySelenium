import ddt
import unittest
from Utils.Interface.Model import *
import requests
import json
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN
from Utils.Report.Log import logger


class AuthToken(Model):
    clientId = CollectionField(True, ['SHZHSH'], str)
    clientSecret = CollectionField(True, ['111111b'], str)


class QueryApplyList(Model):
    accessToken = CollectionField(True, ['valid_token'], str)
    itemCodes = CollectionField(False, ['312090135000'], str, accept_none=False)
    status = CollectionField(False, ['待预审'], str, accept_none=True)
    pageSize = IntField(True, gt=0)
    subApply = CollectionField(True, ['1'], str)
    areaCode = CharField(False, template='', accept_none=True)


templ_str = 'clientId={clientId}&clientSecret={clientSecret}'
auth = AuthToken(templ_str, 'x-www-form-urlencoded')
cases = auth.generate_test_case()
auth_valid_cases = cases['valid_cases']
auth_invaid_cases = cases['invalid_cases']

templ_str = '{{"accessToken": "{accessToken}","itemCodes": ["{itemCodes}"],"status": "{status}","pageSize":  {pageSize},"subApply": "{subApply}","areaCode": "{areaCode}"}}'
apply = QueryApplyList(templ_str, 'json')
cases = apply.generate_test_case()
apply_valid_cases = cases['valid_cases']
apply_invalid_cases = cases['invalid_cases']


@ddt.ddt
class TestApi(unittest.TestCase):
    __doc__ = '-接口测试示例-'

    def setUp(self):
        print('begin')
        self.auth_url = 'http://200.168.168.191:8000/oauth2/getToken'
        self.apply_url = 'http://200.168.168.191:8000/uapply/queryItemsApplyList'
        self.session = requests.session()
        self.log = logger('info')

    def tearDown(self):
        if self.session is not None:
            self.session.close()
        print('end')

    @ddt.data(*auth_valid_cases)
    def test_auth_valid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        headers = {'Content-Type': 'x-www-form-urlencoded'}
        response = self.session.post(self.auth_url, headers=headers, data=dt['data']).text
        self.log.info(f'response: {response}')
        res_json = json.loads(response)
        self.assertEqual(res_json['expires_in'], 3600)

    @ddt.data(*auth_invaid_cases)
    def test_auth_invalid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.session.post(self.auth_url, headers=headers, data=dt['data']).text
        self.log.info(f'response: {response}')
        res_json = json.loads(response)
        self.assertEqual(res_json['error'], 'invalid_client')

    @ddt.data(*apply_valid_cases)
    def test_apply_valid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        # get token
        headers = {'Content-Type': 'x-www-form-urlencoded'}
        data = 'clientId=SHZHSH&clientSecret=111111b'
        response_json = json.loads(self.session.post(self.auth_url, headers=headers, data=data).text)
        token = response_json['access_token']
        headers = {'Content-Type': 'application/json'}
        js = json.loads(dt['data'])
        if 'accessToken' in js.keys() and js['accessToken'] == 'valid_token':
            js['accessToken'] = token
        response = self.session.post(self.apply_url, headers=headers, json=js).text
        self.log.info(f'response: {response}')
        res_json = json.loads(response)
        self.assertEqual(res_json['isSuccess'], True)

    @ddt.data(*apply_invalid_cases)
    def test_apply_invalid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        # get token
        headers = {'Content-Type': 'x-www-form-urlencoded'}
        data = 'clientId=SHZHSH&clientSecret=111111b'
        response_json = json.loads(self.session.post(self.auth_url, headers=headers, data=data).text)
        token = response_json['access_token']
        headers = {'Content-Type': 'application/json'}
        js = json.loads(dt['data'])
        if 'accessToken' in js.keys() and js['accessToken'] == 'valid_token':
            js['accessToken'] = token
        response = self.session.post(self.apply_url, headers=headers, json=js).text
        self.log.info(f'response: {response}')
        res_json = json.loads(response)
        self.assertEqual(res_json['isSuccess'], False)


if __name__ == '__main__':
    # 用例不在这里运行
    # 调试用
    # unittest.main()
    fileBase = '../../Report/api.html'  # 目录
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fileBase,
        title='{ Test API Demo }',
        description='Test API Demo',
        tester='ted',
        retry=0
    )
    suit = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    # suit = unittest.TestSuite()
    # tc = [TestApi('test_apply_valid_case')]
    # suit.addTests(tc)
    runner.run(suit)



