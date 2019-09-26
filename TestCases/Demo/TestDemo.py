# coding=utf-8
import ddt
import unittest
import time
import sys
import logging
import Settings
# from Utils.Report import HTMLTestReportCN
from Utils.Browser.WebBrowser import chrome
from Utils.ElementUtil.Element import Element
# from Pages.TB import AppDetailOrgEdit
# from selenium.webdriver.common.action_chains import ActionChains
import win32gui
import win32api
import win32con
import cx_Oracle
from Utils.DataBase.Oracle import Oracle
from Utils.Report.Log import *
from TestCases import SQL
from Utils.Report import HTMLTestRunner_cn as HTMLTestReportCN

data = [{'a': 'ok'}, {'a': 'ng'}, {'a': 'ok'}]


@ddt.ddt
class TestDemo(unittest.TestCase):

    # 用例组名：__module__: __name__ : __doc__
    # __module__ = '*测试示例*'
    # __name__ = '-测试示例-'
    __doc__ = '-测试示例-'

    def setUp(self):
        print('begin')
        # self.imgs = []
        # self.driver = chrome(path=Settings.DRIVER_PATH['chrome'], user_dir=r'C:\Users\tedwa\AppData\Local\Temp\scoped_dir20784_2096370265')
        self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
        # self.driver = chrome(path='/Users/ted/Documents/Driver/chromedriver')
        self.log = logger('info')
        self.el = Element(self.driver, self.log)

    def tearDown(self):
        # if self.driver:
        #     self.driver.close()
        #     self.driver.quit()
        print('end')

    @ddt.data(*data)
    def test_a(self, dt):
        self._testMethodDoc = '测试data'
        print(dt['a'])
        self.assertEqual('ok', dt['a'])

    def test_b(self):
        # 用例名： __class__._testMethodName : _testMethodDoc *verbosity>1时显示
        # self._testMethodName = '测试1'
        self._testMethodDoc = '测试wait_until_disappeared方法'
        self.log.info('打开百度')
        self.driver.get('http://www.baidu.com')
        self.el.get('id=kw')
        time.sleep(5)
        # self.el.get('id=${kw}', val='kw').send_keys('123')
        # img = self.driver.get_screenshot_as_base64()
        # self.imgs.append(img)
        # self.el.get('id=su').click()
        # self.el.wait_until_disappeared('xpath=//em[text()="12306"]')
        # img = self.driver.get_screenshot_as_base64()
        # self.imgs.append(img)
        # self.driver.find_element_by_id('adfdff')
        # self.driver.get('https://www.w3school.com.cn/tiy/t.asp?f=jquery_fadeout')
        # self.driver.switch_to.frame(self.el.get('id=iframeResult'))
        # print(self.el.get('id=div3').is_displayed())
        # self.el.get('xpath=//button[text()="点击这里，使三个矩形淡出"]').click()
        # print(self.el.get('id=div3').is_displayed())
        # self.el.wait_until_disappeared('id=div3')
        # print(self.el.get('id=div3').is_displayed())
        # img = self.driver.get_screenshot_as_base64()
        # self.imgs.append(img)
        # self.driver.close()
        # self.driver.quit()

    # def test_c(self):
    #     self.driver.get('http://sahitest.com/demo/php/fileUpload.htm')
    #     upload = self.driver.find_element_by_id('file')
    #     upload.click()
    #     time.sleep(1)
    #
    #     # win32gui
    #     dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
    #     ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    #     ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    #     Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    #     button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    #     win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, r'C:\Users\tedwa\Pictures\upload1.png')  # 往输入框输入绝对地址
    #     win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

    def test_d(self):
        # connect = cx_Oracle.connect('zbhxzcs/test!60@200.168.168.60:1523/zbhxz')
        # cursor = connect.cursor()
        # cursor.execute("SELECT * FROM IMS_TB_PC WHERE PCH='20190906020572'")
        # result = cursor.fetchone()
        # print(result)
        # cursor.close()
        # connect.close()
        db = Oracle('zbhxzcs', 'test!60', '200.168.168.60:1523/zbhxz')
        # res = db.query("SELECT TOPNUM FROM IMS_TB_PC WHERE PCH='20190906020572'", 1)
        # res = db.execute("UPDATE IMS_TB_PC SET TOPNUM='1' WHERE PCH='20190906020572'")
        # res = db.query("""SELECT B.CSFZH FROM (SELECT ZBH, MIN(QBRQ) QBRQ, MAX(ZBRQ) ZBRQ FROM IMS_GRTBKZX GROUP BY ZBH) A, IMS_YBXX B, THYKXIU C
        #                  WHERE A.ZBH=C.CZBH
        #                  AND C.CSFZH=B.CSFZH
        #                  AND B.DRYRQ>A.QBRQ
        #                  AND B.DRYRQ<A.ZBRQ
        #                  AND B.DCYRQ>A.QBRQ
        #                  AND B.DCYRQ<A.ZBRQ
        #                  AND B.GFPCH IS NULL AND B.CJYLX='1'
        #                  AND NOT EXISTS(SELECT 1 FROM IMS_GF_PC_YBGL WHERE CLSH=B.CLSH)
        #                  AND B.CZZZBH='       '
        #                  AND ROWNUM<2""")
        # res = db.execute_block("""
        # declare
        #     zbh ims_grtbkzx.zbh%type;
        #     qbrq ims_grtbkzx.qbrq%type;
        #     zbrq ims_grtbkzx.zbrq%type;
        #     sfzh thykxiu.csfzh%type;
        #     ybxx ims_ybxx%rowtype;
        #     lsh_count int;
        #     c int;
        #     y_count int;
        #     cursor c_xiu is select zbh, qbrq, zbrq from ims_grtbkzx;
        # begin
        #     if c_xiu%isopen=false
        #         then
        #         open c_xiu;
        #     end if;
        #     c :=0;
        #     loop
        #         fetch c_xiu into zbh, qbrq, zbrq;
        #         exit when c_xiu%notfound;
        #         select csfzh into sfzh from thykxiu where czbh=zbh;
        #         select count(1) into y_count from ims_ybxx where csfzh=sfzh;
        #         if y_count>0
        #         then
        #                     for ybxx in (select * from ims_ybxx where csfzh=sfzh)
        #                     loop
        #                         select count(1) into lsh_count from ims_gf_pc_ybgl where clsh=ybxx.clsh;
        #                         if ybxx.dryrq>qbrq
        #                                      and ybxx.dryrq<zbrq
        #                                      and ybxx.dcyrq>qbrq
        #                                      and ybxx.dcyrq<zbrq
        #                                      and ybxx.gfpch is null
        #                                      and ybxx.cjylx= :jylx
        #                                      and lsh_count<1
        #                                      and ybxx.CZZZBH='       '
        #                         then
        #                                 c :=c+1;
        #                                 :out_var := to_char(ybxx.dryrq, 'yyyymmdd')||','||to_char(ybxx.dcyrq, 'yyyymmdd')||','||ybxx.csfzh||','||to_char(ybxx.clsh);
        #                         end if;
        #                     end loop;
        #         end if;
        #         exit when c>=1;
        #     end loop;
        #     close c_xiu;
        # end;
        # """, str, jylx='3')
        res = db.execute_block(SQL.TuiXiuPingPiaoChaXun, str, jylx='1')
        print(res)
        # db.close()

    # def test_e(self):
    #     self.driver = chrome(path=Settings.DRIVER_PATH['chrome'])
    #     self.driver.get('http://www.baidu.com')
    #     time.sleep(3)
    #     # Ctrl+P
    #     win32api.keybd_event(17, 0, 0, 0)
    #     win32api.keybd_event(80, 0, 0, 0)
    #     win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     time.sleep(3)
    #     #
    #     win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     # Ctrl+Shift+P
    #     # win32api.keybd_event(17, 0, 0, 0)
    #     # win32api.keybd_event(16, 0, 0, 0)
    #     # win32api.keybd_event(80, 0, 0, 0)
    #     # win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     # win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     # win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)
    #     # time.sleep(3)


if __name__ == '__main__':
    # 用例不在这里运行
    pass
    # unittest.main()
    # fileBase = '../..'  # 目录
    # runner = HTMLTestReportCN.HTMLTestRunner(
    #     stream=fileBase,
    #     title='{ Test Demo }',
    #     description='Test Demo',
    #     tester='ted'
    # )
    # suit = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    # runner.run(suit)

