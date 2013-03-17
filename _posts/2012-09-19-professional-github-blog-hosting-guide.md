---
title: github博客專業教程
layout: post
tags: github
---

## 準備知識
git, github, markdown

## 爲什麼要把博客host在github？

* 彰顯碼農風采
* 你的每篇文章擁有版本控制，每次修改都有版本記錄。
* 文件，markdown，內容樣式分離。

## Github
用過Github的人都知道，github會自動將markdown文件渲染爲html。所以許多項目直接用Readme.md 作爲文檔，簡單有效。有些高級點的github玩家則會爲項目創建一個github page，
你可以使用github page generator來生成頁面，如果你對自己的html/css非常有信心，
那麼我強烈建議你使用[git-extras](https://github.com/visionmedia/git-extras)的
[gh-pages](https://github.com/visionmedia/git-extras/blob/master/bin/git-gh-pages)命令來創建一個乾淨的gh-pages分支，
在這個分支上你可以隨心所欲的編寫你的項目主頁。

![github page generator](/upload/2012/github-page-gen.png)

既然github可以host項目主頁，那麼他是否可以host用戶主頁呢？當然可以，否則，本文就無從談起了。方法很簡單，你只需要創建一個 USERNAME.github.com 的項目即可host你的個人主頁。文中所有USERNAME都表示你的github用戶名。

但是如果只是一堆的html/js/css堆砌而成的個人主頁，是完全無法與博客相提並論的。本文既然叫做《github博客專業教程》，自然不能只教大家host一堆靜態文件。

## Step 1. 創建repository

假定你已經有了github帳號，我的github用户名是`guileen`，請將本文中的`guileen`一律替換爲你的github用戶名。

在github上創建一個新的Repository，命名爲 guileen.github.com，恭喜你，你已經有了一個屬於自己的博客空間，而且你可以隨心所欲的定製它。

接下來，把這個庫clone到本地。

    git clone git@github.com:guileen/guileen.github.com.git

## Step 2. index.html

在项目根目录下创建 index.html

    <html>
        <head>
            <title>Hello</title>
        </head>
        <body>
            <h1>Hello world</h1>
        </body>
    </html>

将这个文件添加到git中

> git add index.html
> git commit -m 'first commit'
> git push origin master

当你将这个文件push到github之后，访问 http://guileen.github.com ，就可以看到你的主页了。
就像你所看到的，github会自动host这个库下的静态文件，也包括 js/css/images。不过有部分文件不在次列，稍候介绍。

## Step 3. 安装jekyll

大家可能会以为，github page只能host静态文件，无法完成类似，分类，分页，日期等功能。对于这些需求，github用一种很巧妙的方法来实现了。

Github初期是使用ruby开发的，现在ruby依然是github主要使用的编程语言。在ruby这样一个富有创造力的社区，诞生过很多神奇的开源项目。
而github就是使用了一个叫做jekyll的ruby项目。

Mac

    gem update --system
    gem install jekyll
    jekyll --server --auto

## Step 4. _config.yml

    # Configure of jekyll

    # github default configurations
    safe: true
    lsi: false
    pygments: true

    # override jekyll configurations

    # use redcarpet more like github
    markdown: redcarpet

    # My configurations
    title: 桂糊涂的流水账
    ga: UA-00000000-0 


## Step 4. \_post

## Step 5. layout

## Step 6. google analytics

## Step 7. comment

使用 [Disqus](https://disqus.com) 服务

## Step 8. highlight

## Step 9. share

## Step 10. RSS

[atom.xml](https://github.com/guileen/guileen.github.com/blob/master/atom.xml)

## Step 11. github info

## 參考

* http://jekyllrb.com/
* https://github.com/mojombo/jekyll
* https://help.github.com/categories/20/articles
* http://erjjones.github.com/blog/How-I-built-my-blog-in-one-day/
