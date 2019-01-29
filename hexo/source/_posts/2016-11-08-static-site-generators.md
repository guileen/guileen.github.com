---
title: 开源静态网站生成工具
layout: post
published: true
categories:
tags: [generator]
---

有博客订阅者反馈我的博客ATOM输出有问题，总有两篇已unpublish的博客出来诈尸。这个是个老问题，当时也是因为总是有这两篇博客捣乱所以unpublish了，但完全无效。

自己的博客一直没有认真维护，只是偶尔随手记录，更没有想到有人订阅了，闻之顿感责任重大。计划认真整理一下自己的博客。

那两篇诈尸的博客，或是github的bug，或是jekyll的bug，未能验证。细思之，将博客系统完全交予github管理，的确不够合理，于是考虑使用本地生成静态文件再行push的方式，代替先push再由github jekyll生成静态文件的方式。顺便也更新一下自己博客的样式。

关于jekyll，也有不少问题，比如不能生存tag page等，也考虑更换一下生成器。奈何目前的静态网站生成器着实太多，无从选择。幸有有心人整理了一个列表，[staticgen.com](https://www.staticgen.com/)，包含了github的关注数、项目使用的语言，模版语言等信息，选择方便了许多。
