---
title: 在命令行解析HTML
date: 2020-12-14 17:02:32
tags:
---

最近要做音乐app，但没有素材。 一个音乐爬虫

https://github.com/BeanWei/MusicSpider

网页版的内容比较容易解析，为了快速了解数据结构，需要一个好工具。于是找到了pup

```
go get github.com/ericchiang/pup

curl -s https://news.ycombinator.com/ | pup 'table table tr:nth-last-of-type(n+2) td.title a json{}'
```


以上解析可以用于命令行的分析，但若要生成更精简的数据结构，可以用下面的结构。

const { parse } = require('node-html-parser')
const fs = require('fs')

var dom = parse(fs.readFileSync("./test_list.xml", "utf8"))
var res = dom.querySelectorAll('li').map(el=> {
     return {
         src: el.querySelector("img").getAttribute("src"),
         title: el.querySelector("a.tit").innerText,
         href: el.querySelector("a.tit").getAttribute("href"),
         cnt: el.querySelector("span.nb").innerText,
     }
 })
console.log(JSON.stringify(res,null,'  '))
