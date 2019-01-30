---
title: 设置邮箱服务器
date: 2019-01-29 22:40:54
tags: [ops]
---

发现自己已经有足足一年多没有更新任何博客了。过去的一年中，自己越来越多的在做管理型的工作，远离了一线开发，开发笔记类的东西也就少了。

最近这段时间一直在整理自己的思路，希望能够做些能够触达用户的事情，比如搞一个公众号之类的。而各种自媒体号都需要邮箱，申请免费邮箱又是很麻烦的事，搞不好密码忘了，也很麻烦。既然自己有域名，为什么不自己搞一个企业邮箱呢。常用的是腾讯的免费企业邮箱，但是只能绑定一个域名，而我的账号下已经绑定了一个域名。于是想着自己动手搭建一个邮箱服务器。

这个邮箱服务器的主要目标是接收各种注册邮件、验证码，并不要求完善的账号管理系统。备选方案有：

1. [Postal](https://postal.atech.media/), write with ruby, MySQL
2. [Modoboa](https://modoboa.org/en/), write with python.
3. postfix
4. dovecot
5. [MailHog](https://github.com/mailhog/MailHog)
6. [tmail](https://github.com/toorop/tmail)
7. [Mail in a box](https://mailinabox.email/)
8. [MailDev](https://github.com/djfarrelly/MailDev)
9. [Inbucket](https://www.inbucket.org/)

最终选择了maildev，安装简单方便
```
npm i -g maildev
maildev --web-user xx --web-pass xx
```

使用supervisor，后台运行
```
# supervisor/conf.d/maildev.conf
[program:maildev]
command=/opt/nodejs/bin/maildev --web-user=xx --web-pass=xx -s 25 -w 1080
redirect_stderr=true
stdout_logfile=/var/log/maildev.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
stdout_capture_maxbytes=100MB
```

修改DNS，添加MX记录为服务器IP。发邮件到test@example.com 测试，打开 `http://example.com:1080/` ，可以看到自己刚发的邮件。说明已经可以有任意多的邮箱了。

把他和brook科学上网服务放在同一台服务器上，充分利用资源。

