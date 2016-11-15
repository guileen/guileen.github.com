---
title: TCP 连接优化
layout: post
published: true
categories: 
tags: [network, tcp]
---

see: http://www.cnblogs.com/fczjuever/archive/2013/04/17/3026694.html

/etc/sysctl.conf文件

　　/etc/sysctl.conf是一个允许你改变正在运行中的Linux系统的接口。它包含一些TCP/IP堆栈和虚拟内存系统的高级选项，可用来控制Linux网络配置，由于/proc/sys/net目录内容的临时性，建议把TCPIP参数的修改添加到/etc/sysctl.conf文件, 然后保存文件，使用命令“/sbin/sysctl –p”使之立即生效。具体修改方案参照上文：

```
net.core.rmem_default = 256960
net.core.rmem_max = 513920
net.core.wmem_default = 256960
net.core.wmem_max = 513920
net.core.netdev_max_backlog = 2000
net.core.somaxconn = 2048
net.core.optmem_max = 81920
net.ipv4.tcp_mem = 131072  262144  524288
net.ipv4.tcp_rmem = 8760  256960  4088000
net.ipv4.tcp_wmem = 8760  256960  4088000
net.ipv4.tcp_keepalive_time = 1800
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_sack = 1
net.ipv4.tcp_fack = 1
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.ip_local_port_range = 1024  65000
net.ipv4.tcp_max_syn_backlog = 2048
```
