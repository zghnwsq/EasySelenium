"""
@Time ： 2021/11/6 09:30
@Auth ： Ted
@File ：recognizer.py
@IDE ：PyCharm
"""
import win32con
import win32gui
import win32print
from cv2 import cv2
import os

# mtd = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]


def match_in_gray_mode(src=None, target=None, output=None, method=cv2.TM_CCOEFF_NORMED):
    """
    匹配图像, 源和目标转灰度, 根据给出方法匹配, 默认TM_CCOEFF_NORMED
    :param src: 源图像, opencv格式或png图像路径
    :param target: 目标图像, opencv格式或png图像路径
    :param output: 匹配结果可视化图像存储路径
    :param method: 匹配方法: cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED
    :return: top_left坐标
    """
    if isinstance(src, str):
        src = cv2.imread(src)
    if isinstance(target, str):
        target = cv2.imread(target)
    # 转灰度
    if src is not None and target is not None:
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    else:
        return -1, -1
    # 匹配
    result = cv2.matchTemplate(src_gray, target_gray, method)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    # 输出匹配图
    if output:
        theight, twidth = target.shape[:2]
        cv2.rectangle(src, top_left, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 255), 2)
        cv2.imwrite(output, src)
    # 返回坐标
    return top_left


def match_in_filter_mode(src=None, target=None, output=None, threshold=127, ksize=1):
    """
    匹配图像, 源和目标转灰度, 拉普拉斯二阶导得出边界轮廓，使用TM_CCOEFF_NORMED方法匹配
    :param src: 源图像, opencv格式或png图像路径
    :param target: 目标图像, opencv格式或png图像路径
    :param output: 匹配结果可视化图像存储路径
    :param threshold: 目标图像阈值
    :param ksize: 拉普拉斯二阶导ksize算子大小，1、3、5、7
    :return: top_left坐标, 匹配度
    """
    if isinstance(src, str):
        src = cv2.imread(src)
    if isinstance(target, str):
        target = cv2.imread(target)
    if src is not None and target is not None:
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    else:
        return -1, -1
    # 模板阈值化
    ret, template_threshold = cv2.threshold(target_gray, threshold, 255, cv2.THRESH_BINARY)
    # 拉普拉斯二阶导
    template_filter = cv2.Laplacian(template_threshold, -1, ksize=ksize)
    target_filter = cv2.Laplacian(src_gray, -1, ksize=ksize)
    # 匹配
    result = cv2.matchTemplate(target_filter, template_filter, cv2.TM_CCOEFF_NORMED)
    # 归一化处理
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 输出匹配图
    if output:
        theight, twidth = target.shape[:2]
        cv2.rectangle(src, max_loc, (max_loc[0] + twidth, max_loc[1] + theight), (0, 0, 255), 2)
        cv2.imwrite(output, src)
    # 返回坐标
    return max_loc, max_val


def get_center_of_target(src, target_path: str, threshold: float = 0.8):
    """
        获取匹配图像中心在源图像中的坐标: x,y
    :param src: 源图像, opencv格式
    :param target_path: 目标图像路径, png
    :param threshold: 阈值,默认0.8. 最好匹配为1.0,大于阈值才返回坐标
    :return: x, y or None, None. dpi缩放前的坐标
    """
    if not os.path.isfile(target_path):
        return 0, 0
    target = cv2.imread(target_path)
    top_left, max_val = match_in_filter_mode(src, target=target)
    if max_val < threshold:
        return None, None, max_val
    else:
        theight, twidth = target.shape[:2]
        dpi = get_dpi()
        return int((top_left[0] + twidth / 2) / dpi), int((top_left[1] + theight / 2) / dpi), max_val


def get_dpi():
    """
        获取DPI
    :return: DPI: float
    """
    # DPI改自动获取
    hdc = win32gui.GetDC(0)
    default_dpi = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc,
                                                                                                    win32con.HORZRES)
    advanced_dpi = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 0.96 / 100
    dpi = default_dpi if advanced_dpi == 1.0 else advanced_dpi
    return dpi



