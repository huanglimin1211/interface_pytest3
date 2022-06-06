#coding=utf-8
import  pymysql

class  ConnectDB():
    def __init__(self):
        self.con=pymysql.connect('rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com','digital_expo_8_test','0Cu68bc^3RM1Kp*F5cl0qOZRYCLfcy','digital_expo_test8')
        # self.con=pymysql.connect('rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com','digital_expo_8_dev','K^bd1TLvcTq7dd@^UvgyRg6HH474Dh','digital_expo_dev8')
        self.cursor=self.con.cursor()


    def select(self,sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data


    def excute_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        # data = self.cursor.fetchone()
        # return data

    def close_db(self):
        self.con.close()


if __name__ == '__main__':
    db1=ConnectDB()
    #SELECT COUNT(*) from  expo_core_exhibitor where exhibitor_name like '%测试展商%'
    sql='SELECT * FROM  expo_core_information WHERE  exhibition_id = "10015032021013100016120640620470000000000271269" AND title LIKE "%测试%" AND publish_status = "PUBLISHED" AND is_delete = 0 AND language_type IN ("ALL", "zh-cn")'
    data=db1.select(sql)
    # data=db1.select("SELECT COUNT(*) from  expo_core_exhibitor where exhibitor_name like '%测试展商%'")
    # print("数据库返回结果为 %s"   %data)
    print(type(data))
    print(data)
    db1.close_db()

