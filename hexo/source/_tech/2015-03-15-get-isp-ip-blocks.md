---
title: 获取运营商IP段
layout: post
published: false
categories:
tags: [network, hack]
---

转载，整理

# 过滤法

apnic.sh

```
#!/bin/bash
FILE=./ip_apnic
rm -f $FILE
wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O $FILE
grep 'apnic|CN|ipv4|' $FILE | cut -f 4,5 -d'|'|sed -e 's/|/ /g' | while read ip cnt
do
        echo $ip:$cnt
        mask=$(cat << EOF | bc | tail -1
        pow=32;
        define log2(x) {
        if (x<=1) return (pow);
                pow--;
                return(log2(x/2));
        }
        log2($cnt)
EOF)
        echo $ip/$mask>> cn.net
        NETNAME=`whois $ip@whois.apnic.net | sed -e '/./{H;$!d;}' -e 'x;/netnum/!d' |grep ^netname | sed -e 's/.*: \(.*\)/\1/g' | sed -e 's/-.*//g'`
        NETNAME=`echo $NETNAME | sed -e 's/cJ/ /g' | awk -F' ' '{ printf $1; }'`
       case $NETNAME in
       CNC)
               echo $ip/$mask >> CNCGROUP
       ;;
       CHINANET|CNCGROUP)
               echo $ip/$mask >> $NETNAME
       ;;
       CHINATELECOM)
               echo $ip/$mask >> CHINANET
       ;;
       *)
               echo $ip/$mask $NETNAME >> OTHER
       ;;
       esac
done
```

# whois3

从apnic获取电信 网通 铁通等ip的办法
　　APNIC是管理亚太地区IP地址分配的机构，它有着丰富准确的IP地址分配库，同时这些信息也是对外公开的！下面就让我们看看如何在Linux下获得一些电信运营商的IP地址分配情况：

```
shell> wget http://ftp.apnic.net/apnic/dbase/tools/ripe-dbase-client-v3.tar.gz
shell> tar xzvf ripe-dbase-client-v3.tar.gz
shell> cd whois-3.1
shell> ./configure
shell> make
```

中国网通：
```
shell> ./whois3 -h whois.apnic.net -l -i mb MAINT-CNCGROUP > /var/cnc
```

中国电信：

```
shell> ./whois3 -h whois.apnic.net -l -i mb MAINT-CHINANET > /var/chinanet
```


中国铁通：
```
shell> ./whois3 -h whois.apnic.net -l -i mb MAINT-CN-CRTC > /var/crtc
```

　　打开获取后的文件可以看到里面的信息非常详细，甚至可以看到各个分公司的负责人、电话、电子邮件等等信息。如果想得到一份整齐干净的IP地址段文件，只要用grep和awk简单过滤就可以了：）


　　使用ripe-whois3获得电信，网通等运营商的ip地址
Linux中下载安装

  http://ftp.apnic.net/apnic/dbase/tools/

ripe-whois-tools-2.3.tar.gz  tar xzvf

ripe-whois-tools-2.3.tar.gz  cd /usr/ports/net/ripe-whois3

  make install clean  rehash

查询：
中国网通: whois3 -h whois.apnic.net -l -i mb MAINT-CNCGROUP

中国电信: whois3 -h whois.apnic.net -l -i mb MAINT-CHINANET

中国铁通: whois3 -h whois.apnic.net -l -i mb MAINT-CNC-CRTC


# 在线列表

```
#!/bin/sh
FILE=/home/ip_apnic
rm -f $FILE
rm -f CNC
rm -f OTHER
rm -f CHINANET
rm -f CRTC
wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O $FILE
grep 'apnic|CN|ipv4|' $FILE | cut -f 4,5 -d'|'|sed -e 's/|/ /g' | while read ip cnt
do
    mask=$(cat << EOF | bc | tail -1
pow=32;
define log2(x) {
if (x<=1) return (pow);
pow--;
return(log2(x/2));
}
log2($cnt)
EOF)
        echo $ip/$mask
        echo $ip/$mask>> cn.net
        NETNAME=`whois $ip | grep ^netname | sed -e 's/.*:      (.*)/1/g' | sed -e 's/-.*//g'`
echo $NETNAME;
        case $NETNAME in
        CNC)
                echo $ip/$mask >> CNC
        ;;
        CNCGROUP)
                echo $ip/$mask >> CNC
        ;;
        CHINANET)
                echo $ip/$mask >> CHINANET
        ;;
        CHINATELECOM)
                echo $ip/$mask >> CHINANET
        ;;
        CRTC)
                echo $ip/$mask >> CRTC
        ;;
        *)
                echo $ip/$mask >> OTHER
        ;;
        esac
done
```

中国电信 IP地址段：
http://ispip.clangcn.com/chinatelecom.html

中国联通（网通）IP地址段：
http://ispip.clangcn.com/unicom_cnc.html

中国移动 IP地址段：
http://ispip.clangcn.com/cmcc.html

中国铁通 IP地址段：
http://ispip.clangcn.com/crtc.html

中国教育网 IP地址段：
http://ispip.clangcn.com/cernet.html

中国其他ISP IP地址段：
http://ispip.clangcn.com/othernet.html

本博缓存 uploads/2015
