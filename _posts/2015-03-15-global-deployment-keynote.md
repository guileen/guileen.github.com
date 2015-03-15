---
title: 全球部署要点
layout: post
published: true
categories: 
tags: 
---

NSServer domain : 就近请求DNS
NSServer IP 分布式 : 就近解析目标地址
Cloud Load Balance : Load Balance, DDoS Protection, Single-Point-Failure
CDN 层: 静态资源的CDN, HTTP, OPEN的，非动态的
反向缓存层 : 动态结果的缓存, compress, etag, last-modified, 优化, 如 varnish
Logic Node : Main Logic
数据路由层 ：根据hash原则，分区标志，进行数据路由，在本地或远程获取数据。
数据缓存 : 本地热门数据缓存，远程数据缓存
Data Cluster : Distribution, Cluster, CAP理论和BASE思想，反ACID。

客户端信息采集：
    DNS信息采集
    PING 延迟采集
    Cloud Load Balance, CDN 延迟采集
    HTTP 失败、慢链接 日志

BASE思想：
Basic Available: 基本可用，支持分区失败
Soft state: 状态可以有一段时间不同步
Eventually consistent: 最终一致，而不是实时一致。

BASE实践：
数据按区域分布，各地有数据中心，存储当地的数据，同时各地都有缓存，缓存对当地用户而言的热点数据。


1. DNS

全球的客户端一律解析至各自最近的服务器。 需要自架DNS，[GEODNS](https://github.com/abh/geodns)。

参考获取各国内运营商ip地址，可知道线路，但并不能知道IP所对应的地域。

根据ip地址的线路进行部署。

这一层同时负责一部分入侵检测工作

在攻击发生时，如果攻击是执行域名的，可以通过DNS将大量未知来源的请求

2. 发布工具

全球部署的效率。

服务升级导致的服务暂停时间缩短。

发布流程：

对试点发布节点：
    宣布某节点进入维护状态。
    代码发布，服务重启，基本测试。
    宣布某节点上线。
    监测节点状态。

对所有待升级节点进行升级。

3. 灰度发布

