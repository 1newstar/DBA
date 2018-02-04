# redis详解

[TOC]

> 根据《redis设计和实现》黄健宏著学习笔记
>
> http://redisbook.com/

## 基本配置

```shell
daemonize yes #是否以后台进程运行
pidfile /var/run/redis/redis-server.pid    #pid文件位置
port 6379	# 监听端口号，默认为 6379，如果你设为 0 ，redis 将不在 socket 上监听任何客户端连接。
bind 127.0.0.1   #绑定地址，如外网需要连接，设置0.0.0.0
timeout 300     #连接超时时间，单位秒
loglevel notice  #日志级别，分别有：
# debug ：适用于开发和测试
# verbose ：更详细信息
# notice ：适用于生产环境
# warning ：只记录警告或错误信息
logfile /var/log/redis/redis-server.log   #日志文件位置
syslog-enabled no    #是否将日志输出到系统日志
databases 16	#设置数据库数量，默认数据库为0
hz 10 # redis内部时间事件每1秒10次循环
```

## 安全

```shell
requirepass foobared # 需要密码
rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52 #如果公共环境,可以重命名部分敏感命令 如config
```

## RDB快照

```shell
save 900 1 #刷新快照到硬盘中，必须满足两者要求才会触发，即900秒之后至少1个关键字发生变化。
save 300 10 #必须是300秒之后至少10个关键字发生变化。
save 60 10000 #必须是60秒之后至少10000个关键字发生变化。
stop-writes-on-bgsave-error yes #后台存储错误停止写。
rdbcompression yes #使用LZF压缩rdb文件。
rdbchecksum yes #存储和加载rdb文件时校验。
dbfilename dump.rdb #设置rdb文件名。
dir ./ #设置工作目录，rdb文件会写入该目录。
```

## AOF配置

```shell
appendonly no #是否仅要日志
appendfsync no # 系统缓冲,统一写,速度快
appendfsync always # 系统不缓冲,直接写,慢,丢失数据少
appendfsync everysec #折衷,每秒写1次

no-appendfsync-on-rewrite no #为yes,则其他线程的数据放内存里,合并写入(速度快,容易丢失的多)
auto-AOF-rewrite-percentage 100 #当前aof文件是上次重写是大N%时重写(#当AOF日志文件即将增长到指定百分比时，redis通过调用BGREWRITEAOF是否自动重写AOF日志文件。)
auto-AOF-rewrite-min-size 64mb #aof重写至少要达到的大小
```

## 主从配置

```shell
slaveof <masterip> <masterport> 设为某台机器的从服务器
masterauth <master-password> 连接主服务器的密码
slave-serve-stale-data yes # 当主从断开或正在复制中,从服务器是否应答
slave-read-only yes #从服务器只读
repl-ping-slave-period 10 #从ping主的时间间隔,秒为单位
repl-timeout 60 #主从超时时间(超时认为断线了),要比period大
slave-priority 100 #如果master不能再正常工作，那么会在多个slave中，选择优先值最小的一个slave提升为master，优先值为0表示不能提升为master。

repl-disable-tcp-nodelay no #主端是否合并数据,大块发送给slave
slave-priority 100 从服务器的优先级,当主服挂了,会自动挑slave priority最小的为主服
```

## 限制

```shell
maxclients 10000 #最大连接数
maxmemory <bytes> #最大使用内存

maxmemory-policy volatile-lru #内存到极限后的处理
volatile-lru -> LRU算法删除过期key
allkeys-lru -> LRU算法删除key(不区分过不过期)
volatile-random -> 随机删除过期key
allkeys-random -> 随机删除key(不区分过不过期)
volatile-ttl -> 删除快过期的key
noeviction -> 不删除,返回错误信息

#解释 LRU ttl都是近似算法,可以选N个,再比较最适宜T踢出的数据
maxmemory-samples 3
```

## 慢查询

```shell
slowlog-log-slower-than 10000 #记录响应时间大于10000微秒的慢查询
slowlog-max-len 128 # 最多记录128条
```


## 高级配置

```shell
hash-max-zipmap-entries 512   #哈希表中元素（条目）总个数不超过设定数量时，采用线性紧凑格式存储来节省空间
hash-max-zipmap-value 64     #哈希表中每个value的长度不超过多少字节时，采用线性紧凑格式存储来节省空间
list-max-ziplist-entries 512  #list数据类型多少节点以下会采用去指针的紧凑存储格式
list-max-ziplist-value 64    #list数据类型节点值大小小于多少字节会采用紧凑存储格式
set-max-intset-entries 512   #set数据类型内部数据如果全部是数值型，且包含多少节点以下会采用紧凑格式存储
activerehashing yes        #是否激活重置哈希
```



## 服务端常用命令

```shell
time 返回时间戳+微秒
dbsize 返回key的数量
bgrewriteaof 重写aof
bgsave 后台开启子进程dump数据
save 阻塞进程dump数据
lastsave

slaveof host port 做host port的从服务器(数据清空,复制新主内容)
slaveof no one 变成主服务器(原数据不丢失,一般用于主服失败后)

flushdb 清空当前数据库的所有数据
flushall 清空所有数据库的所有数据(误用了怎么办?)

shutdown [save/nosave] 关闭服务器,保存数据,修改AOF(如果设置)

slowlog get 获取慢查询日志
slowlog len 获取慢查询日志条数
slowlog reset 清空慢查询


info []

config get 选项(支持*通配)
config set 选项 值
config rewrite 把值写到配置文件
config restart 更新info命令的信息

debug object key #调试选项,看一个key的情况
debug segfault #模拟段错误,让服务器崩溃
object key (refcount|encoding|idletime)
monitor #打开控制台,观察命令(调试用)
client list #列出所有连接
client kill #杀死某个连接 CLIENT KILL 127.0.0.1:43501
client getname #获取连接的名称 默认nil
client setname "名称" #设置连接名称,便于调试
```


## 连接命令

```shell
auth 密码 #密码登陆(如果有密码)
ping #测试服务器是否可用
echo "some content" #测试服务器是否正常交互
select 0/1/2... #选择数据库
quit #退出连接
```

## 持久化方式

### redis提供几种持久化机制

```shell

 a). RDB持久化

 工作方式 ：根据时间的间隔将redis中数据快照（dump）到dump.rdb文件

 优势 ：备份恢复简单。RDB通过子进程完成持久化工作，相对比AOF启动效率高

 劣势 ：服务器故障会丢失几分钟内的数据

 b). AOF持久化

 工作方式 ：以日志的形式记录所有更新操作到AOF日志文件，在redis服务重新启动时会读取该日志文 件来重新构建数据库，以保证启动后数据完整性。

 优势 ：AOF提供两种同步机制，一个是fsync always每次有数据变化就同步到日志文件和fsync everysec每秒同步一次到日志文件，最大限度保证数据完整性。

 劣势：日志文件相对RDB快照文件要大的多

 AOF日志重写功能 ：AOF日志文件过大，redis会自动重写AOF日志，append模式不断的将更新记录写入到老日志文件中，同时redis还会创建一个新的日志文件用于追加后续的记录。

 c). 同时应用AOF和RDB

 对于数据安全性高的场景，可同时使用AOF和RDB，这样会降低性能。

 d). 无持久化

 禁用redis服务持久化功能。
```

### AOF日志文件出错后，修复方法 

```shell
redis-check-aof --fix appendonly.aof  #--fix参数为修复日志文件，不加则对日志检查
```

### 不重启redis从RDB持久化切换到AOF持久化 ：

```shell
redis-cli> CONFIG SET appendonly yes      #启用AOF
redis-cli> CONFIG SET save ""         #关闭RDB
```






