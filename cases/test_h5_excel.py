#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,pytest,os,random,requests,json,allure
import logging,jsonpath
from out.log import Logger
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.interface_get import Run_Main
from util.read_yaml import ReadYaml
from util.operate_json import  OperateJson
from util.operate_excel import OperateExcel
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告



# current_path=os.path.dirname(os.path.realpath('__file__'))
yaml_path='../data/test_data.yml'
json_path='../data/H5.json'
test_data=ReadYaml(yaml_path).read_y()
json_data=OperateJson(json_path).get_json()
expect={"resultCode":"SUCCESS"}  #一般断言code和msg就可以了
print(json_data)



#1204新增
operate=OperateExcel('../data/case_test_H5_simple.xls',0)
log=Logger('../out/h5_all.log',level='debug')
# rand=random.randint(0,2)#包含结尾
rand=0
account=test_data['test_data_login'][rand]['account']
nickName = test_data['test_data_login'][rand]['nickName']
base_url="https://pch5test8.digitalexpo.com"
tenantId='10014032021013100016120583168790000000000328375'
exhibitionId='10015032021013100016120640620470000000000271269'
brandId="10014022021013100016120583171440000000000326917"





@pytest.fixture(scope="module") #一个py文件只登陆一次
def login():
    url=base_url+'/api/v2/app/login'
    data={"account":account,
          "tenantId":tenantId,
          "verifyCode":"888888",
          "userPassword":"59406454EA450777AD40F6516A2D19BF",
          "loginType":"VERIFY_CODE",
          "terminalType":"H5"}
    headers=json_data['headers']
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    global token
    token=res['resultInfo']['authorization']
    assert res['resultCode']=='SUCCESS'
    # print(token)


@pytest.mark.parametrize('data',operate.read_excel())
#login要放在前面
def test_h5_case(login,data):
    headers={
        "x-ca-tenant-id": tenantId,
        "x-ca-exhibition-id": exhibitionId,
        "x-ca-brand-id":brandId,
        "x-access-lang":"zh-cn",
        'authorization': token
    }
    log.logger.info(data)
    log.logger.info(type(data[3]))

    ispass=False
    caseId=data[0]
    excelurl=data[2]
    exceldata=data[3]
    excelmethod=data[5]
    isRun=data[4]
    expect=data[7]
    exceltitle=data[1]
    httpResult=data[8]
    excuteResult=data[9]

    if isRun.upper()=="YES":
        if excelmethod.upper()=='POST':
            res=requests.post(url=base_url+str(excelurl),json=eval(exceldata),headers=headers,verify=False).json()
        elif excelmethod.upper()=="GET":
            res=requests.get(url=base_url+str(excelurl),headers=headers,verify=False).json()
    # eval()可以把字符串格式转化为json格式
    log.logger.info(res)
    # assert res['resultCode']=='SUCCESS'
    assert res['resultCode']==expect
    if res['resultCode']==expect:
        log.logger.info("测试用例："+exceltitle+"，执行通过！")
        ispass=True
    else :
        log.logger.info("测试用例："+exceltitle+"，没有通过")
        ispass=False

    caseId=int(caseId)
    log.logger.info(caseId)
    operate.write_data(caseId,9,json.dumps(res))#dict不能写入excel，要转为json字符串才能写入excel
    operate.write_data(caseId,8,ispass)


if __name__ == '__main__':
    pytest.main('-s','-v','--alluredir','../result')
    os.system("allure generate ../result/ -o ../report/ --clean")