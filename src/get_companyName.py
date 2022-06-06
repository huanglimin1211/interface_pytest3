import requests,os
from bs4 import BeautifulSoup
from lxml import etree
from xlwt import Workbook
from util.operate_excel import OperateExcel
import re
import json
from time import sleep

class BtcSpider(object):
    def __init__(self):
        self.base_url = 'http://m.54114.cn/hangzhou/hangye1_p5/'
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'}
        self.news_name = []
        self.news_url = []

    # 1,发请求：
    def get_response(self, url):
        response = requests.get(url, headers = self.headers).text
        # print(response)
        return response

    # 2,解析数据：
    def parse_data(self, data):
        # 1,转类型; 使用xpath解析网页
        company_name_list = []
        html_etree= etree.HTML(data)
        for i in range(1,21):
            company_name = html_etree.xpath('/html/body/div[3]/div[3]/ul/li['+str(i)+']/a/text()')
            if company_name:
                # print("这是字符串形式：", company_name[0],i)
                # print("这是数组形式：", company_name,i)
                company_name_list.append(company_name[0])
        # print(company_name_list)
        return company_name_list


# /html/body/div[3]/div[3]/ul/li[1]/a
# /html/body/div[3]/div[3]/ul/li[20]
if __name__ == '__main__':
    # url="http://m.54114.cn/changzhou/"
    # citys=getList_city_name(url)
    # print(citys)
    def getList_city_name(url='http://m.54114.cn/changzhou/'):
        city_list = []
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        dl_data = soup.find_all("dd")
        for dlitem in dl_data:
            # print(dlitem.a["href"])
            city_list.append(dlitem.a["href"])
        # print(city_list)
        return city_list

    def get_company(city):
        company_name_list=[]
        for j in range(1, 16):
            # url='http://m.54114.cn/hangzhou/hangye1_p5/'
            print("这是第" + str(j) + "页哦~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            url = 'http://m.54114.cn'+city+'hangye1' + str(j) + '/'
            try:
                bt = BtcSpider()
                res = bt.get_response(url)
                company_name_data = bt.parse_data(res)
                company_name_list.append(company_name_data)
            except:
                print("请稍后重试")
        # print(company_name_list)
        return company_name_list



    def write_data(yuansu):
        filepath = os.path.abspath("../data/company.xls")  # 表格关闭才可以
        operate = OperateExcel(filepath, 0)
        length = len(yuansu)
        # 把返回值列表写入exlce某一列中
        for M in range(length):
            try:
                operate.write_data(M, 0, yuansu[M])
            except:
                print("写入文件失败")
        print("写入完毕~~~~~~~~~~~~~~~")


    def write_excel(yuansu):
        # 创建一个工作簿
        w = Workbook()
        # 创建一个工作表
        ws = w.add_sheet('1')
        length = len(yuansu)
        for M in range(length):
            try:
                ws.write(M, 0, yuansu[M])
            except:
                print("写入文件失败")
        print("写入完毕~~~~~~~~~~~~~~~")
        print("总共生成: %s条数据" %length)
        w.save('write_company.xls')

    url="http://m.54114.cn/changzhou/"
    citys=getList_city_name(url)
    company_total=[]
    for city in citys:
        company_list = get_company(city)
        company_total.append(company_list)
    print("这里是所有公司哦%s" %company_total)

    yuansu = []
    def bianli(lists):
        for i in lists:
            sleep(0.01)
            if type(i) != list:
                yuansu.append(i)
            else:
                bianli(i)
        # print("元素是 %s" %yuansu)
    bianli(company_total)
    leng=len(yuansu)
    print("这里是所有公司的长度%s" %leng)
    write_excel(yuansu)