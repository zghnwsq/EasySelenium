# coding=utf-8


class Element:

    def __init__(self, dr):
        self.dr = dr

    def id(self, ele_id):
        return self.dr.find_element_by_id(ele_id)

    # def id(self, ele_id):
    #     return self.dr.find_element_by_id(ele_id)

    def xpath(self, xpath):
        return self.dr.find_element_by_xpath(xpath)

    def name(self, name):
        return self.dr.find_element_by_name(name)

    def class_name(self, class_name):
        return self.dr.find_element_by_class_name(class_name)

    def css(self, css_selector):
        return self.dr.find_element_by_css_selector(css_selector)

    def locate(self, ob, val=''):
        """
        键值对方式调用定位方法返回元素，支持输入动态变量
        :param ob: ob[0]对应元素定位方法，ob[1]对应定位字符串
        :param val:输入动态变量值
        :return:
        """
        if type(ob) == list:
            method = getattr(self, ob[0])
            pattern = ob[1]
            if '${' in ob[1] and '}' in ob[1]:
                key = ob[1][ob[1].find('${'): ob[1].find('}')+1]
                pattern = pattern.replace(key, val)
            return method(pattern)
        else:
            raise Exception('Wrong param type or length , actual: %s, %d ' % (str(type(ob)), len(ob)))

