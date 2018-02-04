# -*- coding: utf-8 -*-
import MySQLdb
from prettytable import from_db_cursor #以表格的方式打印mysql执行结果

__author__ = 'Booboo Wei'
__write_time__ = '2017-08-01'

# 定义MySQLdb连接和操作的类
class mysqlhelper():
    def __init__(self,url,port,username,password,dbname,charset="utf8"):
        self.url=url
        self.port=port
        self.username=username
        self.password=password
        self.dbname=dbname
        self.charset=charset
        try:
            self.conn=MySQLdb.connect(self.url,self.username,self.password,self.dbname,self.port)
            self.conn.set_character_set(self.charset)
            self.cur=self.conn.cursor()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


    def print_table(self,sql):
        """
        类似在mysql终端执行命令的结果输出，以表格形式
        :return str
        """
        self.cur.execute(sql)
        pt = from_db_cursor(self.cur)
        return pt

    def col_query(self, sql):
        '''
        打印表的列名
        :return list
        '''
        self.cur.execute(sql)
        index = self.cur.description
        result = []
        for res in self.cur.fetchall():
            row = {}
            for i in range(len(index)):
                row[index[i][0]] = res[i]
            result.append(row)
        return result

    def query(self,sql):
        try:
            n=self.cur.execute(sql)
            return n
        except MySQLdb.Error as e:
            print("Mysql Error:%s\nSQL:%s" %(e,sql))

    def queryRow(self,sql):
        """
        :param sql:string
        :return: result:tuple
        """
        self.query(sql)
        result = self.cur.fetchone()
        return result
  


    def queryAll_dict(self,sql):
        """
        :param sql:string
        :return: result:dict
        """
        self.query(sql)
        result=self.cur.fetchall()
        return dict(result)

    def human(self,bytes):
        bytes = float(bytes)
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.0fT' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.0fG' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.0fM' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.0fK' % kilobytes
        else:
            size = '%.0fb' % bytes
        return size

    def commit(self):
        self.conn.commit()
  
    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    print 'this is a mudule for mysqlcon named mysqlhelper()'
    #url, port, username, password, dbname = ("", 3306, 'python', '', 'db1')
    #conn = MySQLdb.connect(url, username, password, dbname, port)
    #conn.set_character_set('utf8')
    #cur=conn.cursor()
