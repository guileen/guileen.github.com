---
title: 一个移动端快速原型开发框架
layout: post
published: false
categories: 
tags: android, ios, agile
---

有许多想法，但是不能快速实现美观的原型，感觉很郁闷。构思了一个基于webview的原型开发框架。以期提高原型的开发效率。
可以用来做demo。

为什么不用Phonegap? Phonegap希望所有的内容都用html + js 来实现，其实无论开发效率还是执行效率，都很低。


## 整体设计

hybrid模式，项目整体上使用原生UI开发，提供极强的可配置性，配置通过URI来实现，这个URL可以是应用内的Resource URL，
也可以是服务端的URL。对于内容难以通过配置来完成的，使用webview实现。

## 功能组件

BootLoader 项目启动器，加载最初的资源URL，配置各UI的配置，以及项目整体属性，检查更新。

```
{
    ui: {
        nav: "android.resource://xxxx/nav.json",
        splash: "http://xxxx/splash.json",
        login: "xx://xx/xx.json"
    }
    icon: "...",
    name: "XX App",
    version: '1.2.3'
}
```

JSBridge
    注入JS，可以通过JS跳转到某个UI。
    可以读写取指定文件夹内的文件

HTTPBridge
    每个Http请求发出的统一入口
    发请求的时候需要带上参数，如session或token之类的。

Splash 

```
{
  [
    {bg: 'xx://xx/xxxx.jpg'},
    {bg: 'xx://xx/xxxx.jpg'},
    {bg: 'xx://xx/xxxx.jpg'}
  ]
}
```

Login

```
{
  api : {
    method: 'post'
    url: 'http://xxx.xx/user/login
    usernameFieldName: 'email'
    passwordFieldName: 'password'
  }
}
```

Navigation

```
{
  type: '' // tab 式的或是左滑 式的
  items: [
    {
      txt: 'xx'
      icon: 'xx://xx/xx.icon'
      action: 'xxview'
      params: []
    },
    {
      txt: 'xx'
      icon: 'xx://xx/xx.icon'
      action: 'xxview'
      params: []
    },
  ]
}
```

ActionBar

```
{
  icon: ''
  name: ''
  buttons: [
    {
        icon: 'search'
        action: 'search'
        params: []
    }
    {
        icon: 'add'
        action: 'webview'
        params: ['xxx/add.html']
    }
    {
        icon: 'menu'
        action: 'menu'
        params:[
          {icon: '', txt:'', action: '', params: []}
          {icon: '', txt:'', action: '', params: []}
          {icon: '', txt:'', action: '', params: []}
        ]
    }
  ]
}
```

MainContent 一个webview

```
{
    pullToRefreash: true
    url: ''
}
```

Search

```
{
    searchUrl: 'http://www.google.com/?q={keyword}'
    completionUrl: 'http://www.xxx.com/autocompletion/?q={input}'
}
```
