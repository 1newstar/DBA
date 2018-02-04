# 自建MySQL_重置root密码方案

> 2017-10-16 驻云DBA组

## 方案说明

1. 无需重启数据库服务
2. 没有权限修改用户授权和认证
3. 存在低权限账号对某库有读写权限
4. 实现重新设置root密码的功能

## 步骤概览

| 步骤                                   | 负责人   | 备注   |
| ------------------------------------ | ----- | ---- |
| 1. 获取低权限账号A（对某个库db1拥有写权限的账号）         | 由客户提供 |      |
| 2. 获取操作系统root权限                      | 由客户提供 |      |
| 3. 确定实施时间                            | 由客户提供 |      |
| 4. 系统root用户复制认证权限表mysql.user到A账号     | 驻云DBA |      |
| 5. A账号登陆数据库修改db1下的user表中数据库root密码    | 驻云DBA |      |
| 6. 系统root用户备份mysql.user表             | 驻云DBA |      |
| 7. 系统root用户拷贝db1.user表覆盖mysql.user表  | 驻云DBA |      |
| 8. 系统root用户向mysql发送SIGHUP信号重新加载认证授权表 | 驻云DBA |      |
| 9. root用户测试新密码登陆                     | 驻云DBA |      |
| 10. 失败回滚事项——将备份的认证授权表还原              | 驻云DBA |      |

## 测试环境

> 本方案已在测试环境中实现，具体步骤如下

```shell
[root@masterb0 ~]# systemctl start mariadb
[root@masterb0 ~]# mysqladmin -uroot password 123
[root@masterb0 ~]# mysql -uroot -p123 -e "create database db1;"
[root@masterb0 ~]# mysql -uroot -p123 -e "grant all on db1.* to booboo@localhost identified by '123'"
[root@masterb0 ~]# mysql -uroot -p123 -e "flush privileges"
[root@masterb0 ~]# mysql -ubooboo -p123 db1 -e 'select user()';
+------------------+
| user()           |
+------------------+
| booboo@localhost |
+------------------+

# 复制user表到booboo用户可以写的db1库中
[root@masterb0 ~]# cp /var/lib/mysql/mysql/user.* /var/lib/mysql/db1/ -p
[root@masterb0 ~]# ll /var/lib/mysql/db1/user*
-rw-rw----. 1 mysql mysql 10630 Oct 16 13:04 /var/lib/mysql/db1/user.frm
-rw-rw----. 1 mysql mysql   476 Oct 16 13:05 /var/lib/mysql/db1/user.MYD
-rw-rw----. 1 mysql mysql  2048 Oct 16 13:05 /var/lib/mysql/db1/user.MYI
# booboo用户修改db1库中的user表
[root@masterb0 ~]# mysql -ubooboo -p123 db1 -e "update user set password=password('uplooking') where user='root' and host='localhost'";
[root@masterb0 ~]# mysql -ubooboo -p123 -e 'select user,host,password from db1.user'
+--------+----------------------+-------------------------------------------+
| user   | host                 | password                                  |
+--------+----------------------+-------------------------------------------+
| root   | localhost            | *6FF883623B8639D08083FF411D20E6856EB7D2BF |
| root   | masterb0.example.com |                                           |
| root   | 127.0.0.1            |                                           |
| root   | ::1                  |                                           |
|        | localhost            |                                           |
|        | masterb0.example.com |                                           |
| booboo | localhost            | *23AE809DDACAF96AF0FD78ED04B6A265E05AA257 |
+--------+----------------------+-------------------------------------------+
# 为了测试效果，使用root查看
[root@masterb0 ~]# mysql -ubooboo -p123 -e 'select user,host,password from mysql.user'
ERROR 1142 (42000) at line 1: SELECT command denied to user 'booboo'@'localhost' for table 'user'
[root@masterb0 ~]# mysql -uroot -p123 -e 'select user,host,password from mysql.user'
+--------+----------------------+-------------------------------------------+
| user   | host                 | password                                  |
+--------+----------------------+-------------------------------------------+
| root   | localhost            | *23AE809DDACAF96AF0FD78ED04B6A265E05AA257 |
| root   | masterb0.example.com |                                           |
| root   | 127.0.0.1            |                                           |
| root   | ::1                  |                                           |
|        | localhost            |                                           |
|        | masterb0.example.com |                                           |
| booboo | localhost            | *23AE809DDACAF96AF0FD78ED04B6A265E05AA257 |
+--------+----------------------+-------------------------------------------+
# 将booboo库中的user表数据拷贝到mysql库中
[root@masterb0 ~]# cp /var/lib/mysql/mysql/user.MYD /var/lib/mysql/mysql/user.MYD.bac
[root@masterb0 ~]# cp -p /var/lib/mysql/db1/user.MYD /var/lib/mysql/mysql
cp: overwrite ‘/var/lib/mysql/mysql/user.MYD’? y

[root@masterb0 ~]# mysql -uroot -p123 -e 'select user,host,password from mysql.user'
+--------+----------------------+-------------------------------------------+
| user   | host                 | password                                  |
+--------+----------------------+-------------------------------------------+
| root   | localhost            | *6FF883623B8639D08083FF411D20E6856EB7D2BF |
| root   | masterb0.example.com |                                           |
| root   | 127.0.0.1            |                                           |
| root   | ::1                  |                                           |
|        | localhost            |                                           |
|        | masterb0.example.com |                                           |
| booboo | localhost            | *23AE809DDACAF96AF0FD78ED04B6A265E05AA257 |
+--------+----------------------+-------------------------------------------+
[root@masterb0 ~]# mysql -uroot -puplooking
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
[root@masterb0 ~]# mysql -ubooboo -p123 -e "flush privileges"
ERROR 1227 (42000) at line 1: Access denied; you need (at least one of) the RELOAD privilege(s) for this operation
# reload数据库
[root@masterb0 ~]# pgrep -n mysql
14344
[root@masterb0 ~]# kill -SIGHUP 14344
[root@masterb0 ~]# mysql -uroot -puplooking 
```

