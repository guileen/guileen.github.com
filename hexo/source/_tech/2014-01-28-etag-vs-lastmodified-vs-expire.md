---
title: Etag与Last-Modified以及浏览器永久缓存的比较
layout: post
published: false
categories:
tags: HTTP
---

Etag 和 Last-Modified 的功效类似，但是Etag出现较晚。

Last-Modified 适合静态文件。

Etag 适合动态内容的变更。

永久缓存。。。这只适合类似图片、视频等内容。对js，css等静态文件可以通过加版本号的方式来永久缓存之。

xxx.js?etag=12345 这种方式来永久缓存
