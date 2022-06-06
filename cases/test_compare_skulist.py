#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,pytest,os,random,requests,json,allure
from seleniumwire import webdriver
from time import  sleep
from src.interface_get import Run_Main
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from util.operate_excel import OperateExcel
# dr = webdriver.Chrome()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




host = 'https://jieroutest.digitalexpo.com/'
tenantId='10014032021013100016120583168790000000000328375'
zhanhui_id='1000149'
account=16616108888

prod_host='https://iwhale.digitalexpo.com/'
prod_tenantId='10014032021032000016161752045388335528290236709'

filepath = os.path.abspath("../data/case_packet_function_name.xls")  # 表格关闭才可以
operate = OperateExcel(filepath, 0)

#主办登录成功   /api/v2/auth/sys/login
@pytest.fixture()
def login_01():
    #获取组织列表
    url = host + '/api/v2/auth/sys/login'
    data = {"verifyCode":"888888","account":"16616102222",
            "tenantId":tenantId,"loginType":"VERIFY_CODE"}
    headers = {
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    userId = res['resultInfo']['userId']
    accessCode = res['resultInfo']['accessCode']
    userOrganizeInfoList = res['resultInfo']['userOrganizeInfoList']
    bizProfileId = res['resultInfo']['userOrganizeInfoList'][0]['bizProfileId']
    rootUserId = res['resultInfo']['userOrganizeInfoList'][0]['userId']

    # 获取token
    url_login2 = host + '/api/v2/pc'
    data_login2 = {
      "userId": userId,
      "accessCode": accessCode,
      "tenantId": tenantId,
      "rootUserId": rootUserId,
      "bizProfileId": bizProfileId,
        "userOrganizeInfoList":userOrganizeInfoList
    }
    req = Run_Main(url_login2, data_login2, headers, 'POST')
    res = req.request_post_json(url_login2, data_login2, headers)
    assert res['resultCode']=="SUCCESS"
    global token
    token=res['resultInfo']['authorization']



#获取套餐列表
def test_sku_list(login_01):
    url = host+'api/v2/package/sku/function/code/my?'
    rand_str=str(random.randint(1,10000))
    data={"skuType":"SPONSOR"}
    headers = {
         'authorization':token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    print(len(res['resultInfo']['functionInfoList']))
    assert res['resultCode']=='SUCCESS'
    return res




def test_compare_list(login_01):
    res=test_sku_list(login_01)
    length=len(res['resultInfo']['functionInfoList'])
    diffs = []
    col_result = []
    for i in range(length):
        try:
            col_result.append(res['resultInfo']['functionInfoList'][i]['functionName'])
        except:
            print("写入实际列表失败")
    col_expect = operate.get_cols_data(0)
    print("------预期功能列表项有%s个" % len(col_expect), "------预期功能项列表%s" % col_expect)
    print("------实际功能列表项有%s个" % len(col_result), "------实际功能项列表为%s" % col_result)
    for t in col_expect:
        if t not in col_result:
            diffs.append(t)#预期中有的，实际没有的打印出来
    if diffs==[]:
        print("实际和预期的套餐功能项一致，恭喜！")
    else:
        print("------实际和预期的套餐功能项一致，不一样的有%s" %diffs)

    # 把不同的地方列表写入exlce某一列
    for m in range(len(diffs)):
        try:
            operate.write_data(m, 2, diffs[m])
        except:
            print("写入文件失败")


    # 把返回值列表写入exlce某一列中
    for j in range(length):
        try:
            operate.write_data(j, 1, res['resultInfo']['functionInfoList'][j]['functionName'])
        except:
            print("写入文件失败")

