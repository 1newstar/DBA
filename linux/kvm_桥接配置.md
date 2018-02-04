# kvm 桥接配置

网络设计概览
宿主		172.25.254.1/24
虚拟机两台：
rhel6.5-2	172.25.254.11/24
servera		172.25.254.10/24

宿主：

```shell
[root@localhost network-scripts]# cat ifcfg-br0
DEVICE=br0
TYPE=Bridge
NAME=br0
ONBOOT=yes
BOOTPROTO=none
IPADDR0=172.25.254.1
PREFIX0=24
GATEWAY0=172.25.254.254
DEFROUTE=yes
IPADDR1=172.25.1.250
PREFIX1=24
DNS1=172.25.254.250
PEERDNS=yes
TYPE=Bridge
DEFROUTE=yes
DELAY=0
STP=no
[root@localhost network-scripts]# cat ifcfg-enp4s0f1 
TYPE=Ethernet
BOOTPROTO=none
NAME=enp4s0f1
UUID=594f612f-5ef6-4e28-810c-3db501f027d5
DEVICE=enp4s0f1
ONBOOT=yes
BRIDGE=br0
[root@localhost network-scripts]# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.80fa5b09146d	no		enp4s0f1
							vnet0
							vnet1
virbr0		8000.5254004cb17a	yes		virbr0-nic
[root@localhost network-scripts]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.25.254.254  0.0.0.0         UG    425    0        0 br0
172.25.1.0      0.0.0.0         255.255.255.0   U     425    0        0 br0
172.25.254.0    0.0.0.0         255.255.255.0   U     425    0        0 br0
192.168.122.0   0.0.0.0         255.255.255.0   U     0      0        0 virbr0
```


\---------------------------------------------------------------------
虚拟机
添加网卡，选择桥接br0 设备型号选择virtio
重新启动虚拟机
\--------------------------------------------------------------------
servera 
该虚拟机是最小化安装的rhel 6.5，因此没有安装NetworkManager软件服务，只需要配置network服务即可
servera重启之后的ifcfg-eth0配置如下

```shell
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0 
DEVICE=eth0
HWADDR=52:54:00:F7:77:B9
TYPE=Ethernet
UUID=06f58e0b-6dbc-4f12-91f2-ffa3a7b518fc
ONBOOT=yes
NM_CONTROLLED=yes
BOOTPROTO=DHCP
```

需要由dhcp动态获取ip改成手动的，如下所示：（因为没有dhcp服务器，因此当前没法动态获取ip的，当然如果你会搭建dhcp服务器，就可以通过dhcp获取ip了）

```shell
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0 
DEVICE=eth0
HWADDR=52:54:00:F7:77:B9
TYPE=Ethernet
UUID=06f58e0b-6dbc-4f12-91f2-ffa3a7b518fc
ONBOOT=yes
NM_CONTROLLED=yes
BOOTPROTO=none
IPADDR=172.25.254.10
PREFIX=255.255.255.0
GATEWAY=172.25.254.254
PREFIX=255.255.255.0
```

接着重新启动服务即可

```shell
service network restart

[root@localhost ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 52:54:00:F7:77:B9  
          inet addr:172.25.254.10  Bcast:172.25.255.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fef7:77b9/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:400 errors:0 dropped:0 overruns:0 frame:0
          TX packets:99 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:68111 (66.5 KiB)  TX bytes:12427 (12.1 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:684 (684.0 b)  TX bytes:684 (684.0 b)
```



rhel6.5-2

该虚拟机是图形化界面安装的rhel6.5，管理网络的服务有两个，一个是network，另一个是NetworkManager
因此，我们可以选择一个服务来管理，
第一种方法，使用network服务

首先需要关闭NetworkManager服务

```shell
service NetworkManager stop
chkconfig NetworkManager off
reboot
```

在kvm图像化界面中删除网卡，重新添加网卡,重启虚拟机
52:54:00:3a:b8:0e

首先通过ip addr查看一下虚拟机网卡名称

```shell
[root@localhost ~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:54:00:3a:b8:0e brd ff:ff:ff:ff:ff:ff

根据网卡名称eth5，手动创建ifcfg-eth5的配置文件，需要用到添加网卡时分配到的网卡mac地址
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth5 
DEVICE=eth5
HWADDR=52:54:00:3a:b8:0e
TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=none
IPADDR=172.25.254.11
PREFIX=24
GATEWAY=172.25.254.254
PREFIX=24

重新启动服务
service network restart
```

第二种方法，使用NetworkManager服务
自己摸索吧  *.*

\-------------------------------------------------------

现在可以到宿主机上通过ssh远程登陆了哈！

远程连接rhel6.5-2

```shell
[root@localhost ~]# ssh root@172.25.254.11
root@172.25.254.11's password: 
Last login: Thu Sep 22 13:27:46 2016 from 172.25.254.1
[root@localhost ~]# exit
logout
Connection to 172.25.254.11 closed.
```

远程连接servera

```shell
[root@localhost ~]# ssh root@172.25.254.10
root@172.25.254.10's password: 
Last login: Thu Sep 22 13:04:49 2016 from 172.25.254.1
[root@localhost ~]# exit
logout
Connection to 172.25.254.10 closed.
[root@localhost ~]# 
```

你学会了吗？以后应该都能配置了吧 ^ ^
















