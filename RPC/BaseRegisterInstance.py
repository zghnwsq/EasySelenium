"""
@Time ： 2023/3/20 15:44
@Auth ： Ted
@File ：BaseRegisterFunctions.py
@IDE ：PyCharm
"""
import os
import Settings
import Utils.FileUtil.Zip.Zip as ZipUtil
import time
import Utils.FileUtil.FileUtil as FileUtil
from xmlrpc.client import Binary


class BaseRegisterInstance:

    def __init__(self):
        """
           RPC Server注册方法基类
        """
        self.suites_dict = {}

    @staticmethod
    def get_report_file(file_path):
        """
           返回节点html报告压缩文件
        :param file_path: 报告在节点的存储路径
        :return: 压缩文件二进制数据
        """
        print(f'Get report file: {file_path}')
        # 新建压缩包路径
        zip_path = os.path.abspath(os.path.join(file_path, '..', 'zip'))
        if not os.path.exists(zip_path):
            os.mkdir(zip_path)
        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            if '.html' in file_path:
                ZipUtil.zip_file(file_path, os.path.join(zip_path, f'{timestamp}.zip'))
                FileUtil.remove(file_path)
                with open(os.path.join(zip_path, f'{timestamp}.zip'), 'rb') as report:
                    bin_data = Binary(report.read())
                FileUtil.remove(zip_path)
            else:
                ZipUtil.zip_dir(file_path, os.path.join(zip_path, f'{timestamp}.zip'))
                FileUtil.remove(file_path)
                with open(os.path.join(zip_path, f'{timestamp}.zip'), 'rb') as report:
                    bin_data = Binary(report.read())
                FileUtil.remove(os.path.abspath(os.path.join(file_path, '..')))
            return bin_data
        else:
            return None

    def replace_datasource(self, suite_name, bin_data):
        print(f'Replace datasource: {suite_name}')
        # print(bin_data)
        if suite_name in self.suites_dict.keys():
            if 'DS_FILE_NAME' in self.suites_dict[suite_name].keys():
                ds_file_name = self.suites_dict[suite_name]['DS_FILE_NAME']
                work_dir = os.path.join(Settings.BASE_DIR, 'DS', suite_name)
                file_path = os.path.join(work_dir, ds_file_name)
                if not os.path.exists(work_dir):
                    os.makedirs(work_dir, exist_ok=True)
                with open(file_path, 'wb') as handle:
                    handle.write(bin_data.data)
                return 'Success:File replaced!'
            else:
                # 用例集不需要数据源，不影响执行
                return 'DS_FILE_NAME not found in suite meta'
        else:
            return 'Error: suite_name not found!'

    # 2021.5.25 废弃, 改为从yaml配置中动态导入
    # def methods(self):
    #     """
    #        获取RPC注册的测试方法
    #     :return:
    #     """
    #     return (list(filter(
    #         lambda m: not m.startswith("__") and not m.endswith("__") and not m.startswith(
    #             "is_alive") and not m.startswith("methods") and not m.startswith("get_report") and callable(
    #             getattr(self, m)), dir(self))
    #     ))
