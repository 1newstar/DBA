# RDS上的binlog分析

> 2017-09-12 BoobooWei

[TOC]

需要在本地linux上安装一下软件

* python2.6 2.7
* MySQLdb模块
* mysql客户端

## 使用场景

多数用户的使用场景都是只需要分析某一个库中的某一个表就可以了，而且客户只会提供一个表的ddl。

## 下载binlog日志到本地

1. 在rds的备份界面通过外网下载到本地
2. 客户下载好钉钉远程传输过来

## 获取具体时间段

根据客户提供的时间段，截取日志，需要在代码中修改，例如booboo.py中的第181行

```shel
ml_str = "mysqlbinlog -vv --base64-output=DECODE-ROWS --start-datetime='2017-09-08 06:00:00' --stop-datetime='2017-09-08 08:00:00' "+ filename + " | awk  '$0~/^###/ || $0~/end_log_pos/ || $0~/BEGIN/ || $0~/COMMIT/ {print $0}' |sed 's/^### //;s@\/\*.*\*\/@@'"
```

指定数据库连接参数

```shell
# 连接mysql需要的变量
url='localhost'
username='root'
password='(Uploo00king)'
dbname='taiping'
```

### 执行脚本

```shell
python booboo.py xxx
```

脚本执行后会在dbname指定的库中新建binlogtosql表来存放分析的binlog记录

### 筛选记录

```shell
select * from binlogtosql where sqlinfo regexp 'xxxx' into outfile '/var/lib/mysql-files/01';
```

将筛选结果导出到文件中

### 转换列名

这一步看情况是否要做

* 根据客户给出的表的ddl，在本地新建该表，然后将列的信息获取存入文件col中

```shell
mysql -u -p taiping -e 'desc binlogtosql' 2> /dev/null|awk '{print $1}' > col
```

* 通过脚本进行转换

```shell
bash a.sh 筛选后的sql文件 存储表的列信息的文件
```

