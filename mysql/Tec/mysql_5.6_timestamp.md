## 关于5.5和5.6的时间戳

> 2017-07-20 BoobooWei

### TIMESTAMP在MySQL5.5中的行为

> 时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数。通俗的讲， 时间戳是一份能够表示一份数据在一个特定时间点已经存在的完整的可验证的数据。 

- 第一个未设置默认值的TIMESTAMP NOT NULL字段隐式默认值： 
  CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- 后面未设置默认值的TIMESTAMP NOT NULL字段隐式默认值： 
  0000-00-00 00:00:00
- TIMESTAMP NOT NULL字段插入NULL时，会使用隐式默认值： 
  CURRENT_TIMESTAMP
- 不支持多个CURRENT_TIMESTAMP 默认值

| table                                    | insert                  | select                                   |
| ---------------------------------------- | ----------------------- | ---------------------------------------- |
| create db1.t1 (id int,created timestamp); | insert db1.t1 set id=1; | 2017-07-20 13:16:25                      |
| create db1.t2 (id int,created timestamp not null); | insert db1.t2 set id=1; | 2017-07-20 13:16:29                      |
| create db1.t3 (id int,created timestamp not null default '0000-00-00 00:00:00'); | insert db1.t3 set id=1; | 0000-00-00 00:00:00                      |
| create db1.t4 (id int,created timestamp not null,modifed not null); | insert db1.t4 set id=1; | 2017-07-20 13:16:35 \| 0000-00-00 00:00:00 |

```shell
MariaDB [db1]> create table db1.t1 (id int,created timestamp);
Query OK, 0 rows affected (0.04 sec)

MariaDB [db1]> create table db1.t2 (id int,created timestamp not null);
Query OK, 0 rows affected (0.35 sec)

MariaDB [db1]> create table db1.t3 (id int,created timestamp not null default '0000-00-00 00:00:00');
Query OK, 0 rows affected (0.32 sec)

MariaDB [db1]> create table db1.t4 (id int,created timestamp not null,modified timestamp not null);
Query OK, 0 rows affected (0.08 sec)

MariaDB [db1]> insert into db1.t1 set id='booboo';
Query OK, 1 row affected, 1 warning (0.30 sec)

MariaDB [db1]> insert into db1.t2 set id='booboo';
Query OK, 1 row affected, 1 warning (0.44 sec)

MariaDB [db1]> insert into db1.t3 set id='booboo';
Query OK, 1 row affected, 1 warning (0.50 sec)

MariaDB [db1]> insert into db1.t4 set id='booboo';
Query OK, 1 row affected, 1 warning (0.47 sec)

MariaDB [db1]> select * from t1;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    0 | 2017-07-20 13:16:25 |
+------+---------------------+
1 row in set (0.00 sec)

MariaDB [db1]> select * from t2;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    0 | 2017-07-20 13:16:29 |
+------+---------------------+
1 row in set (0.00 sec)

MariaDB [db1]> select * from t3;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    0 | 0000-00-00 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

MariaDB [db1]> select * from t4;
+------+---------------------+---------------------+
| id   | created             | modified            |
+------+---------------------+---------------------+
|    0 | 2017-07-20 13:16:35 | 0000-00-00 00:00:00 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)
```



### TIMESTAMP在MySQL5.6中的行为

- 支持多个CURRENT_TIMESTAMP 默认值

- 可以兼容5.5的行为，支持隐性默认值 

  - explicit_defaults_for_timestamp=0

  - 在5.6.6及以后的版本中，如果在配置文件中没有指定explicit_defaults_for_timestamp参数，启动时error日志中会报如下错误

    ```
    [Warning] TIMESTAMP with implicit DEFAULT value is deprecated.
    Please use --explicit_defaults_for_timestamp server option (see
    documentation for more details).
    ```

- 可以去掉隐性默认值 explicit_defaults_for_timestamp=1

  - 如果我们在启动的时候在配置文件中指定了explicit_defaults_for_timestamp=1，mysql会按照如下的方式处理TIMESTAMP 列
  - - 此时如果TIMESTAMP列没有显式的指定not null属性，那么默认的该列可以为null，此时向该列中插入null值时，会直接记录null，而不是current timestamp。


- 不会自动的为表中的第一个TIMESTAMP列加上`DEFAULT CURRENT_TIMESTAMP` 和ON UPDATE CURRENT_TIMESTAMP属性，除非你在建表的时候显式的指明
  - 如果TIMESTAMP列被加上了not null属性，并且没有指定默认值。这时如果向表中插入记录，但是没有给该TIMESTAMP列指定值的时候，如果strict sql_mode被指定了，那么会直接报错。如果strict sql_mode没有被指定，那么会向该列中插入'0000-00-00 00:00:00'并且产生一个warning
  - explicit_defaults_for_timestamp参数主要用来控制TIMESTAMP数据类型跟其他数据类型不一致的特性，但是TIMESTAMP的这个特性在将来会被废弃，所以explicit_defaults_for_timestamp参数也会在将来被废弃

#### 测试结果

##### 设置sql_mode不跳过该错误

```shel
mysql> select @@sql_mode;
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                                                |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```



| explicit_defaults_for_timestamp=0        | insert                  | select                                   |
| ---------------------------------------- | ----------------------- | ---------------------------------------- |
| create table t1 (id int,created timestamp); | insert db1.t1 set id=1; | 2017-07-20 14:23:16                      |
| create table t2 (id int,created timestamp not null); | insert db1.t2 set id=1; | 2017-07-20 14:23:20                      |
| create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00'); | error                   |                                          |
| create table t4 (id int,created timestamp not null,modifed timestamp not null); | error                   |                                          |
| create table db1.t3 (id int,created timestamp not null default '2017-10-01 00:00:00'); | insert db1.t3 set id=1; | 2017-10-01 00:00:00                      |
| create table db1.t4 (id int,created timestamp not null,modified timestamp not null default '2017-10-01 00:00:00'); | insert db1.t4 set id=1; | 2017-07-20 14:23:25 \| 2017-10-01 00:00:00 |

```shell
mysql> select @@explicit_defaults_for_timestamp;
+-----------------------------------+
| @@explicit_defaults_for_timestamp |
+-----------------------------------+
|                                 0 |
+-----------------------------------+
1 row in set (0.00 sec)

mysql> create table db1.t1 (id int,created timestamp);create table db1.t2 (id int,created timestamp not null);
Query OK, 0 rows affected (0.03 sec)

Query OK, 0 rows affected (0.03 sec)

mysql> create table db1.t3 (id int,created timestamp not null default '0000-00-00 00:00:00');
ERROR 1067 (42000): Invalid default value for 'created'
mysql> create table db1.t4 (id int,created timestamp not null,modified timestamp not null);
ERROR 1067 (42000): Invalid default value for 'modified'
mysql> create table db1.t3 (id int,created timestamp not null default '2017-10-01 00:00:00');
Query OK, 0 rows affected (0.09 sec)

mysql> create table db1.t4 (id int,created timestamp not null,modified timestamp not null default '2017-10-01 00:00:00');
Query OK, 0 rows affected (0.03 sec)

mysql> insert into db1.t1 set id=1;
Query OK, 1 row affected (0.01 sec)

mysql> insert into db1.t2 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> insert into db1.t3 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> insert into db1.t4 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> select * from db1.t1;select * from db1.t2;select * from db1.t3;select * from db1.t4;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 2017-07-20 14:23:16 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 2017-07-20 14:23:20 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 2017-10-01 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+---------------------+
| id   | created             | modified            |
+------+---------------------+---------------------+
|    1 | 2017-07-20 14:23:25 | 2017-10-01 00:00:00 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)
```





| explicit_defaults_for_timestamp=1        | insert                  |       | select              |
| ---------------------------------------- | ----------------------- | ----- | ------------------- |
| create table t1 (id int,created timestamp); | insert db1.t1 set id=1; |       | NULL                |
| create table t2 (id int,created timestamp not null); | insert db1.t2 set id=1; | error |                     |
| create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00'); | error                   |       |                     |
| create table t3 (id int,created timestamp not null default '2017-10-01 00:00:00'); | insert db1.t3 set id=1; |       | 2017-10-01 00:00:00 |
| create table t4 (id int,created timestamp not null,modified timestamp not null); | insert db1.t4 set id=1; | error |                     |

```shell
mysql> select @@explicit_defaults_for_timestamp;
+-----------------------------------+
| @@explicit_defaults_for_timestamp |
+-----------------------------------+
|                                 1 |
+-----------------------------------+
1 row in set (0.00 sec)

mysql> drop table t1,t2,t3,t4;
Query OK, 0 rows affected (0.05 sec)

mysql> show tables;
Empty set (0.00 sec)

mysql> create table db1.t1 (id int,created timestamp);create table db1.t2 (id int,created timestamp not null);
Query OK, 0 rows affected (0.05 sec)

Query OK, 0 rows affected (0.03 sec)

mysql> create table db1.t3 (id int,created timestamp not null default '0000-00-00 00:00:00');
ERROR 1067 (42000): Invalid default value for 'created'
mysql> create table db1.t4 (id int,created timestamp not null,modified timestamp not null);
Query OK, 0 rows affected (0.05 sec)

mysql> create table db1.t3 (id int,created timestamp not null default '2017-10-01 00:00:00');
Query OK, 0 rows affected (0.04 sec)

mysql> insert into db1.t1 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> insert into db1.t2 set id=1;
ERROR 1364 (HY000): Field 'created' doesn't have a default value
mysql> insert into db1.t3 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> insert into db1.t4 set id=1;
ERROR 1364 (HY000): Field 'created' doesn't have a default value

mysql> insert into db1.t2 set id=1,created='2017-10-01 00:00:00';
Query OK, 1 row affected (0.01 sec)

mysql> insert into db1.t2 set id=1,created=current_timestamp();
Query OK, 1 row affected (0.00 sec)

mysql> insert into db1.t4 set id=1,created=current_timestamp(),modified=current_timestamp();
Query OK, 1 row affected (0.01 sec)

mysql> select * from t1;
+------+---------+
| id   | created |
+------+---------+
|    1 | NULL    |
+------+---------+
1 row in set (0.00 sec)

mysql> select * from t2;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 2017-10-01 00:00:00 |
|    1 | 2017-07-20 14:44:27 |
+------+---------------------+
2 rows in set (0.00 sec)

mysql> select * from t3;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 2017-10-01 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

mysql> select * from t4;
+------+---------------------+---------------------+
| id   | created             | modified            |
+------+---------------------+---------------------+
|    1 | 2017-07-20 14:44:46 | 2017-07-20 14:44:46 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)

mysql> select * from t5;
Empty set (0.00 sec)

mysql> insert into t5 set id=1;
Query OK, 1 row affected (0.00 sec)

mysql> select * from t5;
+------+---------------------+---------------------+
| id   | created             | modified            |
+------+---------------------+---------------------+
|    1 | 2017-07-20 14:48:12 | 2017-07-20 14:48:12 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)
```



##### 设置sql_mode跳过该错误

```shell
set @@sql_mode='';
```



| explicit_defaults_for_timestamp=0        | insert                  | select                                   |
| ---------------------------------------- | ----------------------- | ---------------------------------------- |
| create table t1 (id int,created timestamp); | insert db1.t1 set id=1; | NULL                                     |
| create table t2 (id int,created timestamp not null); | insert db1.t2 set id=1; | 0000-00-00 00:00:00                      |
| create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00'); | insert db1.t3 set id=1; | 0000-00-00 00:00:00                      |
| create table t4 (id int,created timestamp not null,modified timestamp not null); | insert db1.t4 set id=1; | 0000-00-00 00:00:00 \| 0000-00-00 00:00:00 |

```shell
mysql> set @@sql_mode='';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> select @@sql_mode;
+------------+
| @@sql_mode |
+------------+
|            |
+------------+
1 row in set (0.00 sec)

mysql> create table t1 (id int,created timestamp);
Query OK, 0 rows affected (0.03 sec)

mysql> create table t2 (id int,created timestamp not null);
Query OK, 0 rows affected (0.03 sec)

mysql> create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00');
Query OK, 0 rows affected (0.04 sec)

mysql> create table t4 (id int,created timestamp not null,modifed timestamp not null);
Query OK, 0 rows affected (0.03 sec)

mysql> insert into t1 set id=1;insert into t2 set id=1;insert into t3 set id=1;insert into t4 set id=1;
Query OK, 1 row affected (0.01 sec)

Query OK, 1 row affected, 1 warning (0.00 sec)

Query OK, 1 row affected (0.01 sec)

Query OK, 1 row affected, 2 warnings (0.00 sec)

mysql> select * from t1;select * from t2;select * from t3;select * from t4;
+------+---------+
| id   | created |
+------+---------+
|    1 | NULL    |
+------+---------+
2 rows in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 0000-00-00 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    1 | 0000-00-00 00:00:00 |
+------+---------------------+
2 rows in set (0.00 sec)

+------+---------------------+---------------------+
| id   | created             | modifed             |
+------+---------------------+---------------------+
|    1 | 0000-00-00 00:00:00 | 0000-00-00 00:00:00 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)
```



| explicit_defaults_for_timestamp=1        | insert                  | select                                   |
| ---------------------------------------- | ----------------------- | ---------------------------------------- |
| create table t1 (id int,created timestamp); | insert db1.t1 set id=1; | NULL                                     |
| create table t2 (id int,created timestamp not null); | insert db1.t2 set id=1; | 0000-00-00 00:00:00                      |
| create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00'); | insert db1.t3 set id=1; | 0000-00-00 00:00:00                      |
| create table t4 (id int,created timestamp not null,modifed timestamp not null); | insert db1.t4 set id=1; | 0000-00-00 00:00:00 \| 0000-00-00 00:00:00 |

```shell
mysql> set explicit_defaults_for_timestamp=1;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@explicit_defaults_for_timestamp;
+-----------------------------------+
| @@explicit_defaults_for_timestamp |
+-----------------------------------+
|                                 1 |
+-----------------------------------+
1 row in set (0.00 sec)

mysql> create table t1 (id int,created timestamp);
Query OK, 0 rows affected (0.04 sec)

mysql> create table t2 (id int,created timestamp not null);
Query OK, 0 rows affected (0.03 sec)

mysql> create table t3 (id int,created timestamp not null default '0000-00-00 00:00:00');
Query OK, 0 rows affected (0.03 sec)

mysql> create table t4 (id int,created timestamp not null,modifed not null);
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'not null)' at line 1
mysql> create table t4 (id int,created timestamp not null,modifed timestamp not null);
Query OK, 0 rows affected (0.03 sec)

mysql> insert into t1 set id=1;
Query OK, 1 row affected (0.01 sec)

mysql> insert into t2 set id=2;
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> insert into t3 set id=3;
Query OK, 1 row affected (0.00 sec)

mysql> insert into t4 set id=4;
Query OK, 1 row affected, 2 warnings (0.01 sec)

mysql> select * from t1;select * from t2;select * from t3;select * from t4;
+------+---------+
| id   | created |
+------+---------+
|    1 | NULL    |
+------+---------+
1 row in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    2 | 0000-00-00 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+
| id   | created             |
+------+---------------------+
|    3 | 0000-00-00 00:00:00 |
+------+---------------------+
1 row in set (0.00 sec)

+------+---------------------+---------------------+
| id   | created             | modifed             |
+------+---------------------+---------------------+
|    4 | 0000-00-00 00:00:00 | 0000-00-00 00:00:00 |
+------+---------------------+---------------------+
1 row in set (0.00 sec)
```



### 测试总结

| SQL                                      | MySQL版本 | explicit_defaults_for_timestamp | sql_mode | select                                   |
| ---------------------------------------- | ------- | ------------------------------- | -------- | ---------------------------------------- |
| created timestamp                        | 5.5     | 无该参数                            | 开启       | current_timestamp()插入时的系统时间              |
|                                          | 5.6     | 0                               | 开启       | current_timestamp()插入时的系统时间              |
|                                          | 5.6     | 1                               | 开启       | NULL                                     |
|                                          | 5.6     | 0                               | 关闭       | NULL                                     |
|                                          | 5.6     | 1                               | 关闭       | NULL                                     |
| created timestamp not null               | 5.5     | 无该参数                            | 开启       | current_timestamp()插入时的系统时间              |
|                                          | 5.6     | 0                               | 开启       | current_timestamp()插入时的系统时间              |
|                                          | 5.6     | 1                               | 开启       | error 需要强制插入大于1970年的日期                   |
|                                          | 5.6     | 0                               | 关闭       | 0000-00-00 00:00:00                      |
|                                          | 5.6     | 1                               | 关闭       | 0000-00-00 00:00:00                      |
| created timestamp not null default '0000-00-00 00:00:00' | 5.5     | 无该参数                            | 开启       | 设定的默认值 0000-00-00 00:00:00               |
|                                          | 5.6     | 0                               | 开启       | error 需要强制指定大于1970年的日期                   |
|                                          | 5.6     | 1                               | 开启       | error 需要强制指定大于1970年的日期                   |
|                                          | 5.6     | 0                               | 关闭       | 0000-00-00 00:00:00                      |
|                                          | 5.6     | 1                               | 关闭       | 0000-00-00 00:00:00                      |
| created timestamp not null,modified timestamp not null | 5.5     | 无该参数                            | 开启       | 2017-07-20 13:16:35 \| 0000-00-00 00:00:00 |
|                                          | 5.6     | 0                               | 开启       | created列为current_timestamp()即插入时的系统时间；modified列需要强制设置默认值为大于1970年的日期 |
|                                          | 5.6     | 1                               | 开启       | created列为current_timestamp()即插入时的系统时间；modified列需要强制插入默认值为大于1970年的日期 |
|                                          | 5.6     | 0                               | 关闭       | 0000-00-00 00:00:00                      |
|                                          | 5.6     | 1                               | 关闭       | 0000-00-00 00:00:00                      |

#### MySQL 5.5 自己的总结

1. timestamp默认不会为NULL，所以not null设与不设置都是一样的；
2. 如果用户插入记录时timestamp的列没有插入值，则默认为**当前系统的时间**，或者为用户自定义的default时间；
3. 用户自定义的default时间可以是`0000-00-00 00:00:00`。

#### MySQL 5.6 自己的总结

1. 5.6和5.5的timestamp表示范围

   | 版本   | timestamp范围                              | default                                 | sql_mode关闭          |
   | ---- | ---------------------------------------- | --------------------------------------- | ------------------- |
   | 5.5  | 1970-01-01 00:00:00 到 2037-12-31 23:59:59 | 0000-00-00 00:00:00                     |                     |
   | 5.6  | 1970-01-01 00:00:00 到 2037-12-31 23:59:59 | NULL(explicit_defaults_for_timestamp=1) | 0000-00-00 00:00:00 |

2. 新增explicit_defaults_for_timestamp参数

   如果用户插入记录时timestamp的列没有插入值,则情况入下表：

   | explicit_defaults_for_timestamp | created timestatmp | created timestamp not null |
   | ------------------------------- | ------------------ | -------------------------- |
   | 0（默认）                           | 当前系统的时间            | 当前系统的时间                    |
   | 1                               | NULL               | error 需要强制插入大于1970年的日期     |

   可以观察到，当该参数的值使用默认的0时，与5.5的情况是相同的。

3. 用户设定的default时间不可以是`0000-00-00 00:00:00`，除非关闭sql_mode；



```shell
mysql> insert into t3 set id=4,created='2037-12-31 23:59:59';
Query OK, 1 row affected (0.01 sec)

mysql> insert into t3 set id=5,created='2038-12-31 23:59:59';
Query OK, 1 row affected, 1 warning (0.00 sec)

mysql> select * from t3;
+------+---------------------+
| id   | created             |
+------+---------------------+
|    3 | 0000-00-00 00:00:00 |
|    4 | 2037-12-31 23:59:59 |
|    5 | 0000-00-00 00:00:00 |
+------+---------------------+
3 rows in set (0.00 sec)
```

