# coing=utf-8
import csv  # 导入scv库，可以读取csv文件
from selenium import webdriver
import os,sys,pytest,os,random,requests,json,allure,xlrd
from selenium.webdriver.common.keys import Keys
# import unittest
from time import  sleep
dr = webdriver.Chrome()


@pytest.fixture()
def login_web():
    sleep(2)
    dr.get("https://jieroutest.digitalexpo.com/admin/user/login")
    sleep(2)
    dr.maximize_window()
    local_login='//input[@id="mobileNumber"]'
    local_CODE='//input[@id="verifyCode"]'
    local_login_btn='//button[@class="ant-btn ant-btn-primary ant-btn-round ant-btn-lg ant-btn-block loginButton___2yDBq"]'
    dr.find_element_by_xpath(local_login).send_keys("17816101111")
    sleep(1)
    dr.find_element_by_xpath(local_CODE).send_keys("888888")
    sleep(1)
    dr.find_element_by_xpath(local_login_btn).click()
    sleep(1)
    local_select_org='//input[@id="bizProfileId"]'
    dr.find_element_by_xpath(local_select_org).click()
    sleep(1)
    dr.find_element_by_xpath('//div[@title="中华人民共和国商务部（MOFCOM）测试"]').click()
    sleep(1)
    dr.find_element_by_xpath('//span[contains(text(),"确 定")]').click()
    sleep(2)

    #切换展会
    # dr.execute_script("document.documentElement.scrollTop=2000)")
    dr.execute_script("window.scrollTo(1600,16000)")
    sleep(1)
    dr.execute_script("window.scrollTo(1600,16000)")
    sleep(1)
    dr.execute_script("window.scrollTo(1600,16000)")
    sleep(1)
    dr.find_element_by_xpath('//div[@class="ant-card ant-card-bordered ant-card-hoverable card___2B6cg "]').click()
    sleep(2)






def test_pianhao_set(login_web):
    '''在web自动化测试中，测试工程师经常会碰到frame表单嵌套结构，直接定位会报错，我们需要切换表单后才能成功定位。

        我拿QQ邮箱登录来作为例子说下frame怎么切换。'''
    dr.get("https://jieroutest.digitalexpo.com/admin/audiencepreference?insideExhibition=true")
    sleep(1)
    dr.find_element_by_xpath('//span[contains(text(),"选择类目")]').click()
    sleep(1)
    dr.find_element_by_xpath('//span[@title="三星"]').click()
    sleep(1)
    dr.find_element_by_xpath('//span[contains(text(),"确 定")]').click()
    sleep(1)

def test_tag_set(login_web):
    '''在web自动化测试中，测试工程师经常会碰到frame表单嵌套结构，直接定位会报错，我们需要切换表单后才能成功定位。

        我拿QQ邮箱登录来作为例子说下frame怎么切换。'''
    sleep(3)
    dr.get("https://jieroutest.digitalexpo.com/admin/content/exhibit?insideExhibition=true")
    sleep(1)
    dr.execute_script("window.scrollTo(1600,0)")
    sleep(1)
    dr.find_element_by_xpath('//a[contains(text(),"贴标签")]').click()
    sleep(1)
    dr.find_element_by_xpath('//input[@class="ant-checkbox-input"]').click()
    sleep(1)
    dr.execute_script("window.scrollTo(0,1600)")
    sleep(1)
    dr.find_element_by_xpath('//span[contains(text(),"确 定")]').click()
    sleep(1)
    dr.close()



#
# if __name__ == '__main__':
#     pytest.main('-s', '-v', '--alluredir', '../result')
#     sleep(2)
#     os.system("allure generate ../result/ -o ../report/ --clean")


