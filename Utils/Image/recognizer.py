"""
@Time ： 2021/11/6 09:30
@Auth ： Ted
@File ：recognizer.py
@IDE ：PyCharm
"""
import os
from cv2 import cv2

# mtd = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]


def output_img(src, output, top_left, target_sharp: tuple):
    cv2.rectangle(src, top_left, (top_left[0] + target_sharp[0], top_left[1] + target_sharp[1]), (0, 0, 255), 2)
    cv2.imwrite(output, src)


def to_gray(src, target):
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    return src_gray, target_gray


def laplacian(src, target, ksize=1):
    src_filter = cv2.Laplacian(src, -1, ksize=ksize)
    target_filter = cv2.Laplacian(target, -1, ksize=ksize)
    return src_filter, target_filter


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
    # (取消) 归一化处理
    # cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    # 输出匹配图
    if output:
        theight, twidth = target.shape[:2]
        cv2.rectangle(src, top_left, (top_left[0] + twidth, top_left[1] + theight), (0, 0, 255), 2)
        cv2.imwrite(output, src)
    # 返回坐标
    return top_left


def match_img(src=None, target=None, output=None, mode='rgb', lap: bool = False, ksize=1):
    """
    匹配图像, 源和目标转灰度, 拉普拉斯二阶导得出边界轮廓，使用TM_CCOEFF_NORMED方法匹配
    :param src: 源图像, opencv格式或png图像路径
    :param target: 目标图像, opencv格式或png图像路径
    :param output: 匹配结果可视化图像存储路径
    :param mode: 匹配图像色彩模式: rgb gray
    :param lap: 是否对图像进行拉普拉斯二阶导
    :param ksize: 拉普拉斯二阶导ksize算子大小，1、3、5、7
    :return: top_left坐标, 匹配度
    """
    if isinstance(src, str):
        src = cv2.imread(src)
    if isinstance(target, str):
        target = cv2.imread(target)
    if src is None or target is None:
        return -1, -1
    if mode.lower() == 'gray':
        src, target = to_gray(src, target)
    # 模板阈值化
    # ret, template_threshold = cv2.threshold(target_gray, threshold, 255, cv2.THRESH_BINARY)
    # 拉普拉斯二阶导
    if lap:
        src, target = laplacian(src, target, ksize)
    # 匹配
    result = cv2.matchTemplate(src, target, cv2.TM_CCOEFF_NORMED)
    # (取消)归一化处理
    # cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 输出匹配图
    if output:
        theight, twidth = target.shape[:2]
        output_img(src, output, max_loc, (theight, twidth))
    # 返回坐标
    return max_loc, max_val


def get_center_of_target(src, target_path: str, threshold: float = 0.8, mode='rgb'):
    """
        获取匹配图像中心在源图像中的坐标: x,y
    :param src: 源图像, opencv格式
    :param target_path: 目标图像路径, png
    :param threshold: 阈值,默认0.8. 最好匹配为1.0,大于阈值才返回坐标
    :param mode: 匹配图像色彩模式: rgb gray
    :return: x, y or None, None. dpi缩放前的坐标
    """
    if not os.path.isfile(target_path):
        return 0, 0
    target = cv2.imread(target_path)
    top_left, max_val = match_img(src, target=target, mode=mode)
    if max_val < threshold:
        return None, None, max_val
    else:
        theight, twidth = target.shape[:2]
        dpi = get_dpi()
        return int((top_left[0] + twidth / 2) / dpi), int((top_left[1] + theight / 2) / dpi), max_val


def match_with_BFMatcher(src, target, ratio: float = 0.2, min_match_count: int = 5):
    """
        使用BFMatcher，匹配特征，返回匹配点加权平均坐标和最好匹配坐标
    :param src: 源图像, opencv格式或png图像路径
    :param target: 目标图像, opencv格式或png图像路径
    :param ratio: ratio test explained by D.Lowe in his paper
    :param min_match_count: 最低匹配点数量
    :return: weight_avg_point, best_point or None, None
    """
    try:
        if isinstance(src, str):
            img1 = cv2.imread(src, cv2.IMREAD_GRAYSCALE)  # queryImage
        else:
            img1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # queryImage
        if isinstance(target, str):
            img2 = cv2.imread(target, cv2.IMREAD_GRAYSCALE)  # trainImage
        else:
            img2 = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)  # trainImage
    except cv2.error:
        return None, None
    if img1 is None or img2 is None:
        return None, None
    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # Apply ratio test
    good, points = [], []
    weight_sum, best_distance = 0, 9999
    coord_sum, best_point = [0, 0], [0, 0]
    for m, n in matches:
        # The lower, the better it is, default 0.2
        if m.distance < ratio * n.distance:
            weight = (n.distance / m.distance)
            weight_sum += weight
            query_idx = m.queryIdx
            x, y = kp1[query_idx].pt
            if m.distance < best_distance:
                best_distance = m.distance
                best_point = [round(x), round(y)]
            points.append((x, y))
            coord_sum[0] += x * weight
            coord_sum[1] += y * weight
            good.append([m])
    weight_avg_point = (round(coord_sum[0] / weight_sum), round(coord_sum[1] / weight_sum)) if weight_sum > 0 and len(
        points) >= min_match_count else (
        0, 0)
    print(f'Weight average point: {weight_avg_point}, Matches points: {len(points)}')
    if weight_sum > 0 and len(points) >= min_match_count:
        weight_avg_point = (round(coord_sum[0] / weight_sum), round(coord_sum[1] / weight_sum))
        return weight_avg_point, best_point, len(points)
    else:
        return None, None, len(points)


def get_center_of_target_by_feature_matching(src, target_path: str, ratio: float = 0.2, min_match_count: int = 5):
    """
        使用BFMatcher，匹配特征，返回匹配点加权平均坐标
    :param src: 源图像, opencv格式或png图像路径
    :param target_path: 目标图像, opencv格式或png图像路径
    :param ratio: ratio test explained by D.Lowe in his paper
    :param min_match_count: 最低匹配点数量
    :return: x, y or None, None. dpi缩放前的坐标
    """
    if not os.path.isfile(target_path):
        return 0, 0
    weight_avg_point, best_point, matches = match_with_BFMatcher(src, target_path, ratio, min_match_count)
    if weight_avg_point is None or best_point is None:
        return None, None
    dpi = get_dpi()
    return round(weight_avg_point[0] / dpi), round(weight_avg_point[1] / dpi), matches


def get_dpi():
    """
        获取DPI
    :return: DPI: float
    """
    if 'nt' in os.name:
        import win32con
        import win32gui
        import win32print
        # DPI改自动获取
        hdc = win32gui.GetDC(0)
        default_dpi = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc,
                                                                                                        win32con.HORZRES)
        advanced_dpi = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 0.96 / 100
        dpi = default_dpi if advanced_dpi == 1.0 else advanced_dpi
    else:
        dpi = 1.0
    return dpi



