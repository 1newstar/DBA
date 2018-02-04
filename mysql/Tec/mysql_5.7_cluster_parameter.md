# Cluster

## galera cluster

https://my.oschina.net/u/2363376/blog/494554

```shell
(1).集群完整性检查:

wsrep_cluster_state_uuid:在集群所有节点的值应该是相同的,有不同值的节点,说明其没有连接入集群.

wsrep_cluster_conf_id:正常情况下所有节点上该值是一样的.如果值不同,说明该节点被临时"分区"了.当节点之间网络连接恢复的时候应该会恢复一样的值.

wsrep_cluster_size:如果这个值跟预期的节点数一致,则所有的集群节点已经连接.

wsrep_cluster_status:集群组成的状态.如果不为"Primary",说明出现"分区"或是"split-brain"状况.

(2).节点状态检查:

wsrep_ready: 该值为ON,则说明可以接受SQL负载.如果为Off,则需要检查wsrep_connected.

wsrep_connected: 如果该值为Off,且wsrep_ready的值也为Off,则说明该节点没有连接到集群.

wsrep_local_state_comment:如果wsrep_connected为On,但wsrep_ready为OFF,则可以从该项查看原因.

(3).复制健康检查:

 wsrep_flow_control_paused:表示复制停止了多长时间.即表明集群因为Slave延迟而慢的程度.值为0~1,越靠近0越好,值为1表示复制完全停止.可优化wsrep_slave_threads的值来改善.

wsrep_cert_deps_distance:有多少事务可以并行应用处理.wsrep_slave_threads设置的值不应该高出该值太多.

wsrep_flow_control_sent:表示该节点已经停止复制了多少次.

wsrep_local_recv_queue_avg:表示slave事务队列的平均长度.slave瓶颈的预兆.

最慢的节点的wsrep_flow_control_sent和wsrep_local_recv_queue_avg这两个值最高.这两个值较低的话,相对更好.

(4).检测慢网络问题:

wsrep_local_send_queue_avg:网络瓶颈的预兆.如果这个值比较高的话,可能存在网络瓶

(5).冲突或死锁的数目:

wsrep_last_committed:最后提交的事务数目

 wsrep_local_cert_failures和wsrep_local_bf_aborts:回滚,检测到的冲突数目
```

## innodb cluster

```shell
--group-replication-flow-control-mode=value
```

https://dev.mysql.com/doc/refman/5.7/en/group-replication-options.html