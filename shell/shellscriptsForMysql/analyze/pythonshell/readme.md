## 该脚本的功能如下：
1. 获取日志中的所有DML语句及时间位置
2. 进行DML语法修正
3. 转换时间戳为日期时间
4. 最终将转换后的SQL语句保存在数据库，表名mysqltobinlog

## 脚本使用方法：
1. bash b2s_pre.sh binlogfile 进行日志预处理，该脚本返回binlogfile.new文件
2. python binlog_analyze.py binlogfile.new  该脚本将binlog转换为sql并保存于数据库中
3. python foo.py  该脚本进行sql语句的分析，例如统计某个时段的sql类型占比

## 待改进：
1. 目前一次只能分析一个脚本，第二次分析会覆盖mysqltobinlog表
2. 分析的内容比较简单
3. sql回滚未实现

## example:

```shell
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
```
## 脚本中使用到的list和table

### binlog日志

```shell
#170820 13:28:11 server id 1  end_log_pos 123 CRC32 0x1cd21485 	Start: binlog v 4, server v 5.7.18-log created 170820 13:28:11
#170820 13:28:11 server id 1  end_log_pos 194 CRC32 0x32a7332a 	Previous-GTIDs
#170820 13:28:52 server id 1  end_log_pos 259 CRC32 0xcfd207ca 	Anonymous_GTID	last_committed=0	sequence_number=1
#170820 13:28:52 server id 1  end_log_pos 329 CRC32 0xbbd608e3 	Query	thread_id=366	exec_time=0	error_code=0
BEGIN
#170820 13:28:52 server id 1  end_log_pos 405 CRC32 0xdd20c538 	Table_map: `ks`.`x2_session` mapped to number 149
#170820 13:28:52 server id 1  end_log_pos 659 CRC32 0x9a55d823 	Update_rows: table id 149 flags: STMT_END_F
WHERE
  @1='0m1310tv23guj73i08a1rmgck6' 
  @2=1 
  @3='peadmin' 
  @4='d7bf1a4df987c99646b15a29c0907a56' 
  @5='124.15.243.5' 
  @6=0 
  @7=1 
  @8='' 
  @9='' 
  @10=1503205545 
  @11=1503205545 
  @12=1503206088 
  @13=0 
SET
  @1='0m1310tv23guj73i08a1rmgck6' 
  @2=1 
  @3='peadmin' 
  @4='d7bf1a4df987c99646b15a29c0907a56' 
  @5='124.15.243.5' 
  @6=0 
  @7=1 
  @8='' 
  @9='' 
  @10=1503205545 
  @11=1503205545 
  @12=1503206932 
  @13=0 
#170820 13:28:52 server id 1  end_log_pos 730 CRC32 0x226b6f3b 	Query	thread_id=366	exec_time=0	error_code=0
COMMIT

```

### b_list

| 0               | 1        | 2                                        | 3      | 4      |                   |
| --------------- | -------- | ---------------------------------------- | ------ | ------ | ----------------- |
| 时间戳             | position | events                                   | sql类型  | sql语句  |                   |
| 170820 13:28:11 | 123      | Start: binlog v 4, server v 5.7.18-log created 170820 13:28:11 | others | others |                   |
| 170820 13:28:52 | 194      | Previous-GTIDs                           | others | others |                   |
| 170820 13:28:52 | 259      | Anonymous_GTID	last_committed=0	sequence_number=1 | others | others |                   |
| 170820 13:28:52 | 329      | Query	thread_id=366	exec_time=0	error_code=0 | begin  | BEGIN  |                   |
| 170820 13:28:52 | 405      | Table_map: `ks`.`x2_session` mapped to number 149 | others | others |                   |
| 170820 13:28:52 | 659      | Update_rows: table id 149 flags: STMT_END_F | update | UPDATE | `ks`.`x2_session` |
| 170820 13:28:52 | 730      | Query	thread_id=366	exec_time=0	error_code=0 | commit | COMMIT |                   |

### binlogtosql表

```shell
mysql> desc binlogtosql;
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| id      | int(11)     | NO   | PRI | NULL    | auto_increment |
| edate   | date        | NO   |     | NULL    |                |
| etime   | time        | NO   |     | NULL    |                |
| pos     | int(11)     | NO   |     | NULL    |                |
| event   | text        | NO   |     | NULL    |                |
| type    | varchar(20) | NO   |     | NULL    |                |
| sqlinfo | text        | NO   |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)

```

| id   | edate | etime | pos  | event | type  | sqlinfo |
| ---- | ----- | ----- | ---- | ----- | ----- | ------- |
| 序号   | 执行日期  | 执行时间  | 位置编号 | 事件    | sql类型 | sql语句   |

```shell
mysql> select * from binlogtosql limit 7\G;
*************************** 1. row ***************************
     id: 1
  edate: 2017-08-20
  etime: 13:28:11
    pos: 123
  event: Start: binlog v 4, server v 5.7.18-log created 170820 13:28:11
   type: others
sqlinfo: others
*************************** 2. row ***************************
     id: 2
  edate: 2017-08-20
  etime: 13:28:11
    pos: 194
  event: Previous-GTIDs
   type: others
sqlinfo: others
*************************** 3. row ***************************
     id: 3
  edate: 2017-08-20
  etime: 13:28:52
    pos: 259
  event: Anonymous_GTID	last_committed=0	sequence_number=1
   type: others
sqlinfo: others
*************************** 4. row ***************************
     id: 4
  edate: 2017-08-20
  etime: 13:28:52
    pos: 329
  event: Query	thread_id=366	exec_time=0	error_code=0
   type: begin
sqlinfo: begin;
*************************** 5. row ***************************
     id: 5
  edate: 2017-08-20
  etime: 13:28:52
    pos: 405
  event: Table_map: `ks`.`x2_session` mapped to number 149
   type: others
sqlinfo: others
*************************** 6. row ***************************
     id: 6
  edate: 2017-08-20
  etime: 13:28:52
    pos: 659
  event: Update_rows: table id 149 flags: STMT_END_F
   type: update
sqlinfo: UPDATE `ks`.`x2_session`  SET  sessionid='0m1310tv23guj73i08a1rmgck6', sessionuserid=1, sessionusername='peadmin', sessionpassword='d7bf1a4df987c99646b15a29c0907a56', sessionip='124.15.243.5', sessionmanage=0, sessiongroupid=1, sessioncurrent='', sessionrandcode='', sessionlogintime=1503205545, sessiontimelimit=1503205545, sessionlasttime=1503206932, sessionmaster=0  WHERE  sessionid='0m1310tv23guj73i08a1rmgck6' and  sessionuserid=1 and  sessionusername='peadmin' and  sessionpassword='d7bf1a4df987c99646b15a29c0907a56' and  sessionip='124.15.243.5' and  sessionmanage=0 and  sessiongroupid=1 and  sessioncurrent='' and  sessionrandcode='' and  sessionlogintime=1503205545 and  sessiontimelimit=1503205545 and  sessionlasttime=1503206088 and  sessionmaster=0;
*************************** 7. row ***************************
     id: 7
  edate: 2017-08-20
  etime: 13:28:52
    pos: 730
  event: Query	thread_id=366	exec_time=0	error_code=0
   type: commit
sqlinfo: commit;
```

