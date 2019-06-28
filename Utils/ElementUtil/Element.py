# coding=utf-8


class Element:

    def __init__(self, dr):
        self.dr = dr

    def id(self, ele_id):
        return self.dr.find_element_by_id(ele_id)

    def id(self, ele_id):
        return self.dr.find_element_by_id(ele_id)

    def xpath(self, xpath):
        return self.dr.find_element_by_xpath(xpath)

    def name(self, name):
        return self.dr.find_element_by_name(name)

    def class_name(self, class_name):
        return self.dr.find_element_by_class_name(class_name)

    def css_selector(self, css_selector):
        return self.dr.find_element_by_css_selector(css_selector)

