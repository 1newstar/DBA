#!/usr/bin/python
# -*- coding: utf-8 -*-

# 过滤出没有使用索引的查询
import sys
import os
import re
import time
import datetime

n=re.compile('Count')

str="Count: 1  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=16.0 (16), myexx[myexx]@[172.31.85.81]"


def parse_cstr(cstr):
    matchobj = re.match(r'Count:(.*)Time=(.*)Lock=(.*)Rows=(.*),(.*)', cstr)
    if not matchobj:
        return None
    count = matchobj.group(1).strip()
    time = matchobj.group(2).strip()
    lock = matchobj.group(3).strip()
    rows = matchobj.group(4).strip()
    user = matchobj.group(5).strip()
    return (count,time,lock,rows,user)
		

#1 将slowlog文本中的每一条sql分别保存在不同的列表中，例如第一条sql存放于b_list1=[count,time,lock,rows,user,sql语句]

a_list=open('zyan.txt').readlines()

num=0
names=locals()
for a_str in a_list:
        if n.match(a_str):
                num=num+1
		(count,time,lock,rows,user)=parse_cstr(a_str)
                names['b_list%d'%num]=[count,time,lock,rows,user]
	else:
		names['b_list%d'%num].append(a_str)


for j in range(1,num+1):
        c_list=names['b_list%d'%j]
	time_list=c_list[1].split()
	time_num=float(time_list[0].strip('s'))
	if time_num < 30:
		for k in c_list[5:]:
			if 'where' in k:
				print c_list
			else:
				break
