---
title: github博客專業教程
layout: post
tags: github jekyll
---

## 準備知識
git, github, markdown

## 爲什麼要把博客host在github？

* 彰顯Geek風采
這是主要的目的，雖然github支持自定義域名，但我更喜歡github.com的子域名以彰顯我的碼農身份。

* 你的每篇文章擁有版本控制，每次修改都有版本記錄。
* 文件，markdown，內容樣式分離
想想你留在個類網站上的文章，自己建站所寫的博客

## Github
用過Github的人都知道，github會自動將markdown文件渲染爲html。所以許多項目直接用Readme.md作爲文檔，非常的簡單有效。有些高級點的github玩家則會爲項目創建一個github page，
你可以使用github page generator來生成頁面，如果你對自己的html/css非常有信心，
那麼我強烈建議你使用[git-extras](https://github.com/visionmedia/git-extras)的
[gh-pages](https://github.com/visionmedia/git-extras/blob/master/bin/git-gh-pages)命令來創建一個乾淨的gh-pages分支，
在這個分支上你可以隨心所欲的編寫你的項目主頁。

![github page generator](/upload/2012/github-page-gen.png)

既然github可以host項目主頁，那麼他是否可以host用戶主頁呢？當然可以，否則，本文就無從談起了。方法很簡單，你只需要創建一個 USERNAME.github.com 的項目即可host你的個人主頁。文中所有USERNAME都表示你的github用戶名。

但是如果只是一堆的html/js/css堆砌而成的個人主頁，是完全無法與博客相提並論的。本文既然叫做《github博客專業教程》，自然不能只教大家host一堆靜態文件。

## Step 1. 創建
USERNAME.github.com

## Step 2. 安装jekyll

Mac
```
gem update --system
```

```
gem install jekyll
```

```
jekyll --server --auto
```

## Step 3. index.html

## Step 4. \_post

## Step 5. layout

## Step 6. google analytics

## Step 7. comment

## Step 8. share

## Step 9. RSS

## Step 10. github info

## 參考
http://jekyllrb.com/
https://github.com/mojombo/jekyll
https://help.github.com/categories/20/articles
http://erjjones.github.com/blog/How-I-built-my-blog-in-one-day/