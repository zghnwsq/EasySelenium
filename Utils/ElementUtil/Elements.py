# coding=utf-8
#
#
# class Elements:
#     '''
#         废弃
#     '''
#
#     def __init__(self, dr):
#         self.dr = dr
#
#     def _id(self, ele_id):
#         return self.dr.find_elements_by_id(ele_id)
#
#     # def id(self, ele_id):
#     #     return self.dr.find_elements_by_id(ele_id)
#
#     def _xpath(self, xpath):
#         return self.dr.find_elements_by_xpath(xpath)
#
#     def _name(self, name):
#         return self.dr.find_elements_by_name(name)
#
#     def _class_name(self, class_name):
#         return self.dr.find_elements_by_class_name(class_name)
#
#     def _css(self, css_selector):
#         return self.dr.find_elements_by_css_selector(css_selector)
#
#     def locates(self, locator: list, val='') -> list:
#         """
#         键值对方式调用定位方法返回元素，支持输入动态变量
#         :param locator: locator[0]对应元素定位方法，locator[1]对应定位字符串
#         :param val:输入动态变量值
#         :return: WebElement
#         """
#         if type(locator) == list and len(locator) > 1:
#             method = getattr(self, '_'+locator[0])
#             pattern = locator[1]
#             if '${' in locator[1] and '}' in locator[1]:
#                 key = locator[1][locator[1].find('${'): locator[1].find('}') + 1]
#                 if val:
#                     pattern = pattern.replace(key, val)
#                 else:
#                     raise Exception('Locator required val input: %s = %s' % (str(key), str(val)))
#             return method(pattern)
#         else:
#             raise Exception('Wrong locator type or length , actual: %s, %d ' % (str(type(locator)), len(locator)))
#
#     def gets(self, locator: str, val='') -> list:
#         """
#         键值对方式调用定位方法返回元素，支持输入动态变量
#         :param locator: method=pattern格式的定位字符串
#         :param val:输入动态变量值
#         :return: WebElement
#         """
#         if '=' in locator:
#             pattern = locator.split('=')
#             method = getattr(self, '_'+pattern[0].lower())
#             ptn = pattern[1]
#             if '${' in pattern[1] and '}' in pattern[1]:
#                 key = pattern[1][pattern[1].find('${'): pattern[1].find('}') + 1]
#                 if val:
#                     ptn = ptn.replace(key, val)
#                 else:
#                     raise Exception('Locator required val input: %s = %s' % (str(key), str(val)))
#             return method(ptn)
#         else:
#             raise Exception('Wrong locator format, actual: %s ' % str(locator))
