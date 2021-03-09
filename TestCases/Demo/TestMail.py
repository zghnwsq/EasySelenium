import os
import allure
import pytest
import Settings
from Utils.Browser.WebBrowser import chrome, close_down
from Utils.ElementUtil.Element import Element
from Utils.Report.Log import logger
from Pages import SinaMailPage
import time
from Utils.Runner import Cmd
from Utils.Yaml import yaml

file_path = os.path.join(Settings.BASE_DIR, 'DS', 'TestMail', 'TestMail.yaml')


class TestMail:

    def setup_method(self):
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'], args=['--window-size=1920,1080', '--headless'])
        self.driver.delete_all_cookies()
        self.log = logger('info')
        self.el = Element(self.driver, self.log)
        self.dpi = Settings.DPI

    def teardown_method(self):
        close_down(self)

    @allure.step
    def step_msg(self, msg):
        pass

    @pytest.mark.parametrize('ds', yaml.read_yaml(file_path)['valid_cases'])
    def test_send_mail(self, ds, dsrange):
        self._testMethodDoc = ds['desc']
        Cmd.choose_case(ds, dsrange)
        self.el.open_url(ds['URL'])
        self.step_msg('Login')
        self.el.get(SinaMailPage.MAIL_ADDR).clear()
        self.el.input(SinaMailPage.MAIL_ADDR, text=ds['MAIL_ADDR'])
        self.el.input(SinaMailPage.MAIL_PASSWORD, text=ds['MAIL_PASSWORD'])
        self.el.click(SinaMailPage.LOGIN)
        self.step_msg('Send mail')
        self.el.click(SinaMailPage.MAIL_INDEX)
        self.driver.refresh()
        time.sleep(1)
        old_count = int(self.el.get(SinaMailPage.UNREAD_PRE).text)
        self.step_msg(f'old count: {old_count}')
        self.el.click(SinaMailPage.WRITE_MAIL)
        self.el.switch_to_frame(SinaMailPage.BODY_IFRAME)
        mail_content = ds["MAIL_CONTENT"] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        mail_subject = ds['MAIL_SUBJECT']
        self.driver.execute_script(f'document.querySelector("body").innerHTML="{mail_content}"')
        self.el.switch_to_default_content()
        self.el.input(SinaMailPage.SUBJECT, text=mail_subject)
        self.el.input(SinaMailPage.SEND_TO, text=ds['MAIL_ADDR'])
        self.el.click(SinaMailPage.SEND_NOW)
        img = self.el.catch_screen_as_png(dpi=self.dpi)
        allure.attach(img, '发送邮件', allure.attachment_type.PNG)
        self.step_msg('Check mail')
        new_count = 0
        for i in range(10):
            self.el.click(SinaMailPage.CHECK_MAIL)
            self.el.click(SinaMailPage.MAIL_INDEX)
            new_count = int(self.el.get(SinaMailPage.UNREAD_PRE).text)
            if new_count > old_count:
                break
            else:
                time.sleep(1)
        self.step_msg(f'Assert received the mail: new count {new_count} > old count {old_count}')
        assert new_count > old_count
        self.el.click(SinaMailPage.IN_BOX)
        self.el.click(SinaMailPage.MAIL_LIST_SUBJECT, mail_content)
        subject = self.el.get(SinaMailPage.READ_MAIL_SUBJECT).text
        self.step_msg(f'Assert mail subject "{subject}" contains "{mail_subject}"')
        assert ds['MAIL_SUBJECT'] in subject
        content = self.el.get(SinaMailPage.READ_MAIL_CONTENT).text
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
    allure_cmd = f'allure generate -o  {directory}/html  {directory}/json'
    os.system(allure_cmd)






