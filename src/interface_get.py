#coding=utf-8
import requests
import json,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告

class Run_Main():
    def __init__(self,url,json,headers,method):
        # self.res=self.run_main(url,json,headers,method)
        pass
    
              
    def request_post_json(self,url,json,headers):    
        res=requests.post(url=url,json=json,headers=headers,verify=False).json()
        # res_json=json.dumps(res,sort_keys=True,indent=4)
        # print(res_json)
        return res

    def request_post_data(self,url,data,headers):    
        res=requests.post(url=url,data=data,headers=headers,verify=False).json()
        res=json.dumps(res,sort_keys=True,indent=4)
        # print(res)
        return res

    def request_get(self,url,json,headers):
        res=requests.get(url=url,params=json,headers=headers,verify=False).json()
        # res_json=json.dumps(res,sort_keys=True,indent=4)
        # print(res_json)
        return res


    def run_main(self,url,json,headers,method):
        if method=='POST':
            return self.request_post_json(url,json,headers)
        if method=='GET':
            return self.request_get(url,json,headers)

class Request_Get():
    """docstring for request_get"""
    def __init__(self, url,headers):
        self.url=url
        self.headers=headers
        
    def interface_get(self):
        self.res=requests.get(self.url,self.headers)
        self.text=self.res.text
        print(self.text)
        print(str(self.res.status_code)+'*************')#print要放在return之前
        return self.res


class Request_Post():
    def __init__(self, url,headers,data=None):
        self.data=data
        self.url = url
        self.headers = headers


    def interface_post(self):#headers一定要放在data之前，也不知道为啥
        self.res = requests.post(url=self.url,headers=self.headers,json=self.data,verify=False).json()
        return self.res


if __name__ == '__main__':
    host = 'https://qdtest8.digitalexpo.com/'
    url = host + '/api/v1/auth/sys/login'
    data = {"mobileNumber": "17816104037", "verifyCode": "888888", "loginType": "VERIFY_CODE", "mobileAreaCode": 86,
            "enterpriseLevel": "EXHIBITOR"}
    headers = {
        # 'Content-Type': 'application/json'
    }
    req = Run_Main(url, data, headers, 'POST')
    res = req.request_post_json(url, data, headers)
    print(res)



    




