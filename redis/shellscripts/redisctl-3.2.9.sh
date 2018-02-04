#!/bin/bash
#Usage: redisctl start|stop|status port num
# redisctl start 6379 1


# 同时启动多实例
start_redis(){
for i in `seq $1 $(($1+$2-1))`
do 
	nohup /alidata/redis/src/redis-server /alidata/redis/conf/redis${i}.conf &> /dev/null &
done
}

# 查看所有实例的守护进程
status_redis(){
count=`ps -ef|grep "redis-server" | grep -v 'grep'|wc -l`
if [[ $count == $1 ]] ;then echo redis server is running ;else echo redis server is not running;fi
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
	start_redis $2 $3;;
status)
	status_redis $3;;
stop)
	stop_redis;;
restart)
	stop_redis;
	start_redis $2 $3;;
*)
	echo "Usage: redisctl start|stop|status|restart port num"
esac
