from decimal import Decimal, InvalidOperation
import random
import re
import time
import datetime
from dateutil.relativedelta import relativedelta


class Field:

    def __init__(self, allow_none: bool, *args, **kwargs):
        """
        basic init function:
            check type of allow_none
        :param allow_none: allow feild is none or not
        :param args: None
        :param kwargs: None
        """
        self.valid_set = set()
        self.invalid_set = set()
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
            self.valid_set.update(['None', 'empty'])
        else:
            self.invalid_set.update(['None', 'empty'])


class BooleanField(Field):

    def __init__(self, allow_none: bool):
        super().__init__(allow_none)

    def generate(self):
        super().generate()
        self.valid_set.update(['true', 'false'])


class NumberField(Field):

    def __init__(self, allow_none: bool, gt=None, ge=None, lt=None, le=None):
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
        if lt is None and le is None:
            # missing right bound
            # raise InvalidFieldException('Right bound: lt or le required!')
            # fix: concider if there are no limit about bound
            pass
        elif lt is not None and le is not None:
            # duplicate right bound
            raise InvalidFieldException('Right bound: lt or le duplicate define!')
        # bound logic check
        if lt is not None:
            if gt is not None:
                if float(gt) >= float(lt):
                    raise InvalidFieldException('Wrong bound: gt can not equals or greater than lt!')
            if ge is not None:
                if float(ge) >= float(lt):
                    raise InvalidFieldException('Wrong bound: ge can not equals or greater than lt!')
        if le is not None:
            if gt is not None:
                if float(gt) >= float(le):
                    raise InvalidFieldException('Wrong bound: gt can not equals or greater than le!')
            if ge is not None:
                if float(ge) >= float(le):
                    raise InvalidFieldException('Wrong bound: ge can not equals or greater than le!')
        # else:
        #     raise InvalidFieldException(
        #         f'Unkown error: allow_none: {allow_none}, lt: {lt}, le； {le}, gt: {gt}, ge: {ge}')
        self.lt = lt
        self.le = le
        self.gt = gt
        self.ge = ge


class IntField(NumberField):

    def __init__(self, allow_none: bool, gt=None, ge=None, lt=None, le=None):
        if gt is not None or ge is not None:
            # fix: concider if there are no limit about bound
            # is integer or not
            if not ((isinstance(gt, int)) or isinstance(ge, int)):
                raise InvalidFieldException('Left bound: must be integer!')
        if lt is not None or le is not None:
            # fix: concider if there are no limit about bound
            if not (isinstance(lt, int) or isinstance(le, int)):
                raise InvalidFieldException('Right bound: must be integer!')
        if gt is not None and lt is not None:
            if gt + 1 >= lt:
                raise InvalidFieldException('Invalid bound range!')
        super().__init__(allow_none, gt=gt, ge=ge, lt=lt, le=le)

    def generate(self) -> dict:
        super().generate()
        # left bound
        if self.gt is not None:
            # valid: gt+1; invalid: gt, gt-1
            if (self.lt is not None and (self.gt + 1) < self.lt) or (self.le is not None and (self.gt + 1) < self.le):
                # does not greater than right bound
                self.valid_set.add(self.gt + 1)
            self.invalid_set.update([self.gt, self.gt - 1])
        if self.ge is not None:
            # valid: ge, ge+1; invalid:ge-1
            self.valid_set.add(self.ge)
            if (self.lt is not None and (self.ge + 1) < self.lt) or (self.le is not None and (self.ge + 1) < self.le):
                # does not greater than right bound
                self.valid_set.add(self.ge + 1)
            self.invalid_set.add(self.ge - 1)
        # right bound
        if self.lt is not None:
            # valid: lt-1; invalid: lt, lt+1
            if (self.gt is not None and (self.lt - 1) > self.gt) or (self.ge is not None and (self.lt - 1) > self.ge):
                # does not less than left bound
                self.valid_set.add(self.lt - 1)
            self.invalid_set.update([self.lt, self.lt + 1])
        if self.le is not None:
            # valid: le-1, le; invalid:le+1
            if (self.gt is not None and (self.le - 1) > self.gt) or (self.ge is not None and (self.le - 1) > self.ge):
                # does not less than left bound
                self.valid_set.add(self.le - 1)
            self.valid_set.add(self.le)
            self.invalid_set.add(self.le + 1)
        return {'valid': self.valid_set, 'invalid': self.invalid_set}


class FloatField(NumberField):

    def __init__(self, allow_none: bool, precision: int, gt=None, ge=None, lt=None, le=None):
        if not isinstance(precision, int):
            raise InvalidFieldException('Precision must be integer!')
        elif precision < 1:
            raise InvalidFieldException('Precision must greater than 0!')
        self.precision = precision
        if gt is not None or ge is not None:
            # fix: concider if there are no limit about bound
            # is float or not
            if not (isinstance(gt, str) or isinstance(ge, str)):
                raise InvalidFieldException('Left bound: must be type str!')
        if lt is not None or le is not None:
            # fix: concider if there are no limit about bound
            if not (isinstance(lt, str) or isinstance(le, str)):
                raise InvalidFieldException('Right bound: must be type str!')
        super().__init__(allow_none, gt=gt, ge=ge, lt=lt, le=le)
        try:
            if self.lt is not None:
                self.lt = Decimal(self.lt)
            if self.le is not None:
                self.le = Decimal(self.le)
            if self.gt is not None:
                self.gt = Decimal(self.gt)
            if self.ge is not None:
                self.ge = Decimal(self.ge)
            if self.gt is not None and self.lt is not None:
                delta = 1 / 10 ** Decimal(str(precision))
                if self.gt + delta >= self.lt:
                    raise InvalidFieldException('Invalid bound range!')
        except InvalidOperation as e:
            # if there is non-numeric character in string
            raise InvalidFieldException(e.__str__())

    def generate(self) -> dict:
        super().generate()
        delta = 1 / 10 ** Decimal(str(self.precision))
        # left bound
        if self.gt is not None:
            # valid: gt+delta; invalid: gt, gt-delta
            if (self.lt is not None and (self.gt + delta) < self.lt) or (
                    self.le is not None and (self.gt + delta) < self.le):
                # gt+delta does not greater than right bound
                self.valid_set.add(self.gt + delta)
            self.invalid_set.update([self.gt, self.gt - delta])
        if self.ge is not None:
            # valid: ge, ge+delta; invalid:ge-delta
            self.valid_set.add(self.ge)
            if (self.lt is not None and (self.ge + delta) < self.lt) or (
                    self.le is not None and (self.ge + delta) < self.le):
                # ge+delta does not greater than right bound
                self.valid_set.add(self.ge + delta)
            self.invalid_set.add(self.ge - delta)
        # right bound
        if self.lt is not None:
            # valid: lt-delta; invalid: lt, lt+delta
            if (self.gt is not None and (self.lt - delta) > self.gt) or (
                    self.ge is not None and (self.lt - delta) > self.ge):
                # lt-delta does not less than left bound
                self.valid_set.add(self.lt - delta)
            self.invalid_set.update([self.lt, self.lt + delta])
        if self.le is not None:
            # valid: le-delta, le; invalid:le+delta
            if (self.gt is not None and (self.le - delta) > self.gt) or (
                    self.ge is not None and (self.le - delta) > self.ge):
                # lt-delta does not less than left bound
                self.valid_set.add(self.le - delta)
            self.valid_set.add(self.le)
            self.invalid_set.add(self.le + delta)
        return {'valid': self.valid_set, 'invalid': self.invalid_set}


class CharField(Field):

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
            if len(template) > max_length:
                raise InvalidFieldException('Template must be valid string!')
        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise InvalidFieldException('Min_length can not greater than Max_length!')
        if reg is not None and not isinstance(reg, str):
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
                # min+1 can not greater than max_length
                self.valid_set.add(self.template[:self.min_length])
                if self.min_length + 1 < self.max_length:
                    self.valid_set.add(self.template[:self.min_length + 1])
            else:
                # len(template) == min_length
                self.valid_set.add(self.template[:self.min_length])
                if self.reg is None:
                    # len(template) == min_length and reg is not none, min_length + 1 is meaningless
                    if self.min_length + 1 < self.max_length:
                        # min+1 can not greater than max_length
                        tail = ''.join(random.choices(alphabet, k=1))
                        self.valid_set.add(self.template[:self.min_length] + tail)
            # min-1
            self.invalid_set.add(self.template[:self.min_length - 1])
        if self.max_length is not None:
            # max-1, max
            # max+1
            if len(self.template) == self.max_length:
                # max-1 can not less than min_length
                if self.max_length - 1 > self.min_length:
                    self.valid_set.add(self.template[:self.max_length - 1])
                self.valid_set.add(self.template[:self.max_length])
                tail = ''.join(random.choices(alphabet, k=1))
                self.invalid_set.add(self.template[:self.max_length] + tail)
            else:
                # len(self.template < max_length
                self.valid_set.add(self.template)
                tolerance = self.max_length - len(self.template)
                if self.reg is None:
                    # len(self.template) < max_length and reg is not None, max_length - 1 and max_length is meaningless
                    tail = ''.join(random.choices(alphabet, k=tolerance))
                    # max-1 can not less than min_length
                    if self.max_length - 1 > self.min_length:
                        self.valid_set.add(self.template + tail[:-1])
                    self.valid_set.add(self.template + tail)
                tail = ''.join(random.choices(alphabet, k=tolerance + 1))
                self.invalid_set.add(self.template + tail)
        if self.reg is not None:
            if not re.match(self.reg, self.template):
                raise InvalidFieldException('Template must be valid string!')
            else:
                inv_str = ''.join(random.choices(alphabet, k=len(self.template)))
                # in case of reg pattern can match everything such as '.*'
                max_try = 10
                while re.match(self.reg, self.template) is not None and max_try > 0:
                    inv_str = ''.join(random.choices(alphabet, k=len(self.template)))
                    max_try -= 1
                if max_try > 0:
                    self.invalid_set.add(inv_str)
        return {'valid': self.valid_set, 'invalid': self.invalid_set}


class CollectionField(Field):

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
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if self.value_type == str:
            # make sure string not in template list
            inv_str = ''.join(random.choices(alphabet, k=len(str(self.template[0]))))
            while inv_str in self.template:
                inv_str = ''.join(random.choices(alphabet, k=len(str(self.template[0]))))
            self.invalid_set.add(inv_str)
        elif self.value_type == int:
            for num in self.template:
                if not isinstance(num, int):
                    raise InvalidFieldException('Template collection member are not type int!')
            self.invalid_set.add(max(self.template) + 1)
        elif self.value_type == float:
            for num in self.template:
                if not isinstance(num, float):
                    raise InvalidFieldException('Template collection member are not type float!')
            self.invalid_set.add(max(self.template) + 1.0)
        else:
            raise InvalidFieldException('Unsupported type!')
        self.valid_set.update(self.template)
        return {'valid': self.valid_set, 'invalid': self.invalid_set}


class DatetimeField(Field):

    def __init__(self, allow_none: bool, time_format: str, gt=None, ge=None, lt=None, le=None):
        hint = """Commonly used format codes:   
                %Y  Year with century as a decimal number.
                %m  Month as a decimal number [01,12].
                %d  Day of the month as a decimal number [01,31].
                %H  Hour (24-hour clock) as a decimal number [00,23].
                %M  Minute as a decimal number [00,59].
                %S  Second as a decimal number [00,61].
                %z  Time zone offset from UTC.
                %a  Locale's abbreviated weekday name.
                %A  Locale's full weekday name.
                %b  Locale's abbreviated month name.
                %B  Locale's full month name.
                %c  Locale's appropriate date and time representation.
                %I  Hour (12-hour clock) as a decimal number [01,12].
                %p  Locale's equivalent of either AM or PM.\n
                """
        super().__init__(allow_none)
        self.lt = lt
        self.le = le
        self.gt = gt
        self.ge = ge
        if time_format and not isinstance(time_format, str):
            raise InvalidFieldException('Time_format must be type str!')
        # left bound
        if gt is None and ge is None:
            # fix: concider if there are no limit about bound
            pass
        elif gt is not None and ge is not None:
            # duplicate left bound
            raise InvalidFieldException('Left bound: gt or ge duplicate define!')
        # right bound
        if lt is None and le is None:
            # fix: concider if there are no limit about bound
            pass
        elif lt is not None and le is not None:
            # duplicate right bound
            raise InvalidFieldException('Right bound: lt or le duplicate define!')
        # bound logic check
        if lt is not None:
            try:
                self.lt = datetime.datetime.strptime(lt, time_format)
                if gt is not None:
                    self.gt = datetime.datetime.strptime(gt, time_format)
                    if self.gt >= self.lt or self.__time_shift(self.gt, self.__get_delta_type(time_format),
                                                               1) >= self.lt:
                        raise InvalidFieldException('Wrong bound: gt can not equals or greater than lt!')
                if ge is not None:
                    self.ge = datetime.datetime.strptime(ge, time_format)
                    if self.ge >= self.lt:
                        raise InvalidFieldException('Wrong bound: ge can not equals or greater than lt!')
            except ValueError as e:
                raise InvalidFieldException(hint + e.__str__())
        if le is not None:
            try:
                self.le = datetime.datetime.strptime(le, time_format)
                if gt is not None:
                    self.gt = datetime.datetime.strptime(gt, time_format)
                    if self.gt >= self.le:
                        raise InvalidFieldException('Wrong bound: gt can not equals or greater than le!')
                if ge is not None:
                    self.ge = datetime.datetime.strptime(ge, time_format)
                    if self.ge >= self.le:
                        raise InvalidFieldException('Wrong bound: ge can not equals or greater than le!')
            except ValueError as e:
                raise InvalidFieldException(hint + e.__str__())
        # else:
        #     raise InvalidFieldException(
        #         f'Unknown error: allow_none: {allow_none}, lt: {lt}, le； {le}, gt: {gt}, ge: {ge}')
        self.time_format = time_format

    @staticmethod
    def __time_shift(input_time: datetime.datetime, shift_type: str, delta: int):
        """self, days: float = ..., seconds: float = ..., microseconds: float = ...,
                     milliseconds: float = ..., minutes: float = ..., hours: float = ...,
                     weeks: float = ..., *, fold: int = ..."""
        if not isinstance(input_time, datetime.datetime):
            raise InvalidFieldException('Input_time must be type datetime!')
        if shift_type not in ['seconds', 'minutes', 'hours', 'days', 'months', 'years']:
            raise InvalidFieldException('Shift_type must be in: seconds, minutes, hours, days, months, years!')
        if not isinstance(delta, int):
            raise InvalidFieldException('Delta must be type int!')
        if shift_type == 'seconds':
            return input_time + datetime.timedelta(seconds=delta)
        elif shift_type == 'minutes':
            return input_time + datetime.timedelta(minutes=delta)
        elif shift_type == 'hours':
            return input_time + datetime.timedelta(hours=delta)
        elif shift_type == 'days':
            return input_time + datetime.timedelta(days=delta)
        elif shift_type == 'months':
            return input_time + relativedelta(months=delta)
        elif shift_type == 'years':
            return input_time + relativedelta(years=delta)
        else:
            raise InvalidFieldException('Unsupported shift type!')

    @staticmethod
    def __get_delta_type(time_format):
        if '%S' in time_format:
            return 'seconds'
        elif '%M' in time_format:
            return 'minutes'
        elif '%H' in time_format:
            return 'hours'
        elif '%d' in time_format:
            return 'days'
        elif '%m' in time_format:
            return 'months'
        elif '%Y' in time_format:
            return 'years'
        else:
            raise InvalidFieldException('Unsupported time format!')

    def generate(self) -> dict:
        super().generate()
        delta_type = self.__get_delta_type(self.time_format)
        # left bound
        if self.gt is not None:
            # gt+delta
            # gt+delta can not greater than right bound
            gt_plus_delta = self.__time_shift(self.gt, delta_type, 1)
            if (self.lt is not None and gt_plus_delta < self.lt) or (self.le is not None and gt_plus_delta < self.le):
                self.valid_set.add(gt_plus_delta.strftime(self.time_format))
            # gt, gt-delta
            self.invalid_set.update([self.gt.strftime(self.time_format),
                                     self.__time_shift(self.gt, delta_type, -1).strftime(self.time_format)])
        if self.ge is not None:
            # ge, ge+delta
            self.valid_set.add(self.ge.strftime(self.time_format))
            # ge+delta can not greater than right bound
            ge_plus_delta = self.__time_shift(self.ge, delta_type, 1)
            if (self.lt is not None and ge_plus_delta < self.lt) or (self.le is not None and ge_plus_delta < self.le):
                self.valid_set.add(ge_plus_delta.strftime(self.time_format))
            # ge-delta
            self.invalid_set.add(self.__time_shift(self.ge, delta_type, -1).strftime(self.time_format))
        # right bound
        if self.lt is not None:
            # lt-delta
            # lt-delta can not less than left bound
            lt_minus_delta = self.__time_shift(self.lt, delta_type, -1)
            if (self.gt is not None and lt_minus_delta > self.gt) or (self.ge is not None and lt_minus_delta > self.ge):
                self.valid_set.add(lt_minus_delta.strftime(self.time_format))
            # lt, lt+delta
            self.invalid_set.update([self.lt.strftime(self.time_format),
                                     self.__time_shift(self.lt, delta_type, 1).strftime(self.time_format)])
        if self.le is not None:
            # le, le-delta
            self.valid_set.add(self.le.strftime(self.time_format))
            # le-delta can not less than left bound
            le_minus_delta = self.__time_shift(self.le, delta_type, -1)
            if (self.gt is not None and le_minus_delta > self.gt) or (self.ge is not None and le_minus_delta > self.ge):
                self.valid_set.add(le_minus_delta.strftime(self.time_format))
            # le+delta
            self.invalid_set.add(self.__time_shift(self.le, delta_type, 1).strftime(self.time_format))
        return {'valid': self.valid_set, 'invalid': self.invalid_set}


class InvalidFieldException(Exception):

    def __init__(self, string):
        self.error = string

    def __str__(self):
        return self.error
