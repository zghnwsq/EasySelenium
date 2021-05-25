import os
from importlib import import_module
import Settings
from Utils.RPC.RPCServer import RegisterFunctions
from Utils.Runner.LoadSuite import load_suite
# from TestCases.Demo.TestDemo import TestDemo
# from TestCases.Demo.TestTXYJS import TestTXYJS
import Runner.RunByHtmlRunner as RunByHtmlRunner
import Runner.RunByPytest as RunByPytest
# import TestCases.Demo.TestApiMZ as TestApiMZ
# import TestCases.Demo.TestMail as TestMail
import traceback

from Utils.Yaml import yaml


class TestSuiteFunctions(RegisterFunctions):

    def __init__(self):
        """
           具体的注册在RPC Server的测试方法，一个方法代表一个测试用例组
           继承自RPC Server注册方法基类
           2021.5.25 改为从yaml配置中动态导入
           suites_dict： 测试集的信息
                key: RPC Client调用的suite_name
                value： dict:
                        MODULE：测试集所在模块
                        CLASS： 测试集所在类
                        NAME： 测试集注册名,即RPC Client调用的suite_name
                        TYPE： unittest / pytest
        """
        super().__init__()
        suites = yaml.read_yaml(os.path.join(Settings.BASE_DIR, 'TestCases', 'register.yaml'))['Suite']
        self.suites_dict = {}
        for s in suites:
            self.suites_dict[s['NAME']] = s

    # @staticmethod
    # def Demo_Web(kw):
    #     try:
    #         suite = load_suite(TestDemo, kw['mtd'], kw['rg'])
    #         # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Web', tester=kw['tester'] or '',
    #         #                           comment=kw['comment'] or '')
    #         res = RunByHtmlRunner.run_and_return(suite, test_group=TestDemo.Test_Group, suite_name=TestDemo.Test_Suite,
    #                                              tester=kw['tester'] or '', comment=kw['comment'] or '')
    #     except Exception as e:
    #         return str(e)[:256]
    #     return res
    #
    # @staticmethod
    # def Demo_Api(kw):
    #     try:
    #         suite = load_suite(TestTXYJS, kw['mtd'], kw['rg'])
    #         # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Api', tester=kw['tester'] or '',
    #         #                           comment=kw['comment'] or '')
    #         res = RunByHtmlRunner.run_and_return(suite, test_group=TestTXYJS.Test_Group,
    #                                              suite_name=TestTXYJS.Test_Suite, tester=kw['tester'] or '',
    #                                              comment=kw['comment'] or '')
    #     except Exception as e:
    #         return str(e)[:256]
    #     return res
    #
    # @staticmethod
    # def Demo_Api_GH1018Q1(kw):
    #     try:
    #         mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
    #         RunByPytest.collect_case_count(py_file=TestApiMZ, py_class='TestMZ')
    #         res = RunByPytest.run_and_return(py_file=TestApiMZ, py_class='TestMZ', py_method=mtd,
    #                                          dsrange=dsrange, title='Api_GH1018Q1', comment=kw['comment'],
    #                                          tester=kw['tester'])
    #     except Exception as e:
    #         print(e.args)
    #         msg = traceback.format_exc()
    #         return str(msg)[:256]
    #     return res
    #
    # @staticmethod
    # def Demo_Web_Mail(kw):
    #     try:
    #         mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
    #         RunByPytest.collect_case_count(py_file=TestMail, py_class='TestMail')
    #         res = RunByPytest.run_and_return(py_file=TestMail, py_class='TestMail', py_method=mtd,
    #                                          dsrange=dsrange, title='TestMail', comment=kw['comment'],
    #                                          tester=kw['tester'])
    #     except Exception as e:
    #         print(e.args)
    #         msg = traceback.format_exc()
    #         return str(msg)[:256]
    #     return res

    def methods(self):
        """
        :return: 返回测试集注册名,即RPC Client调用的suite_name列表
        """
        return list(self.suites_dict.keys())

    def run_suite(self, kw: dict):
        """
            根据kw['suite_name'],调用对应的测试集方法
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: None
        """
        if 'suite_name' in kw.keys():
            suite_name = kw['suite_name']
            suite_meta = self.suites_dict[suite_name]
            if suite_meta['TYPE'] == 'unittest':
                res = self.__run_unittest(suite_meta, kw)
            else:
                res = self.__run_pytest(suite_meta, kw)
            return res
        else:
            return '调用参数缺少suite_name字段'

    @staticmethod
    def __run_unittest(suite_meta: dict, kw: dict):
        """
            运行unittest类型的测试集
        :param suite_meta: 测试集的信息
                        MODULE：测试集所在模块
                        CLASS： 测试集所在类
                        NAME： 测试集注册名,即RPC Client调用的suite_name
                        TYPE： unittest / pytest
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: 结果
        """
        module = import_module(suite_meta['MODULE'])
        cls = getattr(module, suite_meta['CLASS'])
        try:
            suite = load_suite(cls, kw['mtd'], kw['rg'])
            res = RunByHtmlRunner.run_and_return(suite, test_group=getattr(cls, 'Test_Group'), suite_name=getattr(cls, 'Test_Suite'),
                                                 tester=kw['tester'] or '', comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def __run_pytest(suite_meta: dict, kw: dict):
        """
            运行pytest类型的测试集
        :param suite_meta:
        :param kw:测试集的信息
                        MODULE：测试集所在模块
                        CLASS： 测试集所在类
                        NAME： 测试集注册名,即RPC Client调用的suite_name
                        TYPE： unittest / pytest
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: 结果
        """
        module = import_module(suite_meta['MODULE'])
        try:
            mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
            RunByPytest.collect_case_count(py_file=module, py_class=suite_meta['CLASS'])
            res = RunByPytest.run_and_return(py_file=module, py_class=suite_meta['CLASS'], py_method=mtd,
                                             dsrange=dsrange, title='Api_GH1018Q1', comment=kw['comment'],
                                             tester=kw['tester'])
        except Exception as e:
            print(e.args)
            msg = traceback.format_exc()
            return str(msg)[:256]
        return res


