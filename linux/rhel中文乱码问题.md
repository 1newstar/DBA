# rhel5

## 问题描述

在rhel5上打开移动硬盘，里面的中文都是乱码

尝试修改为zh_CN.UTF-8后还是乱码

## 解决方法
/etc/sysconfig/i18n

LANG="zh_CN.GB180300"

重新启动机器

如果还不行，可以检查一下bash的启动配置中是否有修改过LANG变量