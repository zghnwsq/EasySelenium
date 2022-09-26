# coding=utf-8
import os
import time
# import sys
import logging
from logging.config import dictConfig
import allure
import numpy
from cv2 import cv2
# import pyautogui
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# import win32gui
# import win32con
# import win32api
import base64
from io import BytesIO
from PIL import Image, ImageDraw
from Utils.Image.recognizer import get_center_of_target, get_dpi, get_center_of_target_by_feature_matching
from Utils.LogConfig import LogConfig


class Element:
    """
        元素查找及等待方法封装
    """

    def __init__(self, dr: WebDriver, imgs: list = None, logger: logging.Logger = None):
        """
        初始化
        :param dr: WebDriver
        :param imgs: 截图列表
        :param logger:日志对象
        """
        self.dr = dr
        if logger is None:
            dictConfig(LogConfig.CONFIG)
            self.logger = logging.getLogger('default')
            # self.logger = logging.getLogger()
            # self.logger.setLevel('INFO')
        else:
            self.logger = logger
        self.imgs = imgs if imgs is not None else []
        self.current_ele = None
        self.frame_chain = []

    def step(self, step_name):
        self.logger.info(
            f'<font class="log-bold" style="color: green; font-weight: larger">{"#" * 30}STEP: {step_name} {"#" * 30}</font>')

    def get(self, locator: str, val='', log='on') -> WebElement:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param log: 是否记录到log
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if 'on' in log:
            self.logger.info(f'Get Element: <font class="log-bold">{locator} , {val}</font>')
        if '=' in locator:
            pattern = self.__split_locator(locator)
            # method = getattr(self, pattern[0].lower())
            mtd = getattr(By, pattern[0].upper())
            ptn = self.__eval_pattern(pattern[1], val)
            ele = None
            try:
                # ele = method(ptn)
                ele = self.dr.find_element(mtd, ptn)
                self.current_ele = [ele]
            except WebDriverException as e:
                self.logger.error(f'<font class="log-error">Fail To Get Element: {locator}, {val}</font>')
                print(e)
            return ele
        else:
            raise Exception(f'<font class="log-error">Wrong locator format, actual: {locator:s} </font>')

    def gets(self, locator: str, val='', log='on') -> list:
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param log: 是否写入日志
        :param locator: method=pattern格式的定位字符串
        :param val:输入动态变量值
        :return: WebElement
        """
        if 'on' in log:
            self.logger.info('Get ElementS: <font class="log-bold">%s , %s</font>' % (locator, val))
        if '=' in locator:
            pattern = self.__split_locator(locator)
            # method = getattr(self, '_'+pattern[0].lower())
            mtd = getattr(By, pattern[0].upper())
            ptn = self.__eval_pattern(pattern[1], val)
            try:
                # eles = method(ptn)
                eles = self.dr.find_elements(mtd, ptn)
                self.current_ele = eles
            except WebDriverException as e:
                self.logger.error(f'<font class="log-error">Fail To Get ElementS: {locator}, {val}</font>')
                self.logger.error(e)
                return []
            return eles
        else:
            raise Exception(f'<font class="log-error">Wrong locator format, actual: {locator:s} </font>')

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
                raise Exception(f'<font class="log-error">Locator required input param : {key:s} = {val:s}</font>')
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
        loc.append(locator[locator.find('=') + 1:])
        return loc

    def open_url(self, url):
        self.logger.info(f'Open url {url}')
        self.dr.get(url)

    def click(self, locator: str, val=''):
        self.logger.info(f'Click on element : <font class="log-bold">{locator}, {val}</font>')
        self.get(locator, val, log='off').click()

    def double_click(self, locator: str, val=''):
        self.logger.info(f'Double click on element : <font class="log-bold">{locator}, {val}</font>')
        act = ActionChains(self.dr)
        act.double_click(self.get(locator, val, log='off')).perform()

    def click_by_js(self, locator: str, val=''):
        """
        执行Javascript语句来点击元素
        :param locator: 定位字符串:method=pattern with param name
        :param val:输入参数值 param value
        :return:None
        """
        self.logger.info(f'Click Element By Execute Javascript: <font class="log-bold">{locator}, {val}</fonnt>')
        self.dr.execute_script('arguments[0].click()', self.get(locator, val=val, log='off'))

    # def click_by_pyautogui(self, locator: str, val=''):
    #     """
    #     使用pyautogui来移动鼠标点击
    #     :param locator: 定位字符串:method=pattern with param name
    #     :param val:输入参数值 param value
    #     :return:None
    #     """
    #     win_position = self.dr.get_window_position()
    #     win_size = self.dr.get_window_size()
    #     html_size = self.get('xpath=/html', log='off').size
    #     x_offset = (win_size['width'] - html_size['width']) // 2
    #     # y方向有工具栏地址栏对称，底边距约等于左边距
    #     y_offset = win_size['height'] - html_size['height'] - x_offset
    #     ele_rect = self.get(locator, val=val, log='off').rect
    #     x = win_position['x'] + x_offset + ele_rect['x'] + ele_rect['width'] // 2
    #     y = win_position['y'] + y_offset + ele_rect['y'] + ele_rect['height'] // 2
    #     self.logger.info(f'Click Element By Pyautogui: <font class="log-bold">{locator}, {val}, x: {x}, y: {y}</font>')
    #     pyautogui.click(x=x, y=y)

    def click_on_element(self, locator: str, val=''):
        """
        使用action点击元素
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: None
        """
        self.logger.info(f'Click On Element: <font class="log-bold">{locator}, {val}</font>')
        act = ActionChains(self.dr)
        act.move_to_element(self.get(locator, val=val, log='off')).click().perform()

    def input(self, locator: str, val='', text=''):
        self.logger.info(f'Input text on element: <font class="log-bold">{text}, {locator}, {val}</font>')
        self.get(locator, val, log='off').send_keys(text)

    def execute_javascript(self, script: str, locator: str = None, val=''):
        """
        执行Javascript语句
        :param script: javascript code
        :param locator: 定位字符串:method=pattern with param name
        :param val:输入参数值 param value
        :return: JavaScript returns
        """
        self.logger.info(f'Execute Javascript: <font class="log-bold">{script}, Element: {locator}, {val}</fonnt>')
        if locator:
            element = self.get(locator, val, log='off')
            return self.dr.execute_script(script, element)
        else:
            return self.dr.execute_script(script)

    def scroll_into_view(self, locator: str, val=''):
        """
        滚动使元素可见
        :param locator: 定位字符串:method=pattern with param name
        :param val: 输入参数值 param value
        :return: None
        """
        self.logger.info(f'Scroll Into View: <font class="log-bold">{locator}, {val}</font>')
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
            self.logger.info(f'Get Matching Elements Count: <font class="log-bold">{locator}, {val}, {count}</font>')
            return count
        except WebDriverException:
            self.logger.info(f'<font class="log-error">Get Matching Elements Count: {locator}, {val}, 0</font>')
            return 0

    def wait_until_disappeared(self, locator: str, val='', time_out=10):
        """
        等待元素消失：元素从DOM中被删除
        :param locator: 定位字符串
        :param val:输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        self.logger.info(
            f'Wait Until Element Disappeared: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until_not(presence_of_element_located(self.get(locator, val=val)))
            tp = self._get_by_obj(locator, val=val)
            wait.until(ec.staleness_of(self.dr.find_element(by=tp[0], value=tp[1])))
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
        self.logger.info(
            f'Wait Until Element Invisible: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        wait = WebDriverWait(self.dr, time_out)
        try:
            # wait.until(invisibility_of_element_located(self._get_by_obj(locator, val=val)))
            target = self.get(locator, val=val, log='off')
            if target:
                wait.until(ec.invisibility_of_element_located(target))
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
        self.logger.info(
            f'Wait Until Element Displayed: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        wait = WebDriverWait(self.dr, time_out)
        return wait.until(ec.visibility_of_element_located(self._get_by_obj(locator, val=val)))

    def wait_until_clickable(self, locator: str, val='', time_out=10):
        """
        等待元素可点击
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return: WebElement
        """
        self.logger.info(
            f'Wait Until Element Clickable: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        wait = WebDriverWait(self.dr, time_out)
        return wait.until(ec.element_to_be_clickable(self._get_by_obj(locator, val=val)))

    def wait_until_selected(self, locator: str, val='', time_out=10):
        """
        等待checkbox或radio已选择
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        self.logger.info(
            f'Wait Until Element Selected: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        wait = WebDriverWait(self.dr, time_out)
        return wait.until(ec.element_located_to_be_selected(self._get_by_obj(locator, val=val)))

    def wait_until_value_not_null(self, locator: str, val='', time_out=10):
        """
        等待元素的value不为null
        :param locator: 定位字符串
        :param val: 输入参数值
        :param time_out: 等待时间（秒）
        :return:
        """
        self.logger.info(
            f'Wait Until Element Value Not Null: <font class="log-bold">{locator}, {val}, time out: {time_out}s</font>')
        while time_out > 0:
            value = self.get(locator, val=val, log='off').get_attribute('value')
            if value:
                self.logger.info(u' %f value of %s is: %s' % (time_out, locator, value))
                return True
            else:
                time_out -= 0.5
                time.sleep(0.5)
        return False

    def wait_until_window_open_and_switch(self, former_hds, time_out=10):
        """
            等待新窗口打开，并切换
        :param former_hds: 窗口打开之前的handlers列表
        :param time_out: 超时时间，默认10s
        :return: new window handle
        """
        self.logger.info(f'Wait Until New Window Open, time out: {time_out}s')
        self.logger.info('Former handles: ' + str(former_hds))
        expired_time = time.time() + time_out
        while True:
            hds = self.dr.window_handles
            if len(hds) > len(former_hds):
                self.logger.info('New handles: ' + str(hds))
                for hd in hds:
                    if hd not in former_hds:
                        self.switch_to_window(hd)
                        # self.dr.switch_to.window(hd)
                        self.current_ele = None
                        self.frame_chain = []
                        # break
                        return hd
                # break
            else:
                if time.time() > expired_time:
                    break
        return None

    def switch_window_by_title(self, title: str):
        """
            根据窗口title切换窗口
        :param title: title
        :return: True or False
        """
        windows = self.dr.window_handles
        for window in windows:
            self.dr.switch_to.window(windows)
            if window.title() == title:
                self.logger.info(f'Switch to window: <font class="log-bold">{title}</font>')
                return True
        self.logger.info(f'<font class="log-error">Window not exists: {title}</font>')
        return False

    def click_and_wait_until_window_open_and_switch(self, locator: str, val='', time_out=10):
        """
            点击元素，等待新窗口打开，并切换
        :param locator:  定位字符串
        :param val: 输入参数值
        :param time_out: 超时时间，默认10s
        :return: None
        """
        former_hds = self.dr.window_handles
        self.logger.info('Click element:<font class="log-bold"> %s, %s</font>' % (locator, val))
        self.get(locator, val, log='off').click()
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

    def wait_until_alert_and_switch(self, time_out=10):
        """
        等待alert可见并切换
        :param time_out: 等待时间（秒）
        :return: Alert
        """
        expired_time = time.time() + time_out
        self.logger.info(f'Wait Until Alert Present: time out: {time_out}s')
        wait = WebDriverWait(self.dr, time_out)
        while True:
            alert = wait.until(ec.alert_is_present())
            if not isinstance(alert, bool):
                break
            if time.time() > expired_time:
                break
        # return self.switch_to_alert()
        return alert

    def wait_alert_and_dismiss(self, time_out=10):
        """
            等待alert弹出并点击取消，返回文本. 没有弹出不报错.
        :param time_out: 超时时间
        :return: Alert text
        """
        alert_text = 'None'
        try:
            alert = self.wait_until_alert_and_switch(time_out=time_out)
            if not isinstance(alert, bool):
                alert_text = alert.text
                alert.dismiss()
            else:
                alert_text = 'None'
            self.logger.info(f'Alert show message: <font class="log-bold">{alert_text}.</font>')
        except WebDriverException:
            self.logger.info(f'<font class="log-bold">Alert does not show, Continue.</font>')
        return alert_text

    def wait_alert_and_accept(self, time_out=10):
        """
            等待alert弹出并点击确定，返回文本. 没有弹出不报错.
        :param time_out: 超时时间
        :return: Alert text
        """
        alert_text = 'None'
        try:
            alert = self.wait_until_alert_and_switch(time_out=time_out)
            if not isinstance(alert, bool):
                alert_text = alert.text
                alert.accept()
            else:
                alert_text = 'None'
            self.logger.info(f'Alert show message: <font class="log-bold">{alert_text}.</font>')
        except WebDriverException:
            self.logger.info(f'<font class="log-bold">Alert does not show, Continue.</font>')
        return alert_text

    def switch_to_frame(self, locator: str, val=''):
        """
            切换到frame
        :param locator:  定位字符串
        :param val: 输入参数值
        :return: None
        """
        self.logger.info(f'Switch to frame: <font class="log-bold">{locator}, {val}</font>')
        frame = self.get(locator, val, log='off')
        loc = frame.location
        self.dr.switch_to.frame(frame)
        self.current_ele = None
        self.frame_chain.append(loc)  # 添加当前frame的相对坐标

    def switch_to_default_content(self):
        """
            切换到defualt frame
        :return: None
        """
        self.logger.info('Switch to default content.')
        self.dr.switch_to.default_content()
        self.frame_chain = []  # 切回最上层则清空

    def switch_to_parent_frame(self):
        """
            切换到父frame
        :return: None
        """
        self.logger.info('Switch to parent frame.')
        self.dr.switch_to.parent_frame()
        if self.frame_chain:
            self.frame_chain.pop()  # 切回父frame则删除当前frame相对坐标

    def switch_to_alert(self):
        """
           切换到alert
        :return: None
        """
        self.logger.info('Switch to alert.')
        alert = self.dr.switch_to.alert
        return alert

    def switch_to_window(self, handle):
        """
            切换到窗口
        :param handle: Window handle
        :return: None
        """
        self.logger.info(f'Switch to window: <font class="log-bold">{handle}</font>')
        self.dr.switch_to.window(handle)

    def __draw_line(self, base64_data, dpi):
        """
            绘制矩形框
        :param base64_data: 原始图片,base64
        :param dpi: 屏幕dpi
        :return: 绘制后图片,binary data
        """
        coords = []
        parent_xy = {'x': 0, 'y': 0}  # 父frame坐标,嵌套frame，坐标累加
        if self.frame_chain:
            for frame in self.frame_chain:
                parent_xy['x'] += frame['x']
                parent_xy['y'] += frame['y']
        for ele in self.current_ele:
            # 截图时,防止元素不可及
            try:
                size = ele.size  # width height
                # loc = ele.location  # x y
                # 相对于视窗的实际坐标  left top x y right bottom
                actual_loc = self.dr.execute_script('return arguments[0].getBoundingClientRect()', ele)
                abs_loc = {'x': actual_loc['x'] + parent_xy['x'], 'y': actual_loc['y'] + parent_xy['y']}  # 相对于窗口绝对坐标
                coords.append(dict(abs_loc, **size))
            except WebDriverException:
                self.logger.info('元素不可及,跳过标示.')
                continue
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

    def catch_screen(self, dpi=1.0, imgs=None, info=''):
        """
            截图，并绘制上一个定位元素示意框
        :param dpi: 屏幕dpi
        :param imgs: 截图列表,自动追加
        :param info: 日志信息
        :return: 截图, base64
        """
        # return base64 data
        # 2020.10.14 增加截图上框出上一定位元素功能
        # 2021.12.20 增加imgs参数，截图增加在列表后
        time.sleep(1)
        if self.current_ele:
            base64_data = self.dr.get_screenshot_as_base64()
            byte_data = self.__draw_line(base64_data, dpi)
            base64_str = base64.b64encode(byte_data).decode(encoding='UTF-8')
            img_base64 = base64_str
        else:
            img_base64 = self.dr.get_screenshot_as_base64()
        # img_base64 = self.dr.get_screenshot_as_base64()
        # 2022.5.5增加title
        if not info:
            info = '截图'
            img = img_base64
        else:
            img = {'img': img_base64, 'desc': info}
        if imgs is not None:
            imgs.append(img)
        # self.imgs.append(img)
        self.logger.info(f'<font class="log-bold">{info}</font>')
        return img

    def catch_screen_as_png(self, dpi=1.0):
        """
            截图，并返回png格式的binary data
        :param dpi: 屏幕dpi
        :return: png格式的binary data
        """
        # return binary data
        time.sleep(1)
        if self.current_ele:
            base64_data = self.dr.get_screenshot_as_base64()
            byte_data = self.__draw_line(base64_data, dpi)
            return byte_data
        else:
            return self.dr.get_screenshot_as_png()
        # return self.dr.get_screenshot_as_png()

    def allure_catch_screen(self, dpi=1.0, tag='手动截图'):
        """
            截图并添加到allure附件
        :param dpi: 屏幕dpi
        :param tag: 附件标签
        :return: None
        """
        img = self.catch_screen_as_png(dpi)
        allure.attach(img, tag, allure.attachment_type.PNG)

    def is_displayed(self, locator: str, val=''):
        """
            元素是否出现
        :param locator:  定位字符串
        :param val: 输入参数值
        :return: True or False
        """
        try:
            ele = self.get(locator, val=val, log='off')
            if ele:
                flag = ele.is_displayed()
            else:
                flag = False
            self.logger.info(
                u'Element: <font class="log-bold">%s, %s</font> Is Displayed, True Or False?: <font class="log-bold">%s</font>' % (
                    locator, val, str(flag)))
            return flag
        except WebDriverException:
            self.logger.info(u'<font class="log-error">Element: %s, %s Is Displayed, True Or False?: %s</font>' % (
                locator, val, 'False'))
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
        if hasattr(By, loc[0].upper()):
            return getattr(By, loc[0].upper()), loc[1]
        else:
            return getattr(By, 'XPATH'), loc[1]

    def get_ele_by_templ_matching(self, target_path: str, threshold: float = 0.8, timeout=10.0, mode='rgb'):
        """
            获取匹配图像中心在页面中的坐标
        :param timeout: 查找元素超时时间,默认10秒
        :param target_path: 目标图像路径, png
        :param threshold: 阈值,默认0.8. 最好匹配为1.0,大于阈值才返回坐标
        :param mode: 匹配图像色彩模式: 'rgb' 'gray', default 'rgb'
        :return: x, y, max_val, window_opencv. x,y: dpi缩放前的坐标或None,None. max_val: 匹配度. window_opencv: cv2格式图像.
        """
        if not os.path.isfile(target_path):
            raise ValueError('Target path is not visitable.')
        x, y, max_val, window_opencv = None, None, None, None
        while timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5
            window_img = self.dr.get_screenshot_as_png()
            window_opencv = numpy.frombuffer(window_img, dtype='uint8')
            window_opencv = cv2.imdecode(window_opencv, cv2.IMREAD_COLOR)
            x, y, max_val = get_center_of_target(window_opencv, target_path, threshold=threshold, mode=mode)
            if x is not None and y is not None:
                break
            else:
                # 没有找到需要重新截图
                window_opencv = None
        self.logger.info(f'Matching coordinate: (x={x}, y={y}), Matching rate: {max_val}, {timeout}s left.')
        return x, y, max_val, window_opencv

    def click_on_page(self, x: int, y: int):
        """
            使用ActionChains点击页面坐标
        :param x: 横坐标
        :param y: 纵坐标
        :return: None
        """
        if x is not None and y is not None:
            action = ActionChains(self.dr)
            # window = self.dr.find_element(By.TAG_NAME, 'html')
            action.move_by_offset(xoffset=x, yoffset=y)
            # action.move_to_element_with_offset(window, xoffset=x, yoffset=y)
            action.pause(0.5)
            action.click()
            action.perform()
            action.reset_actions()  # 重置防止偏移坐标累计
            self.logger.info(f'Click at coordinate: (x={x}, y={y}).')

    @staticmethod
    def __draw_click_point(window_opencv, x, y, max_val=None):
        """
            在截图上标记点击坐标
        :param window_opencv: 截图, opencv格式
        :param x: x
        :param y: y
        :param max_val: None or 匹配度
        :return: img_bytes(png)
        """
        dpi = get_dpi()
        x_dpi, y_dpi = int(x * dpi), int(y * dpi)
        # cv2画图
        # 圆心
        cv2.circle(window_opencv, (x_dpi, y_dpi), 1, (0, 0, 255), 2)
        #  圆
        cv2.circle(window_opencv, (x_dpi, y_dpi), 8, (0, 0, 255), 1)
        cv2.circle(window_opencv, (x_dpi, y_dpi), 16, (0, 0, 255), 1)
        # 文字
        max_val = max_val or ''
        cv2.putText(window_opencv, f'Clicked here!({max_val})', (x_dpi + 10, y_dpi - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, 8)
        png_format = cv2.imencode('.png', window_opencv)[1]
        img_bytes = numpy.array(png_format).tobytes()
        return img_bytes

    def click_by_templ_matching(self, target_path: str, threshold: float = 0.8, img_type=None, mode='rgb'):
        """
            根据目标图像点击网页位置, 并可返回示意图象
        :param target_path: 目标图像路径, png
        :param threshold: 阈值,默认0.8. 最好匹配为1.0,大于阈值才返回坐标
        :param img_type: 'base64'(for unittest HTMLTestRunner) or 'png'(for allure), else: cv2 format
        :param mode: 匹配图像色彩模式: 'rgb' 'gray', default 'rgb'
        :return: base64_str(for unittest HTMLTestRunner) or byte_data(for allure)
        """
        time.sleep(0.5)
        x, y, max_val, window_opencv = self.get_ele_by_templ_matching(target_path, threshold=threshold, mode=mode)
        if x is not None and y is not None:
            self.click_on_page(x, y)
            # if draw:
            if img_type and window_opencv is not None:
                img_bytes = self.__draw_click_point(window_opencv, x, y, max_val)
                if img_type.lower() == 'png':
                    return img_bytes
                elif img_type.lower() == 'base64':
                    base64_str = base64.b64encode(img_bytes).decode(encoding='UTF-8')
                    return base64_str
                else:
                    return window_opencv
        else:
            self.logger.info(f'Matching rate is too low: {max_val} < {threshold}, skip click.')
            return None

    def get_ele_by_feature_matching(self, target_path: str, timeout=10.0):
        """
            获取匹配图像中心在页面中的坐标
        :param timeout: 查找元素超时时间,默认10秒
        :param target_path: 目标图像路径, png
        :return: x, y, max_val, window_opencv. x,y: dpi缩放前的坐标或None,None. window_opencv: cv2格式图像.
        """
        if not os.path.isfile(target_path):
            raise ValueError('Target path is not visitable.')
        x, y, window_opencv = None, None, None
        while timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5
            window_img = self.dr.get_screenshot_as_png()
            window_opencv = numpy.frombuffer(window_img, dtype='uint8')
            window_opencv = cv2.imdecode(window_opencv, cv2.IMREAD_COLOR)
            x, y = get_center_of_target_by_feature_matching(window_opencv, target_path)
            if x is not None and y is not None:
                break
            else:
                # 没有找到需要重新截图
                window_opencv = None
        self.logger.info(f'Matching coordinate: (x={x}, y={y}), {timeout}s left.')
        return x, y, window_opencv

    def click_by_featrue_matching(self, target_path: str, img_type=None):
        """
            根据目标图像点击网页位置, 并可返回示意图象
        :param target_path: 目标图像路径, png
        :param img_type: 'base64'(for unittest HTMLTestRunner) or 'png'(for allure), else: cv2 format
        :return: base64_str(for unittest HTMLTestRunner) or byte_data(for allure)
        """
        time.sleep(0.5)
        x, y, window_opencv = self.get_ele_by_feature_matching(target_path)
        if x is not None and y is not None:
            self.click_on_page(x, y)
            # if draw:
            if img_type and window_opencv is not None:
                img_bytes = self.__draw_click_point(window_opencv, x, y)
                if img_type.lower() == 'png':
                    return img_bytes
                elif img_type.lower() == 'base64':
                    base64_str = base64.b64encode(img_bytes).decode(encoding='UTF-8')
                    return base64_str
                else:
                    return window_opencv
        else:
            self.logger.info(f'Matching rate is too low or miss matching, skip click.')
            return None


