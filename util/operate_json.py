import json
import os

class OperateJson(object):
	"""docstring for OperateJson"""
	def __init__(self,filepath=None):
		if filepath:
			self.filepath=filepath
		else:
			self.filepath='../data/userTest.json'

	def get_json(self):
		with open(self.filepath,'r',encoding='utf-8')  as f:
			res=json.load(f)#load,从字符串类型转变成Python数据类型dict
			print(type(res))
			return res

	def get_data(self,search):
		self.res=self.get_json()
		print(self.res)
		data=self.res[search]
		print(data)
		return data


if __name__ == '__main__':
	filepath=os.path.abspath("../data/H5.json")
	operate=OperateJson(filepath)
	operate.get_data("headers")


	




