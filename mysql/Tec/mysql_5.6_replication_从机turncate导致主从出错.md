# 2017-07-14 ab replication 故障

## 报错信息

```shell
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: System lock
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005166
          Read_Master_Log_Pos: 400660323
               Relay_Log_File: hjkj-mysql-relay-bin.000184
                Relay_Log_Pos: 27858081
        Relay_Master_Log_File: master-bin.005138
             Slave_IO_Running: Yes
            Slave_SQL_Running: No
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: fireway.%,finance.%
  Replicate_Wild_Ignore_Table: mysql.%,edw.%,etl2020.%
                   Last_Errno: 1032
                   Last_Error: Worker 3 failed executing transaction '5cc28f3c-6a8d-11e4-beff-00163e5563d9:491632994' at master log master-bin.005138, end_log_pos 296296999; Could not execute Update_rows event on table fireway.sm_member_realtime_statistics; Can't find record in 'sm_member_realtime_statistics', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log FIRST, end_log_pos 296296999
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 296293666
              Relay_Log_Space: 30608511234
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 1032
               Last_SQL_Error: Worker 3 failed executing transaction '5cc28f3c-6a8d-11e4-beff-00163e5563d9:491632994' at master log master-bin.005138, end_log_pos 296296999; Could not execute Update_rows event on table fireway.sm_member_realtime_statistics; Can't find record in 'sm_member_realtime_statistics', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log FIRST, end_log_pos 296296999
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 100
                  Master_UUID: 5cc28f3c-6a8d-11e4-beff-00163e5563d9
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: 
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 170714 09:22:56
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-493057681
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491632993,
bcba2d0d-6797-11e7-bbb3-00163e00013d:1-269
                Auto_Position: 1
1 row in set (0.01 sec)

ERROR: 
No query specified
```

## 获取信息

1. 事务gtid

master-bin.005138 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491632994

2. 涉及的表

fireway.sm_member_realtime_statistics

3. 获取该pos的sql操作

```shell

[root@hjkj-mysql data]# mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000184 | sed -n '/296296999/p'
#170712 10:08:24 server id 100  end_log_pos 296296999 CRC32 0xbc0308c1 	Update_rows: table id 11310 flags: STMT_END_F

[root@hjkj-mysql data]# mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000184 | sed -n '/296296999/,+100p'|grep '^###' | sed 's/### //'

UPDATE `fireway`.`sm_member_realtime_statistics`
WHERE
  @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
  @2='HJB2000000000001442105' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @3='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @4='惠花现金贷' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
  @5='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @6='惠花现金贷' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @7=22 /* LONGINT meta=0 nullable=1 is_null=0 */
  @8=14 /* LONGINT meta=0 nullable=1 is_null=0 */
  @9=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @10=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
  @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
  @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
  @13=1479957551 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
  @14=22 /* LONGINT meta=0 nullable=1 is_null=0 */
  @15=14 /* LONGINT meta=0 nullable=1 is_null=0 */
  @16=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @17=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
  @18=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @19=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @20=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @21=0.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
SET
  @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
  @2='HJB2000000000001442105' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @3='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @4='惠花现金贷' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
  @5='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @6='惠花现金贷' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
  @7=23 /* LONGINT meta=0 nullable=1 is_null=0 */
  @8=14 /* LONGINT meta=0 nullable=1 is_null=0 */
  @9=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @10=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
  @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
  @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
  @13=1479957551 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
  @14=23 /* LONGINT meta=0 nullable=1 is_null=0 */
  @15=14 /* LONGINT meta=0 nullable=1 is_null=0 */
  @16=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @17=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
  @18=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @19=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @20=0 /* LONGINT meta=0 nullable=1 is_null=0 */
  @21=0.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
```

## 分析故障原因

1. 从机中没有该行记录  
```shell
mysql> select * from fireway.sm_member_realtime_statistics where id=2 \G;
Empty set (0.00 sec)
```
2. 需要确认是什么原因导致的。
3. 可能原因：从机执行了delete或truncate操作
4. 验证方法——从binlog中过滤出所有与该表有关的操作，进一步排查是否有delete和truncate操作。

## 具体步骤


### 1. 查看relaylog 183和184

当前sql重演到184，需要排查183 184，并没有delete和truncate的操作。
```shell
[root@hjkj-mysql data]#  mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000183 | sed -n '/sm_member_realtime_statistics/p'
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:57:06 server id 100  end_log_pos 140753961 CRC32 0x7f18fe66 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:57:16 server id 100  end_log_pos 141286468 CRC32 0x8d6d9c15 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:57:47 server id 100  end_log_pos 170990108 CRC32 0x82a16c88 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:57:58 server id 100  end_log_pos 173579905 CRC32 0xcc98103e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:57:59 server id 100  end_log_pos 173597322 CRC32 0x92959730 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:58:20 server id 100  end_log_pos 188539528 CRC32 0xc0ab026f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:58:31 server id 100  end_log_pos 193133361 CRC32 0x3746098b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:59:12 server id 100  end_log_pos 246486945 CRC32 0x3c39b9d8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712  9:59:53 server id 100  end_log_pos 251761686 CRC32 0xd0b9cd0a 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:01:04 server id 100  end_log_pos 258716318 CRC32 0x3a6ef266 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:02:55 server id 100  end_log_pos 265723194 CRC32 0xec7c9111 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`

[root@hjkj-mysql data]#  mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000184 | sed -n '/sm_member_realtime_statistics/p'
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:05:58 server id 100  end_log_pos 282580861 CRC32 0x8a05b6e7 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:05:59 server id 100  end_log_pos 282766802 CRC32 0xfb66b80c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:06:20 server id 100  end_log_pos 284062278 CRC32 0x28905b89 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:07:31 server id 100  end_log_pos 287812410 CRC32 0x8890ca64 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:08:02 server id 100  end_log_pos 295188615 CRC32 0x517a31b4 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:08:13 server id 100  end_log_pos 295858883 CRC32 0x0e70e614 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:08:24 server id 100  end_log_pos 296285071 CRC32 0xb8d40dbe 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:08:24 server id 100  end_log_pos 296296581 CRC32 0x4f2dcd7e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:09:24 server id 100  end_log_pos 300258446 CRC32 0x2d14416e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:09:26 server id 100  end_log_pos 300335949 CRC32 0x1d61a583 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:09:57 server id 100  end_log_pos 341971639 CRC32 0x90c10dab 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:10:18 server id 100  end_log_pos 343237280 CRC32 0x81656a27 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:11:08 server id 100  end_log_pos 347721738 CRC32 0x5bf6b6ff 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:12:19 server id 100  end_log_pos 361796721 CRC32 0x5e980ea2 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:12:30 server id 100  end_log_pos 362810990 CRC32 0x71da4708 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:12:31 server id 100  end_log_pos 362838199 CRC32 0xac47b7c9 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:13:42 server id 100  end_log_pos 378284666 CRC32 0xc776ed1b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:15:03 server id 100  end_log_pos 388625403 CRC32 0x8499bb2e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:15:03 server id 100  end_log_pos 388677884 CRC32 0x34b6f0c2 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:15:44 server id 100  end_log_pos 393827665 CRC32 0x19a14ed8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`
# INSERT INTO fireway.sm_member_realtime_statistics(
#170712 10:16:36 server id 100  end_log_pos 400260242 CRC32 0xdfd0b5e8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
# UPDATE  fireway.sm_member_realtime_statistics
#170712 10:16:47 server id 100  end_log_pos 401082452 CRC32 0x82fd89b3 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 11310
### UPDATE `fireway`.`sm_member_realtime_statistics`

[root@hjkj-mysql data]#  mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000183 | sed -n '/sm_member_realtime_statistics/,+20p'|grep '^###'
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=45 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002344934' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HLJAS332' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='邵长虹' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJA2000000000002253078' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='高峰' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1495254339 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=46 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001857010' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS689' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='邓琴' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000879035' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='庹志宏' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=5616.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1487556223 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @19=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=47 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000002099046' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HBAS401' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='李路' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000624075' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='肖金阳' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2699.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1491965974 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=48 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002484640' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HBAS502' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='弋小雪' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001811102' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='程茜' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2298.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1497770373 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=49 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001533080' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='CS0049' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='谭忠燕' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000603002' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='杨顺' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2699.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1481540737 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=50 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001088135' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='SCAS332' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='史巧凤' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000441212' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='何明镜' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3480.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1473667595 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=51 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001191122' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HNZZAS041' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='牛少峰' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001191124' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='左珍' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3000.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1476057408 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=52 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001925110' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS942' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='杨涛' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='116577' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='黄超' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3349.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1488871767 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=53 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002530866' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS835' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='唐国庆' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='63330' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='黄大伟' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3399.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1498653811 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=54 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000002021089' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HLJAS229' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='张杨' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000824039' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='李云峰' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2159.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1490750647 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
WARNING: The range of printed events ends with a row event or a table map event that does not have the STMT_END_F flag set. This might be because the last statement was not fully written to the log, or because you are using a --stop-position or --stop-datetime that refers to an event in the middle of a statement. The event(s) from the partial statement have not been written to output.
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=45 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002344934' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HLJAS332' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='邵长虹' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJA2000000000002253078' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='高峰' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1495254339 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */

[root@hjkj-mysql data]# grep @1= /tmp/booboo | awk '{print $2}'|sort -n -t '=' -k 2
@1=45 insert
@1=45 update
@1=46
@1=47
@1=48
@1=49
@1=50
@1=51
@1=52
@1=53
@1=54

[root@hjkj-mysql data]#  mysqlbinlog --no-defaults -v -v hjkj-mysql-relay-bin.000184 | sed -n '/sm_member_realtime_statistics/,+20p'|grep '^###'
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=55 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002236599' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS779' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='罗从友' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000952075' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='张涛' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2899.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1493709438 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=56 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001234314' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HNZZAS095' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='王亚平' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001191124' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='左珍' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3000.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1477049185 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=57 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002505016' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HLJAS385' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='张可嵩' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001118105' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='唐署光' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=1999.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1498099576 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=58 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000000097015' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS414' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='况正秋' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='130947' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='杨寿' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2999.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1449936000 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=59 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001952016' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS967' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='卢娜' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001857201' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='程超超' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=1399.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1489029510 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=60 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002497216' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HBAS497' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='张世超' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001367100' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='冯松涛' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2699.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1498011871 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=61 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001925065' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HBAS367' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='刘丽佳' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000778041' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='高强' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1488766325 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001442105' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='惠花现金贷' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='惠花现金贷' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=22 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=14 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @10=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1479957551 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=22 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @15=14 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @16=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @17=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @18=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=0 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=62 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000002021177' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HNAS382' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='谢容' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001925070' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='王晨旭' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=3988.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1491197547 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=63 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001234160' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS742' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='姬云霄' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='123547' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='田嘉翔' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=1398.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1476779978 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=64 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002505074' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='CS0256' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='雷玉平' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='45065' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='唐昌英' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=1499.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1498112023 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=65 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001955228' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS1019' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='姚莉娟' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000265029' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='刘炜' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1490078472 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=66 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002506384' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS1304' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='王海震' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='158034' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='王治露' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2899.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1498285314 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=18 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002252679' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HLJAS298' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='王海涛' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001118074' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='马金辉' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=1619.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1493961646 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=67 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001811053' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS909' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='金万美' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000297082' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='骆志勇' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=900.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1486521767 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=68 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000000065082' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS405' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='刘艳萍' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='71274' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='左开雨' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2699.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1449331200 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=61 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001925065' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HBAS367' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='刘丽佳' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000778041' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='高强' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1488766325 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001442105' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='惠花现金贷' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HHXJD' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='惠花现金贷' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=23 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=14 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @10=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1479957551 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=23 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @15=14 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @16=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @17=103800.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @18=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=0 /* LONGINT meta=0 nullable=1 is_null=0 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=69 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJA2000000000002433109' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS812' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='张君義' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='120768' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='刘小弟' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2599.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1496901230 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=65 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001955228' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS1019' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='姚莉娟' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000000265029' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='刘炜' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=NULL /* LONGINT meta=4613 nullable=1 is_null=1 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1490078472 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
### INSERT INTO `fireway`.`sm_member_realtime_statistics`
### SET
###   @1=70 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000000036115' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='AS389' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='秦小凤' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='AS389' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='秦小凤' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=NULL /* LONGINT meta=0 nullable=1 is_null=1 */
###   @10=2498.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1447776000 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @15=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @16=NULL /* TIMESTAMP(0) meta=0 nullable=1 is_null=1 */
###   @17=NULL /* TIMESTAMP(0) meta=4613 nullable=1 is_null=1 */
###   @18=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=1 /* LONGINT meta=0 nullable=1 is_null=0 */
WARNING: The range of printed events ends with a row event or a table map event that does not have the STMT_END_F flag set. This might be because the last statement was not fully written to the log, or because you are using a --stop-position or --stop-datetime that refers to an event in the middle of a statement. The event(s) from the partial statement have not been written to output.
### UPDATE `fireway`.`sm_member_realtime_statistics`
### WHERE
###   @1=19 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='HJB2000000000001811020' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @3='GZAS885' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @4='姜华明' /* VARSTRING(300) meta=300 nullable=1 is_null=0 */
###   @5='HJB2000000000001811018' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @6='周彰彬' /* VARSTRING(192) meta=192 nullable=1 is_null=0 */
###   @7=2 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @8=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @9=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @10=7000.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @11='2017:07:12' /* DATE meta=0 nullable=1 is_null=0 */
###   @12=1499788800 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @13=1486363228 /* TIMESTAMP(0) meta=0 nullable=1 is_null=0 */
###   @14=2 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @15=1 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @16=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @17=7000.00000 /* DECIMAL(18,5) meta=4613 nullable=1 is_null=0 */
###   @18=0 /* LONGINT meta=0 nullable=1 is_null=0 */
###   @19=0 /* LONGINT meta=0 nullable=1 is_null=0 */
```

### 2. 查看slave的binlog 

查找所有binlog日志，获取关键字sm_member_realtime_statistics的行
发现其中有`TRUNCATE TABLE sm_member_realtime_statistics`误操作


```shell

[root@hjkj-mysql logs]# for i in `ls mysql-bin*`;do mysqlbinlog --no-defaults $i | grep -H sm_member_realtime_statistics ;if [ $? -eq 0 ] ;then echo $i;fi ; done
(standard input):TRUNCATE TABLE sm_member_realtime_statistics
mysql-bin.000002
(standard input):#170712  8:40:26 server id 100  end_log_pos 131969412 CRC32 0xccad6447 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  8:44:07 server id 100  end_log_pos 132623794 CRC32 0x3bfce4a9 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  8:46:28 server id 100  end_log_pos 133340899 CRC32 0x5c00535b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
mysql-bin.000084
(standard input):#170712  8:50:19 server id 100  end_log_pos 138892 CRC32 0xa74dcce5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  8:53:50 server id 100  end_log_pos 1128836 CRC32 0x95d7e72d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  8:59:12 server id 100  end_log_pos 2661152 CRC32 0x63e54d92 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  8:59:33 server id 100  end_log_pos 2871784 CRC32 0xd3a8f592 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:00:36 server id 100  end_log_pos 4873066 CRC32 0x64682358 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:01:36 server id 100  end_log_pos 5850677 CRC32 0xbf67e189 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:02:26 server id 100  end_log_pos 7384744 CRC32 0x3cf04ad9 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:03:28 server id 100  end_log_pos 11568624 CRC32 0x590d7981 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:04:00 server id 100  end_log_pos 12643320 CRC32 0x6d02ecb4 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:06:01 server id 100  end_log_pos 17872922 CRC32 0x17e860df 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:06:22 server id 100  end_log_pos 18275690 CRC32 0x40d59142 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:06:33 server id 100  end_log_pos 18586989 CRC32 0x848184cf 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:06:44 server id 100  end_log_pos 18888241 CRC32 0x1842a242 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:08:35 server id 100  end_log_pos 21025642 CRC32 0xdf53100b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:09:25 server id 100  end_log_pos 28194448 CRC32 0x2f5eab3b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:10:16 server id 100  end_log_pos 29205026 CRC32 0x03d58c69 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:10:57 server id 100  end_log_pos 30109752 CRC32 0x8774733d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:11:07 server id 100  end_log_pos 32349546 CRC32 0x4e150c44 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:11:58 server id 100  end_log_pos 33537793 CRC32 0xedf7fbce 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:12:39 server id 100  end_log_pos 34375102 CRC32 0x69d641a1 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:12:40 server id 100  end_log_pos 34381894 CRC32 0x36db48ba 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:12:50 server id 100  end_log_pos 34497841 CRC32 0x509e08b2 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:13:01 server id 100  end_log_pos 34735795 CRC32 0x5b9d2bb4 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:13:02 server id 100  end_log_pos 34808939 CRC32 0x248f9ebc 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:13:14 server id 100  end_log_pos 34905542 CRC32 0x9cfaa34b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:14:25 server id 100  end_log_pos 51605038 CRC32 0x80fc5e63 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:15:15 server id 100  end_log_pos 53100420 CRC32 0x9acbe64d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:15:36 server id 100  end_log_pos 66022899 CRC32 0xfa7f2e18 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:15:37 server id 100  end_log_pos 66030110 CRC32 0x5419f87f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:18:47 server id 100  end_log_pos 69278890 CRC32 0x7464c362 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:19:28 server id 100  end_log_pos 83696339 CRC32 0xc92d5312 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:22:09 server id 100  end_log_pos 85707253 CRC32 0x2bcf1536 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:23:20 server id 100  end_log_pos 88309176 CRC32 0x28c2ff0e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:24:01 server id 100  end_log_pos 93203320 CRC32 0xaa10559c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
mysql-bin.000085
(standard input):#170712  9:31:03 server id 100  end_log_pos 14802290 CRC32 0xf84036fb 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:31:14 server id 100  end_log_pos 14978513 CRC32 0x40e96e6c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:32:25 server id 100  end_log_pos 15996350 CRC32 0xc905c17f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:33:56 server id 100  end_log_pos 19101835 CRC32 0x7d49efa5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:34:46 server id 100  end_log_pos 24121529 CRC32 0x5e82be88 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:35:46 server id 100  end_log_pos 25168114 CRC32 0xe6b381ca 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:36:28 server id 100  end_log_pos 25693553 CRC32 0x5b29a88e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:37:19 server id 100  end_log_pos 26528849 CRC32 0xcab08a5c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:37:30 server id 100  end_log_pos 26715811 CRC32 0x0db0f0bf 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:38:41 server id 100  end_log_pos 29094954 CRC32 0x1a7221f1 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:38:51 server id 100  end_log_pos 29405561 CRC32 0x7fc39cc0 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:39:02 server id 100  end_log_pos 29631952 CRC32 0x9b97e4da 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:39:23 server id 100  end_log_pos 30041467 CRC32 0xaf23a8f5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:40:14 server id 100  end_log_pos 34225973 CRC32 0x0138272d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:40:35 server id 100  end_log_pos 34772428 CRC32 0x0fda284f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:41:06 server id 100  end_log_pos 35445712 CRC32 0xb5ed890d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:42:08 server id 100  end_log_pos 40484680 CRC32 0x64352d64 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:42:29 server id 100  end_log_pos 40797311 CRC32 0xad07c0e0 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:43:19 server id 100  end_log_pos 43880638 CRC32 0xe71304b7 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:43:50 server id 100  end_log_pos 45561426 CRC32 0xe6a0a3e8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:44:31 server id 100  end_log_pos 46335371 CRC32 0x38a30b5c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:45:31 server id 100  end_log_pos 47285387 CRC32 0xc121e4e5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:46:32 server id 100  end_log_pos 49786389 CRC32 0x3ab1c72a 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:46:33 server id 100  end_log_pos 49805321 CRC32 0x2c6118f5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:48:25 server id 100  end_log_pos 53175555 CRC32 0xf0c99127 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:48:36 server id 100  end_log_pos 53434564 CRC32 0x6393ddd8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:49:27 server id 100  end_log_pos 54268269 CRC32 0x26c3070a 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:50:38 server id 100  end_log_pos 59523207 CRC32 0x749041de 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:51:08 server id 100  end_log_pos 60117487 CRC32 0x887cd1f1 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:52:58 server id 100  end_log_pos 63023443 CRC32 0xe76668cc 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:53:29 server id 100  end_log_pos 63605074 CRC32 0x38470596 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:54:10 server id 100  end_log_pos 88376377 CRC32 0x155faa0b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:54:41 server id 100  end_log_pos 94498524 CRC32 0x1f3598cd 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:55:21 server id 100  end_log_pos 115001503 CRC32 0xeeb04be5 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
mysql-bin.000086
(standard input):#170712  9:55:33 server id 100  end_log_pos 113935 CRC32 0x9383e68d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:56:04 server id 100  end_log_pos 5643394 CRC32 0xcb12f8f6 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:56:35 server id 100  end_log_pos 13501746 CRC32 0x7c1ddc44 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:57:06 server id 100  end_log_pos 37195667 CRC32 0x96d46fe2 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:57:16 server id 100  end_log_pos 37413944 CRC32 0xedf1702f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:57:47 server id 100  end_log_pos 66583556 CRC32 0xc6c3f69c 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:57:58 server id 100  end_log_pos 68878834 CRC32 0xa8a2e2bb 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:57:59 server id 100  end_log_pos 68888294 CRC32 0xaad2c623 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:58:20 server id 100  end_log_pos 83466598 CRC32 0xbcc5c8ae 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:58:31 server id 100  end_log_pos 87758789 CRC32 0x29109c8f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
mysql-bin.000087
(standard input):#170712  9:59:12 server id 100  end_log_pos 82299 CRC32 0x07176b5d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712  9:59:53 server id 100  end_log_pos 4290842 CRC32 0x6949a03f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712 10:01:04 server id 100  end_log_pos 9244296 CRC32 0x48a4712b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):#170712 10:02:55 server id 100  end_log_pos 12808368 CRC32 0xb66600b6 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 337
(standard input):TRUNCATE TABLE sm_member_realtime_statistics
(standard input):#170712 10:05:58 server id 100  end_log_pos 21328495 CRC32 0x531a51cb 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:05:59 server id 100  end_log_pos 21419607 CRC32 0xbf3c2dcb 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:06:20 server id 100  end_log_pos 22067680 CRC32 0x5675a5d0 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:07:31 server id 100  end_log_pos 23896622 CRC32 0xa07aab11 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:08:02 server id 100  end_log_pos 29857607 CRC32 0x1c41e75b 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:08:13 server id 100  end_log_pos 30163646 CRC32 0x332a24c8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
(standard input):#170712 10:08:24 server id 100  end_log_pos 30382122 CRC32 0x3b8e05fb 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 392
mysql-bin.000088
(standard input):#170714 14:24:29 server id 153  end_log_pos 1420196 CRC32 0x6cca72a6 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:08:24 server id 100  end_log_pos 1422025 CRC32 0x771a712f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:09:24 server id 100  end_log_pos 3359144 CRC32 0xe41ebf9d 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:09:26 server id 100  end_log_pos 3404663 CRC32 0x4480b5e8 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:09:57 server id 100  end_log_pos 44015383 CRC32 0x213db74f 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:10:18 server id 100  end_log_pos 44659605 CRC32 0x9632fb39 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
(standard input):#170712 10:11:08 server id 100  end_log_pos 47053098 CRC32 0x90c6e53e 	Table_map: `fireway`.`sm_member_realtime_statistics` mapped to number 2174
mysql-bin.000089
```


### 3.找出误操作的时间点 


```shell
[root@hjkj-mysql logs]#  mysqlbinlog --no-defaults -v -v mysql-bin.000088 | grep -B 8 'TRUNCATE' 
#170713 23:59:00 server id 153  end_log_pos 15219396 CRC32 0x03cfb7ac 	Query	thread_id=551	exec_time=0	error_code=0
use `fireway`/*!*/;
SET TIMESTAMP=1499961540/*!*/;
SET @@session.sql_auto_is_null=1/*!*/;
SET @@session.sql_mode=1073741824/*!*/;
/*!\C utf8 *//*!*/;
SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=8/*!*/;
SET @@session.collation_database=33/*!*/;
TRUNCATE TABLE sm_member_realtime_statistics
```


### 4. 询问客户是否知道什么导致了误操作

客户说没有客户端程序，没有人执行




# 通过relaylog中记录的update记录做回滚

```shell
mysql> desc fireway.sm_member_realtime_statistics;
+------------------+---------------+------+-----+---------+----------------+
| Field            | Type          | Null | Key | Default | Extra          |
+------------------+---------------+------+-----+---------+----------------+
| id               | bigint(20)    | NO   | PRI | NULL    | auto_increment |
| member_id        | varchar(64)   | YES  |     | NULL    |                |
| job_id           | varchar(64)   | YES  |     | NULL    |                |
| member_name      | varchar(100)  | YES  |     | NULL    |                |
| admin_id         | varchar(64)   | YES  |     | NULL    |                |
| admin_name       | varchar(64)   | YES  |     | NULL    |                |
| apply_count      | bigint(20)    | YES  |     | NULL    |                |
| pass_count       | bigint(20)    | YES  |     | NULL    |                |
| reject_count     | bigint(20)    | YES  |     | NULL    |                |
| trade_amount     | decimal(18,5) | YES  |     | NULL    |                |
| statis_date      | date          | YES  |     | NULL    |                |
| last_time        | timestamp     | YES  |     | NULL    |                |
| create_time      | timestamp     | YES  |     | NULL    |                |
| hui_apply_count  | bigint(20)    | YES  |     | NULL    |                |
| hui_pass_count   | bigint(20)    | YES  |     | NULL    |                |
| hui_reject_count | bigint(20)    | YES  |     | NULL    |                |
| hui_trade_amount | decimal(18,5) | YES  |     | NULL    |                |
| pos_apply_count  | bigint(20)    | YES  |     | NULL    |                |
| pos_pass_count   | bigint(20)    | YES  |     | NULL    |                |
| pos_reject_count | bigint(20)    | YES  |     | NULL    |                |
| pos_trade_amount | decimal(18,5) | YES  |     | NULL    |                |
+------------------+---------------+------+-----+---------+----------------+


insert into  `fireway`.`sm_member_realtime_statistics`
set
  id=2,
  member_id='HJB2000000000001442105',
  job_id='HHXJD' ,
  member_name='惠花现金贷' ,
  admin_id='HHXJD' ,
  admin_name='惠花现金贷' ,
  apply_count=22,
  pass_count=14,
  reject_count=0,
  trade_amount=103800.00000,
  statis_date='2017:07:12',
  last_time=from_unixtime('1499788800'),
  create_time=from_unixtime('1479957551'),
  hui_apply_count=22,
  hui_pass_count=14,
  hui_reject_count=0,
  hui_trade_amount=103800.00000,
  pos_apply_count=0,
  pos_pass_count=0,
  pos_reject_count=0,
  pos_trade_amount=0.00000;

# 注意row格式记录的timestamp格式是unixtime，需要转换以下

​```shell

mysql> select from_unixtime('1499788800');
+-----------------------------+
| from_unixtime('1499788800') |
+-----------------------------+
| 2017-07-12 00:00:00.000000  |
+-----------------------------+
1 row in set (0.00 sec)

mysql> select unix_timestamp('2017-07-12 00:00:00.000000');
+----------------------------------------------+
| unix_timestamp('2017-07-12 00:00:00.000000') |
+----------------------------------------------+
|                            1499788800.000000 |
+----------------------------------------------+
1 row in set (0.00 sec)

mysql> insert into  `fireway`.`sm_member_realtime_statistics`
    -> set
    ->   id=2,
    ->   member_id='HJB2000000000001442105',
    ->   job_id='HHXJD' ,
    ->   member_name='惠花现金贷' ,
    ->   admin_id='HHXJD' ,
    ->   admin_name='惠花现金贷' ,
    ->   apply_count=22,
    ->   pass_count=14,
    ->   reject_count=0,
    ->   trade_amount=103800.00000,
    ->   statis_date='2017:07:12',
    ->   last_time=from_unixtime('1499788800'),
    ->   create_time=from_unixtime('1479957551'),
    ->   hui_apply_count=22,
    ->   hui_pass_count=14,
    ->   hui_reject_count=0,
    ->   hui_trade_amount=103800.00000,
    ->   pos_apply_count=0,
    ->   pos_pass_count=0,
    ->   pos_reject_count=0,
    ->   pos_trade_amount=0.00000;
Query OK, 1 row affected (0.01 sec)

mysql> stop slave;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005170
          Read_Master_Log_Pos: 588938705
               Relay_Log_File: hjkj-mysql-relay-bin.000184
                Relay_Log_Pos: 76867734
        Relay_Master_Log_File: master-bin.005138
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: fireway.%,finance.%
  Replicate_Wild_Ignore_Table: mysql.%,edw.%,etl2020.%
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 345303319
              Relay_Log_Space: 35094719276
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 188042
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 100
                  Master_UUID: 5cc28f3c-6a8d-11e4-beff-00163e5563d9
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Waiting for Slave Worker to release partition
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-493119019
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491641136:491641180:491641188:491641380,
bcba2d0d-6797-11e7-bbb3-00163e00013d:1-280
                Auto_Position: 1
1 row in set (0.00 sec)

mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: 
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005170
          Read_Master_Log_Pos: 731174010
               Relay_Log_File: hjkj-mysql-relay-bin.000184
                Relay_Log_Pos: 93267434
        Relay_Master_Log_File: master-bin.005138
             Slave_IO_Running: No
            Slave_SQL_Running: No
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: fireway.%,finance.%
  Replicate_Wild_Ignore_Table: mysql.%,edw.%,etl2020.%
                   Last_Errno: 1032
                   Last_Error: Worker 2 failed executing transaction '5cc28f3c-6a8d-11e4-beff-00163e5563d9:491645391' at master log master-bin.005138, end_log_pos 361797106; Could not execute Update_rows event on table fireway.sm_member_realtime_statistics; Can't find record in 'sm_member_realtime_statistics', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log master-bin.005138, end_log_pos 361797106
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 361703019
              Relay_Log_Space: 35236954946
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 1032
               Last_SQL_Error: Worker 2 failed executing transaction '5cc28f3c-6a8d-11e4-beff-00163e5563d9:491645391' at master log master-bin.005138, end_log_pos 361797106; Could not execute Update_rows event on table fireway.sm_member_realtime_statistics; Can't find record in 'sm_member_realtime_statistics', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log master-bin.005138, end_log_pos 361797106
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 100
                  Master_UUID: 5cc28f3c-6a8d-11e4-beff-00163e5563d9
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: 
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 170714 14:25:41
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-493120005
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491645390,
bcba2d0d-6797-11e7-bbb3-00163e00013d:1-281
                Auto_Position: 1
1 row in set (0.00 sec)

mysql> select id,member_id,statis_date,last_time,create_time from `fireway`.`sm_member_realtime_statistics`;                          
+----+------------------------+-------------+---------------------+---------------------+
| id | member_id              | statis_date | last_time           | create_time         |
+----+------------------------+-------------+---------------------+---------------------+
|  2 | HJB2000000000001442105 | 2017-07-12  | 2017-07-12 00:00:00 | 2016-11-24 11:19:11 |
| 55 | HJA2000000000002236599 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-05-02 15:17:18 |
| 56 | HJB2000000000001234314 | 2017-07-12  | 2017-07-12 00:00:00 | 2016-10-21 19:26:25 |
| 57 | HJA2000000000002505016 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-06-22 10:46:16 |
| 58 | HJB2000000000000097015 | 2017-07-12  | 2017-07-12 00:00:00 | 2015-12-13 00:00:00 |
| 59 | HJB2000000000001952016 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-03-09 11:18:30 |
| 60 | HJA2000000000002497216 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-06-21 10:24:31 |
| 61 | HJB2000000000001925065 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-03-06 10:12:05 |
| 62 | HJB2000000000002021177 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-04-03 13:32:27 |
| 63 | HJB2000000000001234160 | 2017-07-12  | 2017-07-12 00:00:00 | 2016-10-18 16:39:38 |
| 64 | HJA2000000000002505074 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-06-22 14:13:43 |
| 65 | HJB2000000000001955228 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-03-21 14:41:12 |
| 66 | HJA2000000000002506384 | 2017-07-12  | 2017-07-12 00:00:00 | 2017-06-24 14:21:54 |
+----+------------------------+-------------+---------------------+---------------------+
13 rows in set (0.00 sec)
```

## 还原思路

### 1. 183号日志中的插入记录进行重演，能恢复出id为45到54的记录

```shell
# 获取所有表的记录

[root@hjkj-mysql data]# for i in `seq 183 490`;do mysqlbinlog --no-defaults -v -v --base64-output=DECODE-ROWS hjkj-mysql-relay-bin.000$i | sed -n '/sm_member_realtime_statistics/,/# at/p'|grep '^###' | sed 's/^### //' > /tmp/booboo.$i ;done

# 复制一份183日志

[root@hjkj-mysql tmp]# cp /tmp/booboo.183 /tmp/booboo.183.bac

#183号日志为row格式，需要修改格式
[root@hjkj-mysql tmp]# awk '{print $0,","}' /tmp/booboo.183.bac|sed -e 's/UPDATE\(.*\),/UPDATE\1/;s/INSERT\(.*\),/INSERT\1/;s/WHERE\(.*\),/WHERE\1/;s/SET\(.*\),/SET\1/;s/@21\(.*\),/@21\1;/;' > /tmp/booboo.183.c
[root@hjkj-mysql tmp]# vim /tmp/booboo.183.c
# 删除update @21列后面的;

# 添加函数
[root@hjkj-mysql tmp]# sed -e 's/@12=\(.*\)  ,/@12=from_unixtime(\1)  ,/;s/@13=\(.*\)  ,/@13=from_unixtime(\1)  ,/;' /tmp/booboo.183.c > /tmp/booboo.183.d

# 获取列名
[root@hjkj-mysql tmp]# booboo -e "desc fireway.sm_member_realtime_statistics"|awk '{print $1}' | sed '1d' > /tmp/tablecol

# 修改列名
[root@hjkj-mysql tmp]# cat ~/change.sh
k=1
while read col
do
        sed -i "s/@${k}=/${col}=/g" /tmp/booboo.183.d
        k=$((${k}+1))
done < /tmp/tablecol

# where 关键字后面为and

[root@hjkj-mysql tmp]# sed -i '233,252s/\(.*\),/\1 and /' booboo.183.d

# 导入sql
```

### 2. 184号-490号日志寻找1到44的记录

不用再尝试了，太累了





























```

```