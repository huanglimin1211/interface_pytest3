#coding=utf-8
import  os,sys,json
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASE)
from util.operate_excel import OperateExcel
from src.interface_get import Run_Main
from getdata.get_data import GetData
from jsonpath_rw import  parse,jsonpath

class DenpendData(object):

    def __init__(self,case_id):
        filepath=os.path.abspath("./data_config/case_product.xls")#表格关闭才可以
        self.operate_excel=OperateExcel(filepath,0)
        self.data=GetData(filepath,0)
        self.case_id=case_id
    
    def get_case_line_data(self):
        row_data=self.operate_excel.get_row_data(self.case_id)
        return row_data

    def login(self):
        url = 'https://www.hzzhdj.cn/hzdj-party-admin/index/login'
        data= {"userAdm":"SXB1","userPwd":"by7HgG0sJU/tfnmMeNDyehs92jeWiAJwakwN9k5F4bDvILw19IdXvjWR8s3b6ZohTVXUUahtAr2WN4mtDG7z27oCJuda/Ungsab97USGqr9mz9deQ+q8EtJCzKRTkyUX2lW0EMs/sGBQoxstPXzAbh63F9m8vv2avX/U4ugHeeU=","userLoginChannel":"web"}
        headers = {
			'Content-Type':'application/json'
		}
        req=Run_Main(url,data,headers,'POST')
        res=req.request_post_json(url,data,headers)
        return  res['datas']['Authorization']

    #根据carse_id执行依赖的接口所返回的结果
    def run_denpend(self):
        row_num=self.operate_excel.get_row_num(self.case_id)
        request_data1=self.data.get_request_data(row_num)
        data=json.loads(request_data1)
        method=self.data.get_runmethod(row_num)
        url=self.data.get_url_value(row_num)
        token=self.login()
        headers = {  
                'Content-Type':'application/json',
                'Authorization':token
        } 
        req=Run_Main(url,data,headers,method)
        res=req.request_post_json(url,data,headers)
        # res = json.dumps(res, indent=2)#看看什么时候可以
        return res


    def get_data_for_key(self,row):
        denpend_data=self.data.get_denpend_key(row)
        res_data=self.run_denpend()
        json_exe=parse(denpend_data)
        madle=json_exe.find(res_data)
        print(len([math.value for math in madle]))
        return [math.value for math in madle][0]




