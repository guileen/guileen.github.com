---
title: Nginx 限制访问频率
layout: post
published: true
categories: 
tags: 
---

使用[Nginx http\_limit\_req](http://nginx.org/cn/docs/http/ngx_http_limit_req_module.html)可以限制访问的频率。

```
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=50r/s;
    ...
    server {
        ...
            location /search/ {
                limit_req zone=one burst=5 nodelay;
            }
```

