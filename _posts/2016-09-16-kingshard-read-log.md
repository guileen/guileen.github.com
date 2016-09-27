---
title: Kingshard阅读笔记
layout: post
published: true
categories: mysql
tags: mysql
---

KingShard 是 mysql 代理，可实现分库分表等功能。但因业务复杂，无法使用，故阅读其源码，以便修改。

代码版本：
2016-09-12
3c4a1db63226cb1384047a3f915d10e0594228d1

入口: cmd/

服务启动： proxy/server/server.go

Server.Run()
服务逻辑

Server.onConn(net.Conn)
客户端连接逻辑

*  Server.newClientConn(net.Conn)
  客户端连接初始化

客户端连接：proxy/server/conn.go

ClientConn.IsAllowConnect()
判断客户端IP是否合法

ClientConn.Handshake()
握手

ClientConn.Run()
客户端逻辑

ClientConn.readPacket()
PacketIO.ReadPacket()
拆包逻辑

ClientConn.dispatch(data)
包分发逻辑
data[0] mysql命令
* QUIT  c.handleRollback() c.Close()
* QUERY c.handleQuery(string(data))
* PING
* INIT_DB c.handleUseDB 分配后端节点 backend.Node
* FIELD_LIST
* STMT_PREPARE
* STMT_EXECUTE
* STMT_CLOSE
* STMT_SEND_LONG_DATA
* STMT_RESET
* SET_OPTION
其它命令不支持,log

命令执行成功后，写结果给客户端，某些命令只需 ClientConn.writeOK

执行查询 ClientConn.handleQuery
ClientConn.preHanleShard 不确定什么时候会用
解析sql
handleSelect
handleExec
handleBegin
handleCommit
handleRollback


后端节点: backend/node.go backend.Node
GetSlaveConn
GetMasterConn

后端连接：
基类 backend/backend_conn.go backend.Conn
子类 backend/db.go backend.BackendConn

写入命令，读取返回
writeCommandStr
readOK

SQL 语法解析
sqlparser
需要执行 make，通过yacc编译

其它
Counter  计数器
