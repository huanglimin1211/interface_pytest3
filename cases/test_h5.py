#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,pytest,os,random,requests,json,allure
import  jsonpath
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.interface_get import Run_Main
from util.connect_db_test import ConnectDB
from util.read_yaml import ReadYaml
from util.operate_json import  OperateJson
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告


#此处设置用户数，建议放在yaml文件中，因为即可放list也可以放dict
# current_path=os.path.dirname(os.path.realpath('__file__'))
yaml_path='../data/test_data.yml'
json_path='../data/H5.json'
test_data=ReadYaml(yaml_path).read_y()
json_data=OperateJson(json_path).get_json()
expect={"resultCode":"SUCCESS"}  #一般断言code和msg就可以了
print(json_data)

# rand=random.randint(0,2)#包含结尾
rand=0
account=test_data['test_data_login'][rand]['account']
nickName = test_data['test_data_login'][rand]['nickName']
host='https://pch5test8.digitalexpo.com'
tenantId='10014032021013100016120583168790000000000328375'

db=ConnectDB()

@pytest.mark.skip
def test_2():
    assert 1==1




@pytest.fixture(scope="module") #一个py文件只登陆一次
def login():
    url=host+'/api/v2/app/login'
    data={"account":account,
          "tenantId":"10014032021013100016120583168790000000000328375",
          "verifyCode":"888888",
          "userPassword":"59406454EA450777AD40F6516A2D19BF",
          "loginType":"VERIFY_CODE","terminalType":"H5"}
    headers=json_data['headers']
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    global token
    token=res['resultInfo']['authorization']
    assert res['resultCode']=='SUCCESS'
    # print(token)

def test_usrInfo(login):
    url=host+'/api/v2/app/user/info'
    data=None
    # headers={
    #     "x-ca-tenant-id": "10014032021013100016120583168790000000000328375",
    #     "x-ca-exhibition-id": "10015032021013100016120640620470000000000271269",
    #     "x-ca-brand-id":"10014022021013100016120583171440000000000326917",
    #     'authorization': token
    # }
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print("---------------你好啊，我是"+nickName)
    assert res['resultInfo']['nickName']==nickName


def test_search_exhibits():
    '''#用户搜索展品、展商、会议，传入不同的参数'''
    url='https://pch5test8.digitalexpo.com/api/v2/app/search/exhibits?'
    data={"keyWord":"测试",
          "pageNum":1,
          "pageSize":16}
    headers=json_data['headers']
    # headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url,data,headers)
    print(res)
    exhibitsList=jsonpath.jsonpath(res,"$.resultInfo.list[*].exhibitsName")
    exhibitsList2=jsonpath.jsonpath(res,"$..exhibitsName")#2个点和3个点都可以
    assert exhibitsList2[0] =="测试"
    # assert res['resultCode'] == expect['resultCode']



def test_search_information():
    '''#用户搜索展品、展商、会议，传入不同的参数'''
    url='https://pch5test8.digitalexpo.com/api/v2/app/search/information?'
    data={"keyWord":"测试",
          "pageNum":1,
          "pageSize":16}
    headers=json_data['headers']
    # headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url,data,headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

    #数据库断言
    sql='SELECT count(*) FROM  expo_core_information WHERE  exhibition_id = "10015032021013100016120640620470000000000271269" AND title LIKE "%测试%" AND publish_status = "PUBLISHED" AND is_delete = 0 AND language_type IN ("ALL", "zh-cn")'
    count=db.select(sql)  #搜索出来是tuple元组类型
    print(count)
    assert count[0] == res['resultInfo']['total']

def test_exhibits_detail(login):
    '''查看展品详情'''
    url=host+'/api/v2/app/exhibits/10015052021042500016193343343822115734782753192?exhibitionId=10015032021013100016120640620470000000000271269&preview=false'
    data=None
    # data={"exhibitionId":10015032021013100016120640620470000000000271269,
    #       "preview":False
    #       }
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url,data,headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

    #数据库断言
    sql='select product_name,owner_user_id from expo_core_product where product_id="10015012021020100016121497642290000000000497689"'
    db_result=db.select(sql)  #搜索出来是tuple元组类型
    print(db_result)
    product_name=json.loads(db_result[0])#字符串转成字典
    # assert product_name['zh-cn'] == res['resultInfo']['appProductInfo']['productName']

def test_live_detail(login):
    '''查看直播详情'''
    url=host+'/api/v2/app/living/detail?'
    data={"livingId":100112012021040100016172798264968691423133537686,
          "preview":False
          }
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url,data,headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


def test_exhibits_collect_create(login):
    '''展品详情--收藏展品'''
    url=host+'/api/v2/app/collect/create?'
    data={"followType":"EXHIBIT",
          "followId":"10015052021042500016193343343822115734782753192",
          "device":"H5"}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

def test_exhibits_collect_cancel(login):
    '''展品详情--取消收藏展品'''
    url=host+'/api/v2/app/collect/cancel?'
    data={"followType":"EXHIBIT",
          "followId":"10015052021042500016193343343822115734782753192"}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


def test_card_myself(login):
    '''查看自己的名片'''
    url=host+'/api/v2/app/card/card?'
    data=None
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

def test_edit_mycard(login):
    '''编辑名片'''
    url=host+'/api/v2/app/card/save'
    data={"name":"7441555556817","mobile":"17816104037",
          "title":"十一一你好哦十一你好哦十一你好哦套路图",
          "email":"b.bmakm@pxerwhzj.vb",
          "company":"十一这是个刚领科技哈十一这是个刚领科技哈十一这是个刚领科技哈"}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

def test_exchange_card(login):
    '''和展商交换名片'''
    url=host+'/api/v2/app/card/exchange'
    data={"exhibitorId":"10017012021030900016152570780825517859012187211",
          "exhibitionId":"10015032021013100016120640620470000000000271269",
          "sourceId":"10015052021042500016193343343822115734782753192",
          "sourceType":"EXHIBIT"}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


def test_cardslist(login):
    '''查看名片夹列表'''
    url=host+'/api/v2/app/card/cards?'
    data=None
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

def test_remove_card(login):
    '''移除展商A的名片'''
    url=host+'/api/v2/app/card/remove'
    data={"exhibitorId":"10017012021030900016152570780825517859012187211",
          "exhibitionId":"10015032021013100016120640620470000000000271269"}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


def test_tickets_list(login):
    '''查看门票列表,参数里goodIds就是门票列表的id'''
    url=host+'/api/v2/app/ticket?pageSize=10&pageNum=1&exhibitionId=10015032021013100016120640620470000000000271269&goodsIds=100119002021110900016364498033842057770996019390%2C100119002021102500016351751265907283462859128401%2C100119002021093000016329678599143569298273901185%2C100119002021092800016328358899527798674096823611%2C100119002021111800016372273537719856711869583867'
    data=None
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']

def test_buy_ticket(login):
    '''门票下单,包括门票id、购买人id、张数、商家id'''
    url=host+'/api/v2/app/appOrderCenter/save'
    data={"orderType":"TICKET","orderSource":"H5","isOnline":"ONLINE","buyId":"10018012021030800016151756674982175925440228630","buyName":"88888","exhibitionId":"10015032021013100016120640620470000000000271269","exhibitionName":"纸业制造大会第一届234纸业制造大会第一届1大幅度4方法","goodsAmount":12.88,"tenantId":"10014032021013100016120583168790000000000328375","orderGoodsInfoList":[{"stockId":"10015172021111800016372273537733268236152263280","exhibitionId":"10015032021013100016120640620470000000000271269","isFreight":0,"freight":0,"discountAmount":0,"originalPrice":12.88,"costPrice":12.88,"goodsPrice":12.88,"goodsSpecs":[{"name":"18收费票--12月过期","value":"2021/11/18-2021/12/31"},{"name":"18收费票--12月过期","value":"2021/12/29-2021/12/31"}],"goodsName":"18收费票--12月过期","goodsAmount":12.88,"sellerId":"10018012021013100016120583168550000000000447424","goodsId":"100119002021111800016372273537719856711869583867","buyNum":1}]}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    # assert res['resultCode'] == 'EXCEEDING_THE_PURCHASE_LIMIT'
    assert res['resultCode'] == expect['resultCode']


def test_order_list(login):
    '''查看门票订单列表'''
    url=host+'/api/v2/app/appOrderCenter/list'
    data={"orderType":"ALL","orderStatus":"ALL","pageNum":1,"pageSize":10}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


#获取标签类目列表---后台主办配置的
def test_tagList(login):
    url=host+'/api/v2/app/preference/list'
    data=None
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    assert '小米' in  res['resultInfo']['CATEGORY'][1]['preferenceName']

#设置标签类目列表---用户手动选择
@pytest.mark.parametrize("input_category,input_tag,expect",test_data['test_data_tag'])
def test_selectTag(login,input_category,input_tag,expect):
    url=host+'/api/v2/app/preference'
    print(input_category)
    print(expect)
    data={"categoryIdList":input_category,
          "tagIdList":input_tag}
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)
    assert res['resultCode'] == expect['resultCode']


#获取标签类目列表---用户手动选择
def test_get_tagList(login):
    url=host+'/api/v2/app/preference'
    data=None
    headers=json_data['headers']
    headers['authorization']=token
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    print(res)
    #取参数化最后一组，标签进行对比，是否一样
    # assert test_data['test_data_tag'][-1][0]==res['resultInfo']['categoryIdList']
    assert test_data['test_data_tag'][-1][1]==res['resultInfo']['tagIdList']
    # assert '02' in  res['resultInfo']['tagIdList'][0]

if __name__ == '__main__':
#注意，生成allure报告，是用allure命令行生成的
    # pytest  'test_h5.py'  --alluredir=../result    #设置测试结果的路径，生成json等结果
    # allure generate ../result/ -o ../report/ --clean   #生成报告的路径，并且清除上次结果
    # pytest  'test_h5.py'  -s -q --alluredir=../result   #-q静默执行-s显示调试内容
    pytest.main('-s','-v','--alluredir','../result')
    os.system("allure generate ../result/ -o ../report/ --clean")