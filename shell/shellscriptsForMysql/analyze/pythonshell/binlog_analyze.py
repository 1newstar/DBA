#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
该脚本的功能如下：
1. 获取日志中的所有DML语句及时间位置
2. 进行DML语法修正
3. 转换时间戳为日期时间
4. 最终将转换后的SQL语句保存在数据库，表名mysqltobinlog

脚本使用方法：
1. bash b2s_pre.sh binlogfile 进行日志预处理，该脚本返回binlogfile.new文件
2. python binlog_analyze.py binlogfile.new  该脚本将binlog转换为sql并保存于数据库中
3. python foo.py  该脚本进行sql语句的分析，例如统计某个时段的sql类型占比

待改进：
1. 目前一次只能分析一个脚本，第二次分析会覆盖mysqltobinlog表
2. 分析的内容比较简单
3. sql回滚未实现

example:
# cp /var/lib/mysql-log/mastera.000028 .
# bash b2s_pre.sh mastera.000028 
# python binlog_analyze.py mastera.000028.new 
# python foo.py
该日志记录的时间段为：2017-07-20 2017-07-18 
某时段统计sql类型
Plz input t1:2017-07-18
Plz input t2:2017-07-20
2017-07-18~2017-07-20时间段内的不同SQL类型执行的数量为：
update 268 
insert 255 
delete 27 
2017-07-18~2017-07-20时间段内不同类型的sql所占比重：
update 0.4873 
insert 0.4636 
delete 0.0491
'''


__author__='Booboo Wei'
__write_time__='2017-08-01'

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

# 设定正则表达式
r=re.compile('INSERT|DELETE|UPDATE')
n=re.compile('#')
insert=re.compile('INSERT')
delete=re.compile('DELETE')
update=re.compile('UPDATE')
e=re.compile('@.*=')
w=re.compile('WHERE')
s=re.compile('SET')

# 通过位置参数读取需要分析的binlog文件
a_file=open(sys.argv[1],'ro')
a_list=a_file.readlines()

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
		
		
		
class row_format:
	def __init__(self,i):
	# 初始化函数
		self.i=i
	
	def insert_syntax(self):
	# insert语法调整
		insert_list=[]
		for i_str in self.i:
			if e.match(i_str.strip()):
				i_str_new=i_str.strip()+','
			else:
				i_str_new=i_str.strip()+' '
			insert_list.append(i_str_new)
	
		insert_list[-1]=insert_list[-1].replace(',',';')
		return insert_list
	
	def delete_syntax(self):
	# delete语法调整
		delete_list=[]

		for i_str in self.i:
			if e.match(i_str.strip()):
				i_str_new=i_str.strip()+' and '
			else:
				i_str_new=i_str.strip()+' '
			delete_list.append(i_str_new)

		delete_list[-1]=delete_list[-1].replace('and',';')
		return delete_list

	def update_syntax(self):
	# update语法调整
		update_list=[]
		where_list=[]
		set_list=[]
		u_len_num=len(self.i)
		for i_num in range(0,u_len_num):

			if w.match(self.i[i_num].strip()):
				w_index=i_num
			if s.match(self.i[i_num].strip()):
				s_index=i_num
		for i_num in range(0,u_len_num):
			if i_num < w_index:
				i_str_new=self.i[i_num].strip()+' '	
				update_list.append(i_str_new)
			if i_num == w_index:
				i_str_new=self.i[i_num].strip()+' '	
				where_list.append(i_str_new)
			if i_num > w_index and i_num < s_index-1:
				i_str_new=self.i[i_num].strip()+' and '
				where_list.append(i_str_new)
			if i_num == s_index-1:
				i_str_new=self.i[i_num].strip()+';'
				where_list.append(i_str_new)
			if i_num > s_index and i_num < u_len_num-1:
				i_str_new=self.i[i_num].strip()+','
				set_list.append(i_str_new)
			if i_num == s_index:
				i_str_new=self.i[i_num].strip()+' '
				set_list.append(i_str_new)
			if i_num == u_len_num-1:
				i_str_new=self.i[i_num].strip()+' '
				set_list.append(i_str_new)

		for set_str in set_list:
			update_list.append(set_str)
		for where_str in where_list:
			update_list.append(where_str)
			
		return update_list	
	
	def change_col(self,sql_list):
	# 转换@为对应的列名
	# 转换时间戳为日期
		self.sql_list=sql_list
		# 设定list分别存储表的列名，数据类型，数据类型为时间戳的列名
		tb_col_list=[]
		tb_col_type_list=[]
		timestamp_list=[]
		
		# 获取表名
		tb_str=self.sql_list[0].split()[-1]
		dbname=tb_str.split('.')[0].strip('`')
		tbname=tb_str.split('.')[1].strip('`')
		
		# 连接数据库获取列名
		sql='desc ' + tbname + ';'
		p=mysqlhelper(url,username,password,dbname)
		data = p.queryAll(sql)

		for v in data:
			tb_col_list.append(v[0])
			tb_col_type_list.append(v[1])
		p.close()
		
		# 字典保存列和类型
		tb_col_dict=dict(zip(tb_col_list,tb_col_type_list))

		# 获取列类型为timestamp的列存入timestamp_list中
		for key in tb_col_dict:
			if tb_col_dict[key]=='timestamp':
				timestamp_list.append(key)
					
		
		# 转换@为列名
		col_len_num=len(tb_col_list)
		for j in range(1,col_len_num+1):
			for u in self.sql_list:
				if e.match(u):
					u_new=u.replace('@'+str(j)+'=',tb_col_list[j-1]+'=')
					# 将unix_timestamp进行转换
					for k in timestamp_list:
						time_re=re.compile('^'+k)
						if time_re.match(u_new):
							if 'and' in u_new:
				               			_u_new_value=u_new.split('=')[1]
								u_new_value=_u_new_value.split()[0]
                            				else:
								u_new_value=u_new.split('=')[1][:-1]
							
							# python时间函数进行时间戳的转换
							t1=time.localtime(int(u_new_value))
							t2="'"+time.strftime("%Y-%m-%d %H:%M:%S",t1)+"'"
							u_new=u_new.replace(u_new_value,t2)
					num22=self.sql_list.index(u)
					self.sql_list[num22]=u_new
		isql_str = ' '.join(self.sql_list)
		return isql_str
	
def execute_insert(b,s):
	# 将b_list存入数据到binlogtosql表中
	# insert into binlogtosql values (null,'170731', '12:09:18',254,'insert','insert into sdfsdf  set a=1');
	col1='null'
	col2=b[0].split()[0]
	col3=b[0].split()[1]
	col4=b[1]
	col5=b[2]
	col6=s
	sql="insert into binlogtosql values (" + col1 + ",'" + col2 + "','" + col3 + "'," + col4 + ",'" + col5 + '''',"''' + col6 + '''");'''
	p2 = mysqlhelper(url,username,password,dbname )
        p2.insert(sql)
	p2.commit()
	p2.close()		
		

#1 将binlog文本中的每一条sql分别保存在不同的列表中，例如第一条sql存放于b_list1=[时间，pos，sql类型，sql语句]
num=0
names=locals()
for a_str in a_list:
        if n.match(a_str):
                num=num+1
                names['b_list%d'%num]=[]
                time_str=a_str[1:16]
                s_num=a_str.index('end_log_pos')+11
                e_num=a_str.index('CRC')
                pos_str=a_str[s_num:e_num]
                names['b_list%d'%num].append(time_str)
                names['b_list%d'%num].append(pos_str)

        if r.match(a_str):
                if insert.match(a_str):
                        sql_type_str='insert'
                if delete.match(a_str):
                        sql_type_str='delete'
                if update.match(a_str):
                        sql_type_str='update'
                names['b_list%d'%num].append(sql_type_str)
                names['b_list%d'%num].append(a_str)

        if not r.match(a_str) and not n.match(a_str):
                names['b_list%d'%num].append(a_str)
		
	

#2 将b_list1~b_listN存入数据库中【时间,pos,type,sql】
#2.1 连接数据库创建表binlogtosql

sql='create table binlogtosql (id int primary key auto_increment,edate date not null,etime time not null,pos int not null,type varchar(20) not null,sqlinfo text not null);'
p = mysqlhelper(url,username,password,dbname )
p.createtable(sql)
p.close()


#2.2 插入记录
for j in range(1,num+1):
	a1=names['b_list%d'%j]
    	if names['b_list%d'%j][2]=='insert':
		p1=row_format(names['b_list%d'%j][3:])
		sql_list=p1.insert_syntax()
		a2=p1.change_col(sql_list)
	elif names['b_list%d'%j][2]=='delete':
		p1=row_format(names['b_list%d'%j][3:])
		sql_list=p1.delete_syntax()
		a2=p1.change_col(sql_list)	
	else:
		p1=row_format(names['b_list%d'%j][3:])
		sql_list=p1.update_syntax()
		a2=p1.change_col(sql_list)
	execute_insert(a1,a2.replace('"','\\\"'))

