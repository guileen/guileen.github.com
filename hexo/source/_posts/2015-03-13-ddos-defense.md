---
title: DDoS 防御笔记
layout: post
published: true
categories: 
tags: [SA, security, DDoS]
---

DDoS 意为分布式拒绝服务攻击

## DDoS 分类：

* IP欺骗攻击 利用RST位欺骗服务器大量合法用户连接错误，用户将会掉线。
* ICMP-Flood 
* SYN-Flood
* UDP-Flood  网络带宽耗尽攻击。
* HTTP-Flood 又名 CC 攻击

## 应对DDoS的方案

### DNS攻击
攻击你的DNS服务器，导致拒绝服务。选择专业的DNS服务。

DNS层也可以选择自架DNS，主要是用于第一时间进行攻击检测，将检测到的攻击解析至一个黑洞地址，也可以解析至BAT的地址。

服务分级。将信任的，重要的客户解析至单独设立的服务区。

对于客户IP的日志分析，确定哪些是老用户。

DNS攻击防御也有类似HTTP的防御手段，第一方案是缓存。其次是重发，可以是直接丢弃DNS报文导致UDP层面的请求重发，可以是返回特殊响应强制要求客户端使用TCP协议重发DNS查询请求。

特殊的，对于授权域DNS的保护，设备会在业务正常时期提取收到的DNS域名列表和ISP DNS IP列表备用，在攻击时，非此列表的请求一律丢弃，大幅降低性能压力。对于域名，实行同样的域名白名单机制，非白名单中的域名解析请求，做丢弃处理。

对于每个向DNS请求的IP，都进行计数。在每分钟请求数正常时，形成白名单。在每分钟请求激增时，拒绝所有非白名单请求。

#### 流量攻击

网络架构层面

流量攻击是最常用的手法，也是最难防御的手法。而流量攻击通常可以达到10G的流量，这是普通网站所无法负担的。解决方案有2：一是买带宽，买机器，这就是拼钱，也是拼运维。二是将自己的网站置于强大的保护盾之后。

怎么理解这个保护盾？普通网站没有财力购买如此大的网络流量，并且这些资源在大多数的时候都是无用的，只有在攻击发生时，起到冗余带宽的作用。现在有专业的公司开始从事这种业务，他们拥有大量的带宽和入侵检测技术，将你的真实IP置于这个保护盾之后，让这个保护盾分担掉大部分的攻击，你的网站的带宽压力就降低了。

国内云盾，国外CloudFlare, rockspace
http://totaluptime.com/solutions/cloud-load-balancing/
http://www.fortinet.com/
http://dyn.com/traffic-director/
http://aws.amazon.com/cn/elasticloadbalancing/
http://www.hpcloud.com/products-services/load-balancer
https://cloud.google.com/compute/docs/load-balancing/http/


关键字：cloud load balance

#### SYN-Flood

运维层面

SYN-cookie 技术。在SYN握手时不立即分配资源。

地址状态监控技术。

### 系统安全

运维层面

SSH, Fail2Ban, Firewall, SYN-Flood 策略

### CC攻击

拒绝http-proxy的访问。
人机识别，HTTP，用js的方式，将IP加入黑名单。
移动网络也需要考虑人机识别。

对于合法数据的甄别。
安全性，数据校验，非法数据记录丢弃，加入黑名单。

静态化，高性能

### 测试工具

架设一个目标服务器，自己尝试攻击自己，或者让黑客攻击自己。
