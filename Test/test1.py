from Utils.Interface.Model import *


class A(Model):
    integer = IntField(True, ge=1, lt=3)
    number = FloatField(False, 1, gt='1.0', le='1.1', accept_none=True)
    name = CharField(False, '13829302938', min_length=11, max_length=11, reg='^1[0-9]{10}$')
    bank = CollectionField(False, [1.0, 8.2, 10.0], float)
    create_time = DatetimeField(False, '%Y-%m-%d %H:%M:%S', ge='2019-12-31 23:59:59', lt='2020-01-01 00:00:00')


templ_str = '{{ "integer": {integer}, "number": {number}, "name": "{name}", "bank": {bank}, "create_time": "{create_time}" }}'
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
# print(a.generate_valid_case(valid_max_count, valid_class))
print(invalid_max_count)
print(invalid_class)
# print(a.generate_invalid_case(invalid_class, valid_class))
print(a.generate_test_case())

a = '{{  "user": "{user}",   "password"  :  ["a": " {a} ", "b": " {b} " ,"c": " {c} "]  ,  "number"  : {info}   }}'
b = '{{ "user": "{user}"}}'
c = '{{  "user": "{user}",   "password"  :  "{password}"  ,  "number"  : {info}   }}'
only_one = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + 'user' + r'\}[\]\s\"]*)[\}\]]{1}'
first = r'[\{\[]{1}([\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + 'integer' + r'\}[\]\s\"]*,)'
last = r'(,[\s\"]+\w+[^\{]*[\s\"]+:[\[\s\"]*\{' + 'c' + r'\}[\s\"]*)[\}\]]{1}'
middle = r',{1}([\s\[\"]*\w+[^\{][\[\"\s]*:[\s\"]*\{' + 'b' + r'\}[\]\s\"]*,{1})'

span = re.search(only_one, b).span(1)
print(span)
print(b[:span[0]]+b[span[1]:])

span = re.search(last, a).span(1)
print(span)
print(a[:span[0]]+a[span[1]:])

span = re.search(middle, a).span(1)
print(re.search(middle, a))
print(a[:span[0]]+a[span[1]:])

span = re.search(last, a).span(1)
print(re.search(last, a))
print(a[:span[0]]+a[span[1]:])

md = '{{ "integer": {integer}, "number": {number}, "name": {name}, "bank": {bank}, "create_time": {create_time} }}'
print(re.search(first, md))
print(re.sub(first, 'null', md, count=1))

# '{{"accessToken": "{accessToken}","itemCodes": ["{itemCodes}"],"status": "{status}","pageSize":  {pageSize},"subApply": "{subApply}","areaCode": "{areaCode}"}}'
# '{{"accessToken": "{accessToken}","status": "{status}","pageSize":  {pageSize},"subApply": "{subApply}","areaCode": "{areaCode}", "itemCodes": ["{itemCodes}"] }}'

d = '{{"accessToken": "{accessToken}","itemCodes": [""],"status": "{status}","pageSize":  {pageSize},"subApply": "{subApply}","areaCode": "{areaCode}"}}'
middle = r',{1}([\s\[\"]*\w+[^\{][\[\"\s]*:[\s\"]*\{status\}[\s\"]*,{1})'
print(re.search(middle, d))
spn = re.search(middle, d).span(1)
print(spn)
print(d[:spn[0]]+d[spn[1]:])



# a = 'user={user}'
# b = 'user={user}&password={password}&number={number}'
#
# only_one = r'\s*(\S[^\{]*\s*=\s*\{\s*user\s*\}\s*$)'
# first = r'\s*(\S[^\{]*\s*=\s*\{\s*user\s*\}\s*&*)'
# mid = r'&+?(\s*\S[^\{]*\s*=\s*\{\s*password\s*\}\s*&+?)'
# last = r'(&+?\s*\S[^\{]*\s*=\s*\{\s*number\s*\})\s*'
# print(re.search(first, a).span(1))
# # print('-' + re.sub(first, '', a, count=1) + '-')
# span = re.search(first, a).span(1)
# print('-' + a[:span[0]] + a[span[1]:] + '-')
