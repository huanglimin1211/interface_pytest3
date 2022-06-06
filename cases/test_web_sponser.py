#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest,os,random
import requests,json
import logging
from src.interface_get import Run_Main
from util.connect_db_test import ConnectDB
from util.getTicket import  GetTicket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告



@pytest.mark.skip
def test_2():
    assert 1==1

host = 'https://jieroutest.digitalexpo.com'
tenantId='10014032021013100016120583168790000000000328375'
exhibitionId='10015032021013100016120640620470000000000271269'
# zhanhui_id='1000149'
getticket=GetTicket()


def get_randomInt():
    res=random.randint(0,1000)
    return  str(res)


#主办登录成功   /api/v2/auth/sys/login
@pytest.fixture()
def login_01():
    #获取组织列表
    url = host + '/api/v2/auth/sys/login'
    data = {"verifyCode":"888888",
            # "account":"16616102222",
            "account":"19916105555",
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



def test_add_information(login_01):
    '''主办新增资讯'''
    url = host + '/api/v2/information/addOrEdit?'
    data ={
	"informationId": "",
	"title": "{\"zh-cn\":\"鸟语花12345\"}",
	"cover": "{\"zh-cn\":\"https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021013100016120640620470000000000271269/ad/20220105002904670_9bnu8ws5.jpeg\"}",
	"languageType": "zh-cn",
	"content": "{\"zh-cn\":\"<!DOCTYPE html><html>\\n  <head>\\n  <meta name=\\\"viewport\\\"content=\\\"width=device-width, initial-scale=1, maximum-scale=1\\\">\\n  <style>\\n    #haojing_body {\\n      margin: 0;\\n      padding: 0 3%;\\n      background-color: white;\\n      color: black;\\n      font-size: 16px;\\n    }\\n    #haojing_body a {\\n      color: #2f54eb;\\n      text-decoration: underline;\\n    }\\n    #haojing_body img {\\n      max-width: 100%;\\n    }\\n    #haojing_body video {\\n      max-width: 100%;\\n    }\\n    #haojing_body p {\\n      word-break: break-all;\\n      min-height: 1em;\\n      margin: 0;\\n      padding: 0;\\n    }\\n    #haojing_body hr{\\n      display: block;\\n      unicode-bidi: isolate;\\n      margin-block-start: 0.5em;\\n      margin-block-end: 0.5em;\\n      margin-inline-start: auto;\\n      margin-inline-end: auto;\\n      overflow: hidden;\\n      border-style: inset;\\n      border-width: 1px;\\n  }\\n    #haojing_body h1{ font-size:2em; margin: .67em 0 }\\n    #haojing_body h2{ font-size:1.5em; margin: .75em 0 }\\n    #haojing_body h3{ font-size:1.17em; margin: .83em 0 }\\n    #haojing_body h4, blockquote, ul,fieldset, form,ol, dl, dir,menu { margin: 1.12em 0}\\n    #haojing_body h5 { font-size:.83em; margin: 1.5em 0 }\\n    #haojing_body h6{ font-size:.75em; margin: 1.67em 0 }\\n    #haojing_body h1, h2, h3, h4,h5, h6, b,strong  { font-weight: bolder }\\n    #haojing_body.mobile {\\n      font-size: 14px;\\n    }\\n    #haojing_body a::before {\\n      background-repeat: no-repeat;\\n      width: 1em;\\n      height: 1em;\\n      vertical-align: text-top;\\n      display: inline-block;\\n      content: \\\"\\\";\\n      line-height: 1;\\n      margin-right: 3px;\\n    }\\n    #haojing_body a[href]::before {\\n      background-image: url(\\\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAEKADAAQAAAABAAAAEAAAAAA0VXHyAAABC0lEQVQ4EcVSMW7CQBCctULppA0i1LwlEr+ITAcFJQVPQInokOjyBxo+kipFHEQLuMXLrMOeDiQDqfDJ2tXdzNzN3AH3/uSWAzxP9VVKzAyrCXrrviyc9+DNpWpkVbwY5ijUdnziTV3tzDVVIPV1FZxwak9gxO0O/W2BIcnCsaHfggKZi1kNGUQ+RUssJUG3AiomjymmX2+yi4neB4Hmh+b02aoWBHtRjC8RXeDEj0/+pwYBXk8mgpz/L0p80tyQ/r+b7zqyPOpEg4VzgIdoQryFBteZH0PkRvE7qBVwQRPaFPiB4qmaS7BaD+QvK04EC044r5Y+dwk3wHDLGHNVwMD2fI/55NbHAvfvD7uQV+HAsyIfAAAAAElFTkSuQmCC\\\");\\n    }\\n    #haojing_body a:not([href])::before {\\n      background-image: url(\\\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAEKADAAQAAAABAAAAEAAAAAA0VXHyAAABj0lEQVQ4EcWQvUsDQRDFZy6JNhKIUcmHVhEstLKSCKJ2NmltbUQlJBcrUbAXBTWHEYyWNrbaKIJ/gGBtIwGj5CRR0ggqJje+A/dYJMQyB8vMzc7v7Zsh6vTH/xmIHcqI80076JtCcxVnu2LyieLaCsQOZFwadCVEfQBKzBQXoW7EJdvkoitiKKW/MW7JhNOkGxc2mNZfcpzwM40C/oLImupvKeDCTaFrNAUNg0xY3nKBcoZKEKxDJKQE/CrRI+A9Euphg5YBvEf3pWwEKBWzaB71CDGdqv6WDnA5hlO1s3yEJdUgMuQ0qIBaE69fGj7KKQFviRFL+qF+BsU7AEnMmYT9VCXLF9G8vOK/C3sIKlBFzwE7lIfADBo/sVoTL9UdohCEV1ALw/atgvSo72AOF7ad483fhl7Mvgo3uxCrkZ8yOqhyz4EwvWGe8GBBht1LwBsujNTG3bSd5nsF6dHbQdSSRXGoiMIHgArGSSB/8gVo9jnNDzqk554DbPwYcy7gPAIeQNM5B2iyHawLdS7/Aaa9g2B/Pz2tAAAAAElFTkSuQmCC\\\");\\n    }\\n\\n    #haojing_body .media-wrap.image-wrap a[href]::before {\\n      background-image: none;\\n    }\\n    #haojing_body ul,\\n    #haojing_body ol {\\n      padding-left: 2em;\\n    }\\n    #haojing_body ul li {\\n      list-style: disc;\\n    }\\n    #haojing_body ol li {\\n      list-style: decimal;\\n    }\\n  </style>\\n  </head>\\n  <body id=\\\"haojing_body\\\">\\n  <p>大家好，2022年即将到来。我在北京向大家致以新年祝福！</p><p></p><p>回首这一年，意义非凡。我们亲历了党和国家历史上具有里程碑意义的大事。“两个一百年”奋斗目标历史交汇，我们开启了全面建设社会主义现代化国家新征程，正昂首阔步行进在实现中华民族伟大复兴的道路上。</p>\\n  <div id=\\\"mark\\\">\\n  </div>\\n  </body>\\n  <script>\\n      const isMobile = /Android|webOS|iPhone|iPod|BlackBerry/i.test(\\n        navigator.userAgent,\\n      );\\n\\n      if (isMobile) {\\n        const __styleEle = document.getElementById(\\\"haojing_body\\\");\\n        __styleEle.className = \\\"mobile\\\";\\n      }\\n    </script>\\n  </html>\"}",
	"publishType": "RIGHT_NOW",
	"status": "AUDITING",
	"materialList": [{
		"thumbInfo": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021013100016120640620470000000000271269/pdf/20220105002955475_csd3d7g8.pdf",
		"url": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021013100016120640620470000000000271269/pdf/20220105002955475_csd3d7g8.pdf",
		"size": 21336,
		"type": "application/pdf",
		"name": "6813983E1.pdf"
	}]
}
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,  #展会内必带，不然我知道是哪个展会吗？？？？？
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    assert res['resultCode'] == "SUCCESS"


def test_information_list(login_01):
    '''资讯列表'''
    url = host + '/api/v2/information/page'
    data = {
        "pageSize": 10,
        "pageNum": 1,
        "keyword": "",
        "statusType": "ALL"
    }
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    assert res['resultCode'] == "SUCCESS"



def test_add_org(login_01):
    '''主办新增参展方,组织名称和邮箱不能重复'''
    url = host + '/api/v2/auth/organization?'
    data ={"userId":"10018012021040900016179586793474216359140581632",
           "tenantId":"10014032021013100016120583168790000000000328375",
           "organizationName":"小方新增企业名称"+get_randomInt(),
           "accountNum":"169765213457"+get_randomInt()+"@qq.com",
           "groupTagList":[{"tagId":"32","tagName":"{\"en-us\": \"Foreign Enterprise\", \"zh-cn\": \"国外企业\"}","isOwner":True},{"tagId":"33","tagName":"{\"en-us\": \"High Value\", \"zh-cn\": \"高价值\"}","isOwner":True}],"roleType":"SPONSOR","sendMsgFlag":True,"extParam":{"contactName":"小方","contactMobile":"17816104031","contactEmail":"1697652134@qq.com","industry":"20002","district":"[\"156\",\"110000\",\"110100\"]"}}
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    assert res['resultCode'] == "SUCCESS"


def test_org_list(login_01):
    '''参展方列表'''
    url = host + '/api/v2/auth/organization/page'
    data = {
        "pageSize": 10,
        "pageNum": 1,
        "tenantId": "10014032021013100016120583168790000000000328375"
    }
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    assert res['resultCode'] == "SUCCESS"


def certificate_Type_list(login_01):
    '''证件----种类列表'''
    url = host + '/api/v2/certificateType/config/selectCertificateType'
    data = None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-exhibition-id': exhibitionId,  # 展会内必带，不然我知道是哪个展会呢
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    assert res['resultCode'] == "SUCCESS"
    leng=len(res['resultInfo'])
    rand_index=random.randint(0,leng)
    # global rand_cer_type_id
    rand_cer_type_id=res['resultInfo'][rand_index]['certificateTypeId']
    return rand_cer_type_id

# @pytest.mark.skip
#门票类型不支持
def test_createCertificate_default(login_01):
    rand_cer_type_id=certificate_Type_list(login_01)
    '''主办新增证件---系统默认----证件种类随机选择'''
    url = host + '/api/v2/certificateStore/config/createCertificateStore'
    data ={"certificateStoreName":"{\"zh-cn\":\"小房新增证件----系统默认66\"}",
           "certificateTypeId":rand_cer_type_id,"applyStartTime":"2021-10-31",
           "applyEndTime":"2021-11-30","makeRealFlag":0,"printPhotoFlag":0,"coreFlag":0,
           "healthCodeFlag":0,"verifyActivationFlag":1,"nucleicReportFlag":0,"certificateStoreId":None,
           "validityStartTime":"2021-10-31","validityEndTime":"2021-11-30",
           "defaultStoreFlag":1,"stockTotal":1000,"stockId":None,
           "verificationMethod":"[\"ELECTRONIC_CODE\",\"FACE_SCAN\",\"ID_CARD\"]","passCode":False}

    #更改门票字段名称
    certificateStoreName={"zh-cn":"小方证件-默认"+get_randomInt(),"en-us":"zhengjian"+get_randomInt()}
    data['certificateStoreName']=str(certificateStoreName)
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,  # 展会内必带，不然我知道是哪个展会呢
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    assert res['resultCode'] == "SUCCESS"

@pytest.mark.skip
def test_createCertificate_codeRule(login_01):
    '''主办新增证件---编码规则'''
    url = host + '/api/v2/certificateStore/config/createCertificateStore'
    data ={"certificateStoreName":"{\"zh-cn\":\"小房新增证件----有编码77\"}","certificateTypeId":"1395326708109099009",
           "applyStartTime":"2021-10-31","applyEndTime":"2021-11-30",
           "makeRealFlag":0,"printPhotoFlag":0,"coreFlag":0,"healthCodeFlag":0,
           "verifyActivationFlag":1,"nucleicReportFlag":0,"certificateStoreId":None,
           "validityStartTime":"2021-10-31","validityEndTime":"2021-11-30","defaultStoreFlag":1,
           "stockTotal":100,"stockId":None,"verificationMethod":"[\"ELECTRONIC_CODE\",\"ID_CARD\",\"FACE_SCAN\"]",
           "passCode":True,"throughRule":{"prefix":"jihho","seqInit":"200"}}
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,  # 展会内必带，不然我知道是哪个展会呢
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    assert res['resultCode'] == "SYSTEM_EXCEPTION"


def test_certificate_list(login_01):
    '''证件列表'''
    url = host + '/api/v2/certificateStore/config/queryCertificatePage?'
    data = {
        "pageSize": 10,
        "pageNum": 1,
        "certificateStoreName":"publishState",
        "tenantId": "10014032021013100016120583168790000000000328375"
    }
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-exhibition-id': exhibitionId,  # 展会内必带，不然我知道是哪个展会呢
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    assert res['resultCode'] == "SUCCESS"




# @pytest.mark.skip
def test_add_tickets(login_01):
    '''主办新增门票,门票名称'''
    url = host + '/api/v2/goods/tickets?'
    data ={
	"exhibitionId": "10015032021013100016120640620470000000000271269",
	"tenantId": "10014032021013100016120583168790000000000328375",
	# "goodsId": "100119002021121300016393640509055179249824649395",
	"goodsName": "{\"zh-cn\":\"1212门票1222\"}",
	"stockTotal": 100,
	"sellTotal": 2,
	"stockRemain": None,
	"stockRemainWithoutPreDeduct": None,
	"feeConfig": "FREE",
	"goodsPrice": None,
	"sellStartTime": "2021-12-13",
	"sellEndTime": "2021-12-31",
	"admissionTimes": [{
		"startDate": "2022-01-01",
		"endDate": "2022-01-02",
		"startTime": "00:00",
		"endTime": "07:00"
	}],
	"verifyConfig": "NON_VERIFY",
	"formId": "",
	"ticketRights": "{}",
	"maxBuyCount": 10,
	"ticketStatus": "",
	"stockId": "10015172021121300016393640509064128234096506534",
	"verificationMethod": "[\"ELECTRONIC_CODE\"]",
	"ticketChannelInfoList": [{
		"channelId": "100118022021113000016382375368676690243662969880",
		"tenantId": "10014032021013100016120583168790000000000328375",
		"exhibitionId": "10015032021013100016120640620470000000000271269",
		"channelName": "王敬的渠道",
		"headPicture": "https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021013100016120640620470000000000271269/ad/20211130101423700_r24zt6ky.jpeg",
		"channelType": "COMMON",
		"channelOwnerName": None,
		"channelOwnerId": None,
		"channelOwnerIds": None,
		"promotionLinkId": None,
		"mark": "",
		"relationTicketCount": 0,
		"totalSaleCount": 0,
		"totalSaleIncome": 0,
		"isSelected": None,
		"ticketId": None,
		"showStatus": None,
		"saleStatus": None,
		"relationId": None
	}],
	"isSpecifyChannel": 1,
	"headPicture": "https://digital-prod-8.oss-cn-hangzhou.aliyuncs.com/admin/defaultHeadPicture.png",
	"channelIdList": ["100118022021113000016382375368676690243662969880"]
}

    #更改门票字段名称
    goodName={"zh-cn":"小方新增门票-免费-3种"+get_randomInt(),"en-us":"xfmenpiao"+get_randomInt()}
    data['goodsName']=str(goodName)
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("新增门票成功啦~")
    assert res['resultCode'] == "SUCCESS"

@pytest.mark.skip
def test_edit_tickets(login_01):
    '''主办编辑门票'''
    url = host + '/api/v2/goods/tickets'
    data={"exhibitionId":"10015032021013100016120640620470000000000271269","tenantId":"10014032021013100016120583168790000000000328375","goodsId":"100119002021111800016372167258169644982456163946","goodsName":"{\"zh-cn\":\"付费门票10.29付费门票10.29付费门票10.29付费门\"}","stockTotal":5,"sellTotal":1,"stockRemain":None,"stockRemainWithoutPreDeduct":None,"feeConfig":"FREE","goodsPrice":None,"sellStartTime":"2021-11-18","sellEndTime":"2021-12-10","admissionTimes":[{"startDate":"2021-11-29","endDate":"2021-12-15","startTime":"00:23","endTime":"08:00"}],"verifyConfig":"VERIFY","formId":"100115012021102900016354930098183405272282322699","ticketRights":"{}","maxBuyCount":99,"ticketStatus":"OFFLINE","stockId":"10015172021111800016372167258173707902077716847","verificationMethod":"[\"FACE_SCAN_AND_ID_CARD\"]","ticketChannelInfoList":[{"channelId":"100118022021112900016381585888177628345725123845","tenantId":"10014032021013100016120583168790000000000328375","exhibitionId":"10015032021013100016120640620470000000000271269","channelName":"官方默认渠道","headPicture":None,"channelType":"OFFICIAL","channelOwnerName":None,"channelOwnerId":None,"channelOwnerIds":None,"promotionLinkId":None,"mark":None,"relationTicketCount":0,"totalSaleCount":0,"totalSaleIncome":0,"isSelected":None,"ticketId":None,"showStatus":None,"saleStatus":None,"relationId":None}],"isSpecifyChannel":0,"headPicture":"https://digital-test-8.oss-cn-hangzhou.aliyuncs.com/expo/10015032021013100016120640620470000000000271269/ad/20211129141751997_wje969v6.jpeg"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'Content-Type': 'application/json',
        'x-ca-exhibition-id':exhibitionId

    }
    # req = Run_Main(url, data, headers, 'POST')
    # res = req.request_post_json(url, data, headers)
    res=requests.put(url=url,json=data,headers=headers,verify=False).json()
    logging.info("编辑门票成功啦~")
    assert res['resultCode'] == "SUCCESS"


# @pytest.mark.skip
def test_ticket_list(login_01):
    '''门票列表+按照门票名称搜素'''
    url = host + '/api/v2/goods/tickets/page?pageNum=1&pageSize=10&goodsName=%E5%B0%8F%E6%96%B9'
    data=None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    setattr(getticket,'ticket',res['resultInfo']['records'][0]['goodsId'])
    logging.info(getattr(getticket,'ticket'))
    logging.info("门票---搜索成功啦~")
    assert res['resultCode'] == "SUCCESS"


def test_ticket_detail(login_01):
    '''门票详情'''
    url = host + '/api/v2/goods/tickets/100119002021112900016381714031798999779253867898'
    data=None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("门票---查看详情成功啦~")
    assert res['resultCode'] == "SUCCESS"



# @pytest.mark.skip
def test_ticket_publish(login_01):
    '''门票上架'''
    test_ticket_list(login_01)
    url = host + '/api/v2/goods/tickets/updateTicketStatus'
    data = {"goodsId":getattr(getticket,'ticket'),
        "ticketStatus": "PUBLISHED"
        }
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票---上架成功啦~")
    assert res['resultCode'] == "SUCCESS"

# @pytest.mark.skip
def test_ticket_soldout(login_01):
    '''门票手动售罄'''
    # test_ticket_list(login_01)
    url = host + '/api/v2/goods/tickets/updateTicketStatus'
    data = {"goodsId":getattr(getticket,'ticket'),
            "ticketStatus":"SOLD_OUT_MANUALLY"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票---手动售罄成功啦~")
    assert res['resultCode'] == "SUCCESS"



@pytest.mark.skip
def test_ticket_offline(login_01):
    '''门票下架'''
    test_ticket_publish(login_01)
    url = host + '/api/v2/goods/tickets/updateTicketStatus'
    data = {"goodsId":getattr(getticket,'ticket'),
            "ticketStatus":"OFFLINE"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票---下架成功啦~")
    assert res['resultCode'] == "SUCCESS"

# @pytest.mark.skip
def test_ticket_delete(login_01):
    '''门票删除'''
    # test_add_tickets(login_01)
    test_ticket_publish(login_01)
    test_ticket_soldout(login_01)
    test_ticket_offline(login_01)
    url = host + "/api/v2/goods/tickets/"+getattr(getticket,'ticket')
    data = {}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
        'Content-Type': 'application/json'
    }
    res=requests.delete(url=url,data=data,headers=headers,verify=False).json()
    #不要忘了要转成dict格式，并且不要校验ssl证书
    logging.info("门票---删除成功啦~")
    assert res['resultCode'] == "SUCCESS"




##########此处票券设置
def test_ticket_formList(login_01):
    '''门票表单--列表查看'''
    url = host + '/api/v2/dynamicForm/pageByFormType'
    data={"newFormTypeCodeList":["TICKET_REAL_NAME_FORM","TICKET_NON_REAL_NAME_FORM"],"pageNum":1,"pageSize":10}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票表单---列表查看成功啦~")
    assert res['errMsg'] == "success"

def test_ticket_formList_all(login_01):
    '''门票表单--全部表单列表查看'''
    url = host + '/api/v2/dataItem/list?itemLabel='
    data=None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("门票表单---全部表单列表查看成功啦~")
    assert res['resultCode'] == "SUCCESS"


def test_ticket_form_detail(login_01):
    '''门票表单--详情查看'''
    # test_ticket_formList(login_01)
    # test_ticket_formList_all(login_01)
    url = host + '/api/v2/dynamicForm/100115012021062800016248790861403116565817788464'
    data=None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    # setattr(getticket,'ticket',res['resultInfo']['records'][0]['goodsId'])
    # logging.info(getattr(getticket,'ticket'))
    logging.info("门票表单---详情查看成功啦~")
    assert res['resultCode'] == "SUCCESS"




############此处开始门票订单列表拉
def test_orderCenter_list(login_01):
    '''门票订单订单---列表'''
    url = host + '/api/v2/orderCenter/page'
    data={"orderType":"TICKET","ownerType":"SPONSOR","pageNum":1,"pageSize":10}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票订单订单---列表查看成功啦~")
    assert res['resultCode'] == "SUCCESS"

def test_orderCenter_detail(login_01):
    '''门票订单---详情'''
    url = host + '/api/v2/orderCenter/detail'
    data={"orderId":"1001300032021112600016378956574872315439973942768"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票订单---详情查看成功啦~")
    assert res['resultCode'] == "SUCCESS"


def test_orderCenter_verify(login_01):
    '''门票订单---导出验证'''
    # test_orderCenter_detail(login_01)
    # test_orderCenter_list(login_01)
    url = host + '/api/v2/message/verify/verification'
    data={"account":"229250457@qq.com","codeType":"EXPORT_TICKETS_VERIFY_CODE","code":"888888"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id':exhibitionId,
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    logging.info("门票订单---导出验证成功啦~")
    assert res['resultCode'] == "SUCCESS"

##########票券管理列表
def test_ticket_useList(login_01):
    '''票券管理列表'''
    url = host + '/api/v2/ticket/page?pageNum=1&pageSize=10&ticketState='
    data = None
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("票券管理列表---列表信息获取成功~")
    assert res['resultCode'] == "SUCCESS"


def test_ticket_use_count(login_01):
    '''票券管理列表---总数计算'''
    url = host + '/api/v2/ticket/count?ticketState='
    data = None
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("票券管理列表---总数计算成功~")
    assert res['resultCode'] == "SUCCESS"

def test_account_enterprise(login_01):
    '''票券管理列表---企业账号获取'''
    url = host + '/api/v2/user/enterprise/account'
    data = None
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId,
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("票券管理列表---企业账号获取信息获取成功~")
    assert res['resultCode'] == "SUCCESS"


@pytest.mark.skip
#请补充
def test_ticket_usedetail(login_01):
    '''票券管理列表---用票人和购票人信息获取'''
    # test_ticket_use_count(login_01)
    # test_ticket_useList(login_01)
    # test_account_enterprise(login_01)
    url = host + '/api/v2/ticket/detail/100118002021112200016375699110965260987713251318'
    data = None
    headers = {
        'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId,
        'x-ca-exhibition-id': exhibitionId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info("票券管理列表---用票人和购票人信息获取成功~")
    assert res['resultCode'] == "SUCCESS"





def test_menusList_qiye(login_01):
    url = host + '/api/v2/organization/menu/menuList?'
    data = {"insideExhibition":"false"}
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    assert res['resultCode'] == "SUCCESS"


def test_userInfo(login_01):
    url = host + '/api/v2/user/info'
    data = None
    headers = {
         'Authorization': token,
        'x-access-lang': 'zh-cn',
        'x-ca-tenant-id': tenantId
    }
    req = Run_Main(url, data, headers, 'GET')
    res = req.request_get(url, data, headers)
    logging.info(res)
    assert res['resultCode']=="SUCCESS"

if __name__ == '__main__':
    pytest.main("-s","-v")