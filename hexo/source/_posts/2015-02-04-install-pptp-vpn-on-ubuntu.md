---
title: Ubuntu安装pptp vpn 防火墙
layout: post
published: true
categories:
tags: [ops]
---

打开ufw后，pptp无法连接。转载一篇文章。[原文](http://www.darrenfang.com/2014/01/install-pptp-vpn-on-ubuntu/)

有时需要访问一些国外的技术网站，但是国内网络时常连接不上，只好在服务器上面安装VPN来访问了。本文介绍如何在Ubuntu Server 12.04中安装及配置PPTD VPN服务。

关于VPN的说明可以查看维基百科：http://zh.wikipedia.org/wiki/VPN

安装PPTPD和防火墙UFW

```
sudo apt-get install pptpd ufw
```

配置防火墙

```
# 允许SSH
sudo ufw allow 22
# 允许HTTP
sudo ufw allow 80
# 允许VPN
sudo ufw allow 1723
# 启用UFW
sudo ufw enable
```

注意，需要允许SSH端口，不然无法用SSH登录服务器。

配置PPTPD

```
sudo vi /etc/ppp/pptpd-options
```

配置加密方式。使用加密连接时，请查看以下配置是否在改文件中，默认是存在的

```
refuse-pap
refuse-chap
refuse-mschap
require-mschap-v2
require-mppe-128
```

添加DNS配置。可以根据实际情况修改。

```
ms-dns 114.114.114.114
ms-dns 8.8.4.4
```

配置IP地址。

```
sudo vi /etc/pptpd.conf
```

添加以下配置。

```
# 根据实际网卡名修改
bcrelay eth0
# 本地IP，可以写成服务器的公网IP
localip 192.168.0.2
# 分配的地址池，可以和服务器IP不在一个网段内
remoteip 192.168.1.100-110
```

添加VPN帐号

```
sudo vi /etc/ppp/chap-secrets
```

添加以下内容，用tab键分隔。

```
vpn *       123456        *
```

其中用户名是vpn，密码是123456。 重启PPTPD服务。

```
sudo /etc/init.d/pptpd restart
```

重启后就可以连接上VPN服务器了。但是发现除了能连接上服务器外，不能访问外网。这时候还需要配置NAT。 第五步：配置NAT 启用IPv4转发

```
vi /etc/sysctl.conf
```

添加以下内容

```
net.ipv4.ip_forward=1
```

保存退出后执行以下命令

```
sudo sysctl -p
```

修改UFW配置文件

```
vi /etc/default/ufw
```

将“DEFAULT_FORWARD_POLICY” 的值改为 “ACCEPT” 修改UFW规则

```
vi /etc/ufw/before.rules
```

在*filter这个规则前添加以下内容

```
# NAT table rules
*nat
:POSTROUTING ACCEPT [0:0]
# Allow forward traffic to eth0
-A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE
# Process the NAT table rules
COMMIT
```

其中第5行改成地址池中的网段。 再次重启PPTPD服务就可以了
