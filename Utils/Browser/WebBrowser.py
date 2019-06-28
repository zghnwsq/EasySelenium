# coding:utf-8

from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.ie.options import Options
# from selenium.webdriver.safari.webdriver import WebDriver as Safari


def chrome(path='./chromedriver.exe', user_dir=''):
    opt = None
    if user_dir:
        arg = '--user-data-dir=' + user_dir
        opt = Options()
        opt.add_argument(arg)
    dr = Chrome(executable_path=path, options=opt)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr


def ie(path='./IEDriverServer.exe'):
    dr = IE(executable_path=path)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr


def firefox(path='./geckodriver.exe', profile=None):
    dr = Firefox(executable_path=path, firefox_profile=profile)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr



