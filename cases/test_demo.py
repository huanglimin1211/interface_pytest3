from functools import  reduce
import time,pytest,sys,os
from seleniumwire import webdriver
# dr = webdriver.Chrome()



#os和sys的区别，os一般是获取文件的路径，sys是获取
def test():
    #当前文件名
    print(__file__)
    #当前文件的路径名和文件名
    print(os.path.dirname(__file__))
    print(os.path.basename(__file__))
    #当前的文件的绝对路径
    print(os.path.abspath(__file__))

    #命令行参数
    print(sys.argv)
    print(sys.path)




def test_01():
    time.sleep(2)
    dr.get("https://iwhale.digitalexpo.com/admin/user/login")
    time.sleep(2)
    dr.find_element_by_xpath("//*[@id='verifyCode']").send_keys("189326")
    time.sleep(2)
    dr.find_element_by_xpath("//*[@id='mobileNumber']").send_keys("17716108888")
    time.sleep(2)
    dr.find_element_by_xpath("//*[@id='root']/div/div[2]/div[2]/div[2]/div[2]/form/div[4]/div/div/div/button").click()
    time.sleep(2)
    # Access requests via the `requests` attribute
    for request in dr.requests:
        try:
            if request.response and "Authorization" in request.headers:
                print(request.headers["Authorization"])
        except:
            print("没有找到token")
    dr.close()



#
# # 已知一个队列,如： [1, 3, 5, 7], 如何把第一个数字，放到第三个位置，得到： [3, 5, 1, 7]
# a=[1,3,5,7]
# a.insert(3,a[0])  # L.insert(index,obj)
# print(a[1:])
#
# # 统计在一个队列中的数字，有多少个正数，多少个负数，如[1, 3, 5, 7, 0, -1,-9, -4, -5, 8]
# l3=[1, 3, 5, 7, 0, -1,-9, -4, -5, 8]
# l4=[i for i in l3 if i >0]
# print("整数多少个 %s" %(len(l4)))
#
#
#
# 字符串切片
# 字符串 "axbyczdj"，如果得到结果“abcd”
str1="axbyczdj"
print(str1[0::2])#也可以简写成print(str1[::2])

#
#
# # 字符串切割
# # 已知一个字符串为“hello_world_yoyo”, 如何得到一个队列 ["hello","world","yoyo"]
# str="hello_world_yoyo"
# l=str.split("_")
# print(l)
#
#
# # 已知一个队列[1, 3, 6, 9, 7, 3, 4, 6]
# # 按从大大小排序
# # 去除重复数字
# l2=[1, 3, 6, 9, 7, 3, 4, 6]
# l2.sort(reverse=True)
# print(list(set(l2)))
#
#
#
# # 计算 n!,例如 n=3(计算 321=6)， 求 10!
# # 方法 1：可以用 python 里面的 reduce 函数，reduce() 函数会对参数序列中元素进行累积。
# n=3
# a1=reduce(lambda x,y:x*y,range(1,n+1))
# print(a1)
#
# #利用递归
# def fact(n):
#     if n==1:
#         return 1
#     else:
#         return n*fact(n-1)
#
# number=int(input('请输入一个正整数：'))
# result=fact(number)
# print("阶乘结果 %s",%result)
#
#
# # li = [10,8,4,7,5],进行冒泡排序，大的往后排
# li=[10,8,4,7,5]
# for i in range(len(li)):
#     for j in range(len(li)-i-1):
#         if li[j]>li[j+1]:
#             li[j],li[j+1]=li[j+1],li[j]
#             print(li)


