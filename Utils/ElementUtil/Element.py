# coding=utf-8

import time
import sys
import logging
from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import win32gui
import win32con
import win32api
import base64
from io import BytesIO
from PIL import Image, ImageDraw


class Element:
    """
        元素查找及等待方法封装
    """

    def __init__(self, dr: WebDriver, logger: logging.Logger):
        """
        初始化
        :param dr: WebDriver
        :param logger:日志对象
        """
        self.dr = dr
        self.logger = logger
        self.current_ele = None
        self.frame_chain = []

    def id(self, ele_id) -> WebElement:
        # self.current_ele = None
        self.current_ele = [self.dr.find_element_by_id(ele_id)]
        return self.dr.find_element_by_id(ele_id)

    def xpath(self, xpath) -> WebElement:
        # self.current_ele = None
        self.current_ele = [self.dr.find_element_by_xpath(xpath)]
        return self.dr.find_element_by_xpath(xpath)

    def name(self, name) -> WebElement:
        # self.current_ele = None
        self.current_ele = [self.dr.find_element_by_name(name)]
        return self.dr.find_element_by_name(name)

    def class_name(self, class_name) -> WebElement:
        # self.current_ele = None
        self.current_ele = [self.dr.find_element_by_class_name(class_name)]
        return self.dr.find_element_by_class_name(class_name)

    def css(self, css_selector) -> WebElement:
        # self.current_ele = None
        self.current_ele = [self.dr.find_element_by_css_selector(css_selector)]
        return self.dr.find_element_by_css_selector(css_selector)

    # def locate(self, locator: list, val='') -> WebElement or None:
    #     """
    #     ！！！！废弃！！！！
    #     键值对方式调用定位方法返回元素，支持输入动态变量
    #     :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
    #     :param val:输入动态变量值
    #     :return: WebElement
    #     """
    #     if type(locator) == list and len(locator) > 1:
    #         method = getattr(self, locator[0])
    #         pattern = self.__eval_pattern(locator[1], val)
    #         ele = None
    #         try:
    #             ele = method(pattern)
    #         except WebDriverException as e:
    #             print('Locate失败 locator: %s, %s' % (locator, val))
    #             print(e)
    #             # return None
    #         return ele
    #     else:
    #         raise Exception('Wrong locator type or length , actual: %s, %d ' % (str(type(locator)), len(locator)))

    def get(self, locator: str, val='', log='on') -> WebElement:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param log: 是否记录到log
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if 'on' in log:
            self.logger.info(f'Get Element: {locator} , {val}')
        if '=' in locator:
            pattern = self.__split_locator(locator)
            method = getattr(self, pattern[0].lower())
            ptn = self.__eval_pattern(pattern[1], val)
            ele = None
            try:
                ele = method(ptn)
            except WebDriverException as e:
                self.logger.error(f'Fail To Get Element: {locator}, {val}')
                print(e)
            return ele
        else:
            raise Exception(f'Wrong locator format, actual: {locator:s} ')

    def _id(self, ele_id):
        self.current_ele = None
        self.current_ele = self.dr.find_elements_by_id(ele_id)
        return self.dr.find_elements_by_id(ele_id)

    def _xpath(self, xpath):
        self.current_ele = None
        self.current_ele = self.dr.find_elements_by_xpath(xpath)
        return self.dr.find_elements_by_xpath(xpath)

    def _name(self, name):
        self.current_ele = None
        self.current_ele = self.dr.find_elements_by_name(name)
        return self.dr.find_elements_by_name(name)

    def _class_name(self, class_name):
        self.current_ele = None
        self.current_ele = self.dr.find_elements_by_class_name(class_name)
        return self.dr.find_elements_by_class_name(class_name)

    def _css(self, css_selector):
        self.current_ele = None
        self.current_ele = self.dr.find_elements_by_css_selector(css_selector)
        return self.dr.find_elements_by_css_selector(css_selector)

    # def locates(self, locator: list, val='') -> list:
    #     """
    #     ！！！！废弃！！！！
    #     键值对方式调用定位方法返回元素，支持输入动态变量
    #     :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
    #     :param val:输入动态变量值
    #     :return: WebElement
    #     """
    #     if type(locator) == list and len(locator) > 1:
    #         method = getattr(self, '_'+locator[0])
    #         pattern = self.__eval_pattern(locator[1], val)
    #         try:
    #             eles = method(pattern)
    #         except WebDriverException as e:
    #             print('Locate失败 locator: %s, %s' % (locator, val))
    #             print(e)
    #             return []
    #         return eles
    #     else:
    #         raise Exception('Wrong locator type or length , actual: %s, %d ' % (str(type(locator)), len(locator)))

    def gets(self, locator: str, val='', log='on') -> list:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param log: 是否写入日志
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if 'on' in log:
            self.logger.info('Get ElementS: %s , %s' % (locator, val))
        if '=' in locator:
            pattern = self.__split_locator(locator)
            method = getattr(self, '_'+pattern[0].lower())
            ptn = self.__eval_pattern(pattern[1], val)
            try:
                eles = method(ptn)
            except WebDriverException as e:
                self.logger.error(f'Fail To Get ElementS: {locator}, {val}')
                self.logger.error(e)
                return []
            return eles
        else:
            raise Exception(f'Wrong locator format, actual: {locator:s} ')

    @staticmethod
    def __eval_pattern(locator, val):
        """
        如果定位字符串中要求输入参数，则将参数名替换成参数值后返回
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: 转化后的定位字符串，如无需参数则原样返回 method=pattern with param value or original locator
        """
        pattern = locator
        if '${' in locator and '}' in locator:
            key = locator[locator.find('${'): locator.find('}') + 1]
            if val:
                pattern = pattern.replace(key, str(val))
            else:
                raise Exception(f'Locator required input param : {key:s} = {val:s}')
        return pattern

    @staticmethod
    def __split_locator(locator) -> list:
        """
        分解定位字符串为[定位方法，定位匹配字符串]
        :param locator: 原始定位字符串 method=pattern
        :return: [method，pattern]
        """
        loc = list()
        loc.append(locator[:locator.find('=')])
        loc.append(locator[locator.find('=')+1:])
        return loc

    def open_url(self, url):
        self.logger.info(f'Open url {url}')
        self.dr.get(url)

    def click(self, locator: str, val=''):
        self.logger.info(f'Click on element : {locator}, {val}')
        self.get(locator, val).click()

    def click_by_js(self, locator: str, val=''):
        """
        执行Javascript语句来点击元素
        :param locator: 定位字符串:method=pattern with param name
        :param val:输入参数值 param value
        :return:None
        """
        self.logger.info(f'Click Element By Execute Javascript: {locator}, {val}')
        self.dr.execute_script('arguments[0].click()', self.get(locator, val=val, log='off'))

    def click_on_element(self, locator: str, val=''):
        """
        使用action点击元素
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: None
        """
        # rect = self.get(locator, val=val).rect
        # center_x = int(rect['x']) + int(rect['width']/2)
        # center_y = int(rect['y']) + int(rect['height']/2)
        # win32api.SetCursorPos([center_x, center_y])
        # time.sleep(0.5)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        self.logger.info(f'Click On Element: {locator}, {val}')
        act = ActionChains(self.dr)
        act.move_to_element(self.get(locator, val=val, log='off')).click().perform()

    def input(self, locator: str, val='', text=''):
        self.logger.info(f'Input text {text} on: {locator}, {val}')
        self.get(locator, val).send_keys(text)

    def scroll_into_view(self, locator: str, val=''):
        """
        滚动使元素可见
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: None
        """
        self.logger.info(f'Scroll Into View: {locator}, {val}')
        self.dr.execute_script('arguments[0].scrollIntoView()', self.get(locator, val=val, log='off'))

    def get_matching_element_count(self, locator: str, val=''):
        """
        获取匹配定位字符串的元素个数
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: 匹配的元素个数
        """
        try:
            count = len(self.gets(locator, val=val, log='off'))
            self.logger.info(f'Get Matching Elements Count: {locator}, {val}, {count}')
            return count
        except WebDriverException:
            self.logger.info(f'Get Matching Elements Count: {locator}, {val}, 0')
            return 0

    def wait_until_disappeared(self, locator: str, val='', time_out=10):
        """
        等待元素消失：元素从DOM中被删除
        :param locator: 定位字符串
        :param val:输入参数值
        :param time_out: 等待时间（秒）
        :return: 
        """
        self.logger.info(f'Wait Until Element Disappeared: {locator}, {val}, time out: {time_out}s')
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until_not(presence_of_element_located(self.get(locator, val=val)))
            tp = self._get_by_obj(locator, val=val)
            wait.until(staleness_of(self.dr.find_element(by=tp[0], value=tp[1])))
            self.current_ele = None
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
            self.logger.info(u'%s 元素消失: %s' % (t, locator))
            self.current_ele = None
            return True
        except WebDriverException as e:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.logger.warning(u'%s error: %s' % (t, e.__str__()))
            self.current_ele = None
            return True

    def wait_until_invisible(self, locator: str, val='', time_out=10):
        """
        等待元素不可见，DOM中仍可能存在
        :param locator: 定位字符串
        :param val:输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        self.logger.info(f'Wait Until Element Invisible: {locator}, {val}, time out: {time_out}s')
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until(invisibility_of_element_located(self._get_by_obj(locator, val=val)))
            target = self.get(locator, val=val, log='off')
            if target:
                wait.until(invisibility_of_element_located(target))
                self.current_ele = None
        except StaleElementReferenceException:
            self.logger.info(u'元素消失:' + locator)
            self.current_ele = None
            return True
        except NoSuchElementException:
            self.logger.info(u'元素消失:' + locator)
            self.current_ele = None
            return True
        except WebDriverException as e:
            self.logger.info(e.stacktrace)
            self.current_ele = None
            return True

    def wait_until_displayed(self, locator: str, val='', time_out=10):
        """
        等待元素可见
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return: WebElement
        """
        self.logger.info(f'Wait Until Element Displayed: {locator}, {val}, time out: {time_out}s')
        wait = WebDriverWait(self.dr, time_out)
        return wait.until(visibility_of_element_located(self._get_by_obj(locator, val=val)))

    def wait_until_clickable(self, locator: str, val='', time_out=10):
        """
        等待元素可点击
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return: WebElement
        """
        self.logger.info(f'Wait Until Element Clickable: {locator}, {val}, time out: {time_out}s')
        wait = WebDriverWait(self.dr, time_out)
        return wait.until(element_to_be_clickable(self._get_by_obj(locator, val=val)))

    def wait_until_value_not_null(self, locator: str, val='', time_out=10):
        """
        等待元素的value不为null
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        self.logger.info(f'Wait Until Element Value Not Null: {locator}, {val}, time out: {time_out}s')
        while time_out > 0:
            value = self.get(locator, val=val, log='off').get_attribute('value')
            if value:
                self.logger.info(u' %f value of %s is: %s' % (time_out, locator, value))
                return True
            else:
                time_out -= 0.5
                time.sleep(0.5)

    def wait_until_window_open_and_switch(self, former_hds, time_out=10):
        self.logger.info(f'Wait Until New Window Open, time out: {time_out}s')
        self.logger.info('Former handles: ' + str(former_hds))
        while time_out > 0:
            hds = self.dr.window_handles
            if len(hds) > len(former_hds):
                self.logger.info('New handles: ' + str(hds))
                for hd in hds:
                    if hd not in former_hds:
                        self.dr.switch_to.window(hd)
                        self.current_ele = None
                        self.frame_chain = []
                        break
                break
            else:
                time_out -= 0.5
                time.sleep(0.5)

    def click_and_wait_until_window_open_and_switch(self, locator: str, val='', time_out=10):
        former_hds = self.dr.window_handles
        self.logger.info('Click element: %s, %s' % (locator, val))
        self.get(locator, val).click()
        self.logger.info(f'Wait Until New Window Open, time out: {time_out}s')
        while time_out > 0:
            hds = self.dr.window_handles
            if len(hds) > len(former_hds):
                self.logger.info('New handles: ' + str(hds))
                for hd in hds:
                    if hd not in former_hds:
                        self.dr.switch_to.window(hd)
                        self.current_ele = None
                        self.frame_chain = []
                        break
                break
            else:
                time_out -= 0.5
                time.sleep(0.5)

    def switch_to_frame(self, locator: str, val=''):
        self.logger.info(f'Switch to frame: {locator}, {val}')
        frame = self.get(locator, val)
        loc = frame.location
        self.dr.switch_to.frame(frame)
        self.current_ele = None
        self.frame_chain.append(loc)  # 添加当前frame的相对坐标

    def switch_to_default_content(self):
        self.logger.info('Switch to default content.')
        self.dr.switch_to.default_content()
        self.frame_chain = []  # 切回最上层则清空

    def switch_to_parent_frame(self):
        self.logger.info('Switch to parent frame.')
        self.dr.switch_to.parent_frame()
        if self.frame_chain:
            self.frame_chain.pop()  # 切回父frame则删除当前frame相对坐标

    def switch_to_alert(self):
        self.logger.info('Switch to alert.')
        self.dr.switch_to.alert()

    def switch_to_window(self, handle):
        self.logger.info(f'Switch to window: {handle}')
        self.dr.switch_to.window(handle)

    def __draw_line(self, base64_data, dpi):
        coords = []
        parent_xy = {'x': 0, 'y': 0}  # 父frame坐标,嵌套frame，坐标累加
        if self.frame_chain:
            for frame in self.frame_chain:
                parent_xy['x'] += frame['x']
                parent_xy['y'] += frame['y']
        for ele in self.current_ele:
            size = ele.size  # width height
            # loc = ele.location  # x y
            # 相对于视窗的实际坐标  left top x y right bottom
            actual_loc = self.dr.execute_script('return arguments[0].getBoundingClientRect()', ele)
            abs_loc = {'x': actual_loc['x'] + parent_xy['x'], 'y': actual_loc['y'] + parent_xy['y']}  # 相对于窗口绝对坐标
            coords.append(dict(abs_loc, **size))
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        draw = ImageDraw.ImageDraw(img)
        for items in coords:
            # (左上x y 右下x y) outline线条颜色 width线宽
            if items['x'] > 0 and items['y'] > 0:
                draw.rectangle((items['x'] * dpi, items['y'] * dpi, (items['x'] + items['width']) * dpi,
                                (items['y'] + items['height']) * dpi),
                               outline='yellow',
                               width=3)
        output_buffer = BytesIO()
        img.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        return byte_data

    def catch_screen(self, dpi=1.0):
        # 2020.10.14 增加截图上框出上一定位元素功能
        time.sleep(1)
        if self.current_ele:
            base64_data = self.dr.get_screenshot_as_base64()
            byte_data = self.__draw_line(base64_data, dpi)
            base64_str = base64.b64encode(byte_data).decode(encoding='UTF-8')
            return base64_str
        else:
            return self.dr.get_screenshot_as_base64()

    def catch_screen_as_png(self, dpi=1.0):
        time.sleep(1)
        if self.current_ele:
            base64_data = self.dr.get_screenshot_as_base64()
            byte_data = self.__draw_line(base64_data, dpi)
            return byte_data
        else:
            return self.dr.get_screenshot_as_png()

    def is_displayed(self, locator: str, val=''):
        try:
            flag = self.get(locator, val=val, log='off').is_displayed()
            self.logger.info(u'Element: %s, %s Is Displayed, True Or False?: %s' % (locator, val, str(flag)))
            return flag
        except WebDriverException as e:
            return False

    def _get_by_obj(self, locator, val=''):
        """
        获取By对象
        :param locator: 定位字符串
        :param val: 输入参数值
        :return:
        """
        evaled_locator = self.__eval_pattern(locator, val)
        loc = self.__split_locator(evaled_locator)
        if loc[0].strip().lower() == 'id':
            obj = (By.ID, loc[1])
            return obj
        elif loc[0].strip().lower() == 'xpath':
            obj = (By.XPATH, loc[1])
            return obj
        elif loc[0].strip().lower() == 'name':
            obj = (By.NAME, loc[1])
            return obj
        elif loc[0].strip().lower() == 'class_name':
            obj = (By.CLASS_NAME, loc[1])
            return obj
        elif loc[0].strip().lower() == 'css':
            obj = (By.CSS_SELECTOR, loc[1])
            return obj
