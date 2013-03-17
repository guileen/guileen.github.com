---
title: 肖维勒准则
layout: post
published: true
categories: 
tags: algorithm
---

数据中并不总是合法数据，为了更好的完成统计，我们必须剔除异常的数据。

如何剔除异常的实验数据(Outlier rejection)，有许多的方法。

介绍一种易于实现的方法，叫做[肖维勒准则(Chauvenet's criterion)](http://en.wikipedia.org/wiki/Chauvenet's_criterion)

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
