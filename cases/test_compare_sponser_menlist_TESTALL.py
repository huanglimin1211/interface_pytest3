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
#一级菜单OK，二级菜单OK；
# role：3级tab或二级tab、4级button或3级button   menu:2级tab或3级tab居多，tab和button在一块
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
        # sleep(1)
        edit_employee_role(json_da)
    #直接通过[]，把id放到列表里了
        # res=get_roleDetails([id])
        res=get_roleDetails([rand_role_id])
        outsideMenu_role=res['resultInfo']['outsideMenus']

        account="15180619999"
        login_01(account)
        res = get_menulist_outside()
        outsideMenu_menu = res['resultInfo']


        # length_folder=len(outsideMenu_role)
        length_folder=len(outsideMenu_menu)
        for M in range(length_folder):
            if outsideMenu_role[M]['menuCode']==outsideMenu_menu[M]['menuCode']:
                pass
                print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code一致")
            else:
                print(outsideMenu_menu[M]['menuName'])
                print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code不一致!!!!!!!!!!!!!!!!!!!")
            # length_menu = len(outsideMenu_role[M]['children'])
            length_menu=len(outsideMenu_menu[M]['children'])
            for N in range(length_menu):
                children_role = outsideMenu_role[M]['children']
                children_menu = outsideMenu_menu[M]['children']
                if children_role[N]['menuType'] == 'MENU':
                    if children_role[N]['menuCode'] == children_menu[N]['menuCode']:
                        pass
                        print("菜单列表和角色接口-----第2级菜单Code一致")
                    else:
                        print(children_menu[N]['menuName'])
                        print("菜单列表和角色接口-----第2级菜单Code不一致!!!!!!!!!!!!!!!!!!!")


#遍历角色列表----更改员工的角色---登录员工账号查看菜单列表--对比角色菜单树的每个层级
def test_insidemenu_role_compare():
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
        insideMenu_role=res['resultInfo']['insideMenus']

        account="15180619999"
        login_01(account)
        res = get_menulist_inside()
        insideMenu_menu = res['resultInfo']


        length_folder=len(insideMenu_role)
        for M in range(length_folder):
            if insideMenu_role[M]['menuCode']==insideMenu_menu[M]['menuCode']:
                pass
                # print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code一致")
            else:
                print(insideMenu_menu[M]['menuName'])
                print("菜单列表和角色接口-----第一级菜单的第"+str(M+1)+"个Code不一致!!!!!!!!!!!!!!!!!!!")
            length_menu = len(insideMenu_role[M]['children'])
            for N in range(length_menu):
                children_role = insideMenu_role[M]['children']
                children_menu = insideMenu_menu[M]['children']
                if children_role[N]['menuType'] == 'MENU':
                    if children_role[N]['menuCode'] == children_menu[N]['menuCode']:
                        pass
                        # print("菜单列表和角色接口-----第2级菜单Code一致")
                    else:
                        print(children_menu[N]['menuName'])
                        print("菜单列表和角色接口-----第2级菜单Code不一致!!!!!!!!!!!!!!!!!!!")


def test_outsidemenu_doc_compare():
    #获取一级菜单名称
    operate = OperateExcel(filepath, 0)
    lines=operate.get_lines()
    print("一级菜单有"+str(lines)+"行~~~~~~~~~~~~~~~")
    outside_first_menu=[]
    for i in range(1,lines):
        first_data=operate.get_cell_value(i,1)
        if first_data != '':
            outside_first_menu.append(first_data)
    print(outside_first_menu)

#获取二级菜单名称
    outside_second_menu=[]
    #遍历表格的多少行（0,64），从第2行开始，因为第一行是标题
    for i in range(1,lines):
        second_data=operate.get_cell_value(i,3)
        if second_data != '':
            outside_second_menu.append(second_data)
    print(outside_second_menu)

    account = "16616102222"
    login_01(account)
    res = get_menulist_outside()
    outsideMenu_menu = res['resultInfo']

    length_folder = len(outsideMenu_menu)
    menu_num=0
    for M in range(len(outsideMenu_menu)):
        if outsideMenu_menu[M]['menuName']  in outside_first_menu:
            # print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Name一致")
            pass
        else:
            print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Name不一致!!!!!!!!!!!!!!!!!!!")
        length_menu = len(outsideMenu_menu[M]['children'])
        for N in range(length_menu):
            # children_role = outside_first_menu[M]['children']
            children_menu = outsideMenu_menu[M]['children']
            # if children_role[N]['menuType'] == 'MENU':
            #对比doc第二级和菜单列表的第2级
            if children_menu[N]['menuName']  in outside_second_menu:
                pass
                # print("菜单列表和角色接口-----第2级菜单Name一致")
            else:
                menu_num = menu_num + 1
                print(children_menu[N]['menuName'])
                print("菜单列表和角色接口-----第2级菜单Name不一致!!!!!!!!!!!!!!!!!!!")
    print("展会外--第2级菜单，请查看结果：有"+str(menu_num)+"个不一样")



def test_insidemenu_doc_compare():
    #获取一级菜单名称
    operate = OperateExcel(filepath, 1)
    lines=operate.get_lines()
    print("一级菜单有"+str(lines)+"行~~~~~~~~~~~~~~~")
    inside_first_menu=[]
    for i in range(1,lines):
        first_data=operate.get_cell_value(i,1)
        if first_data != '':
            inside_first_menu.append(first_data)
    # print(inside_first_menu)

    #获取二级菜单名称
    inside_second_menu=[]
    #遍历表格的多少行（0,64），从第2行开始，因为第一行是标题
    for i in range(1,lines):
        second_data=operate.get_cell_value(i,3)
        if second_data != '':
            inside_second_menu.append(second_data)
    # print(inside_second_menu)

    #获取3级TAB名称
    inside_third_tab=[]
    #遍历表格的多少行（0,64），从第2行开始，因为第一行是标题
    for i in range(3,lines):
        third_data=operate.get_cell_value(i,6)
        if third_data != '':
            inside_third_tab.append(third_data)
    # print(inside_third_tab)


    #获取4级按钮code
    inside_fourth_tab=[]
    #遍历表格的多少行（0,64），从第2行开始，因为第一行是标题
    for i in range(3,lines):
        fourth_data=operate.get_cell_value(i,8)
        if fourth_data != '':
            inside_fourth_tab.append(fourth_data)
    # print(inside_fourth_tab)

    account = "16616102222"
    login_01(account)
    res = get_menulist_inside()
    insideMenu_menu = res['resultInfo']

    length_folder = len(insideMenu_menu)
    menu_num=0
    buttonList=[]
    for M in range(len(insideMenu_menu)):
        if insideMenu_menu[M]['menuName']  in inside_first_menu:
            # print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Name一致")
            pass
        else:
            # menu_num = menu_num + 1
            print("菜单列表和角色接口-----第一级菜单的第" + str(M + 1) + "个Name不一致!!!!!!!!!!!!!!!!!!!")
        buttonList.append(insideMenu_menu[M]['buttonList'])
        length_menu = len(insideMenu_menu[M]['children'])
        for N in range(length_menu):
            children_menu = insideMenu_menu[M]['children']
            #对比doc第二级和菜单列表的第2级
            if children_menu[N]['menuName']  in inside_second_menu:
                pass
                # print("菜单列表和角色接口-----第2级菜单Name一致")
            else:
                menu_num = menu_num + 1
                print(children_menu[N]['menuName'])
                print("菜单列表和角色接口-----第2级菜单Name不一致!!!!!!!!!!!!!!!!!!!")
            TAB_menu=children_menu[N]
            buttonList.append(TAB_menu['buttonList'])
    print(buttonList)
    yuansu = []
    def bianli(lists):
        for i in lists:
            sleep(0.01)
            if type(i) != list:
                yuansu.append(i)
            else:
                bianli(i)
        # print("元素是 %s" %yuansu)
    bianli(buttonList)

    for T in inside_third_tab:
        print(T)
        if T in yuansu:
            # print("菜单列表和角色接口-----3级tab文档一样")
            pass
        else:
            print(T+"菜单列表和角色接口-----3级tab文档不一致!!!!!!!!!!!!!!!!!!!")

    for T in inside_fourth_tab:
        print(T)
        if T in yuansu:
            # print("菜单列表和角色接口-----4级button文档一样")
            pass
        else:
            print(T+"菜单列表和角色接口-----4级button文档不一致!!!!!!!!!!!!!!!!!!!")

    print(yuansu)
    print(len(yuansu))
    print("展会外--第2级菜单，请查看结果：有"+str(menu_num)+"个不一样")