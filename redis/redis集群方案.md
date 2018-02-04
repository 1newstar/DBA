## redis集群方案

* 60s1万条是正常的
* mycat多实例join的分析
* hash算法

redis使用哈希槽，而不是一致性hash

没有槽的节点不发生切换（S升级为主），为何还要保留没有槽的节点？

当有槽节点压力大时，可以作数据迁移，分当压力

### 数据一致性保证

M和S各8个节点
如果2号M节点出现故障，那么2号S节点立刻升级为M
当master fail，S会全量同步，是否会有数据丢失呢？

save 900 1 #15分钟1条
save 300 1000 #5分钟1000条
save 60 10000 #1分钟1万条

假设距离上一次保存后的52秒写了9999条，那么就会全部丢了

可以使用AOF，有点类似mysql的二进制的日志，redis写一条记一条。

### redis集群搭建步骤

#### 1.安装软件

```shell
[root@mastera0 redis]# cp redis-3.0.7.tar.gz /usr/local
[root@mastera0 redis]# cd /usr/local/
[root@mastera0 local]# ls
bin  etc  games  include  lib  lib64  libexec  redis-3.0.7.tar.gz  sbin  share  src
[root@mastera0 local]# tar -xf redis-3.0.7.tar.gz 
[root@mastera0 local]# ls
bin  etc  games  include  lib  lib64  libexec  redis-3.0.7  redis-3.0.7.tar.gz  sbin  share  src

[root@mastera0 local]# ln -s  redis-3.0.7 redis
[root@mastera0 redis]# ls
00-RELEASENOTES  CONTRIBUTING  deps     Makefile   README      runtest          runtest-sentinel  src    utils
BUGS             COPYING       INSTALL  MANIFESTO  redis.conf  runtest-cluster  sentinel.conf     tests
```

创建数据目录

```shell
[root@mastera0 redis]# mkdir /app/redis_cluster/node{6380..6385} -p
```

创建配置目录

```shell
[root@mastera0 redis]# mkdir /app/redis_cluster/conf
```

源码编译

```shell
[root@mastera0 redis]# yum install -y gcc* 
[root@mastera0 redis]# make
[root@mastera0 redis]# make install
cd src && make install
make[1]: Entering directory `/usr/local/redis-3.0.7/src'

Hint: It's a good idea to run 'make test' ;)

    INSTALL install
    INSTALL install
    INSTALL install
    INSTALL install
    INSTALL install
make[1]: Leaving directory `/usr/local/redis-3.0.7/src'
[root@mastera0 redis]#  
```


#### 2.集群配置文件

```shell
port 6380
pidfile /var/run/redis6380.pid
dir /app/redis_cluster/node6380
cluster-enabled yes
cluster-config-file node6380.conf
cluster-node-timeout 5000

[root@mastera0 redis]# vim create_redis_conf.sh 
#!/bin/bash
for i in `seq $1 $2`
do 
	cat > $3/redis$i.conf << ENDF
daemonize no
pidfile /var/run/redis$i.pid
port $i
tcp-backlog 511
timeout 0
tcp-keepalive 0
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /app/redis_cluster/node$i
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-entries 512
list-max-ziplist-value 64
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
cluster-enabled yes
cluster-config-file node$i.conf
cluster-node-timeout 5000
ENDF
done

[root@mastera0 redis]# bash create_redis_conf.sh 6380 6384 /app/redis_cluster/conf
[root@mastera0 redis]# ll /app/redis_cluster/conf
total 24
-rw-r--r--. 1 root root 1232 Dec 17 12:57 redis6380.conf
-rw-r--r--. 1 root root 1232 Dec 17 12:57 redis6381.conf
-rw-r--r--. 1 root root 1232 Dec 17 12:57 redis6382.conf
-rw-r--r--. 1 root root 1232 Dec 17 12:57 redis6383.conf
-rw-r--r--. 1 root root 1232 Dec 17 12:57 redis6384.conf
-rw-r--r--. 1 root root 1232 Dec 17 13:27 redis6385.conf

[root@mastera0 redis]# pwd
/usr/local/redis
[root@mastera0 redis]# cd /app/redis_cluster/
[root@mastera0 redis_cluster]# ls
conf  node6380  node6381  node6382  node6383  node6384
```

#### 3.启动redis服务

```shell
[root@mastera0 redis_cluster]# redis-server /app/redis_cluster/conf/node6380.conf 
29837:M 17 Dec 13:02:36.216 * Increased maximum number of open files to 10032 (it was originally set to 1024).
29837:M 17 Dec 13:02:36.226 * No cluster configuration found, I'm d3609c8b68dcc4884501d14ec7803eef6223513b
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 3.0.7 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in cluster mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6380
 |    `-._   `._    /     _.-'    |     PID: 29837
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

29837:M 17 Dec 13:02:36.422 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
29837:M 17 Dec 13:02:36.422 # Server started, Redis version 3.0.7
29837:M 17 Dec 13:02:36.422 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
29837:M 17 Dec 13:02:36.423 * The server is now ready to accept connections on port 6380
^C29837:signal-handler (1481950975) Received SIGINT scheduling shutdown...
29837:M 17 Dec 13:02:55.685 # User requested shutdown...
29837:M 17 Dec 13:02:55.686 * Saving the final RDB snapshot before exiting.
29837:M 17 Dec 13:02:55.850 * DB saved on disk
29837:M 17 Dec 13:02:55.850 # Redis is now ready to exit, bye bye...

[root@mastera0 redis_cluster]# vim /etc/sysctl.conf
vm.overcommit_memory = 1
[root@mastera0 redis_cluster]# sysctl -a

[root@mastera0 redis_cluster]# redis-server /app/redis_cluster/conf/node6380.conf 
29861:M 17 Dec 13:04:39.478 * Increased maximum number of open files to 10032 (it was originally set to 1024).
29861:M 17 Dec 13:04:39.479 * Node configuration loaded, I'm d3609c8b68dcc4884501d14ec7803eef6223513b
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 3.0.7 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in cluster mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6380
 |    `-._   `._    /     _.-'    |     PID: 29861
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

29861:M 17 Dec 13:04:39.480 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
29861:M 17 Dec 13:04:39.480 # Server started, Redis version 3.0.7
29861:M 17 Dec 13:04:39.480 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
29861:M 17 Dec 13:04:39.480 * DB loaded from disk: 0.000 seconds
29861:M 17 Dec 13:04:39.480 * The server is now ready to accept connections on port 6380
```

测试1台成功后，同时启动6台


#### 4.安装ruby rubygems 

目的是使用gem工具安装redis.gem

ruby，rhel6中自带，而rubygems没有，需要下载

```shell
[root@mastera0 redis_cluster]# cd
[root@mastera0 ~]# ls
anaconda-ks.cfg  Downloads           Music     rubygems-1.3.7-5.el6.noarch.rpm
Desktop          install.log         Pictures  Templates
Documents        install.log.syslog  Public    Videos
[root@mastera0 ~]# yum install -y ruby
[root@mastera0 ~]# rpm -ivh rubygems-1.3.7-5.el6.noarch.rpm 
warning: rubygems-1.3.7-5.el6.noarch.rpm: Header V3 RSA/SHA1 Signature, key ID c105b9de: NOKEY
error: Failed dependencies:
	ruby-rdoc is needed by rubygems-1.3.7-5.el6.noarch
[root@mastera0 ~]# yum localinstall -y rubygems-1.3.7-5.el6.noarch.rpm 

[root@mastera0 ~]# cp /mnt/lesson9/redis/redis-3.0.7.gem ~
[root@mastera0 ~]# ls
anaconda-ks.cfg  install.log         Public                           Videos
Desktop          install.log.syslog  redis-3.0.7.gem
Documents        Music               rubygems-1.3.7-5.el6.noarch.rpm
Downloads        Pictures            Templates
[root@mastera0 ~]# gem install redis-3.0.7.gem 
Successfully installed redis-3.0.7
1 gem installed
Installing ri documentation for redis-3.0.7...
Installing RDoc documentation for redis-3.0.7...
```


#### 5.启动reids集群

至少 3 master

此处写了一个小脚本来实现多个实例启动关闭

```shell
[root@mastera0 redis]# cat redis_multi_ctl.sh 
#!/bin/bash
redis_conf_dir="/app/redis_cluster/conf"
redis_data_dir="/app/redis_cluster"
ALL_start()
{
	for i in `seq 6380 6385`
	do
	 	redis-server $redis_conf_dir/redis$i.conf &> $redis_data_dir/redis$i.log &
	done
	
}

ALL_stop()
{
	for i in `ps -ef|grep redis|grep cluster |awk '{print $2}'`
	do 
		kill -9 $i
	done
}

ALL_status()
{
	ps -ef|grep redis
}

case $1 in
start)
	ALL_start;;
status)
	ALL_status;;
stop)
	ALL_stop;;
*)
	echo "start|stop|status";;
esac
[root@mastera0 redis]# bash redis_multi_ctl.sh start
[root@mastera0 redis]# bash redis_multi_ctl.sh status
root     30115     1  0 13:47 pts/0    00:00:00 redis-server *:6380 [cluster]                      
root     30116     1  0 13:47 pts/0    00:00:00 redis-server *:6381 [cluster]                      
root     30117     1  0 13:47 pts/0    00:00:00 redis-server *:6382 [cluster]                      
root     30118     1  0 13:47 pts/0    00:00:00 redis-server *:6383 [cluster]                      
root     30119     1  0 13:47 pts/0    00:00:00 redis-server *:6384 [cluster]                      
root     30120     1  0 13:47 pts/0    00:00:00 redis-server *:6385 [cluster]                      
root     30133  1717  0 13:47 pts/0    00:00:00 bash redis_multi_ctl.sh status
root     30135 30133  0 13:47 pts/0    00:00:00 grep redis
```

此时还没有启动集群，只启动了节点

```shell
[root@mastera0 redis]# redis-cli -p 6380 cluster info
cluster_state:fail
cluster_slots_assigned:0
cluster_slots_ok:0
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:1
cluster_size:0
cluster_current_epoch:0
cluster_my_epoch:0
cluster_stats_messages_sent:0
cluster_stats_messages_received:0
```

启动集群的命令为 src/redis-trib.rb

```shell
[root@mastera0 redis]# pwd
/usr/local/redis
[root@mastera0 redis]# src/redis-trib.rb create --replicas 1 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384 127.0.0.1:6385
>>> Creating cluster
>>> Performing hash slots allocation on 6 nodes...
Using 3 masters:
127.0.0.1:6380
127.0.0.1:6381
127.0.0.1:6382
Adding replica 127.0.0.1:6383 to 127.0.0.1:6380
Adding replica 127.0.0.1:6384 to 127.0.0.1:6381
Adding replica 127.0.0.1:6385 to 127.0.0.1:6382
M: d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380
   slots:0-5460 (5461 slots) master
M: 0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381
   slots:5461-10922 (5462 slots) master
M: cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382
   slots:10923-16383 (5461 slots) master
S: 7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383
   replicates d3609c8b68dcc4884501d14ec7803eef6223513b
S: 26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384
   replicates 0dedd063912ddd0eae7cf111f8be805929290c6e
S: a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385
   replicates cb5c188083e726c85ac1270f203255ba1c784894
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join...
>>> Performing Cluster Check (using node 127.0.0.1:6380)
M: d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380
   slots:0-5460 (5461 slots) master
M: 0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381
   slots:5461-10922 (5462 slots) master
M: cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382
   slots:10923-16383 (5461 slots) master
M: 7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383
   slots: (0 slots) master
   replicates d3609c8b68dcc4884501d14ec7803eef6223513b
M: 26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384
   slots: (0 slots) master
   replicates 0dedd063912ddd0eae7cf111f8be805929290c6e
M: a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385
   slots: (0 slots) master
   replicates cb5c188083e726c85ac1270f203255ba1c784894
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

#### 6.查看redis集群状态


```shell
[root@mastera0 redis]# for i in `seq 6380 6385`;do redis-cli -p $i cluster info;echo ======================;done
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_sent:742
cluster_stats_messages_received:742
======================
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:2
cluster_stats_messages_sent:724
cluster_stats_messages_received:724
======================
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:3
cluster_stats_messages_sent:720
cluster_stats_messages_received:720
======================
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_sent:745
cluster_stats_messages_received:745
======================
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:2
cluster_stats_messages_sent:719
cluster_stats_messages_received:719
======================
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:3
cluster_stats_messages_sent:718
cluster_stats_messages_received:718
======================
```

redis-trib.rb 命令使用方法

- 启动集群 `create --replicas 1 ip:port`
  - 添加节点`add-node masterip`		`add-node --slave --master-id [masterid] slaveip:prot`
- 删除节点 `del-node ip:port id`

   删除时节点必须为空，无数据


#### 7. 使用reids集群

客户端以集群的方式来连接，-c 任意一个master的端口即可

```shell
[root@mastera0 redis]# redis-cli -c -p 6380
127.0.0.1:6380> set name booboo
-> Redirected to slot [5798] located at 127.0.0.1:6381
OK
127.0.0.1:6381> set age 99
-> Redirected to slot [741] located at 127.0.0.1:6380
OK
127.0.0.1:6380> set addr shagnhai
-> Redirected to slot [12790] located at 127.0.0.1:6382
OK
127.0.0.1:6382> set tel 10086
-> Redirected to slot [7485] located at 127.0.0.1:6381
OK
127.0.0.1:6381> get name
"booboo"
127.0.0.1:6381> get tel
"10086"
127.0.0.1:6381> get age
-> Redirected to slot [741] located at 127.0.0.1:6380
"99"
127.0.0.1:6380> get addr
-> Redirected to slot [12790] located at 127.0.0.1:6382
"shagnhai"
127.0.0.1:6382> exit
[root@mastera0 redis]# redis-cli -p 6380
127.0.0.1:6380> get name
(error) MOVED 5798 127.0.0.1:6381
127.0.0.1:6380> get age
"99"
127.0.0.1:6380> get addr
(error) MOVED 12790 127.0.0.1:6382
127.0.0.1:6380> get tel
(error) MOVED 7485 127.0.0.1:6381
127.0.0.1:6380> exit
```

#### 8.哈希槽的配置

redis-cli

集群命令

- CLUSTER INFO 打印集群的信息
- CLUSTER NODES 列出集群当前已知的所有节点( node ),以及这些节点的相关信息。

节点

- CLUSTER MEET <ip> <port> 将 ip 和 port 所指定的节点添加到集群当中,让它成为集群的一份子。
- CLUSTER FORGET <node_id> 从集群中移除 node_id 指定的节点。
- CLUSTER REPLICATE <node_id> 将当前节点设置为 node_id 指定的节点的从节点。
- CLUSTER SAVECONFIG 将节点的配置文件保存到硬盘里面。

槽 (slot)

- CLUSTER ADDSLOTS <slot> [slot ...] 将一个或多个槽( slot )指派( assign )给当前节点。
- CLUSTER DELSLOTS <slot> [slot ...] 移除一个或多个槽对当前节点的指派。
- CLUSTER FLUSHSLOTS 移除指派给当前节点的所有槽,让当前节点变成一个没有指派任何槽的节点。
- CLUSTER SETSLOT <slot> NODE <node_id> 将槽 slot 指派给 node_id 指定的节点,如果槽已经指派给另一个节点,那么先让另一个节点删除该槽 > ,然后再进行指派。
- CLUSTER SETSLOT <slot> MIGRATING <node_id> 将本节点的槽 slot 迁移到 node_id 指定的节点中。
- CLUSTER SETSLOT <slot> IMPORTING <node_id> 从 node_id 指定的节点中导入槽 slot 到本节点。
- CLUSTER SETSLOT <slot> STABLE 取消对槽 slot 的导入( import )或者迁移( migrate )。

键

- CLUSTER KEYSLOT <key> 计算键 key 应该被放置在哪个槽上。
- CLUSTER COUNTKEYSINSLOT <slot> 返回槽 slot 目前包含的键值对数量。
- CLUSTER GETKEYSINSLOT <slot> <count> 返回 count 个 slot 槽中的键。


```shell
[root@mastera0 redis]# redis-cli -p 6380 -c
127.0.0.1:6380> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_sent:3410
cluster_stats_messages_received:3410
127.0.0.1:6380> cluster nodes
7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383 slave d3609c8b68dcc4884501d14ec7803eef6223513b 0 1481954680681 4 connected
26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384 slave 0dedd063912ddd0eae7cf111f8be805929290c6e 0 1481954681683 5 connected
a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385 slave cb5c188083e726c85ac1270f203255ba1c784894 0 1481954682685 6 connected
0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381 master - 0 1481954681683 2 connected 5461-10922
cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382 master - 0 1481954681683 3 connected 10923-16383
d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380 myself,master - 0 0 1 connected 0-5460
127.0.0.1:6380> CLUSTER SLOTS
1) 1) (integer) 5461
   2) (integer) 10922
   3) 1) "127.0.0.1"
      2) (integer) 6381
   4) 1) "127.0.0.1"
      2) (integer) 6384
2) 1) (integer) 10923
   2) (integer) 16383
   3) 1) "127.0.0.1"
      2) (integer) 6382
   4) 1) "127.0.0.1"
      2) (integer) 6385
3) 1) (integer) 0
   2) (integer) 5460
   3) 1) "127.0.0.1"
      2) (integer) 6380
   4) 1) "127.0.0.1"
      2) (integer) 6383
```

redis集群不应该配密码

### redis集群测试

1. 向集群中循环插入10000个key
2. 模拟node6380fail，查看集群状态；重新启动node6380，查看集群状态
3. 模拟node6384fial后，插入记录，其主node6381fail，查看集群是否失效

什么时候整个集群不可用(cluster_state:fail)?

a:如果集群任意 master 挂掉,且当前 master 没有 slave.集群进入 fail 状态,也可以理解成集群的 slot 映射[0-16383]不完成 时进入 fail 状态. ps : redis-3.0.0.rc1 加入 cluster-require-full-coverage 参数,默认关闭,打开集群兼容部分失败.

b:如果集群超过半数以上 master 挂掉,无论是否有 slave 集群进入 fail 状态.

```shell
[root@mastera0 redis]# cat insert.sh
#!/bin/bash
for i in `seq 1 10000`
do
cat >> insert.file << ENDF
set name$i $i
ENDF
done
[root@mastera0 redis]# bash insert.sh
[root@mastera0 redis]# tail insert.file
set name9991 9991
set name9992 9992
set name9993 9993
set name9994 9994
set name9995 9995
set name9996 9996
set name9997 9997
set name9998 9998
set name9999 9999
set name10000 10000
[root@mastera0 redis]# redis-cli -c -p 6380 < insert.file
[root@mastera0 redis]# redis-cli -c -p 6380 get name100
"100"
[root@mastera0 redis]# redis-cli -c -p 6380 get name10000
"10000"
-------------------------
[root@mastera0 redis]# ps -ef|grep redis
root      8073  1717  0 14:33 pts/0    00:00:00 grep redis
root     30293     1  0 14:19 pts/0    00:00:01 redis-server *:6380 [cluster]                      
root     30294     1  0 14:19 pts/0    00:00:01 redis-server *:6381 [cluster]                      
root     30295     1  0 14:19 pts/0    00:00:01 redis-server *:6382 [cluster]                      
root     30296     1  0 14:19 pts/0    00:00:01 redis-server *:6383 [cluster]                      
root     30297     1  0 14:19 pts/0    00:00:01 redis-server *:6384 [cluster]                      
root     30298     1  0 14:19 pts/0    00:00:01 redis-server *:6385 [cluster]                      
[root@mastera0 redis]# kill -9 30293
[root@mastera0 redis]# redis-cli -c -p 6381 cluster nodes
7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383 master - 0 1481956452010 7 connected 0-5460
a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385 slave cb5c188083e726c85ac1270f203255ba1c784894 0 1481956450405 3 connected
d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380 master,fail - 1481956439636 1481956438935 1 disconnected
0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381 myself,master - 0 0 2 connected 5461-10922
cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382 master - 0 1481956449903 3 connected 10923-16383
26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384 slave 0dedd063912ddd0eae7cf111f8be805929290c6e 0 1481956451408 5 connected
```

看到master6380挂了后，slave6383已经升级为master了

重新启动6380，发现他已经变成了slave

```shell
[root@mastera0 redis]# redis-server /app/redis_cluster/conf/redis6380.conf &> /app/redis_cluster/node6380/node6380.log &
[2] 8093

[root@mastera0 redis]# redis-cli -p 6380 cluster nodes
7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383 master - 0 1481956789544 7 connected 0-5460
0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381 master - 0 1481956787538 2 connected 5461-10922
a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385 slave cb5c188083e726c85ac1270f203255ba1c784894 0 1481956789544 6 connected
26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384 slave 0dedd063912ddd0eae7cf111f8be805929290c6e 0 1481956788541 5 connected
d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380 myself,slave 7fd120256350adf8f0d1378f60bd6ea9ddd8376f 0 0 1 connected
cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382 master - 0 1481956788039 3 connected 10923-16383

-----------

[root@mastera0 redis]# ps -ef |grep redis
root      8093  1717  0 14:38 pts/0    00:00:00 redis-server *:6380 [cluster]                      
root      8120  1717  0 14:43 pts/0    00:00:00 grep redis
root     30294     1  0 14:19 pts/0    00:00:02 redis-server *:6381 [cluster]                      
root     30295     1  0 14:19 pts/0    00:00:02 redis-server *:6382 [cluster]                      
root     30296     1  0 14:19 pts/0    00:00:01 redis-server *:6383 [cluster]                      
root     30297     1  0 14:19 pts/0    00:00:01 redis-server *:6384 [cluster]                      
root     30298     1  0 14:19 pts/0    00:00:01 redis-server *:6385 [cluster]                      
[root@mastera0 redis]# kill -9 30297
[root@mastera0 redis]# redis-cli -p 6384 cluster slots
Could not connect to Redis at 127.0.0.1:6384: Connection refused
[root@mastera0 redis]# vim insert.sh
[root@mastera0 redis]# cat insert.sh
#!/bin/bash
for i in `seq 1 10000`
do
cat >> insert.file << ENDF
set age$i $i
ENDF
done
[root@mastera0 redis]# bash insert.sh
[root@mastera0 redis]# tail -n 4 insert.file
set age9997 9997
set age9998 9998
set age9999 9999
set age10000 10000
[root@mastera0 redis]# time redis-cli -c -p 6381 < insert.file &> /dev/null

real	0m4.140s
user	0m0.473s
sys	0m1.859s
[root@mastera0 redis]# kill -9 30294

[root@mastera0 redis]# ps -ef|grep redis
root      8093  1717  0 14:38 pts/0    00:00:01 redis-server *:6380 [cluster]                      
root     18142  1717  0 14:46 pts/0    00:00:00 grep redis
root     30295     1  0 14:19 pts/0    00:00:03 redis-server *:6382 [cluster]                      
root     30296     1  0 14:19 pts/0    00:00:03 redis-server *:6383 [cluster]                      
root     30298     1  0 14:19 pts/0    00:00:02 redis-server *:6385 [cluster]                      
[root@mastera0 redis]# redis-cli -p 6382 cluster nodes
cb5c188083e726c85ac1270f203255ba1c784894 127.0.0.1:6382 myself,master - 0 0 3 connected 10923-16383
0dedd063912ddd0eae7cf111f8be805929290c6e 127.0.0.1:6381 master,fail - 1481957155300 1481957154698 2 disconnected 5461-10922
d3609c8b68dcc4884501d14ec7803eef6223513b 127.0.0.1:6380 slave 7fd120256350adf8f0d1378f60bd6ea9ddd8376f 0 1481957227007 7 connected
26b67747334de461c57eef438f282c332d736a8b 127.0.0.1:6384 slave,fail 0dedd063912ddd0eae7cf111f8be805929290c6e 1481957013040 1481957012739 5 disconnected
7fd120256350adf8f0d1378f60bd6ea9ddd8376f 127.0.0.1:6383 master - 0 1481957226003 7 connected 0-5460
a6a4c51535ad00407f8c636cd620b63a4469c796 127.0.0.1:6385 slave cb5c188083e726c85ac1270f203255ba1c784894 0 1481957226506 3 connected
[root@mastera0 redis]# redis-cli -p 6382 cluster slots
1) 1) (integer) 10923
   2) (integer) 16383
   3) 1) "127.0.0.1"
      2) (integer) 6382
   4) 1) "127.0.0.1"
      2) (integer) 6385
2) 1) (integer) 5461
   2) (integer) 10922
   3) 1) "127.0.0.1"
      2) (integer) 6381
3) 1) (integer) 0
   2) (integer) 5460
   3) 1) "127.0.0.1"
      2) (integer) 6383
   4) 1) "127.0.0.1"
      2) (integer) 6380
[root@mastera0 redis]# redis-cli -p 6382
127.0.0.1:6382> get age10000
(error) CLUSTERDOWN The cluster is down
127.0.0.1:6382> cluster info
cluster_state:fail
cluster_slots_assigned:16384
cluster_slots_ok:10922
cluster_slots_pfail:0
cluster_slots_fail:5462
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:7
cluster_my_epoch:3
cluster_stats_messages_sent:14759
cluster_stats_messages_received:6997
```

### redis集群手动启动

除了使用src/redis-trib.rb 还可以通过redis-cli

* cluster meet 配置集群中的master

  * cluster replicate配置master的slave

  * cluster addslots配置hash槽


```shell
[root@mastera0 redis]# bash redis_multi_ctl.sh stop
[2]-  Killed                  redis-server /app/redis_cluster/conf/redis6380.conf &>/app/redis_cluster/node6380/node6380.log
[root@mastera0 redis]# bash redis_multi_ctl.sh status
root     18185  1717  0 14:54 pts/0    00:00:00 bash redis_multi_ctl.sh status
root     18187 18185  0 14:54 pts/0    00:00:00 grep redis
[3]+  Killed                  redis-server /app/redis_cluster/conf/redis6381.conf &>/app/redis_cluster/node6381/node6381.log
[root@mastera0 redis]# bash redis_multi_ctl.sh status
root     18189  1717  0 14:55 pts/0    00:00:00 bash redis_multi_ctl.sh status
root     18191 18189  0 14:55 pts/0    00:00:00 grep redis
[root@mastera0 redis]# cd /app/redis_cluster/
[root@mastera0 redis_cluster]# ls
conf      node6381  node6383  node6385       redis6381.log  redis6383.log  redis6385.log
node6380  node6382  node6384  redis6380.log  redis6382.log  redis6384.log
[root@mastera0 redis_cluster]# ll node6380
total 96
-rw-r--r--. 1 root root 82548 Dec 17 14:50 dump.rdb
-rw-r--r--. 1 root root   753 Dec 17 14:51 node6380.conf
-rw-r--r--. 1 root root  4191 Dec 17 14:51 node6380.log
[root@mastera0 redis_cluster]# vim conf/redis6380.conf 
[root@mastera0 redis_cluster]# rm -rf node6380/*
[root@mastera0 redis_cluster]# rm -rf node6381/*
[root@mastera0 redis_cluster]# rm -rf node6382/*
[root@mastera0 redis_cluster]# rm -rf node6383/*
[root@mastera0 redis_cluster]# rm -rf node6384/*
[root@mastera0 redis_cluster]# rm -rf node6385/*
[root@mastera0 redis_cluster]# rm -rf *.log
[root@mastera0 redis_cluster]# ls
conf  node6380  node6381  node6382  node6383  node6384  node6385


[root@mastera0 redis_cluster]# cd -
/usr/local/redis
[root@mastera0 redis]# pwd
/usr/local/redis
[root@mastera0 redis]# bash redis_multi_ctl.sh start
[root@mastera0 redis]# bash redis_multi_ctl.sh status
root     18293     1  0 15:07 pts/0    00:00:00 redis-server *:6380 [cluster]                      
root     18294     1  0 15:07 pts/0    00:00:00 redis-server *:6381 [cluster]                      
root     18295     1  0 15:07 pts/0    00:00:00 redis-server *:6382 [cluster]                      
root     18296     1  0 15:07 pts/0    00:00:00 redis-server *:6383 [cluster]                      
root     18297     1  0 15:07 pts/0    00:00:00 redis-server *:6384 [cluster]                      
root     18298     1  0 15:07 pts/0    00:00:00 redis-server *:6385 [cluster]                      
root     18311  1717  0 15:07 pts/0    00:00:00 bash redis_multi_ctl.sh status
root     18313 18311  0 15:07 pts/0    00:00:00 grep redis
```

查看当前的集群信息，发现每一个节点就是一个独立的集群

```shell
[root@mastera0 redis]# for i in `seq 6380 6385`;do redis-cli -p $i cluster nodes;done
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 :6380 myself,master - 0 0 0 connected
f95d8a90e129c8b9067ba1c97e77cd71508c42a0 :6381 myself,master - 0 0 0 connected
0e0958e72964fd922820ef9ed4377d10a33a2356 :6382 myself,master - 0 0 0 connected
ef29f1294accee3ec85d9272becbe20307f4fc9e :6383 myself,master - 0 0 0 connected
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a :6384 myself,master - 0 0 0 connected
fa7c7d5e866359f3863d9ef54654f3cfee8ccc4a :6385 myself,master - 0 0 0 connected
```

将master节点加入一个集群中

```shell
[root@mastera0 redis]# redis-cli -p 6380 cluster meet 127.0.0.1 6381
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster meet 127.0.0.1 6382
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster meet 127.0.0.1 6383
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster meet 127.0.0.1 6384
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster meet 127.0.0.1 6385
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster nodes
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481958712420 2 connected
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 myself,master - 0 0 1 connected
f95d8a90e129c8b9067ba1c97e77cd71508c42a0 127.0.0.1:6381 master - 0 1481958712921 0 connected
```

设置主从

```shell
[root@mastera0 redis]# redis-cli -p 6381 cluster replicate 8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2
OK
[root@mastera0 redis]# redis-cli -p 6383 cluster replicate 0e0958e72964fd922820ef9ed4377d10a33a2356
OK
[root@mastera0 redis]# redis-cli -p 6385 cluster replicate d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a
OK
[root@mastera0 redis]# redis-cli -p 6380 cluster nodes
fa7c7d5e866359f3863d9ef54654f3cfee8ccc4a 127.0.0.1:6385 slave d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 0 1481959454916 3 connected
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 127.0.0.1:6384 master - 0 1481959453913 3 connected
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481959452911 2 connected
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 myself,master - 0 0 1 connected
f95d8a90e129c8b9067ba1c97e77cd71508c42a0 127.0.0.1:6381 slave 8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 0 1481959454416 1 connected
ef29f1294accee3ec85d9272becbe20307f4fc9e 127.0.0.1:6383 slave 0e0958e72964fd922820ef9ed4377d10a33a2356 0 1481959455079 4 connected
```


哈希槽还没有设置

```shell
[root@mastera0 redis]# redis-cli -p 6380 cluster slots
(empty list or set)
```

0-16383 （16383是15 * 2^10）

通过cluster addslots来为节点分配槽

如果平均分配，则为每个node为5461个槽
- 0-5460
- 5461-10922
- 10923-16383 

我有三个master，分配如下：

| 节点   | node6380 | 6382        | 6384        |
| :--- | :------- | :---------- | :---------- |
| 槽范围  | 0-15999  | 16000-16200 | 16201-16383 |
| 槽数量  | 16000    | 200         | 182         |

```shell
[root@mastera0 redis]# for i in `seq 0 16000`;do redis-cli -p 6380 cluster addslots $i;done
[root@mastera0 redis]# for i in `seq 16001 16200`;do redis-cli -p 6382 cluster addslots $i;done
[root@mastera0 redis]# for i in `seq 16201 16383`;do redis-cli -p 6384 cluster addslots $i;done

[root@mastera0 redis]# redis-cli -p 6380 cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:4
cluster_my_epoch:1
cluster_stats_messages_sent:7042
cluster_stats_messages_received:7042

[root@mastera0 redis]# redis-cli -p 6380 cluster nodes|grep master
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 127.0.0.1:6384 master - 0 1481960686619 3 connected 16201-16383
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481960685617 2 connected 16001-16200
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 myself,master - 0 0 1 connected 0-16000
```

0-16383的槽是固定的，一定是连续的，否则集群的状态就会是no。

向集群中插入10000条数据

```shell
[root@mastera0 redis]# cat insert.sh
#!/bin/bash
for i in `seq 1 10000`
do
cat >> insert.file << ENDF
set $i $i
ENDF
done
[root@mastera0 redis]# bash insert.sh
[root@mastera0 redis]# tail -n 3 insert.file
set 9998 9998
set 9999 9999
set 10000 10000

[root@mastera0 redis]# time redis-cli -c -p 6380 < insert.file &> /dev/null

real	0m2.383s
user	0m0.438s
sys	0m1.024s
```

到此已经成功插入10000条记录

```shell
[root@mastera0 redis]# redis-cli -c -p 6384 
127.0.0.1:6384> get 1
-> Redirected to slot [9842] located at 127.0.0.1:6380
"1"
127.0.0.1:6380> get 2
"2"
127.0.0.1:6380> get 3
"3"
127.0.0.1:6380> get 5
"5"
127.0.0.1:6380> get 100
"100"
127.0.0.1:6380> get 1000
"1000"
127.0.0.1:6380> get 10000
"10000"
127.0.0.1:6380> exit
```

## redis数据迁移

实验目标：将9842槽（6380实例）中的数据key 1迁移到6382实例中

通过dbsize来判断数据是否丢失

数据迁移之前的总大小为30000

```shell
[root@mastera0 redis]# for i in 6380 6382 6384;do redis-cli -p $i dbsize;done|awk 'BEGIN{sum=0};{sum=$1+sum};END{print sum}'
30000
```

查看要迁移的数据在哪个槽上

1.get的时候返回信息

```shell
[root@mastera0 redis]# redis-cli -c -p 6384
127.0.0.1:6384> get 1
-> Redirected to slot [9842] located at 127.0.0.1:6380
"1"
```

2.cluster keyslot查看

```shell
[root@mastera0 redis]# redis-cli -c -p 6384 cluster keyslot 1
(integer) 9842
[root@mastera0 redis]# redis-cli -c -p 6384 cluster keyslot 10000
(integer) 15413
```

---

### slot数据迁移详细步骤

```shell
1. 保存数据 save
2. 备份数据 tar -jcf /tmp/redis.all /app/redis_cluster/  
3. 查看要迁移数据所在节点和槽
4. 开始迁移
	1）目标原节点接收原节点的槽		<old_port> cluster setslot <slot> migrating <new_node_id> 
	2）原节点移出槽到目标节点 	<new_port> cluster setslot <slot> importing <old_node_id>
	3）查看槽中key的个数		cluster countkeysinslot <slot>
	   返回槽中num个数量的key		cluster getkeysinslot <slot> <num>
	4）将槽中的key value迁移到目标槽中	<old_port> migrate <ip>  <new_port> <key> 0 1000  
 	5）将槽指派给节点			<port> cluster setslot <slot> node <node_id>
```

```shell
[root@mastera0 redis]# redis-cli -c -p 6384 cluster nodes
f95d8a90e129c8b9067ba1c97e77cd71508c42a0 127.0.0.1:6381 slave 8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 0 1481964122803 1 connected
ef29f1294accee3ec85d9272becbe20307f4fc9e 127.0.0.1:6383 slave 0e0958e72964fd922820ef9ed4377d10a33a2356 0 1481964122303 4 connected
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 127.0.0.1:6384 myself,master - 0 0 3 connected 16201-16383
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 master - 0 1481964121901 1 connected 0-16000
fa7c7d5e866359f3863d9ef54654f3cfee8ccc4a 127.0.0.1:6385 slave d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 0 1481964120798 3 connected
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481964122803 2 connected 16001-16200
[root@mastera0 redis]# redis-cli -c -p 6384 cluster keyslot 1
(integer) 9842
```

从以上查询的信息得到以下分析：

分析结果

```
slot=9842
old_port=6380
old_node_id=8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2
key=1
new_port=6382
newo_node_id=0e0958e72964fd922820ef9ed4377d10a33a2356
```

目标节点6382你愿意接收原节点6380指定的槽9842吗？

原节点6380你确定要将槽9842迁移到目标节点6382吗？

```shell
[root@mastera0 redis]# redis-cli -c -p 6382 cluster setslot 9842 importing 8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2
OK
[root@mastera0 redis]# redis-cli -c -p 6380 cluster setslot 9842 migrating 0e0958e72964fd922820ef9ed4377d10a33a2356
OK
[root@mastera0 redis]# redis-cli -c -p 6380 cluster nodes|grep master|sort -r
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 127.0.0.1:6384 master - 0 1481964395490 3 connected 16201-16383
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 myself,master - 0 0 1 connected 0-16000 [9842->-0e0958e72964fd922820ef9ed4377d10a33a2356]
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481964394488 2 connected 16001-16200
```

查看9842槽中的key

```shell
[root@mastera0 redis]# redis-cli -c -p 6380 cluster countkeysinslot 9842
(integer) 3
[root@mastera0 redis]# redis-cli -c -p 6380 cluster getkeysinslot 9842 3
1) "1"
2) "age8413"
3) "name1087"
```

将槽中的key迁移到目标节点

```shell
[root@mastera0 redis]# redis-cli -c -p 6380 migrate 127.0.0.1 6382 1 0 1000
OK
[root@mastera0 redis]# redis-cli -c -p 6380 migrate 127.0.0.1 6382 age8413 0 1000
OK
[root@mastera0 redis]# redis-cli -c -p 6380 migrate 127.0.0.1 6382 name1087 0 1000
```

双方确认槽的去向

```shell
[root@mastera0 redis]# redis-cli -c -p 6380 cluster setslot 9842 node 8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2
OK
[root@mastera0 redis]# redis-cli -c -p 6382 cluster setslot 9842 node 0e0958e72964fd922820ef9ed4377d10a33a2356
OK
[root@mastera0 redis]# redis-cli -c -p 6380 cluster nodes|grep master|sort -r
d4f9c7b0dc141a86a9d1b7b1381540d8aca04b5a 127.0.0.1:6384 master - 0 1481965375019 3 connected 16201-16383
8b60be5c7dc08c85fbf3e46854f13bb0f36f59b2 127.0.0.1:6380 myself,master - 0 0 1 connected 0-9841 9843-16000
0e0958e72964fd922820ef9ed4377d10a33a2356 127.0.0.1:6382 master - 0 1481965376021 5 connected 9842 16001-16200
```

测试

```shell
[root@mastera0 redis]# redis-cli  -p 6380 get 1
(error) MOVED 9842 127.0.0.1:6382
```
