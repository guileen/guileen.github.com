---
title: Cursor 与 Page
layout: post
published: false
categories:
tags: [architecture]
---

分页是一个非常普通的业务需求。对于一个有大量数据的列表，我们必须分段查看数据。在API层面的设计上，一般会使用 page, limit 两个参数来控制分页。

缺陷：page, limit 在性能上有问题，翻页时可能会有新插入的数据导致位置错乱。在数据过滤上有问题，在判断尾页上有问题。

优势：可以准确的跳转到中间任意页。


Cursor 是一种比较适合移动互联网的分页方式。它可以保证列表数据是连续的。
