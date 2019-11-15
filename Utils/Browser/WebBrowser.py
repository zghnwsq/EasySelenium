# coding:utf-8

from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.ie.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.safari.webdriver import WebDriver as Safari
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as Remote

'''
    浏览器初始化及设置
'''


def remote_chrome(url='127.0.0.1:4444', user_dir='') -> WebDriver:
    """
    remote chrome
    :param url: ip:port
    :param user_dir: Chrome用户文件路径，用于使用已有缓存及cookie
    :return: WebDriver
    """
    opt = webdriver.ChromeOptions()
    if user_dir:
        arg = '--user-data-dir=' + user_dir
        opt.add_argument(arg)
    dr = Remote(command_executor='http://%s/wd/hub' % url, options=opt)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def chrome(path='./chromedriver.exe', user_dir='') -> WebDriver:
    """
    Chrome
    :param path: Chrome Driver路径
    :param user_dir: Chrome用户文件路径，用于使用已有缓存及cookie
    :return: WebDriver
    """
    # opt = options.Options()
    opt = webdriver.ChromeOptions()
    if user_dir:
        # opt = options.Options()
        # opt = webdriver.ChromeOptions()
        arg = '--user-data-dir=' + user_dir
        opt.add_argument(arg)
    # opt.add_argument('enable-automation')
    # opt.add_argument('disable-infobars')
    dr = Chrome(executable_path=path, options=opt)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def ie(path='./IEDriverServer.exe') -> WebDriver:
    """
    IE
    :param path:IE Driver路径
    :return: WebDriver
    """
    dr = IE(executable_path=path)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def edge() -> WebDriver:
    """
    Edge
    :return: WebDriver
    """
    dr = Edge()
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr


def firefox(path='./geckodriver.exe', profile=None) -> WebDriver:
    """
    Firefox
    :param path: Firefox Driver路径
    :param profile: Firefox设置
    :return: WebDriver
    """
    dr = Firefox(executable_path=path, firefox_profile=profile)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(10)
    dr.maximize_window()
    return dr



