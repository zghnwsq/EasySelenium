"""
@Time ： 2022/4/13 10:04
@Auth ： Ted
@File ：SinaMailIndexPage.py
@IDE ：PyCharm
"""
import logging
import time
from selenium.webdriver.remote.webdriver import WebDriver
from Pages.SinaMail.SinaMailEditPage import SinaMailEditPage
from Pages.SinaMail.SinaMailInboxPage import SinaMailInboxPage
from Utils.ElementUtil.Element import Element


class SinaMailIndexPage(Element):

    def __init__(self, dr: WebDriver, el: Element = None):
        if el is not None:
            super(SinaMailIndexPage, self).__init__(el.dr, el.logger)
        else:
            super(SinaMailIndexPage, self).__init__(dr)

    def open_write_mail(self):
        self.click(self.MAIL_INDEX)
        self.dr.refresh()
        time.sleep(1)
        old_count = int(self.get(self.UNREAD_PRE).text)
        self.logger.info(f'old count: {old_count}')
        self.click(self.WRITE_MAIL)
        return old_count, SinaMailEditPage(self.dr)

    def wait_new_mail(self, old_count):
        new_count = 0
        for i in range(10):
            self.click(self.CHECK_MAIL)
            self.wait_until_clickable(self.MAIL_INDEX)
            self.click(self.MAIL_INDEX)
            self.wait_until_displayed(self.UNREAD_PRE)
            new_count = int(self.get(self.UNREAD_PRE).text or 0)
            if new_count > old_count:
                time.sleep(1)
                break
            else:
                time.sleep(1)
        return new_count, SinaMailInboxPage(self.dr)

    def into_inbox(self):
        self.click(self.IN_BOX)

    """
       mail index
    """
    MAIL_INDEX = 'xpath=//li[@title="邮箱首页"]'
    UNREAD_PRE = 'xpath=//b[@id="unread_num_all"]/i[1]'
    UNREAD_NEXT = 'xpath=//b[@id="unread_num_all"]/i[1]'

    """
       left navigator bar
    """
    WRITE_MAIL = 'XPATH=//a[@title="写信"]'
    CHECK_MAIL = 'XPATH=//li[@class="wrReceiveBtn"]//a[text()="收信"]'
    IN_BOX = 'xpath=//a[text()="收件夹"]'

