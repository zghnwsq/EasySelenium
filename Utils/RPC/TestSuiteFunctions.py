from Utils.RPC.RPCServer import RegisterFunctions
from Utils.Runner.LoadSuite import load_suite
from TestCases.Demo.TestDemo import TestDemo
from TestCases.Demo.TestTXYJS import TestTXYJS
import Runner.RunByHtmlRunner as RunByHtmlRunner
import Runner.RunByPytest as RunByPytest
import TestCases.Demo.TestApiMZ as TestApiMZ
import TestCases.Demo.TestMail as TestMail
import traceback


class TestSuiteFunctions(RegisterFunctions):

    def __init__(self):
        """
           具体的注册在RPC Server的测试方法，一个方法代表一个测试用例组
           继承自RPC Server注册方法基类
        """
        super().__init__()

    @staticmethod
    def Demo_Web(kw):
        try:
            suite = load_suite(TestDemo, kw['mtd'], kw['rg'])
            # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Web', tester=kw['tester'] or '',
            #                           comment=kw['comment'] or '')
            res = RunByHtmlRunner.run_and_return(suite, test_group=TestDemo.Test_Group, suite_name=TestDemo.Test_Suite,
                                                 tester=kw['tester'] or '', comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def Demo_Api(kw):
        try:
            suite = load_suite(TestTXYJS, kw['mtd'], kw['rg'])
            # res = RunByHtmlRunner.run(suite, test_group='Demo', suite_name='Api', tester=kw['tester'] or '',
            #                           comment=kw['comment'] or '')
            res = RunByHtmlRunner.run_and_return(suite, test_group=TestTXYJS.Test_Group,
                                                 suite_name=TestTXYJS.Test_Suite, tester=kw['tester'] or '',
                                                 comment=kw['comment'] or '')
        except Exception as e:
            return str(e)[:256]
        return res

    @staticmethod
    def Demo_Api_GH1018Q1(kw):
        try:
            mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
            RunByPytest.collect_case_count(py_file=TestApiMZ, py_class='TestMZ')
            res = RunByPytest.run_and_return(py_file=TestApiMZ, py_class='TestMZ', py_method=mtd,
                                             dsrange=dsrange, title='Api_GH1018Q1', comment=kw['comment'],
                                             tester=kw['tester'])
        except Exception as e:
            print(e.args)
            msg = traceback.format_exc()
            return str(msg)[:256]
        return res

    @staticmethod
    def Demo_Web_Mail(kw):
        try:
            mtd, dsrange = RunByPytest.get_method_and_dsrange(kw)
            RunByPytest.collect_case_count(py_file=TestMail, py_class='TestMail')
            res = RunByPytest.run_and_return(py_file=TestMail, py_class='TestMail', py_method=mtd,
                                             dsrange=dsrange, title='TestMail', comment=kw['comment'],
                                             tester=kw['tester'])
        except Exception as e:
            print(e.args)
            msg = traceback.format_exc()
            return str(msg)[:256]
        return res



