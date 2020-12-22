---
title: Ubuntu 16 安装 IKEV2 VPN SERVER
date: 2020-12-18 10:50:16
tags:
---

https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ikev2-vpn-server-with-strongswan-on-ubuntu-16-04

## 命令

注意替换 server_name_or_ip 为服务器地址

```
sudo apt-get install strongswan strongswan-plugin-eap-mschapv2 moreutils iptables-persistent

mkdir vpn-certs
cd vpn-certs

ipsec pki --gen --type rsa --size 4096 --outform pem > server-root-key.pem
chmod 600 server-root-key.pem
ipsec pki --self --ca --lifetime 3650 \
--in server-root-key.pem \
--type rsa --dn "C=US, O=VPN Server, CN=VPN Server Root CA" \
--outform pem > server-root-ca.pem

ipsec pki --gen --type rsa --size 4096 --outform pem > vpn-server-key.pem

ipsec pki --pub --in vpn-server-key.pem \
--type rsa | ipsec pki --issue --lifetime 1825 \
--cacert server-root-ca.pem \
--cakey server-root-key.pem \
--dn "C=US, O=VPN Server, CN=server_name_or_ip" \
--san server_name_or_ip \
--flag serverAuth --flag ikeIntermediate \
--outform pem > vpn-server-cert.pem

sudo cp ./vpn-server-cert.pem /etc/ipsec.d/certs/vpn-server-cert.pem
sudo cp ./vpn-server-key.pem /etc/ipsec.d/private/vpn-server-key.pem

sudo chown root /etc/ipsec.d/private/vpn-server-key.pem
sudo chgrp root /etc/ipsec.d/private/vpn-server-key.pem
sudo chmod 600 /etc/ipsec.d/private/vpn-server-key.pem

sudo cp /etc/ipsec.conf /etc/ipsec.conf.original
echo '' | sudo tee /etc/ipsec.conf

sudo vim /etc/ipsec.conf
```

### /etc/ipsec.conf

```
config setup
    charondebug="ike 1, knl 1, cfg 0"
    uniqueids=no

conn ikev2-vpn
    auto=add
    compress=no
    type=tunnel
    keyexchange=ikev2
    fragmentation=yes
    forceencaps=yes
    ike=aes256-sha1-modp1024,3des-sha1-modp1024!
    esp=aes256-sha1,3des-sha1!
    dpdaction=clear
    dpddelay=300s
    rekey=no
    left=%any
    leftid=@server_name_or_ip
    leftcert=/etc/ipsec.d/certs/vpn-server-cert.pem
    leftsendcert=always
    leftsubnet=0.0.0.0/0
    right=%any
    rightid=%any
    rightauth=eap-mschapv2
    rightdns=8.8.8.8,8.8.4.4
    rightsourceip=10.10.10.0/24
    rightsendcert=never
    eap_identity=%identity
```

## 防火墙设置

可选
```
sudo ufw disable
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -F
iptables -Z
```

默认保持
```
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
```

VPN端口
```
sudo iptables -A INPUT -p udp --dport  500 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 4500 -j ACCEPT
sudo iptables -A FORWARD --match policy --pol ipsec --dir in  --proto esp -s 10.10.10.10/24 -j ACCEPT
sudo iptables -A FORWARD --match policy --pol ipsec --dir out --proto esp -d 10.10.10.10/24 -j ACCEPT
sudo iptables -t nat -A POSTROUTING -s 10.10.10.10/24 -o eth0 -m policy --pol ipsec --dir out -j ACCEPT
sudo iptables -t nat -A POSTROUTING -s 10.10.10.10/24 -o eth0 -j MASQUERADE
sudo iptables -t mangle -A FORWARD --match policy --pol ipsec --dir in -s 10.10.10.10/24 -o eth0 -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360

```

可选，禁用其他
```
sudo iptables -A INPUT -j DROP
sudo iptables -A FORWARD -j DROP
```

重启防火墙

```
sudo netfilter-persistent save
sudo netfilter-persistent reload
```

## 网络配置

sudo vim /etc/sysctl.conf

### /etc/sysctl.conf
```
. . .

# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.ip_forward=1

. . .

# Do not accept ICMP redirects (prevent MITM attacks)
net.ipv4.conf.all.accept_redirects = 0
# Do not send ICMP redirects (we are not a router)
net.ipv4.conf.all.send_redirects = 0

. . .

net.ipv4.ip_no_pmtu_disc = 1
```

## 重启
`sudo reboot`

## 客户端测试

`scp hk:~/vpn-certs/server-root-ca.pem ./`

安装并信任证书，测试

## Relay server 

```
brook relay -f :500 -t 1.2.3.4:500 &
brook relay -f :4500 -t 1.2.3.4:4500 &
```