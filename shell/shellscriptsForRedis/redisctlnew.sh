#!/bin/bash
#Usage: redisctl start|stop|status


# 同时启动多实例
start_redis(){
for i in `seq 6379 6478`
do /usr/local/redis-3.0.7/src/redis-server /data/redis/conf/redis${i}.conf &
done
}

# 查看所有实例的守护进程
status_redis(){
count=`ps -ef|grep "redis-server" | grep -v 'grep'|wc -l`
if [ $count == 100 ] ;then echo redis server is running ;else echo redis server is not running;fi
}

# 停止所有实例
stop_redis(){
for i in `ps -ef|grep "redis-server" | grep -v 'grep' | awk '{print $2}'`
do
	kill -9 $i
done
}

case $1 in
start)
	start_redis;;
status)
	status_redis;;
stop)
	stop_redis;;
restart)
	stop_redis;
	start_redis;;
*)
	echo "Usage: redisctl start|stop|status|restart"
esac
