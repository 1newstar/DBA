# SQL_exists的使用

> 2017-11-29 booboowei

[toc]

## 准备测试环境

mysql5.7

3张表具体如下：
 
```shell
mysql> select * from t1;
+----+----------+
| id | name     |
+----+----------+
|  1 | superman |
|  2 | batman   |
+----+----------+
2 rows in set (0.00 sec)

mysql> select * from t2;
+-----+--------+
| eid | ename  |
+-----+--------+
|   1 | mysql  |
|   2 | oracle |
|   3 | redis  |
+-----+--------+
3 rows in set (0.00 sec)

mysql> select * from t3;
+-----+------+------+
| sid | id   | eid  |
+-----+------+------+
|   1 |    1 |    1 |
|   2 |    1 |    2 |
|   3 |    2 |    3 |
+-----+------+------+
3 rows in set (0.00 sec)
```

## 测试过程

### exists

```shell
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id;                                     
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+
3 rows in set (0.00 sec)


mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where exists(select * from t2 where t2.eid=t3.eid and t2.ename='mysql') and t3.sid=3;
Empty set (0.00 sec)

mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where exists(select * from t2 where t2.ename='mysql') and t3.sid=3;
+-----+------+--------+------+
| sid | id   | name   | eid  |
+-----+------+--------+------+
|   3 |    2 | batman |    3 |
+-----+------+--------+------+
1 row in set (0.00 sec)


# exists中的查询与外表没有连接，则仅仅作为判断真假的依据，因此第二条sql的查询过程是t1和t3联合后对sid做过略即可
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+
# 只保留sid=3的行
+-----+------+--------+------+
| sid | id   | name   | eid  |
+-----+------+--------+------+
|   3 |    2 | batman |    3 |
+-----+------+--------+------+

# exists中的查询与外表有连接，则第一步先与外表连接生产一个虚拟表如下：
mysql> select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename='mysql';
+-----+-------+-----+------+
| eid | ename | sid | id   |
+-----+-------+-----+------+
|   1 | mysql |   1 |    1 |
+-----+-------+-----+------+

# 接下来再与t1表连接，条件是t1.id=t3.id，如下所示
mysql> select * from (select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename='mysqll')as t4 join t1 on t1.id=t4.id;
+-----+-------+-----+------+----+----------+
| eid | ename | sid | id   | id | name     |
+-----+-------+-----+------+----+----------+
|   1 | mysql |   1 |    1 |  1 | superman |
+-----+-------+-----+------+----+----------+

# 最后从结果集中过滤sid=3的行
mysql> select * from (select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename='mysqll')as t4 join t1 on t1.id=t4.id and sid=3;
Empty set (0.00 sec)
```


### not exists

```shell
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where not exists(select * from t2 wherre t2.eid=t3.eid and t2.ename='mysql') and t3.sid=3;
+-----+------+--------+------+
| sid | id   | name   | eid  |
+-----+------+--------+------+
|   3 |    2 | batman |    3 |
+-----+------+--------+------+
1 row in set (0.00 sec)

mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where not exists(select * from t2 where t2.ename='mysql') and t3.sid=3;
Empty set (0.00 sec)
```

分析如下

```shell
# not exists中的查询与外表没有连接，则仅仅作为判断真假的依据，因此第二条sql的查询过程是where条件后的判断为假，所以没有结果集返回
# not exists中的查询与外表有连接，则第一步先与外表连接生产一个虚拟表如下：
mysql> select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename='mysql';
+-----+-------+-----+------+
| eid | ename | sid | id   |
+-----+-------+-----+------+
|   1 | mysql |   1 |    1 |
+-----+-------+-----+------+
由于not exists，所以对结果集合取反，即：
mysql> select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename!='mysql';
+-----+--------+-----+------+
| eid | ename  | sid | id   |
+-----+--------+-----+------+
|   2 | oracle |   2 |    1 |
|   3 | redis  |   3 |    2 |
+-----+--------+-----+------+
接下来再与t1表连接，条件是t1.id=t3.id，如下所示
mysql> select * from (select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename!='mysqll')as t4 join t1 on t1.id=t4.id;
+-----+--------+-----+------+----+----------+
| eid | ename  | sid | id   | id | name     |
+-----+--------+-----+------+----+----------+
|   1 | mysql  |   1 |    1 |  1 | superman |
|   2 | oracle |   2 |    1 |  1 | superman |
|   3 | redis  |   3 |    2 |  2 | batman   |
+-----+--------+-----+------+----+----------+
最后从结果集中过滤sid=3的行
mysql> select * from (select t2.eid,t2.ename,t3.sid,t3.id from t2,t3 where t2.eid=t3.eid and t2.ename!='mysqll')as t4 join t1 on t1.id=t4.id  where sid=3;
+-----+-------+-----+------+----+--------+
| eid | ename | sid | id   | id | name   |
+-----+-------+-----+------+----+--------+
|   3 | redis |   3 |    2 |  2 | batman |
+-----+-------+-----+------+----+--------+
```


## 总结

exists()的两种情况
* exists中的查询与外表没有连接，则仅仅作为判断真假的依据
* exists中的查询与外表有连接，则第一步先与外表连接生产一个虚拟表；接下来再与外表其他连接；最后从结果集中过滤

not exists()的两种情况
* exists中的查询与外表没有连接，则仅仅作为判断真假的依据
* exists中的查询与外表有连接，则第一步先与外表连接根据过滤条件取反的一个虚拟表；接下来再与外表其他表连接；最后从结果集中过滤




```shell
# 集合A1
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where not exists(select * from t1 where t1.id=t3.id and t1.id=3);
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+
# 集合A2
select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where not exists(select * from t1 where t1.id=t3.id and t1.id=1);
+-----+------+--------+------+
| sid | id   | name   | eid  |
+-----+------+--------+------+
|   3 |    2 | batman |    3 |
+-----+------+--------+------+
# 集合B
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select * from t2 where t2.eid=t3.eid and t2.ename='mysql') or exists(select * from t1 where t1.id=t3.id and t1.id=1) or exists(select * from t1 where t1.id=t3.id and t1.id=2));
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+
============================
# 集合A1和集合B的交集
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select * from t2 where t2.eid=t3.eid and t2.ename='mysql') or exists(select * from t1 where t1.id=t3.id and t1.id=1) or exists(select * from t1 where t1.id=t3.id and t1.id=2)) and not exists(select * from t1 where t1.id=t3.id and t1.id=3);
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+

# 集合A2和集合B的交集
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select * from t2 where t2.eid=t3.eid and t2.ename='mysql') or exists(select * from t1 where t1.id=t3.id and t1.id=1) or exists(select * from t1 where t1.id=t3.id and t1.id=2)) and not exists(select * from t1 where t1.id=t3.id and t1.id=1);
+-----+------+--------+------+
| sid | id   | name   | eid  |
+-----+------+--------+------+
|   3 |    2 | batman |    3 |
+-----+------+--------+------+
============================================
# 如果 集合B中a,b,c的列不同呢？
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t2.eid from t2 where t2.eid=t3.eid and t2.ename='mysql') or exists(select t1.name from t1 where t1.id=t3.id and t1.id=1) or exists(select t1.id from t1 where t1.id=t3.id and t1.id=2));
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
|   3 |    2 | batman   |    3 |
+-----+------+----------+------+

select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t2.eid from t2 where t2.eid=t3.eid and t2.ename='mysql') )
union
select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t1.name from t1 where t1.id=t3.id and t1.id=1) )
union
select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t1.id from t1 where t1.id=t3.id and t1.id=2) );

mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t2.eid from t2 where t2.eid=t3.eid and t2.ename='mysql') );
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
+-----+------+----------+------+
1 row in set (0.00 sec)

mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select 1 from t2 where t2.eid=t3.eid and t2.ename='mysql') );
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
+-----+------+----------+------+

# 我们发现子查询中select的列不管是写什么都没有影响，永远都是一个包含所有列的结果集
mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t1.name from t1 where t1.id=t3.id and t1.id=1) );
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
+-----+------+----------+------+
2 rows in set (0.00 sec)

mysql> select sid,t3.id,t1.name,t3.eid from t3 join t1 on t1.id=t3.id where (exists(select t1.name from t1 where t1.id=t3.id and t1.id=1 limit 1) );
+-----+------+----------+------+
| sid | id   | name     | eid  |
+-----+------+----------+------+
|   1 |    1 | superman |    1 |
|   2 |    1 | superman |    2 |
+-----+------+----------+------+



```

* exists( 集合a or 集合b or 集合c) 求a，b，c的并集
* exists() and exists() 求集合的交集
* 子查询中select的列不管是什么都没有影响，永远都是一个包含所有列的结果集




































