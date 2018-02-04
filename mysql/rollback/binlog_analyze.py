#!/usr/bin/python
# -*- coding: utf-8 -*-

# Usage: python xxx.py 文件名-------------------------------------------------------------------------------------#
# #日志文件需要提前准备 											  #
# mysqlbinlog -vv --base64-output=DECODE-ROWS mastera.000028 > /root/mybinlog.txt 				  #	
# # 截取所有sql带时间点和pos											  #
# awk  '$0~/^###/ || $0~/end_log_pos.*flags/ {print $0}' mybinlog.txt | sed 's/^### //;s@\/\*.*\*\/@@' > new      #
#-----------------------------------------------------------------------------------------------------------------#
import sys
import re
import MySQLdb

url='localhost'
username='root'
password='(Uploo00king)'

sql_list=['INSERT','UPDATE','DELETE']

r=re.compile('INSERT|DELETE|UPDATE')
n=re.compile('#')
insert=re.compile('INSERT')
delete=re.compile('DELETE')
update=re.compile('UPDATE')
e=re.compile('@.*=')
w=re.compile('WHERE')
s=re.compile('SET')
a_file=open(sys.argv[1],'ro')
a_list=a_file.readlines()


def insert_row_format(i,url,username,password):
	insert_list=[]
	for i_str in i:
		if e.match(i_str.strip()):
			i_str_new=i_str.strip()+','
		else:
			i_str_new=i_str.strip()+' '
		insert_list.append(i_str_new)

	insert_list[-1]=insert_list[-1].replace(',',';')	 
	# 获取表名
	tb_col_list=[]
	tb_str=i[0].split()[2]
	dbname=tb_str.split('.')[0].strip('`')
	tbname=tb_str.split('.')[1].strip('`')
	# 连接数据库获取列名
	sql='desc ' + tbname + ';'
	db = MySQLdb.connect(url,username,password,dbname )
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()

	for i in data:
                tb_col_list.append(i[0])
	db.close()

	col_len_num=len(tb_col_list)
	for j in range(1,col_len_num+1):
		for u in insert_list:
			if e.match(u):
				u_new=u.replace('@'+str(j)+'=',tb_col_list[j-1]+'=')
				num22=insert_list.index(u)
				insert_list[num22]=u_new


	for aa in insert_list:
		sys.stdout.write(aa)
	print

def delete_row_format(i,url,username,password):
	delete_list=[]
	for i_str in i:
		if e.match(i_str.strip()):
			i_str_new=i_str.strip()+' and '
		else:
			i_str_new=i_str.strip()+' '
		delete_list.append(i_str_new)

	delete_list[-1]=delete_list[-1].replace('and',';')	 
	# 获取表名
	tb_col_list=[]
	tb_str=i[0].split()[2]
	dbname=tb_str.split('.')[0].strip('`')
	tbname=tb_str.split('.')[1].strip('`')
	# 连接数据库获取列名
	sql='desc ' + tbname + ';'
	db = MySQLdb.connect(url,username,password,dbname )
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()

	for i in data:
                tb_col_list.append(i[0])
	db.close()

	col_len_num=len(tb_col_list)
	for j in range(1,col_len_num+1):
		for u in delete_list:
			if e.match(u):
				u_new=u.replace('@'+str(j)+'=',tb_col_list[j-1]+'=')
				num22=delete_list.index(u)
				delete_list[num22]=u_new


	for aa in delete_list:
		sys.stdout.write(aa)
	print
	
def update_row_format(i,url,username,password):
	update_list=[]
	where_list=[]
	set_list=[]
	u_len_num=len(i)
	for i_num in range(0,u_len_num):

		if w.match(i[i_num].strip()):
			w_index=i_num
		if s.match(i[i_num].strip()):
			s_index=i_num
	for i_num in range(0,u_len_num):
		if i_num < w_index:
			i_str_new=i[i_num].strip()+' '	
			update_list.append(i_str_new)
		if i_num == w_index:
			i_str_new=i[i_num].strip()+' '	
			where_list.append(i_str_new)
		if i_num > w_index and i_num < s_index-1:
			i_str_new=i[i_num].strip()+' and '
			where_list.append(i_str_new)
		if i_num == s_index-1:
			i_str_new=i[i_num].strip()+';'
			where_list.append(i_str_new)
		if i_num > s_index and i_num < u_len_num-1:
			i_str_new=i[i_num].strip()+','
			set_list.append(i_str_new)
		if i_num == s_index:
			i_str_new=i[i_num].strip()+' '
			set_list.append(i_str_new)
		if i_num == u_len_num-1:
			i_str_new=i[i_num].strip()+' '
			set_list.append(i_str_new)

	for set_str in set_list:
		update_list.append(set_str)
	for where_str in where_list:
		update_list.append(where_str)
	# 获取表名
	tb_col_list=[]
	tb_str=i[0].split()[1]
	dbname=tb_str.split('.')[0].strip('`')
	tbname=tb_str.split('.')[1].strip('`')
	# 连接数据库获取列名
	sql='desc ' + tbname + ';'
	db = MySQLdb.connect(url,username,password,dbname )
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()

	for i in data:
                tb_col_list.append(i[0])
	db.close()

	col_len_num=len(tb_col_list)
	for j in range(1,col_len_num+1):
		for u in update_list:
			if e.match(u):
				u_new=u.replace('@'+str(j)+'=',tb_col_list[j-1]+'=')
				num22=update_list.index(u)
				update_list[num22]=u_new


	for aa in update_list:
		sys.stdout.write(aa)
	print

num=0
names=locals()
for a_str in a_list:
	if n.match(a_str):
		num=num+1
		names['b_list%d'%num]=[]	
		time_str=a_str[1:16]
		pos_str=a_str[41:46]
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
		
	

# 打印出时间点 位置编号 sql语句
print "时间点\t\t位置编号\tSQL类型\tSQL语句"
print "-------------------------------------------------------"
for j in range(1,num+1):
	sys.stdout.write('{0}\t{1}\t\t{2}\t'.format(names['b_list%d'%j][0],names['b_list%d'%j][1],names['b_list%d'%j][2]))

	if names['b_list%d'%j][2]=='insert':
		insert_row_format(names['b_list%d'%j][3:],url,username,password)
	elif names['b_list%d'%j][2]=='delete':
		delete_row_format(names['b_list%d'%j][3:],url,username,password)
	else:
		update_row_format(names['b_list%d'%j][3:],url,username,password)
