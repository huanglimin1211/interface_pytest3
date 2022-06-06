# coding= utf-8
import json


class Common_Util(object):
    """docstring for Common_Util"""

    def is_contain(self, str_one, str_two):
        flag = None
        if str_one in str_two:
            flag = True
        else:
            flag = False
        return flag


if __name__ == '__main__':
    common = Common_Util()
    expect = 'SUCCESS'
    res = {'traceId': '1623406305735301889684978', 'success': True, 'resultCode': 'SUCCESS', 'errorMsg': None, 'extInfo': None}
    print(type(res))
    res = json.dumps(res, indent=2, sort_keys=True, ensure_ascii=False)
    print(type(res))
    flag=common.is_contain(expect, res)
    print(flag)
