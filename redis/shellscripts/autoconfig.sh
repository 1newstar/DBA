#!/bin/bash
#Usage: auto_config.sh 起始端口 实例总数
#example: auto-config.sh 6379 100
REDIS_HOME=/usr/local/redis-3.0.7
mkdir /data/redis -p
cd /data/redis
mkdir conf data log pid


for i in `seq $1 $(($1+$2-1))`
do
mkdir data/$i
grep -v '^#\|^$' $REDIS_HOME/redis.conf > /data/redis/conf/redis${i}.conf
sed -i 's/appendonly no/appendonly yes/' /data/redis/conf/redis${i}.conf
sed -i "s/port.*/port $i/" /data/redis/conf/redis${i}.conf
sed -i "s@dir.*@dir \/data\/redis\/data\/${i}@" /data/redis/conf/redis${i}.conf 
sed -i "s@pid.*@pidfile \/data\/redis\/pid\/redis${i}.pid@" /data/redis/conf/redis${i}.conf
sed -i "s@logfile.*@logfile \/data\/redis\/log\/redis${i}.log@" /data/redis/conf/redis${i}.conf
done
