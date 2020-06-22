#encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: Mysql.py
@Time: 2019/3/19 19:37
Mysql连接事务类
"""
import pymysql
import traceback

class Mysqldb:

    mysql_ip = '127.0.0.1'
    mysql_user = 'root'
    mysql_pass = 'root'
    mysql_dbname = ''
    db = ''
    cursor = ''

    def __init__(self, db_name):
        print('[o] Mysql模块初始化中...')
        self.mysql_dbname = db_name
        try:
            self.db = pymysql.connect(self.mysql_ip, self.mysql_user, self.mysql_pass, self.mysql_dbname)
            self.cursor = self.db.cursor()
            print('[+] 数据库连接成功')
        except Exception:
            print('[x] 数据连接出错')

    # 数据库的增删改查封装操作：

    def mysql_update(self, tb_name, content_name, content, condition):
        if condition == '':
            condition = '1=1'
        try:
            sql = 'Update {0} set {2}={3} where'.format(tb_name, content_name, content, condition)
            print(sql)
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
        except Exception:
            print('[x] 数据库删除异常')
            traceback.print_exc()

    def mysql_insert(self, tb_name, val_name, val_str):
        try:
            sql = 'Insert into {0}({1}) values(\'{2}\')'.format(tb_name, val_name ,val_str)
            print(sql)
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
        except Exception:
            print('[x] 数据库插入异常')
            #traceback.print_exc()

    def mysql_select(self, tb_name, content_name, condition, limit):
        if condition == '':
            condition = '1=1'
        try:
            sql = 'Select {0} from {1} where {2} {3}'.format(content_name, tb_name, condition, limit)
            print(sql)
            self.cursor.execute(sql)
            return self.cursor
        except Exception:
            print('[x] 数据库查询异常')
            traceback.print_exc()
            return ''

    def mysql_delete(self, tb_name, condition):
        try:
            sql = 'Delete From {0} where {1}'.format(tb_name, condition)
            print(sql)
            self.cursor.execute(sql)
        except Exception:
            print('[x] 数据库删除异常')
            traceback.print_exc()


    def mysql_diy(self, sentence):
        cursor = self.db.cursor()
        try:
            sql = sentence
            print(sql)
            cursor.execute(sql)
            return cursor
        except Exception:
            print('[x] 数据库语句执行异常')
            traceback.print_exc()
            return ''


    # 获取URL列表
    def mysql_get_url(self, cursor):
        try:
            urls = cursor.fetchall()
            urllist = []
            for i in urls:
                urllist.append(str(i)[2:-3])
            return urllist
        except Exception:
            print('[x] 获取URL异常')
            return ''
