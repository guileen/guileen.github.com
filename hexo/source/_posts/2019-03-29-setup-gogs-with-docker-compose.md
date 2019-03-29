---
title: 使用docker-compose设置Gogs
date: 2019-03-29 16:58:02
tags:
---


创建 ~/gogs/docker-compose.yml

```
version: '2'
services:
  gogs:
    container_name: gogs
    image: gogs/gogs
    volumes:
      - /data/gogs/:/data
    ports:
      - "3080:3000"
      - "3022:22"
    restart: always
```

执行

```
sudo docker-compose up -d
```

Nginx配置

```
server {
  listen 80;
  server_name git.example.com;

  location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:3080;
        proxy_redirect off;
  }
}
```

配置注意事项：

* *SSH Port:* Use the exposed port from Docker container. For example, your SSH server listens on 22 inside Docker, but you expose it by 10022:22, then use 10022 for this value. Builtin SSH server is not recommended inside Docker Container
* *HTTP Port:* Use port you want Gogs to listen on inside Docker container. For example, your Gogs listens on 3000 inside Docker, and you expose it by 10080:3000, but you still use 3000 for this value.
* *Application URL:* Use combination of Domain and exposed HTTP Port values (e.g. http://192.168.99.100:10080/).
