# MySQL waiting  for metadata lock排查脚本
> 2017-08-21该bash脚本用来排查metadata lock错误

演示如下：

```shell
[root@ToBeRoot ~]# bash  CheckMetadataLock.sh 
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
Id	User	Host	db	Command	Time	State	Info
4	root	localhost	uplooking	Sleep	23		NULL
5	root	localhost	uplooking	Query	17	Waiting for table metadata lock	alter table t1 add a3 int default 0
6	root	localhost	uplooking	Query	13	Waiting for table metadata lock	select * from t1 where id=3
7	root	localhost	uplooking	Query	5	Waiting for table metadata lock	select * from t1 where id=4
8	root	localhost	NULL	Query	0	starting	show processlist
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
id	State	command	info
5	Waiting for table metadata lock	Query	alter table t1 add a3 int default 0
7	Waiting for table metadata lock	Query	select * from t1 where id=4
6	Waiting for table metadata lock	Query	select * from t1 where id=3
查看未提交的事务运行时间，线程id，用户等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
查看未提交的事务运行时间，线程id，用户，sql语句等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
查看错误语句
mysql: [Warning] Using a password on the command line interface can be insecure.
*************************** 1. row ***************************
thread_id: 29
 sql_text: select x from t1 where id=1
*************************** 2. row ***************************
thread_id: 30
 sql_text: alter table t1 add a3 int default 0
*************************** 3. row ***************************
thread_id: 31
 sql_text: select * from t1 where id=3
*************************** 4. row ***************************
thread_id: 32
 sql_text: select * from t1 where id=4
*************************** 5. row ***************************
thread_id: 37
 sql_text: select thread_id,sql_text from performance_schema.events_statements_current where SQL_TEXT regexp 't1'
根据错误语句thread_id定位到session会话或连接id:29
mysql: [Warning] Using a password on the command line interface can be insecure.
processlist_id
4
错误语句会话id:4
mysql: [Warning] Using a password on the command line interface can be insecure.
*************************** 1. row ***************************
     ID: 4
   USER: root
   HOST: localhost
     DB: uplooking
COMMAND: Sleep
   TIME: 41
  STATE: 
   INFO: NULL
[root@ToBeRoot ~]# booboo -e 'kill 4'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@ToBeRoot ~]# bash  CheckMetadataLock.sh 
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
Id	User	Host	db	Command	Time	State	Info
5	root	localhost	uplooking	Query	57	Waiting for table metadata lock	alter table t1 add a3 int default 0
6	root	localhost	uplooking	Sleep	53		NULL
7	root	localhost	uplooking	Sleep	45		NULL
16	root	localhost	NULL	Query	0	starting	show processlist
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
id	State	command	info
5	Waiting for table metadata lock	Query	alter table t1 add a3 int default 0
查看未提交的事务运行时间，线程id，用户等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
timediff	sysdate()	trx_started	id	USER	DB	COMMAND	STATE	trx_state	trx_query
00:00:21	2017-08-21 16:20:03	2017-08-21 16:19:42	5	root	uplooking	Query	Waiting for table metadata lock	RUNNING	alter table t1 add a3 int default 0
00:00:21	2017-08-21 16:20:03	2017-08-21 16:19:42	7	root	uplooking	Sleep		RUNNING	NULL
查看未提交的事务运行时间，线程id，用户，sql语句等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
*************************** 1. row ***************************
   timediff: 00:00:23
  sysdate(): 2017-08-21 16:20:05
trx_started: 2017-08-21 16:19:42
         id: 5
       USER: root
         DB: uplooking
    COMMAND: Query
      STATE: Waiting for table metadata lock
  trx_state: RUNNING
*************************** 2. row ***************************
   timediff: 00:00:23
  sysdate(): 2017-08-21 16:20:05
trx_started: 2017-08-21 16:19:42
         id: 7
       USER: root
         DB: uplooking
    COMMAND: Sleep
      STATE: 
  trx_state: RUNNING
查看错误语句
mysql: [Warning] Using a password on the command line interface can be insecure.
*************************** 1. row ***************************
thread_id: 30
 sql_text: alter table t1 add a3 int default 0
*************************** 2. row ***************************
thread_id: 31
 sql_text: select * from t1 where id=3
*************************** 3. row ***************************
thread_id: 32
 sql_text: select * from t1 where id=4
*************************** 4. row ***************************
thread_id: 45
 sql_text: select thread_id,sql_text from performance_schema.events_statements_current where SQL_TEXT regexp 't1'
根据错误语句thread_id定位到session会话或连接id:
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1
错误语句会话id:
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1
[root@ToBeRoot ~]# booboo -e 'kill 7'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@ToBeRoot ~]# bash  CheckMetadataLock.sh 
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
Id	User	Host	db	Command	Time	State	Info
5	root	localhost	uplooking	Sleep	98		NULL
6	root	localhost	uplooking	Sleep	94		NULL
24	root	localhost	NULL	Query	0	starting	show processlist
当前等待metadatalock的连接：
mysql: [Warning] Using a password on the command line interface can be insecure.
查看未提交的事务运行时间，线程id，用户等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
查看未提交的事务运行时间，线程id，用户，sql语句等信息
mysql: [Warning] Using a password on the command line interface can be insecure.
查看错误语句
mysql: [Warning] Using a password on the command line interface can be insecure.
*************************** 1. row ***************************
thread_id: 30
 sql_text: alter table t1 add a3 int default 0
*************************** 2. row ***************************
thread_id: 31
 sql_text: select * from t1 where id=3
*************************** 3. row ***************************
thread_id: 53
 sql_text: select thread_id,sql_text from performance_schema.events_statements_current where SQL_TEXT regexp 't1'
根据错误语句thread_id定位到session会话或连接id:
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1
错误语句会话id:
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1

```

