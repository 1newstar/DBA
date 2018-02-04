# 在线yum源安装mplayer 和 splayer

> splayer比mplayer好用

### 安装mplayer

1. 安装在线yum源两个

https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

https://mirrors.tuna.tsinghua.edu.cn/epel/7/x86_64/e/epel-release-7-9.noarch.rpm

2. 依次安装所需要的各种软件

yum -y install mplayer              播放器主程序，约15MB

yum -y install mplayer-gui          图形界面的壳，约230KB

yum -y install ffmpeg*              各种解码器，约22MB

3. 播放时候如果用命令行方式，

mplayer abc.mp3
 
4. 查看mplayer的说明书

man mplayer
 
5. 如果用图形界面，下面命令启动图形界面

gmplayer
 


```shell
[root@foundation0 yum.repos.d]# curl -O https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6140  100  6140    0     0   1750      0  0:00:03  0:00:03 --:--:--  1751
[root@foundation0 yum.repos.d]# ll
total 20
drwxr-xr-x  2 root root  139 Jun 10 22:53 booboo
-rw-r--r--. 1 root root  358 Jun  6 05:51 redhat.repo
-rw-r--r--. 1 root root  100 Jun  6 05:53 rhel-dvd.repo
-rw-r--r--. 1 root root   64 Jun  6 05:53 rht-ucf.repo
-rw-r--r--  1 root root 6140 Jun 10 22:51 rpmfusion-free-release-7.noarch.rpm
[root@foundation0 yum.repos.d]# rpm -ivh rpmfusion-free-release-7.noarch.rpm 
warning: rpmfusion-free-release-7.noarch.rpm: Header V4 RSA/SHA1 Signature, key ID f5cf6c1e: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:rpmfusion-free-release-7-1       ################################# [100%]
[root@foundation0 yum.repos.d]# ll
total 28
drwxr-xr-x  2 root root  139 Jun 10 22:53 booboo
-rw-r--r--. 1 root root  358 Jun  6 05:51 redhat.repo
-rw-r--r--. 1 root root  100 Jun  6 05:53 rhel-dvd.repo
-rw-r--r--. 1 root root   64 Jun  6 05:53 rht-ucf.repo
-rw-r--r--  1 root root 6140 Jun 10 22:51 rpmfusion-free-release-7.noarch.rpm
-rw-r--r--  1 root root 1002 Sep 15  2016 rpmfusion-free-updates.repo
-rw-r--r--  1 root root 1062 Sep 15  2016 rpmfusion-free-updates-testing.repo
[root@foundation0 yum.repos.d]# yum clean all
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Cleaning repos: rhel-dvd rht-ext rpmfusion-free-updates
Cleaning up everything
[root@foundation0 yum.repos.d]# yum makecache
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
rhel-dvd                                                                                                                                                              | 4.1 kB  00:00:00     
rht-ext                                                                                                                                                               | 2.9 kB  00:00:00     
rpmfusion-free-updates                                                                                                                                                | 3.0 kB  00:00:00     
(1/10): rhel-dvd/group_gz                                                                                                                                             | 136 kB  00:00:00     
(2/10): rhel-dvd/filelists_db                                                                                                                                         | 3.2 MB  00:00:00     
(3/10): rhel-dvd/primary_db                                                                                                                                           | 3.6 MB  00:00:00     
(4/10): rhel-dvd/other_db                                                                                                                                             | 1.4 MB  00:00:00     
(5/10): rht-ext/filelists_db                                                                                                                                          | 1.5 kB  00:00:00     
(6/10): rht-ext/primary_db                                                                                                                                            | 2.3 kB  00:00:00     
(7/10): rht-ext/other_db                                                                                                                                              | 1.2 kB  00:00:00     
(8/10): rpmfusion-free-updates/x86_64/filelists_db                                                                                                                    | 123 kB  00:00:00     
(9/10): rpmfusion-free-updates/x86_64/other_db                                                                                                                        |  46 kB  00:00:00     
(10/10): rpmfusion-free-updates/x86_64/primary_db                                                                                                                     | 166 kB  00:01:03     
Metadata Cache Created
[root@foundation0 yum.repos.d]# yum install -y mplayer 
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: mplayer-common = 1.1-23.20140414svn.el7 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: faad2-libs >= 1:2.6.1 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3(LIBSWSCALE_3)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53(LIBPOSTPROC_53)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54(LIBAVUTIL_54)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56(LIBAVFORMAT_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56(LIBAVCODEC_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libxvidcore.so.4()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libx264.so.148()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libvdpau.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: librtmp.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpg123.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpeg2.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmp3lame.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liblirc_client.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfaad.so.2()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libenca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libdca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libcaca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libbs2b.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libaa.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liba52.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libXss.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Running transaction check
---> Package a52dec.x86_64 0:0.7.4-21.el7 will be installed
---> Package faad2-libs.x86_64 1:2.7-8.el7 will be installed
---> Package ffmpeg-libs.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libx265.so.79()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libvo-amrwbenc.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libva.so.1()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libsoxr.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libschroedinger-1.0.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrwb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrnb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
---> Package lame-libs.x86_64 0:3.99.5-6.el7 will be installed
---> Package libXScrnSaver.x86_64 0:1.2.2-6.1.el7 will be installed
---> Package libdca.x86_64 0:0.0.5-9.el7 will be installed
---> Package libmpeg2.x86_64 0:0.5.1-10.el7 will be installed
---> Package librtmp.x86_64 0:2.4-7.20160224.gitfa8646d.el7 will be installed
---> Package libvdpau.x86_64 0:1.1-2.el7 will be installed
---> Package mpg123-libs.x86_64 0:1.23.6-2.el7 will be installed
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: liblirc_client.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libenca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libcaca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libbs2b.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libaa.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
---> Package mplayer-common.x86_64 0:1.1-23.20140414svn.el7 will be installed
---> Package x264-libs.x86_64 0:0.148-11.20160614gita5e06b9.el7 will be installed
---> Package xvidcore.x86_64 0:1.3.4-2.el7 will be installed
--> Running transaction check
---> Package ffmpeg-libs.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libva.so.1()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libsoxr.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libschroedinger-1.0.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: liblirc_client.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libenca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libcaca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libbs2b.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libaa.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
---> Package opencore-amr.x86_64 0:0.1.3-3.el7 will be installed
---> Package vo-amrwbenc.x86_64 0:0.1.3-1.el7 will be installed
---> Package x265-libs.x86_64 0:1.9-4.el7 will be installed
--> Finished Dependency Resolution
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libass.so.5()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libcaca.so.0()(64bit)
Error: Package: ffmpeg-libs-2.8.11-1.el7.x86_64 (rpmfusion-free-updates)
           Requires: libass.so.5()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libbs2b.so.0()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libfribidi.so.0()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libenca.so.0()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: liblirc_client.so.0()(64bit)
Error: Package: ffmpeg-libs-2.8.11-1.el7.x86_64 (rpmfusion-free-updates)
           Requires: libschroedinger-1.0.so.0()(64bit)
Error: Package: ffmpeg-libs-2.8.11-1.el7.x86_64 (rpmfusion-free-updates)
           Requires: libsoxr.so.0()(64bit)
Error: Package: ffmpeg-libs-2.8.11-1.el7.x86_64 (rpmfusion-free-updates)
           Requires: libva.so.1()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libaa.so.1()(64bit)
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
[root@foundation0 yum.repos.d]# mv booboo/epel.repo .
[root@foundation0 yum.repos.d]# vim epel.repo 
[root@foundation0 yum.repos.d]# yum makecache
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
epel/x86_64/metalink                                                                                                                                                  | 5.3 kB  00:00:00     
epel-debuginfo/x86_64/metalink                                                                                                                                        | 5.4 kB  00:00:00     
epel-debuginfo                                                                                                                                                        | 3.0 kB  00:00:00     
epel-source/x86_64/metalink                                                                                                                                           | 5.3 kB  00:00:00     
epel-source                                                                                                                                                           | 3.5 kB  00:00:00     
rhel-dvd                                                                                                                                                              | 4.1 kB  00:00:00     
rht-ext                                                                                                                                                               | 2.9 kB  00:00:00     
rpmfusion-free-updates                                                                                                                                                | 3.0 kB  00:00:00     
(1/7): epel-debuginfo/x86_64/filelists_db                                                                                                                             | 3.6 MB  00:00:06     
(2/7): epel-debuginfo/x86_64/primary_db                                                                                                                               | 632 kB  00:00:01     
(3/7): epel-debuginfo/x86_64/other_db                                                                                                                                 | 662 kB  00:00:01     
(4/7): epel-source/x86_64/filelists_db                                                                                                                                | 483 kB  00:00:01     
(5/7): epel-source/x86_64/updateinfo                                                                                                                                  | 805 kB  00:00:01     
(6/7): epel-source/x86_64/primary_db                                                                                                                                  | 1.7 MB  00:00:03     
(7/7): epel-source/x86_64/other_db                                                                                                                                    | 1.4 MB  00:00:01     
Metadata Cache Created
[root@foundation0 yum.repos.d]# yum install -y mplayer
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: mplayer-common = 1.1-23.20140414svn.el7 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: faad2-libs >= 1:2.6.1 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3(LIBSWSCALE_3)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53(LIBPOSTPROC_53)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54(LIBAVUTIL_54)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56(LIBAVFORMAT_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56(LIBAVCODEC_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libxvidcore.so.4()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libx264.so.148()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libvdpau.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: librtmp.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpg123.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpeg2.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmp3lame.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liblirc_client.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfaad.so.2()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libenca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libdca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libcaca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libbs2b.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libaa.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liba52.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libXss.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Running transaction check
---> Package a52dec.x86_64 0:0.7.4-21.el7 will be installed
---> Package aalib-libs.x86_64 0:1.4.0-0.22.rc5.el7 will be installed
---> Package enca.x86_64 0:1.18-1.el7 will be installed
---> Package faad2-libs.x86_64 1:2.7-8.el7 will be installed
---> Package ffmpeg-libs.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libx265.so.79()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libvo-amrwbenc.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libva.so.1()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libsoxr.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libschroedinger-1.0.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrwb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrnb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
---> Package lame-libs.x86_64 0:3.99.5-6.el7 will be installed
---> Package libXScrnSaver.x86_64 0:1.2.2-6.1.el7 will be installed
---> Package libass.x86_64 0:0.13.4-1.el7 will be installed
--> Processing Dependency: libfribidi.so.0()(64bit) for package: libass-0.13.4-1.el7.x86_64
---> Package libbs2b.x86_64 0:3.1.0-13.el7 will be installed
---> Package libcaca.x86_64 0:0.99-0.17.beta17.el7 will be installed
--> Processing Dependency: libglut.so.3()(64bit) for package: libcaca-0.99-0.17.beta17.el7.x86_64
---> Package libdca.x86_64 0:0.0.5-9.el7 will be installed
---> Package libmpeg2.x86_64 0:0.5.1-10.el7 will be installed
---> Package librtmp.x86_64 0:2.4-7.20160224.gitfa8646d.el7 will be installed
---> Package libvdpau.x86_64 0:1.1-2.el7 will be installed
---> Package lirc-libs.x86_64 0:0.9.1a-4.el7 will be installed
---> Package mpg123-libs.x86_64 0:1.23.6-2.el7 will be installed
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
---> Package mplayer-common.x86_64 0:1.1-23.20140414svn.el7 will be installed
---> Package x264-libs.x86_64 0:0.148-11.20160614gita5e06b9.el7 will be installed
---> Package xvidcore.x86_64 0:1.3.4-2.el7 will be installed
--> Running transaction check
---> Package freeglut.x86_64 0:2.8.1-3.el7 will be installed
---> Package libass.x86_64 0:0.13.4-1.el7 will be installed
--> Processing Dependency: libfribidi.so.0()(64bit) for package: libass-0.13.4-1.el7.x86_64
---> Package libva.x86_64 0:1.2.1-3.el7 will be installed
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: libfribidi.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
---> Package opencore-amr.x86_64 0:0.1.3-3.el7 will be installed
---> Package schroedinger.x86_64 0:1.0.11-4.el7 will be installed
---> Package soxr.x86_64 0:0.1.2-1.el7 will be installed
---> Package vo-amrwbenc.x86_64 0:0.1.3-1.el7 will be installed
---> Package x265-libs.x86_64 0:1.9-4.el7 will be installed
--> Finished Dependency Resolution
Error: Package: libass-0.13.4-1.el7.x86_64 (epel)
           Requires: libfribidi.so.0()(64bit)
Error: Package: mplayer-1.1-23.20140414svn.el7.x86_64 (rpmfusion-free-updates)
           Requires: libfribidi.so.0()(64bit)
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
[root@foundation0 yum.repos.d]# rpm -ivh http://mirror.centos.org/centos/7/os/x86_64/Packages/fribidi-0.19.4-6.el7.x86_64.rpm
Retrieving http://mirror.centos.org/centos/7/os/x86_64/Packages/fribidi-0.19.4-6.el7.x86_64.rpm
warning: /var/tmp/rpm-tmp.qADbT2: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:fribidi-0.19.4-6.el7             ################################# [100%]
[root@foundation0 yum.repos.d]# yum install -y mplayer
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package mplayer.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: mplayer-common = 1.1-23.20140414svn.el7 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: faad2-libs >= 1:2.6.1 for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3(LIBSWSCALE_3)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53(LIBPOSTPROC_53)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54(LIBAVUTIL_54)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56(LIBAVFORMAT_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56(LIBAVCODEC_56)(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libxvidcore.so.4()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libx264.so.148()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libvdpau.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libswscale.so.3()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: librtmp.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libpostproc.so.53()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpg123.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmpeg2.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libmp3lame.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liblirc_client.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libfaad.so.2()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libenca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libdca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libcaca.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libbs2b.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavutil.so.54()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavformat.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libavcodec.so.56()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libass.so.5()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libaa.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: liba52.so.0()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Processing Dependency: libXss.so.1()(64bit) for package: mplayer-1.1-23.20140414svn.el7.x86_64
--> Running transaction check
---> Package a52dec.x86_64 0:0.7.4-21.el7 will be installed
---> Package aalib-libs.x86_64 0:1.4.0-0.22.rc5.el7 will be installed
---> Package enca.x86_64 0:1.18-1.el7 will be installed
---> Package faad2-libs.x86_64 1:2.7-8.el7 will be installed
---> Package ffmpeg-libs.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libx265.so.79()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libvo-amrwbenc.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libva.so.1()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libsoxr.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libschroedinger-1.0.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrwb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
--> Processing Dependency: libopencore-amrnb.so.0()(64bit) for package: ffmpeg-libs-2.8.11-1.el7.x86_64
---> Package lame-libs.x86_64 0:3.99.5-6.el7 will be installed
---> Package libXScrnSaver.x86_64 0:1.2.2-6.1.el7 will be installed
---> Package libass.x86_64 0:0.13.4-1.el7 will be installed
---> Package libbs2b.x86_64 0:3.1.0-13.el7 will be installed
---> Package libcaca.x86_64 0:0.99-0.17.beta17.el7 will be installed
--> Processing Dependency: libglut.so.3()(64bit) for package: libcaca-0.99-0.17.beta17.el7.x86_64
---> Package libdca.x86_64 0:0.0.5-9.el7 will be installed
---> Package libmpeg2.x86_64 0:0.5.1-10.el7 will be installed
---> Package librtmp.x86_64 0:2.4-7.20160224.gitfa8646d.el7 will be installed
---> Package libvdpau.x86_64 0:1.1-2.el7 will be installed
---> Package lirc-libs.x86_64 0:0.9.1a-4.el7 will be installed
---> Package mpg123-libs.x86_64 0:1.23.6-2.el7 will be installed
---> Package mplayer-common.x86_64 0:1.1-23.20140414svn.el7 will be installed
---> Package x264-libs.x86_64 0:0.148-11.20160614gita5e06b9.el7 will be installed
---> Package xvidcore.x86_64 0:1.3.4-2.el7 will be installed
--> Running transaction check
---> Package freeglut.x86_64 0:2.8.1-3.el7 will be installed
---> Package libva.x86_64 0:1.2.1-3.el7 will be installed
---> Package opencore-amr.x86_64 0:0.1.3-3.el7 will be installed
---> Package schroedinger.x86_64 0:1.0.11-4.el7 will be installed
---> Package soxr.x86_64 0:0.1.2-1.el7 will be installed
---> Package vo-amrwbenc.x86_64 0:0.1.3-1.el7 will be installed
---> Package x265-libs.x86_64 0:1.9-4.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=============================================================================================================================================================================================
 Package                                  Arch                             Version                                                    Repository                                        Size
=============================================================================================================================================================================================
Installing:
 mplayer                                  x86_64                           1.1-23.20140414svn.el7                                     rpmfusion-free-updates                           1.1 M
Installing for dependencies:
 a52dec                                   x86_64                           0.7.4-21.el7                                               rpmfusion-free-updates                            57 k
 aalib-libs                               x86_64                           1.4.0-0.22.rc5.el7                                         epel                                              65 k
 enca                                     x86_64                           1.18-1.el7                                                 epel                                             107 k
 faad2-libs                               x86_64                           1:2.7-8.el7                                                rpmfusion-free-updates                           149 k
 ffmpeg-libs                              x86_64                           2.8.11-1.el7                                               rpmfusion-free-updates                           5.5 M
 freeglut                                 x86_64                           2.8.1-3.el7                                                rhel-dvd                                         183 k
 lame-libs                                x86_64                           3.99.5-6.el7                                               rpmfusion-free-updates                           343 k
 libXScrnSaver                            x86_64                           1.2.2-6.1.el7                                              rhel-dvd                                          24 k
 libass                                   x86_64                           0.13.4-1.el7                                               epel                                              92 k
 libbs2b                                  x86_64                           3.1.0-13.el7                                               epel                                              24 k
 libcaca                                  x86_64                           0.99-0.17.beta17.el7                                       epel                                             216 k
 libdca                                   x86_64                           0.0.5-9.el7                                                rpmfusion-free-updates                           102 k
 libmpeg2                                 x86_64                           0.5.1-10.el7                                               rpmfusion-free-updates                            66 k
 librtmp                                  x86_64                           2.4-7.20160224.gitfa8646d.el7                              rpmfusion-free-updates                            71 k
 libva                                    x86_64                           1.2.1-3.el7                                                epel                                              68 k
 libvdpau                                 x86_64                           1.1-2.el7                                                  rhel-dvd                                          32 k
 lirc-libs                                x86_64                           0.9.1a-4.el7                                               epel                                              39 k
 mpg123-libs                              x86_64                           1.23.6-2.el7                                               rpmfusion-free-updates                           191 k
 mplayer-common                           x86_64                           1.1-23.20140414svn.el7                                     rpmfusion-free-updates                           1.2 M
 opencore-amr                             x86_64                           0.1.3-3.el7                                                rpmfusion-free-updates                           173 k
 schroedinger                             x86_64                           1.0.11-4.el7                                               epel                                             291 k
 soxr                                     x86_64                           0.1.2-1.el7                                                epel                                              77 k
 vo-amrwbenc                              x86_64                           0.1.3-1.el7                                                rpmfusion-free-updates                            71 k
 x264-libs                                x86_64                           0.148-11.20160614gita5e06b9.el7                            rpmfusion-free-updates                           556 k
 x265-libs                                x86_64                           1.9-4.el7                                                  rpmfusion-free-updates                           1.5 M
 xvidcore                                 x86_64                           1.3.4-2.el7                                                rpmfusion-free-updates                           263 k

Transaction Summary
=============================================================================================================================================================================================
Install  1 Package (+26 Dependent packages)

Total download size: 12 M
Installed size: 38 M
Downloading packages:
(1/24): aalib-libs-1.4.0-0.22.rc5.el7.x86_64.rpm                                                                                                                      |  65 kB  00:00:00     
(2/24): enca-1.18-1.el7.x86_64.rpm                                                                                                                                    | 107 kB  00:00:00     
warning: /var/cache/yum/x86_64/7Server/rpmfusion-free-updates/packages/a52dec-0.7.4-21.el7.x86_64.rpm: Header V4 RSA/SHA1 Signature, key ID f5cf6c1e: NOKEY
Public key for a52dec-0.7.4-21.el7.x86_64.rpm is not installed
(3/24): a52dec-0.7.4-21.el7.x86_64.rpm                                                                                                                                |  57 kB  00:00:00     
(4/24): libass-0.13.4-1.el7.x86_64.rpm                                                                                                                                |  92 kB  00:00:00     
(5/24): libbs2b-3.1.0-13.el7.x86_64.rpm                                                                                                                               |  24 kB  00:00:00     
(6/24): libcaca-0.99-0.17.beta17.el7.x86_64.rpm                                                                                                                       | 216 kB  00:00:01     
(7/24): libdca-0.0.5-9.el7.x86_64.rpm                                                                                                                                 | 102 kB  00:00:05     
(8/24): librtmp-2.4-7.20160224.gitfa8646d.el7.x86_64.rpm                                                                                                              |  71 kB  00:00:02     
(9/24): libva-1.2.1-3.el7.x86_64.rpm                                                                                                                                  |  68 kB  00:00:01     
(10/24): lirc-libs-0.9.1a-4.el7.x86_64.rpm                                                                                                                            |  39 kB  00:00:00     
(11/24): ffmpeg-libs-2.8.11-1.el7.x86_64.rpm                                                                                                                          | 5.5 MB  00:00:10     
(12/24): mplayer-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                                    | 1.1 MB  00:00:02     
(13/24): lame-libs-3.99.5-6.el7.x86_64.rpm                                                                                                                            | 343 kB  00:00:14     
(14/24): mplayer-common-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                             | 1.2 MB  00:00:02     
(15/24): schroedinger-1.0.11-4.el7.x86_64.rpm                                                                                                                         | 291 kB  00:00:00     
(16/24): soxr-0.1.2-1.el7.x86_64.rpm                                                                                                                                  |  77 kB  00:00:00     
(17/24): vo-amrwbenc-0.1.3-1.el7.x86_64.rpm                                                                                                                           |  71 kB  00:00:00     
(18/24): mpg123-libs-1.23.6-2.el7.x86_64.rpm                                                                                                                          | 191 kB  00:00:05     
(19/24): x264-libs-0.148-11.20160614gita5e06b9.el7.x86_64.rpm                                                                                                         | 556 kB  00:00:00     
(20/24): xvidcore-1.3.4-2.el7.x86_64.rpm                                                                                                                              | 263 kB  00:00:00     
(21/24): opencore-amr-0.1.3-3.el7.x86_64.rpm                                                                                                                          | 173 kB  00:00:03     
(22/24): x265-libs-1.9-4.el7.x86_64.rpm                                                                                                                               | 1.5 MB  00:00:06     
(23/24): libmpeg2-0.5.1-10.el7.x86_64.rpm                                                                                                                             |  66 kB  00:00:25     
(24/24): faad2-libs-2.7-8.el7.x86_64.rpm                                                                                                                              | 149 kB  00:00:44     
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                        283 kB/s |  12 MB  00:00:45     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-free-el-7
Importing GPG key 0xF5CF6C1E:
 Userid     : "RPM Fusion free repository for EL (7) <rpmfusion-buildsys@lists.rpmfusion.org>"
 Fingerprint: db9a 9a57 cafd 23da 3a88 792f 758b 3d18 f5cf 6c1e
 Package    : rpmfusion-free-release-7-1.noarch (installed)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-free-el-7
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : x264-libs-0.148-11.20160614gita5e06b9.el7.x86_64                                                                                                                         1/27 
  Installing : libass-0.13.4-1.el7.x86_64                                                                                                                                               2/27 
  Installing : xvidcore-1.3.4-2.el7.x86_64                                                                                                                                              3/27 
  Installing : lame-libs-3.99.5-6.el7.x86_64                                                                                                                                            4/27 
  Installing : enca-1.18-1.el7.x86_64                                                                                                                                                   5/27 
  Installing : opencore-amr-0.1.3-3.el7.x86_64                                                                                                                                          6/27 
  Installing : libXScrnSaver-1.2.2-6.1.el7.x86_64                                                                                                                                       7/27 
  Installing : libvdpau-1.1-2.el7.x86_64                                                                                                                                                8/27 
  Installing : libva-1.2.1-3.el7.x86_64                                                                                                                                                 9/27 
  Installing : schroedinger-1.0.11-4.el7.x86_64                                                                                                                                        10/27 
  Installing : freeglut-2.8.1-3.el7.x86_64                                                                                                                                             11/27 
  Installing : libcaca-0.99-0.17.beta17.el7.x86_64                                                                                                                                     12/27 
  Installing : mpg123-libs-1.23.6-2.el7.x86_64                                                                                                                                         13/27 
  Installing : libdca-0.0.5-9.el7.x86_64                                                                                                                                               14/27 
  Installing : libbs2b-3.1.0-13.el7.x86_64                                                                                                                                             15/27 
  Installing : lirc-libs-0.9.1a-4.el7.x86_64                                                                                                                                           16/27 
  Installing : a52dec-0.7.4-21.el7.x86_64                                                                                                                                              17/27 
  Installing : x265-libs-1.9-4.el7.x86_64                                                                                                                                              18/27 
  Installing : 1:faad2-libs-2.7-8.el7.x86_64                                                                                                                                           19/27 
  Installing : mplayer-common-1.1-23.20140414svn.el7.x86_64                                                                                                                            20/27 
  Installing : libmpeg2-0.5.1-10.el7.x86_64                                                                                                                                            21/27 
  Installing : vo-amrwbenc-0.1.3-1.el7.x86_64                                                                                                                                          22/27 
  Installing : aalib-libs-1.4.0-0.22.rc5.el7.x86_64                                                                                                                                    23/27 
  Installing : librtmp-2.4-7.20160224.gitfa8646d.el7.x86_64                                                                                                                            24/27 
  Installing : soxr-0.1.2-1.el7.x86_64                                                                                                                                                 25/27 
  Installing : ffmpeg-libs-2.8.11-1.el7.x86_64                                                                                                                                         26/27 
  Installing : mplayer-1.1-23.20140414svn.el7.x86_64                                                                                                                                   27/27 
  Verifying  : soxr-0.1.2-1.el7.x86_64                                                                                                                                                  1/27 
  Verifying  : librtmp-2.4-7.20160224.gitfa8646d.el7.x86_64                                                                                                                             2/27 
  Verifying  : ffmpeg-libs-2.8.11-1.el7.x86_64                                                                                                                                          3/27 
  Verifying  : aalib-libs-1.4.0-0.22.rc5.el7.x86_64                                                                                                                                     4/27 
  Verifying  : vo-amrwbenc-0.1.3-1.el7.x86_64                                                                                                                                           5/27 
  Verifying  : libmpeg2-0.5.1-10.el7.x86_64                                                                                                                                             6/27 
  Verifying  : mplayer-common-1.1-23.20140414svn.el7.x86_64                                                                                                                             7/27 
  Verifying  : 1:faad2-libs-2.7-8.el7.x86_64                                                                                                                                            8/27 
  Verifying  : x265-libs-1.9-4.el7.x86_64                                                                                                                                               9/27 
  Verifying  : lame-libs-3.99.5-6.el7.x86_64                                                                                                                                           10/27 
  Verifying  : a52dec-0.7.4-21.el7.x86_64                                                                                                                                              11/27 
  Verifying  : lirc-libs-0.9.1a-4.el7.x86_64                                                                                                                                           12/27 
  Verifying  : libbs2b-3.1.0-13.el7.x86_64                                                                                                                                             13/27 
  Verifying  : mplayer-1.1-23.20140414svn.el7.x86_64                                                                                                                                   14/27 
  Verifying  : libdca-0.0.5-9.el7.x86_64                                                                                                                                               15/27 
  Verifying  : xvidcore-1.3.4-2.el7.x86_64                                                                                                                                             16/27 
  Verifying  : mpg123-libs-1.23.6-2.el7.x86_64                                                                                                                                         17/27 
  Verifying  : libcaca-0.99-0.17.beta17.el7.x86_64                                                                                                                                     18/27 
  Verifying  : libass-0.13.4-1.el7.x86_64                                                                                                                                              19/27 
  Verifying  : freeglut-2.8.1-3.el7.x86_64                                                                                                                                             20/27 
  Verifying  : schroedinger-1.0.11-4.el7.x86_64                                                                                                                                        21/27 
  Verifying  : x264-libs-0.148-11.20160614gita5e06b9.el7.x86_64                                                                                                                        22/27 
  Verifying  : libva-1.2.1-3.el7.x86_64                                                                                                                                                23/27 
  Verifying  : libvdpau-1.1-2.el7.x86_64                                                                                                                                               24/27 
  Verifying  : libXScrnSaver-1.2.2-6.1.el7.x86_64                                                                                                                                      25/27 
  Verifying  : opencore-amr-0.1.3-3.el7.x86_64                                                                                                                                         26/27 
  Verifying  : enca-1.18-1.el7.x86_64                                                                                                                                                  27/27 

Installed:
  mplayer.x86_64 0:1.1-23.20140414svn.el7                                                                                                                                                    

Dependency Installed:
  a52dec.x86_64 0:0.7.4-21.el7         aalib-libs.x86_64 0:1.4.0-0.22.rc5.el7           enca.x86_64 0:1.18-1.el7                         faad2-libs.x86_64 1:2.7-8.el7                       
  ffmpeg-libs.x86_64 0:2.8.11-1.el7    freeglut.x86_64 0:2.8.1-3.el7                    lame-libs.x86_64 0:3.99.5-6.el7                  libXScrnSaver.x86_64 0:1.2.2-6.1.el7                
  libass.x86_64 0:0.13.4-1.el7         libbs2b.x86_64 0:3.1.0-13.el7                    libcaca.x86_64 0:0.99-0.17.beta17.el7            libdca.x86_64 0:0.0.5-9.el7                         
  libmpeg2.x86_64 0:0.5.1-10.el7       librtmp.x86_64 0:2.4-7.20160224.gitfa8646d.el7   libva.x86_64 0:1.2.1-3.el7                       libvdpau.x86_64 0:1.1-2.el7                         
  lirc-libs.x86_64 0:0.9.1a-4.el7      mpg123-libs.x86_64 0:1.23.6-2.el7                mplayer-common.x86_64 0:1.1-23.20140414svn.el7   opencore-amr.x86_64 0:0.1.3-3.el7                   
  schroedinger.x86_64 0:1.0.11-4.el7   soxr.x86_64 0:0.1.2-1.el7                        vo-amrwbenc.x86_64 0:0.1.3-1.el7                 x264-libs.x86_64 0:0.148-11.20160614gita5e06b9.el7  
  x265-libs.x86_64 0:1.9-4.el7         xvidcore.x86_64 0:1.3.4-2.el7                   

Complete!
```

继续安装图形化界面，帮助文档

```shell
[root@foundation0 yum.repos.d]# yum install -y mplayer*
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Package mplayer-common-1.1-23.20140414svn.el7.x86_64 already installed and latest version
Package mplayer-1.1-23.20140414svn.el7.x86_64 already installed and latest version
Resolving Dependencies
--> Running transaction check
---> Package mplayer-doc.x86_64 0:1.1-23.20140414svn.el7 will be installed
---> Package mplayer-gui.x86_64 0:1.1-23.20140414svn.el7 will be installed
---> Package mplayer-tools.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: mencoder = 1.1-23.20140414svn.el7 for package: mplayer-tools-1.1-23.20140414svn.el7.x86_64
--> Running transaction check
---> Package mencoder.x86_64 0:1.1-23.20140414svn.el7 will be installed
--> Processing Dependency: libtwolame.so.0()(64bit) for package: mencoder-1.1-23.20140414svn.el7.x86_64
--> Running transaction check
---> Package twolame-libs.x86_64 0:0.3.13-5.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=============================================================================================================================================================================================
 Package                                   Arch                               Version                                               Repository                                          Size
=============================================================================================================================================================================================
Installing:
 mplayer-doc                               x86_64                             1.1-23.20140414svn.el7                                rpmfusion-free-updates                             1.5 M
 mplayer-gui                               x86_64                             1.1-23.20140414svn.el7                                rpmfusion-free-updates                             1.5 M
 mplayer-tools                             x86_64                             1.1-23.20140414svn.el7                                rpmfusion-free-updates                              41 k
Installing for dependencies:
 mencoder                                  x86_64                             1.1-23.20140414svn.el7                                rpmfusion-free-updates                             835 k
 twolame-libs                              x86_64                             0.3.13-5.el7                                          rpmfusion-free-updates                              52 k

Transaction Summary
=============================================================================================================================================================================================
Install  3 Packages (+2 Dependent packages)

Total download size: 3.9 M
Installed size: 16 M
Downloading packages:
(1/5): mplayer-doc-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                                  | 1.5 MB  00:00:02     
(2/5): mencoder-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                                     | 835 kB  00:04:46     
(3/5): twolame-libs-0.3.13-5.el7.x86_64.rpm                                                                                                                           |  52 kB  00:00:00     
(4/5): mplayer-tools-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                                |  41 kB  00:00:14     
(5/5): mplayer-gui-1.1-23.20140414svn.el7.x86_64.rpm                                                                                                                  | 1.5 MB  00:07:58     
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                        8.4 kB/s | 3.9 MB  00:07:58     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : twolame-libs-0.3.13-5.el7.x86_64                                                                                                                                          1/5 
  Installing : mencoder-1.1-23.20140414svn.el7.x86_64                                                                                                                                    2/5 
  Installing : mplayer-tools-1.1-23.20140414svn.el7.x86_64                                                                                                                               3/5 
  Installing : mplayer-gui-1.1-23.20140414svn.el7.x86_64                                                                                                                                 4/5 
  Installing : mplayer-doc-1.1-23.20140414svn.el7.x86_64                                                                                                                                 5/5 
  Verifying  : twolame-libs-0.3.13-5.el7.x86_64                                                                                                                                          1/5 
  Verifying  : mplayer-tools-1.1-23.20140414svn.el7.x86_64                                                                                                                               2/5 
  Verifying  : mencoder-1.1-23.20140414svn.el7.x86_64                                                                                                                                    3/5 
  Verifying  : mplayer-doc-1.1-23.20140414svn.el7.x86_64                                                                                                                                 4/5 
  Verifying  : mplayer-gui-1.1-23.20140414svn.el7.x86_64                                                                                                                                 5/5 

Installed:
  mplayer-doc.x86_64 0:1.1-23.20140414svn.el7                   mplayer-gui.x86_64 0:1.1-23.20140414svn.el7                   mplayer-tools.x86_64 0:1.1-23.20140414svn.el7                  

Dependency Installed:
  mencoder.x86_64 0:1.1-23.20140414svn.el7                                                         twolame-libs.x86_64 0:0.3.13-5.el7                                                        

Complete!

[root@foundation0 opt]# yum install -y ffmpeg*
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Package ffmpeg-libs-2.8.11-1.el7.x86_64 already installed and latest version
Resolving Dependencies
--> Running transaction check
---> Package ffmpeg.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libavdevice.so.56(LIBAVDEVICE_56)(64bit) for package: ffmpeg-2.8.11-1.el7.x86_64
--> Processing Dependency: libavdevice.so.56()(64bit) for package: ffmpeg-2.8.11-1.el7.x86_64
---> Package ffmpeg-compat.x86_64 0:0.6.7-4.el7 will be installed
--> Processing Dependency: libdirac_encoder.so.0()(64bit) for package: ffmpeg-compat-0.6.7-4.el7.x86_64
--> Processing Dependency: libdc1394.so.22()(64bit) for package: ffmpeg-compat-0.6.7-4.el7.x86_64
---> Package ffmpeg-compat-devel.x86_64 0:0.6.7-4.el7 will be installed
---> Package ffmpeg-devel.x86_64 0:2.8.11-1.el7 will be installed
---> Package ffmpegthumbnailer.x86_64 0:2.0.8-7.el7 will be installed
---> Package ffmpegthumbnailer-devel.x86_64 0:2.0.8-7.el7 will be installed
--> Running transaction check
---> Package dirac-libs.x86_64 0:1.0.2-14.el7 will be installed
---> Package libavdevice.x86_64 0:2.8.11-1.el7 will be installed
--> Processing Dependency: libopenal.so.1()(64bit) for package: libavdevice-2.8.11-1.el7.x86_64
---> Package libdc1394.x86_64 0:2.2.2-3.el7 will be installed
--> Running transaction check
---> Package openal-soft.x86_64 0:1.16.0-3.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=============================================================================================================================================================================================
 Package                                             Arch                               Version                                     Repository                                          Size
=============================================================================================================================================================================================
Installing:
 ffmpeg                                              x86_64                             2.8.11-1.el7                                rpmfusion-free-updates                             1.3 M
 ffmpeg-compat                                       x86_64                             0.6.7-4.el7                                 rpmfusion-free-updates                             2.5 M
 ffmpeg-compat-devel                                 x86_64                             0.6.7-4.el7                                 rpmfusion-free-updates                             127 k
 ffmpeg-devel                                        x86_64                             2.8.11-1.el7                                rpmfusion-free-updates                             678 k
 ffmpegthumbnailer                                   x86_64                             2.0.8-7.el7                                 rpmfusion-free-updates                              46 k
 ffmpegthumbnailer-devel                             x86_64                             2.0.8-7.el7                                 rpmfusion-free-updates                             9.3 k
Installing for dependencies:
 dirac-libs                                          x86_64                             1.0.2-14.el7                                epel                                               256 k
 libavdevice                                         x86_64                             2.8.11-1.el7                                rpmfusion-free-updates                              72 k
 libdc1394                                           x86_64                             2.2.2-3.el7                                 epel                                               121 k
 openal-soft                                         x86_64                             1.16.0-3.el7                                epel                                               282 k

Transaction Summary
=============================================================================================================================================================================================
Install  6 Packages (+4 Dependent packages)

Total download size: 5.4 M
Installed size: 17 M
Downloading packages:
(1/10): dirac-libs-1.0.2-14.el7.x86_64.rpm                                                                                                                            | 256 kB  00:00:00     
(2/10): ffmpeg-2.8.11-1.el7.x86_64.rpm                                                                                                                                | 1.3 MB  00:00:03     
(3/10): ffmpeg-devel-2.8.11-1.el7.x86_64.rpm                                                                                                                          | 678 kB  00:00:01     
(4/10): ffmpegthumbnailer-2.0.8-7.el7.x86_64.rpm                                                                                                                      |  46 kB  00:00:00     
(5/10): ffmpegthumbnailer-devel-2.0.8-7.el7.x86_64.rpm                                                                                                                | 9.3 kB  00:00:00     
(6/10): libavdevice-2.8.11-1.el7.x86_64.rpm                                                                                                                           |  72 kB  00:00:00     
(7/10): libdc1394-2.2.2-3.el7.x86_64.rpm                                                                                                                              | 121 kB  00:00:00     
(8/10): openal-soft-1.16.0-3.el7.x86_64.rpm                                                                                                                           | 282 kB  00:00:00     
(9/10): ffmpeg-compat-0.6.7-4.el7.x86_64.rpm                                                                                                                          | 2.5 MB  00:00:08     
(10/10): ffmpeg-compat-devel-0.6.7-4.el7.x86_64.rpm                                                                                                                   | 127 kB  00:00:09     
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                        597 kB/s | 5.4 MB  00:00:09     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : libdc1394-2.2.2-3.el7.x86_64                                                                                                                                             1/10 
  Installing : dirac-libs-1.0.2-14.el7.x86_64                                                                                                                                           2/10 
  Installing : ffmpeg-compat-0.6.7-4.el7.x86_64                                                                                                                                         3/10 
  Installing : ffmpegthumbnailer-2.0.8-7.el7.x86_64                                                                                                                                     4/10 
  Installing : openal-soft-1.16.0-3.el7.x86_64                                                                                                                                          5/10 
  Installing : libavdevice-2.8.11-1.el7.x86_64                                                                                                                                          6/10 
  Installing : ffmpeg-2.8.11-1.el7.x86_64                                                                                                                                               7/10 
  Installing : ffmpeg-devel-2.8.11-1.el7.x86_64                                                                                                                                         8/10 
  Installing : ffmpegthumbnailer-devel-2.0.8-7.el7.x86_64                                                                                                                               9/10 
  Installing : ffmpeg-compat-devel-0.6.7-4.el7.x86_64                                                                                                                                  10/10 
  Verifying  : openal-soft-1.16.0-3.el7.x86_64                                                                                                                                          1/10 
  Verifying  : ffmpegthumbnailer-2.0.8-7.el7.x86_64                                                                                                                                     2/10 
  Verifying  : dirac-libs-1.0.2-14.el7.x86_64                                                                                                                                           3/10 
  Verifying  : ffmpeg-2.8.11-1.el7.x86_64                                                                                                                                               4/10 
  Verifying  : ffmpeg-compat-devel-0.6.7-4.el7.x86_64                                                                                                                                   5/10 
  Verifying  : libdc1394-2.2.2-3.el7.x86_64                                                                                                                                             6/10 
  Verifying  : ffmpegthumbnailer-devel-2.0.8-7.el7.x86_64                                                                                                                               7/10 
  Verifying  : libavdevice-2.8.11-1.el7.x86_64                                                                                                                                          8/10 
  Verifying  : ffmpeg-compat-0.6.7-4.el7.x86_64                                                                                                                                         9/10 
  Verifying  : ffmpeg-devel-2.8.11-1.el7.x86_64                                                                                                                                        10/10 

Installed:
  ffmpeg.x86_64 0:2.8.11-1.el7                  ffmpeg-compat.x86_64 0:0.6.7-4.el7                  ffmpeg-compat-devel.x86_64 0:0.6.7-4.el7        ffmpeg-devel.x86_64 0:2.8.11-1.el7       
  ffmpegthumbnailer.x86_64 0:2.0.8-7.el7        ffmpegthumbnailer-devel.x86_64 0:2.0.8-7.el7       

Dependency Installed:
  dirac-libs.x86_64 0:1.0.2-14.el7               libavdevice.x86_64 0:2.8.11-1.el7               libdc1394.x86_64 0:2.2.2-3.el7               openal-soft.x86_64 0:1.16.0-3.el7              

Complete!

```

实际上安装完以上软件，CentOS自带的各种媒体播放软件因为有了解码器，都可以播放mp3了，如要设置Mplayer为默认播放器，
右键单击音乐文件，属性，打开方式，添加，找到Mplayer Media Player，添加。只能播放mp3，音乐，不能播放视频，如果要播放还需要额外安装视频编码。

## 安装splayer

该软件更简单，无需额外安装编码，装好就能看视频，测试了mp4和rmvb

```shell

[root@foundation0 ~]# yum list|grep mplayer
mplayer.x86_64                           1.1-23.20140414svn.el7   @rpmfusion-free-updates
mplayer-common.x86_64                    1.1-23.20140414svn.el7   @rpmfusion-free-updates
mplayer-doc.x86_64                       1.1-23.20140414svn.el7   @rpmfusion-free-updates
mplayer-gui.x86_64                       1.1-23.20140414svn.el7   @rpmfusion-free-updates
mplayer-tools.x86_64                     1.1-23.20140414svn.el7   @rpmfusion-free-updates
smplayer.x86_64                          17.4.2-1.el7             rpmfusion-free-updates
smplayer-themes.x86_64                   17.4.2-1.el7             rpmfusion-free-updates
[root@foundation0 ~]# yum install -y smplayer*
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package smplayer.x86_64 0:17.4.2-1.el7 will be installed
--> Processing Dependency: qt5-qtbase(x86-64) >= 5.6.1 for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Xml.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Widgets.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Script.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Network.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Gui.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5DBus.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Core.so.5(Qt_5.6)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Core.so.5(Qt_5)(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Xml.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Widgets.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Solutions_SingleApplication-2.6.so.1()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Script.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Network.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Gui.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5DBus.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
--> Processing Dependency: libQt5Core.so.5()(64bit) for package: smplayer-17.4.2-1.el7.x86_64
---> Package smplayer-themes.x86_64 0:17.4.2-1.el7 will be installed
--> Running transaction check
---> Package qt5-qtbase.x86_64 0:5.6.1-3.el7 will be installed
--> Processing Dependency: qt5-qtbase-common = 5.6.1-3.el7 for package: qt5-qtbase-5.6.1-3.el7.x86_64
---> Package qt5-qtbase-gui.x86_64 0:5.6.1-3.el7 will be installed
--> Processing Dependency: libxcb-render-util.so.0()(64bit) for package: qt5-qtbase-gui-5.6.1-3.el7.x86_64
--> Processing Dependency: libxcb-keysyms.so.1()(64bit) for package: qt5-qtbase-gui-5.6.1-3.el7.x86_64
--> Processing Dependency: libxcb-image.so.0()(64bit) for package: qt5-qtbase-gui-5.6.1-3.el7.x86_64
--> Processing Dependency: libxcb-icccm.so.4()(64bit) for package: qt5-qtbase-gui-5.6.1-3.el7.x86_64
---> Package qt5-qtscript.x86_64 0:5.6.1-1.el7 will be installed
---> Package qtsingleapplication-qt5.x86_64 0:2.6.1-28.el7 will be installed
--> Processing Dependency: libQt5Solutions_LockedFile-2.4.so.1()(64bit) for package: qtsingleapplication-qt5-2.6.1-28.el7.x86_64
--> Running transaction check
---> Package qt5-qtbase-common.noarch 0:5.6.1-3.el7 will be installed
---> Package qtlockedfile-qt5.x86_64 0:2.4-20.20150629git5a07df5.el7 will be installed
---> Package xcb-util-image.x86_64 0:0.4.0-2.el7 will be installed
---> Package xcb-util-keysyms.x86_64 0:0.4.0-1.el7 will be installed
---> Package xcb-util-renderutil.x86_64 0:0.3.9-3.el7 will be installed
---> Package xcb-util-wm.x86_64 0:0.4.1-5.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==============================================================================================================
 Package                     Arch       Version                              Repository                  Size
==============================================================================================================
Installing:
 smplayer                    x86_64     17.4.2-1.el7                         rpmfusion-free-updates     3.6 M
 smplayer-themes             x86_64     17.4.2-1.el7                         rpmfusion-free-updates     2.7 M
Installing for dependencies:
 qt5-qtbase                  x86_64     5.6.1-3.el7                          epel                       2.9 M
 qt5-qtbase-common           noarch     5.6.1-3.el7                          epel                        26 k
 qt5-qtbase-gui              x86_64     5.6.1-3.el7                          epel                       5.4 M
 qt5-qtscript                x86_64     5.6.1-1.el7                          epel                       1.0 M
 qtlockedfile-qt5            x86_64     2.4-20.20150629git5a07df5.el7        epel                        31 k
 qtsingleapplication-qt5     x86_64     2.6.1-28.el7                         epel                        39 k
 xcb-util-image              x86_64     0.4.0-2.el7                          rhel-dvd                    15 k
 xcb-util-keysyms            x86_64     0.4.0-1.el7                          rhel-dvd                    10 k
 xcb-util-renderutil         x86_64     0.3.9-3.el7                          rhel-dvd                    13 k
 xcb-util-wm                 x86_64     0.4.1-5.el7                          rhel-dvd                    25 k

Transaction Summary
==============================================================================================================
Install  2 Packages (+10 Dependent packages)

Total download size: 16 M
Installed size: 48 M
Downloading packages:
(1/8): qt5-qtbase-5.6.1-3.el7.x86_64.rpm                                               | 2.9 MB  00:00:04     
(2/8): qt5-qtbase-common-5.6.1-3.el7.noarch.rpm                                        |  26 kB  00:00:00     
(3/8): qt5-qtbase-gui-5.6.1-3.el7.x86_64.rpm                                           | 5.4 MB  00:00:09     
(4/8): qt5-qtscript-5.6.1-1.el7.x86_64.rpm                                             | 1.0 MB  00:00:01     
(5/8): qtlockedfile-qt5-2.4-20.20150629git5a07df5.el7.x86_64.rpm                       |  31 kB  00:00:00     
(6/8): qtsingleapplication-qt5-2.6.1-28.el7.x86_64.rpm                                 |  39 kB  00:00:00     
(7/8): smplayer-17.4.2-1.el7.x86_64.rpm                                                | 3.6 MB  00:00:09     
(8/8): smplayer-themes-17.4.2-1.el7.x86_64.rpm                                         | 2.7 MB  00:00:10     
--------------------------------------------------------------------------------------------------------------
Total                                                                         601 kB/s |  16 MB  00:00:26     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : qt5-qtbase-5.6.1-3.el7.x86_64                                                             1/12 
  Installing : qt5-qtbase-common-5.6.1-3.el7.noarch                                                      2/12 
  Installing : qtlockedfile-qt5-2.4-20.20150629git5a07df5.el7.x86_64                                     3/12 
  Installing : xcb-util-wm-0.4.1-5.el7.x86_64                                                            4/12 
  Installing : xcb-util-renderutil-0.3.9-3.el7.x86_64                                                    5/12 
  Installing : xcb-util-keysyms-0.4.0-1.el7.x86_64                                                       6/12 
  Installing : xcb-util-image-0.4.0-2.el7.x86_64                                                         7/12 
  Installing : qt5-qtbase-gui-5.6.1-3.el7.x86_64                                                         8/12 
  Installing : qtsingleapplication-qt5-2.6.1-28.el7.x86_64                                               9/12 
  Installing : qt5-qtscript-5.6.1-1.el7.x86_64                                                          10/12 
  Installing : smplayer-17.4.2-1.el7.x86_64                                                             11/12 
  Installing : smplayer-themes-17.4.2-1.el7.x86_64                                                      12/12 
  Verifying  : xcb-util-image-0.4.0-2.el7.x86_64                                                         1/12 
  Verifying  : qtsingleapplication-qt5-2.6.1-28.el7.x86_64                                               2/12 
  Verifying  : xcb-util-keysyms-0.4.0-1.el7.x86_64                                                       3/12 
  Verifying  : qt5-qtscript-5.6.1-1.el7.x86_64                                                           4/12 
  Verifying  : qt5-qtbase-common-5.6.1-3.el7.noarch                                                      5/12 
  Verifying  : qtlockedfile-qt5-2.4-20.20150629git5a07df5.el7.x86_64                                     6/12 
  Verifying  : qt5-qtbase-5.6.1-3.el7.x86_64                                                             7/12 
  Verifying  : xcb-util-renderutil-0.3.9-3.el7.x86_64                                                    8/12 
  Verifying  : qt5-qtbase-gui-5.6.1-3.el7.x86_64                                                         9/12 
  Verifying  : xcb-util-wm-0.4.1-5.el7.x86_64                                                           10/12 
  Verifying  : smplayer-themes-17.4.2-1.el7.x86_64                                                      11/12 
  Verifying  : smplayer-17.4.2-1.el7.x86_64                                                             12/12 

Installed:
  smplayer.x86_64 0:17.4.2-1.el7                     smplayer-themes.x86_64 0:17.4.2-1.el7                    

Dependency Installed:
  qt5-qtbase.x86_64 0:5.6.1-3.el7                            qt5-qtbase-common.noarch 0:5.6.1-3.el7          
  qt5-qtbase-gui.x86_64 0:5.6.1-3.el7                        qt5-qtscript.x86_64 0:5.6.1-1.el7               
  qtlockedfile-qt5.x86_64 0:2.4-20.20150629git5a07df5.el7    qtsingleapplication-qt5.x86_64 0:2.6.1-28.el7   
  xcb-util-image.x86_64 0:0.4.0-2.el7                        xcb-util-keysyms.x86_64 0:0.4.0-1.el7           
  xcb-util-renderutil.x86_64 0:0.3.9-3.el7                   xcb-util-wm.x86_64 0:0.4.1-5.el7                

Complete!
```
