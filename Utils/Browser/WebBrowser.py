# coding:utf-8

from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.ie.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.safari.webdriver import WebDriver as Safari
from selenium import webdriver


def chrome(path='./chromedriver.exe', user_dir='') -> WebDriver:
    # opt = options.Options()
    opt = webdriver.ChromeOptions()
    if user_dir:
        # opt = options.Options()
        # opt = webdriver.ChromeOptions()
        arg = '--user-data-dir=' + user_dir
        opt.add_argument(arg)
    # opt.add_argument('enable-automation')
    # opt.add_argument('disable-infobars')
    dr = Chrome(executable_path=path, chrome_options=opt)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr


def ie(path='./IEDriverServer.exe') -> WebDriver:
    dr = IE(executable_path=path)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr


def firefox(path='./geckodriver.exe', profile=None) -> WebDriver:
    dr = Firefox(executable_path=path, firefox_profile=profile)
    dr.set_page_load_timeout(30)
    dr.implicitly_wait(30)
    return dr



