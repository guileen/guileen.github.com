---
title: redis的list类型控制随机性分布
layout: post
published: true
categories: 
tags: redis
---

有这样一个需求：
1. 随机的给用户1篇文章
2. 最新的文章有更大的几率被随机到
3. 被随机到之后，文章被随机到的几率降低
4. 同一文章大约可以被最多随机到5次
5. 在文章较少时，1操作很多时，系统依然可以正常运行

实现：

```
# 新文章加入系统时 插入5份
LPUSH articles id1
LPUSH articles id1
LPUSH articles id1
LPUSH articles id1
LPUSH articles id1
# 根据随机数x取一篇文章, 结果为idx, x < N， N代表最新的N篇文章
LINDEX articles x
# 将x从articles 移除 1份
LREM articles 1 idx
# 将idx从右方插入
RPUSH articles idx
```
