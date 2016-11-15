---
title: LocalStorage的异常处理
layout: post
published: true
categories: web
tags: [web]
---

当达到localStorage容量上限时，按照标准描述会抛出 `QUOTA_EXCEEDED_ERR`. 但这个 `QUOTA_EXCEEDED_ERR` 到底是什么？一个常量？一个字符串？[各浏览器的实现却不一样](http://chrisberkhout.com/blog/localstorage-errors/).

所以我使用了以下简单的方法来处理这个异常。

```js
try{
    localStorage.setItem(key, value);
}catch(e) {
    localStorage.clear();
}
```
