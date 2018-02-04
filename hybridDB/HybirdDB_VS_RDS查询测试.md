# HybirdDB_VS_RDS查询测试

> 2017-11-03 驻云DBA组

## 获取测试数据

```shell
mysqldump -h[ip] -uxxx -pxxx --default-character-set=utf8 --databases vingoo_manage_sys --tables vg_terminal_logs_021_2016 vg_terminal_logs_021_2017 vg_card_info > testdb.sql

[root@ToBeRoot juang]# file testdb.sql 
testdb.sql: UTF-8 Unicode text, with very long lines
```

## RDS测试环境的准备

> RDS For MySQL 5.6 8核32G

```shell
mysql -uzyadmin -pUploo00king -h rm-bp1nix28m50dinb27.mysql.rds.aliyuncs.com juang < testdb.sql
mysql>show table status ;
```


| Name                      | Engine | Rows    | Avg_row_length | Data_length | Index_length |
| :------------------------ | :----- | :------ | :------------- | :---------- | :----------- |
| vg_card_info              | InnoDB | 61810   | 367            | 22740992    | 51445760     |
| vg_terminal_logs_021_2016 | InnoDB | 1965345 | 820            | 1612709888  | 341671936    |
| vg_terminal_logs_021_2017 | InnoDB | 2854918 | 820            | 2341470208  | 558202880    |



##  HybirdDB测试环境准备

> 8核32G 2个节点

```shell
mysql -uzyadmin -pUploo00king -h pub-m-bp18e997b01056b4.petadata.rds.aliyuncs.com juang

CREATE TABLE `vg_card_info` (
  `id_outside` char(50) DEFAULT '' PRIMARY KEY,
  `id_inside` char(50) NOT NULL,
  `brand_id` int(11) DEFAULT '0',
  `id_code` char(50) DEFAULT '' ,
  `id_remark` varchar(50) DEFAULT '',
  `id_weixin` char(50) DEFAULT '',
  `id_alipay` char(50) DEFAULT '',
  `card_value` decimal(11,2) DEFAULT '0.00',
  `card_value_face` decimal(11,2) DEFAULT '0.00',
  `card_type` int(11) DEFAULT '1',
  `card_checkout` int(11) DEFAULT '0',
  `card_recharge` int(11) DEFAULT '0',
  `create_id` int(11) DEFAULT '0',
  `tips` int(11) DEFAULT '0' ,
  `status` int(10) DEFAULT '1',
  `add_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `add_name` varchar(20) DEFAULT NULL,
  `remark` text CHARACTER SET utf8 COLLATE utf8_icelandic_ci,
  `edit_op` varchar(20) DEFAULT NULL,
  `edit_date` varchar(20) DEFAULT NULL,
  KEY `IDX_brand_id` (`brand_id`),
  KEY `IDX_card_type` (`card_type`),
  KEY `IDX_id_inside` (`id_inside`),
  KEY `IDX_id_weixin` (`id_weixin`) USING BTREE
) distribute_key (id_outside) DEFAULT CHARSET=utf8;

CREATE TABLE `vg_terminal_logs_021_2016` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `brand_id` int(11) DEFAULT '0' ,
  `terminal_num` varchar(100) DEFAULT NULL ,
  `address` varchar(100) DEFAULT NULL ,
  `kiosk_time` int DEFAULT NULL,
  `kiosk_info` char(255) DEFAULT NULL,
  `kiosk_initstatus` int(20) DEFAULT '0' ,
  `purchase_way` int(20) DEFAULT '0' ,
  `price` decimal(10,2) DEFAULT '10.00',
  `trade_no` varchar(100) DEFAULT NULL,
  `cash_starting` int(20) DEFAULT '0',
  `cash_prerecieved` int(20) DEFAULT '0',
  `cash_recieved` int(20) DEFAULT '0',
  `card_starting` int(20) DEFAULT '0' ,
  `card_reading` char(255) DEFAULT NULL,
  `card_account` decimal(10,2) DEFAULT '0.00' ,
  `card_preorder` int(11) DEFAULT '0' ,
  `kiosk_temperature` int(11) DEFAULT '0' ,
  `kiosk_humidity` int(11) DEFAULT '0',
  `kiosk_ozone` int(11) DEFAULT '0' ,
  `orange_stock` int(20) DEFAULT '0' ,
  `coins_stock` char(50) DEFAULT '-1' ,
  `upload_date` datetime DEFAULT NULL ,
  UNIQUE KEY `IDX_terminal_num_time` (`terminal_num`,`kiosk_time`) USING BTREE,
  KEY `IDX_brand_id` (`brand_id`),
  KEY `IDX_card_account` (`card_account`),
  KEY `IDX_kiosk_time` (`kiosk_time`),
  KEY `IDX_trade_no` (`trade_no`),
  KEY `IDX_terminal_num_update` (`terminal_num`,`upload_date`),
  KEY `IDX_update` (`upload_date`)
)distribute_key (kiosk_time) DEFAULT CHARSET=utf8 ;



CREATE TABLE `vg_terminal_logs_021_2017` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `brand_id` int(11) DEFAULT '0' ,
  `terminal_num` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `kiosk_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `kiosk_info` char(255) DEFAULT NULL,
  `kiosk_initstatus` int(20) DEFAULT '0' ,
  `purchase_way` int(20) DEFAULT '0' ,
  `price` decimal(10,2) DEFAULT '10.00' ,
  `trade_no` varchar(100) DEFAULT NULL ,
  `cash_starting` int(20) DEFAULT '0' ,
  `cash_prerecieved` int(20) DEFAULT '0' ,
  `cash_recieved` int(20) DEFAULT '0' ,
  `card_starting` int(20) DEFAULT '0' ,
  `card_reading` char(255) DEFAULT NULL,
  `card_account` decimal(10,2) DEFAULT '0.00' ,
  `card_preorder` int(11) DEFAULT '0',
  `kiosk_temperature` int(11) DEFAULT '0' ,
  `kiosk_humidity` int(11) DEFAULT '0' ,
  `kiosk_ozone` int(11) DEFAULT '0' ,
  `orange_stock` int(20) DEFAULT '0' ,
  `coins_stock` char(50) DEFAULT '-1' ,
  `upload_date` int DEFAULT NULL,
  UNIQUE KEY `IDX_terminal_num_time` (`terminal_num`,`kiosk_time`) USING BTREE,
  KEY `IDX_brand_id` (`brand_id`),
    KEY `IDX_card_account` (`card_account`),
  KEY `IDX_kiosk_time` (`kiosk_time`),
  KEY `IDX_trade_no` (`trade_no`),
  KEY `IDX_terminal_num_update` (`terminal_num`,`upload_date`) USING BTREE,
  KEY `IDX_update` (`upload_date`)
) distribute_key (upload_date) DEFAULT CHARSET=utf8 ;
```

**注意事项：**
> ddl规则如链接：https://help.aliyun.com/document_detail/48679.html?spm=5176.product26320.6.561.ilcKkj

1. PRIMARY KEY AUTO_INCREMENT
2. comment只能是英文
3. distribute_key在前
4. ddl语句创建时间消耗在1分钟左右


## 测试过程

> 测试语句经过简化

```shell
select count(id) from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-09-01 00:00:00' and upload_date<='2017-09-30 23:59:59';

select count(*) from (select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2016 as a left join vg_card_info as b on a.card_reading=b.id_outside where kiosk_time >='2016-12-01 00:00:00' and kiosk_time<='2016-12-31 23:59:59'
union 
select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-01-01 00:00:00' and upload_date<='2017-01-31 23:59:59'
) as t1;
```

###  RDS执行时间

```shell
mysql> select count(id) from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-09-01 00:00:00' and upload_date<='2017-09-30 23:59:59';
+-----------+
| count(id) |
+-----------+
|    348626 |
+-----------+
1 row in set (2.79 sec)

mysql> select count(id) from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-09-01 00:00:00' and upload_date<='2017-09-30 23:59:59';
+-----------+
| count(id) |
+-----------+
|    348626 |
+-----------+
1 row in set (2.77 sec)


mysql> select count(*) from (select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2016 as a left join vg_card_info as b on a.card_reading=b.id_outside where kiosk_time >='2016-12-01 00:00:00' and kiosk_time<='2016-12-31 23:59:59'
    -> union 
    -> select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-01-01 00:00:00' and upload_date<='2017-01-31 23:59:59'
    -> ) as t1;
+----------+
| count(*) |
+----------+
|   471910 |
+----------+
1 row in set (9.86 sec)
mysql> select count(*) from (select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2016 as a left join vg_card_info as b on a.card_reading=b.id_outside where kiosk_time >='2016-12-01 00:00:00' and kiosk_time<='2016-12-31 23:59:59' union  select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-01-01 00:00:00' and upload_date<='2017-01-31 23:59:59' ) as t1;
+----------+
| count(*) |
+----------+
|   471910 |
+----------+
1 row in set (9.68 sec)
```

###  HybirdDB测试过程

```shell
mysql> select count(id) from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-09-01 00:00:00' and upload_date<='2017-09-30 23:59:59';
+-----------+
| COUNT(id) |
+-----------+
|         0 |
+-----------+
1 row in set (1.55 sec)

mysql> select count(id) from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-09-01 00:00:00' and upload_date<='2017-09-30 23:59:59';
+-----------+
| COUNT(id) |
+-----------+
|         0 |
+-----------+
1 row in set (0.35 sec)

mysql> select count(*) from (select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2016 as a left join vg_card_info as b on a.card_reading=b.id_outside where kiosk_time >='2016-12-01 00:00:00' and kiosk_time<='2016-12-31 23:59:59'
    -> union 
    -> select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-01-01 00:00:00' and upload_date<='2017-01-31 23:59:59'
    -> ) as t1;
+----------+
| COUNT(*) |
+----------+
|     1786 |
+----------+
1 row in set (2.18 sec)


mysql> select count(*) from (select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2016 as a left join vg_card_info as b on a.card_reading=b.id_outside where kiosk_time >='2016-12-01 00:00:00' and kiosk_time<='2016-12-31 23:59:59' union  select terminal_num,kiosk_initstatus,purchase_way,cash_recieved,card_preorder,kiosk_info,kiosk_time,upload_date,price,b.card_type from vg_terminal_logs_021_2017 as a left join vg_card_info as b on a.card_reading=b.id_outside where upload_date >='2017-01-01 00:00:00' and upload_date<='2017-01-31 23:59:59' ) as t1;
+----------+
| COUNT(*) |
+----------+
|     1786 |
+----------+
1 row in set (0.63 sec)
```

## 测试总结

> 测试前提，相同的配置，相同的数据，相同的索引，相同的测试语句

| 数据库      | SQL1 最大耗时 | SQL1 最小耗时 | SQL2 最大耗时 | SQL2 最小耗时 |
| -------- | --------- | --------- | --------- | --------- |
| RDS      | 2.79 sec  | 2.77 sec  | 9.86 sec  | 9.68 sec  |
| HybirdDB | 1.55 sec  | 0.35sec   | 2.18 sec  | 0.63 sec  |

HybirdDB在本轮测试中占优。
