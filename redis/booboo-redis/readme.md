# redis���

[TOC]

> ���ݡ�redis��ƺ�ʵ�֡��ƽ�����ѧϰ�ʼ�
>
> http://redisbook.com/

## ��������

```shell
daemonize yes #�Ƿ��Ժ�̨��������
pidfile /var/run/redis/redis-server.pid    #pid�ļ�λ��
port 6379	# �����˿ںţ�Ĭ��Ϊ 6379���������Ϊ 0 ��redis ������ socket �ϼ����κοͻ������ӡ�
bind 127.0.0.1   #�󶨵�ַ����������Ҫ���ӣ�����0.0.0.0
timeout 300     #���ӳ�ʱʱ�䣬��λ��
loglevel notice  #��־���𣬷ֱ��У�
# debug �������ڿ����Ͳ���
# verbose ������ϸ��Ϣ
# notice ����������������
# warning ��ֻ��¼����������Ϣ
logfile /var/log/redis/redis-server.log   #��־�ļ�λ��
syslog-enabled no    #�Ƿ���־�����ϵͳ��־
databases 16	#�������ݿ�������Ĭ�����ݿ�Ϊ0
hz 10 # redis�ڲ�ʱ���¼�ÿ1��10��ѭ��
```

## ��ȫ

```shell
requirepass foobared # ��Ҫ����
rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52 #�����������,���������������������� ��config
```

## RDB����

```shell
save 900 1 #ˢ�¿��յ�Ӳ���У�������������Ҫ��Żᴥ������900��֮������1���ؼ��ַ����仯��
save 300 10 #������300��֮������10���ؼ��ַ����仯��
save 60 10000 #������60��֮������10000���ؼ��ַ����仯��
stop-writes-on-bgsave-error yes #��̨�洢����ֹͣд��
rdbcompression yes #ʹ��LZFѹ��rdb�ļ���
rdbchecksum yes #�洢�ͼ���rdb�ļ�ʱУ�顣
dbfilename dump.rdb #����rdb�ļ�����
dir ./ #���ù���Ŀ¼��rdb�ļ���д���Ŀ¼��
```

## AOF����

```shell
appendonly no #�Ƿ��Ҫ��־
appendfsync no # ϵͳ����,ͳһд,�ٶȿ�
appendfsync always # ϵͳ������,ֱ��д,��,��ʧ������
appendfsync everysec #����,ÿ��д1��

no-appendfsync-on-rewrite no #Ϊyes,�������̵߳����ݷ��ڴ���,�ϲ�д��(�ٶȿ�,���׶�ʧ�Ķ�)
auto-AOF-rewrite-percentage 100 #��ǰaof�ļ����ϴ���д�Ǵ�N%ʱ��д(#��AOF��־�ļ�����������ָ���ٷֱ�ʱ��redisͨ������BGREWRITEAOF�Ƿ��Զ���дAOF��־�ļ���)
auto-AOF-rewrite-min-size 64mb #aof��д����Ҫ�ﵽ�Ĵ�С
```

## ��������

```shell
slaveof <masterip> <masterport> ��Ϊĳ̨�����Ĵӷ�����
masterauth <master-password> ������������������
slave-serve-stale-data yes # �����ӶϿ������ڸ�����,�ӷ������Ƿ�Ӧ��
slave-read-only yes #�ӷ�����ֻ��
repl-ping-slave-period 10 #��ping����ʱ����,��Ϊ��λ
repl-timeout 60 #���ӳ�ʱʱ��(��ʱ��Ϊ������),Ҫ��period��
slave-priority 100 #���master������������������ô���ڶ��slave�У�ѡ������ֵ��С��һ��slave����Ϊmaster������ֵΪ0��ʾ��������Ϊmaster��

repl-disable-tcp-nodelay no #�����Ƿ�ϲ�����,��鷢�͸�slave
slave-priority 100 �ӷ����������ȼ�,����������,���Զ���slave priority��С��Ϊ����
```

## ����

```shell
maxclients 10000 #���������
maxmemory <bytes> #���ʹ���ڴ�

maxmemory-policy volatile-lru #�ڴ浽���޺�Ĵ���
volatile-lru -> LRU�㷨ɾ������key
allkeys-lru -> LRU�㷨ɾ��key(�����ֹ�������)
volatile-random -> ���ɾ������key
allkeys-random -> ���ɾ��key(�����ֹ�������)
volatile-ttl -> ɾ������ڵ�key
noeviction -> ��ɾ��,���ش�����Ϣ

#���� LRU ttl���ǽ����㷨,����ѡN��,�ٱȽ�������T�߳�������
maxmemory-samples 3
```

## ����ѯ

```shell
slowlog-log-slower-than 10000 #��¼��Ӧʱ�����10000΢�������ѯ
slowlog-max-len 128 # ����¼128��
```


## �߼�����

```shell
hash-max-zipmap-entries 512   #��ϣ����Ԫ�أ���Ŀ���ܸ����������趨����ʱ���������Խ��ո�ʽ�洢����ʡ�ռ�
hash-max-zipmap-value 64     #��ϣ����ÿ��value�ĳ��Ȳ����������ֽ�ʱ���������Խ��ո�ʽ�洢����ʡ�ռ�
list-max-ziplist-entries 512  #list�������Ͷ��ٽڵ����»����ȥָ��Ľ��մ洢��ʽ
list-max-ziplist-value 64    #list�������ͽڵ�ֵ��СС�ڶ����ֽڻ���ý��մ洢��ʽ
set-max-intset-entries 512   #set���������ڲ��������ȫ������ֵ�ͣ��Ұ������ٽڵ����»���ý��ո�ʽ�洢
activerehashing yes        #�Ƿ񼤻����ù�ϣ
```



## ����˳�������

```shell
time ����ʱ���+΢��
dbsize ����key������
bgrewriteaof ��дaof
bgsave ��̨�����ӽ���dump����
save ��������dump����
lastsave

slaveof host port ��host port�Ĵӷ�����(�������,������������)
slaveof no one �����������(ԭ���ݲ���ʧ,һ����������ʧ�ܺ�)

flushdb ��յ�ǰ���ݿ����������
flushall ����������ݿ����������(��������ô��?)

shutdown [save/nosave] �رշ�����,��������,�޸�AOF(�������)

slowlog get ��ȡ����ѯ��־
slowlog len ��ȡ����ѯ��־����
slowlog reset �������ѯ


info []

config get ѡ��(֧��*ͨ��)
config set ѡ�� ֵ
config rewrite ��ֵд�������ļ�
config restart ����info�������Ϣ

debug object key #����ѡ��,��һ��key�����
debug segfault #ģ��δ���,�÷���������
object key (refcount|encoding|idletime)
monitor #�򿪿���̨,�۲�����(������)
client list #�г���������
client kill #ɱ��ĳ������ CLIENT KILL 127.0.0.1:43501
client getname #��ȡ���ӵ����� Ĭ��nil
client setname "����" #������������,���ڵ���
```


## ��������

```shell
auth ���� #�����½(���������)
ping #���Է������Ƿ����
echo "some content" #���Է������Ƿ���������
select 0/1/2... #ѡ�����ݿ�
quit #�˳�����
```

## �־û���ʽ

### redis�ṩ���ֳ־û�����

```shell

 a). RDB�־û�

 ������ʽ ������ʱ��ļ����redis�����ݿ��գ�dump����dump.rdb�ļ�

 ���� �����ݻָ��򵥡�RDBͨ���ӽ�����ɳ־û���������Ա�AOF����Ч�ʸ�

 ���� �����������ϻᶪʧ�������ڵ�����

 b). AOF�־û�

 ������ʽ ������־����ʽ��¼���и��²�����AOF��־�ļ�����redis������������ʱ���ȡ����־�� �������¹������ݿ⣬�Ա�֤���������������ԡ�

 ���� ��AOF�ṩ����ͬ�����ƣ�һ����fsync alwaysÿ�������ݱ仯��ͬ������־�ļ���fsync everysecÿ��ͬ��һ�ε���־�ļ�������޶ȱ�֤���������ԡ�

 ���ƣ���־�ļ����RDB�����ļ�Ҫ��Ķ�

 AOF��־��д���� ��AOF��־�ļ�����redis���Զ���дAOF��־��appendģʽ���ϵĽ����¼�¼д�뵽����־�ļ��У�ͬʱredis���ᴴ��һ���µ���־�ļ�����׷�Ӻ����ļ�¼��

 c). ͬʱӦ��AOF��RDB

 �������ݰ�ȫ�Ըߵĳ�������ͬʱʹ��AOF��RDB�������ή�����ܡ�

 d). �޳־û�

 ����redis����־û����ܡ�
```

### AOF��־�ļ�������޸����� 

```shell
redis-check-aof --fix appendonly.aof  #--fix����Ϊ�޸���־�ļ������������־���
```

### ������redis��RDB�־û��л���AOF�־û� ��

```shell
redis-cli> CONFIG SET appendonly yes      #����AOF
redis-cli> CONFIG SET save ""         #�ر�RDB
```






