#!/bin/bash
#Usage: auto_config.sh 起始端口 实例总数 masterip masterport
#example: auto-config.sh 6379 100 127.0.0.1 6379
REDIS_HOME=/usr/local/redis-3.2.9
mkdir /data/redis -p &> /dev/null
cd /data/redis &> /dev/null
mkdir conf data log pid &> /dev/null
masterip=$3
masterport=$4

for i in `seq $1 $(($1+$2-1))`
do
mkdir data/$i $> /dev/null
grep -v '^#\|^$' $REDIS_HOME/redis.conf > /data/redis/conf/redis${i}.conf
sed -i 's/appendonly no/appendonly yes/' /data/redis/conf/redis${i}.conf
sed -i "s/port.*/port $i/" /data/redis/conf/redis${i}.conf
sed -i "s@dir.*@dir \/data\/redis\/data\/${i}@" /data/redis/conf/redis${i}.conf
sed -i "s@pid.*@pidfile \/data\/redis\/pid\/redis${i}.pid@" /data/redis/conf/redis${i}.conf
sed -i "s@logfile.*@logfile \/data\/redis\/log\/redis${i}.log@" /data/redis/conf/redis${i}.conf
sed -i "21islaveof ${masterip} ${masterport}" /data/redis/conf/redis${i}.conf
done
