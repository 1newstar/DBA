# MySQL replicate-ignore-db详解

官方的解释是：在主从同步的环境中，replicate-ignore-db用来设置不需要同步的库。解释的太简单了，但是里面还有很多坑呢。

生产库上不建议设置过滤规则。如果非要设置，那就用Replicate_Wild_Ignore_Table: mysql.%吧。实验的很简单，如下

```shell
第一种情况
从库：
replicate-ignore-db = mysql
主库：
use mysql
CREATE TABLE test.testrepl1(
id int(5))ENGINE=INNODB DEFAULT CHARSET=UTF8;
从库不会同步。坑
 
第二种情况
从库：
replicate-ignore-db = mysql
 
主库：
use test
CREATE TABLE mysql.testrepl2(
id int(5))ENGINE=INNODB DEFAULT CHARSET=UTF8;
从库不会同步。
 
 
第三种情况
use test
update mysql.user set user = 'testuser5' where user = 'testuser1';
从库会同步
 
第四种情况
grant all on *.* to testnowild@'%' identified by 'ge0513.hudie';
从库会同步
 
第二大类：
Replicate_Wild_Ignore_Table: mysql.%
 
第五种情况
主库：
use test
update mysql.user set user = 'testuser1' where user = 'testuser5';
从库没有同步。
 
第六种情况
主库：
grant all on *.* to testwild@'%' identified by 'ge0513.hudie';
从库没有同步。
```
	replicate_wild_do_table=fireway.%
	replicate_wild_do_table=finance.%
	replicate_wild_ignore_table=mysql.%
	replicate_wild_ignore_table=edw.%
	replicate_wild_ignore_table=etl2020.%