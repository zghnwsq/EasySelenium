# coding=utf-8

import xlrd

"""
    读取excel，返回结果数组
"""


# 竖版数据源
def read_data(path, index):
    sheet = xlrd.open_workbook(path).sheet_by_index(index)
    row = sheet.nrows  # 总行数
    col = sheet.ncols  # 总列数
    col_name = sheet.row_values(0)  # 列名
    data = []
    for i in range(1, row, 1):
        row_data = {}
        for j in range(1, col, 1):
            # print type(sheet.row_values(i)[j])
            # row_data[col_name[j]] = sheet.cell(i, j).value
            row_data[col_name[j]] = str(sheet.row_values(i)[j])
            # row_data[col_name[j]] = sheet.cell_value(i, j).encode('utf-8')
            # print row_data
        data.append(row_data)
    # print data
    return data


# 横版数据源
# type
# 0 empty（空的）
# 1 string（text）
# 2 number
# 3 date
# 4 boolean
# 5 error
# 6 blank（空白表格）
# 描述 参数名 场景1 场景2 ...
def read_data_by_sheet_name(path, sheet_name):
    """
    读取excel中指定sheet的数据，返回数组
    :param path:excel路径
    :param sheet_name:sheet名
    :return: 结果字典数组
    """
    sheet = xlrd.open_workbook(path).sheet_by_name(sheet_name)
    row = sheet.nrows  # 总行数
    col = sheet.ncols  # 总列数
    # col_name = sheet.row_values(0)  # 列名
    param_name = sheet.col_values(1)  # 参数名
    data = []  # 列字典数组
    for i in range(2, col, 1):
        col_data = {}  # 列字典
        for j in range(1, row, 1):
            col_data[param_name[j]] = str(sheet.row_values(j)[i])  # 参数名=参数值
        data.append(col_data)
    return data

