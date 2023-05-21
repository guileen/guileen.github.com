---
title: 分布式事务
date: 2021-03-11 21:24:22
tags:
---


微服务架构中，分布式事务、全链路跟踪、监控报警、限流降级、灰度发布、服务网关等等都很重要，大多是比较简单的工程性问题，有成熟的解决方案。其中在理论上比较复杂的，主要就是分布式事务了。

## 异步场景的分布式事务

主服务完成事务后将结果用事件（消息队列）通知从服务。从服务消费完成事务后，将事件删除（否则将持续收到事件通知）。这一模式的主要问题是，消息队列与主事务如何保持一致。解决方案是主事务中增加一个本地Msg表，事件投递成功后，删除本地Msg。若事件投递失败，由消息补偿定时任务将未投递消息写入消息服务。

目前看来是比较完美的，但是这一方案对主业务有很大的侵入性。因此可以考虑将Msg持久化独立为一个服务。在开始主事务前，先将Msg置为Prepare状态，然后主事务完成后，Commit Msg。如果Prepare Msg失败，则主事务不会开始，如果Msg Prepare失败，但没有Commit Msg，则Msg服务会向主服务回调检测任务是否完成。RocketMQ实现了类似的机制。这一模式的主要缺点是需要写一个回调检查方法。这种方法也被成为**半投递**。

![](/img/dtx/half-message.jpg)

## 同步场景分布式事务

### 二阶段提交协议（2 Phase Commit）（XA）

![](/img/dtx/2pc.png)

2PC协议中，用户与协调者通信。事务的执行分为准备阶段和提交阶段。在准备阶段，完成资源的锁定。协调者收到所有的投票都为Yes后，通知所有参与者提交事务，否则通知参与者取消事务。为了完成事务，需要实现以下几个接口

* [参与者]canCommit(trans) -> Yes/No  协调者询问参与者能否开始任务。参与者若返回yes，需要锁定相关资源。
* [参与者]doCommit(trans)  协调者通知参与者执行他的事务。
* [参与者]doAbort(trans) 协调者通知参与者放弃事务。
* [协调者]haveCommitted(trans) 参与者调用协调者的该接口，通知协调者，自己已经完成了任务。
* [协调者]getDecision(trans) 参与者投Yes后一段时间未收到通知，参与者主动询问表决结果，主动恢复事务。

我们必须要考虑超时的情况：

* 每一个网络动作都要包含一个超时的动作，超时并不意味失败。
* 当协调者调用canCommit超时时，事务将不会开始，协调者将向所有参与者发送doAbort。
* 当参与者在canCommit返回了No之后，参与者终止事务（没有超时）
* 当参与者在canCommit返回了Yes之后超时，我们称其进入了不确定状态，参与者需要调用getDecision来决定下一步的动作。如果协调者发生故障，需要继续检测getDecision，等待协调者恢复后则可恢复事务。（可能持续的等待）

我们还需要考虑到进程崩溃的情况：

* 当参与者回复了Yes之后崩溃，后继服务需要从数据库中恢复该事务。因此参与者在回复Yes之前必须将事务状态写入数据库。
* 当协调者崩溃后，需要正确的处理getDecision

缺点：

* 在一切正常的情况下，2PC的性能是2N次请求。但如果出现了异常，则可能出现长时间的等待，并锁定了相关资源。3PC用来解决这样的问题。

### 三阶段提交协议（3 Phase Commit）

![](/img/dtx/3pc.png)

3PC与2PC的异同：

* 3PC将2PC的准备阶段拆分为『询问』和『准备』两个阶段。
* 在询问阶段，参与者不锁定资源，只返回是否可以执行。这一步避免了2PC最终表决为No却锁定了资源的情况。
* 当询问所有参与者都可以执行的情况下，才要求参与者进行准备，锁定资源。
* 询问、准备必须都成功，才会执行Commit，否则执行Abort。这与2PC是类似的。

### TCC协议

TCC本质上依然是2PC，他们的区别是TCC是服务级别的，而2PC是资源级别的（也可以是服务级别的）。在2PC、3PC中，都会对资源进行长时间的占用，同一时间只能有一个事务执行，有一个锁竞争的问题。为了解决这个问题，TCC在Try阶段，就将事务所需的资源进行预留，后续的锁只发生在预留的资源上。

![](/img/dtx/tcc.png)

为了解释这个问题，我们先来想象这样一种场景，用户在电商网站购买商品1000元，使用余额支付800元，使用红包支付200元。我们看一下在 2PC 中的流程：

Prepare 阶段：

- 下单系统插入一条订单记录，不提交
- 余额系统减 800 元，给记录加锁，写 redo 和 undo 日志，不提交
- 红包系统减 200 元，给记录加锁，写 redo 和 undo 日志，不提交

Commit 阶段：

- 下单系统提交订单记录
- 余额系统提交，释放锁
- 红包系统提交，释放锁

我们在事务执行过程中，锁定了整个用户账户。而TCC 在该场景中的流程：

Try操作

- tryX 下单系统创建待支付订单
- tryY 冻结账户红包 200 元
- tryZ 冻结资金账户 800 元

Confirm操作

- confirmX 订单更新为支付成功
- confirmY 扣减账户红包 200 元
- confirmZ 扣减资金账户 800 元

Cancel操作

- cancelX 订单处理异常，资金红包退回，订单支付失败
- cancelY 冻结红包失败，账户余额退回，订单支付失败
- cancelZ 冻结余额失败，账户红包退回，订单支付失败

我们只对参与事务的部分资源进行了锁定，因此极大的降低了锁竞争的情况，也就提升了系统的性能。缺点是，TCC的实现对业务的侵入性较强，必须由开发人员来编写。而2PC、3PC则可以抽象为统一的框架。

## AT 模式

本地关系型数据库   [Seata AT模式]http://seata.io/zh-cn/docs/dev/mode/at-mode.html

两阶段提交协议的演变：

- 一阶段：业务数据和回滚日志记录在同一个本地事务中提交，释放本地锁和连接资源。
- 二阶段：
  - 提交异步化，非常快速地完成。
  - 回滚通过一阶段的回滚日志进行反向补偿。

TODO

## SAGA

长事务解决方案，订机票的例子

TODO

[[1]分布式事务——2PC、3PC 和 TCC](https://huzb.me/2019/06/30/%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%8B%E5%8A%A1%E2%80%94%E2%80%942PC%E3%80%813PC%E5%92%8CTCC/#%E4%BA%94%E3%80%81TCC-%E5%8D%8F%E8%AE%AE)
