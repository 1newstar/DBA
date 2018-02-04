## Redis 持久化

Redis之所以拥有非常高的性能，很大一个原因是只使用内存进行读写，所以一但宕机或重启导致内存数据丢失，那么Redis数据库也会丢失。为了解决这个问题，Redis需要能够将数据保存到硬盘上，这个过程称之为持久化。

Redis持久化有两种方案，分别为RDB方式与AOF方式。

### RDB持久化

RDB的实现原理非常简单，根据一定的规则周期化的将内存中的Redis的数据同步到硬盘上。整个过程会使用类似快照的方法来实现。简单的讲，父进程先fork出一个子进程，之后父进程继续处理用户请求，子进程创建临时文件执行数据同步。为了保证数据一致性，会启用COW方式进行读写。当数据同步完成后再用临时文件覆盖真正的RDB文件。

同步规则主要由配置文件中的save参数定义。
​

```
save 900 1
save 300 10
save 60 10000
```

以上这些参数的含义为：

900秒内有10个以上的键被更改则执行RDB同步，300秒内有10个键发生更改则同步，60秒内有10000个键发生更改则同步。三者关系为“或”，只要满足任何一个条件都会执行同步操作。

除了以上参数以外，还有些指令与事件也会自动触发同步，比如save,bgsave,flushall,主从同步事件等等。

RDB方式有一个比较严重的问题，如果在一次同步完成之后，连续15分钟内只做了2次修改，那么最终要到15分钟的时候才会同步，对应的对数为“save 900 1”。那如果在15分钟服务器宕机或者重启了，那么就有可能丢失这2次操作，所以RDB方式的持久化并不是非常完整。

Ex:配置RDB持久化并测试

```shell
[root@mastera0 ~]# vi /etc/redis.conf
save 900 1
save 300 10
save 60 10000
dbfilename dump.rdb
dir /var/lib/redis/

[root@mastera0 ~]# systemctl  restart redis
[root@mastera0 ~]# redis-cli  -h 127.0.0.1
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> set name aa
OK
127.0.0.1:6379> exit

等待15分钟
[root@mastera0 ~]# systemctl  restart redis
[root@mastera0 ~]# redis-cli  -h 127.0.0.1
127.0.0.1:6379> get name
"aa"
```

### AOF持久化

相对于RDB方式而言，AOF对数据完整性就做的更好了。AOF会将用户执行过的每一条指令都记录到硬盘上。如果出现意外中断，那么可以通过重演指令来还原数据库。由于经常要将指令同步到硬盘上，所以会对性能造成一定影响。

相关参数：

​

```
appendonly yes
```

```
auto-aof-rewrite-percentage 100
```

```
auto-aof-rewrite-min-size 64mb
```

以上两个参数用于重写AOF文件，以便自动去除重复指令，减小文件体积。

```
appendfsync [always|everysec|no]
```

此参数用于定义同步的频率，always代表每个操作都立刻同步，everysec代表1秒同步1次，no代表按操作系统默认的同步方式（Linux默认内存中修改过的文件会以30秒为周期同步到硬盘）。

Ex：配置AOF持久化并测试

```shell
[root@mastera0 ~]# vi /etc/redis.conf
appendonly yes
appendfsync everysec
[root@mastera0 ~]# systemctl  restart redis
[root@mastera0 ~]# redis-cli  -h 127.0.0.1
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> set name aa
OK
127.0.0.1:6379> exit
[root@mastera0 ~]# systemctl  restart redis
[root@mastera0 ~]# redis-cli  -h 127.0.0.1
127.0.0.1:6379> get name
"aa"
```

Redis允许RDB与AOF是可以同时打开。