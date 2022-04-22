import os
import time
import allure
import pytest
import Settings
from Utils.Browser.WebBrowser import chrome, close_down
from Pages.SinaMail.SinaMailLoginPage import SinaMailLoginPage
from Utils.Runner import Cmd
from Utils.Yaml import yaml
# from selenium.webdriver.common.action_chains import ActionChains

file_path = os.path.join(Settings.BASE_DIR, 'DS', 'Demo_Web_Mail', 'TestMail.yaml')
# 废弃:Test_Group-用例组,唯一
# 非必填:Case_Count-用例数
# Test_Group = 'TestMail'
Case_Count = 1


class TestMail:

    def setup_method(self):
        # self.driver = chrome(path=Settings.DRIVER_PATH['chrome'], args=['--window-size=1920,1080', '--headless'])
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'], user_dir=r'C:\Users\tedwa\AppData\Local\Google\UserData')
        self.driver.delete_all_cookies()
        # self.log = logger('info')
        # self.el = Element(self.driver, self.log)
        # self.dpi = Settings.DPI

    def teardown_method(self):
        close_down(self)

    @allure.step('Step message: {msg}')
    def step_msg(self, msg):
        pass

    # @allure.title('Parameterized test title: ')
    @pytest.mark.parametrize('ds', yaml.read_yaml(file_path)['valid_cases'])
    def test_send_mail(self, ds, dsrange):
        sina_mail_login_page = SinaMailLoginPage(self.driver)
        self._testMethodDoc = ds['desc']
        allure.dynamic.title(f'Case: {ds["desc"]}')
        Cmd.choose_case(ds, dsrange)
        self.step_msg('Login')
        sina_mail_index_page = sina_mail_login_page.login(ds)
        self.step_msg('Send mail')
        old_count, sina_mail_edit_page = sina_mail_index_page.open_write_mail()
        mail_content = ds["MAIL_CONTENT"] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        mail_subject = ds['MAIL_SUBJECT']
        sina_mail_edit_page.send_mail(ds, mail_subject, mail_content)
        self.step_msg('Check mail')
        new_count, sina_mail_inbox_page = sina_mail_index_page.wait_new_mail(old_count)
        self.step_msg(f'Assert received the mail: new count {new_count} > old count {old_count}')
        assert new_count > old_count, 'No new mail received'
        sina_mail_read_mail_page = sina_mail_inbox_page.click_mail(mail_content)
        subject, content = sina_mail_read_mail_page.read_mail()
        self.step_msg(f'Assert mail subject "{subject}" contains "{mail_subject}"')
        assert ds['MAIL_SUBJECT'] in subject
        self.step_msg(f'Assert mail content "{content}" contains "{mail_content}"')
        assert ds['MAIL_CONTENT'] in content


if __name__ == '__main__':
    # pass
    # debug
    # import time, os
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    directory = os.path.join(Settings.BASE_DIR, 'Report', 'TestMail', now)
    pytest.main(
        ['TestMail.py::TestMail::test_send_mail', '--alluredir', directory + '/json'])
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)



