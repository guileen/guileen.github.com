---
title: 通用的項目文件結構
layout: post
published: true
categories: programming
tags: programming, node.js
---

在項目開發過程中經常會因爲“應該將某個文件放在哪個文件夾下”，以及文件夾應該叫什麼名字這種問題而糾結。在經歷一次次痛苦糾結後，決定整理一個通用的項目文件結構。

```
/root
|- README ( LICENSE etc)
|- Makefile ( Gruntfile.js Dockfile etc)
|- /build (if you have complex build scripts)
|- /deps (node_modules, bower_components)
|- /test (test cases)
`- /src
    |- example.conf (example config or default config)
    |- /res (public resources, pack to client)
    |  |- img
    |  |- i18n
    |  `- ...
    |- /etc (miscs)
    |- /utils (utils depends nothing, reuseable)
    |- /core (engine, framework part, depends on utils, reuseable)
    |- /models (or services, talking to data and lowlevel interface)
    |- /routes (handle client request, most use in HTTP, sometimes it called `commands` in CLI or socket program.)
    |- /actions (controllers, UI delegates)
    |- /views (templates, UI, etc)
    `- /helper (like utils, but it is highly relatated with /core /models /actions /views.)
```
