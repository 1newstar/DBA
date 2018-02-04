#!/bin/bash
# Usage: bash xxx.sh
# 2017-08-21 Booboo Wei

dbuser=root
dbpassword="(Uploo00king)"

# 查看有metalock锁的线程
# 查看未提交的事务运行时间，线程id，用户等信息
# 查看未提交的事务运行时间，线程id，用户，sql语句等信息
# 查看错误语句
# 根据错误语句的THREAD_ID，查看PROCESSLIST_ID

sql0="
show processlist"

sql1="
select id,State,command,info from information_schema.processlist where State='Waiting for table metadata lock';"

sql2="
select  timediff(sysdate(),trx_started) timediff,sysdate(),trx_started,id,USER,DB,COMMAND,STATE,trx_state,trx_query from information_schema.processlist,information_schema.innodb_trx  where trx_mysql_thread_id=id;"

sql3="
select  timediff(sysdate(),trx_started) timediff,sysdate(),trx_started,id,USER,DB,COMMAND,STATE,trx_state from information_schema.processlist,information_schema.innodb_trx where trx_mysql_thread_id=id\G;"

sql4="
select thread_id,sql_text from performance_schema.events_statements_current where SQL_TEXT regexp 't1'\G;"



#select processlist_id from performance_schema.threads where thread_id==(select thread_id from performance_schema.events_statements_current where SQL_TEXT like '%booboo%');


read -p '当前等待metadatalock的连接：' x
echo $sql0 | mysql -u $dbuser -p$dbpassword  
read -p '当前等待metadatalock的连接：' a
echo $sql1 | mysql -u $dbuser -p$dbpassword  
read -p "查看未提交的事务运行时间，线程id，用户等信息" b
echo $sql2 | mysql -u $dbuser -p$dbpassword
read -p '查看未提交的事务运行时间，线程id，用户，sql语句等信息' c
echo $sql3 | mysql -u $dbuser -p$dbpassword
read -p '查看错误语句' d
echo $sql4 | mysql -u $dbuser -p$dbpassword
read -p '根据错误语句thread_id定位到session会话或连接id:' tid
sql5="
select processlist_id from performance_schema.threads where thread_id=${tid};"
echo $sql5 | mysql -u $dbuser -p$dbpassword
read -p '错误语句会话id:' sid
sql6="
select p.* from information_schema.processlist p where id=${sid}\G;"
echo $sql6 | mysql -u $dbuser -p$dbpassword
