#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__='Booboo Wei'
__write_time__='2017-08-01'

# 加载模块，其中MySQLdb需要另外安装
import sys
import re
import time
import datetime
import MySQLdb
import os

# 连接mysql需要的变量
#url='localhost'
#username='root'
#password='(Uploo00king)'
#dbname='uplooking'


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
		
if __name__ == '__main__':
	print 'this is a mudule for mysqlcon named mysqlhelper()'
		

