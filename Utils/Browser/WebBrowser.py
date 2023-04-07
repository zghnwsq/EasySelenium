# coding:utf-8
import logging
import time
from selenium.common.exceptions import WebDriverException
# Firefox
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.firefox.service import Service as Firefox_Service
# IE
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.ie.service import Service as IE_Service
from selenium.webdriver.ie.options import Options
# from selenium.webdriver.ie.options import Options as IE_Options
# Edge
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.edge.service import Service as Edge_Service
# Safari
# from selenium.webdriver.safari.webdriver import WebDriver as Safari
# Remote
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Chrome
from selenium.webdriver.chrome.service import Service as Chrome_Service
from selenium.webdriver.chrome.webdriver import Options as Chrome_Options
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
import Settings
from Utils.ElementUtil.Element import Element
# from Utils.Report.Log import logger

'''
    浏览器初始化及设置
'''


def remote_chrome(node: dict, user_dir='') -> Remote:
    """
    remote chrome
    :param node: Node Desired Capabilities dict
    :param user_dir: Chrome用户文件路径，用于使用已有缓存及cookie
    :return: WebDriver
    """
    dc = DesiredCapabilities().CHROME.copy()
    dc['platform'] = node['platform']
    dc['version'] = node['version']
    opt = webdriver.ChromeOptions()
    if user_dir:
        arg = '--user-data-dir=' + user_dir
        opt.add_argument(arg)
    hub_url = 'http://%s/wd/hub' % node['hub']
    dr = Remote(command_executor=hub_url, options=opt, desired_capabilities=dc)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def chrome(path='./chromedriver.exe', user_dir='', args: list = None) -> Chrome:
    """
    Chrome
    :param args: 浏览器参数
    :param path: Chrome Driver路径
    :param user_dir: Chrome用户文件路径，用于使用已有缓存及cookie
    :return: WebDriver
    """
    # opt = options.Options()
    service = Chrome_Service(path)
    opt = Chrome_Options()
    # opt = webdriver.ChromeOptions()
    if user_dir:
        # opt = options.Options()
        # opt = webdriver.ChromeOptions()
        arg = '--user-data-dir=' + user_dir
        opt.add_argument(arg)
    # opt.add_argument('enable-automation')
    # opt.add_argument('disable-infobars')
    # 不显示受自动化控制的提示
    opt.add_experimental_option('useAutomationExtension', False)
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    if args:
        for arg in args:
            opt.add_argument(arg)
    dr = Chrome(service=service, options=opt)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def ie(path='./IEDriverServer.exe', options=None) -> IE:
    """
    IE
    :param options: IE options
    :param path:IE Driver路径
    :return: WebDriver
    """
    service = IE_Service(executable_path=path)
    dr = IE(service=service, options=options)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def edge(path='./msedgedriver.exe') -> Edge:
    """
    Edge
    :return: WebDriver
    """
    service = Edge_Service(path)
    dr = Edge(service=service)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def firefox(path='./geckodriver.exe', profile=None) -> Firefox:
    """
    Firefox
    :param path: Firefox Driver路径
    :param profile: Firefox设置
    :return: WebDriver
    """
    service = Firefox_Service(executable_path=path)
    dr = Firefox(service=service, firefox_profile=profile)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def init_chrome_browser(obj, user_dir='', wait=10):
    """
    默认初始化谷歌浏览器方法, 初始化driver, 设置浏览器
    :param obj: unittest.TestCase
    :param user_dir: (可选)浏览器用户目录, 用来复用浏览器缓存
    :param wait: 查找元素默认等待时间
    :return: None
    """
    obj.driver = chrome(path=Settings.DRIVER_PATH['chrome'], user_dir=user_dir)
    obj.driver.implicitly_wait(wait)
    obj.driver.set_page_load_timeout(30)
    obj.driver.maximize_window()


def init_ie_browser(obj, wait=10):
    """
    默认初始化谷歌浏览器方法, 初始化driver, 截图列表, dpi, 开始时间, 设置浏览器
    :param obj: unittest.TestCase
    :param wait: 查找元素默认等待时间
    :return: None
    """
    options = Options()
    options.ignore_protected_mode_settings = True
    options.page_load_strategy = 'normal'
    obj.driver = ie(path=Settings.DRIVER_PATH['ie'], options=options)
    obj.driver.implicitly_wait(wait)
    obj.driver.set_page_load_timeout(120)
    obj.driver.set_script_timeout(30)
    obj.driver.maximize_window()


def close_down(self):
    """
    通用测试结束方法，如果失败则截图后再关闭浏览器
    :param self: unittest object
    :return: None
    """
    print('\nClose down.')
    succ = True
    if hasattr(self, '_outcome'):
        for err in self._outcome.errors:
            if err[1] is not None:
                succ = False
    if hasattr(self, 'driver'):
        try:
            logger = getattr(self, 'logger', logging.getLogger('default'))
            # driver = getattr(self, 'driver')
            # if not succ:
            #     el = Element(driver, logger=logger)
            #     imgs = getattr(self, 'imgs', None)
            #     if imgs is not None:
            #         el.catch_screen(Settings.DPI, imgs=imgs, info='错误自动截图')
            self.driver.delete_all_cookies()
            # 成功才在这里关闭,失败由runner截图后关闭
            if succ:
                hds = self.driver.window_handles
                logger.info(f'Still have {len(hds)} windows.')
                for hd in hds:
                    logger.info(f'Close window {hd}.')
                    self.driver.switch_to.window(hd)
                    self.driver.close()
                self.driver.quit()
        except WebDriverException:
            pass
