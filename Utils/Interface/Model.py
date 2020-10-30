# coding:utf-8
from Utils.Interface.Field import *


class Model:

    def __init__(self, template_str: str, application_type: str):
        tips = """
        Using python format function,  parameter palceholder should be '{' and '}',
        such as: 
            'the value of a is {a}'.
        In json:
         1. '{' and '}' should replace with '{{' and '}}',
         2. type number and boolean should not surround with quotation marks.
         3. quotation marks should be: "        
        for example:
            original json: {"user": "admin", "password": "admin", "opt_num": 123, "safe": true}
            template_str: '{{"user": "{user}", "password": "{password}", "opt_num": {opt_num}, "safe": {is_admin} }}'     
        """
        if '{' not in template_str and '}' not in template_str:
            raise ValueError(tips)
        self.template_str = template_str
        self.application_type = application_type
        self.valid_class_dict = {}
        self.invalid_class_dict = {}
        self.fields_name = list(filter(lambda v: not v.startswith("__") and not v.endswith("__"), vars(self.__class__)))

    def get_fields(self):
        self.fields_name = list(filter(lambda v: not v.startswith("__") and not v.endswith("__"), vars(self.__class__)))
        return self.fields_name

    def get_equivalent_class(self):
        fields_name = self.get_fields()
        valid_set_max_count = 0
        invalid_set_max_count = 0
        for name in fields_name:
            field = getattr(self, name)
            field.generate()
            self.valid_class_dict[name] = field.valid_set
            if len(field.valid_set) > valid_set_max_count:
                valid_set_max_count = len(field.valid_set)
            self.invalid_class_dict[name] = field.invalid_set
            if len(field.invalid_set) > invalid_set_max_count:
                invalid_set_max_count = len(field.invalid_set)
        return valid_set_max_count, self.valid_class_dict, invalid_set_max_count, self.invalid_class_dict

    def __replace_none(self, string, field):
        if 'josn' in self.application_type:
            pattern = r'[\{\[]{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            # only one parameter in string or in list
            if re.search(pattern, string) is not None:
                spn = re.search(pattern, string).span(1)
                return string[:spn[0]] + string[spn[1]:]
            # todo
        elif 'x-www-form-urlencoded' in self.application_type:
            pass
        else:
            pass
        return string

    def __replace_empty(self, string, field):
        pass
        return string

    def __generate_valid_case(self, valid_set_max_count, valid_class_dict):
        # todo
        valid_class_cases = []
        for i in range(0, valid_set_max_count):
            # count of valid class cases = valid_set_max_count
            tmp_str = self.template_str
            for field in self.fields_name:
                # replace placeholder with field value in template_str one by one
                if i < len(valid_class_dict[field]):
                    # index not out of border
                    if 'None' not in valid_class_dict[field][i] and 'empty' not in valid_class_dict[field][i]:
                        format_dict = {field: valid_class_dict[field][i]}
                        tmp_str.format(**format_dict)
                    elif 'empty' in valid_class_dict[field][i]:
                        # empty
                        tmp_str = self.__replace_empty(tmp_str, field)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str)
                else:
                    # index out of border, use value of index zero
                    if 'None' not in valid_class_dict[field][0] and 'empty' not in valid_class_dict[field][0]:
                        format_dict = {field: valid_class_dict[field][0]}
                        tmp_str.format(**format_dict)
                    elif 'empty' in valid_class_dict[field][0]:
                        # empty
                        tmp_str = self.__replace_empty(tmp_str)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str)
            valid_class_cases.append(tmp_str)
        return valid_class_cases

    def __generate_invalid_case(self, invalid_set_max_count, invalid_class_dict):
        # todo
        pass

    def generate_test_case(self):
        # todo
        pass


class A(Model):
    integer = IntField(False, ge=1, lt=3)
    number = FloatField(False, 1, gt='1.0', le='1.1')
    name = CharField(False, '13829302938', min_length=11, max_length=11, reg='^1[0-9]{10}$')
    bank = CollectionField(False, [1.0, 8.2, 10.0], float)
    create_time = DatetimeField(False, '%Y-%m-%d %H:%M:%S', ge='2019-12-31 23:59:59', lt='2020-01-01 00:00:00')


templ_str = '{{ "integer": {integer}, "number": {number}, "name": {name}, "bank": {bank}, "create_time": {create_time} }}'
a = A(templ_str, 'json')
print(a.fields_name)
a.create_time.generate()
print(a.create_time.valid_set)
print(a.create_time.invalid_set)
valid_max_count, valid_class, invalid_max_count, invalid_class = a.get_equivalent_class()
print(valid_max_count)
print(valid_class)
print(invalid_max_count)
print(invalid_class)

a = '{{  "user": "{user}",   "password"  :  ["a": " {a} ", "b": " {b} " ,"c": " {c} "]  ,  "number"  : {info}   }}'
b = '{{ "user": "{user}"}}'
c = '{{  "user": "{user}",   "password"  :  "{password}"  ,  "number"  : {info}   }}'


span = re.search(r'[\{\[]{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{user\}[\s\"]*)[\}\]]{1}', b).span(1)
print(span)
print(b[:span[0]]+b[span[1]:])

span = re.search(r'(,[\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{c\}[\s\"]*)[\}\]]{1}', a).span(1)
print(span)
print(a[:span[0]]+a[span[1]:])

span = re.search(r',{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*{b}[\s\"]*,{1})', a).span(1)
print(re.search(r',{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*{b}[\s\"]*,{1})', a))
print(a[:span[0]]+a[span[1]:])



