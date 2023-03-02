"""
@Time ： 2022/4/13 10:29
@Auth ： Ted
@File ：SinaMailReadMailPage.py
@IDE ：PyCharm
"""
import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver
from Utils.ElementUtil.Element import Element


class SinaMailReadMailPage(Element):

    # def __init__(self, dr: WebDriver, el: Element = None):
    #     if el is not None:
    #         super(SinaMailReadMailPage, self).__init__(el.dr, el.logger)
    #     else:
    #         super(SinaMailReadMailPage, self).__init__(dr)

    def read_mail(self):
        time.sleep(20)
        subject = self.get(self.READ_MAIL_SUBJECT).text
        content = self.get(self.READ_MAIL_CONTENT).text
        return subject, content

    """
       right mail reading area
    """
    READ_MAIL_SUBJECT = 'XPATH=//div[@class="subCBody"]//span[@class="subject"]'
    READ_MAIL_CONTENT = 'xpath=//div[@class="subCBody"]//div[@class="mailMainArea"]'
