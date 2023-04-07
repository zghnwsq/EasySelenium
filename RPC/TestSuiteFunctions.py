import os
import string
from importlib import import_module, reload
import Settings
from RPC.BaseRegisterInstance import BaseRegisterInstance
from Utils.Runner.LoadSuite import load_suite
# from TestCases.Demo.Demo_Web import Demo_Web
# from TestCases.Demo.TestTXYJS import TestTXYJS
import Runner.RunByHtmlRunner as RunByHtmlRunner
import Runner.RunByPytest as RunByPytest
# import TestCases.Demo.TestApiMZ as TestApiMZ
# import TestCases.Demo.TestMail as TestMail
import traceback
from Utils.Yaml import yaml


class TestSuiteInstance(BaseRegisterInstance):

    def __init__(self):
        """
           具体的注册在RPC Server的测试方法，一个方法代表一个测试用例组
           继承自RPC Server注册方法基类
           2021.5.25 改为从yaml配置中动态导入,允许多个文件
           suites_dict： 测试集的信息
                key: RPC Client调用的suite_name
                value： dict:
                        MODULE：测试集所在模块
                        CLASS： 测试集所在类
                        NAME： 测试集注册名,即RPC Client调用的suite_name
                        TYPE： unittest / pytest
                        DS_FILE_NAME： 数据源文件名称
        """
        super().__init__()
        suites = []
        for yml in Settings.RPC_SERVER_SUITES:
            suites += yaml.read_yaml(os.path.join(Settings.BASE_DIR, 'TestSuiteRegister', yml))['Suite']
        # self.suites_dict = {}
        for s in suites:
            self.suites_dict[s['NAME']] = s

    def methods(self):
        """
        :return: 返回字典{测试集注册名:tests列表(","连接的字符串)},即RPC Client调用的suite_name列表和可供选择的mtd
        """
        methods_dict = {}
        for suite_meta in self.suites_dict.values():
            name = suite_meta['NAME']
            module = import_module(suite_meta['MODULE'])
            cls = getattr(module, suite_meta['CLASS'])
            tests = filter(lambda m: m.startswith('test_') and callable(getattr(cls, m)), dir(cls))
            methods_dict[name] = ','.join(
                sorted(set(func.replace('test_', '').rstrip(string.digits).rstrip('_') for func in tests)))
        return methods_dict

    def run_suite(self, kw: dict):
        """
            根据kw['suite_name'],调用对应的测试集方法
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: None
        """
        print(f'Run suite: {kw}')
        if 'suite_name' in kw.keys():
            suite_name = kw['suite_name']
            suite_meta = self.suites_dict[suite_name]
            if suite_meta['TYPE'] == 'unittest':
                res = self.__run_unittest(suite_meta, kw)
            elif suite_meta['TYPE'] == 'pytest':
                res = self.__run_pytest(suite_meta, kw)
            else:
                return 'TYPE:用例类型错误.'
            print(res)
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
                        NAME： 测试集注册名,即RPC Client调用的suite_name, 格式: 'groupName' + '_' + 'suiteName'
                        TYPE： unittest / pytest
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: 结果
        """
        module = import_module(suite_meta['MODULE'])
        # 重新编译模块,否则新数据源文件不加载
        reload(module)
        cls = getattr(module, suite_meta['CLASS'])
        try:
            group_suite = suite_meta['NAME'].split('_')
            # 加载用例,同时统计测试集用例数
            suite = load_suite(cls, kw['mtd'], kw['rg'], test_group=group_suite[0],
                               suite_name='_'.join(group_suite[1:]))
            if suite.countTestCases() == 0:
                print('Suite length: 0!')
                raise Exception('Suite length: 0!')
            # 2021.6.3 getattr(cls, 'Test_Group') getattr(cls, 'Test_Suite') 废弃
            # 2022.9.26 增加多线程参数
            is_thread = True if 'TRUE' == suite_meta.get('IS_THREAD', 'FALSE').upper() else False
            threads = suite_meta.get('THREADS', 1)
            res = RunByHtmlRunner.run_and_return(suite, test_group=group_suite[0], suite_name='_'.join(group_suite[1:]),
                                                 tester=kw['tester'] or '', comment=kw['comment'] or '',
                                                 is_thread=is_thread, threads=threads)
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def __run_pytest(suite_meta: dict, kw: dict):
        """
            运行pytest类型的测试集
        :param suite_meta:测试集的信息
                            MODULE：测试集所在模块
                            CLASS： 测试集所在类
                            NAME： 测试集注册名,即RPC Client调用的suite_name, 格式: 'groupName' + '_' + 'suiteName'
                            TYPE： unittest / pytest
        :param kw: eg: {'suite_name': 'Demo_Web', 'mtd': 'b', 'rg': '1', 'comment': '备注', 'tester': 'TED'}
        :return: 结果
        """
        module = import_module(suite_meta['MODULE'])
        reload(module)
        try:
            mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
            RunByPytest.collect_case_count(py_file=module, name=suite_meta['NAME'])
            res = RunByPytest.run_and_return(py_file=module, py_method=mtd, dsrange=dsrange, comment=kw['comment'],
                                             tester=kw['tester'], suite_meta=suite_meta)
        except Exception as e:
            print(e.args)
            msg = traceback.format_exc()
            return str(msg)[:256]
        return res
