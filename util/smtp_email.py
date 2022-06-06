#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
# from  data.read_config    import *
import os,time
import configparser
from time  import sleep


# config_path="D:\\CESHI66666666666666666666666\\11AUTOTEST\\GXV3370_lmhuang\\inter\\data\\data.ini"
# cf=configparser.ConfigParser()
# cf.read(config_path)
# smtpserver=cf.get('email','smtpserver')
# username=cf.get('email', 'username')
# password=cf.get('email','password')
# sender=cf.get('email', 'sender')
# receiver=cf.get('email', 'receiver')

# rd=Read_Config(config_path)
# print(smtpserver)
# print(username)
# print(receiver)


smtpserver='smtp.qq.com'
username='1697652134'
password='qhisdsxfhxnheahi'#报错535，原因是第3方登录时，密码这要需填成授权码
sender='1697652134@qq.com'
receiver='1697652134@qq.com'#接收者list会报错，list没有encode属性
print(type(smtpserver))


class Send_Email(object):
    """docstring for Send_Email"""
    def __init__(self,url,content):
        self.url=url
        self.content=content
        
    def send_email(self):       
        textApart=MIMEText(self.content)

        # imageFile=os.path.abspath('./data/1.jpg')
        # imageApart=MIMEApplication(open(imageFile,'rb').read())
        # imageApart.add_header('Content-Disposition','attachment',filename=imageFile)

        htmlFile=self.url
        htmlApart=MIMEApplication(open(htmlFile,'rb').read())
        htmlApart.add_header('Content-Disposition','attachment',filename=htmlFile)

        msg=MIMEMultipart()
        msg.attach(textApart)
        msg.attach(htmlApart)
        # msg.attach(imageApart)
        msg['Subject']='黄丽敏_接口_自动化测试报告66'
        try:
            smtp=smtplib.SMTP()
            smtp.connect(smtpserver)
            smtp.login(username,password)
            smtp.sendmail(sender,receiver,msg.as_string())
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败")


if __name__ == '__main__':
    content="hello,my name is lmhuang"
    now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now_time)
    url=os.path.abspath("../report/2019-08-09Test.html")
    # url=
    print(url)
    mail=Send_Email(url,content)
    mail.send_email()





