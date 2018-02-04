#!/bin/bash
# kill掉 ecshoptest库中的导致lock wait会话id
user=root
password="(Uploo00king)"
host=localhost
port=3306





mysql -u$user -p$password -h$host  -P$port -e "select concat('kill ',id,';') from information_schema.processlist,information_schema.innodb_trx  where trx_mysql_thread_id=id and trx_id in (select blocking_trx_id from (select blocking_trx_id, count(blocking_trx_id) as countnum from (select a.trx_id,a.trx_state,b.requesting_trx_id,b.blocking_trx_id from information_schema.innodb_lock_waits as  b left join information_schema.innodb_trx as a on a.trx_id=b.requesting_trx_id) as t1 group by blocking_trx_id order by  countnum desc limit 1) c) ;" > tmpfile

awk '{if (NR != 1) print $0 }' tmpfile | mysql -u$user -p$password -h$host  -P$port 


