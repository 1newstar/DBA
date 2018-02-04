#  mysql日期函数应用场景实例

[TOC]



## 需求

BST监控中需要获取近4周的每周事务处理情况，用mysql的sql语句来实现，需要用where进行过滤。

## 分析

需求分析后，可以从以下思路解决：

通过执行查询语句时的当前的系统时间curdate()，来推出近四周的每一周的周一和周日的日期

## 解决方案

| 每一周  |      | sql                                      |
| ---- | ---- | ---------------------------------------- |
| 本周   | 周一   | SELECT date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY); |
|      | 周日   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL 6 DAY); |
| 上一周  | 周一   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -7 day); |
|      | 周日   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -1 day); |
| 上上周  | 周一   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -14 day); |
|      | 周日   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -8 day); |
| 上上上周 | 周一   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -21 day); |
|      | 周日   | SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -15 day); |



* date_add() 日期加减法；例如` 日期-3天` 表示为`date_add(日期,INTERVAL -3 DAY)` 

  - `interval` 为固定的关键字
  - `-3` 是负数3 
  - `DAY`是单位天，还可以是其他单位，具体看官方帮助。

* curdate() 获取当前日期

* weekday() 将日期显示为0-6的数字，规则为周一0 周二1 周三2 周四3 周五4 周六5 周日6

  ​



```shell
[root@ToBeRoot ~]# cat sql
# 相对于执行sql语句的时间
# 本周一
SELECT date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY);
# 本周日
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL 6 DAY);
# 上周一
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -7 day);
# 上周日
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -1 day);
# 上上周一
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -14 day);
# 上上周日
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -8 day);
# 上上上周一
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -21 day);
# 上上上周日
SELECT date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -15 day);

[root@ToBeRoot ~]# booboo < sql
date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY)
2017-06-26
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL 6 DAY)
2017-07-02
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -7 day)
2017-06-19
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -1 day)
2017-06-25
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -14 day)
2017-06-12
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -8 day)
2017-06-18
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -21 day)
2017-06-05
date_add(date_add(CURDATE( ) ,INTERVAL -WEEKDAY( CURDATE( ) ) DAY),INTERVAL -15 day)
2017-06-11

```


