# coding=utf-8
import os
import time
import pytest
import Settings
from Pages.DemoPage import DemoPage
from Utils.Browser.WebBrowser import chrome, close_down
from Utils.Excel.readXls import read_data_by_sheet_name
from Utils.Report.Log import logger


class TestDemoTwo:

    def setup_method(self):
        # self.imgs = []  # 截图存储列表
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        self.log = logger('info')
        # self.el = Element(self.driver, self.log)
        self.dpi = Settings.DPI

    def teardown_method(self):
        close_down(self)

    @pytest.mark.parametrize('ds',
                             read_data_by_sheet_name(os.path.join(Settings.BASE_DIR, 'DS', 'Demo_Web', 'TestDemo.xlsx'),
                                                     'test_b'))
    def test_disapear(self, ds):
        # 测试描述
        self._testMethodDoc = ds['desc']
        if 'skip' in ds.keys():
            if 'yes' in ds['skip']:
                pytest.skip('skip: {}'.format(ds['desc']))
        demo_page = DemoPage(self.driver, self.log)
        self.log.info('打开网页')
        # self.driver.get(ds['url'])
        demo_page.open_url(ds['url'])
        # 引用页面中的常量
        # self.driver.switch_to.frame(self.el.get(DemoPage.IFRAME))
        demo_page.switch_to_frame(demo_page.IFRAME)
        # 定位字符串参数化 ${test}=点击这里，使三个矩形淡出
        demo_page.get(DemoPage.BUTTON, ds['button'])
        # self.imgs.append(self.el.catch_screen(dpi=self.dpi))
        # allure.attach(self.el.catch_screen_as_png(dpi=self.dpi), '手动截图', allure.attachment_type.PNG)
        demo_page.allure_catch_screen(dpi=self.dpi, tag='手动截图')
        demo_page.click(demo_page.BUTTON, ds['button'])
        # 等待
        demo_page.wait_until_invisible(demo_page.SQUARE)
        # 手动截图
        # img = self.driver.get_screenshot_as_base64()
        # self.imgs.append(self.el.catch_screen(dpi=self.dpi))
        demo_page.get(demo_page.BUTTON, ds['button'])
        img = demo_page.catch_screen_as_png(dpi=self.dpi)
        # allure.attach(img, '手动截图', allure.attachment_type.PNG)
        demo_page.allure_catch_screen(dpi=self.dpi, tag='手动截图')
        # 检查点
        assert demo_page.get(demo_page.SQUARE).is_displayed() is False


if __name__ == '__main__':
    # pass
    # debug
    # import time, os
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestDemoTwo', now)
    pytest.main(
        ['TestDemoTwo.py::TestDemoTwo::test_disapear', '--alluredir', directory + '/json'])
    # allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    # os.system(allure_cmd)

