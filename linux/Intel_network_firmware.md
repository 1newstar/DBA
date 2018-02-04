# 新笔记本安装rhel 7.2 后无线网卡无法检测到

机械革命rhel7.2网卡设置

## 解决思路

1. 确定无线网卡型号  intel的所以直接上github上下载所有的firmware驱动
2. 升级内核	   kernel升级到4.9 官方要求4.7以上
3. 重启动服务	   reboot

### 走的弯路

1. 不知道无线网卡的驱动是/lib/firmware/iwlwifi-*
2. 不知道github上有所有的驱动，不要去管intel的具体型号，把所有驱动都放进去
3. 内核升级到最新版本4.11，结果显卡又有问题

### 详细操作


1. 查看pci，最后两行，第一个是有线网卡，第二个是无线网卡

```shell
[root@foundation0 ~]# lspci
00:00.0 Host bridge: Intel Corporation Device 5910 (rev 05)
00:01.0 PCI bridge: Intel Corporation Sky Lake PCIe Controller (x16) (rev 05)
00:02.0 VGA compatible controller: Intel Corporation Device 591b (rev 04)
00:08.0 System peripheral: Intel Corporation Sky Lake Gaussian Mixture Model
00:14.0 USB controller: Intel Corporation Sunrise Point-H USB 3.0 xHCI Controller (rev 31)
00:14.2 Signal processing controller: Intel Corporation Sunrise Point-H Thermal subsystem (rev 31)
00:16.0 Communication controller: Intel Corporation Sunrise Point-H CSME HECI #1 (rev 31)
00:17.0 SATA controller: Intel Corporation Sunrise Point-H SATA Controller [AHCI mode] (rev 31)
00:1c.0 PCI bridge: Intel Corporation Sunrise Point-H PCI Express Root Port #4 (rev f1)
00:1c.4 PCI bridge: Intel Corporation Sunrise Point-H PCI Express Root Port #5 (rev f1)
00:1f.0 ISA bridge: Intel Corporation Sunrise Point-H LPC Controller (rev 31)
00:1f.2 Memory controller: Intel Corporation Sunrise Point-H PMC (rev 31)
00:1f.3 Audio device: Intel Corporation Device a171 (rev 31)
00:1f.4 SMBus: Intel Corporation Sunrise Point-H SMBus (rev 31)
01:00.0 VGA compatible controller: NVIDIA Corporation Device 1c8d (rev a1)
02:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 0c)
03:00.0 Network controller: Intel Corporation Device 24fb (rev 10)
```

2. 用dmesg查看设备对应的驱动，有线的驱动是r8169，无线不知道？

```shell
[root@foundation0 ~]# dmesg | grep eth
[    1.024502] r8169 0000:02:00.0 eth0: RTL8168g/8111g at 0xffffc90000c28000, b0:25:aa:22:51:9d, XID 0c000800 IRQ 126
[    1.024505] r8169 0000:02:00.0 eth0: jumbo features [frames: 9200 bytes, tx checksumming: ko]
[    1.040372] VGA switcheroo: detected Optimus DSM method \_SB_.PCI0.PEG0.PEGP handle
```

3. 用lsmod查看到有线网卡驱动已经安装并加载

```shell
[root@foundation0 ~]# lsmod | grep r8169
r8169                  80945  0 
mii                    13934  1 r8169
```

4. 查看该模块加载的具体文件为/lib/firmware/rtl_nic/*.fw

```shell
[root@foundation0 ~]# modinfo r8169
filename:       /lib/modules/3.10.0-327.el7.x86_64/kernel/drivers/net/ethernet/realtek/r8169.ko
firmware:       rtl_nic/rtl8107e-2.fw
firmware:       rtl_nic/rtl8107e-1.fw
firmware:       rtl_nic/rtl8168h-2.fw
firmware:       rtl_nic/rtl8168h-1.fw
firmware:       rtl_nic/rtl8168g-3.fw
firmware:       rtl_nic/rtl8168g-2.fw
firmware:       rtl_nic/rtl8106e-2.fw
firmware:       rtl_nic/rtl8106e-1.fw
firmware:       rtl_nic/rtl8411-2.fw
firmware:       rtl_nic/rtl8411-1.fw
firmware:       rtl_nic/rtl8402-1.fw
firmware:       rtl_nic/rtl8168f-2.fw
firmware:       rtl_nic/rtl8168f-1.fw
firmware:       rtl_nic/rtl8105e-1.fw
firmware:       rtl_nic/rtl8168e-3.fw
firmware:       rtl_nic/rtl8168e-2.fw
firmware:       rtl_nic/rtl8168e-1.fw
firmware:       rtl_nic/rtl8168d-2.fw
firmware:       rtl_nic/rtl8168d-1.fw
version:        2.3LK-NAPI
license:        GPL
description:    RealTek RTL-8169 Gigabit Ethernet driver
author:         Realtek and the Linux r8169 crew <netdev@vger.kernel.org>
rhelversion:    7.2
srcversion:     17C11305BF371984CB1A920
alias:          pci:v00000001d00008168sv*sd00002410bc*sc*i*
alias:          pci:v00001737d00001032sv*sd00000024bc*sc*i*
alias:          pci:v000016ECd00000116sv*sd*bc*sc*i*
alias:          pci:v00001259d0000C107sv*sd*bc*sc*i*
alias:          pci:v00001186d00004302sv*sd*bc*sc*i*
alias:          pci:v00001186d00004300sv*sd*bc*sc*i*
alias:          pci:v00001186d00004300sv00001186sd00004B10bc*sc*i*
alias:          pci:v000010ECd00008169sv*sd*bc*sc*i*
alias:          pci:v000010ECd00008168sv*sd*bc*sc*i*
alias:          pci:v000010ECd00008167sv*sd*bc*sc*i*
alias:          pci:v000010ECd00008136sv*sd*bc*sc*i*
alias:          pci:v000010ECd00008129sv*sd*bc*sc*i*
depends:        mii
intree:         Y
vermagic:       3.10.0-327.el7.x86_64 SMP mod_unload modversions 
signer:         Red Hat Enterprise Linux kernel signing key
sig_key:        BC:73:C3:CE:E8:9E:5E:AE:99:4A:E5:0A:0D:B1:F0:FE:E3:FC:09:13
sig_hashalgo:   sha256
parm:           use_dac:Enable PCI DAC. Unsafe on 32 bit PCI slot. (int)
parm:           debug:Debug verbosity level (0=none, ..., 16=all) (int)
```


---


5. 对于无线设备`03:00.0 Network controller: Intel Corporation Device 24fb (rev 10)`，进一步分析，先google一下，该网卡的驱动需要升级内核到多少版本？

```shell
[root@foundation0 ~]# lspci -knn | grep -A 1 Net
03:00.0 Network controller [0280]: Intel Corporation Device [8086:24fb] (rev 10)
	Subsystem: Intel Corporation Device [8086:2110]


[root@foundation0 ~]# rfkill list
0: hci0: Bluetooth
	Soft blocked: no
	Hard blocked: no
```shell

----

6. 将内核升级到4.9，再将firmware驱动下载后导入到/lib/firmware/目录下

```shell
[root@foundation0 ~]# uname -r
4.9.25-27.el7.x86_64
[root@foundation0 ~]# lsmod|grep iwlwifi
iwlwifi               147456  1 iwlmvm
cfg80211              565248  3 iwlmvm,iwlwifi,mac80211
[root@foundation0 ~]# modinfo iwlwifi
filename:       /lib/modules/4.9.25-27.el7.x86_64/kernel/drivers/net/wireless/intel/iwlwifi/iwlwifi.ko
license:        GPL
author:         Copyright(c) 2003- 2015 Intel Corporation <linuxwifi@intel.com>
description:    Intel(R) Wireless WiFi driver for Linux
firmware:       iwlwifi-100-5.ucode
firmware:       iwlwifi-1000-5.ucode
firmware:       iwlwifi-135-6.ucode
firmware:       iwlwifi-105-6.ucode
firmware:       iwlwifi-2030-6.ucode
firmware:       iwlwifi-2000-6.ucode
firmware:       iwlwifi-5150-2.ucode
firmware:       iwlwifi-5000-5.ucode
firmware:       iwlwifi-6000g2b-IWL6000G2B_UCODE_API_MAX.ucode
firmware:       iwlwifi-6000g2a-6.ucode
firmware:       iwlwifi-6050-5.ucode
firmware:       iwlwifi-6000-6.ucode
firmware:       iwlwifi-7265D-26.ucode
firmware:       iwlwifi-7265-17.ucode
firmware:       iwlwifi-3168-26.ucode
firmware:       iwlwifi-3160-17.ucode
firmware:       iwlwifi-7260-17.ucode
firmware:       iwlwifi-8265-26.ucode
firmware:       iwlwifi-8000C-26.ucode
firmware:       iwlwifi-9000-pu-a0-lc-a0--26.ucode
firmware:       iwlwifi-9260-th-a0-jf-a0--26.ucode
firmware:       iwlwifi-9000-pu-a0-jf-a0--26.ucode
firmware:       iwlwifi-Qu-a0-jf-b0--26.ucode
srcversion:     5415E21FB503EDA2F465CB4
alias:          pci:v00008086d00002720sv*sd00000A10bc*sc*i*
alias:          pci:v00008086d0000A370sv*sd00001030bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00001030bc*sc*i*
alias:          pci:v00008086d000031DCsv*sd00000030bc*sc*i*
alias:          pci:v00008086d0000A370sv*sd00000030bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000030bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00000030bc*sc*i*
alias:          pci:v00008086d000031DCsv*sd00000060bc*sc*i*
alias:          pci:v00008086d0000A370sv*sd00000060bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000060bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00000060bc*sc*i*
alias:          pci:v00008086d000030DCsv*sd00000060bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00002A10bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000710bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00001420bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00002010bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000510bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000000bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000310bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000610bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000410bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000210bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000010bc*sc*i*
alias:          pci:v00008086d00009DF0sv*sd00000A10bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00001410bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00000010bc*sc*i*
alias:          pci:v00008086d00002526sv*sd00000000bc*sc*i*
alias:          pci:v00008086d0000271Bsv*sd00000010bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000012bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000850bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000950bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000930bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000910bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00008130bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00009110bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000810bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00008010bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00008050bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00008110bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00009010bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000150bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000050bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd000010D0bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00001010bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000130bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00001130bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00001110bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000110bc*sc*i*
alias:          pci:v00008086d000024FDsv*sd00000010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000000bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000930bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000950bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000850bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000910bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000810bc*sc*i*
alias:          pci:v00008086d000024F6sv*sd00000030bc*sc*i*
alias:          pci:v00008086d000024F5sv*sd00000010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000044bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000004bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009150bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008150bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009132bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008132bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009130bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008130bc*sc*i*
alias:          pci:v00008086d000024F4sv*sd00009030bc*sc*i*
alias:          pci:v00008086d000024F4sv*sd00008030bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009110bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00009010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008110bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00008010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000B0B0bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000D0B0bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000D050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000C050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000D010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000C110bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd0000C010bc*sc*i*
alias:          pci:v00008086d000024F4sv*sd00001030bc*sc*i*
alias:          pci:v00008086d000024F4sv*sd00000030bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001150bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000150bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000250bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000050bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001110bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001012bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000012bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd000001F0bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000110bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001132bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000132bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001130bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000130bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd000010B0bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00001010bc*sc*i*
alias:          pci:v00008086d000024F3sv*sd00000010bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009400bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009000bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd0000520Abc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005212bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005F10bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005490bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005290bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005590bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005190bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005090bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005420bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd0000502Abc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005020bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009410bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00009310bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009510bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00009200bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00009210bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009112bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009110bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd0000900Abc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009012bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00009010bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005202bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005102bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005002bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005200bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd0000500Abc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005000bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00001010bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005400bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005510bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005410bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005412bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005012bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005C10bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005210bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005302bc*sc*i*
alias:          pci:v00008086d0000095Bsv*sd00005310bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005100bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005110bc*sc*i*
alias:          pci:v00008086d0000095Asv*sd00005010bc*sc*i*
alias:          pci:v00008086d000024FBsv*sd00000000bc*sc*i*
alias:          pci:v00008086d000024FBsv*sd00002150bc*sc*i*
alias:          pci:v00008086d000024FBsv*sd00002050bc*sc*i*
alias:          pci:v00008086d000024FBsv*sd00002110bc*sc*i*
alias:          pci:v00008086d000024FBsv*sd00002010bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00008110bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00008010bc*sc*i*
alias:          pci:v00008086d00003166sv*sd00004210bc*sc*i*
alias:          pci:v00008086d00003166sv*sd00004310bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00004110bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00004510bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00004410bc*sc*i*
alias:          pci:v00008086d00003166sv*sd00004212bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00004012bc*sc*i*
alias:          pci:v00008086d00003165sv*sd00004010bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00001170bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00001070bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008570bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008470bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00008272bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00008370bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00008270bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008062bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008060bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008172bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008170bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008072bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00008070bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00000370bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000472bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000470bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00000272bc*sc*i*
alias:          pci:v00008086d000008B4sv*sd00000270bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000062bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000060bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000172bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000170bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000072bc*sc*i*
alias:          pci:v00008086d000008B3sv*sd00000070bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C420bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C220bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C02Abc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C020bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C360bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C370bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C560bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C570bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C462bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C460bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C472bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C470bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C262bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C26Abc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C260bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C272bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000CC60bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000CC70bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000C270bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C760bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C770bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C162bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C062bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C160bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C06Abc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C060bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C170bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C072bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000C070bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004420bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004220bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000402Abc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004020bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00005770bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00005170bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00005072bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00005070bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004360bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004370bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004560bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004570bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004A6Cbc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004A6Ebc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004A70bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000486Ebc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004870bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004462bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000446Abc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004460bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004472bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004470bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004262bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd0000426Abc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004260bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004272bc*sc*i*
alias:          pci:v00008086d000008B2sv*sd00004270bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004162bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004062bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004160bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd0000406Abc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004060bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004C70bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004C60bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004170bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004072bc*sc*i*
alias:          pci:v00008086d000008B1sv*sd00004070bc*sc*i*
alias:          pci:v00008086d00000892sv*sd00000462bc*sc*i*
alias:          pci:v00008086d00000893sv*sd00000262bc*sc*i*
alias:          pci:v00008086d00000892sv*sd00000062bc*sc*i*
alias:          pci:v00008086d00000894sv*sd00000822bc*sc*i*
alias:          pci:v00008086d00000894sv*sd00000422bc*sc*i*
alias:          pci:v00008086d00000895sv*sd00000222bc*sc*i*
alias:          pci:v00008086d00000894sv*sd00000022bc*sc*i*
alias:          pci:v00008086d0000088Fsv*sd00005260bc*sc*i*
alias:          pci:v00008086d0000088Esv*sd00004860bc*sc*i*
alias:          pci:v00008086d0000088Esv*sd0000446Abc*sc*i*
alias:          pci:v00008086d0000088Esv*sd00004460bc*sc*i*
alias:          pci:v00008086d0000088Fsv*sd0000426Abc*sc*i*
alias:          pci:v00008086d0000088Fsv*sd00004260bc*sc*i*
alias:          pci:v00008086d0000088Esv*sd0000406Abc*sc*i*
alias:          pci:v00008086d0000088Esv*sd00004060bc*sc*i*
alias:          pci:v00008086d00000887sv*sd00004462bc*sc*i*
alias:          pci:v00008086d00000888sv*sd00004262bc*sc*i*
alias:          pci:v00008086d00000887sv*sd00004062bc*sc*i*
alias:          pci:v00008086d00000890sv*sd00004822bc*sc*i*
alias:          pci:v00008086d00000890sv*sd00004422bc*sc*i*
alias:          pci:v00008086d00000891sv*sd00004222bc*sc*i*
alias:          pci:v00008086d00000890sv*sd00004022bc*sc*i*
alias:          pci:v00008086d00000896sv*sd00005027bc*sc*i*
alias:          pci:v00008086d00000896sv*sd00005025bc*sc*i*
alias:          pci:v00008086d00000897sv*sd00005017bc*sc*i*
alias:          pci:v00008086d00000897sv*sd00005015bc*sc*i*
alias:          pci:v00008086d00000896sv*sd00005007bc*sc*i*
alias:          pci:v00008086d00000896sv*sd00005005bc*sc*i*
alias:          pci:v00008086d000008AEsv*sd00001027bc*sc*i*
alias:          pci:v00008086d000008AEsv*sd00001025bc*sc*i*
alias:          pci:v00008086d000008AFsv*sd00001017bc*sc*i*
alias:          pci:v00008086d000008AFsv*sd00001015bc*sc*i*
alias:          pci:v00008086d000008AEsv*sd00001007bc*sc*i*
alias:          pci:v00008086d000008AEsv*sd00001005bc*sc*i*
alias:          pci:v00008086d00000084sv*sd00001316bc*sc*i*
alias:          pci:v00008086d00000084sv*sd00001216bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001326bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001226bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001306bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001206bc*sc*i*
alias:          pci:v00008086d00000084sv*sd00001315bc*sc*i*
alias:          pci:v00008086d00000084sv*sd00001215bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001325bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001225bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001305bc*sc*i*
alias:          pci:v00008086d00000083sv*sd00001205bc*sc*i*
alias:          pci:v00008086d00000886sv*sd00001317bc*sc*i*
alias:          pci:v00008086d00000886sv*sd00001315bc*sc*i*
alias:          pci:v00008086d00000885sv*sd00001327bc*sc*i*
alias:          pci:v00008086d00000885sv*sd00001325bc*sc*i*
alias:          pci:v00008086d00000885sv*sd00001307bc*sc*i*
alias:          pci:v00008086d00000885sv*sd00001305bc*sc*i*
alias:          pci:v00008086d00000089sv*sd00001316bc*sc*i*
alias:          pci:v00008086d00000089sv*sd00001311bc*sc*i*
alias:          pci:v00008086d00000087sv*sd00001326bc*sc*i*
alias:          pci:v00008086d00000087sv*sd00001321bc*sc*i*
alias:          pci:v00008086d00000087sv*sd00001306bc*sc*i*
alias:          pci:v00008086d00000087sv*sd00001301bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005226bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005225bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005221bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005207bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005206bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005205bc*sc*i*
alias:          pci:v00008086d00000091sv*sd00005201bc*sc*i*
alias:          pci:v00008086d00000090sv*sd00005216bc*sc*i*
alias:          pci:v00008086d00000090sv*sd00005215bc*sc*i*
alias:          pci:v00008086d00000090sv*sd00005211bc*sc*i*
alias:          pci:v00008086d0000008Bsv*sd00005317bc*sc*i*
alias:          pci:v00008086d0000008Bsv*sd00005315bc*sc*i*
alias:          pci:v00008086d0000008Asv*sd00005327bc*sc*i*
alias:          pci:v00008086d0000008Asv*sd00005325bc*sc*i*
alias:          pci:v00008086d0000008Asv*sd00005307bc*sc*i*
alias:          pci:v00008086d0000008Asv*sd00005305bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001305bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001304bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00004820bc*sc*i*
alias:          pci:v00008086d00000085sv*sd0000C228bc*sc*i*
alias:          pci:v00008086d00000085sv*sd0000C220bc*sc*i*
alias:          pci:v00008086d00000082sv*sd0000C020bc*sc*i*
alias:          pci:v00008086d00000085sv*sd00001316bc*sc*i*
alias:          pci:v00008086d00000085sv*sd00001318bc*sc*i*
alias:          pci:v00008086d00000085sv*sd00001311bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001328bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001326bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001321bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001308bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001307bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001306bc*sc*i*
alias:          pci:v00008086d00000082sv*sd00001301bc*sc*i*
alias:          pci:v00008086d00004239sv*sd00001316bc*sc*i*
alias:          pci:v00008086d00004239sv*sd00001311bc*sc*i*
alias:          pci:v00008086d00004238sv*sd00001118bc*sc*i*
alias:          pci:v00008086d00004238sv*sd00001111bc*sc*i*
alias:          pci:v00008086d0000422Csv*sd00001326bc*sc*i*
alias:          pci:v00008086d0000422Csv*sd00001321bc*sc*i*
alias:          pci:v00008086d0000422Csv*sd00001307bc*sc*i*
alias:          pci:v00008086d0000422Csv*sd00001306bc*sc*i*
alias:          pci:v00008086d0000422Csv*sd00001301bc*sc*i*
alias:          pci:v00008086d0000422Bsv*sd00001128bc*sc*i*
alias:          pci:v00008086d0000422Bsv*sd00001121bc*sc*i*
alias:          pci:v00008086d0000422Bsv*sd00001108bc*sc*i*
alias:          pci:v00008086d0000422Bsv*sd00001101bc*sc*i*
alias:          pci:v00008086d0000423Dsv*sd00001316bc*sc*i*
alias:          pci:v00008086d0000423Dsv*sd00001216bc*sc*i*
alias:          pci:v00008086d0000423Dsv*sd00001311bc*sc*i*
alias:          pci:v00008086d0000423Dsv*sd00001211bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001326bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001321bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001221bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001306bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001206bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001301bc*sc*i*
alias:          pci:v00008086d0000423Csv*sd00001201bc*sc*i*
alias:          pci:v00008086d0000423Bsv*sd00001011bc*sc*i*
alias:          pci:v00008086d0000423Asv*sd00001021bc*sc*i*
alias:          pci:v00008086d0000423Asv*sd00001001bc*sc*i*
alias:          pci:v00008086d00004236sv*sd00001114bc*sc*i*
alias:          pci:v00008086d00004236sv*sd00001014bc*sc*i*
alias:          pci:v00008086d00004236sv*sd00001111bc*sc*i*
alias:          pci:v00008086d00004236sv*sd00001011bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001104bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001004bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001101bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001001bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001124bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001024bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001121bc*sc*i*
alias:          pci:v00008086d00004235sv*sd00001021bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001316bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001216bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001315bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001215bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001314bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001214bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001311bc*sc*i*
alias:          pci:v00008086d00004237sv*sd00001211bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001326bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001226bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001325bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001225bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001324bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001224bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001321bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001221bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001306bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001206bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001305bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001205bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001304bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001204bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001301bc*sc*i*
alias:          pci:v00008086d00004232sv*sd00001201bc*sc*i*
depends:        cfg80211
intree:         Y
vermagic:       4.9.25-27.el7.x86_64 SMP mod_unload modversions 
parm:           swcrypto:using crypto in software (default 0 [hardware]) (int)
parm:           11n_disable:disable 11n functionality, bitmap: 1: full, 2: disable agg TX, 4: disable agg RX, 8 enable agg TX (uint)
parm:           amsdu_size:amsdu size 0: 12K for multi Rx queue devices, 4K for other devices 1:4K 2:8K 3:12K (default 0) (int)
parm:           fw_restart:restart firmware in case of error (default true) (bool)
parm:           antenna_coupling:specify antenna coupling in dB (default: 0 dB) (int)
parm:           nvm_file:NVM file name (charp)
parm:           d0i3_disable:disable d0i3 functionality (default: Y) (bool)
parm:           lar_disable:disable LAR functionality (default: N) (bool)
parm:           uapsd_disable:disable U-APSD functionality bitmap 1: BSS 2: P2P Client (default: 3) (uint)
parm:           bt_coex_active:enable wifi/bt co-exist (default: enable) (bool)
parm:           led_mode:0=system default, 1=On(RF On)/Off(RF Off), 2=blinking, 3=Off (default: 0) (int)
parm:           power_save:enable WiFi power management (default: disable) (bool)
parm:           power_level:default power save level (range from 1 - 5, default: 1) (int)
parm:           fw_monitor:firmware monitor - to debug FW (default: false - needs lots of memory) (bool)
parm:           d0i3_timeout:Timeout to D0i3 entry when idle (ms) (uint)
parm:           disable_11ac:Disable VHT capabilities (default: false) (bool)


[root@foundation0 ~]# dmesg | grep wifi
[    4.105945] iwlwifi 0000:03:00.0: Direct firmware load for iwlwifi-3168-26.ucode failed with error -2
[    4.105951] iwlwifi 0000:03:00.0: Direct firmware load for iwlwifi-3168-25.ucode failed with error -2
[    4.105956] iwlwifi 0000:03:00.0: Direct firmware load for iwlwifi-3168-24.ucode failed with error -2
[    4.105961] iwlwifi 0000:03:00.0: Direct firmware load for iwlwifi-3168-23.ucode failed with error -2
[    4.112454] iwlwifi 0000:03:00.0: loaded firmware version 22.361476.0 op_mode iwlmvm
[    4.166599] iwlwifi 0000:03:00.0: Detected Intel(R) Dual Band Wireless AC 3168, REV=0x220
[    4.168636] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled
[    4.168809] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled
[    4.206658] iwlwifi 0000:03:00.0 wlp3s0: renamed from wlan0
[    6.070961] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled
[    6.071198] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled
[    6.113100] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled
[    6.113281] iwlwifi 0000:03:00.0: L1 Disabled - LTR Enabled


[root@foundation0 ~]# rfkill list
1: phy0: Wireless LAN
	Soft blocked: no
	Hard blocked: no
2: hci0: Bluetooth
	Soft blocked: no
	Hard blocked: no

```

成功解决！

