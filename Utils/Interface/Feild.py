from decimal import Decimal, InvalidOperation
import random
import re
import time


class Feild:

    def __init__(self, allow_none: bool, *args, **kwargs):
        """
        basic init function:
            check type of allow_none
        :param allow_none: allow feild is none or not
        :param args: None
        :param kwargs: None
        """
        self.valid_list = []
        self.invalid_list = []
        if not isinstance(allow_none, bool):
            raise InvalidFieldException('Allow_none must be type bool!')
        self.allow_none = allow_none

    def generate(self):
        """
        basic function:
            if allow none: valid: None(do not sed this key) and ''(empty value for this key);
            else: invalid: None(do not sed this key) and ''(empty value for this key).
        :return: None
        """
        if self.allow_none:
            self.valid_list.append([None, ''])
        else:
            self.invalid_list.append([None, ''])


class NumberFeild(Feild):

    def __init__(self, allow_none: bool, lt=None, le=None, gt=None, ge=None):
        """
        check duplication of bound
        check weather left bound is greater than right bound
        :param allow_none:
        :param lt:
        :param le:
        :param gt:
        :param ge:
        """
        super().__init__(allow_none)
        # required and duclicate
        # left bound
        if gt is None and ge is None:
            # missing left bound
            # raise InvalidFieldException('Left bound: gt or ge required!')
            # fix: concider if there are no limit about bound
            pass
        elif gt is not None and ge is not None:
            # duplicate left bound
            raise InvalidFieldException('Left bound: gt or ge duplicate define!')
        # right bound
        elif self.lt is None and self.le is None:
            # missing right bound
            # raise InvalidFieldException('Right bound: lt or le required!')
            # fix: concider if there are no limit about bound
            pass
        elif self.lt is not None and self.le is not None:
            # duplicate right bound
            raise InvalidFieldException('Right bound: lt or le duplicate define!')
        # bound logic check
        elif lt is not None:
            if gt is not None:
                if gt >= lt:
                    raise InvalidFieldException('Wrong bound: gt can not equals or greater than lt!')
            if ge is not None:
                if ge >= lt:
                    raise InvalidFieldException('Wrong bound: ge can not equals or greater than lt!')
        elif le is not None:
            if gt is not None:
                if gt >= le:
                    raise InvalidFieldException('Wrong bound: gt can not equals or greater than le!')
            if ge is not None:
                if ge >= le:
                    raise InvalidFieldException('Wrong bound: ge can not equals or greater than le!')
        else:
            raise InvalidFieldException(
                f'Unkown error: allow_none: {allow_none}, lt: {lt}, le； {le}, gt: {gt}, ge: {ge}')
        self.lt = lt
        self.le = le
        self.gt = gt
        self.ge = ge


class IntFeild(NumberFeild):

    def __init__(self, allow_none: bool, lt=None, le=None, gt=None, ge=None):
        super().__init__(allow_none, lt=None, le=None, gt=None, ge=None)
        if gt is not None or ge is not None:
            # fix: concider if there are no limit about bound
            # is integer or not
            if not isinstance(gt, int) or not isinstance(ge, int):
                raise InvalidFieldException('Left bound: must be integer!')
        if lt is not None or le is not None:
            # fix: concider if there are no limit about bound
            if not isinstance(lt, int) or not isinstance(le, int):
                raise InvalidFieldException('Right bound: must be integer!')

    def generate(self) -> dict:
        super().generate()
        # left bound
        if self.gt is not None:
            # valid: gt+1; invalid: gt, gt-1
            self.valid_list.append(self.gt + 1)
            self.invalid_list.append([self.gt, self.gt - 1])
        if self.ge is not None:
            # valid: ge, ge+1; invalid:ge-1
            self.valid_list.append([self.ge, self.ge + 1])
            self.invalid_list.append(self.ge - 1)
        # right bound
        if self.lt is not None:
            # valid: lt-1; invalid: lt, lt+1
            self.valid_list.append(self.lt - 1)
            self.invalid_list.append([self.lt, self.lt + 1])
        if self.le is not None:
            # valid: le-1, le; invalid:le+1
            self.valid_list.append([self.le - 1, self.le])
            self.invalid_list.append(self.le + 1)
        return {'valid': self.valid_list, 'invalid': self.invalid_list}


class FloatFeild(NumberFeild):

    def __init__(self, allow_none: bool, precision: int, lt=None, le=None, gt=None, ge=None):
        super().__init__(allow_none, lt=None, le=None, gt=None, ge=None)
        if not isinstance(precision, int):
            raise InvalidFieldException('Precision must be integer!')
        elif precision < 1:
            raise InvalidFieldException('Precision must greater than 0!')
        self.precision = precision
        if gt is not None or ge is not None:
            # fix: concider if there are no limit about bound
            # is float or not
            if not isinstance(gt, str) or not isinstance(ge, str):
                raise InvalidFieldException('Left bound: must be type str!')
        if lt is not None or le is not None:
            # fix: concider if there are no limit about bound
            if not isinstance(lt, str) or not isinstance(le, str):
                raise InvalidFieldException('Right bound: must be type str!')
        try:
            self.lt = Decimal(self.lt)
            self.le = Decimal(self.le)
            self.gt = Decimal(self.gt)
            self.ge = Decimal(self.ge)
        except InvalidOperation as e:
            # if there is non-numeric character in string
            raise InvalidFieldException(e.__str__())

    def generate(self) -> dict:
        super().generate()
        delta = 1/10**Decimal(str(self.precision))
        # left bound
        if self.gt is not None:
            # valid: gt+delta; invalid: gt, gt-delta
            self.valid_list.append(self.gt + delta)
            self.invalid_list.append([self.gt, self.gt - delta])
        if self.ge is not None:
            # valid: ge, ge+delta; invalid:ge-delta
            self.valid_list.append([self.ge, self.ge + delta])
            self.invalid_list.append(self.ge - delta)
        # right bound
        if self.lt is not None:
            # valid: lt-delta; invalid: lt, lt+delta
            self.valid_list.append(self.lt - delta)
            self.invalid_list.append([self.lt, self.lt + delta])
        if self.le is not None:
            # valid: le-delta, le; invalid:le+delta
            self.valid_list.append([self.le - delta, self.le])
            self.invalid_list.append(self.le + delta)
        return {'valid': self.valid_list, 'invalid': self.invalid_list}


class CharFeild(Feild):

    def __init__(self, allow_none: bool, template: str, min_length=None, max_length=None, reg=None):
        super().__init__(allow_none)
        if not isinstance(template, str):
            raise InvalidFieldException('Template must be valid string!')
        if min_length is not None:
            if not isinstance(min_length, int):
                raise InvalidFieldException('Min_length must be integer!')
            if min_length < 1:
                raise InvalidFieldException('Min_length must greater than 0!')
            if len(template) < min_length:
                raise InvalidFieldException('Template must be valid string!')
        if max_length is not None:
            if not isinstance(max_length, int):
                raise InvalidFieldException('Max_length must be integer!')
            if max_length < 1:
                raise InvalidFieldException('Max_length must greater than 0!')
        if min_length is not None and max_length is not None:
            if max_length > min_length:
                raise InvalidFieldException('Min_length can not greater than Max_length!')
        if not isinstance(reg, str):
            raise InvalidFieldException('Reg must be string!')
        self.template = template
        self.min_length = min_length
        self.max_length = max_length
        self.reg = reg

    def generate(self) -> dict:
        super().generate()
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if self.min_length is not None:
            # min, min+1
            if len(self.template) > self.min_length:
                self.valid_list.append([self.template[:self.min_length], self.template[:self.min_length + 1]])
            else:
                # len(template) == min_length
                tail = ''.join(random.choices(alphabet, k=1))
                self.valid_list.append([self.template[:self.min_length], self.template[:self.min_length] + tail])
            # min-1
            self.invalid_list.append(self.template[:self.min_length - 1])
        if self.max_length is not None:
            # max-1, max
            # max+1
            if len(self.template) > self.max_length:
                self.valid_list.append([self.template[:self.max_length - 1], self.template[self.max_length]])
                self.invalid_list.append(self.template[:self.max_length + 1])
            elif len(self.template) == self.max_length:
                self.valid_list.append([self.template[:self.max_length-1], self.template[self.max_length]])
                tail = ''.join(random.choices(alphabet, k=1))
                self.invalid_list.append(self.template[:self.max_length] + tail)
            else:
                tolerance = self.max_length - len(self.template)
                tail = ''.join(random.choices(alphabet, k=tolerance))
                self.valid_list.append([self.template + tail[:-1], self.template + tail])
                tail = ''.join(random.choices(alphabet, k=tolerance + 1))
                self.invalid_list.append(self.template + tail)
        if self.reg is not None:
            if not re.match(self.reg, self.template):
                raise InvalidFieldException('Template must be valid string!')
            else:
                inv_str = ''.join(random.choices(alphabet, k=len(self.template)))
                while re.match(self.reg, self.template) is not None:
                    inv_str = ''.join(random.choices(alphabet, k=len(self.template)))
                self.invalid_list.append(inv_str)
        return {'valid': self.valid_list, 'invalid': self.invalid_list}


class CollectionFeild(Feild):

    def __init__(self, allow_none: bool, template: list, value_type: type):
        super().__init__(allow_none)
        if not isinstance(template, list):
            raise InvalidFieldException('Template must be type list!')
        if len(template) < 1:
            raise InvalidFieldException('Template collection can not be empty!')
        if not isinstance(value_type, type):
            raise InvalidFieldException('Value_type must be str or int or float!')
        self.template = template
        self.value_type = value_type

    def generate(self) -> dict:
        super().generate()
        self.valid_list.append(self.template)
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if self.value_type == str:
            # make sure string not in template list
            inv_str = ''.join(random.choices(alphabet, k=len(self.template[0])))
            while inv_str in self.template:
                inv_str = ''.join(random.choices(alphabet, k=len(self.template[0])))
            self.invalid_list.append(inv_str)
        elif self.value_type == int:
            for num in self.template:
                if not isinstance(num, int):
                    raise InvalidFieldException('Template collection member are not type int!')
            self.invalid_list.append(max(self.template) + 1)
        elif self.value_type == float:
            for num in self.template:
                if not isinstance(num, float):
                    raise InvalidFieldException('Template collection member are not type float!')
            self.invalid_list.append(max(self.template) + 1.0)
        else:
            raise InvalidFieldException('Unsupport type!')
        return {'valid': self.valid_list, 'invalid': self.invalid_list}


class DatetimeFeild(Feild):

    def __init__(self, allow_none: bool, time_format: str, lt=None, le=None, gt=None, ge=None):
        super().__init__(allow_none)
        # todo

    def generate(self) -> dict:
        super().generate()
        # todo
        return {'valid': self.valid_list, 'invalid': self.invalid_list}









class InvalidFieldException(Exception):

    def __init__(self, string):
        self.error = string

    def __str__(self):
        return self.error








