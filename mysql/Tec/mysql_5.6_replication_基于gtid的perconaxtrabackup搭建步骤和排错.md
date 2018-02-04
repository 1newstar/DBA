# AB rplication 搭建步骤

> 从库当前用户名和密码 mysql -uroot -p'cqhjkj624991557.'

## 一、主从搭建步骤

》主库：
1. 授权信息，用户名和密码


2. 主库的全备份

`innobackupex --user=root --password=xxx /xxx`


》从库：

1. 停止服务
  `systemctl stop mysqld`

2. 清空数据文件，日志文件

```shell
rm -rf /HJKJ-DATA/mysql/data/*
rm -rf /data/mysqlLog/logs/*
```

3. 配置文件中，需要添加参数

```shell
	replicate_wild_do_table=fireway.%
	replicate_wild_do_table=finance.%
	replicate_wild_ignore_table=mysql.%
	replicate_wild_ignore_table=edw.%
	replicate_wild_ignore_table=etl2020.%
```

4. 导入数据 (percona xtrabackup 软件已经安装)

```shell
innobackupex --apply-log /HJKJ-DATA/2017-07-11_22-37-30
innobackupex --copy-back /HJKJ-DATA/2017-07-11_22-37-30
```

5. 修改权限

```shell
chown mysql. /HJKJ-DATA/mysql/data -R
```

6. 启动服务

```shell
systemctl start mysqld
```

7. 测试全备份数据状态，查看事务编号

8. 配置主从

- 1. `change master to master_user='repluser',master_password='replpass',master_host='119.90.40.222',master_auto_position=1;`

- 2. `start slave;`

- 3. `show slave status\G;`





## 具体操作记录

```shell

# 全备份文件压缩包60G，解压后294G，耗时70min

[root@hjkj-mysql ~]# date
Thu Jul 13 11:18:00 CST 2017


[root@hjkj-mysql HJKJ-DATA]# ll -h
total 60G
-rw-r--r-- 1 root  root   60G Jul 13 04:31 2017-07-11_22-37-30.tar.gz
drwx------ 2 root  root   16K Jul  7 09:54 lost+found
drwxr-xr-x 3 mysql mysql 4.0K Jul 13 09:29 mysql
-rw-r--r-- 1 root  root  324K Jul 13 09:34 zabbix-agent-3.0.3-1.el7.x86_64.rpm
[root@hjkj-mysql HJKJ-DATA]# ls
1.txt  2017-07-11_22-37-30.tar.gz  lost+found  mysql
[root@hjkj-mysql HJKJ-DATA]# du -h
16K	./lost+found
8.0K	./mysql/data/edw
8.0K	./mysql/data/finance
8.0K	./mysql/data/fireway
12M	./mysql/data/mysql
636K	./mysql/data/performance_schema
15M	./mysql/data/etl2020
263M	./mysql/data
263M	./mysql
60G	.
[root@hjkj-mysql HJKJ-DATA]# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G   30G  7.8G  80% /
devtmpfs        7.8G     0  7.8G   0% /dev
tmpfs           7.8G     0  7.8G   0% /dev/shm
tmpfs           7.8G   17M  7.8G   1% /run
tmpfs           7.8G     0  7.8G   0% /sys/fs/cgroup
/dev/vdb1       787G   60G  719G   8% /HJKJ-DATA
[root@hjkj-mysql HJKJ-DATA]# tar -zxf 2017-07-11_22-37-30.tar.gz 


12:53:24 解压完成

[root@hjkj-mysql HJKJ-DATA]# du -h
16K	./lost+found
14G	./2017-07-11_22-37-30/finance
266G	./2017-07-11_22-37-30/fireway
13M	./2017-07-11_22-37-30/mysql
636K	./2017-07-11_22-37-30/performance_schema
294G	./2017-07-11_22-37-30
8.0K	./mysql/data/edw
8.0K	./mysql/data/finance
8.0K	./mysql/data/fireway
12M	./mysql/data/mysql
636K	./mysql/data/performance_schema
15M	./mysql/data/etl2020
263M	./mysql/data
263M	./mysql
354G	.

[root@hjkj-mysql HJKJ-DATA]# ls
1.txt  2017-07-11_22-37-30  2017-07-11_22-37-30.tar.gz  lost+found  mysql
[root@hjkj-mysql HJKJ-DATA]# cd 2017-07-11_22-37-30/
[root@hjkj-mysql 2017-07-11_22-37-30]# cat xtrabackup_binlog_info 
master-bin.005119	480213344	5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028360

[root@hjkj-mysql 2017-07-11_22-37-30]# cat xtrabackup_info
uuid = 90703d66-664e-11e7-a7d3-44a8421278f5
name = 
tool_name = innobackupex
tool_command = --user=xtra --password=... /data/xtra_backu
tool_version = 2.3.4
ibbackup_version = 2.3.4
server_version = 5.6.25-log
start_time = 2017-07-11 22:37:31
end_time = 2017-07-11 23:35:27
lock_time = 0
binlog_pos = filename 'master-bin.005119', position '480213344', GTID of the last change '5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028360'
innodb_from_lsn = 0
innodb_to_lsn = 5187639613061
partial = N
incremental = N
format = file
compact = N
compressed = N
encrypted = N

备份工具的版本为 ibbackup_version = 2.3.4

[root@hjkj-mysql ~]# ls
lm_month_deduct.sql  Percona-XtraBackup-2.3.4-re80c779-el7-x86_64-bundle.tar
[root@hjkj-mysql ~]# tar -xf Percona-XtraBackup-2.3.4-re80c779-el7-x86_64-bundle.tar 
[root@hjkj-mysql ~]# ls
lm_month_deduct.sql                                      percona-xtrabackup-debuginfo-2.3.4-1.el7.x86_64.rpm
percona-xtrabackup-2.3.4-1.el7.x86_64.rpm                percona-xtrabackup-test-2.3.4-1.el7.x86_64.rpm
Percona-XtraBackup-2.3.4-re80c779-el7-x86_64-bundle.tar
[root@hjkj-mysql ~]# cat /etc/redhat-release 
CentOS Linux release 7.0.1406 (Core) 
[root@hjkj-mysql ~]# yum localinstall -y percona-xtrabackup-2.3.4-1.el7.x86_64.rpm 
Loaded plugins: langpacks
Examining percona-xtrabackup-2.3.4-1.el7.x86_64.rpm: percona-xtrabackup-2.3.4-1.el7.x86_64
Marking percona-xtrabackup-2.3.4-1.el7.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package percona-xtrabackup.x86_64 0:2.3.4-1.el7 will be installed
--> Processing Dependency: perl(DBD::mysql) for package: percona-xtrabackup-2.3.4-1.el7.x86_64
--> Processing Dependency: libev.so.4()(64bit) for package: percona-xtrabackup-2.3.4-1.el7.x86_64
--> Running transaction check
---> Package libev.x86_64 0:4.15-6.el7 will be installed
---> Package perl-DBD-MySQL.x86_64 0:4.023-5.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

========================================================================================================================
 Package                     Arch            Version              Repository                                       Size
========================================================================================================================
Installing:
 percona-xtrabackup          x86_64          2.3.4-1.el7          /percona-xtrabackup-2.3.4-1.el7.x86_64           21 M
Installing for dependencies:
 libev                       x86_64          4.15-6.el7           extras                                           44 k
 perl-DBD-MySQL              x86_64          4.023-5.el7          base                                            140 k

Transaction Summary
========================================================================================================================
Install  1 Package (+2 Dependent packages)

Total size: 22 M
Total download size: 184 k
Installed size: 22 M
Downloading packages:
(1/2): libev-4.15-6.el7.x86_64.rpm                                                               |  44 kB  00:00:00     
(2/2): perl-DBD-MySQL-4.023-5.el7.x86_64.rpm                                                     | 140 kB  00:00:00     
------------------------------------------------------------------------------------------------------------------------
Total                                                                                   553 kB/s | 184 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : libev-4.15-6.el7.x86_64                                                                              1/3 
  Installing : perl-DBD-MySQL-4.023-5.el7.x86_64                                                                    2/3 
  Installing : percona-xtrabackup-2.3.4-1.el7.x86_64                                                                3/3 
  Verifying  : perl-DBD-MySQL-4.023-5.el7.x86_64                                                                    1/3 
  Verifying  : percona-xtrabackup-2.3.4-1.el7.x86_64                                                                2/3 
  Verifying  : libev-4.15-6.el7.x86_64                                                                              3/3 

Installed:
  percona-xtrabackup.x86_64 0:2.3.4-1.el7                                                                               

Dependency Installed:
  libev.x86_64 0:4.15-6.el7                             perl-DBD-MySQL.x86_64 0:4.023-5.el7                            

Complete!
[root@hjkj-mysql ~]# which innobackupex
/usr/bin/innobackupex

============================================================================
[root@hjkj-mysql HJKJ-DATA]# systemctl stop mysqld
[root@hjkj-mysql HJKJ-DATA]# ll /HJKJ-DATA/mysql/data/
total 241944
-rw-rw---- 1 mysql mysql        56 Jul  7 11:36 auto.cnf
drwx------ 2 mysql mysql      4096 Jul 11 11:57 edw
drwx------ 2 mysql mysql      4096 Jul  7 13:28 etl2020
-rw-r--r-- 1 root  root      97249 Jul  7 13:12 etl.sql
drwx------ 2 mysql mysql      4096 Jul 13 09:25 finance
drwx------ 2 mysql mysql      4096 Jul 13 09:25 fireway
-rw-r----- 1 mysql mysql    153964 Jul  7 13:57 hjkj-mysql.err
-rw-rw---- 1 mysql mysql 146800640 Jul 13 13:07 ibdata1
-rw-rw---- 1 mysql mysql  50331648 Jul 13 13:07 ib_logfile0
-rw-rw---- 1 mysql mysql  50331648 Jul 13 09:23 ib_logfile1
drwx------ 2 mysql mysql      4096 Jul  7 11:36 mysql
drwx------ 2 mysql mysql      4096 Jul  7 11:36 performance_schema
[root@hjkj-mysql HJKJ-DATA]# rm -rf /HJKJ-DATA/mysql/data/*
[root@hjkj-mysql HJKJ-DATA]# ll /HJKJ-DATA/mysql/data/
total 0


[root@hjkj-mysql HJKJ-DATA]# ll /data/mysqlLog/logs/
total 21677232
-rw-rw---- 1 mysql mysql      225104 Jul 13 13:07 error.log
-rw-rw---- 1 mysql mysql         198 Jul 10 16:49 mysql-bin.000001
-rw-rw---- 1 mysql mysql     6132370 Jul 10 17:48 mysql-bin.000002
-rw-rw---- 1 mysql mysql        1095 Jul 10 19:45 mysql-bin.000003
-rw-rw---- 1 mysql mysql         254 Jul 10 19:46 mysql-bin.000004
-rw-rw---- 1 mysql mysql         772 Jul 11 11:33 mysql-bin.000005
-rw-rw---- 1 mysql mysql   134217989 Jul 11 12:50 mysql-bin.000006
-rw-rw---- 1 mysql mysql   134218175 Jul 11 12:59 mysql-bin.000007
-rw-rw---- 1 mysql mysql   134218103 Jul 11 13:08 mysql-bin.000008
-rw-rw---- 1 mysql mysql   134217801 Jul 11 13:17 mysql-bin.000009
-rw-rw---- 1 mysql mysql   134217842 Jul 11 13:26 mysql-bin.000010
-rw-rw---- 1 mysql mysql   134218044 Jul 11 13:35 mysql-bin.000011
-rw-rw---- 1 mysql mysql   134218186 Jul 11 13:44 mysql-bin.000012
-rw-rw---- 1 mysql mysql   134217825 Jul 11 13:54 mysql-bin.000013
-rw-rw---- 1 mysql mysql   134217905 Jul 11 14:03 mysql-bin.000014
-rw-rw---- 1 mysql mysql   134217890 Jul 11 14:12 mysql-bin.000015
-rw-rw---- 1 mysql mysql   134217957 Jul 11 14:22 mysql-bin.000016
-rw-rw---- 1 mysql mysql   134218196 Jul 11 14:31 mysql-bin.000017
-rw-rw---- 1 mysql mysql   134217843 Jul 11 14:40 mysql-bin.000018
-rw-rw---- 1 mysql mysql   134217909 Jul 11 14:49 mysql-bin.000019
-rw-rw---- 1 mysql mysql   134218079 Jul 11 14:59 mysql-bin.000020
-rw-rw---- 1 mysql mysql   134218099 Jul 11 15:08 mysql-bin.000021
-rw-rw---- 1 mysql mysql   134217915 Jul 11 15:17 mysql-bin.000022
-rw-rw---- 1 mysql mysql   134217775 Jul 11 15:27 mysql-bin.000023
-rw-rw---- 1 mysql mysql   134217977 Jul 11 15:36 mysql-bin.000024
-rw-rw---- 1 mysql mysql   134217817 Jul 11 15:45 mysql-bin.000025
-rw-rw---- 1 mysql mysql   134218161 Jul 11 15:55 mysql-bin.000026
-rw-rw---- 1 mysql mysql   134218054 Jul 11 16:04 mysql-bin.000027
-rw-rw---- 1 mysql mysql   134217803 Jul 11 16:14 mysql-bin.000028
-rw-rw---- 1 mysql mysql   134217944 Jul 11 16:23 mysql-bin.000029
-rw-rw---- 1 mysql mysql   134218183 Jul 11 16:32 mysql-bin.000030
-rw-rw---- 1 mysql mysql   134218120 Jul 11 16:42 mysql-bin.000031
-rw-rw---- 1 mysql mysql   134218116 Jul 11 16:51 mysql-bin.000032
-rw-rw---- 1 mysql mysql   134217968 Jul 11 17:01 mysql-bin.000033
-rw-rw---- 1 mysql mysql   134217780 Jul 11 17:10 mysql-bin.000034
-rw-rw---- 1 mysql mysql   134218108 Jul 11 17:20 mysql-bin.000035
-rw-rw---- 1 mysql mysql   134218066 Jul 11 17:29 mysql-bin.000036
-rw-rw---- 1 mysql mysql   134217967 Jul 11 17:39 mysql-bin.000037
-rw-rw---- 1 mysql mysql   134217822 Jul 11 17:48 mysql-bin.000038
-rw-rw---- 1 mysql mysql   134253957 Jul 11 21:35 mysql-bin.000039
-rw-rw---- 1 mysql mysql   134235229 Jul 11 21:35 mysql-bin.000040
-rw-rw---- 1 mysql mysql   134266102 Jul 11 21:35 mysql-bin.000041
-rw-rw---- 1 mysql mysql   134266686 Jul 11 21:36 mysql-bin.000042
-rw-rw---- 1 mysql mysql   134294173 Jul 11 21:36 mysql-bin.000043
-rw-rw---- 1 mysql mysql    93751775 Jul 11 22:34 mysql-bin.000044
-rw-rw---- 1 mysql mysql         254 Jul 11 22:35 mysql-bin.000045
-rw-rw---- 1 mysql mysql         396 Jul 12 14:45 mysql-bin.000046
-rw-rw---- 1 mysql mysql         254 Jul 12 14:59 mysql-bin.000047
-rw-rw---- 1 mysql mysql   134237788 Jul 12 15:42 mysql-bin.000048
-rw-rw---- 1 mysql mysql   134243754 Jul 12 15:42 mysql-bin.000049
-rw-rw---- 1 mysql mysql   134270158 Jul 12 15:42 mysql-bin.000050
-rw-rw---- 1 mysql mysql   518772326 Jul 12 15:43 mysql-bin.000051
-rw-rw---- 1 mysql mysql     4414719 Jul 12 17:56 mysql-bin.000052
-rw-rw---- 1 mysql mysql         254 Jul 12 18:09 mysql-bin.000053
-rw-rw---- 1 mysql mysql         882 Jul 13 13:07 mysql-bin.000054
-rw-rw---- 1 mysql mysql        1998 Jul 12 18:09 mysql-bin.index
-rw-rw---- 1 mysql mysql 16070727871 Jul 12 14:58 mysql.slow
[root@hjkj-mysql HJKJ-DATA]# rm -rf /data/mysqlLog/logs/*
[root@hjkj-mysql HJKJ-DATA]# ll /data/mysqlLog/logs/
total 0

[root@hjkj-mysql HJKJ-DATA]# innobackupex --apply-log /HJKJ-DATA/2017-07-11_22-37-30 
170713 13:22:32 innobackupex: Starting the apply-log operation

IMPORTANT: Please check that the apply-log run completes successfully.
           At the end of a successful apply-log run innobackupex
           prints "completed OK!".

innobackupex version 2.3.4 based on MySQL server 5.6.24 Linux (x86_64) (revision id: e80c779)
xtrabackup: cd to /HJKJ-DATA/2017-07-11_22-37-30
xtrabackup: This target seems to be not prepared yet.
xtrabackup: xtrabackup_logfile detected: size=64339968, start_lsn=(5187582419027)
xtrabackup: using the following InnoDB configuration for recovery:
xtrabackup:   innodb_data_home_dir = ./
xtrabackup:   innodb_data_file_path = ibdata1:12M:autoextend
xtrabackup:   innodb_log_group_home_dir = ./
xtrabackup:   innodb_log_files_in_group = 1
xtrabackup:   innodb_log_file_size = 64339968
xtrabackup: using the following InnoDB configuration for recovery:
xtrabackup:   innodb_data_home_dir = ./
xtrabackup:   innodb_data_file_path = ibdata1:12M:autoextend
xtrabackup:   innodb_log_group_home_dir = ./
xtrabackup:   innodb_log_files_in_group = 1
xtrabackup:   innodb_log_file_size = 64339968
xtrabackup: Starting InnoDB instance for recovery.
xtrabackup: Using 104857600 bytes for buffer pool (set by --use-memory parameter)
InnoDB: Using atomics to ref count buffer pool pages
InnoDB: The InnoDB memory heap is disabled
InnoDB: Mutexes and rw_locks use GCC atomic builtins
InnoDB: Memory barrier is not used
InnoDB: Compressed tables use zlib 1.2.7
InnoDB: Using CPU crc32 instructions
InnoDB: Initializing buffer pool, size = 100.0M
InnoDB: Completed initialization of buffer pool
InnoDB: Highest supported file format is Barracuda.
InnoDB: Log scan progressed past the checkpoint lsn 5187582419027
InnoDB: Database was not shutdown normally!
InnoDB: Starting crash recovery.
InnoDB: Reading tablespace information from the .ibd files...
InnoDB: Restoring possible half-written data pages 
InnoDB: from the doublewrite buffer...
InnoDB: Doing recovery: scanned up to log sequence number 5187587661824 (9%)
InnoDB: Doing recovery: scanned up to log sequence number 5187592904704 (18%)
InnoDB: Doing recovery: scanned up to log sequence number 5187598147584 (27%)
InnoDB: Doing recovery: scanned up to log sequence number 5187603390464 (36%)
InnoDB: Doing recovery: scanned up to log sequence number 5187608633344 (45%)
InnoDB: Doing recovery: scanned up to log sequence number 5187613876224 (55%)
InnoDB: Starting an apply batch of log records to the database...
InnoDB: Progress in percent: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 
InnoDB: Apply batch completed
InnoDB: Doing recovery: scanned up to log sequence number 5187619119104 (64%)
InnoDB: Doing recovery: scanned up to log sequence number 5187624361984 (73%)
InnoDB: Doing recovery: scanned up to log sequence number 5187629604864 (82%)
InnoDB: Doing recovery: scanned up to log sequence number 5187634847744 (91%)
InnoDB: Doing recovery: scanned up to log sequence number 5187639613061 (100%)
InnoDB: Starting an apply batch of log records to the database...
InnoDB: Progress in percent: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 
InnoDB: Apply batch completed
InnoDB: 128 rollback segment(s) are active.
InnoDB: Waiting for purge to start
InnoDB: 5.6.24 started; log sequence number 5187639613061
xtrabackup: Last MySQL binlog file position 480213344, file name master-bin.005119

xtrabackup: starting shutdown with innodb_fast_shutdown = 1
InnoDB: FTS optimize thread exiting.
InnoDB: Starting shutdown...
InnoDB: Shutdown completed; log sequence number 5187639617444
xtrabackup: using the following InnoDB configuration for recovery:
xtrabackup:   innodb_data_home_dir = ./
xtrabackup:   innodb_data_file_path = ibdata1:12M:autoextend
xtrabackup:   innodb_log_group_home_dir = ./
xtrabackup:   innodb_log_files_in_group = 2
xtrabackup:   innodb_log_file_size = 50331648
InnoDB: Using atomics to ref count buffer pool pages
InnoDB: The InnoDB memory heap is disabled
InnoDB: Mutexes and rw_locks use GCC atomic builtins
InnoDB: Memory barrier is not used
InnoDB: Compressed tables use zlib 1.2.7
InnoDB: Using CPU crc32 instructions
InnoDB: Initializing buffer pool, size = 100.0M
InnoDB: Completed initialization of buffer pool
InnoDB: Setting log file ./ib_logfile101 size to 48 MB
InnoDB: Setting log file ./ib_logfile1 size to 48 MB
InnoDB: Renaming log file ./ib_logfile101 to ./ib_logfile0
InnoDB: New log files created, LSN=5187639617444
InnoDB: Highest supported file format is Barracuda.
InnoDB: 128 rollback segment(s) are active.
InnoDB: Waiting for purge to start
InnoDB: 5.6.24 started; log sequence number 5187639617548
xtrabackup: starting shutdown with innodb_fast_shutdown = 1
InnoDB: FTS optimize thread exiting.
InnoDB: Starting shutdown...
InnoDB: Shutdown completed; log sequence number 5187639630072
170713 13:23:30 completed OK!


[root@hjkj-mysql HJKJ-DATA]# innobackupex --copy-back /HJKJ-DATA/2017-07-11_22-37-30 
170713 13:25:26 innobackupex: Starting the copy-back operation

IMPORTANT: Please check that the copy-back run completes successfully.
           At the end of a successful copy-back run innobackupex
           prints "completed OK!".

70713 14:38:10 [01]        ...done
170713 14:38:10 [01] Copying ./performance_schema/events_waits_summary_global_by_event_name.frm to /HJKJ-DATA/mysql/data/performance_schema/events_waits_summary_global_by_event_name.frm
170713 14:38:10 [01]        ...done
170713 14:38:10 [01] Copying ./performance_schema/events_statements_summary_by_thread_by_event_name.frm to /HJKJ-DATA/mysql/data/performance_schema/events_statements_summary_by_thread_by_event_name.frm
170713 14:38:10 [01]        ...done
170713 14:38:10 [01] Copying ./performance_schema/socket_summary_by_event_name.frm to /HJKJ-DATA/mysql/data/performance_schema/socket_summary_by_event_name.frm
170713 14:38:10 [01]        ...done
170713 14:38:10 [01] Copying ./performance_schema/events_stages_history.frm to /HJKJ-DATA/mysql/data/performance_schema/events_stages_history.frm
170713 14:38:10 [01]        ...done
170713 14:38:10 completed OK!




[root@hjkj-mysql HJKJ-DATA]# cd /HJKJ-DATA/mysql/data/
[root@hjkj-mysql data]# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G  2.3G   35G   7% /
devtmpfs        7.8G     0  7.8G   0% /dev
tmpfs           7.8G     0  7.8G   0% /dev/shm
tmpfs           7.8G   17M  7.8G   1% /run
tmpfs           7.8G     0  7.8G   0% /sys/fs/cgroup
/dev/vdb1       787G  648G  132G  84% /HJKJ-DATA

[root@hjkj-mysql data]# ll
total 15249548
drwx------ 2 root root       28672 Jul 13 13:38 finance
drwx------ 2 root root       94208 Jul 13 14:38 fireway
-rw-r----- 1 root root 15514730496 Jul 13 13:32 ibdata1
-rw-r----- 1 root root    50331648 Jul 13 13:25 ib_logfile0
-rw-r----- 1 root root    50331648 Jul 13 13:25 ib_logfile1
drwx------ 2 root root        4096 Jul 13 14:38 mysql
drwx------ 2 root root        4096 Jul 13 14:38 performance_schema
-rw-r----- 1 root root          28 Jul 13 14:38 xtrabackup_binlog_pos_innodb
-rw-r----- 1 root root         561 Jul 13 14:38 xtrabackup_info
[root@hjkj-mysql data]# chown mysql. /HJKJ-DATA/mysql/data -R
[root@hjkj-mysql data]# ll
total 15249548
drwx------ 2 mysql mysql       28672 Jul 13 13:38 finance
drwx------ 2 mysql mysql       94208 Jul 13 14:38 fireway
-rw-r----- 1 mysql mysql 15514730496 Jul 13 13:32 ibdata1
-rw-r----- 1 mysql mysql    50331648 Jul 13 13:25 ib_logfile0
-rw-r----- 1 mysql mysql    50331648 Jul 13 13:25 ib_logfile1
drwx------ 2 mysql mysql        4096 Jul 13 14:38 mysql
drwx------ 2 mysql mysql        4096 Jul 13 14:38 performance_schema
-rw-r----- 1 mysql mysql          28 Jul 13 14:38 xtrabackup_binlog_pos_innodb
-rw-r----- 1 mysql mysql         561 Jul 13 14:38 xtrabackup_info

[root@hjkj-mysql data]# getenforce
Disabled

#启动服务

[root@hjkj-mysql data]# systemctl start mysqld
[root@hjkj-mysql data]# ps -ef|grep mysqld
mysql    15331     1  0 14:51 ?        00:00:00 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
mysql    15848 15331  2 14:51 ?        00:00:01 /usr/sbin/mysqld --basedir=/usr --datadir=/HJKJ-DATA/mysql/data --plugin-dir=/usr/lib64/mysql/plugin --log-error=/data/mysqlLog/logs/error.log --pid-file=/HJKJ-DATA/mysql/data/hjkj-mysql.pid --socket=/var/lib/mysql/mysql.sock --port=3306
root     15901 10540  0 14:52 pts/0    00:00:00 grep --color=auto mysqld

[root@hjkj-mysql data]# vim /etc/my.cnf
skip-grant-tables
[root@hjkj-mysql data]# systemctl restart mysqld
[root@hjkj-mysql data]# 
[root@hjkj-mysql data]# mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.6.36-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> update mysql.user set password=password('cqhjkj624991557.') where user='root' and host='localhost';
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye

[root@hjkj-mysql data]# vim /etc/my.cnf
[root@hjkj-mysql data]# systemctl restart mysqld
[root@hjkj-mysql data]# alias booboo="mysql -uroot -p'cqhjkj624991557.'"
[root@hjkj-mysql data]# booboo
Warning: Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.6.36-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> change master to master_user='repluser',master_password='replpass',master_host='119.90.40.222',master_auto_position=1;
Query OK, 0 rows affected, 2 warnings (0.03 sec)

mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: 
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: 
          Read_Master_Log_Pos: 4
               Relay_Log_File: hjkj-mysql-relay-bin.000001
                Relay_Log_Pos: 4
        Relay_Master_Log_File: 
             Slave_IO_Running: No
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
          Exec_Master_Log_Pos: 0
              Relay_Log_Space: 151
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 1236
                Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.'
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 100
                  Master_UUID: 5cc28f3c-6a8d-11e4-beff-00163e5563d9
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for the slave I/O thread to update it
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 170713 15:04:08
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 
            Executed_Gtid_Set: bcba2d0d-6797-11e7-bbb3-00163e00013d:1-2
                Auto_Position: 1
1 row in set (0.00 sec)

ERROR: 
No query specified

mysql> stop slave;
Query OK, 0 rows affected (0.00 sec)



# 报错显示主服务器上的设置了gtid_purged的值，从机也要同样设置才可。


mysql> set global gtid_purged="5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028360";
ERROR 1840 (HY000): @@GLOBAL.GTID_PURGED can only be set when @@GLOBAL.GTID_EXECUTED is empty.
mysql> reset master;
Query OK, 0 rows affected (0.01 sec)

mysql> set global gtid_purged="5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028360";
Query OK, 0 rows affected (0.00 sec)

mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> show slave stuatus\G;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'stuatus' at line 1
ERROR: 
No query specified

mysql> mysql> sho status\G;
*************************** 1. row ***************************
               Slave_IO_State: System lock
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005119
          Read_Master_Log_Pos: 481170511
               Relay_Log_File: hjkj-mysql-relay-bin.000002
                Relay_Log_Pos: 134561
        Relay_Master_Log_File: master-bin.005119
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
          Exec_Master_Log_Pos: 480347494
              Relay_Log_Space: 957787
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 146333
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
      Slave_SQL_Running_State: Reading event from the relay log
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-491029179
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028522
                Auto_Position: 1
1 row in set (0.04 sec)

ERROR: 
No query specified

mysql> show variables like '%gtid%';
+---------------------------------+--------------------------------------------------+
| Variable_name                   | Value                                            |
+---------------------------------+--------------------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                              |
| enforce_gtid_consistency        | ON                                               |
| gtid_executed                   |                                                  |
| gtid_mode                       | ON                                               |
| gtid_next                       | AUTOMATIC                                        |
| gtid_owned                      |                                                  |
| gtid_purged                     | 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491028360 |
| simplified_binlog_gtid_recovery | OFF                                              |
+---------------------------------+--------------------------------------------------+
8 rows in set (0.00 sec)




# 报错以为找不到主服务器上的日志，后来经过确认日志是存在的，而是gtid的问题，从库由于执行过写操作，所以事务标识与主库不一致。
# 必须清空gtid_executed ，并设置gtid_purged的值为全备份数据中最后一个全局事务标识符号。


mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: System lock
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005119
          Read_Master_Log_Pos: 1241946810
               Relay_Log_File: hjkj-mysql-relay-bin.000005
                Relay_Log_Pos: 86846475
        Relay_Master_Log_File: master-bin.005119
             Slave_IO_Running: Yes
            Slave_SQL_Running: No
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: fireway.%,finance.%
  Replicate_Wild_Ignore_Table: mysql.%,edw.%,etl2020.%
                   Last_Errno: 1146
                   Last_Error: Worker 0 failed executing transaction '' at master log master-bin.005119, end_log_pos 971381272; Error 'Table 'fireway.PR_DELAY_RETURN_AMOUNT' doesn't exist' on query. Default database: 'fireway'. Query: 'TRUNCATE TABLE  PR_DELAY_RETURN_AMOUNT'
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 969727047
              Relay_Log_Space: 493292169
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
               Last_SQL_Errno: 1146
               Last_SQL_Error: Worker 0 failed executing transaction '' at master log master-bin.005119, end_log_pos 971381272; Error 'Table 'fireway.PR_DELAY_RETURN_AMOUNT' doesn't exist' on query. Default database: 'fireway'. Query: 'TRUNCATE TABLE  PR_DELAY_RETURN_AMOUNT'
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
     Last_SQL_Error_Timestamp: 170713 16:35:40
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-491046904
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491042021,
bcba2d0d-6797-11e7-bbb3-00163e00013d:1-2
                Auto_Position: 1
1 row in set (0.05 sec)



[root@hjkj-mysql ~]# vim /etc/my.cnf
lower_case_table_names=1
[root@hjkj-mysql ~]# systemctl restart mysqld
[root@hjkj-mysql ~]# booboo
Warning: Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.6.36-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> show slave statsus\G;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'statsus' at line 1
ERROR: 
No query specified

mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 119.90.40.222
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: master-bin.005120
          Read_Master_Log_Pos: 199101835
               Relay_Log_File: hjkj-mysql-relay-bin.000005
                Relay_Log_Pos: 95706145
        Relay_Master_Log_File: master-bin.005119
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
          Exec_Master_Log_Pos: 978586717
              Relay_Log_Space: 704452747
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 145918
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
           Retrieved_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:491028361-491051646
            Executed_Gtid_Set: 5cc28f3c-6a8d-11e4-beff-00163e5563d9:1-491045976,
bcba2d0d-6797-11e7-bbb3-00163e00013d:1-2
                Auto_Position: 1
1 row in set (0.00 sec)

ERROR: 
No query specified

# 报错是由于查询使用大写表名，而从机没有配置不区分大小
lower_case_table_names=1

```



