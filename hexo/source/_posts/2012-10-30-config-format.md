---
title: 配置文件格式比较
layout: post
published: true
categories: 
tags: data-format
---

1. java项目用的比较多的是 XML、properties，容错性很差，配置起来相当痛苦。

2. 动态语言的项目往往用代码来配置，node用js配置，python用python配置，ruby用ruby配置。
优点是简单
缺点：
a. 不能跨语言共享配置
b. 配置文件里面可以写代码，本身是有风险的
c. 运维人员必须了解相应的语言

3. ini文件，是一个不错的选择，容错性较强。只是对于list类型的配置支持不好，比如一个cluster的所有host，port信息。

4. YAML 比较简洁，是个不错的选择，但也有人不习惯这种极简的风格。
http://www.yaml.org/spec/1.2/spec.html#Preview

5. JSON现在非常流行，但JSON的缺点也很明显的，如下面的语句是非法的

```
{key: 'value',} //注释
```

key 必须是 "key", value 必须是双引号，} 前多了个逗号，不支持注释。

前段时间node社区出现了一种新格式，叫做JSON5，免去了一些JSON的痛苦，https://github.com/aseemk/json5

如下面的配置是合法

```
{key: 'value',} //注释
```

可惜他出现于node社区，noder们可以使用JS代码来代替JSON5。所以JSON5可能无法在node社区有所发展，其他的语言实现它的可能性也就更低了。
