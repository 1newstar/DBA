for i in `ps -ef|grep redi[s]|awk '{print $2}'`;do kill -9 $i;done
rm -rf /alidata/redis
yum install -y dos2unix &> /dev/null
dos2unix -n redisctl-3.2.9.sh redisctl &> /dev/null
dos2unix -n redis-3.2.9.sh redis-master-install &> /dev/null
dos2unix -n redis-3.2.9-slave.sh redis-slave-install &> /dev/null
dos2unix -n redis-sentinel-3.2.9.sh redis-sentinel-install &> /dev/null
dos2unix -n consul-0.8.5.sh consul-install &> /dev/null
for i in redisctl redis-master-install redis-slave-install redis-sentinel-install consul-install
do
	chmod a+x $i &> /dev/null
done

