---
title: Deploy node.js apps with supervisor
layout: post
published: false
categories:
tags: [ops]
---

许多的文章介绍Node应用部署都是使用upstart 或是手动编写 init script, 我个人是很不习惯为每个应用去配置启动脚本。

本文所要介绍的supervisor是配置式的，配置启动命令，环境变量，进程数，等等。

进入正题：

创建用户nodeapp

    sudo adduser --disabled-login --gecos 'Node App' nodeapp
    cd /home/nodeapp

clone project

    sudo -u nodeapp -H git clone repo
    cd repo

Install dependencies modules

    sudo -u nodeapp -H npm install -d

安装 supervisor

    apt-get install supervisor


配置

    [program:yourappname]
    command=/usr/local/bin/node /home/nodeapp/yourappname/app.js
    process_name=%(program_name)s%(process_num)s
    numprocs=1
    directory=/tmp
    umask=022
    priority=999
    autostart=true
    autorestart=true
    startsecs=10
    startretries=3
    exitcodes=0,2
    stopsignal=TERM
    stopwaitsecs=10
    user=nodeapp
    redirect_stderr=false
    stdout_logfile=/home/nodeapp/yourappname/logs/stdout.log
    stdout_logfile_maxbytes=1MB
    stdout_logfile_backups=10
    stdout_capture_maxbytes=1MB
    stderr_logfile=/home/nodeapp/yourappname/logs/stderr.log
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    stderr_capture_maxbytes=1MB
    environment=NODE_ENV=production,B=2
    serverurl=AUTO

启动

    supervisorctl
    > help
    > update
    > status
    > restart yourappname
