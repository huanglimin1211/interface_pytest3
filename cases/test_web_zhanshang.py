#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest,os,random
import requests,json
import logging
from src.interface_get import Run_Main
from util.getTicket import  GetTicket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告



@pytest.mark.skip
def test_2():
    assert 1==1


#测试环境五一
host = 'https://fiveone.digitalexpo.com'
tenantId='10014032021042900016196959127459967122081127855'
exhibitionId='10015032021072000016267474096106330737612565547'
getticket=GetTicket()


host = 'https://jieroutest.digitalexpo.com'
tenantId='10014032021013100016120583168790000000000328375'
exhibitionId='10015032021013100016120640620470000000000271269'

def get_randomInt():
    res=random.randint(0,1000)
    return  str(res)


#主办登录成功   /api/v2/auth/sys/login
@pytest.fixture()
def login_01():
    #获取组织列表
    url = host + '/api/v2/auth/sys/login'
    data = {"verifyCode":"888888",
            "account":"17816108888",
            'x-ca-exhibition-id': exhibitionId,
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
    global goodid
    token=res['resultInfo']['authorization']


def test_add_exbits(login_01):
    '''主办新增展品,展品名称'''
    url = host + '/api/v2/product'
    data ={"isClaim": 0,
	"exhibitsVisibility": "1",
	"viewGroupId": 0,
	"productCategoryInfoList": ["1387746624260673538,1387746624273256450,1387746624281645057,1387746624290033665,1387746624294227970"],
	"productPics": ["https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/exhibits/pic/20211216173237019_bv3dl9e2.jpeg"],
	"coverVideo": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/exhibits/video/20211216173304013_pje6b6r1.mp4",
	"sellingPointCn": "卖点描述（CN）卖点描述（CN）卖点描",
	"sellingPointEn": "卖点描述（EN）卖点描述（EN）卖点描述（EN）",
	"materialInfoList": [{
		"businessId": "rc-upload-1639640224874-22",
		"materialName": "6813983E1.pdf",
		"materialUrl": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/pdf/20211216173252441_sly0g5uz.pdf",
		"businessType": "PRODUCT",
		"materialSize": 21336
	}],
	"productDescription": "{}",
	"productName": "{\"zh-cn\":\"产品11111\"}",
	"extParam": "{\"sellingPoint\":{\"zh-cn\":\"卖点描述（CN）卖点描述（CN）卖点描\",\"en-us\":\"卖点描述（EN）卖点描述（EN）卖点描述（EN）\"}}",
	"productDescriptionContent": None,
	"exhibitorId": "10017012021121600016396253286921763620654743193"
}

    #更改展品字段名称
    productName={"zh-cn":"小方产品"+get_randomInt(),"en-us":"cp1230211"+get_randomInt()}
    data['productName']=str(productName)
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("新增展品成功啦~")
    assert res['resultCode'] == "SUCCESS"

def test_add_meetings(login_01):
    '''主办新增会议,会议名称'''
    url = host + '/api/v2/meetings/addOrUpdateMeeting'
    data ={
	"type": "LIVE",
	"cover": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/ad/20211216175735428_msfi2ldf.jpeg",
	"outward": 1,
	"hostUserId": "10018012021121500016395635803182401759429387205",
	"planStartTime": "2021-12-16 13:59:00",
	"planEndTime": "2021-12-16 17:59:00",
	"targetTagListInfoList": [],
	"meetingGuestList": [],
	"meetingMaterialList": [{
		"name": "6813983E1.pdf",
		"size": 21336,
		"type": "application/pdf",
		"url": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/pdf/20211216175742804_9cw6wiu5.pdf"
	}],
	"meetingAgendaList": [],
	"status": "INIT",
	"ownerType": "EXHIBITOR",
	"ownerId": "10017012021121600016396253286921763620654743193",
	"reviewable": 1,
	"showVisitor": 1,
	"title": {"zh-cn": "会议名称","en-us": ""},
	"description": "{\"zh-cn\":\"会议介绍(CN)\\n\",\"en-us\":\"\"}",
	"location": "{\"zh-cn\":\"\",\"en-us\":\"\"}",
	"channelNameList": ["中文"],
	"provider": "ALI_YUN",
	"praiseSwitch": 1,
	"chatSwitch": 1,
	"isCreateSubmit": True
}

    #更改会议字段名称
    title={"zh-cn":"小方会议"+get_randomInt(),"en-us":"xfhuiyi"+get_randomInt()}
    data['title']=title
    # data['title']=str(title)
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("新增会议成功啦~")
    assert res['resultCode'] == "SUCCESS"


@pytest.mark.skip
def test_add_lives(login_01):
    '''主办新增直播,直播名称'''
    url = host + '/api/v2/multimedia/live'
    data ={
	"source": "LIVE",
	"coverPic": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/ad/20211216185944668_sa4k9n6n.jpeg",
	"hostUserId": "10018012021121500016395635803182401759429387205",
	"planStartTime": "2021-12-16 18:59:00",
	"planEndTime": "2021-12-16 18:59:00",
	"materialSaasReqs": [{
		"name": "6813983E1.pdf",
		"size": 21336,
		"type": "application/pdf",
		"url": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021072000016267474096106330737612565547/pdf/20211216185950887_eeaq0ehp.pdf"
	}],
	"liveStatus": "INIT",
	"ownerType": "EXHIBITOR",
	"ownerId": "10017012021121600016396253286921763620654743193",
	"reviewable": 1,
	"showVisitor": 0,
	"liveName": "{\"zh-cn\":\"243\",\"en-us\":\"直播名称(EN)\"}",
	"liveDesc": "{\"zh-cn\":\"直播介绍(CN)\\n直播介绍(CN)\\n直播介绍(CN)\\n直播介绍(CN)\\n\",\"en-us\":\"直播介绍(EN)\\n直播介绍(EN)\\n直播介绍(EN)\\n\"}",
	"targetTagListInfoList": [],
	"praiseSwitch": 1,
	"chatSwitch": 1,
	"isCreateSubmit": True
}

    #更改直播字段名称
    liveName={"zh-cn":"小方直播"+get_randomInt(),"en-us":"xfzhibo"+get_randomInt()}
    data['liveName']=str(liveName)
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("新增直播成功啦~")
    assert res['resultCode'] == "SUCCESS"


if __name__ == '__main__':
    pytest.main("-s","-v")