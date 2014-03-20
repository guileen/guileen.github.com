---
title: Karam：多瀏覽器平臺的測試工具
layout: post
published: true
categories: 
tags: web, 前端
---

nodejs讓js脫離了瀏覽器，它的包管理工具npm讓js代碼能夠更好的分享，此後前端開發因此產生了巨大的變革。

前端開發最痛苦的過程莫過於跨瀏覽器測試了。我一直期盼有一種更好的前端測試方案，當然不只是我這麼想。

ArgularJS團隊在開發過程中希望有一種更好的測試方案，他們定義了3條理想的測試工具應該具備的特點：

1. `it('should be fast')`

> 它（‘應該很快’）

2. `it('should use real browsers')`

> 它（‘應該使用真正的瀏覽器‘）

3. `it('should be reliable/stable')`

> 它（’應該是穩定的‘）

在2012年11月27日，google發佈了博客[Testacular-Spectacular Test Runner for JavaScript](http://googletesting.blogspot.com/2012/11/testacular-spectacular-test-runner-for.html)
介紹他們所開發的測試執行器（Test runner）Testacular，之後他們將此項目改名爲Karma。

## 安裝Karma

> npm install karma-cli -g
> cd projecthome
> npm install karma
> karma init

blabla, 讓我們跳過這一部分吧，直接給大家介紹最佳實踐。

## 最佳實踐

### 安裝yeoman, grunt, karma

> sudo npm install yo -g
> sudo npm install generator-argular -g
> sudo npm install grunt-cli -g
> sudo npm install karma-cli -g

### 創建項目

> mkdir /path/to/project
> cd /path/to/project
> yo argular

### 安裝一些測試模塊

> npm install karma-jasmin --save-dev
> npm install karma-chrome-launcher --save-dev

### 執行測試
> grunt test

### 增加其他瀏覽器

編輯karam.conf.js將browser改爲
```js
browsers:['Chrome', 'Firefox', 'Safari']
```

> npm install karma-firefox-launcher --save-dev
> npm install karma-safari-launcher --save-dev

### 再次執行測試

> grunt test
