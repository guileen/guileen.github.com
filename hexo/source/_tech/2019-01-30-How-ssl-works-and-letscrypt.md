---
title: How ssl works and Letscrypt
date: 2019-01-30 20:49:39
tags:
---

## SSL/TLS 解决了什么问题？

假设A给B发信息，直接明文发送，那么所有的中间传输节点，都可以截获明文，这种通信是不安全的，想象一下你的密码全部在网上明文传输，是不是很危险。

现在A将信息加密后传输给B，B解密信息，加密密钥和解密密钥是相同，这种加密算法叫做对称加密算法。题是，A如何把密钥告诉B？如果依然通过同一个中间人告诉B，一旦中间人知道这个密钥，那么传输过程就依然是不安全的了。

这时非对称加密算法出现了，非对称加密的加密解密需要两把钥匙，我们称之为公钥和私钥，所谓公钥就是可以公开的钥匙，可以安全的分享出去。使用公钥加密的数据必须用私钥解密，使用私钥加密的必须用公钥解密。如果A和B之间进行通信，那么AB双方首先交换各自的公钥，保留各自的私钥，这个过程是安全的。A要给B发信息则使用B的公钥加密，因为只有B自己拥有私钥，所以只有B可以解密信息，反之依然。这是非对称加密的第一个用途，防止中间人破译信息。非对称加密还有另一个用途————身份验证，如果A要向B表明身份证明自己的确是A，只需要按照B的要求加密一段随机字符串S即可，A使用自己的私钥加密S，将加密结果发送给B，B使用A提供的公钥进行解密，若结果为S，则证明对方的身份的确是A，这样就完成了认证过程，我们常用的ssh公钥登录，就是这个原理。

一切看起来很完美，但是还有一个问题没有解决。假设A、B之间有一个中间人C，AB之间的所有消息都经过C传递。这是C在这个传输过程做了手脚，当AB交换公钥时，A把公钥发给C，希望C把A的公钥转交给B，可是这是C没有把A的公钥交给B，而是把C的公钥交给了B，B误以为C的公钥就是A的公钥。在B把公钥发给A的过程中，C做了同样的手脚。这时A、B手上都是C的公钥，而C手上也有A、B的公钥。这时A给B发消息时，会使用C的公钥加密，C则先用C的私钥解密得出原文完成信息窃取，再用B的公钥加密信息发给B。AB都认为自己进行了安全的传输，一切天衣无缝。更可怕的是C还可以直接篡改信息。谁有能力做这件事？你的网络提供商，你连接的免费wifi，网络上的交换节点，都有能力实施这个中间人攻击。那么问题来了，既然交换公钥这种非对称加密手段都无法奏效，还搞毛线呢？这时就需要CA上场了。

    A  ---- A的公钥 --->  C  ---- C的公钥 ---> B
    A  <--- C的公钥 ----  C  <--- B的公钥 ---- B
    A  --C公钥加密信息-->  C  -- B公钥加密信息--> B
    A  <-C公钥加密信息---  C  <- A公钥加密信息--- B

CA的全称是Certificate Authority，即证书颁发机构。A为了保证自己的公钥不被中间人篡改，会先将自己的公钥交给CA，CA用自己的私钥教秘A的公钥，B使用CA的公钥解密A的公钥，只要CA的签名的公钥没有问题，则A的公钥也必然没有问题。那么又有一个新的问题来了，如果中间人C伪造CA的公钥怎么办？这个问题的解决方案比较粗暴，CA的公钥是直接写在浏览器里的。如果CA的公钥被篡改，浏览器会直接提示不安全的网络连接。因此我们也需要警惕一些山寨浏览器，如果没有道德底线的约束，他们完全可以篡改CA证书，为网络监听大开方便之门。

因为CA需要各大浏览器厂商的共同认可，因此是个壁垒很高的生意。如果一个网站需要提供安全的网络连接，则需要将自己的网站公钥通过CA生成一个认证公钥，这个认证的公钥也就是证书，这个证书不便宜。想象一下，每一年你都需要付出两千块钱，就是为了证明你是你，这钱花的是不是挺冤枉。你说我的网站就不提供安全传输不就完了吗，反正我这信息也都是公开的，也没什么值得监听的。不行，因为很多业务场景，第三方接口，必须要求你提供安全的网络连接。这就增加了开设一个网络服务的成本，尤其是增加了玩票的成本，小微创新就会受影响。

![](/img/https_flowchart.jpg)

现在就该今天的主角上场了，[Letsencrypt](https://letsencrypt.org/)，他是一个免费、自动化的证书颁发机构。今天就向大家安利一下Letsencrypt。 Letsencryt在web server上运行了一个证书管理代理（Certificate management agent）的程序。假设我们希望设置`https://example.com`的证书。那么一共有两个步骤，第一步，证明你拥有exmaple.com，第二步，代理程序可以请求（request）、更新（renew）以及废除（revoke）证书，

Letsencrypt根据agent公钥来验证账号，agent第一次与Letsencrypt交互时，Letsencrypt会要求agent证明自己拥有某个域名。agent会询问需要自己做什么来证明自己拥有这个域名，这时Letsencrypt会下发一组任务，比如添加某个DNS记录，在网站下提供某个制定的资源。这和传统的CA证书机构类似。当agent完成操作后，CA就认为该agent已经拥有这个域名了，之后的域名更新都可以通过agent操作。

```
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot
$ sudo certbot certonly -d ipub.io -d *.ipub.io --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```
跟着提示填写，其中一步要求在DNS记录中添加一个TXT，修改后继续，准确无误的话，证书会在/etc/letsencrypt/live/ipub.io/ 目录下, 修改nginx配置文件。

```
server {
  listen 443 ssl;
  listen [::]:443 ssl;
  keepalive_timeout 70;

  root /var/www/leen.ipub.io;
  index index.html index.htm;
  server_name leen.ipub.io;
  ssl_certificate  /etc/letsencrypt/live/ipub.io/fullchain.pem;
  ssl_certificate_key  /etc/letsencrypt/live/ipub.io/privkey.pem;
  location / {
    try_files $uri $uri/ /index.html =404;
  }
}
```
