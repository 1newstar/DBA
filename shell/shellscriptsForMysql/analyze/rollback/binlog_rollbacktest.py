#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__='Booboo Wei'
__write_time__='2017-08-23'

# 加载模块，其中MySQLdb需要另外安装
import sys
import re
import time
import datetime
import MySQLdb
import os

# 连接mysql需要的变量
url='localhost'
username='root'
password='(Uploo00king)'
dbname='uplooking'

# 设定正则表达式
r=re.compile('INSERT|DELETE|UPDATE|BEGIN|COMMIT')
n=re.compile('#')
flag=re.compile('.*flags.*')
thread=re.compile('.*thread_id.*')
xid=re.compile('.*Xid.*')
insert=re.compile('INSERT')
delete=re.compile('DELETE')
update=re.compile('UPDATE')
begin=re.compile('BEGIN')
commit=re.compile('COMMIT')
e=re.compile('@.*=')
w=re.compile('WHERE')
s=re.compile('SET')


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
		self.query("DROP TABLE IF EXISTS binlogrollback")
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
                delete_list=[]
                where_list=['WHERE ']
                u_len_num=len(self.i)
		tb_str=self.i[0].split()[-1]
                s_index=1
                for i_num in range(0,u_len_num):
                        if i_num < s_index:
				i_str_new='DELETE FROM '+tb_str.strip()+' '
				delete_list.append(i_str_new)
                        if i_num > s_index and i_num < u_len_num-1:
                                i_str_new=self.i[i_num].strip()+' and '
                                where_list.append(i_str_new)
                        if i_num == u_len_num-1:
                                i_str_new=self.i[i_num].strip()+';'
                                where_list.append(i_str_new)
                for where_str in where_list:
                        delete_list.append(where_str)
		return delete_list
	

	def delete_syntax(self):
	# delete语法调整
		insert_list=[]
                set_list=['SET ']
                u_len_num=len(self.i)
                w_index=1
		tb_str=self.i[0].split()[-1]
                for i_num in range(0,u_len_num):
                        if i_num < w_index:
                                i_str_new='INSERT INTO '+tb_str.strip()+' '
                                insert_list.append(i_str_new)
                        if i_num > w_index and i_num < u_len_num-1:
                                i_str_new=self.i[i_num].strip()+','
                                set_list.append(i_str_new)
                        if i_num == u_len_num-1:
                                i_str_new=self.i[i_num].strip()+';'
                                set_list.append(i_str_new)
                for set_str in set_list:
                        insert_list.append(set_str)
                return insert_list


	def update_syntax(self):
	# update语法调整
                update_list=[]
                where_list=['where ']
                set_list=['set ']
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
                        if i_num > w_index and i_num < s_index-1:
                                i_str_new=self.i[i_num].strip('')+','
                                set_list.append(i_str_new)
                        if i_num == s_index-1:
                                i_str_new=self.i[i_num].strip()+' '
                                set_list.append(i_str_new)
                        if i_num > s_index and i_num < u_len_num-1:	
                                i_str_new=self.i[i_num].strip()+' and '
                                where_list.append(i_str_new)
                        if i_num == u_len_num-1:
                                i_str_new=self.i[i_num].strip('')+';'
                                where_list.append(i_str_new)
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
				if e.match(u.strip()):
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
	# 将b_list存入数据到binlogrollback表中
	# insert into binlogrollback values (null,'170731', '12:09:18',254,'insert','insert into sdfsdf  set a=1');
	col1='null'
	col2=b[0].split()[0]
	col3=b[0].split()[1]
	col4=b[1]
	col5=b[2]
	# new event
	col6_pre=b[3]
	col6=col6_pre.replace('"','\\\"')
	col7=s
	sql="insert into binlogrollback values (" + col1 + ",'" + col2 + "','" + col3 + "'," + col4 + ",'" + col5 + "','" + col6 + '''',"''' + col7 + '''");'''
	p2 = mysqlhelper(url,username,password,dbname )
        p2.insert(sql)
	p2.commit()
	p2.close()		
		
#0 通过位置参数读取需要分析的binlog文件
filename = sys.argv[1]
spos_str=raw_input( 'plz input start_postion:')
epos_str=raw_input('plz input end_postion:' )
#ml_str = "mysqlbinlog -vv --base64-output=DECODE-ROWS "+ filename + " | awk  '$0~/^###/ || $0~/end_log_pos/ || $0~/BEGIN/ || $0~/COMMIT/ {print $0}' |sed 's/^### //;s@\/\*.*\*\/@@'"
ml_str = "mysqlbinlog -vv --base64-output=DECODE-ROWS --start-position="+ spos_str +' --stop-position=' + epos_str + ' '  + filename + " | awk  '$0~/^###/ || $0~/end_log_pos/ || $0~/BEGIN/ || $0~/COMMIT/ {print $0}' |sed 's/^### //;s@\/\*.*\*\/@@'"
a_list = os.popen(ml_str).readlines()


#1 将binlog文本中的每一条sql分别保存在不同的列表中，例如第一条sql存放于b_list1=[时间，pos，event,sql类型，sql语句]

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
		# new event
		event_num=e_num+18
		# new event
		event_str=a_str[event_num:]
                names['b_list%d'%num].append(time_str)
                names['b_list%d'%num].append(pos_str)
                names['b_list%d'%num].append(event_str.strip())
		if not flag.match(a_str.strip()) and not thread.match(a_str.strip()) and not xid.match(a_str.strip()):
			sql_type_str='others'
         		names['b_list%d'%num].append(sql_type_str)

        if r.match(a_str):
		if begin.match(a_str):
			sql_type_str='begin'
		elif commit.match(a_str):
			sql_type_str='commit'
                elif insert.match(a_str):
                        sql_type_str='insert'
                elif delete.match(a_str):
                        sql_type_str='delete'
                elif update.match(a_str):
                        sql_type_str='update'
	
         	names['b_list%d'%num].append(sql_type_str)
                names['b_list%d'%num].append(a_str)

        if not r.match(a_str) and not n.match(a_str):
                names['b_list%d'%num].append(a_str)


#2 将b_list1~b_listN存入数据库中【时间,pos,type,sql】
#2.1 连接数据库创建表binlogrollback

sql='create table binlogrollback (id int primary key auto_increment,edate date not null,etime time not null,pos int not null,event text not null,type varchar(20) not null,sqlinfo text not null) charset utf8;'
p = mysqlhelper(url,username,password,dbname )
p.createtable(sql)
p.close()



#2.2 插入记录
for j in range(1,num+1):
	a1=names['b_list%d'%j]
	if len(a1) < 4:
		names['b_list%d'%j].append('others')
    	if names['b_list%d'%j][3]=='insert':
		p1=row_format(names['b_list%d'%j][4:])
		sql_list=p1.insert_syntax()
		a2=p1.change_col(sql_list)
	elif names['b_list%d'%j][3]=='delete':
		p1=row_format(names['b_list%d'%j][4:])
		sql_list=p1.delete_syntax()
		a2=p1.change_col(sql_list)	
	elif names['b_list%d'%j][3]=='update':
		p1=row_format(names['b_list%d'%j][4:])
		sql_list=p1.update_syntax()
		a2=p1.change_col(sql_list)
	elif names['b_list%d'%j][3]=='begin':
                a2='commit;'
	elif names['b_list%d'%j][3].strip()=='commit':
		a2='begin;'
	else:
		a2='others'
	execute_insert(a1,a2.replace('"','\\\"'))



# 3 确定时间点后，生成回滚语句'
print '============================================输出回滚语句==========================================================='
sql="select sqlinfo from binlogrollback where sqlinfo !='others' and pos between "+ spos_str +' and ' + epos_str + ' order by id desc;'
#sql = "select sqlinfo from binlogrollback where sqlinfo !='others' order by id desc;"
p = mysqlhelper(url,username,password,dbname )
result_tuple = p.queryAll(sql)
for i in result_tuple:
	print i[0]
p.close()

print "==========================================END========================================================================="
