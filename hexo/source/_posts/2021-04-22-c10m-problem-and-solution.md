---
title: c10m单机千万连接问题及解决方案
date: 2021-04-22 14:24:01
tags:
---


C10m是继c10k问题之后提出的新问题，指单机1000万连接问题。40gbps网卡、32核、256G内存，这样的配置理论上已经可以处理千万并发连接了。但虽然硬件已经能够满足条件了，但是软件系统依然是复杂的。这就是C10M问题。

使用Go语言开发的TCP server，可以比较轻松的保持1000万的连接。大约消耗56G内存，用于连接对象和goroutine，不包含业务对象。但仅仅保持空闲连接并不够，最重要的是拥有更高的包处理速度（Packet per second），和更低的时延。

Robert Graham的演讲[《C10M Defending The Internet At Scale》(pdf)](https://www.cs.dartmouth.edu/~sergey/cs258/2013/C10M-Defending-the-Internet-at-Scale-Dartmouth-2013.pdf) [(youtube)](https://www.youtube.com/watch?v=D09jdbS6oSI)回答了C10M的问题原因：内核不是解决方案，而是问题本身。因为内核处理数据包是经过了一个复杂的过程。对于C10m的定义如下：

* 千万并发连接
* 每秒百万连接接入
* 每秒千万数据包
* 10gb/s
* 10微秒延迟
* 10微秒抖动
* 10核CPU并行

其中最核心的指标，是前3项。而面临的挑战主要是**用户态协议栈和多核并发问题**。用户态协议栈可以在网关类、云原生等应用中发挥极大的价值，但是对于业务层的开发并不友好。用户态协议栈的技术有SDP、BPF、DPDK等。我们需要**重点关注的是多核并发情况下的网络编程问题**。

## 为什么多核编程是复杂的？

大多数的程序在高于4核的CPU上不能发挥更好的性能，有时甚至会降低性能。其中主要的影响因素是CPU的缓存流水线。L1 cache 4个cycle（cpu时钟），L2 cache 12个cycle，L3 30 cycles，内存 300 cycles。如果命中L1、L2缓存，性能则是很高的，若缓存miss性能则会降低。在高并发的情况下，我们最好是保证程序是绑定在某个CPU上执行的。

![img](/Users/admin/work/guileen.github.com/hexo/source/img/c10m/cpu-cache.png)

在千万并发情况下，因为上下文的切换过于频繁，缓存miss的情况将大大增加。在上下文切换时，如果同一个连接的处理线程不是绑定在同一个CPU上的，那么将进一步加剧缓存miss的情况。

除缓存miss情况外，cacheline还存在一种**伪共享**的问题，会造成性能的下降。当从内存中取单元到cache中时，会一次取一个cacheline大小的内存区域到cache中，然后存进相应的cacheline中, 所以当你读取一个变量的时候，可能会把它相邻的变量也读取到CPU的缓存中(如果正好在一个cacheline中)，因为有很大的几率你回继续访问相邻的变量，这样CPU利用缓存就可以加速对内存的访问。这本来是一种优化策略，避免加载相邻变量时多次访问内存。但是在多核并发的情况下，则可能造成性能下降。

![preview](https://segmentfault.com/img/bVcNCKX/view)

当两个CPU操作两个相邻的变量时，这段相同的数据被加载到内存中。这将产生数据竞争，为了保证一致性，性能必然会下降。

![preview](https://segmentfault.com/img/bVcNCLf/view)

因此，**保持CPU亲和性**，就成为了C10M中需要重点关注的问题。其中端口复用、prefork、taskset这些技术比较值得尝试。我将这些资料都整理在了 [guileen/c10m-test](github.com/guileen/c10m-test)

