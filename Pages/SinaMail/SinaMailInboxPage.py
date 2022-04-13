"""
@Time ： 2022/4/13 10:23
@Auth ： Ted
@File ：SinaMailInboxPage.py
@IDE ：PyCharm
"""
import time
from selenium.webdriver.remote.webdriver import WebDriver
from Pages.SinaMail.SinaMailReadMailPage import SinaMailReadMailPage
from Utils.ElementUtil.Element import Element


class SinaMailInboxPage(Element):

    def __init__(self, dr: WebDriver, el: Element = None):
        if el is not None:
            super(SinaMailInboxPage, self).__init__(el.dr, el.logger)
        else:
            super(SinaMailInboxPage, self).__init__(dr)

    def click_mail(self, mail_content):
        self.wait_until_clickable(self.MAIL_LIST_SUBJECT, mail_content)
        self.click(self.MAIL_LIST_SUBJECT, mail_content)
        # self.click('xpath=//div[@id="maillist"]//div[@class="tbl_mList mailli"]//a[@class="subject spec"]/span[contains(text(), "${mail_content}")]/..', mail_content)
        return SinaMailReadMailPage(self.dr)

    """
       in box mail list
    """
    IN_BOX_MAIL_LIST = 'xpath=//div[@id="maillist"]//div[@class="classData"]//div[@class="tbl_mList mailli"]'
    MAIL_LIST_SUBJECT = 'xpath=//div[@id="maillist"]//div[@class="tbl_mList mailli"]//a[@class="subject spec"]/span[contains(text(), "${mail_content}")]/..'
