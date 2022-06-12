#coding=utf-8
import  pymysql
dbconf = {"host": 'rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com',
          "user": 'digital_expo_8_test',
          "password": '0Cu68bc^3RM1Kp*F5cl0qOZRYCLfcy',
          "database": 'digital_expo_test8'}

class  ConnectDB():
    def __init__(self,dbinfo=dbconf):#给定默认值，哈哈哈真不错
        # dbinfo=('rm-bp1foe402p295lpmu7o.mysql.rds.aliyuncs.com','digital_expo_8_test','0Cu68bc^3RM1Kp*F5cl0qOZRYCLfcy','digital_expo_test8')
        self.con=pymysql.connect(**dbinfo)
        self.cursor=self.con.cursor()


    def select(self,sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data


    def excute_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except:
            self.con.rollback()


    def close_db(self):
        self.con.close()


if __name__ == '__main__':
    db1=ConnectDB()
    sql=r'SELECT * FROM  expo_core_information WHERE ' \
    ' exhibition_id = "10015032021013100016120640620470000000000271269" ' \
    'AND title LIKE "%测试%" AND publish_status = "PUBLISHED" ' \
    'AND is_delete = 0 AND language_type IN ("ALL", "zh-cn")'
    data=db1.select(sql)
    print(data)
    print(type(data))
    db1.close_db()

