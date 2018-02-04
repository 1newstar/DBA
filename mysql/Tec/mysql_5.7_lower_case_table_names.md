mysql5.7 测试表名不区分大小写后

myisam表的文件名区分大小写时，数据库层面上支持小写，和部分大写
innodb表的文件名区分大小写时，数据库层面上依然可以不区分大小写


==============================================
mysql> show variables like 'lower%';
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| lower_case_file_system | OFF   |
| lower_case_table_names | 1     |
+------------------------+-------+
2 rows in set (0.00 sec)

[root@ToBeRoot uplooking]# mv ggg.MYI Ggg.MYI
[root@ToBeRoot uplooking]# mv ggg.MYD Ggg.MYD
[root@ToBeRoot uplooking]# mv Gff.frm Ggg.frm
[root@ToBeRoot uplooking]# booboo uplooking
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.7.18-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> select * from Ggg;
ERROR 29 (HY000): File './uplooking/ggg.MYD' not found (Errcode: 2 - No such file or directory)
mysql> select * from ggg;
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> select * from ggG;
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> select * from GGG;
ERROR 29 (HY000): File './uplooking/ggg.MYD' not found (Errcode: 2 - No such file or directory)
mysql> select * from GgG;
ERROR 29 (HY000): File './uplooking/ggg.MYD' not found (Errcode: 2 - No such file or directory)
mysql> select * from gGG;
ERROR 29 (HY000): File './uplooking/ggg.MYD' not found (Errcode: 2 - No such file or directory)
mysql> select * from gGg;
ERROR 29 (HY000): File './uplooking/ggg.MYD' not found (Errcode: 2 - No such file or directory)
mysql> select * from ggg;
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> select * from ggg;
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> select * from ggG;
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

====================================================
[root@ToBeRoot uplooking]# ll Gai*
-rw-r----- 1 mysql mysql   8684 Sep 19 15:35 Gai.frm
-rw-r----- 1 mysql mysql 557056 Sep 19 15:37 Gai.ibd
[root@ToBeRoot uplooking]# booboo uplooking
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.18-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> select * from Gai where id=20000;
+-------+-------+------+---------------------+------+
| id    | name  | age  | updatetime          | uuu  |
+-------+-------+------+---------------------+------+
| 20000 | a9998 | 9998 | 2017-08-24 11:40:26 |    0 |
+-------+-------+------+---------------------+------+
1 row in set (0.00 sec)

mysql> select * from GAI where id=20000;
+-------+-------+------+---------------------+------+
| id    | name  | age  | updatetime          | uuu  |
+-------+-------+------+---------------------+------+
| 20000 | a9998 | 9998 | 2017-08-24 11:40:26 |    0 |
+-------+-------+------+---------------------+------+
1 row in set (0.00 sec)

mysql> select * from gai where id=20000;
+-------+-------+------+---------------------+------+
| id    | name  | age  | updatetime          | uuu  |
+-------+-------+------+---------------------+------+
| 20000 | a9998 | 9998 | 2017-08-24 11:40:26 |    0 |
+-------+-------+------+---------------------+------+
1 row in set (0.00 sec)

mysql> select * from gaI where id=20000;
+-------+-------+------+---------------------+------+
| id    | name  | age  | updatetime          | uuu  |
+-------+-------+------+---------------------+------+
| 20000 | a9998 | 9998 | 2017-08-24 11:40:26 |    0 |
+-------+-------+------+---------------------+------+
1 row in set (0.00 sec)