---
title: Nginx log 模版
layout: post
published: true
categories: 
tags: nginx
---

记录 `$upstream_addr` `$upstream_response_time` 有助于定位请求，定位延迟，定位问题。

```
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent $request_time $upstream_addr $upstream_response_time "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for" "$gzip_ratio"';
    access_log  /var/logs/nginx/access.log main;
```
