# coding=utf-8

import win32gui
import win32con
import win32api
import time


def close_print(title, wait_time=1):
    # print('kaishi')
    time.sleep(wait_time)
    # win32api
    # win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    # win32gui
    # 父窗口 类名: Chrome_WidgetWin_1 标题: '无标题 - Google Chrome'
    father = win32gui.FindWindow(None, title)
    # print(father)
    print(win32gui.GetWindowText(father))
    # 子窗口 类名: Chrome_RenderWidgetHostHWND 标题: Chrome Legacy Window
    # son = win32gui.FindWindowEx(father, None, 'Intermediate D3D Window', '')
    # print(son)
    # win32gui.SetActiveWindow(father)
    # ENTER
    # win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
    # win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
    # win32gui.SendMessage(son, win32con.WM_CLOSE, 0, 0)
    # 设置为最前窗口
    # win32gui.SetForegroundWindow(son)
    # ESC
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32gui.SendMessage(father, win32con.WM_CLOSE, 0, 0)  # 关闭打印窗口
    # ctrl+shift+P
    # win32api.keybd_event(17, 0, 0, 0)
    # win32api.keybd_event(16, 0, 0, 0)
    # win32api.keybd_event(80, 0, 0, 0)
    # win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    # win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
    # win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)
    # time.sleep(1)
    # 设置为最前窗口
    # win32gui.SetForegroundWindow(son)
    # # 发送ESC-取消打印
    # win32api.keybd_event(27, 0, 0, 0)
    # win32api.keybd_event(27, 0, win32con.KEYEVENTF_KEYUP, 0)
    # time.sleep(1)

    '''    
    FindWindow(lpClassName=None, lpWindowName=None)
    描述：自顶层窗口（也就是桌面）开始搜索条件匹配的窗体，并返回这个窗体的句柄。
    不搜索子窗口、不区分大小写。找不到就返回0
    参数：
    lpClassName：字符型，是窗体的类名，这个可以在Spy + +里找到。
    lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：这个函数我们仅能用来找主窗口。'''
    # sub_window = win32gui.FindWindowEx(dialog, 0, 'Intermediate D3D Window', None)
    # print(sub_window)
    '''
    FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None)
    描述：搜索类名和窗体名匹配的窗体，并返回这个窗体的句柄。不区分大小写，找不到就返回0。 参数：
    hwndParent：若不为0，则搜索句柄为hwndParent窗体的子窗体。
    hwndChildAfter：若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。
    lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
    lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：找到了主窗口以后就靠它来定位子窗体啦。
    '''
    # win32gui.SendMessage(dialog, win32con.WM_CHAR, 27, sub_window)  # 按Esc
    # win32gui.SendMessage(dialog, win32con.WM_KEYDOWN, 27, 0)
    # win32gui.SendMessage(dialog, win32con.WM_KEYUP, 27, 0)
    # win32gui.PostMessage(dialog, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
    # win32gui.PostMessage(dialog, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
