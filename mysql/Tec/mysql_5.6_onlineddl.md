# MySQL 在线DDL

[TOC]

[RDS for MySQL Online DDL 使用 ](https://help.aliyun.com/knowledge_detail/41733.html)
[RDS for MySQL 如何使用 Percona Toolkit](https://help.aliyun.com/knowledge_detail/41734.html)
[RDS for MySQL 只读实例同步延迟原因与处理](https://help.aliyun.com/knowledge_detail/41767.html)
[大表上新增字段问题－－相关解决方案](http://blog.csdn.net/sollion/article/details/6095931)
[只读实例简介]( https://help.aliyun.com/document_detail/26136.html?spm=5176.2020520104.200.7.75e47270RwLjA7)
[Online DDL与pt-online-schema-change](http://www.cnblogs.com/zengkefu/p/5671661.html)
[ONLINE DDL VS PT-ONLINE-SCHEMA-CHANGE](http://www.fromdual.com/online-ddl_vs_pt-online-schema-change)

[RDS最佳实践(五)—Mysql大字段的频繁更新导致binlog暴增](https://m.th7.cn/show/51/201408/66846.html)

## **pt-online-schema-change介绍**

[官网](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)

[资料](http://www.cnblogs.com/erisen/p/5971416.html)

RDS 在线更新大表加索引[【链接地址】]() (https://help.aliyun.com/knowledge_detail/41734.html)



​      percona 公司提供的一款在线更新表的工具，更新过程不会锁表，也就是说操作alter的过程不会阻塞写和读取。即使如此，建议大家操作前还是先做好表备份。

## **工作原理**

1. 创建需要执行alter操作的原表的一个临时表，然后在临时表中更改表结构。


1. 在原表中创建触发器（3个）三个触发器分别对应insert,update,delete操作
2. 从原表拷贝数据到临时表，拷贝过程中在原表进行的写操作都会更新到新建的临时表。
3. Rename 原表到old表中，在把临时表Rename为原表，最后将原表删除(可能不删除)，将原表上所创建的触发器删除。

| 步骤   | 说明    | 命令                                       |
| ---- | ----- | ---------------------------------------- |
| 1    | 创建新表  | create table t2 like t1 ;                |
| 2    | 创建索引  | alter table t2 add index(col1);          |
| 3    | 创建触发器 | 三个触发器分别对应insert,update,delete操作          |
| 4    | 导入数据  | insert into t2 (col1,col2....) select (col1,col2...) from t1; |
| 5    | 重命名   | rename table t1 to t1_tmp , t2 to t1;    |
| 6    | 删除原表  | drop table t1_tmp;                       |



## 参数说明

pt-online-schema-change [OPTIONS] DSN

- *options 可以自行查看 help*

1. DNS 为你要操作的[数据库](http://www.111cn.net/list-55/)和表。
2. `–dry-run`这个参数不建立触发器，不拷贝数据，也不会替换原表。只是创建和更改新表。
3. `–execute`这个参数会建立触发器，来保证最新变更的数据会影响至新表。注意：如果不加这个参数，这个工具会在执行一些检查后退出。
4. **注**：操作的表必须有主键；否则报错：`Cannot chunk the original table houy.ga: There is no good index and the table is oversized. at ./pt-online-schema-change line 5353.`
5. 该工具是用perl写的，操作系统需要安装一些依赖包`libdbi-perl perl-DBD-MySQL`

## 案例

1. 安装工具包

```shell
[root@ToBeRoot ~]# wget https://www.percona.com/downloads/percona-toolkit/3.0.3/binary/redhat/6/i386/percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar
--2017-07-04 12:04:30--  https://www.percona.com/downloads/percona-toolkit/3.0.3/binary/redhat/6/i386/percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar
Resolving www.percona.com... 74.121.199.234
Connecting to www.percona.com|74.121.199.234|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4792320 (4.6M) [application/x-tar]
Saving to: “percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar”

100%[============================================================================>] 4,792,320   1.71M/s   in 2.7s    

2017-07-04 12:04:34 (1.71 MB/s) - “percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar” saved [4792320/4792320]
[root@ToBeRoot ~]# tar -xf percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar 
[root@ToBeRoot ~]# ls
dx_1.txt  foo     hins2883083_data_20170629152533.tar.gz  percona-toolkit-3.0.3-rf61508f-el6-i386-bundle.tar  test
dx_2.txt  foo.sh  percona-toolkit-3.0.3-1.el6.i386.rpm    percona-toolkit-debuginfo-3.0.3-1.el6.i386.rpm
[root@ToBeRoot ~]# rpm -ivh percona-toolkit-3.0.3-1.el6.i386.rpm 
warning: percona-toolkit-3.0.3-1.el6.i386.rpm: Header V4 DSA/SHA1 Signature, key ID cd2efd2a: NOKEY
error: Failed dependencies:
	perl(DBI) >= 1.13 is needed by percona-toolkit-3.0.3-1.el6.i386
	perl(DBD::mysql) >= 1.0 is needed by percona-toolkit-3.0.3-1.el6.i386
	perl(Time::HiRes) is needed by percona-toolkit-3.0.3-1.el6.i386
	perl(IO::Socket::SSL) is needed by percona-toolkit-3.0.3-1.el6.i386
	perl(Term::ReadKey) is needed by percona-toolkit-3.0.3-1.el6.i386

[root@ToBeRoot ~]# yum localinstall -y percona-toolkit-3.0.3-1.el6.i386.rpm 
Installed:
  percona-toolkit.i386 0:3.0.3-1.el6                                                                                  
此处省略
Dependency Installed:
  perl-DBD-MySQL.i686 0:4.013-3.el6        perl-DBI.i686 0:1.609-4.el6                           
  perl-IO-Socket-SSL.noarch 0:1.31-3.el6_8.2      perl-Net-LibIDN.i686 0:0.12-3.el6              perl-Net-SSLeay.i686 0:1.35-10.el6_8.1      perl-TermReadKey.i686 0:2.30-13.el6                  perl-Time-HiRes.i686 4:1.9721-144.el6                        

Dependency Updated:
  perl.i686 4:5.10.1-144.el6                               perl-CGI.i686 0:3.51-144.el6          perl-ExtUtils-MakeMaker.i686 0:6.55-144.el6       perl-ExtUtils-ParseXS.i686 1:2.2003.0-144.el6   perl-Module-Pluggable.i686 1:3.90-144.el6                perl-Pod-Escapes.i686 1:1.04-144.el6   perl-Pod-Simple.i686 1:3.13-144.el6                      perl-Test-Harness.i686 0:3.17-144.el6   perl-Test-Simple.i686 0:0.92-144.el6                     perl-devel.i686 4:5.10.1-144.el6       perl-libs.i686 4:5.10.1-144.el6                          perl-version.i686 3:0.77-144.el6      
Complete!

# --user -u 数据库的用户名
# --password -p 密码
[root@ToBeRoot ~]# pt-online-schema-change --user=root --password='(Uploo00king)' --alter='add index (questiontype)' D=ks,t=booboo --execute
No slaves found.  See --recursion-method if host ToBeRoot has slaves.
Not checking slave lag because no slaves were found and --check-slave-lag was not specified.
Operation, tries, wait:
  analyze_table, 10, 1
  copy_rows, 10, 0.25
  create_triggers, 10, 1
  drop_triggers, 10, 1
  swap_tables, 10, 1
  update_foreign_keys, 10, 1
Altering `ks`.`booboo`...
Creating new table...
Created new table ks._booboo_new OK.
Altering new table...
Altered `ks`.`_booboo_new` OK.
2017-07-04T13:40:45 Creating triggers...
2017-07-04T13:40:45 Created triggers OK.
2017-07-04T13:40:45 Copying approximately 404 rows...
2017-07-04T13:40:45 Copied rows OK.
2017-07-04T13:40:45 Analyzing new table...
2017-07-04T13:40:45 Swapping tables...
2017-07-04T13:40:45 Swapped original and new tables OK.
2017-07-04T13:40:45 Dropping old table...
2017-07-04T13:40:45 Dropped old table `ks`.`_booboo_old` OK.
2017-07-04T13:40:45 Dropping triggers...
2017-07-04T13:40:45 Dropped triggers OK.
Successfully altered `ks`.`booboo`.

mysql> show index from booboo;
+--------+------------+--------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table  | Non_unique | Key_name     | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+--------+------------+--------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| booboo |          0 | PRIMARY      |            1 | questionid   | A         |         404 |     NULL | NULL   |      | BTREE      |         |               |
| booboo |          1 | questiontype |            1 | questiontype | A         |           5 |     NULL | NULL   |      | BTREE      |         |               |
+--------+------------+--------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
2 rows in set (0.00 sec)
```

