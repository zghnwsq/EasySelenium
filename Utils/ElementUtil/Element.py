# coding=utf-8

from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By


class Element:

    def __init__(self, dr: WebDriver):
        self.dr = dr

    def id(self, ele_id):
        return self.dr.find_element_by_id(ele_id)

    def xpath(self, xpath):
        return self.dr.find_element_by_xpath(xpath)

    def name(self, name):
        return self.dr.find_element_by_name(name)

    def class_name(self, class_name):
        return self.dr.find_element_by_class_name(class_name)

    def css(self, css_selector):
        return self.dr.find_element_by_css_selector(css_selector)

    def locate(self, locator: list, val='') -> WebElement:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if type(locator) == list and len(locator) > 1:
            method = getattr(self, locator[0])
            pattern = self.__get_pattern(locator[1], val)
            return method(pattern)
        else:
            raise Exception('Wrong locator type or length , actual: %s, %d ' % (str(type(locator)), len(locator)))

    def get(self, locator: str, val='') -> WebElement:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if '=' in locator:
            pattern = self.__split_locator(locator)
            method = getattr(self, pattern[0].lower())
            ptn = self.__get_pattern(pattern[1], val)
            # if '${' in pattern[1] and '}' in pattern[1]:
            #     key = pattern[1][pattern[1].find('${'): pattern[1].find('}') + 1]
            #     if val:
            #         ptn = ptn.replace(key, val)
            #     else:
            #         raise Exception('Locator required val input: %s = %s' % (str(key), str(val)))
            return method(ptn)
        else:
            raise Exception('Wrong locator format, actual: %s ' % str(locator))

    def _id(self, ele_id):
        return self.dr.find_elements_by_id(ele_id)

    def _xpath(self, xpath):
        return self.dr.find_elements_by_xpath(xpath)

    def _name(self, name):
        return self.dr.find_elements_by_name(name)

    def _class_name(self, class_name):
        return self.dr.find_elements_by_class_name(class_name)

    def _css(self, css_selector):
        return self.dr.find_elements_by_css_selector(css_selector)

    def locates(self, locator: list, val='') -> list:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if type(locator) == list and len(locator) > 1:
            method = getattr(self, '_'+locator[0])
            pattern = self.__get_pattern(locator[1], val)
            return method(pattern)
        else:
            raise Exception('Wrong locator type or length , actual: %s, %d ' % (str(type(locator)), len(locator)))

    def gets(self, locator: str, val='') -> list:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if '=' in locator:
            pattern = self.__split_locator(locator)
            method = getattr(self, '_'+pattern[0].lower())
            ptn = self.__get_pattern(pattern[1], val)
            return method(ptn)
        else:
            raise Exception('Wrong locator format, actual: %s ' % str(locator))

    @staticmethod
    def __get_pattern(locator, val):
        """
        如果定位字符串中要求输入参数，则将参数名替换成参数值后返回
        :param locator: 定位字符串
        :param val: 输入参数值
        :return: 转化后的定位字符串，如无参数则原样返回
        """
        pattern = locator
        if '${' in locator and '}' in locator:
            key = locator[locator.find('${'): locator.find('}') + 1]
            if val:
                pattern = pattern.replace(key, str(val))
            else:
                raise Exception('Locator required val input: %s = %s' % (str(key), str(val)))
        return pattern

    @staticmethod
    def __split_locator(locator):
        loc = list()
        loc.append(locator[:locator.find('=')])
        loc.append(locator[locator.find('=')+1:])
        return loc

    def wait_until_disappeared(self, locator: str, val='', wait=10):
        t = wait
        # ele = self.get(locator, val).is_displayed()
        loc = self.__split_locator(locator)
        by = getattr(By, loc[0].upper())
        ele = self.dr.find_element(by, loc[1]).is_displayed()
        while ele and t > 0:
            ele = self.dr.find_element(loc[0], loc[1]).is_displayed()
            time.sleep(1)
            t -= 1
        # wait = WebDriverWait(self.dr, wait)
        # wait.until(invisibility_of_element(self.get(locator, val)))

    def wait_until_displayed(self, locator: str, val='', wait=10):
        wait = WebDriverWait(self.dr, wait)
        wait.until(visibility_of(self.get(locator, val)))

    def click_by_js(self, locator: str, val=''):
        self.dr.execute_script('arguments[0].click()', self.get(locator, val))

    def is_displayed(self, locator: str, val=''):
        try:
            return self.get(locator, val)
        except WebDriverException as e:
            return False
