# coding=utf-8
import os
import allure
import pytest
import Settings
from Pages import DemoPage
from Utils.Browser.WebBrowser import chrome, close_down
from Utils.ElementUtil.Element import Element
from Utils.Excel.readXls import read_data_by_sheet_name
from Utils.Report.Log import logger


class TestDemoTwo:

    def setup_method(self):
        # self.imgs = []  # 截图存储列表
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.dpi = Settings.DPI

    def teardown_method(self):
        close_down(self)

    @pytest.mark.parametrize('ds',
                             read_data_by_sheet_name(os.path.join(Settings.BASE_DIR, 'DS', 'TestDemo.xlsx'), 'Sheet1'))
    def test_disapear(self, ds):
        # 测试描述
        self._testMethodDoc = ds['desc']
        if 'skip' in ds.keys():
            if 'yes' in ds['skip']:
                pytest.skip('skip: {}'.format(ds['desc']))
        self.log.info('打开网页')
        # self.driver.get(ds['url'])
        self.el.open_url(ds['url'])
        # 引用页面中的常量
        # self.driver.switch_to.frame(self.el.get(DemoPage.IFRAME))
        self.el.switch_to_frame(DemoPage.IFRAME)
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        self.el.get(DemoPage.BUTTON, ds['button'])
        # self.imgs.append(self.el.catch_screen(dpi=self.dpi))
        allure.attach(self.el.catch_screen_as_png(dpi=self.dpi), '手动截图', allure.attachment_type.PNG)
        self.el.click(DemoPage.BUTTON, ds['button'])
        # 等待
        self.el.wait_until_invisible(DemoPage.SQUARE)
        # 手动截图
        # img = self.driver.get_screenshot_as_base64()
        # self.imgs.append(self.el.catch_screen(dpi=self.dpi))
        self.el.get(DemoPage.BUTTON, ds['button'])
        img = self.el.catch_screen_as_png(dpi=self.dpi)
        allure.attach(img, '手动截图', allure.attachment_type.PNG)
        # 检查点
        assert self.el.get(DemoPage.SQUARE).is_displayed() is False
