---
title: Too many open files 的解决办法
s: fix-too-many-open-files
date: 2016-11-14 22:26:31
tags: [ops, network, tcp]
---

在开发TCP网络应用的过程中，我们经常会遇到“Too many open files”这个问题。这说明你的程序以达到Linux所允许的打开文件数上限。你需要按照以下方式来提升：

### 每用户上限：

打开 `/etc/security/limits.conf`
在末尾添加：

```
*         hard    nofile      500000
*         soft    nofile      500000
root      hard    nofile      500000
root      soft    nofile      500000
```

修改后，你需要logout并重新login。

#### pam-limits

据说对于Daemon进程需要额外的步骤，但目前我并不需要。如果以上改动不能对你有所帮助，可能需要以下步骤。

打开 `/etc/pam.d/common-session`

添加以下内容：

```
session required pam_limits.so
```

### 系统级限制

这项设置应该大于没用户限制。

打开 `/etc/sysctl.conf`

添加以下内容：

```
fs.file-max = 2097152
```

运行：

```
sysctl -p
```

这会增加系统级的最大打开文件数。

## 验证效果

使用以下命令验证系统级最大打开文件数

```
cat /proc/sys/fs/file-max
```

Hard Limit

```
ulimit -Hn
```

Soft Limit

```
ulimit -Sn
```

### 检测用户限制

将`www-data`替换为你希望检测的用户。

```
su - www-data -c 'ulimit -aHS' -s '/bin/bash'
```

### 检测运行中的进程限制

将`XXX`替换为PID

```
cat /proc/XXX/limits
```

今日在一台新启动的服务器上，系统级、用户级配置都正常，唯独进程的limits仅为默认1024。进程使用的是supervisor守护启动，使用supervisor restart进程后，limits依然为1024，后重启了supervisor服务，limits恢复所设定数值。
