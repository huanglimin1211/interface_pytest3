#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,pytest,os,random,requests,json,allure
from seleniumwire import webdriver
from time import  sleep
from src.interface_get import Run_Main
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from util.operate_excel import OperateExcel
dr = webdriver.Chrome()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




host = 'https://jieroutest.digitalexpo.com/'
tenantId='10014032021013100016120583168790000000000328375'
zhanhui_id='1000149'
prod_host='https://iwhale.digitalexpo.com/'
prod_tenantId='10014032021032000016161752045388335528290236709'

#主办登录成功   /api/v2/auth/sys/login
@pytest.fixture()
def login_01():
    global token
    dr.get("https://jieroutest.digitalexpo.com/admin/user/login")
    sleep(3)
    dr.find_element_by_xpath("//*[@id='verifyCode']").send_keys("888888")
    sleep(1)
    dr.find_element_by_xpath("//*[@id='mobileNumber']").send_keys("15180619999")
    sleep(1)
    dr.find_element_by_xpath("//*[@id='root']/div/div[2]/div[2]/div[2]/div[2]/form/div[4]/div/div/div/button").click()
    sleep(2)
    # Access requests via the `requests` attribute
    for request in dr.requests:
        try:
            if request.response and "Authorization" in request.headers:
                print(request.headers["Authorization"])
                token=request.headers["Authorization"]
        except:
            print("没有找到token")
    dr.close()


def write_excel(yuansu,N):
    # 创建一个工作簿
    w = Workbook()
    # 创建一个工作表
    ws = w.add_sheet('1')
    length = len(yuansu)
    for M in range(length):
        try:
            ws.write(M, N, yuansu[M])
        except:
            print("写入文件失败")
    print("写入完毕~~~~~~~~~~~~~~~")
    print("总共生成: %s条数据" %length)
    w.save('../data/case_menulist_name.xls')



#获取套餐列表
def test_menu_list(login_01):
    menulist_menuCode_folder=[]
    menulist_menuName_folder=[]
    menulist_menuCode_MENU=[]
    menulist_menuName_MENU=[]
    menulist_menuCode_BUTTON=[]
    menulist_menuName_BUTTON=[]
    filepath = os.path.abspath("../data/case_menulist_name&code.xls")  # 表格关闭才可以
    operate = OperateExcel(filepath, 0)
    url = host+'/api/v2/organization/menu/menuList?'
    rand_str=str(random.randint(1,10000))
    data={"insideExhibition": "false"}
    headers = {
        # 'Content-Type': 'application/json',
         'authorization':token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    # print(len(res['resultInfo'][0]['children']))
    # print(res['resultInfo'][0]['children'][0]['menuCode'])
    length_folder=len(res['resultInfo'])
    for M in range(length_folder):
        children = res['resultInfo'][M]['children']
        # print(res['resultInfo'][M]['children'])
        # print('\n')
        menulist_menuCode_folder.append(res['resultInfo'][M]['menuCode'])
        # 把返回值列表写入exlce某一列中
        try:
            operate.write_data(M, 1, res['resultInfo'][M]['menuCode'])
        except:
            print("写入文件失败")
        length_menu = len(children)
        for i in range(length_menu):
            sleep(1)
            print(children[i]['menuCode'])
            print('\n')
            print(children[i]['menuName'])
            print('\n')
            menulist_menuCode_MENU.append(children[i]['menuCode'])
    print(menulist_menuCode_folder)
    print(menulist_menuCode_MENU)
    for j in range(len(menulist_menuCode_MENU)):
        try:
            operate.write_data(j, 2, menulist_menuCode_MENU[j])
        except:
            print("写入文件失败")
    assert res['resultCode']=='SUCCESS'


def test_get_roleDetails(login_01):
    role_menuCode_folder=[]
    role_menuName_folder=[]
    role_menuCode_MENU=[]
    role_menuName_MENU=[]
    role_menuCode_BUTTON=[]
    role_menuName_BUTTON=[]
    url=host+'/api/v2/organization/menu/mergeRoleDetailedByIds'
    data=["10010042021052600016220426710836383850424367487"]
    headers = {
        'Content-Type': 'application/json',
        'authorization': token,
        # 'authorization':'eyJhbGciOiJIUzI1NiJ9.eyJhcHAiOmZhbHNlLCJkZXZpY2VUeXBlIjpudWxsLCJ1aWQiOiIxMDAxODAxMjAyMTA0MDkwMDAxNjE3OTU4Njc5MzQ3NDIxNjM1OTE0MDU4MTYzMiIsInN0YSI6MTYyNjg1ODU3ODM5NCwiZW50ZXJwcmlzZUxldmVsIjpudWxsLCJtb2JpbGUiOm51bGwsInRlbmFudElkIjoiMTAwMTQwMzIwMjEwMTMxMDAwMTYxMjA1ODMxNjg3OTAwMDAwMDAwMDAzMjgzNzUiLCJhcHBXb3JrZXIiOmZhbHNlLCJyb290VXNlcklkIjoiMTAwMTgwMTIwMjEwMTMxMDAwMTYxMjA1ODMxNjg1NTAwMDAwMDAwMDA0NDc0MjQiLCJlbWFpbCI6bnVsbCwiYWNjb3VudCI6IjE3ODE2MTA1NTU1In0.jp2bL04dVpje1dpQa9BcstRxCzebpytYgE1gVfwe9Us',
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    length_folder=len(res['resultInfo']['outsideMenus'])
    for M in range(length_folder):
        # print(res['resultInfo']['outsideMenus'][M]['children'])
        # print('\n')
        role_menuCode_folder.append(res['resultInfo']['outsideMenus'][M]['menuCode'])
        # 把返回值列表写入exlce某一列中
        try:
            operate.write_data(M, 5, res['resultInfo']['outsideMenus'][M]['menuCode'])
        except:
            print("写入文件失败")
        length_menu = len(res['resultInfo']['outsideMenus'][M]['children'])
        for i in range(length_menu):
            children=res['resultInfo']['outsideMenus'][M]['children']
            if children[i]['menuType']=='MENU':
                print(children[i]['menuCode'])
                print('\n')
                print(children[i]['menuName'])
                print('\n')
                role_menuCode_MENU.append(children[i]['menuCode'])
                try:
                    operate.write_data(i, 6, children[i]['menuCode'])
                except:
                    print("写入文件失败")
    print(role_menuCode_folder)
    print(role_menuCode_MENU)
    assert res['resultCode']=='SUCCESS'