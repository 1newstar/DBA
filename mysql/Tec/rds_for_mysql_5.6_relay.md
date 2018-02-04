# RDS只读实例大表DDL导致主从延迟大

## 资料搜集

[RDS for MySQL Online DDL 使用 ](https://help.aliyun.com/knowledge_detail/41733.html)
[RDS for MySQL 如何使用 Percona Toolkit](https://help.aliyun.com/knowledge_detail/41734.html)
[RDS for MySQL 只读实例同步延迟原因与处理](https://help.aliyun.com/knowledge_detail/41767.html)
[大表上新增字段问题－－相关解决方案](http://blog.csdn.net/sollion/article/details/6095931)
[只读实例简介]( https://help.aliyun.com/document_detail/26136.html?spm=5176.2020520104.200.7.75e47270RwLjA7)
[Online DDL与pt-online-schema-change](http://www.cnblogs.com/zengkefu/p/5671661.html)
[ONLINE DDL VS PT-ONLINE-SCHEMA-CHANGE](http://www.fromdual.com/online-ddl_vs_pt-online-schema-change)

[RDS最佳实践(五)—Mysql大字段的频繁更新导致binlog暴增](https://m.th7.cn/show/51/201408/66846.html)

##初步了解客户情况

1. 目前为一主两从，数据量1.2T
2. 在线DDL后从机延迟较大

## 需进一步了解客户情况

1. 架构：当前经典网络中的一主两从架构中，从机是使用rds的只读实例吗？还是独立的rds，通过DTS同步搭建的主从？

   A：只读实例

2. 规格：当前经典网络中的主从规格是否相同呢？

   A：规格相同

3. 参数：当前经典网络中的主库中binlog_row_image参数当前的值为多少？

   A：默认参数full

4. 业务：业务高峰和低峰期分别是什么时间段？

5. ddl操作：目前在线ddl使用的工具和方法是什么？在线ddl后目前的主从延迟时间为多少？多久从机能追上主库？

   A：原生的onlineddl和ptosc都有用。最长2个小时



## 建议方法

### 只读rds搭建主从

【分析】

1. 只读节点的数据为了和主节点保持同步，采用了 MySQL 原生的 binlog 复制技术，由一个 IO 线程和**一个 SQL 线程**来完成。IO 线程负责将主库的 binlog 拉取到只读节点，SQL 线程负责消费这些 binlog 日志应用到只读实例。
2. 由于是单线程重演，所以在大表DDL时，从机延迟较大。
3. 没有办法彻底解决延迟问题。
4. 可以修改binlog_row_image值为minimal，当设置为minimal时候，binlog只记录了要修改的列的记录，这样就可以大大减小了binlog的长度，进而减少了空间的使用，对从机稍微提速。

### DTS同步搭建主从

【分析】

1. DTS同步搭建主从，从机可多线程重演，并发
2. 避免在高分期进行在线ddl操作