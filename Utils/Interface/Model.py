# coding:utf-8
from Utils.Interface.Field import *


class Model:

    def __init__(self, template_str: str, application_type: str):
        tips = """
        Using python format function,  parameter placeholder should be '{parameter_name}',
        and parameter name should be unique.
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
            self.valid_class_dict[name] = list(field.valid_set)
            if len(field.valid_set) > valid_set_max_count:
                valid_set_max_count = len(field.valid_set)
            self.invalid_class_dict[name] = list(field.invalid_set)
            if len(field.invalid_set) > invalid_set_max_count:
                invalid_set_max_count = len(field.invalid_set)
        return valid_set_max_count, self.valid_class_dict, invalid_set_max_count, self.invalid_class_dict

    def __replace_none(self, string, field):
        tmp = string
        if 'json' in self.application_type:
            only_one = r'[\{\[]{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            first = r'[\{\[]{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*,)'
            last = r'(,[\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            middle = r',{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*,{1})'
            # spn = None
            # only one parameter in string or in list
            if re.search(only_one, string) is not None:
                spn = re.search(only_one, string).span(1)
            # parameter in the first place
            elif re.search(first, string) is not None:
                spn = re.search(first, string).span(1)
            # parameter in the last place
            elif re.search(last, string) is not None:
                spn = re.search(last, string).span(1)
            # parameter in the middle
            elif re.search(middle, string) is not None:
                spn = re.search(middle, string).span(1)
            else:
                raise KeyError('Missing field placeholder!')
            tmp = tmp[:spn[0]] + string[spn[1]:]
        elif 'x-www-form-urlencoded' in self.application_type:
            only_one = r'\s*(\S[^\{]*\s*=\s*\{\s*' + field + r'\s*\}\s*$)'
            first = r'\s*(\S[^\{]*\s*=\s*\{\s*' + field + r'\s*\}\s*&*)'
            mid = r'&+?(\s*\S[^\{]*\s*=\s*\{\s*' + field + r'\s*\}\s*&+?)'
            last = r'(&+?\s*\S[^\{]*\s*=\s*\{\s*' + field + r'\s*\})\s*'
            # spn = None
            if re.search(only_one, string) is not None:
                return ''
            elif re.search(first, string) is not None:
                spn = re.search(first, string).span(1)
            elif re.search(mid, string) is not None:
                spn = re.search(mid, string).span(1)
            elif re.search(last, string) is not None:
                spn = re.search(last, string).span(1)
            else:
                raise KeyError('Missing field placeholder!')
            tmp = tmp[:spn[0]] + string[spn[1]:]
        else:
            pass
        return tmp

    def __replace_empty(self, string, field):
        tmp = string
        if 'json' in self.application_type:
            obj = getattr(self, field)
            if isinstance(obj, NumberField) or isinstance(obj, BooleanField):
                # replace :"{field_placeholder}" with :null
                ptn = r'["\s]*\{\s*' + field + r'\s*\}[\s"]*'
                tmp = re.sub(ptn, 'null', tmp, count=1)
            else:
                # replace with empty string :''
                format_dict = {field: ''}
                tmp.format(**format_dict)
        elif 'x-www-form-urlencoded' in self.application_type:
            # replace with empty string :''
            format_dict = {field: ''}
            tmp.format(**format_dict)
        else:
            pass
        return tmp

    def generate_valid_case(self, valid_set_max_count, valid_class_dict):
        valid_class_cases = []
        for i in range(0, valid_set_max_count):
            # count of valid class cases = valid_set_max_count
            tmp_str = self.template_str
            format_dict = {}
            for field in self.fields_name:
                # replace placeholder with field value in template_str one by one
                if i < len(valid_class_dict[field]):
                    # index not out of border
                    if 'None' not in str(valid_class_dict[field][i]) and 'empty' not in str(valid_class_dict[field][i]):
                        format_dict[field] = str(valid_class_dict[field][i])

                    elif 'empty' in str(valid_class_dict[field][i]):
                        # empty
                        tmp_str = self.__replace_empty(tmp_str, field)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str, field)
                else:
                    # index out of border, use value of index zero
                    if 'None' not in str(valid_class_dict[field][0]) and 'empty' not in str(valid_class_dict[field][0]):
                        format_dict[field] = str(valid_class_dict[field][0])

                    elif 'empty' in str(valid_class_dict[field][0]):
                        # empty
                        tmp_str = self.__replace_empty(tmp_str, field)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str, field)
            format_str = tmp_str.format(**format_dict)
            valid_class_cases.append(format_str)
        return valid_class_cases

    def __generate_invalid_case(self, invalid_set_max_count, invalid_class_dict):
        # todo
        pass

    def generate_test_case(self):
        # todo
        pass


class A(Model):
    integer = IntField(True, ge=1, lt=3)
    number = FloatField(False, 1, gt='1.0', le='1.1')
    name = CharField(False, '13829302938', min_length=11, max_length=11, reg='^1[0-9]{10}$')
    bank = CollectionField(False, [1.0, 8.2, 10.0], float)
    create_time = DatetimeField(False, '%Y-%m-%d %H:%M:%S', ge='2019-12-31 23:59:59', lt='2020-01-01 00:00:00')


templ_str = '{{ "integer": {integer}, "number": {number}, "name": {name}, "bank": {bank}, "create_time": {create_time} }}'
a = A(templ_str, 'json')
# print(a.fields_name)
# print(isinstance(a.integer, NumberField))
# print(isinstance(a.integer, IntField))
# a.create_time.generate()
# print(a.create_time.valid_set)
# print(a.create_time.invalid_set)
valid_max_count, valid_class, invalid_max_count, invalid_class = a.get_equivalent_class()
print(valid_max_count)
print(valid_class)
print(invalid_max_count)
print(invalid_class)
print(a.generate_valid_case(valid_max_count, valid_class))

# a = '{{  "user": "{user}",   "password"  :  ["a": " {a} ", "b": " {b} " ,"c": " {c} "]  ,  "number"  : {info}   }}'
# b = '{{ "user": "{user}"}}'
# c = '{{  "user": "{user}",   "password"  :  "{password}"  ,  "number"  : {info}   }}'


# span = re.search(r'[\{\[]{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{user\}[\s\"]*)[\}\]]{1}', b).span(1)
# print(span)
# print(b[:span[0]]+b[span[1]:])
#
# span = re.search(r'(,[\s\"]+\S[^\{]*[\s\"]+:[\s\"]*\{c\}[\s\"]*)[\}\]]{1}', a).span(1)
# print(span)
# print(a[:span[0]]+a[span[1]:])
#
# span = re.search(r',{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*{b}[\s\"]*,{1})', a).span(1)
# print(re.search(r',{1}([\s\"]+\S[^\{]*[\s\"]+:[\s\"]*{b}[\s\"]*,{1})', a))
# print(a[:span[0]]+a[span[1]:])
#
# span = re.search(r'["\s]*\{\s*info\s*\}[\s"]*', a).span()
# print(re.search(r'["\s]*\{\s*info\s*\}[\s"]*', a))
# print(re.sub(r'["\s]*\{\s*info\s*\}[\s"]*', 'null', a, count=1))
#
# md = '{{ "integer": {integer}, "number": {number}, "name": {name}, "bank": {bank}, "create_time": {create_time} }}'
# print(re.search(r'["\s]*\{\s*integer\s*\}[\s"]*', md))
# print(re.sub(r'["\s]*\{\s*integer\s*\}[\s"]*', 'null', md, count=1))

a = 'user={user}'
b = 'user={user}&password={password}&number={number}'

only_one = r'\s*(\S[^\{]*\s*=\s*\{\s*user\s*\}\s*$)'
first = r'\s*(\S[^\{]*\s*=\s*\{\s*user\s*\}\s*&*)'
mid = r'&+?(\s*\S[^\{]*\s*=\s*\{\s*password\s*\}\s*&+?)'
last = r'(&+?\s*\S[^\{]*\s*=\s*\{\s*number\s*\})\s*'
print(re.search(first, a).span(1))
# print('-' + re.sub(first, '', a, count=1) + '-')
span = re.search(first, a).span(1)
print('-' + a[:span[0]] + a[span[1]:] + '-')

