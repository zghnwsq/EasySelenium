# coding=utf-8
from Utils.Interface.Model import *
import requests
import json
import os
import time
import allure
import pytest
import Settings
from Utils.Yaml import yaml
import Utils.Runner.Cmd as Cmd


class GH1018Q1(Model):
    method_code = CharField(True, template='GH1018Q1')
    user_exp_id = CharField(True, template='1711')
    applyno = CharField(False, template='111', accept_none=False)
    suid = CharField(False, template='222', accept_none=False)
    data = CollectionField(True, [{
        "sfzh": "310105196208092416",
        "xm": "胡雄惠",
        "gfdl": "1"
    }], dict)
    sfzh = CharField(True, template='310105196208092416', min_length=18, max_length=18)
    xm = CharField(True, template='胡雄惠')
    gfdl = CollectionField(True, ['1', '3', '4'], str)


templ_dict = {
    "method_code": "GH1018Q1",
    "user_exp_id": "1711",
    "user_exp_name": "Q06011",
    "applyno": "111",
    "suid": "222",
    "data": {
        "sfzh": "",
        "xm": "",
        "gfdl": "1"
    }
}

file_path = os.path.join(Settings.BASE_DIR, 'DS', 'TestApi', 'GH1018Q1.yaml')


def get_case_file(fi_path):
    if not os.path.exists(fi_path):
        apply = GH1018Q1('json', template_dict=templ_dict)
        cases = apply.generate_test_case()
        # apply_valid_cases = cases['valid_cases']
        # apply_invalid_cases = cases['invalid_cases']
        yaml.write_yaml(fi_path, cases)
    return fi_path


class TestAPI:

    def setup_method(self):
        self.session = requests.session()
        self.url = 'http://200.168.168.123:9003/mzjk'

    def teardown_method(self):
        self.session.close()

    @allure.step
    def step_msg(self, msg):
        pass

    @pytest.mark.parametrize('ds', yaml.read_yaml(get_case_file(file_path))['valid_cases'])
    def test_GH1018Q1_valid(self, ds, dsrange):
        self.step_msg(ds['desc'])
        Cmd.choose_case(ds, dsrange)
        headers = {'Content-Type': 'application/json;charset:UTF-8'}
        response = self.session.post(self.url, headers=headers, json=ds['data']).text
        res_json = json.loads(response)
        self.step_msg(res_json)
        self.step_msg(f'Assert Equals: Expected: "", Actual: "{res_json["err_msg"]}"')
        assert res_json['err_msg'] == ''

    @pytest.mark.parametrize('ds', yaml.read_yaml(file_path)['invalid_cases'])
    def test_GH1018Q1_invalid(self, ds, dsrange):
        self.step_msg(ds['desc'])
        Cmd.choose_case(ds, dsrange)
        headers = {'Content-Type': 'application/json;charset:UTF-8'}
        response = self.session.post(self.url, headers=headers, json=ds['data']).text
        res_json = json.loads(response)
        self.step_msg(res_json)
        if 'err_code' in res_json.keys():
            self.step_msg(f'Assert Equals: Expected: "EEEEEE", Actual: "{res_json["err_code"]}"')
            assert res_json['err_code'] == 'EEEEEE'
        else:
            self.step_msg(f'Assert not Equals: Expected: not "", Actual: "{res_json["resDesc"]}"')
            assert res_json['resDesc'] != ''


if __name__ == '__main__':
    # debug
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestApi', now)
    pytest.main(
        ['TestApiMZ.py::TestAPI::test_GH1018Q1_invalid', '--dsrange', '1,3,6,7', '--alluredir', directory + '/json'])
    # allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    # os.system(allure_cmd)


