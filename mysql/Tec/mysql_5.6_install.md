# mySQL-5.6.20-二进制安装

[TOC]

> 之前一直是用rpm包直接安装，今天用二进制包解压安装（不需要源码编译），在学会安装的基础上，写出shell自动化安装脚本

| server  | ip          |
| :------ | :---------- |
| mastera | 172.25.0.11 |
| masterb | 172.25.0.12 |

## 安装二进制的mysql5.6

事先规划好数据目录，binlog，pid，临时目录等路径

| mysql    | 软件架构                 |
| :------- | :------------------- |
| 数据目录     | /data/mysql/data     |
| binlog目录 | /data/mysql/log-data |
| pid文件    | /data/tmp            |
| 临时目录     | /data1/tmp/          |

以上目录所属者和所属组都需要为mysql.mysql

## 详细步骤

```shell	
[root@mastera0 ~]# tar -xf mysql-5.6.20-linux-glibc2.5-x86_64.tar.gz 
[root@mastera0 ~]# cd mysql-5.6.20-linux-glibc2.5-x86_64
[root@mastera0 mysql-5.6.20-linux-glibc2.5-x86_64]# ls
bin  COPYING  data  docs  include  INSTALL-BINARY  lib  man  mysql-test  README  scripts  share  sql-bench  support-files
[root@mastera0 mysql-5.6.20-linux-glibc2.5-x86_64]# cat INSTALL-BINARY
... ...
 To install and use a MySQL binary distribution, the basic command
   sequence looks like this:
shell> groupadd mysql
shell> useradd -r -g mysql mysql
shell> cd /usr/local
shell> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
shell> ln -s full-path-to-mysql-VERSION-OS mysql
shell> cd mysql
shell> chown -R mysql .
shell> chgrp -R mysql .
shell> scripts/mysql_install_db --user=mysql
shell> chown -R root .
shell> chown -R mysql data
shell> bin/mysqld_safe --user=mysql &
# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server
... ...

[root@mastera0 mysql-5.6.20-linux-glibc2.5-x86_64]# groupadd mysql
[root@mastera0 mysql-5.6.20-linux-glibc2.5-x86_64]# cd ..
[root@mastera0 ~]# useradd -r -g mysql mysql
[root@mastera0 ~]# cd /usr/local
[root@mastera0 local]# mv /root/mysql-5.6.20-linux-glibc2.5-x86_64 .
[root@mastera0 local]# ls
bin  games    lib    libexec                             sbin   src
etc  include  lib64  mysql-5.6.20-linux-glibc2.5-x86_64  share
[root@mastera0 local]# ln -s mysql-5.6.20-linux-glibc2.5-x86_64 mysql
[root@mastera0 local]# ll mysql
lrwxrwxrwx.  1 root root   34 Dec 11 12:20 mysql -> mysql-5.6.20-linux-glibc2.5-x86_64
[root@mastera0 mysql]# cd mysql
[root@mastera0 mysql]# mkdir /data/mysql/data -p
[root@mastera0 mysql]# chown mysql. /data/mysql/data
[root@mastera0 mysql]# chown mysql. /data/mysql/data -R
[root@mastera0 mysql]# ll -d /data/mysql/data
drwxr-xr-x. 2 mysql mysql 4096 Dec 11 12:24 /data/mysql/data
[root@mastera0 mysql]# scripts/mysql_install_db --user=mysql --datadir=/data/mysql/data --basedir=/usr/local/mysql

[root@mastera0 mysql]# ll /data/mysql/data
total 110604
-rw-rw----. 1 mysql mysql 12582912 Dec 11 12:28 ibdata1
-rw-rw----. 1 mysql mysql 50331648 Dec 11 12:28 ib_logfile0
-rw-rw----. 1 mysql mysql 50331648 Dec 11 12:28 ib_logfile1
drwx------. 2 mysql mysql     4096 Dec 11 12:28 mysql
drwx------. 2 mysql mysql     4096 Dec 11 12:28 performance_schema
drwx------. 2 mysql mysql     4096 Dec 11 12:28 test
[root@mastera0 mysql]# cp /mnt/mysql/my.cnf /etc/my.cnf
[root@mastera0 mysql]# vim /etc/my.cnf
[client]
#如果不认识这个参数会忽略
loose-default-character-set=utf8
loose-prompt='\u@\h:\p [\d]>'
socket=/tmp/mysql.sock

[mysqld]
basedir = /usr/local/mysql
datadir = /data/mysql/data
user=mysql
port = 3306
socket=/tmp/mysql.sock
pid-file=/data/tmp/mysql.pid
tmpdir=/data1/tmp
character_set_server=utf8

#skip
skip-external_locking=1
skip-name-resolve=1

#AB replication
server-id = 1
log-bin = /data/mysql/log-data/mastera
binlog_format=row
max_binlog_cache_size=2000M
max_binlog_size=1G
sync_binlog=1
#expire_logs_days=7

#semi_sync
#rpl_semi_sync_master_enabled=1
#rpl_semi_sync_master_timeout=1000


[root@mastera0 mysql]# pwd
/usr/local/mysql
[root@mastera0 mysql]# cp support-files/mysql.server /etc/init.d/mysql.server
[root@mastera0 mysql]# echo export PATH=$PATH:/usr/local/mysql/support-files/ >> /etc/bashrc
```

同样去安装masterb slavea

## 脚本实现自动安装MySQL

如果需要同时安装10台甚至1000台，通过脚本来完成一定是极好的！

```shell
#!/bin/bash

# auto_install_mysql_5.6.20 

# 参数设置
# --binpos=指定mysql二进制安装包的位置
# --basedir=指定mysql安装位置
# --datadir=指定mysql数据存放位置
# --binlogdir=指定mysqlbinlog存放位置
# --piddir=指定mysql进程存放位置
# --tmpdir=指定mysql临时文件位置
# --help 查看帮助

# eg. auto_install_mysql_5.6.20 --binpos=/tmp/mysql.tar.gz --datadir=/data/mysql/data --basedir=/usr/local/mysql

# 遍历位置参数，获取对应的参数值
for i in ${@}
do
	case ${i%=*} in 
	--binpos)
			binpos=${i#*=};;
	--basedir)
			basedir=${i#*=};;
	--datadir)
			datadir=${i#*=};;
	--binlogdir)
			binlogdir=${i#*=};;
	--piddir)
			piddir=${i#*=};;
	--tmpdir)
			tmpdir=${i#*=};;
	esac
done

TAR(){
# 解压mysql二进制安装包到指定mysql安装位置
tar -xf $binpos -C /tmp &> /dev/null
rpm=${binpos##*/}
rm -r $basedir 
mkdir $basedir -p 
mv /tmp/${rpm%.tar.gz}/* $basedir
}

ADD_user_dir(){
# 创建mysql用户和组
# 创建数据目录，二进制日志存放路径，临时目录，pid目录
useradd mysql &> /dev/null 
for i in $datadir $binlogdir $piddir $tmpdir;do
	rm -r $i
	mkdir $i -p &> /dev/null 
	chown -R mysql:mysql $i
done
}

INIT(){
# 通过脚本生成初始化数据
$basedir/scripts/mysql_install_db --user=mysql --datadir=$datadir --basedir=$basedir
}

CONF(){
# 获取服务器IP地址的主机位，用作server-id的值
serverid=`ifconfig|grep -A 1 eno|tail -n 1|awk '{print $2}'|awk -F '.' '{print $4}'`

cat > /etc/my.cnf << ENDF
[client]
#如果不认识这个参数会忽略
loose-default-character-set=utf8
loose-prompt='\u@\h:\p [\d]>'
socket=/tmp/mysql.sock

[mysqld]
basedir = $basedir
datadir = $datadir
user=mysql
port = 3306
socket=/tmp/mysql.sock
pid-file=$piddir/mysql.pid
tmpdir=$tmpdir
character_set_server=utf8


#skip
skip-external_locking=1
skip-name-resolve=1

#AB replication
server-id = $serverid
log-bin = $binlogdir/`hostname|awk -F . '{print $1}'`
binlog_format=row
max_binlog_cache_size=2000M
max_binlog_size=1G
sync_binlog=1
#expire_logs_days=7

#semi_sync
#rpl_semi_sync_master_enabled=1
#rpl_semi_sync_master_timeout=1000
ENDF

# 将数据库服务启动脚本复制到/etc/init.d/
cp $basedir/support-files/mysql.server /etc/init.d/mysql

# 修改PATH路径，将mysql相关命令所在目录加入
echo export PATH=$PATH:$basedir/bin/ >> /etc/bashrc
source /etc/bashrc
}

Main(){
TAR 
ADD_user_dir 
INIT 
CONF 
}

Main

```

将脚本和mysql二进制安装文件复制到masterb，并执行脚本，实现自动安装

```shell
[root@masterb ~]# ./auto_install_mysql_5.6.20.sh --binpos=/software/mysql-5.6.20-linux-glibc2.5-x86_64.tar.gz --basedir=/usr/local/mysql --datadir=/data/mysql/data --binlogdir=/data/mysql/binlog --piddir=/data/mysql/pid --tmpdir=/data/mysql/tmp
rm: cannot remove ‘/usr/local/mysql’: No such file or directory
rm: cannot remove ‘/data/mysql/data’: No such file or directory
rm: cannot remove ‘/data/mysql/binlog’: No such file or directory
rm: cannot remove ‘/data/mysql/pid’: No such file or directory
rm: cannot remove ‘/data/mysql/tmp’: No such file or directory
WARNING: The host 'masterb.uplooking.com' could not be looked up with /usr/local/mysql/bin/resolveip.
This probably means that your libc libraries are not 100 % compatible
with this binary MySQL version. The MySQL daemon, mysqld, should work
normally with the exception that host name resolving will not work.
This means that you should use IP addresses instead of hostnames
when specifying MySQL privileges !

Installing MySQL system tables...2017-02-23 14:57:25 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-02-23 14:57:26 2836 [Note] InnoDB: Using atomics to ref count buffer pool pages
2017-02-23 14:57:26 2836 [Note] InnoDB: The InnoDB memory heap is disabled
2017-02-23 14:57:26 2836 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2017-02-23 14:57:26 2836 [Note] InnoDB: Memory barrier is not used
2017-02-23 14:57:26 2836 [Note] InnoDB: Compressed tables use zlib 1.2.3
2017-02-23 14:57:26 2836 [Note] InnoDB: Using Linux native AIO
2017-02-23 14:57:26 2836 [Note] InnoDB: Not using CPU crc32 instructions
2017-02-23 14:57:26 2836 [Note] InnoDB: Initializing buffer pool, size = 128.0M
2017-02-23 14:57:26 2836 [Note] InnoDB: Completed initialization of buffer pool
2017-02-23 14:57:26 2836 [Note] InnoDB: The first specified data file ./ibdata1 did not exist: a new database to be created!
2017-02-23 14:57:26 2836 [Note] InnoDB: Setting file ./ibdata1 size to 12 MB
2017-02-23 14:57:26 2836 [Note] InnoDB: Database physically writes the file full: wait...
2017-02-23 14:57:26 2836 [Note] InnoDB: Setting log file ./ib_logfile101 size to 48 MB
2017-02-23 14:57:29 2836 [Note] InnoDB: Setting log file ./ib_logfile1 size to 48 MB
2017-02-23 14:57:31 2836 [Note] InnoDB: Renaming log file ./ib_logfile101 to ./ib_logfile0
2017-02-23 14:57:31 2836 [Warning] InnoDB: New log files created, LSN=45781
2017-02-23 14:57:31 2836 [Note] InnoDB: Doublewrite buffer not found: creating new
2017-02-23 14:57:31 2836 [Note] InnoDB: Doublewrite buffer created
2017-02-23 14:57:31 2836 [Note] InnoDB: 128 rollback segment(s) are active.
2017-02-23 14:57:31 2836 [Warning] InnoDB: Creating foreign key constraint system tables.
2017-02-23 14:57:31 2836 [Note] InnoDB: Foreign key constraint system tables created
2017-02-23 14:57:31 2836 [Note] InnoDB: Creating tablespace and datafile system tables.
2017-02-23 14:57:31 2836 [Note] InnoDB: Tablespace and datafile system tables created.
2017-02-23 14:57:31 2836 [Note] InnoDB: Waiting for purge to start
2017-02-23 14:57:31 2836 [Note] InnoDB: 5.6.20 started; log sequence number 0
2017-02-23 14:57:31 2836 [Note] Binlog end
2017-02-23 14:57:31 2836 [Note] InnoDB: FTS optimize thread exiting.
2017-02-23 14:57:32 2836 [Note] InnoDB: Starting shutdown...
2017-02-23 14:57:33 2836 [Note] InnoDB: Shutdown completed; log sequence number 1625977
OK

Filling help tables...2017-02-23 14:57:33 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-02-23 14:57:33 2858 [Note] InnoDB: Using atomics to ref count buffer pool pages
2017-02-23 14:57:33 2858 [Note] InnoDB: The InnoDB memory heap is disabled
2017-02-23 14:57:33 2858 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2017-02-23 14:57:33 2858 [Note] InnoDB: Memory barrier is not used
2017-02-23 14:57:33 2858 [Note] InnoDB: Compressed tables use zlib 1.2.3
2017-02-23 14:57:33 2858 [Note] InnoDB: Using Linux native AIO
2017-02-23 14:57:33 2858 [Note] InnoDB: Not using CPU crc32 instructions
2017-02-23 14:57:33 2858 [Note] InnoDB: Initializing buffer pool, size = 128.0M
2017-02-23 14:57:34 2858 [Note] InnoDB: Completed initialization of buffer pool
2017-02-23 14:57:34 2858 [Note] InnoDB: Highest supported file format is Barracuda.
2017-02-23 14:57:34 2858 [Note] InnoDB: 128 rollback segment(s) are active.
2017-02-23 14:57:34 2858 [Note] InnoDB: Waiting for purge to start
2017-02-23 14:57:34 2858 [Note] InnoDB: 5.6.20 started; log sequence number 1625977
2017-02-23 14:57:34 2858 [Note] Binlog end
2017-02-23 14:57:34 2858 [Note] InnoDB: FTS optimize thread exiting.
2017-02-23 14:57:34 2858 [Note] InnoDB: Starting shutdown...
2017-02-23 14:57:36 2858 [Note] InnoDB: Shutdown completed; log sequence number 1625987
OK

To start mysqld at boot time you have to copy
support-files/mysql.server to the right place for your system

PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
To do so, start the server, then issue the following commands:

  /usr/local/mysql/bin/mysqladmin -u root password 'new-password'
  /usr/local/mysql/bin/mysqladmin -u root -h masterb.uplooking.com password 'new-password'

Alternatively you can run:

  /usr/local/mysql/bin/mysql_secure_installation

which will also give you the option of removing the test
databases and anonymous user created by default.  This is
strongly recommended for production servers.

See the manual for more instructions.

You can start the MySQL daemon with:

  cd . ; /usr/local/mysql/bin/mysqld_safe &

You can test the MySQL daemon with mysql-test-run.pl

  cd mysql-test ; perl mysql-test-run.pl

Please report any problems at http://bugs.mysql.com/

The latest information about MySQL is available on the web at

  http://www.mysql.com

Support MySQL by buying support/licenses at http://shop.mysql.com

New default config file was created as /usr/local/mysql/my.cnf and
will be used by default by the server when you start it.
You may edit this file to change server settings
[root@masterb ~]# ll /data/mysql
total 0
drwxr-xr-x. 2 mysql mysql   6 Feb 23 14:57 binlog
drwxr-xr-x. 5 mysql mysql 104 Feb 23 14:57 data
drwxr-xr-x. 2 mysql mysql   6 Feb 23 14:57 pid
drwxr-xr-x. 2 mysql mysql   6 Feb 23 14:57 tmp
[root@masterb ~]# ll /data/mysql/data
total 110600
-rw-rw----. 1 mysql mysql 12582912 Feb 23 14:57 ibdata1
-rw-rw----. 1 mysql mysql 50331648 Feb 23 14:57 ib_logfile0
-rw-rw----. 1 mysql mysql 50331648 Feb 23 14:57 ib_logfile1
drwx------. 2 mysql mysql     4096 Feb 23 14:57 mysql
drwx------. 2 mysql mysql     4096 Feb 23 14:57 performance_schema
drwx------. 2 mysql mysql        6 Feb 23 14:57 test
[root@masterb ~]# ll /data/mysql/binlog
total 0
[root@masterb ~]# ll /data/mysql/pid
total 0
[root@masterb ~]# ll /data/mysql/tmp
total 0
[root@masterb ~]# cat /etc/my.cnf
[client]
#如果不认识这个参数会忽略
loose-default-character-set=utf8
loose-prompt='\u@\h:\p [\d]>'
socket=/tmp/mysql.sock

[mysqld]
basedir = /usr/local/mysql
datadir = /data/mysql/data
user=mysql
port = 3306
socket=/tmp/mysql.sock
pid-file=/data/mysql/pid/mysql.pid
tmpdir=/data/mysql/tmp
character_set_server=utf8


#skip
skip-external_locking=1
skip-name-resolve=1

#AB replication
server-id = 12
log-bin = /data/mysql/binlog/masterb
binlog_format=row
max_binlog_cache_size=2000M
max_binlog_size=1G
sync_binlog=1
#expire_logs_days=7

#semi_sync
#rpl_semi_sync_master_enabled=1
#rpl_semi_sync_master_timeout=1000

[root@masterb ~]# service mysql start
Starting MySQL.............. SUCCESS! 
```


## 总结

相对于rpm包安装，二进制安装稍复杂一点，但只需要实现规划好basedir、datadir、binlogdir、tmpdir等路径即可

另需要注意给mysql使用的相关目录的权限为mysql:mysql

还有就是，如果已经安装过其他版本的数据库，记得卸载干净了。


## 拓展

试着安装5.7.17和8.0版本


5.6的初始化脚本与5.7存放位置不同，并且从5.7开始不建议使用mysql_install_db，而是使用: mysqld --initialize

`$basedir/bin/mysql_install_db`

```shell
[root@mastera mysql]# /usr/local/mysql/bin/mysql_install_db --user=mysql --datadir=/data/mysql/data --basedir=/usr/local/mysql
2017-02-23 17:13:55 [WARNING] mysql_install_db is deprecated. Please consider switching to mysqld --initialize
```

在默认初始化后，记得将目录权限修改，此处我没有另外去指定数据目录，而是使用默认配置，都放在basedir中

```shell
[root@mastera data]# mysqld --initialize
2017-02-23T09:25:26.955095Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-02-23T09:25:29.898671Z 0 [Warning] InnoDB: New log files created, LSN=45790
2017-02-23T09:25:30.432274Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2017-02-23T09:25:30.651188Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 0516b717-f9aa-11e6-a392-000c29a023bc.
2017-02-23T09:25:30.690310Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2017-02-23T09:25:30.720824Z 1 [Note] A temporary password is generated for root@localhost: o2O<!d)Tkjyu

[root@mastera mysql]# ll  /usr/local/mysql
total 48
drwxr-xr-x.  2 mysql mysql  4096 Feb 23 15:49 bin
-rw-r--r--.  1 mysql mysql 17987 Nov 28 21:32 COPYING
drwxr-x---.  5 root  root   4096 Feb 23 17:28 data
drwxr-xr-x.  2 mysql mysql    52 Feb 23 15:49 docs
drwxr-xr-x.  3 mysql mysql  4096 Feb 23 15:48 include
drwxr-xr-x.  5 mysql mysql  4096 Feb 23 15:49 lib
drwxr-xr-x.  4 mysql mysql    28 Feb 23 15:48 man
-rw-r--r--.  1 mysql mysql  2478 Nov 28 21:32 README
drwxr-xr-x. 28 mysql mysql  4096 Feb 23 15:49 share
drwxr-xr-x.  2 mysql mysql  4096 Feb 23 17:04 support-files
[root@mastera mysql]# chown mysql. /usr/local/mysql -R
[root@mastera mysql]# service mysql start
Starting MySQL...Logging to '/usr/local/mysql/data/mastera.uplooking.com.err'.
......... SUCCESS! 
```

5.7之后初始化状态有密码，需要修改后才可使用

```shell
[root@mastera mysql]# mysqladmin -uroot -p'o2O<!d)Tkjyu' password '(Uploo00king)'
mysqladmin: [Warning] Using a password on the command line interface can be insecure.
Warning: Since password will be sent to server in plain text, use ssl connection to ensure password safety.
[root@mastera mysql]# mysql -uroot -p'(Uploo00king)' -e "show databases"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```
