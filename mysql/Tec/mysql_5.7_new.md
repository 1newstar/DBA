## What Is New in MySQL 5.7

> 官方文档 https://dev.mysql.com/doc/refman/5.7/en/mysql-nutshell.html

## Optimizer

### 说明

可以使用EXPLAIN来获得连接的执行计划:

```
EXPLAIN [options] FOR CONNECTION connection_id;
```

### 案例

```shell
# sessionA
mysql> select *,sleep(10) from t1;

# sessionB
mysql> explain FOR CONNECTION 1180;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    4 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------+
1 row in set (0.00 sec)

mysql> show processlist;
+------+------+-----------+-----------+---------+------+----------+------------------+
| Id   | User | Host      | db        | Command | Time | State    | Info             |
+------+------+-----------+-----------+---------+------+----------+------------------+
| 1180 | root | localhost | uplooking | Sleep   |   41 |          | NULL             |
| 1181 | root | localhost | NULL      | Query   |    0 | starting | show processlist |
+------+------+-----------+-----------+---------+------+----------+------------------+
2 rows in set (0.00 sec)

mysql> explain FOR CONNECTION 1181;
ERROR 3012 (HY000): EXPLAIN FOR CONNECTION command is supported only for SELECT/UPDATE/INSERT/DELETE/REPLACE
mysql> select connection_id();

```

