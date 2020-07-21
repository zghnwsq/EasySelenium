# coding=utf-8

import win32gui
import win32con
import time


def upload(title, file_path, wait_time=1):
    """
    上传窗口控制
    :param title: 上传窗口title
    :param file_path: 上传文件路径
    :param wait_time: 等待窗口时间(秒)
    :return:
    """
    time.sleep(wait_time)
    # win32gui
    dialog = win32gui.FindWindow('#32770', title)  # 对话框
    '''    
    FindWindow(lpClassName=None, lpWindowName=None)
    描述：自顶层窗口（也就是桌面）开始搜索条件匹配的窗体，并返回这个窗体的句柄。
    不搜索子窗口、不区分大小写。找不到就返回0
    参数：
    lpClassName：字符型，是窗体的类名，这个可以在Spy + +里找到。
    lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：这个函数我们仅能用来找主窗口。'''
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    '''
    FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None)
    描述：搜索类名和窗体名匹配的窗体，并返回这个窗体的句柄。不区分大小写，找不到就返回0。 参数：
    hwndParent：若不为0，则搜索句柄为hwndParent窗体的子窗体。
    hwndChildAfter：若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。
    lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
    lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：找到了主窗口以后就靠它来定位子窗体啦。
    '''
    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, file_path)  # 往输入框输入绝对地址
    time.sleep(2)
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
