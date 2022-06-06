import os,time
import configparser


# #获取文件的当前路径（绝对路径）
# cur_path=os.path.dirname(os.path.realpath(__file__))
# #获取config.ini的路径
# config_path=os.path.join(cur_path,'data.ini')
# config_path="D:\\CESHI66666666666666666666666\\11AUTOTEST\\GXV3370_lmhuang\\inter\\data\\data.ini"

cf=configparser.ConfigParser()
cf.read("D:\\CESHI66666666666666666666666\\11AUTOTEST\\GXV3370_lmhuang\\inter\\data\\data.ini")
# sections=cf.sections()
# print(sections)
# for sec in sections:
#     options=cf.options(sec)
#     print(options)

# for sec in sections:
#     for op in(cf.options(sec)):
#         print("%s" %(op))

smtpserver=cf.get('email','smtpserver')
username=cf.get('email', 'username')
password=cf.get('email','password')
sender=cf.get('email', 'sender')
receiver=cf.get('email', 'receiver')




# class Read_Config():
#     def __init__(self,path):
#         self.path=path
#         cf=configparser.ConfigParser()
#         cf.read(self.path)
#         self.smtpserver=cf.get('email','smtpserver')
#         self.username=cf.get('email', 'username')
#         self.password=cf.get('email','password')
#         self.sender=cf.get('email', 'sender')
#         self.receiver=cf.get('email', 'receiver')
        

# rd=Read_Config(config_path)
# smtpserver=rd.smtpserver
# username=rd.username
# password=rd.password
# sender=rd.sender
# receiver=rd.receiver






# if __name__ == '__main__':
#    url=""
#    mail=Send_Email(url)
#    mail.send_email()
