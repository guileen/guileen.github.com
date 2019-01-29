---
title: compile ledis
layout: post
published: true
categories:
tags: [ops]
---

ledis 很简单，安装leveldb比较麻烦

```
source dev.sh
sudo sh tools/build_leveldb.sh
```

autoreconf 找不到，PKG_MODULE_CONF, LIBTOOL, AM_PROG_AR 等等问题

解决办法, 安装新版本打 automake, pkg-config, libtool

```
brew install automake
brew install pkg-config
brew install libtool
```
