#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 获取最新的5个新用户显示在网站首页

import mysqlbala
import redis

my = mysqlbala.mysqlhelper('localhost','root','xxx','uplooking')
res = my.queryAll('select name from gai order by  updatetime desc limit 5')
content = []
for i in res:
	for j in i:
		content.append(j)

r = redis.Redis('127.0.0.1',6379,0)
r.setex('5user',content,10)
print r.get('5user')
my.close()
