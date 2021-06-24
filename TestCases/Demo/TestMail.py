import os
import allure
import pytest
import Settings
from Utils.Browser.WebBrowser import chrome, close_down
from Utils.Report.Log import logger
from Pages.SinaMailPage import SinaMailPage
from Utils.Runner import Cmd
from Utils.Yaml import yaml

file_path = os.path.join(Settings.BASE_DIR, 'DS', 'Demo_Web_Mail', 'TestMail.yaml')
# 废弃:Test_Group-用例组,唯一
# 非必填:Case_Count-用例数
# Test_Group = 'TestMail'
Case_Count = 1


class TestMail:

    def setup_method(self):
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'], args=['--window-size=1920,1080', '--headless'])
        self.driver.delete_all_cookies()
        self.log = logger('info')
        # self.el = Element(self.driver, self.log)
        self.dpi = Settings.DPI

    def teardown_method(self):
        close_down(self)

    @allure.step('Step message: {msg}')
    def step_msg(self, msg):
        pass

    # @allure.title('Parameterized test title: ')
    @pytest.mark.parametrize('ds', yaml.read_yaml(file_path)['valid_cases'])
    def test_send_mail(self, ds, dsrange):
        sina_mail_page = SinaMailPage(self.driver, self.log)
        self._testMethodDoc = ds['desc']
        allure.dynamic.title(f'Case: {ds["desc"]}')
        Cmd.choose_case(ds, dsrange)
        sina_mail_page.open_url(ds['URL'])
        self.step_msg('Login')
        sina_mail_page.get(sina_mail_page.MAIL_ADDR).clear()
        sina_mail_page.input(sina_mail_page.MAIL_ADDR, text=ds['MAIL_ADDR'])
        sina_mail_page.input(sina_mail_page.MAIL_PASSWORD, text=ds['MAIL_PASSWORD'])
        sina_mail_page.click(sina_mail_page.LOGIN)
        self.step_msg('Send mail')
        sina_mail_page.click(sina_mail_page.MAIL_INDEX)
        self.driver.refresh()
        time.sleep(1)
        old_count = int(sina_mail_page.get(sina_mail_page.UNREAD_PRE).text)
        self.step_msg(f'old count: {old_count}')
        sina_mail_page.click(sina_mail_page.WRITE_MAIL)
        mail_content = ds["MAIL_CONTENT"] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        mail_subject = ds['MAIL_SUBJECT']
        # self.el.input(SinaMailPage.SEND_TO, text=ds['MAIL_ADDR'])
        self.driver.execute_script(f'arguments[0].value="{ds["MAIL_ADDR"]}"', sina_mail_page.get(sina_mail_page.SEND_TO))
        sina_mail_page.wait_until_displayed(sina_mail_page.SEND_TO_ADDR, ds['MAIL_ADDR'])
        sina_mail_page.input(sina_mail_page.SUBJECT, text=mail_subject)
        sina_mail_page.click(sina_mail_page.SUBJECT)
        time.sleep(0.5)
        sina_mail_page.switch_to_frame(sina_mail_page.BODY_IFRAME)
        sina_mail_page.wait_until_displayed(sina_mail_page.BODY)
        sina_mail_page.click(sina_mail_page.BODY)
        self.driver.execute_script(f'document.querySelector("body").innerHTML="{mail_content}"')
        sina_mail_page.switch_to_default_content()
        sina_mail_page.click(sina_mail_page.SEND_NOW)
        img = sina_mail_page.catch_screen_as_png(dpi=self.dpi)
        allure.attach(img, '发送邮件', allure.attachment_type.PNG)
        self.step_msg('Check mail')
        new_count = 0
        for i in range(10):
            sina_mail_page.click(sina_mail_page.CHECK_MAIL)
            sina_mail_page.wait_until_clickable(sina_mail_page.MAIL_INDEX)
            sina_mail_page.click(sina_mail_page.MAIL_INDEX)
            new_count = int(sina_mail_page.get(sina_mail_page.UNREAD_PRE).text)
            if new_count > old_count:
                break
            else:
                time.sleep(1)
        self.step_msg(f'Assert received the mail: new count {new_count} > old count {old_count}')
        assert new_count > old_count
        sina_mail_page.click(sina_mail_page.IN_BOX)
        sina_mail_page.wait_until_clickable(sina_mail_page.MAIL_LIST_SUBJECT, mail_content)
        sina_mail_page.click(sina_mail_page.MAIL_LIST_SUBJECT, mail_content)
        subject = sina_mail_page.get(sina_mail_page.READ_MAIL_SUBJECT).text
        self.step_msg(f'Assert mail subject "{subject}" contains "{mail_subject}"')
        assert ds['MAIL_SUBJECT'] in subject
        content = sina_mail_page.get(sina_mail_page.READ_MAIL_CONTENT).text
        self.step_msg(f'Assert mail content "{content}" contains "{mail_content}"')
        assert ds['MAIL_CONTENT'] in content


if __name__ == '__main__':
    # pass
    # debug
    import time, os
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestMail', now)
    pytest.main(
        ['TestMail.py::TestMail::test_send_mail', '--alluredir', directory + '/json'])
    # allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    # os.system(allure_cmd)



