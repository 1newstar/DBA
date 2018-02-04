[root@ToBeRoot python]# cat qqa
#!/usr/local/python
# -*-coding:utf8 -*-
import redis
from multiprocessing import Process
import os

print "欢迎来到公共聊天室"
r=redis.Redis(host='localhost', port=6380, db=0, password='zyadmin',)
name_str=raw_input('亲，取个昵称吧：')
chan=r.pubsub()
chan.subscribe('qq')
chan.parse_response()

def publish(w_str):
	r.publish('qq',name_str+': '+w_str)



def subscribe():
	while True:
        	p_list=chan.parse_response()
        	print p_list[2]



if __name__ == '__main__':
	p2 = Process(target=subscribe)
	p2.start()
	while True:
		w_str=raw_input()
        	p1 = Process(target=publish,args=(w_str,))
		p1.start()



================================
运行结果如下：

[root@ToBeRoot python]# python qqa
欢迎来到公共聊天室
亲，取个昵称吧：superman
大家好！我是超人superman
superman: 大家好！我是超人superman
batman: 你们好，我是蝙蝠侠哈
superwoman: 你们好，我是神奇女侠哟
superwoman: 我要回家了下次聊啊
88
superman: 88
batman: 88


[root@ToBeRoot python]# 
[root@ToBeRoot python]# python qqa
欢迎来到公共聊天室
亲，取个昵称吧：batman
superman: 大家好！我是超人superman
你们好，我是蝙蝠侠哈
batman: 你们好，我是蝙蝠侠哈
superwoman: 你们好，我是神奇女侠哟
superwoman: 我要回家了下次聊啊
superman: 88
88
batman: 88

[root@ToBeRoot python]# python qqa
欢迎来到公共聊天室
亲，取个昵称吧：superwoman
superman: 大家好！我是超人superman
batman: 你们好，我是蝙蝠侠哈
你们好，我是神奇女侠哟
superwoman: 你们好，我是神奇女侠哟
我要回家了下次聊啊
superwoman: 我要回家了下次聊啊
superman: 88
batman: 88
