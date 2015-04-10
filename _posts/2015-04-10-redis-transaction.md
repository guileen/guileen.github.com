---
title: Redis事务
layout: post
published: true
categories: 
tags: 
---

Redis不支持Rollback，但是redis有更轻量的方法满足常见的我们对事务需求。

我们有时需要对数据同时进行一批修改，这些操作应该同时被修改成功。Redis提供了Multi和Exec来实现批量操作。

比如，点赞这个操作，需要在文章点赞用户列表中增加一个用户，同时要给文章点赞数加1，可以用如下命令来完成：

```
MULTI
SADD user:tom:vote:posts 123    // TOM 赞了123
SADD post:123:voters tom   // 123 被 TOM赞了
INCR post:123:votecount  // 123 点赞数＋1
EXEC
```

如果我们要求一人只能对一篇文章赞一次，那我们必须在客户端增加一个判断。

```
if SISMEMBER user:tom:vote:posts 123 
MULTI
SADD user:tom:vote:posts 123 
SADD post:123:voters tom
INCR post:123:votecount
EXEC
endif
```

但上面但代码存在着一个bug，假设tom非常快连续两次对同一文章点赞，两次 SISMEMBER 都判断为false，则这篇文章会被tom赞两次。redis提供了WATCH命令来实现这个功能。

```
WATCH user:tom:vote:posts
if SISMEMBER user:tom:vote:posts 123 
MULTI
SADD user:tom:vote:posts 123 
SADD post:123:voters tom
INCR post:123:votecount
EXEC
endif
```

在 WATCH和EXEC之间，被WATCH的key如果发生了修改，那么EXEC将会自动放弃。WATCH user:tom:vote:posts 表示，tom如果同一时刻又赞了一篇文章，那么本次操作将失败。

除此之外，Redis的lua script也是事务性的。更详细的资料可以参考[这里](http://redis.io/topics/transactions)

