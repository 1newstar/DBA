#!/bin/bash

# redis多实例安装
# Usage： bash redis-3.2.9.sh 6379 6 #配置6个实例，监听端口从6379到6384

if [ $# -ne 0 ]
then
	# 创建软件目录
	mkdir -p /alidata/redis &> /dev/null 
	cd /alidata/redis &> /dev/null
	mkdir conf data log pid &> /dev/null
	mkdir -p /alidata/install &> /dev/null
	cd /alidata/install

	# 下载软件并编译安装
	if [ ! -f /alidata/redis/src/redis-server ] 
	then
		wget http://download.redis.io/releases/redis-3.2.9.tar.gz
		tar -xf redis-3.2.9.tar.gz
		cd redis-3.2.9
		make && make install
		mv /alidata/install/redis-3.2.9/* /alidata/redis
	fi

	# 创建配置文件
	cd /alidata/redis

	for i in `seq $1 $(($1+$2-1))`
	do
		mkdir data/$i &> /dev/null
		grep -v '^#\|^$' redis.conf > /alidata/redis/conf/redis${i}.conf
		sed -i 's/appendonly no/appendonly yes/' /alidata/redis/conf/redis${i}.conf
		sed -i "s/port.*/port $i/" /alidata/redis/conf/redis${i}.conf
		sed -i "s@dir.*@dir \/data\/redis\/data\/${i}@" /alidata/redis/conf/redis${i}.conf 
		sed -i "s@pid.*@pidfile \/data\/redis\/pid\/redis${i}.pid@" /alidata/redis/conf/redis${i}.conf
		sed -i "s@logfile.*@logfile \/data\/redis\/log\/redis${i}.log@" /alidata/redis/conf/redis${i}.conf
	done

	# 优化路径和命令
	if ! cat /etc/profile | grep "export PATH=\$PATH:/alidata/redis/src" &> /dev/null;then
		echo "export PATH=\$PATH:/alidata/redis/src" >> /etc/profile
	fi
	source /etc/profile

	# 检查安装结果
	which redis-server
	which redis-cli
	ls -l /alidata/redis;ls -l /alidata/redis/conf
else
	echo "Usage： bash redis-3.2.9.sh 6379 6 #配置6个实例，监听端口从6379到6384"
fi
