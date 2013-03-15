---
title: 网络游戏延迟检测技术
layout: post
published: true
categories: 
tags: 算法
---

如何检测网络延迟, 检测网络延迟很简单。但我们必须进行多次检测，计算一个平均值。

计算平均值也非常简单，但我们必须剔除那些异常值。如何剔除异常值，鄙人通过google找到了几种算法，

只有这一种我能看得懂，貌似也是最容易实现的，叫做 [肖维勒准则(Chauvenet's criterion)](http://en.wikipedia.org/wiki/Chauvenet's_criterion)

平均值

    mean = sum(v) / n

标准差

    sd = sqrt(sum(v(i) * v(i) - mean * mean, i=1 to n) / (n - 1))

[肖维勒准则(Chauvenet's criterion)](http://en.wikipedia.org/wiki/Chauvenet's_criterion)

如果某样本数据d满足

    |v(d)| > w(n) * sd

则认为v(d)是一个异常数据，将其剔除。

W(n) 是一个常数，可以用查表法获得

Table of Chauvenet’s Criterion for data rejection, with curve fit equation

Chauvenet's Criterion
  
    --------------------------
    | n          | c         |
    --------------------------
    | 3          | 1.38      |
    | 4          | 1.54      |
    | 5          | 1.65      |
    | 6          | 1.73      |
    | 7          | 1.8       |
    | 10         | 1.96      |
    | 15         | 2.13      |
    | 25         | 2.33      |
    | 50         | 2.57      |
    | 100        | 2.81      |
    --------------------------
    |c = 0.9969+0.4040*ln(n) |
    --------------------------

很奇怪，通过公式获得的结果和表上给的结果并不一致。
