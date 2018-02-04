# MySQL-Monitor-Zabbix

[TOC]

> 监控后端两台数据库服务器

| server      | ip          | OS      | software     | role                 |
| :---------- | :---------- | :------ | :----------- | :------------------- |
| mastera     | 172.25.0.11 | rhel7.2 | mysql 5.7.17 | zabbix 客户端           |
| masterb     | 172.25.0.12 | rhel7.2 | mysql 8.0.0  | zabbix 客户端           |
| workstation | 172.25.0.10 | rhel7.2 | zabbix 3.0.4 | web服务器、zabbix服务器、数据库 |

## 安装软件

### 解决依赖关系

| Pre-requisite                            | Minimum                                  | value Description                        |
| :--------------------------------------- | :--------------------------------------- | :--------------------------------------- |
| PHP version                              | 5.4.0                                    |                                          |
| PHP memory_limit option                  | 128MB                                    | In php.ini:memory_limit = 128M           |
| PHP post_max_size option                 | 16MB                                     | In php.ini:post_max_size = 16M           |
| PHP upload_max_filesize option           | 2MB                                      | In php.ini:upload_max_filesize = 2M      |
| PHP max_execution_time option            | 300 seconds                              | (values 0 and -1 are allowed)            |
| PHP max_input_time option                | 300 seconds (values 0 and -1 are allowed) | In php.ini:max_input_time = 300          |
| PHP session.auto_start option            | must be disabled                         | In php.ini:session.auto_start = 0        |
| Database support                         | One of: IBM DB2, MySQL, Oracle, PostgreSQL, SQLite | One of the following modules must be installed:ibm_db2, mysql, oci8, pgsql, sqlite3 |
| bcmath                                   |                                          | php-bcmath                               |
| mbstring                                 |                                          | php-mbstring                             |
| PHP mbstring.func_overload option        | must be disabled                         | In php.ini:mbstring.func_overload = 0    |
| PHP always_populate_raw_post_data option | must be disabled                         | Required only for PHP versions 5.6.0 or newer. |
| sockets                                  |                                          | php-net-socket. Required for user script support. |
| gd                                       | 2.0 or higher                            | php-gd. PHP GD extension must support PNG images (--with-png-dir), JPEG (--with-jpeg-dir) images and FreeType 2 (--with-freetype-dir). |
| libxml                                   | 2.6.15                                   | php-xml or php5-dom                      |
| xmlwriter                                |                                          | php-xmlwriter                            |
| xmlreader                                |                                          | php-xmlreader                            |
| ctype                                    |                                          | php-ctype                                |
| session                                  |                                          | php-session                              |
| gettext                                  |                                          | php-gettext Since Zabbix 2.2.1, the PHP gettext extension is not a mandatory requirement for installing Zabbix. If gettext is not installed, the frontend will work as usual, however, the translations will not be available. |

根据上表安装需要的依赖包，注意版本,并进行相应设置，以及下面`[]`表示ini中的默认配置值


```shell
yum install -y httpd mariadb-server php php-mysql php-bcmath php-mbstring php-gd php-xml php-xmlwriter php-xmlreader  php-ctype php-session php-gettext

vim /etc/php.ini
memory_limit = 128M
post_max_size = 16M [8M]
upload_max_filesize = 2M
max_execution_time = 300 [30]
max_input_time = 300 [60]
session.auto_start = 0
mbstring.func_overload = 0
# always_populate_raw_post_data参数只有在 PHP versions 5.6.0 以上需要设置为 -1 
# always_populate_raw_post_data = -1 



```

安装软件,有些软件是本地yum源中没有的:

- [ ] `php-bcmath`
- [ ] `php-mbstring` 
- [ ] `php-net-socket`

```shell
[root@workstation zabbix-3.0.4]# yum install -y httpd mariadb-server php php-mysql php-bcmath php-mbstring php-gd php-xml php-xmlwriter php-xmlreader  php-ctype php-session php-gettext
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Package httpd-2.4.6-40.el7.x86_64 already installed and latest version
Package 1:mariadb-server-5.5.44-2.el7.x86_64 already installed and latest version
Package php-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-mysql-5.4.16-36.el7_1.x86_64 already installed and latest version
No package php-bcmath available.
No package php-mbstring available.
Package php-gd-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-xml-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-xml-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-xml-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-common-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-common-5.4.16-36.el7_1.x86_64 already installed and latest version
Package php-common-5.4.16-36.el7_1.x86_64 already installed and latest version
Nothing to do

[root@workstation zabbix-3.0.4]# ls /software/monitor/
graylog-2.2.1.tgz                  php-bcmath-5.4.16-36.el7_1.x86_64.rpm    zabbix-3.0.4
graylog-2.2-repository_latest.rpm  php-mbstring-5.4.16-36.el7_1.x86_64.rpm  zabbix-3.0.4.tar.gz
[root@workstation zabbix-3.0.4]# rpm -ivh /software/monitor/php-bcmath-5.4.16-36.el7_1.x86_64.rpm /software/monitor/php-mbstring-5.4.16-36.el7_1.x86_64.rpm 
warning: /software/monitor/php-bcmath-5.4.16-36.el7_1.x86_64.rpm: Header V4 DSA/SHA1 Signature, key ID 192a7d7d: NOKEY
warning: /software/monitor/php-mbstring-5.4.16-36.el7_1.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:php-mbstring-5.4.16-36.el7_1     ################################# [ 50%]
   2:php-bcmath-5.4.16-36.el7_1       ################################# [100%]

# 观察当前php配置文件的参数设置情况,并修改
[root@workstation ~]# grep -v '^#' /etc/php.ini | grep -v '^$'| grep -v '^;'
[root@workstation zabbix-3.0.4]# sed -i 's@post_max_size.*@post_max_size = 16M@g' /etc/php.ini
[root@workstation zabbix-3.0.4]# sed -i 's@max_input_time.*@max_input_time = 300M@g' /etc/php.ini|grep max_input_time
[root@workstation zabbix-3.0.4]# sed -i 's@max_execution_time.*@max_execution_time = 300@g' /etc/php.ini
[root@workstation zabbix-3.0.4]# sed -i 's@;mbstring.func_overload@mbstring.func_overload@g' /etc/php.ini
[root@workstation zabbix-3.0.4]# sed -n '/post_max_size/p;/max_execution_time/p;/max_input_time/p' /etc/php.ini
; max_input_time
max_execution_time = 300
max_input_time = 300M
post_max_size = 16M

```

### 安装 zabbix server/agent

> #### 1 下载源码

下载地址:	http://www.zabbix.com/download

```shell
[root@workstation ~]# tar -xf /software/monitor/zabbix-3.0.4.tar.gz -C /opt
```

> #### 2 编译源码

编译之前，需要确认：

- [ ] 服务端和客户端在同一台机器上
- [ ] 仅是服务端
- [ ] 仅是客户端
- [ ] 仅是代理端

```shell
# 服务端和客户端在同一台机器上
./configure --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2

# 仅是服务端
./configure --enable-server --with-mysql --with-net-snmp

# 仅是客户端
./configure --enable-agent

# ./configure --prefix=/usr --enable-proxy --with-net-snmp --with-sqlite3 --with-ssh2
```

还以通过`--prefix=/home/zabbix`指定安装路径

> #### 3 安装

Running make install will by default install the daemon binaries (zabbix_server, zabbix_agentd,zabbix_proxy) in /usr/local/sbin and the client binaries (zabbix_get, zabbix_sender) in /usr/local/bin.

```shell
[root@workstation ~]# cd /opt/zabbix-3.0.4
[root@workstation zabbix-3.0.4]# ./configure --prefix=/usr/local/mysql --enable-server --with-mysql=/usr/bin/mysql_config --with-net-snmp
[root@workstation zabbix-3.0.4]# make install
[root@workstation zabbix-3.0.4]# ll /usr/local/zabbix/
total 0
drwxr-xr-x. 3 root root 58 Feb 24 15:08 etc
drwxr-xr-x. 2 root root  6 Feb 24 15:08 lib
drwxr-xr-x. 2 root root 26 Feb 24 15:08 sbin
drwxr-xr-x. 4 root root 29 Feb 24 15:08 share
```

### 安装 zabbix web

> #### 复制php文件

```shell
mkdir <htdocs>/zabbix
cd frontends/php
cp -a . <htdocs>/zabbix
```


## 修改配置并启动服务

### 配置数据库

数据文件存放在database中，需要注意导入顺序

```shell
# 数据库需要新建数据库供zabbix使用
[root@workstation ~]# systemctl start mariadb
[root@workstation ~]# systemctl enable mariadb
[root@workstation ~]# mysqladmin -uroot password 'uplooking'
[root@workstation ~]# mysql -uroot -puplooking -e 'create database zabbix default charset utf8'
[root@workstation ~]# mysql -uroot -puplooking -e "grant all on zabbix.* to zabbix@localhost identified by 'uplooking'"
[root@workstation ~]# mysql -uroot -puplooking  zabbix < /usr/local/zabbix/database/mysql/schema.sql 
[root@workstation ~]# mysql -uroot -puplooking  zabbix < /usr/local/zabbix/database/mysql/images.sql 
[root@workstation ~]# mysql -uroot -puplooking  zabbix < /usr/local/zabbix/database/mysql/data.sql
```


### 配置zabbix server

* Zabbix server configuration file /usr/local/zabbix/etc/zabbix_server.conf

#### 创建用户账户

server端用户和agent端用户最好不要用一个名字，为了安全。

```shell
[root@workstation ~]# groupadd -g 201 zabbix
[root@workstation ~]# useradd -g zabbix -u 201 zabbix -s /sbin/nologin
[root@workstation ~]# id zabbix
uid=201(zabbix) gid=201(zabbix) groups=201(zabbix)
```

#### 创建链接

为了方便使用，可以设置一个软连接到对应的目录

```shell
[root@workstation zabbix-3.0.4]# ln -s /usr/local/zabbix/etc /etc/zabbix
[root@workstation zabbix-3.0.4]# ln -s /usr/local/zabbix/sbin/* /usr/sbin/
[root@workstation zabbix-3.0.4]# mkdir /var/log/zabbix
[root@workstation zabbix-3.0.4]# chown zabbix. /var/log/zabbix
[root@workstation zabbix-3.0.4]# cp /opt/zabbix-3.0.4/misc/init.d/fedora/core/zabbix_server /etc/init.d
```

#### 修改服务启动脚本

```shell
[root@workstation zabbix-3.0.4]# sed -i 's@BASEDIR=/usr/local@BASEDIR=/usr/local/zabbix@g' /etc/init.d/zabbix_server
```

#### 修改配置文件

```shell
[root@workstation zabbix-3.0.4]# sed -i 's@LogFile=/tmp/zabbix_server.log@LogFile=/var/log/zabbix/zabbix_server.log@g' /etc/zabbix/zabbix_server.conf
# 与数据库有关的参数，观察
[root@workstation zabbix-3.0.4]# grep -v '^#' /etc/zabbix/zabbix_server.conf|grep -v '^$'
LogFile=/var/log/zabbix/zabbix_server.log
DBName=zabbix
DBUser=zabbix
Timeout=4
LogSlowQueries=3000
[root@workstation zabbix-3.0.4]# grep Password /etc/zabbix/zabbix_server.conf
#	For SQLite3 path to database file must be provided. DBUser and DBPassword are ignored.
### Option: DBPassword
# DBPassword=

# 通过sed修改
[root@workstation zabbix-3.0.4]# sed -i 's@# DBPassword=@DBPassword=uplooking@g' /etc/zabbix/zabbix_server.conf
```

#### 启动服务

* zabbix_server

```shell
[root@workstation zabbix-3.0.4]# service zabbix_server start
Reloading systemd:                                         [  OK  ]
Starting zabbix_server (via systemctl):                    [  OK  ] 
[root@workstation zabbix-3.0.4]# ss -luntp|grep zabbix
tcp    LISTEN     0      128       *:10051                 *:*                   users:(("zabbix_server",pid=31074,fd=4),("zabbix_server",pid=31073,fd=4),("zabbix_server",pid=31071,fd=4),("zabbix_server",pid=31067,fd=4),("zabbix_server",pid=31058,fd=4),("zabbix_server",pid=31057,fd=4),("zabbix_server",pid=31056,fd=4),("zabbix_server",pid=31055,fd=4),("zabbix_server",pid=31054,fd=4),("zabbix_server",pid=31052,fd=4),("zabbix_server",pid=31050,fd=4),("zabbix_server",pid=31049,fd=4),("zabbix_server",pid=31047,fd=4),("zabbix_server",pid=31045,fd=4),("zabbix_server",pid=31042,fd=4),("zabbix_server",pid=31040,fd=4),("zabbix_server",pid=31039,fd=4),("zabbix_server",pid=31038,fd=4),("zabbix_server",pid=31037,fd=4),("zabbix_server",pid=31036,fd=4),("zabbix_server",pid=31035,fd=4),("zabbix_server",pid=31034,fd=4),("zabbix_server",pid=31033,fd=4),("zabbix_server",pid=31030,fd=4),("zabbix_server",pid=31029,fd=4),("zabbix_server",pid=31028,fd=4),("zabbix_server",pid=31019,fd=4))
[root@workstation zabbix-3.0.4]# chkconfig zabbix_server on
```

### 配置zabbix agent

* Zabbix agent configuration file /usr/local/zabbix_agent/etc/zabbix_agentd.conf

agent的安装只需要解压编译即可，不需要依赖关系包

```shell
[root@mastera zabbix-3.0.4]# ls /usr/local/zabbix_agent
bin  etc  lib  sbin  share
```

#### 创建用户账户

server端用户和agent端用户最好不要用一个名字，为了安全。

```shell
[root@mastera ~]# groupadd -g 201 zabbixagent
[root@mastera ~]# useradd -g 201 -u 201 zabbixagent -s /sbin/nologin
[root@mastera ~]# id zabbixagent
uid=201(zabbixagent) gid=201(zabbixagent) groups=201(zabbixagent)
```

#### 创建链接

为了方便使用，可以设置一个软连接到对应的目录

```shell
[root@mastera ~]# ln -s /usr/local/zabbix_agent/etc /etc/zabbix_agent 
[root@mastera ~]# ln -s /usr/local/zabbix_agent/sbin/* /usr/sbin/
[root@mastera ~]# ln -s /usr/local/zabbix_agent/bin/* /usr/bin/
[root@mastera ~]# cp /opt/zabbix-3.0.4/misc/init.d/fedora/core/zabbix_agentd /etc/init.d
```

#### 修改服务启动脚本

```shell
[root@mastera ~]# sed -i 's@BASEDIR=/usr/local@BASEDIR=/usr/local/zabbix_agent@g' /etc/init.d/zabbix_agentd
```

#### 修改配置文件

```shell
[root@mastera ~]# sed -i 's@Server=127.0.0.1@Server=192.168.58.10@g' /etc/zabbix_agent/zabbix_agentd.conf
[root@mastera ~]# sed -i 's@ServerActive=127.0.0.1@ServerActive=192.168.58.10@g' /etc/zabbix_agent/zabbix_agentd.conf
[root@mastera ~]# sed -i 's@Hostname=Zabbix server@Hostname=mastera.uplooking.com@g' /etc/zabbix_agent/zabbix_agentd.conf
[root@mastera ~]# echo UnsafeUserParameters=1 >> /etc/zabbix_agent/zabbix_agentd.conf
[root@mastera ~]# grep -v '^#' /etc/zabbix_agent/zabbix_agentd.conf|grep -v "^$"
LogFile=/tmp/zabbix_agentd.log
Server=192.168.58.10
ServerActive=192.168.58.10
Hostname=mastera.uplooking.com
UnsafeUserParameters=1
```

* `Server=`Zabbix Server 端主机名或 IP 地址
* `ServerActive= `Zabbix Server 端主机名或 IP 地址
* `Hostname=` Agent 端的主机名 
* `UnsafeUserParameters=1` 是否限制用户自定义 keys 使用特殊字符


#### 启动服务

* zabbix_agentd

```shell
[root@mastera ~]# service zabbix_agentd start
Reloading systemd:                                         [  OK  ]
Starting zabbix_agentd (via systemctl):                    [  OK  ]
[root@mastera ~]# chkconfig zabbix_agentd on
```


### 配置zabbix web

```shell
[root@workstation ~]# echo php_value date.timezone Asia/Shanghai > /etc/httpd/conf.d/zabbix.conf
[root@workstation ~]# mkdir /var/www/html/zabbix
[root@workstation ~]# cp -r /opt/zabbix-3.0.4/frontends/php/ /var/www/html/zabbix
[root@workstation ~]# chown apache. /var/www/html/zabbix -R
[root@workstation ~]# systemctl start httpd
[root@workstation ~]# systemctl enable httpd
```
In your browser, open Zabbix URL: http://<server_ip_or_name>/zabbix

The default user name is Admin, password zabbix.

## 数据库监控项目


