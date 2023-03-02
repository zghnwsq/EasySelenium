"""
@Time ： 2022/4/13 10:10
@Auth ： Ted
@File ：SinaMailEditPage.py
@IDE ：PyCharm
"""
import time
from selenium.webdriver.remote.webdriver import WebDriver
import Settings
from Utils.ElementUtil.Element import Element


class SinaMailEditPage(Element):

    def __init__(self, dr: WebDriver, el: Element = None):
        if el is not None:
            super(SinaMailEditPage, self).__init__(el.dr, el.logger)
        else:
            super(SinaMailEditPage, self).__init__(dr)

    def send_mail(self, ds, mail_subject='', mail_content=''):
        # self.el.input(SinaMailLoginPage.SEND_TO, text=ds['MAIL_ADDR'])
        self.dr.execute_script(f'arguments[0].value="{ds["MAIL_ADDR"]}"', self.get(self.SEND_TO))
        self.wait_until_displayed(self.SEND_TO_ADDR, ds['MAIL_ADDR'])
        self.input(self.SUBJECT, text=mail_subject)
        self.click(self.SUBJECT)
        time.sleep(0.5)
        self.switch_to_frame(self.BODY_IFRAME)
        self.wait_until_displayed(self.BODY)
        self.click(self.BODY)
        self.dr.execute_script(f'document.querySelector("body").innerHTML="{mail_content}"')
        self.switch_to_default_content()
        self.click(self.SEND_NOW)
        # img = sina_mail_page.catch_screen_as_png(dpi=self.dpi)
        # allure.attach(img, '发送邮件', allure.attachment_type.PNG)
        self.allure_catch_screen(dpi=Settings.DPI, tag='发送邮件')

    """
        mail edit area
    """
    SEND_TO = 'XPATH=//tr[@class="fwReceiver"]//ul//input'
    SEND_TO_ADDR = 'XPATH=//tr[@class="fwReceiver"]//ul//li//span[contains(text(),"${mail_addr}")]'
    SUBJECT = 'xpath=//input[@name="subj"]'
    BODY_IFRAME = 'XPATH=//div[@id="SinaEditor"]/iframe'
    BODY = 'xpath=//body'
    SEND_NOW = 'xpath=//i[text()="发送"]'



