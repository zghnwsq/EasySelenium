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
auth = AuthToken('x-www-form-urlencoded', template_str=templ_str)
cases = auth.generate_test_case()
auth_valid_cases = cases['valid_cases']
auth_invaid_cases = cases['invalid_cases']

templ_str = '{{"accessToken": "{accessToken}","itemCodes": ["{itemCodes}"],"status": "{status}","pageSize":  {pageSize},"subApply": "{subApply}","areaCode": "{areaCode}"}}'
apply = QueryApplyList('json', template_str=templ_str)
cases = apply.generate_test_case()
apply_valid_cases = cases['valid_cases']
apply_invalid_cases = cases['invalid_cases']

# Test_Group = 'Demo'


@ddt.ddt
class TestTXYJS(unittest.TestCase):
    # 必填且唯一: Test_Group  Test_Suite
    # 非必填：__doc__ 报告title
    __doc__ = '-接口测试示例-'
    Test_Group = 'Demo'
    Test_Suite = 'API'

    def setUp(self):
        print('begin')
        self.auth_url = 'http://200.168.168.192:8888/oauth2/getToken'
        self.apply_url = 'http://200.168.168.192:8888/uapply/queryItemsApplyList'
        self.session = requests.session()
        self.log = logger('info')

    def tearDown(self):
        if self.session is not None:
            self.session.close()
        print('end')

    def get_auth(self, data):
        # get token
        headers = {'Content-Type': 'x-www-form-urlencoded'}
        resp = self.session.post(self.auth_url, headers=headers, data=data)
        self.assertEquals(resp.status_code, 200, msg=f'状态码不为200,实际: {resp.status_code}')
        response_json = json.loads(resp.text)
        return response_json

    @ddt.data(*auth_valid_cases)
    def test_auth_valid_case(self, dt):
        # _testMethodDoc: 用例名
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        response_json = self.get_auth(data=dt['data'])
        self.log.info(f'response: {response_json}')
        self.assertEqual(response_json['expires_in'], 3600, msg='Expect expires_in==3600')

    @ddt.data(*auth_invaid_cases)
    def test_auth_invalid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        response_json = self.get_auth(data=dt['data'])
        self.log.info(f'response: {response_json}')
        self.assertEqual(response_json['error'], 'invalid_client', msg='Expect invalid_client==error')

    @ddt.data(*apply_valid_cases)
    def test_apply_valid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        # get token
        data = 'clientId=SHZHSH&clientSecret=111111b'
        response_json = self.get_auth(data)
        token = response_json['access_token']
        headers = {'Content-Type': 'application/json'}
        js = json.loads(dt['data'])
        if 'accessToken' in js.keys() and js['accessToken'] == 'valid_token':
            js['accessToken'] = token
        response = self.session.post(self.apply_url, headers=headers, json=js)
        self.assertEquals(response.status_code, 200, msg=f'状态码不为200,实际: {response.status_code}')
        self.log.info(f'response: {response.text}')
        res_json = json.loads(response.text)
        self.assertEqual(res_json['isSuccess'], True, msg='Expect isSuccess==true')

    @ddt.data(*apply_invalid_cases)
    def test_apply_invalid_case(self, dt):
        self._testMethodDoc = dt['desc']
        self.log.info(f'data: {dt}')
        # get token
        data = 'clientId=SHZHSH&clientSecret=111111b'
        response_json = self.get_auth(data)
        token = response_json['access_token']
        headers = {'Content-Type': 'application/json'}
        js = json.loads(dt['data'])
        if 'accessToken' in js.keys() and js['accessToken'] == 'valid_token':
            js['accessToken'] = token
        response = self.session.post(self.apply_url, headers=headers, json=js)
        self.assertEquals(response.status_code, 200, msg=f'状态码不为200,实际: {response.status_code}')
        self.log.info(f'response: {response.text}')
        res_json = json.loads(response.text)
        self.assertEqual(res_json['isSuccess'], False, msg='Expect isSuccess==false')


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
    suit = unittest.TestLoader().loadTestsFromTestCase(TestTXYJS)
    print(suit.countTestCases())
    # suit = unittest.TestSuite()
    # tc = [TestTXYJS('test_apply_valid_case')]
    # suit.addTests(tc)
    # runner.run(suit)



