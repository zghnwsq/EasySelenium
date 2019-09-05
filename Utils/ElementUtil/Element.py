# coding=utf-8

import time
from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import win32gui
import win32con
import win32api


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

    def locate(self, locator: list, val='') -> WebElement or None:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if type(locator) == list and len(locator) > 1:
            method = getattr(self, locator[0])
            pattern = self.__get_pattern(locator[1], val)
            ele = None
            try:
                ele = method(pattern)
            except WebDriverException as e:
                print('Locate失败 locator: %s, %s' % (locator, val))
                print(e)
                # return None
            return ele
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
            ele = None
            try:
                ele = method(ptn)
            except WebDriverException as e:
                print('Get失败 locator: %s, %s' % (locator, val))
                print(e)
                # return None
            return ele
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
            try:
                eles = method(pattern)
            except WebDriverException as e:
                print('Locate失败 locator: %s, %s' % (locator, val))
                print(e)
                return []
            return eles
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
            try:
                eles = method(ptn)
            except WebDriverException as e:
                print('Get失败 locator: %s, %s' % (locator, val))
                print(e)
                return []
            return eles
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

    def click_by_js(self, locator: str, val=''):
        self.dr.execute_script('arguments[0].click()', self.get(locator, val=val))

    def click_on_element(self, locator: str, val=''):
        # rect = self.get(locator, val=val).rect
        # center_x = int(rect['x']) + int(rect['width']/2)
        # center_y = int(rect['y']) + int(rect['height']/2)
        # win32api.SetCursorPos([center_x, center_y])
        # time.sleep(0.5)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        act = ActionChains(self.dr)
        act.move_to_element(self.get(locator, val=val)).click().perform()

    def scroll_into_view(self, locator: str, val=''):
        self.dr.execute_script('arguments[0].scrollIntoView()', self.get(locator, val=val))

    def wait_until_disappeared(self, locator: str, val='', time_out=10):
        """
        等待元素消失：元素从DOM中被删除
        :param locator: 定位字符串
        :param val:输入参数值
        :param time_out: 等待时间（秒）
        :return: 
        """
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until_not(presence_of_element_located(self.get(locator, val=val)))
            tp = self._get_by_obj(locator, val=val)
            wait.until(staleness_of(self.dr.find_element(by=tp[0], value=tp[1])))
            # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            # while time_out > 0:
            #     ele = self.get(locator, val=val)
            #     if not ele:
            #         print(u'\r\n' + str(time_out) + ' 元素不存在:' + locator)
            #         return True
            #     else:
            #         print(u'元素仍存在:' + locator)
            #         time_out -= 0.5
            #         print(u'剩余等待时间:' + str(time_out))
            #         time.sleep(0.5)
        except NoSuchElementException:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(u'%s 元素不存在了: %s' % (t, locator))
            return True
        except WebDriverException:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(u'%s error: ' % t)
            return True

    def wait_until_invisible(self, locator: str, val='', time_out=10):
        """
        等待元素不可见，DOM中仍可能存在
        :param locator: 定位字符串
        :param val:输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until_not(visibility_of(self.get(locator, val=val)))
            # wait.until_not(visibility_of_element_located(self._get_by_obj(locator, val=val)))
            wait.until(invisibility_of_element_located(self._get_by_obj(locator, val=val)))
        except StaleElementReferenceException:
            print(u'元素不存在了:' + locator)
            return True
        except NoSuchElementException:
            print(u'元素不存在了:' + locator)
            return True

    def wait_until_displayed(self, locator: str, val='', time_out=10):
        wait = WebDriverWait(self.dr, time_out)
        # wait.until(visibility_of(self.get(locator, val=val)))
        wait.until(visibility_of_element_located(self._get_by_obj(locator, val=val)))

    def wait_until_value_not_null(self, locator: str, val='', time_out=10):
        while time_out > 0:
            value = self.get(locator, val=val).get_attribute('value')
            if value:
                print(u' %f value of %s is: %s' % (time_out, locator, value))
                return True
            else:
                time_out -= 0.5
                # print(u'剩余等待时间:' + str(time_out))
                time.sleep(0.5)

    def is_displayed(self, locator: str, val=''):
        try:
            return self.get(locator, val=val).is_displayed()
        except WebDriverException as e:
            return False

    def _get_by_obj(self, locator, val=''):
        evaled_locator = self.__get_pattern(locator, val)
        loc = self.__split_locator(evaled_locator)
        if loc[0].strip() == 'id':
            obj = (By.ID, loc[1])
            return obj
        elif loc[0].strip() == 'xpath':
            obj = (By.XPATH, loc[1])
            return obj
        elif loc[0].strip() == 'name':
            obj = (By.NAME, loc[1])
            return obj
        elif loc[0].strip() == 'class_name':
            obj = (By.CLASS_NAME, loc[1])
            return obj
        elif loc[0].strip() == 'css':
            obj = (By.CSS_SELECTOR, loc[1])
            return obj
