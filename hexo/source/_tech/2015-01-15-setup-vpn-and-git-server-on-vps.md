---
title: 自己动手搭建VPN和Git仓库
layout: post
published: false
categories:
tags: [ops]
---

工作中是否想过自己动手搭建VPN服务？如果你是码农，是否想过顺便搭建个git私有仓库？

自己搭建VPN和Git仓库，贵不贵？github个人版私有仓库7美元一个月，5个私有仓库。不过，读完本文，你将以5美元/月的成本，收获一个VPN，一个SSH Tunnel，以及一个不限数量的git私有仓库。


## 需要准备什么？
需要有一个VPS了。一个安装了ubuntu操作系统的VPS。最低配置的就行。当然得在外面的机房，你懂的。
为什么选ubuntu？因为我懒，谢谢。

推荐[DigitalOcean](https://www.digitalocean.com/?refcode=6c7bd4a13044)，或者[Linode](https://www.linode.com/?r=94d2619aa76f5ffbd8d0869d575829f311322f69)

## 到底选什么VPN协议？
VPN主要有L2TP，PPTP，以及IPsec三种。本文不打算详细讲解VPN的协议原理，也不讲如何选择，只讲答案：选PPTP，因为搭建简单。如果你的目的和我一样，只是为了能够方便工作，那么就选PPTP吧，至于什么加密啥啥的，我不是太care。

## 如何搭建PPTP服务
搭建PPTP服务这一步有点麻烦，我曾经踩了不少坑，花了一整天的时间才网vpn网络连通。你需要知道如何设置iptables，ppp，pptpd。

不过别怕，懒人们有福了！我知道iptables，ppp，pptpd的设置你都不想关心，你只关心把服务run起来然后设置用户名密码。
一键脚本：[github.com/nowall/setup-simple-pptp-vpn](https://github.com/nowall/setup-simple-pptp-vpn/blob/master/setup.sh)

```
wget https://raw.githubusercontent.com/nowall/setup-simple-pptp-vpn/master/setup.sh
sh setup.sh
```

执行完后，控制台会提示你用户名密码（随机生成）。编辑/etc/ppp/chap-secrets 可以修改用户名密码

```
用户名 pptpd 密码 *
```

## 如何安装git服务
你一定听过gitlab，不过这货占用内存太大，另外配置复杂，维护困难，不适合在VPS上用。今天给大家介绍一个利器，[gogs](gogs.io)，用go语言开发，内存占用小的git服务。
[下载gogs](http://gogs.io/docs/installation/install_from_binary.html)

```
sudo useradd -m git
sudo su git
wget http://gogs.dn.qbox.me/gogs-xxx.zip
unzip gogs-xxx.zip
cd gogs-xxx
nohup scripts/start.sh&
```

浏览器访问 http://你的ip:3000 。第一步要进行设置，建议选择，sqlite数据库，因为省事。

## VPS选择哪个机房？

如果选择[Linode](https://www.linode.com/?r=94d2619aa76f5ffbd8d0869d575829f311322f69)，建议选用Tokoy（东京）机房，速度很快。

DigitalOcean的价格更便宜，并且支持按小时付费，而且他的快照服务是免费的。机房建议选择[DigitalOcean SFO数据中心](https://www.digitalocean.com/?refcode=6c7bd4a13044)，虽然在某些网络中SGP（新加坡）速度很快，但是本人在电信网络中实测，SGP机房非常不稳定。SFO（旧金山）机房综合比较是个不错的选择。

## 如何给你的VPS提供商汇报问题？

网络不通，速度慢的时候，你需要把你的问题反馈给你的VPS提供商，最好提供一些数据。
ping ip 日志
traceroute ip 日志
mtr日志
mtr -rwc 100 112.64.205.210
最好还有从远程主机的控制台 mtr -rwc 100 本地外网ip（通过很多网站可以查到自己的外网ip）
