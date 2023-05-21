---
title: 安装gitlab
layout: post
published: false
categories:
tags: [ops]
---

跟着安装文档一步步的安装，但是遇到了几个坑。

1. 文档中给的 ruby 安装脚本有问题，要安装最新版的ruby。

2. nginx 安装好后，要删掉site-enabled/default.
 第一次可能会有 502 bad gameway，多试两次，多等一会就好。

3. 修改 `/home/git/.gitolite.rc` 的 `GIT_CONFIG_KEYS`, 从 `''` 改为 `'.*'`，否则无法创建新项目。

    GIT_CONFIG_KEYS             =>  '.*',


