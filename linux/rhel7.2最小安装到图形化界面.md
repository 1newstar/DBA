# rhel 7.2 minimall to graphical

```shell
# yum grouplist
# yum -y groupinstall "Server with GUI"
# startx
# systemctl get-default
# cat /etc/inittab
# systemctl set-default graphical.target \\����Ĭ��ͼ�λ����м���
rm '/etc/systemd/system/default.target'
ln -s '/usr/lib/systemd/system/graphical.target' '/etc/systemd/system/default.target'
# systemctl get-default                    \\�鿴Ĭ�����м���
graphical.target                           \\ͼ�λ�����OK
```

