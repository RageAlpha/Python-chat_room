from pymysql import connect
from config import *


class data_base(object):
    """建立数据库以及基本信息查询"""
    def __init__(self):
        self.con = connect(host=DB_HOST,
                           port=DB_PORT,
                           database=DB_NAME,
                           user=DB_USER,
                           password=DB_PASS,
                           )
        self.cursor = self.con.cursor()

    def close(self):
        # 释放数据库资源
        self.cursor.close()
        self.con.close()

    def get_user(self,sql):
        self.cursor.execute(sql)


        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        fileds = [filed[0] for filed in self.cursor.description]

        return_data = {}

        for filed, value in zip(fileds, query_result):
            return_data[filed] = value

        return return_data


if __name__ == "__main__":
    db = data_base()
    data = db.get_user("select * from users WHERE user_name = 'user2'")
    print(data)
    db.close()

