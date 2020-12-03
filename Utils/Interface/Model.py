# coding:utf-8
from Utils.Interface.Field import *
import copy


class Model:

    def __init__(self, application_type: str, template_str: str = None, template_dict: dict = None):
        tips = """
        template_str and template_dict neither can be None.
        For template_str:
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
        if template_str is not None:
            if '{' not in template_str and '}' not in template_str:
                raise ValueError(tips)
        if template_str is None and template_dict is None:
            raise ValueError(tips)
        self.template_str = template_str
        self.template_dict = template_dict
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
            # only_one = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            # first = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*,)'
            # last = r'(,[\s\"]+\w+[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            # middle = r',{1}([\s\"]+\w+[^\{]*[\s\"]+:[\s\"]*\{' + field + r'\}[\s\"]*,{1})'
            only_one = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + field + r'\}[\]\s\"]*)[\}\]]{1}'
            first = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + field + r'\}[\]\s\"]*,)'
            last = r'(,[\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + field + r'\}[\s\"]*)[\}\]]{1}'
            middle = r',{1}([\s\[\"]*\w+[^\{][\[\"\s]*:[\s\"]*\{' + field + r'\}[\]\s\"]*,{1})'
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
            tmp = tmp[:spn[0]] + tmp[spn[1]:]
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
            tmp = tmp[:spn[0]] + tmp[spn[1]:]
        else:
            pass
        return tmp

    def __replace_empty(self, string, field):
        tmp = string
        if 'json' in self.application_type:
            obj = getattr(self, field)
            if isinstance(obj, NumberField) or isinstance(obj, BooleanField) or (
                    isinstance(obj, CollectionField) and obj.value_type != str):
                # replace :"{field_placeholder}" with :null
                ptn = r'["\s]*\{\s*' + field + r'\s*\}[\s"]*'
                tmp = re.sub(ptn, 'null', tmp, count=1)
            else:
                # replace with empty string :''
                ptn = r'\s*\{\s*' + field + r'\s*\}\s*'
                tmp = re.sub(ptn, '', tmp, count=1)
        elif 'x-www-form-urlencoded' in self.application_type:
            # replace with empty string :''
            ptn = r'\s*\{\s*' + field + r'\s*\}\s*'
            tmp = re.sub(ptn, '', tmp, count=1)
        else:
            pass
        return tmp

    def __recursion_replace(self, target_key, target_value, dictionery):
        temp = copy.deepcopy(dictionery)
        for key in temp.keys():
            if key == target_key:
                temp[key] = target_value
                break
            elif isinstance(temp[key], dict):
                temp[key] = self.__recursion_replace(target_key, target_value, temp[key])
            else:
                continue
        return temp

    def __recursion_pop(self, target_key, dictionery):
        temp = copy.deepcopy(dictionery)
        for key in temp.keys():
            if key == target_key:
                temp.pop(key)
                break
            if isinstance(temp[key], dict):
                temp[key] = self.__recursion_pop(target_key, temp[key])
        return temp

    def generate_valid_case(self, valid_set_max_count, valid_class_dict):
        valid_class_cases = []
        for i in range(0, valid_set_max_count):
            if self.template_str is not None:
                # count of valid class cases = valid_set_max_count
                tmp_str = self.template_str
                format_dict = {}
                for field in self.fields_name:
                    # replace placeholder with field value in template_str one by one
                    if i < len(valid_class_dict[field]):
                        # index not out of border
                        field_value = str(valid_class_dict[field][i])
                    else:
                        # index out of border, use value of index zero
                        field_value = str(valid_class_dict[field][0])
                    if 'None' not in field_value and 'empty' not in field_value:
                        format_dict[field] = field_value
                    elif 'empty' in field_value:
                        # empty
                        tmp_str = self.__replace_empty(tmp_str, field)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str, field)
                format_str = tmp_str.format(**format_dict)
                case = {'desc': f'valid_{i}', 'data': format_str}
                valid_class_cases.append(case)
            elif self.template_dict is not None:
                # count of valid class cases = valid_set_max_count
                tmp_dict = copy.deepcopy(self.template_dict)
                for field in self.fields_name:
                    # replace placeholder with field value in template_str one by one
                    if i < len(valid_class_dict[field]):
                        # index not out of border
                        field_value = valid_class_dict[field][i]
                    else:
                        # index out of border, use value of index zero
                        field_value = valid_class_dict[field][0]
                    if 'None' not in field_value and 'empty' not in field_value:
                        # format_dict[field] = str(valid_class_dict[field][i])
                        tmp_dict = self.__recursion_replace(field, field_value, tmp_dict)
                    elif 'empty' in field_value:
                        # empty
                        if 'json' in self.application_type:
                            obj = getattr(self, field)
                            if isinstance(obj, NumberField) or isinstance(obj, BooleanField) or (
                                    isinstance(obj, CollectionField) and obj.value_type != str):
                                tmp_dict = self.__recursion_replace(field, None, tmp_dict)
                            else:
                                tmp_dict = self.__recursion_replace(field, '', tmp_dict)
                        else:
                            tmp_dict = self.__recursion_replace(field, '', tmp_dict)
                    else:
                        # None
                        tmp_dict = self.__recursion_pop(field, tmp_dict)
                case = {'desc': f'valid_{i}', 'data': copy.deepcopy(tmp_dict)}
                valid_class_cases.append(case)
            else:
                pass
        return valid_class_cases

    def generate_invalid_case(self, invalid_class_dict, valid_class_dict):
        invalid_class_cases = []
        # one invalid field one time
        for field in invalid_class_dict.keys():
            for values in invalid_class_dict[field]:
                if self.template_str is not None:
                    # iterate
                    tmp_str = self.template_str
                    format_dict = {}
                    # one invalid field one time, the other field valid
                    for fid in self.fields_name:
                        if field == fid:
                            for valid_value in valid_class_dict[fid]:
                                # replace other field with valid value that not be None and empty
                                if 'None' not in str(valid_value) and 'empty' not in str(valid_value):
                                    format_dict[fid] = str(valid_value)
                            # in case of that there are no other value except 'None' or 'empty'
                            if fid not in format_dict.keys():
                                format_dict[fid] = ''
                    # replace target field with invalid value
                    if 'None' not in str(values) and 'empty' not in str(values):
                        format_dict[field] = str(values)
                    elif 'empty' in str(values):
                        # empty
                        tmp_str = self.__replace_empty(tmp_str, field)
                    else:
                        # None
                        tmp_str = self.__replace_none(tmp_str, field)
                    format_str = tmp_str.format(**format_dict)
                    case = {'desc': f'invalid {field}: {values}', 'data': format_str}
                    invalid_class_cases.append(case)
                elif self.template_dict is not None:
                    # iterate
                    tmp_dict = copy.deepcopy(self.template_dict)
                    # one invalid field one time, the other field valid
                    for fid in self.fields_name:
                        if field != fid:
                            for valid_value in valid_class_dict[fid]:
                                # replace other field with valid value that not be None and empty
                                if 'None' not in str(
                                        valid_value) and 'empty' not in str(valid_value):
                                    # format_dict[fid] = str(valid_value)
                                    tmp_dict = self.__recursion_replace(fid, valid_value, tmp_dict)
                                    break
                                # in case of that there are no other value except 'None' or 'empty'
                                elif 'empty' in str(valid_value):
                                    tmp_dict = self.__recursion_replace(fid, '', tmp_dict)
                                else:
                                    continue
                    # replace target field with invalid value
                    if 'None' not in str(values) and 'empty' not in str(values):
                        # format_dict[field] = str(values)
                        tmp_dict = self.__recursion_replace(field, values, tmp_dict)
                    elif 'empty' in str(values):
                        # empty
                        if 'json' in self.application_type:
                            obj = getattr(self, field)
                            if isinstance(obj, NumberField) or isinstance(obj, BooleanField) or (
                                    isinstance(obj, CollectionField) and obj.value_type != str):
                                tmp_dict = self.__recursion_replace(field, None, tmp_dict)
                            else:
                                tmp_dict = self.__recursion_replace(field, '', tmp_dict)
                        else:
                            tmp_dict = self.__recursion_replace(field, '', tmp_dict)
                    elif 'None' in str(values):
                        # None
                        tmp_dict = self.__recursion_pop(field, tmp_dict)
                    else:
                        pass
                    case = {'desc': f'invalid {field}: {values}', 'data': copy.deepcopy(tmp_dict)}
                    invalid_class_cases.append(case)
                else:
                    pass
        return invalid_class_cases

    def generate_test_case(self) -> dict:
        valid_max_cnt, valid_cls, invalid_max_cnt, invalid_cls = self.get_equivalent_class()
        valid_cases = self.generate_valid_case(valid_max_cnt, valid_cls)
        invalid_cases = self.generate_invalid_case(invalid_cls, valid_cls)
        return {'valid_cases': valid_cases, 'invalid_cases': invalid_cases}
