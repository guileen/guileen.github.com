---
title: 靜態網站生成器
layout: post
published: true
categories: 
tags: web
---

靜態網頁依然應用的很廣，但是開發一個靜態網站並不像想象的那麼簡單，快速，易於維護。

搭建慢。首先我們需要搭建項目的結構，引入我們需要的js，css，layout文件。

復用難。也許同樣的網頁我們之前已經做過一個，但當我們需要再做一個的時候，我們還需要從頭再做一次。如果我們直接複製粘貼此前的代碼到新項目中，
對代碼的合併，網站名稱，logo等信息的修改，刪除不需要的代碼，要花去我們很多的時間。一個網站下的多個頁面在結構上應該是復用的。

維護繁。對於一個已經完成的靜態網站，當我們想要修改它的時候，也並不是那麼簡單。比如我們要修改一個樣式，運氣好的話我們只需要修改一兩處css即可，
運氣差的話我們可能要修改DOM結構，但同一類頁面元素的DOM結構是分散在很多地方的，比如contact頁面，about頁面，某個landing page。
這就讓我們的代碼變得難以維護。

如果我們對靜態網站做一個總結的話，一般來說包含以下內容。

* lyaout
網站的基本外觀框架。
* partial
網站的常用局部組件。
* data
網站基本配置，如標題，logo，base url，等。
* pages
幾個頁面，比如about，contact。
* posts
很多文章。

於是靜態網站生成器（static site generator）產生了。

現在比較常見的靜態網站生成器：
* jekyll
Ruby 實現，github支持，插件豐富，支持諸如tag，分類，本博客使用的就是jekyll。
* [harp](http://harpjs.com)
* [hexo](http://zespia.tw/hexo)
* [docpad](docpad.org) 基於coffeescript
* [assemble](assemble.io)
* [cabin](cabinjs.com)
* [Yeoman](yeoman.io) nodejs環境。yeoman不能算是一個靜態網站生成器，你可以叫它項目生成器。它可以生成諸如。

我的選擇 Yeoman + x，Yeoman 的設計是面向開發者的。

對於x的選擇，必須是nodejs的，從github關注量來看，docpad最多。

計劃用這種方式來實現項目主頁，Landing Page。
