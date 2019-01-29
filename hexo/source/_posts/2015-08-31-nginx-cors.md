---
title: Nginx解决跨域问题
layout: post
published: true
categories:
tags: [ops, nginx]
---

Nginx 根据条件设置跨域访问权限

```bash
#
# CORS header support
#
# One way to use this is by placing it into a file called "cors_support"
# under your Nginx configuration directory and placing the following
# statement inside your location block(s):
#
#   include cors_support;
#
# A limitation to this method is that Nginx doesn't currently send headers
# specified by add_header when the backend returns a 4xx or 5xx status code.
#
# For more information on CORS, please see: http://enable-cors.org/
# Forked from this Gist: https://gist.github.com/michiel/1064640
#

set $cors '';
if ($http_origin ~* 'https?://(localhost|www\.yourdomain\.com|www\.yourotherdomain\.com)') {
        set $cors 'true';
}

if ($cors = 'true') {
        add_header 'Access-Control-Allow-Origin' "$http_origin";
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Mx-ReqToken,X-Requested-With';
}

if ($request_method = 'OPTIONS') {
        return 204;
}
```
