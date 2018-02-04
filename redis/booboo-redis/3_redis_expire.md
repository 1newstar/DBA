# Redis 过期键值清理

> 20170918 Booboowei

[TOC]

## 过期键值清理策略

过期键值清理策略为：

- 惰性删除：碰到过期键时才会删除，scan num(触发惰性删除)
- 定期删除：每隔一段时间主动查找并删除，通过hz参数设定，默认每秒执行10次
- 加载RDB：载入时都会进行过期键值的清理，节约内存空间
- 加载AOF：载入时都会进行过期键值的清理，节约内存空间
- 重写AOF：重写时都会进行过期键值的清理，节约内存空间
- 内存溢出：内存达到设定的max值，根据清除策略进行（不论数据是否过期）

### 惰性删除

### 定期删除

### 加载RDB

- Redis 使用惰性删除和定期删除两种策略来删除过期的键： 惰性删除策略只在碰到过期键时才进行删除操作， 定期删除策略则每隔一段时间， 主动查找并删除过期键。
- 执行 SAVE 命令或者 BGSAVE 命令所产生的新 RDB 文件不会包含已经过期的键。
- 执行 BGREWRITEAOF 命令所产生的重写 AOF 文件不会包含已经过期的键。
- 当一个过期键被删除之后， 服务器会追加一条 DEL 命令到现有 AOF 文件的末尾， 显式地删除过期键。
- 当主服务器删除一个过期键之后， 它会向所有从服务器发送一条 DEL 命令， 显式地删除过期键。
- 从服务器即使发现过期键， 也不会自作主张地删除它， 而是等待主节点发来 DEL 命令， 这种统一、中心化的过期键删除策略可以保证主从服务器数据的一致性

### 加载AOF

### 重写AOF

### 内存溢出



## 实验1——RDB写入和载入

| key  | expire | NOW   | RDB写入 | RDB载入 |
| :--- | :----- | :---- | :---- | :---- |
|      |        | 12:00 | 12:23 | 13:30 |
| key1 | 3600s  | yes   | yes   | no    |
| key2 | 7200s  | yes   | yes   | yes   |
| key3 | 60s    | yes   | no    | no    |


```shell
# 12:00 向redis服务器中更新3个key
[root@mastera0 redisshell]# redis-cli -a zyadmin
127.0.0.1:6379> set key1 booboo
OK
127.0.0.1:6379> set key2 tom
OK
127.0.0.1:6379> set key3 jack
OK
127.0.0.1:6379> EXPIRE key1 3600
(integer) 1
127.0.0.1:6379> expire key2 7200
(integer) 1
127.0.0.1:6379> expire key3 60
(integer) 1
# key3当前已经过期
127.0.0.1:6379> ttl key3
(integer) -2
127.0.0.1:6379> ttl key1
(integer) 3507
127.0.0.1:6379> ttl key2
(integer) 7117
# 12:23通过save命令将数据写入RDB文件
127.0.0.1:6379> save
OK
127.0.0.1:6379> exit

# 到redis数据目录下查看rdb文件
[root@mastera0 6379]# ll -h
-rw-r--r--. 1 root root 122 Sep 18 12:22 dump.rdb

# 13:30启动数据库服务器，载入RDB文件
[root@mastera0 redisshell]# ./redisctl stop 6379

# 客户端登陆查看key的情况，只有key2被还原
[root@mastera0 redisshell]# redis-cli -p 6379
127.0.0.1:6379> auth zyadmin
OK
127.0.0.1:6379> keys *
1) "key2"

```

## 实验2——AOF写入、重写、载入


```shell
[root@mastera0 redisshell]# cat /root/test.redis 
set key1 booboo
set key2 jack
set key3 tom
expire key1 10
expire key2 120
expire key3 3600

# 14:34 写入key
[root@mastera0 redisshell]# redis-cli -p 6379 -a zyadmin < /root/test.redis
OK
OK
OK
(integer) 1
(integer) 1
(integer) 1

# 14:36 kye1已过期，此时的aof文件为
[root@mastera0 6379]# sed -n  '/^\*/!p' appendonly.aof | grep -v '^\$'
SELECT
0
set
key1
booboo
set
key2
jack
set
key3
tom
PEXPIREAT
key1
1505716445681
PEXPIREAT
key2
1505716555681
PEXPIREAT
key3
1505720035681
DEL
key1

# 停止服务
[root@mastera0 redisshell]# redisctl stop 6379

# 14:38 key2 已过期时，启动服务
[root@mastera0 redisshell]# redisctl start 6379

# AOF文件中自动追加delete key2
[root@mastera0 6379]# sed -n  '/^\*/!p' appendonly.aof | grep -v '^\$'
SELECT
0
set
key1
booboo
set
key2
jack
set
key3
tom
PEXPIREAT
key1
1505716445681
PEXPIREAT
key2
1505716555681
PEXPIREAT
key3
1505720035681
DEL
key1
SELECT
0
DEL
key2

# 客户端查看key的情况
[root@mastera0 redisshell]# redis-cli -p 6379 -a zyadmin 
127.0.0.1:6379> get key2
(nil)
127.0.0.1:6379> get key3
"tom"
```

## 实验3——复制

设置hz为1，每秒只执行一次删除过期值的操作，进行本次测试


```shell
[root@mastera0 redisshell]# redisctl start 6379
[root@mastera0 redisshell]# redisctl start 6380
# master 导入10万个key，并设置过期值为60s
# set a1 1
# set a100000 100000
[root@mastera0 redisshell]# redis-cli -p 6379 -a zyadmin  < /root/afile &> /dev/null

# 动态观察master的aof文件
[root@mastera0 6379]# tail -f appendonly.aof 

# 一旦看到开始追加delete操作，立刻在slave上执行查询
# slave
[root@mastera0 redisshell]# redis-cli -p 6380 -a zyadmin
127.0.0.1:6380> get a100000
"100000"
127.0.0.1:6380> get a100000
(nil)


# 虽然a100000已经过期，但是slave还是会将值返回给客户端，就像没有过期一样
# 直到master上发送delete命令，slave才会将会delete

```

## 总结

过期键值清理策略为：

* 惰性删除：碰到过期键时才会删除，scan num(触发惰性删除)
* 定期删除：每隔一段时间主动查找并删除，通过hz参数设定，默认每秒执行10次
* 加载RDB：载入时都会进行过期键值的清理，节约内存空间
* 加载AOF：载入时都会进行过期键值的清理，节约内存空间
* 重写AOF：重写时都会进行过期键值的清理，节约内存空间
* 内存溢出：内存达到设定的max值，根据清除策略进行（不论数据是否过期）

```shell
# volatile-lru -> LRU算法，从已经设置过过期值的数据集中挑选最近最少使用的数据淘汰
# allkeys-lru -> LRU算法，从所有的数据集中挑选最近最少值用的数据淘汰
# volatile-random -> 随即算法，从已经设置过过期值的数据集中随即挑选数据淘汰
# allkeys-random -> 随即算法，从所有数据集中随即挑选数据淘汰
# volatile-ttl -> 最少时间，从已经设置过过期值的数据集中挑选将要过期的数据淘汰
# noeviction -> 不清理，直接报错OMM
# The default is:
# maxmemory-policy noeviction
```













