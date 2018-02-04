#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__='Booboo Wei'

# 加载模块，其中MySQLdb需要另外安装
import sys
import re
import time
import datetime
import MySQLdb

# 连接mysql需要的变量
url='localhost'
username='root'
password='(Uploo00king)'
dbname='uplooking'
# 定义MySQLdb连接和操作的类
class mysqlhelper:
        def __init__(self,url,username,password,dbname,charset="utf8"):
                self.url=url
                self.username=username
                self.password=password
                self.dbname=dbname
                self.charset=charset
                try:
                        self.conn=MySQLdb.connect(self.url,self.username,self.password,self.dbname)
                        self.conn.set_character_set(self.charset)
                        self.cur=self.conn.cursor()
                except MySQLdb.Error as e:
                        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

        def query(self,sql):
                try:
                        n=self.cur.execute(sql)
                        return n
                except MySQLdb.Error as e:
                        print("Mysql Error:%s\nSQL:%s" %(e,sql))

        def queryRow(self,sql):
                self.query(sql)
                result = self.cur.fetchone()
                return result

        def queryAll(self,sql):
                self.query(sql)
                result=self.cur.fetchall()
                return result

        def createtable(self,sql):
                self.query("DROP TABLE IF EXISTS binlogtosql")
                self.query(sql)

        def insert(self,sql):
                self.query(sql)

        def commit(self):
                self.conn.commit()

        def close(self):
                self.cur.close()
                self.conn.close()




def binlog_time():
        sys.stdout.write("该日志记录的时间段为：")
        mysqldb=mysqlhelper(url,username,password,dbname)
        data=mysqldb.queryAll('select max(edate),min(edate) from binlogtosql order by edate;')
	for i in data:
		for j in i:
			sys.stdout.write(j.isoformat()+' ')
		print
	mysqldb.close()

def binlog_sql_type():
	'''统计某个时间段的SQL类型，从大到小排列
	统计不同类型的sql所占比重'''
	t1=raw_input('Plz input t1:')
	t2=raw_input('Plz input t2:')
	print(t1+'~'+t2+"时间段内的不同SQL类型执行的数量为：")
        mysqldb=mysqlhelper(url,username,password,dbname)
	sql="select type,count(id) from binlogtosql where edate >='"+ t1 +"' and "+ "edate <= '" + t2 + "'  group by type order by count(id) desc;"
# select type,count(id) from binlogtosql where edate >= '2017-07-19' and edate <= '2017-07-19' group by type order by count(id) desc;
        data=mysqldb.queryAll(sql)
        for i in data:
                for j in i:
                        sys.stdout.write(str(j)+' ')
                print
	print(t1+'~'+t2+"时间段内不同类型的sql所占比重：")
	sql='''select * from 
	(
		(
			select t2.type,t2.c/t1.c insert_p from 
				(select count(id) c from binlogtosql where edate>='{0}' and edate<='{1}') t1 , 
				(select type,count(id) c from binlogtosql where edate>='{0}' and edate<='{1}' and type='insert') t2
		)	 
		union 
		(
			select t2.type,t2.c/t1.c insert_p from 
				(select count(id) c from binlogtosql where edate>='{0}' and edate<='{1}') t1 , 
				(select type,count(id) c from binlogtosql where edate>='{0}' and edate<='{1}' and type='delete') t2
		)
 
		union 
		(
			select t2.type,t2.c/t1.c insert_p from 
				(select count(id) c from binlogtosql where edate>='{0}' and edate<='{1}') t1 , 
				(select type,count(id) c from binlogtosql where edate>='{0}' and edate<='{1}' and type='update') t2
		)
	) t3 
	order by insert_p desc;'''.format(t1,t2)
	
	data=mysqldb.queryAll(sql)
	for i in data:
		for j in i:
			sys.stdout.write(str(j)+' ')
		print
	mysqldb.close()
	
 
binlog_time()
print "某时段统计sql类型"
binlog_sql_type()	




