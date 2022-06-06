#coding=utf-8
import  pymysql

class  ConnectDB():
    def __init__(self):
        #测试环境
        self.con=pymysql.connect('rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com','digital_expo_8_test','0Cu68bc^3RM1Kp*F5cl0qOZRYCLfcy','digital_expo_test8')
        #开发环境
        # self.con = pymysql.connect('rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com', 'digital_expo_8_dev','K^bd1TLvcTq7dd@^UvgyRg6HH474Dh', 'digital_expo_dev8')
        self.cursor = self.con.cursor()


    def search_one(self,sql):
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            return row
        # data=self.cursor.fetchone()
        # return data
    def search_all(self,sql):
        self.cursor.execute(sql)
        data=self.cursor.fetchall()#获取出来的是元组
        data=list(data)
        return data

    def search_all_datalist(self,sql):
        l=[]
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            l.append(list(row))
        return l

    def close_db(self):
        self.con.close()


if __name__ == '__main__':
    db1=ConnectDB()
    sql='SELECT * FROM 	expo_core_information WHERE exhibition_id = "10015032021013100016120640620470000000000271269" AND title LIKE "%测试%" AND publish_status = "PUBLISHED" AND is_delete = 0 AND language_type IN ("ALL", "zh-cn")'
    data=db1.search_all_datalist(sql)
    # print("数据库返回结果为 %s"  %data)
    print(data)
    print(len(data))
    print(data[0][4])
    db1.close_db()
