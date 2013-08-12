---
title: 消息服务器集群的管理
layout: post
published: true
categories: 
tags: 
---

N台服务器，N > 10，相互之间会有通信，每台服务器都会开启数个进程监听数个端口用于接收来自其他服务器的消息。每个进程都必须设置一个id，其他服务器发送消息时需要根据目标服务器的id获取该id对应的进程ip和port。

## 静态配置

```
all_server_ids[id] = {host: 'xxx', port: 1234};
```
启动每个进程时，用参数指定id，如 
```
./run-server --id 123，
```

```
host, port = all_server_ids[id]
```
缺点：配置繁琐，服务器多的时候容易出错。

## 用KeyValue数据库注册， 

在进程启动后， id = db.incr('server-id'); db.set('sid:'+id, 'host:port');
在发送消息时，host, port = db.get('sid' + id)
缺点：获取host,port的操作会很频繁，无法根据消息接收人id做hash来得知目标服务器id。

## 中央服务器
所有消息都通过一个中央服务器转发。所有节点服务器只与中央服务器通讯。所有节点服务器使用统一的配置连接中央服务器。消息发送至中央服务器。
