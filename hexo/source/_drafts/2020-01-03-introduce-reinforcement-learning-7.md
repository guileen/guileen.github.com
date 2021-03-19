---
title: 强化学习简介（七）：Actor-Critic
date: 2020-01-03 17:25:03
tags:
categories: AI
---

对于Q-learning算法而言，我们学习了一个价值函数\`Q\`，而策略则选择最大Q值并按照一定概率探索。对于策略梯度而言，我们学习了一个策略函数\`pi\`，对于累计价值则使用单步奖励按折扣累计。那么很自然的可以想到，我们可以同时学习策略函数和价值函数，其各自更新方法不变。在学习价值函数时，以策略函数来进行探索。学习策略函数时，以价值函数结果为累计价值。

![Actor-Critic](/img/rl-7/1.png)

```
初始化 s
for each step do
  r = R(s, a); s' = P(s, a)
  δ = r + γ * Q(s', a') − Q(s, a)
  θ = θ + α * log π(s, a) * Q(s, a)
  w = w + βδ
  s = s'
  a = a'
end
```