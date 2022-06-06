#coding=utf-8
import xlrd
import os
from xlutils.copy import copy
class OperateExcel(object):
	def __init__(self, filepath,index):
		self.filepath=filepath
		self.index=index
		self.data=self.get_data()
	# def __init__(self, filepath=None,index=None):
	# 	# if filepath:
	# 	# 	self.filepath=filepath
	# 	# 	self.index=index
	# 	# else:
	# 	# 	self.filepath="./data/case1.xls"
	# 	# 	self.index=0
	# 	self.data=self.get_data()
	def get_data(self):	
		book=xlrd.open_workbook(self.filepath)
		print(book.sheet_names())
		sheet=book.sheet_by_index(self.index)
		return sheet
	def get_lines(self):
		nrows=self.data.nrows
		print(nrows)
		return nrows
	def get_cell_value(self,row,col):#先行后列，从0开始
		value=self.data.cell(row,col).value
		print(value)
		return value

	def write_data(self,row,col,value):
		read_data=xlrd.open_workbook(self.filepath)
		write_data=copy(read_data)
		sheet=write_data.get_sheet(0)
		sheet.write(row,col,value)
		write_data.save(self.filepath)



	#获取某一列的内容：
	def get_cols_data(self,col_id=None):
		if col_id!=None:
			col_data=self.data.col_values(col_id)
		else:
			col_data=self.data.col_values(0)
		return col_data	

	#根据对应caseid找到对应行的行号
	def  get_row_num(self,case_id):
		num=0
		col_datas=self.get_cols_data()
		for col_data in col_datas:
			if str(case_id) in col_data:
				print(num)
				return num
			num=num+1
		

	#根据行号，找到行的内容
	def get_row_values(self,row):
		sheet=self.data
		row_data=sheet.row_values(row)
		return row_data
	
	#根据对应的caseid找到对应行的内容
	def get_row_data(self,case_id):
		row_num=self.get_row_num(case_id)
		data=self.get_row_values(row_num)
		print(data)
		return data


	#1204--excel获取接口数据，获取所有行的内容
	def read_excel(self):
		ll=[]
		for i in range(1,self.get_lines()):
			ll.append(self.get_row_values(i))
		return ll



if __name__ == '__main__':
	filepath=os.path.abspath("../data/case_test_yunzhan_web.xls")#表格关闭才可以
	operate=OperateExcel(filepath,0)
	operate.get_data()
	operate.get_lines()
	operate.get_cell_value(2,2)
	operate.write_data(2,3,'no')
	operate.get_cell_value(2,2)

	operate.get_row_num('Imooc-05')
	operate.get_row_data('Imooc-05')









