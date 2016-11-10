---
title: MySQL 优化
layout: post
published: true
categories: 
tags: mysql
---

近期mysql 主从同步延迟过高，依次进行了如下优化。

1. 增加从库，将应用负载分散到多个从库，以降低从库同步延迟。

2. 查看slow query，优化慢查询，必要位置添加索引。

3. 打印所有sql日志，搜集一段时间日志后，去掉条件，按语句合并，汇总执行次数并排序。定位执行次数最高的语句，然后进行代码层面的优化，降低IO。

4. READ IO已经被降低，但CPU使用量却居高不下。SHOW PROCESSLIST; 定位到一些慢查询（执行时间小于long_query_time 但执行次数很多的语句），对这类语句再进行优化。
