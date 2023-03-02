"""
@Time ： 2023/3/2 10:31
@Auth ： Ted
@File ：TestResult.py
@IDE ：PyCharm
"""


class SummaryResult:

    def __init__(self, group_name: str, test_suite: str, title: str, tester: str, description: str, comment: str,
                 report: str, result: list):
        """
        统一汇总结果
        :param group_name: 用例组
        :param test_suite: 用例集
        :param title: 标题
        :param tester: 测试人
        :param description: 描述
        :param comment: 备注
        :param report: 报告相对路径
        :param result: 用例结果列表
        """
        self.group_name = group_name
        self.test_suite = test_suite
        self.title = title
        self.tester = tester
        self.description = description
        self.comment = comment
        self.report = report
        self.result = result

    @property
    def values(self):
        return self.__dict__


class CaseResult:

    def __init__(self, case: str, title: str, result: str, finish_time: str):
        """
        用例结果
        :param case: 用例
        :param title: 标题
        :param result: 用例结果
        :param finish_time: 结束时间
        """
        self.case = case
        self.title = title
        self.result = result
        self.finish_time = finish_time

    @property
    def values(self):
        return self.__dict__
