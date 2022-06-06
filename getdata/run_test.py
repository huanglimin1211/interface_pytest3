#coding= utf-8
import os,sys,json
from time import  sleep
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASE)
from src.interface_get  import Run_Main
from getdata.get_data import GetData
from util.commom_util import Common_Util
from util.connect_db import   ConnectDB
from util.smtp_email import Send_Email
from getdata.depend_data import DenpendData

host = 'https://pch5test8.digitalexpo.com'

class RunTest(object):
	def __init__(self,filepath,index):
		# self.runmethod=Run_Main(url,json,headers,method)
		self.data = GetData(filepath,index)
		self.commom_util=Common_Util()
		# self.db=ConnectDB()

	def login_in_H5(self):
			host = 'https://pch5test8.digitalexpo.com'
			url = host + '/api/v2/app/login?'
			data = {"account":17816109999,
					  "tenantId":"10014032021013100016120583168790000000000328375",
					  "verifyCode":"888888",
					  "userPassword":"59406454EA450777AD40F6516A2D19BF",
					  "loginType":"VERIFY_CODE","terminalType":"H5"}
			headers = {
				'Content-Type': 'application/json'
			}
			req = Run_Main(url, data, headers, 'POST')
			res = req.request_post_json(url, data, headers)
			return res['resultInfo']['authorization']

		
	def run_test(self):	
		pass_list=[]
		fail_list=[]	
		
		token = self.login_in_H5()
		cases=self.data.get_case_lines()
		for i in range(2,cases):
			sleep(1)
			isrun=self.data.get_isrun(i)
			# host='https://qdtest7.digitalexpo.com/'
			url=host+self.data.get_url_value(i)
			method=self.data.get_runmethod(i)
			expect_string=self.data.get_expect_value(i)
			get_modelName=self.data.get_modelName(i)
			#根据json的key找到value
			json = self.data.get_data_forjson()
			res = self.data.get_request_data(3)
			data = json[res]
			print(type(data))
			# print(expect_string)
			# expect_data=self.db.search_one(expect)
			# expect_string0=expect_data.__str__()#将tuple类型转换为str类型
			# expect_string=expect_string0.split("'",1)[1].split("'",1)[0]
			# print(expect_string0)
			headers = {
				    "x-ca-tenant-id": "10014032021013100016120583168790000000000328375",
				    "x-ca-exhibition-id": "10015032021013100016120640620470000000000271269",
				    "x-ca-brand-id":"10014022021013100016120583171440000000000326917",
				    'authorization': token
        	} 
			#print("data的数据为：%s"  %data)
			# is_denpend=self.data.get_is_denpend(i)
			# if is_denpend !=None:
			# 	self.denpend_data=DenpendData(is_denpend)
			# 	denpend_response_data=self.denpend_data.get_data_for_key(i)
			# 	denpend_key=self.data.get_denpend_field(i)
			# 	data[denpend_key]=denpend_response_data



			sleep(1)
			if isrun=="yes":
				print("****************现在执行的用例是： "+get_modelName)
				req=Run_Main(url,data,headers,method)
				res=req.request_post_json(url,data,headers)
				# res=req.run_main(url,data,headers,method)
				# res = json.dumps(res, indent=2)
				print(type(res))
				# res = json.dumps(res)  #报错dict没有dumps
				result=self.commom_util.is_contain(str(expect_string),str(res))
				if result==True:
					self.data.write_value(i,"pass")
					pass_list.append(i)
					print("*****************"+get_modelName+"  用例执行通过")
				else:
					self.data.write_value(i,"fail")
					fail_list.append(i)
					print("*****************"+get_modelName+"  用例执行失败，不通过！")
			else:
				pass

		pass_num=len(pass_list)
		fail_num=len(fail_list)
		total_num=pass_num+fail_num
		pass_result="%.2f%%"   %(pass_num/total_num*100)
		fail_result="%.2f%%"   %(fail_num/total_num*100)
		content="测试通过的用例个数为%s，失败的个数为%s，通过率%s，失败率%s"  %(pass_num,fail_num,pass_result,fail_result)
		print(content)
		# mail_url=os.path.abspath("../report/2020-05-23Test.html")
		# mail=Send_Email(mail_url,content)
		# mail.send_email()
		

if __name__ == '__main__':
	filepath=os.path.abspath('../data/case_test_H5.xls')
	run=RunTest(filepath,0)
	res=run.run_test()

