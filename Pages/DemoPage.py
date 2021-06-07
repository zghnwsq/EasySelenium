# coding=utf-8

"""
    页面元素定位
"""
# iframe
IFRAME = 'id=iframeResult'
# 按钮
BUTTON = 'xpath=//button[text()="${text}"]'
# 方形
SQUARE = 'id=div3'

"""
    百度
"""
KW = 'id=kw'
SEARCH = 'id=su'
RES = 'xpath=//div[contains(@class,"result")]//a//*[string()="${kw}"]/..'
# TEACHER = 'xpath=//span[text()="测试免费公开课"]'
TEACHER = 'XPATH=//h3[contains(text(), "明星老师")]'
ROY = 'XPATH=//h4[contains(text(), "Roy")]/../../..//img'
WILL = 'XPATH=//h4[contains(text(), "Will")]/../../..//img'
TUFEI = 'XPATH=//h4[contains(text(), "土匪")]/../../..//img'

