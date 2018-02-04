# **JAVA**连接**MySQL**数据库异常

[TOC]



## 故障现象

在HybridDB for Mysql中，有张表的字段是timestamp，然后设置了默认值是 0000-00-00 00:00:00，字段：`created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'；

查询的时候报：[9001, 2017062917221501119222214403025012876] Value '0000-00-00' can not be represented as java.sql.Timestamp；

程序中jdbc后加了&zeroDateTimeBehavior=convertToNull，还是报错，求解决。

联系人：吴文云

联系方式：13611515615

## 故障原因

1. 现在用户将低于MySQL 5.6 版本的比较老的数据导入到 HybridDB for Mysql 5.6中
2. 数据中有一个列是数据类型为时间戳属性`created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
3. 而5.6版本的timestamp不能使用'0000-00-00 00:00:00'

## 故障类型

SQL语句

## 故障处理

### Java端的处理

https://my.oschina.net/u/2284972/blog/479297

**JAVA**连接**MySQL**数据库，在操作值为0的timestamp类型时不能正确的处理，而是默认抛出一个异常，就是所见的：java.sql.SQLException: Cannot convert value '0000-00-00 00:00:00' from column 7 to TIMESTAMP。

在JDBC连接串中有一项属性：zeroDateTimeBehavior,可以用来配置出现这种情况时的处理策略，该属性有下列三个属性值：

* exception：默认值，即抛出SQL state [S1009]. Cannot convert value....的异常；
* convertToNull：将日期转换成NULL值；
* round：替换成最近的日期即0001-01-01；

因此对于这类异常，可以考虑通过修改连接串，附加zeroDateTimeBehavior=convertToNull属性的方式予以规避，例如：

`jdbc:mysql://localhost:3306/mydbname?zeroDateTimeBehavior=convertToNull`


这类异常的触发与timestamp赋值的操作有关，如果能够在设计阶段和记录写入阶段做好逻辑判断，避免写入 '0000-00-00 00:00:00'这类值，那么也可以避免出现 Cannot convert value '0000-00-00 00:00:00' from column N to TIMESTAMP的错误。

### MySQL端的处理

TIMESTAMP时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数。通俗的讲， 时间戳是一份能够表示一份数据在一个特定时间点已经存在的完整的可验证的数据。  

** 5.6版本的timestamp不能使用'0000-00-00 00:00:00'**

解决方法：

1. 建议将该列的声明改为　timestamp not null default current_timestamp；将老数据该列的值修改为可用值
2. （由于HybridDB不能修改数据库参数，所以此法在HDB上不可行）修改数据库sql_mode的值，跳过不可用数据的报错。


### 测试验证过程

测试环境使用MySQL 5.6

1. 查看当前默认的sql_mode的值
```shell
mysql> select @@sql_mode;
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                                                |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

2. 创建测试库后创建测试表booboo1，尝试使用默认时间戳值为'0000-00-00 00:00:00'，结果失败。
```shell
mysql> create database db100;
Query OK, 1 row affected (0.01 sec)

mysql> create table booboo1 (id int,t1 timestamp not null default '0000-00-00 00:00:00');
ERROR 1067 (42000): Invalid default value for 't1'
```

3. 重新以可用的默认时间戳值声明列，创建测试表booboo1。
```shell
mysql> create table booboo1 (id int,t1 timestamp not null default current_timestamp);
Query OK, 0 rows affected (0.04 sec)

mysql> desc booboo1;
+-------+-----------+------+-----+-------------------+-------+
| Field | Type      | Null | Key | Default           | Extra |
+-------+-----------+------+-----+-------------------+-------+
| id    | int(11)   | YES  |     | NULL              |       |
| t1    | timestamp | NO   |     | CURRENT_TIMESTAMP |       |
+-------+-----------+------+-----+-------------------+-------+
2 rows in set (0.00 sec)

mysql> insert into booboo1 set id=1;
Query OK, 1 row affected (0.01 sec)

mysql> insert into booboo1 set id=2;
Query OK, 1 row affected (0.00 sec)

mysql> select * from booboo1;
+------+---------------------+
| id   | t1                  |
+------+---------------------+
|    1 | 2017-06-30 10:16:43 |
|    2 | 2017-06-30 10:16:46 |
+------+---------------------+
2 rows in set (0.00 sec)
```

4. 设置sql_mode跳过sql错误后，再去创建测试表t1,声明列time timestamp not null default '0000-00-00 00:00:00'),显示成功。
```shell
mysql> set @@sql_mode='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
Query OK, 0 rows affected (0.00 sec)

mysql> select @@sql_mode;
+--------------------------------------------+
| @@sql_mode                                 |
+--------------------------------------------+
| NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+--------------------------------------------+
1 row in set (0.00 sec)

mysql> use db100;
Database changed
mysql> create table t1 (id int,time timestamp not null default '0000-00-00 00:00:00');
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t1 set id=1;
Query OK, 1 row affected (0.01 sec)

mysql> select * from t1;
+------+---------------------+
| id   | time                |
+------+---------------------+
|    1 | 0000-00-00 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)
```

## 故障总结

1. 这类异常的触发与timestamp赋值的操作有关，如果能够在设计阶段和记录写入阶段做好逻辑判断，避免写入 '0000-00-00 00:00:00'这类值，那么也可以避免出现 Cannot convert value '0000-00-00 00:00:00' from column N to TIMESTAMP的错误。
2. Mysql 5.5 和MySQL 5.6 中日期类型timestamp不一样了，需要注意。




