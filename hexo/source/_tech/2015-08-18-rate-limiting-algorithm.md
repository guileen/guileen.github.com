---
title: 频率限制算法
layout: post
published: false
categories:
tags: [algorithms, architecture]
---

实现接口访问频率限制并不难，只要一些计数器，计时器就可以了。但接口频率限制的目的是减少IO，所以，如果能够在不增加IO的情况下做到频率限制才是完美的，但在集群环境下，这一算法并不精确，但我认为这种损失是值得的。

[一个来自Stackoverflow的答案](http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm/668327#668327)

```
rate = 5.0; // unit: messages
per  = 8.0; // unit: seconds
allowance = rate; // unit: messages
last_check = now(); // floating-point, e.g. usec accuracy. Unit: seconds

when (message_received):
  current = now();
  time_passed = current - last_check;
  last_check = current;
  allowance += time_passed * (rate / per);
  if (allowance > rate):
    allowance = rate; // throttle
  if (allowance < 1.0):
    discard_message();
  else:
    forward_message();
    allowance -= 1.0;
```
