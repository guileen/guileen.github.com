---
title: 集群运维工具
layout: post
published: true
categories: 
tags: [SA]
---

[17ce](www.17ce.com)
[ip.cn](ip.cn)

zookeeper
docker
[kubernetes](https://github.com/googlecloudplatform/kubernetes)
[codis](https://github.com/wandoulabs/codis)
ssdb
stridecd
devops - 开发运营



## 直接Mark！开源的DevOps开发工具箱

来源CSDN| 作者张红月

开源工具DevOps监控工具开源
摘要：在DevOps的整个流程中，使用一些开源工具可以促进开发与运维之间的沟通，有利于项目的管理，甚至可以达到事半功倍的效果。
DevOps是一组过程、方法与系统的统称，用于促进开发（应用程序/软件工程）、技术运营和质量保障（QA）部门之间的沟通、协作与整合。在DevOps的整个流程中，使用一些开源工具可以促进开发与运维之间的沟通，有利于项目的管理，甚至可以达到事半功倍的效果。

本文作者Richard Kraaijenhagen是Owlin创始人，全栈工程师，数据科学家。他收集了DevOps开发可能用到的所有工具，并且把它们按照职责进行分类，本文摘取了部分工具分享给大家，这些工具也可以用于日常软件方面的开发，所以，大家直接Mark吧！



包&产品管理工具

Chocolatey：Chocolatey是Windows下一款开源的命令行包管理软件 ，简单说这就是Windows的apt-get；
FPM：全称是Effing package management，该死的软件包管理器，极大的缓解了多个平台构建软件包(deb,rpm,等)的痛苦；
Herd：是一个基于Twitter Murder的文件分布系统；
Vagrant Cachier：Vagrant的一个插件，用于缓存包方面的管理；
WiX Toolset：提供一组最强大的工具集来帮助你创建Windows安装包。该工具集从XML源代码构建你的Windows安装程序包，可以无缝集成到构建过程；
Boxstarter：利用Chocolatey包管理工具来自动化安装软件和创建可重复、脚本化的Windows环境；
Elita：Elita是一个利用git和salt进行持续部署（部署作为服务）和API-driven基础设施的引擎/框架；
Fig：主要用来跟Docker一起来实现的快速隔离的开发环境；
Pulp：Pulp是一个用来管理软件库以及相关内容的平台；
Veewee：Veewee是一个开源工具，用来创建和配置轻量级、可再生、便捷式虚拟机环境。

日志&监控
AmonOne：现代化的自托管服务器监控工具；
Anthracite：一个事件/日志改变/管理应用程序；
collectd3：是一个可视化的collectd系统性能统计工具；
collectd：是一个守护(daemon)进程，用来收集系统性能和提供各种存储方式来存储不同值的机制；
Diamond：是一个基于Python的守护程序，主要用来收集系统指标，并且把它们发布到Graphite（或其它）工具中；
Errbit：是一个用于收集和管理程序错误的开源工具；
Sensu：一个开源的监控框架；
Logstash：是一个应用程序日志、事件的传输、处理、管理和搜索的平台。你可以用它来统一对应用程序日志进行收集管理，提供Web接口用于查询和统计；
log.io：一个实时的开源日志监控工具；
FnordMetric：是一个基于redis/ruby的实时事件跟踪应用，是个收集和可视化时间序列数据的框架，用户可以在几分钟内创建漂亮的实时分析仪表盘；
Logster：是一个工具，读取日志文件然后创建Graphite 或 Ganglia可用的指标数据。比如你可能使用logster来图形化在你的Web Server日志中的HTTP响应发生数量；
Kibana：是一个为Logstash和ElasticSearch提供的日志分析的Web接口。可使用它对日志进行高效的搜索、可视化、分析等各种操作；
Monit：是一款功能非常丰富的进程、文件、目录和设备的监测软件，用于Unix平台。 它可以自动修复那些已经停止运作的程序，适合处理那些由于多种原因导致的软件错误；
Metrics：这并不是Java库，而是基于Go的一个轻量级的检测器；
Graphite：是一个用于采集网站实时信息并进行统计的开源项目，可用于采集多种网站服务运行状态信息；
Ganglia：Ganglia是一个跨平台可扩展的、高性能计算系统下的分布式监控系统，如集群和网格；
Server Density：一个跨平台的监控系统；
Folsom：Folsom是一款受 Coda Hale's metrics启发的、基于Erlang的度量系统；
CMB (Cloud Message Bus)：是一个高可用、横向扩展的队列和通知服务，兼容AWS SQS和SNS；
Glances：是一款用于Linux、BSD的开源命令行系统监视工具，它使用Python语言开发，能够监视CPU、负载、内存、磁盘I/O、网络流量、文件系统、系统温度等信息。
Uptime：使用Node.js、MongoDB和Twitter Bootstrap开发的远程监控系统；
Icinga：Nagios的扩展版本；
Packetbeat： 是开源应用监控和包跟踪系统；
Zipkin：是Twitter的一个开源项目，允许开发者收集Twitter各个服务上的监控数据，并提供查询接口；
Dead Manâs Snitch：是一款监控Heroku Scheduler、计划的监视工具；
Statsd：是一个Node.js的daemon程序，简单，轻巧。使用的UDP协议，可以和Graphite图片渲染应用结合；
Riemann：一个网络监控系统；
Puppet Dashboard：Puppet Dashboard是一个Web接口，为Puppet提供节点分类和报告功能，是一个开源的配置管理工具；
jmxtrans：jmxtrans是一款非常强大的工具，使用它可以轻易生成基于json的配置文章，然后再以你想要的格式输出；
Scales：跟踪服务器状态和统计指标，使你全面掌握服务器状态，还可以发送指标到Graphite来图像呈现或者向文件写入崩溃信息；
Zabbix：是一个基于Web界面的提供分布式系统监视以及网络监视功能的企业级的开源解决方案；
Graylog 2：Graylog2是一个用来将系统日志syslog保存到MongoDB中的工具。
进程管理

Bouncy：可以作为HTTP路由主机；
Supervisor：是一个客户端服务器系统，允许用户监控和控制类Unix操作系统上的进程数；
God：由Ruby实现的进程监控框架。
服务发现 
Consul：简化了分布式环境中的服务的注册和发现流程，通过HTTP或者DNS接口发现。支持外部SaaS 提供者等；
etcd：是一个高可用的Key/Value存储系统，主要用于分享配置和服务发现；
Apache ZooKeeper：是Apache Hadoop的一个子项目，它主要是用来解决分布式应用中经常遇到的一些数据管理问题；
Weave：创建一个虚拟网络并连接到部署在多个主机上的Docker容器。
持续集成和交付

Buildbot：是一个系统的自动化编译/测试周期最需要的软件，以验证代码的变化。通过自动重建和测试每次发生了变化的东西，在建设迅速查明之前，减少不必要的失败；
Cabot：是一个开源，自我托管的监控工具；
Jenkins：是基于Java开发的一种持续集成工具，用于监控持续重复的工作；
Hubot：基于脚本具有很高的灵活性，任何人都可以编写自己的脚本来扩展基本功能；
Hudson：是一个可扩展的持续集成引擎，主要用于：持续、自动地构建/测试软件项目、监控一些定时执行的任务；
CruiseControl.rb：是一个持续集成服务器，它可以让团队里的每个人随时了解项目的健康状况和进度；
OpsBot：是一个开源的、可插入的改善通信的机器人。
希望这些工具能够给开发者带来实实在在的帮助，想要查看更多工具，大家可以 访问原文，原文中的工具列表会持续更新。

最后，再跟大家分享一个 DevOps BookMarks，这里面涉及了DevOps方方面面的工具和内容，有兴趣的同学可以前去学习。
