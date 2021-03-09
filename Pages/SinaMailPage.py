"""
   sina mail login page
"""

MAIL_ADDR = 'id=freename'
MAIL_PASSWORD = 'id=freepassword'
LOGIN = 'XPATH=//div[@class="freeMailbox"]//a[@class="loginBtn"]'

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

"""
    mail edit area
"""
SEND_TO = 'XPATH=//tr[@class="fwReceiver"]//ul//input'
SUBJECT = 'xpath=//input[@name="subj"]'
BODY_IFRAME = 'XPATH=//div[@id="SinaEditor"]/iframe'
BODY = 'xpath=//body'
SEND_NOW = 'xpath=//i[text()="发送"]'

"""
   in box mail list
"""
IN_BOX_MAIL_LIST = 'xpath=//div[@id="maillist"]//div[@class="classData"]//div[@class="tbl_mList mailli"]'
MAIL_LIST_SUBJECT = 'xpath=//div[@id="maillist"]//div[@class="tbl_mList mailli"]//a[@class="subject spec"]/span[contains(text(), "${mail_content}")]/..'

"""
   right mail reading area
"""
READ_MAIL_SUBJECT = 'XPATH=//div[@class="subCBody"]//span[@class="subject"]'
READ_MAIL_CONTENT = 'xpath=//div[@class="subCBody"]//div[@class="mailMainArea"]'


