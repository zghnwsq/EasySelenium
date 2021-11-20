# coding:utf-8
from selenium.common.exceptions import WebDriverException
# Firefox
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.firefox.service import Service as Firefox_Service
# IE
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.ie.service import Service as IE_Service
# Edge
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.edge.service import Service as Edge_Service
# from selenium.webdriver.ie.options import Options as IE_Options
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


def ie(path='./IEDriverServer.exe') -> IE:
    """
    IE
    :param path:IE Driver路径
    :return: WebDriver
    """
    service = IE_Service(executable_path=path)
    dr = IE(service=service)
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


def close_down(self):
    """
    通用测试结束方法，如果失败则截图后再关闭浏览器
    :param self: unittest object
    :return: None
    """
    succ = True
    if hasattr(self, '_outcome'):
        for err in self._outcome.errors:
            if err[1] is not None:
                succ = False
        if not succ:
            try:
                self.imgs.append(self.el.catch_screen(Settings.DPI))
                # self.driver.delete_all_cookies()
                # self.driver.close()
                # self.driver.quit()
            except WebDriverException:
                pass
    if hasattr(self, 'driver'):
        self.driver.delete_all_cookies()
        self.driver.close()
        self.driver.quit()


