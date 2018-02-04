# rhel 7.2 minimall to graphical

```shell
# yum grouplist
# yum -y groupinstall "Server with GUI"
# startx
# systemctl get-default
# cat /etc/inittab
# systemctl set-default graphical.target \\设置默认图形化运行级别
rm '/etc/systemd/system/default.target'
ln -s '/usr/lib/systemd/system/graphical.target' '/etc/systemd/system/default.target'
# systemctl get-default                    \\查看默认运行级别
graphical.target                           \\图形化设置OK
```

