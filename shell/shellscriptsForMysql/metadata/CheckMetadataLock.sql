# 查看有metalock锁的线程
# 查看未提交的事务运行时间，线程id，用户等信息
# 查看未提交的事务运行时间，线程id，用户，sql语句等信息
# 查看错误语句
# 根据错误语句的THREAD_ID，查看PROCESSLIST_ID

select id,State,command from information_schema.processlist where State="Waiting for table metadata lock";
select  timediff(sysdate(),trx_started) timediff,sysdate(),trx_started,id,USER,DB,COMMAND,STATE,trx_state,trx_query from information_schema.processlist,information_schema.innodb_trx  where trx_mysql_thread_id=id;
select  timediff(sysdate(),trx_started) timediff,sysdate(),trx_started,id,USER,DB,COMMAND,STATE,trx_state from information_schema.processlist,information_schema.innodb_trx where trx_mysql_thread_id=id\G;
select * from performance_schema.events_statements_current where SQL_TEXT like '%booboo%'\G;
select * from performance_schema.threads where thread_id=46052\G;
select * from information_schema.processlist where id=xxx\G;

select processlist_id from performance_schema.threads where thread_id==(select thread_id from performance_schema.events_statements_current where SQL_TEXT like '%booboo%');