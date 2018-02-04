# MySQL 在线开启和关闭GTID

> 测试环境为mysql 5.7.18主从同步没有开启gtid模式

```shell
[root@ToBeRoot ~]# mysql --version
mysql  Ver 14.14 Distrib 5.7.18, for Linux (i686) using  EditLine wrapper
```

## 5.6 GTID

从MySQL5.6开始，支持了GTID复制模式，这种模式其实是把双刃剑，虽然容易搭建主从复制了，但使用不当，就容易出现一些错误，例如error 1236。在MySQL5.6如果开启GTID模式，需要在my.cnf中加入以下几个参数：

```shell
log-bin=MySQL-bin
binlog_format=row
log_slave_updates=1
gtid_mode=ON
enforce_gtid_consistency=ON

```

Warning:警告这里的一些参数不是动态参数，也就是需要重启服务才能生效。

## 5.7 GTID

### 在线开

1. 主从都必须执行以下命令

   > 思考主从配置的先后
   >
   > 如果先配置主，主从复制会断开，当从机配置成功后，start slave; 恢复主从
   >
   > 如果先配置从，再配置主，那么主从不受影响。

```shell
set global gtid_mode='OFF_PERMISSIVE';
set global gtid_mode='ON_PERMISSIVE';
set global enforce_gtid_consistency=ON;
set global gtid_mode='ON';
```

2. 主中插入数据，并查看主的状态

```shell
mysql> create database test02;
mysql> show master status;
+------------------+----------+--------------+------------------+----------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                      |
+------------------+----------+--------------+------------------+----------------------------------------+
| mysql-bin.000005 |      154 |              |                  | 82b160c7-9a8f-11e6-8412-000c29c6361d:1 |
+------------------+----------+--------------+------------------+----------------------------------------+
1 row in set (0.00 sec)
```



### 在线关

1. 从机执行以下命令

```shell
stop slave;
set global gtid_mode='ON_PERMISSIVE';
set global gtid_mode='OFF_PERMISSIVE';
CHANGE MASTER TO MASTER_AUTO_POSITION=0;
set global gtid_mode='OFF';
```

2. 主库执行以下命令：

```shell
set global gtid_mode='ON_PERMISSIVE';
set global gtid_mode='OFF_PERMISSIVE';
CHANGE MASTER TO MASTER_AUTO_POSITION=0;
set global gtid_mode='OFF';
```

3. 启动主从

```shell
start slave;
```



