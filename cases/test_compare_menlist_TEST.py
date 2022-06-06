#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,pytest,os,random,requests,json,allure
from seleniumwire import webdriver
from time import  sleep
from src.interface_get import Run_Main
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from util.operate_json import  OperateJson
from lxml import etree
from xlwt import Workbook
from util.operate_excel import OperateExcel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




host = 'https://jieroutest.digitalexpo.com/'
tenantId='10014032021013100016120583168790000000000328375'
zhanhui_id='1000149'
prod_host='https://iwhale.digitalexpo.com/'
prod_tenantId='10014032021032000016161752045388335528290236709'
json_path='../data/web_test.json'
json_data=OperateJson(json_path).get_json()
print(json_data)
filepath = os.path.abspath("../data/菜单-权限-910测试.xlsx")  # 表格关闭才可以，文件名可以自动补全
operate = OperateExcel(filepath, 0)

#主办登录成功   /api/v2/auth/sys/login
# @pytest.fixture()
def login_01(account):
    #获取组织列表
    url = host + '/api/v2/auth/sys/login'
    data = {"verifyCode":"888888","account":account,
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

def get_queryRoleList():
    url=host+'/api/v2/organization/permission/role/queryRoleList'
    data=None
    headers = {
         'authorization':token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    return res


def change_json(jsondata,id):
    data=jsondata['roleModel']
    for i in range(len(data)):
        # print(i)
        if data[i]["roleId"]==id:
            data[i]["isCheck"] = True
        else:
            data[i]["isCheck"] = False
    return  jsondata


def edit_employee_role(data):
    url=host+'/api/v2/organization/permission/employee'
    # data=json_data['edit_employee_role']
    headers = {
        'Content-Type': 'application/json',
        'authorization': token,
        # 'authorization':'eyJhbGciOiJIUzI1NiJ9.eyJhcHAiOmZhbHNlLCJkZXZpY2VUeXBlIjpudWxsLCJ1aWQiOiIxMDAxODAxMjAyMTA0MDkwMDAxNjE3OTU4Njc5MzQ3NDIxNjM1OTE0MDU4MTYzMiIsInN0YSI6MTYyNjg1ODU3ODM5NCwiZW50ZXJwcmlzZUxldmVsIjpudWxsLCJtb2JpbGUiOm51bGwsInRlbmFudElkIjoiMTAwMTQwMzIwMjEwMTMxMDAwMTYxMjA1ODMxNjg3OTAwMDAwMDAwMDAzMjgzNzUiLCJhcHBXb3JrZXIiOmZhbHNlLCJyb290VXNlcklkIjoiMTAwMTgwMTIwMjEwMTMxMDAwMTYxMjA1ODMxNjg1NTAwMDAwMDAwMDA0NDc0MjQiLCJlbWFpbCI6bnVsbCwiYWNjb3VudCI6IjE3ODE2MTA1NTU1In0.jp2bL04dVpje1dpQa9BcstRxCzebpytYgE1gVfwe9Us',
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    return res
    # print(res)

def get_roleDetails(data):
    url=host+'/api/v2/organization/menu/mergeRoleDetailedByIds'
    # data=["10010042021052600016220426710836383850424367487"]
    headers = {
        'Content-Type': 'application/json',
        'authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    return res

def get_menulist_outside():
    url = host + '/api/v2/organization/menu/menuList?'
    data = {"insideExhibition": "false"}
    headers = {
        'authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    return res

def get_menulist_inside():
    url = host + '/api/v2/organization/menu/menuList?'
    data = {"insideExhibition": "true"}
    headers = {
        'authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    return res


#遍历角色列表----更改员工的角色---登录员工账号查看菜单列表--对比角色菜单树的每个层级
def test_outsidemenu_role_compare():
    account2="16616102222"
    login_01(account2)
    res=get_queryRoleList()
    for ls in res['resultInfo']:
        rand_role_id=ls['roleId']
        roleNameCn=ls['roleNameCn']
        print("现在的角色是" + roleNameCn + "#$%^&********************************")
        data=json_data['edit_employee_role']
        # rand_role_id="10010012021012000016111334966700000000000390395"
        # json_da=change_json(data,id)
        json_da=change_json(data,rand_role_id)
        edit_employee_role(json_da)
    #直接通过[]，把id放到列表里了
        # res=get_roleDetails([id])
        res=get_roleDetails([rand_role_id])
        outsideMenu_role=res['resultInfo']['outsideMenus']

        account="15180619999"
        login_01(account)
        res = get_menulist_outside()
        outsideMenu_menu = res['resultInfo']


        length_folder=len(outsideMenu_role)
        for M in range(length_folder):
            if outsideMenu_role[M]['menuCode']==outsideMenu_menu[M]['menuCode']:
                print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code一致")
            else:
                print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code不一致!!!!!!!!!!!!!!!!!!!")
            length_menu = len(outsideMenu_role[M]['children'])
            for N in range(length_menu):
                children_role = outsideMenu_role[M]['children']
                children_menu = outsideMenu_menu[M]['children']
                if children_role[N]['menuType'] == 'MENU':
                    if children_role[N]['menuCode'] == children_menu[N]['menuCode']:
                        print("菜单列表和角色接口-----第2级菜单Code一致")
                    else:
                        print("菜单列表和角色接口-----第2级菜单Code不一致!!!!!!!!!!!!!!!!!!!")


#遍历角色列表----更改员工的角色---登录员工账号查看菜单列表--对比角色菜单树的每个层级-------905最新哦
def test_insidemenu_role_compare():
    account2="16616102222"
    login_01(account2)
    res=get_queryRoleList()
    # for ls in res['resultInfo']:
        # rand_role_id=ls['roleId']
        # roleNameCn=ls['roleNameCn']
        # print("现在的角色是" + roleNameCn + "#$%^&********************************")
    data=json_data['edit_employee_role']
    rand_role_id="10010012021012000016111334966700000000000390395"
    json_da=change_json(data,id)
    json_da=change_json(data,rand_role_id)
    edit_employee_role(json_da)
#直接通过[]，把id放到列表里了
    # res=get_roleDetails([id])
    res=get_roleDetails([rand_role_id])
    insideMenu_role=res['resultInfo']['insideMenus']

    account="15180619999"
    login_01(account)
    res = get_menulist_inside()
    insideMenu_menu = res['resultInfo']

    # 遍历角色列表----更改员工的角色---登录员工账号查看菜单列表--对比角色菜单树的每个层级
    # 一级菜单OK，二级菜单OK；
    # role：3级tab或二级tab、4级button或3级button   menu显示在buttonList:2级tab或3级tab居多，tab和button在一块，
    length_folder=len(insideMenu_role)
    for M in range(length_folder):
        if insideMenu_role[M]['menuCode']==insideMenu_menu[M]['menuCode']:
            # print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code一致")
            pass
        else:
            print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code不一致!!!!!!!!!!!!!!!!!!!")
        length_menu = len(insideMenu_role[M]['children'])
        for N in range(length_menu):
            children_role = insideMenu_role[M]['children']
            children_menu = insideMenu_menu[M]['children']
            if children_role[N]['menuType'] == 'MENU':
                if children_role[N]['menuCode'] == children_menu[N]['menuCode']:
                    # print("菜单列表和角色接口-----第2级菜单Code一致")
                    pass
                else:
                    print("菜单列表和角色接口-----第2级菜单Code不一致!!!!!!!!!!!!!!!!!!!")
            if children_role[N]['menuType'] == 'TAB':
            # if children_role[N]['menuType'] == 'BUTTON':#好像没有button？？
                if children_role[N]['menuCode']  in insideMenu_menu[M]['buttonList']:
                    print("菜单列表和角色接口-----第2级TAB的Code一致")
                    pass
                else:
                    print("菜单列表和角色接口-----第2级TAB的Code不一致!!!!!!!!!!!!!!!!!!!")
            # try:
            #     length_TAB=len(children_role[N]['children'])
            #     for T in range(length_TAB):
            #         TAB_role=children_role[N]['children']
            #         TAB_menu=children_menu[N]
            #         #role接口返回的第3级可能是tab，也可能是button
            #         # print(TAB_menu['buttonList'])
            #         # print("这个是角色接口的3级mencode+"+TAB_role[T]['menuCode'])
            #         if TAB_role[T]['menuCode'] in TAB_menu['buttonList']:
            #             pass
            #             # print("菜单列表和角色接口------------第3级TAB的Code一致")
            #         else:
            #             print("菜单列表和角色接口-------------第3级TAB的Code不一致!!!!!!!!!!!!!!!!!!!")
            #         #如果role接口的第3级是tab，那么一般都会有下一级button，也可能无下级
            #         if TAB_role[T]['menuType'] == 'TAB' and len(TAB_role[T]['children']) !=0 :
            #             # print(TAB_role[T]['children'])
            #             button_list_role=TAB_role[T]['children']
            #             # print(button_list_role[0]['menuCode'])
            #             # print(TAB_menu['buttonList'])
            #             length_button=len(button_list_role)
            #             for B in  range(length_button):
            #                 if button_list_role[B]['menuCode'] in TAB_menu['buttonList']:
            #                     # print("菜单列表和角色接口------------第4级button的Code一致")
            #                     pass
            #                 else:
            #                     print("菜单列表和角色接口-------------第4级button的Code不一致!!!!!!!!!!!!!!!!!!!")
            #             # length_button=len(button_list)
            # except:
            #     print("没有3级哦~~~~~~~~~~~~~~~")







#登录高级管理员工账号查看菜单列表--对比角色菜单树的每个层级--第一层级菜单，存list并set去重，菜单名称在文档的list里
def test_outsidemenu_doc_compare():
    operate.get_lines()
    outside_first_menu=[]
    for i in range(1,35):
        firt_data=operate.get_cell_value(i,1)
        if firt_data != '':
            outside_first_menu.append(firt_data)
    print(outside_first_menu)

#登录高级管理员工账号查看菜单列表--对比角色菜单树的每个层级--第一层级菜单，存list并set去重，菜单名称在文档的list里
# def test_outsidemenu_doc_compare_finally():
#     #获取一级菜单名称
#     operate.get_lines()
#     outside_first_menu=[]
#     for i in range(1,35):
#         first_data=operate.get_cell_value(i,1)
#         if first_data != '':
#             outside_first_menu.append(first_data)
#     print(outside_first_menu)
#
# #获取二级菜单名称
#     outside_second_menu=[]
#     for i in range(1,35):
#         second_data=operate.get_cell_value(i,1)
#         if second_data != '':
#             outside_second_menu.append(second_data)
#     print(outside_second_menu)
#
#     account = "16616102222"
#     login_01(account)
#     res = get_menulist_outside()
#     outsideMenu_menu = res['resultInfo']
#
#     length_folder = len(outsideMenu_menu)
#     for M in range(len(outside_first_menu)):
#         if outside_first_menu[M] == outsideMenu_menu[M]['menuName']:
#             print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Code一致")
#         else:
#             print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Code不一致!!!!!!!!!!!!!!!!!!!")
#         length_menu = len(outsideMenu_menu[M]['children'])
#         for N in range(len(outside_second_menu)):
#             # children_role = outside_first_menu[M]['children']
#             children_menu = outsideMenu_menu[M]['children']
#             # if children_role[N]['menuType'] == 'MENU':
#             if outside_first_menu[N] == children_menu[N]['menuName']:
#                 print("菜单列表和角色接口-----第2级菜单Code一致")
#             else:
#                 print("菜单列表和角色接口-----第2级菜单Code不一致!!!!!!!!!!!!!!!!!!!")