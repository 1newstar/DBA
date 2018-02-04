# 制作u盘装机

## 格式化u盘
```shell
[root@foundation0 ~]# mount |tail -n 1
/dev/sdb1 on /run/media/kiosk/U type vfat (rw,nosuid,nodev,relatime,uid=1000,gid=1000,fmask=0022,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,showexec,utf8,flush,errors=remount-ro,uhelper=udisks2)
[root@foundation0 ~]# umount /dev/sdb1
[root@foundation0 ~]# partprobe /dev/sdb1
[root@foundation0 ~]# mkfs.ext4 /dev/sdb1
mke2fs 1.42.9 (28-Dec-2013)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
932064 inodes, 3722784 blocks
186139 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=2151677952
114 block groups
32768 blocks per group, 32768 fragments per group
8176 inodes per group
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
```
## 制作u盘启动


```shell
[root@foundation0 ~]# rht-usb usbformat /dev/sdb1
INFO     Configuration file: /root/.icrm/config.yml
INFO     Formatting USB Device: /dev/sdb1
Confirm reformatting /dev/sdb1 (y/N) y
INFO     mkfs.ext4 64-bit support
INFO     /dev/sdb1: format OK
INFO     Appear to have properly formatted USB device.

[root@foundation0 ~]# cd /home/kiosk/booboo/cache
[root@foundation0 cache]# ll
total 4038772
-rw------- 1 kiosk kiosk      27967 Mar  3  2016 ClassPrep-7.x-4.r35344.txt
-rw------- 1 kiosk kiosk      16186 Mar  3  2016 ClassroomReset-7.x-4.r35344.txt
-rw------- 1 kiosk kiosk      38605 Mar  3  2016 ClassroomSetup-7.x-4.r35344.txt
-rw------- 1 kiosk kiosk      27054 Mar  3  2016 ClassroomTroubleshooting-7.x-4.r35344.txt
-rw------- 1 kiosk kiosk      75892 Mar  3  2016 foundation0-config-7.x-4.r35344.noarch.rpm
-rw------- 1 kiosk kiosk      27568 Mar  3  2016 foundation-config-7.x-4.r35344.noarch.rpm
-rw------- 1 kiosk kiosk     189984 Mar  3  2016 redhat-survey-7.x-55.1.noarch.rpm
-rw------- 1 kiosk kiosk   91254784 Mar  4  2016 rhci-foundation-7.2-4.r35344.iso
-rw------- 1 kiosk kiosk       2775 May  9 11:02 RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf
-rw------- 1 kiosk kiosk     621805 Oct 20  2014 RHEL7和CentOS7打开屏幕VNC.pdf
-rw------- 1 kiosk kiosk 4043309056 Mar  4  2016 rhel-server-7.2-x86_64-dvd.iso
-rw------- 1 kiosk kiosk      96050 Mar  3  2016 rht-usb-7.x-4.r35344

[root@foundation0 cache]# vim /root/.icrm/config.yml
---
repository: /root/.icrm/repository
repository: /home/kiosk/booboo/cache

[root@foundation0 cache]# rht-usb verify *.icmf
INFO     Configuration file: /root/.icrm/config.yml
INFO     Verifying Cache Directory: /home/kiosk/booboo/cache

Verifying manifest file RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf
  Publish date: 2016-02-24 20:43:25
  type        md5sum  artifact-name
  ----------- ------- -----------------------------------------------
  content     CORRUPT rhel-server-7.2-x86_64-dvd.iso
  content     GOODSUM foundation-config-7.x-4.r35344.noarch.rpm
  content     GOODSUM foundation0-config-7.x-4.r35344.noarch.rpm
  content     GOODSUM redhat-survey-7.x-55.1.noarch.rpm
  content     GOODSUM rhci-foundation-7.2-4.r35344.iso
  content     GOODSUM rht-usb-7.x-4.r35344
  content     GOODSUM ClassroomSetup-7.x-4.r35344.txt
  content     GOODSUM ClassroomReset-7.x-4.r35344.txt
  content     GOODSUM ClassroomTroubleshooting-7.x-4.r35344.txt
  content     GOODSUM ClassPrep-7.x-4.r35344.txt
  content     GOODSUM RHEL7和CentOS7打开屏幕VNC.pdf
=====================================================================
WARNING  Manifest RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf failed.

WARNING  Verification FAILED - look above for problem



[root@foundation0 cache]# rht-usb usbadd RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf
INFO     Configuration file: /root/.icrm/config.yml
INFO     Adding to USB: RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf
INFO     New files needed space is 3.9G out of 3.9G
INFO     Calculation finds we need: 4135687726 bytes (3.9G)
INFO     USB space Total: 14.2G  Used: 35.5M  Free: 13.4G
INFO     Starting copy of RHCIfoundation-RHEL72-4.r35344.1-ILT-7-en_US.icmf
INFO     Copying artifact: rhel-server-7.2-x86_64-dvd.iso
INFO     Copying /home/kiosk/booboo/cache/rhel-server-7.2-x86_64-dvd.iso (3.8G) to /tmp/tmpKRYNm9/rhel7.2/x86_64/isos/rhel-server-7.2-x86_64-dvd.iso

rht-usb usbmkboot

```
