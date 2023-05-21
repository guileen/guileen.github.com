---
title: web前端脏乱差及其解决之道
layout: post
published: false
categories:
tags: [web, engineering]
---

## 这是一个软件工程问题

先吐槽一下，遇到许多所谓“软件工程师”，根本没有“软件工程”的概念，make，ant，持续集成，自动化测试，一概无视，这样的人只能称码农，不能叫软件工程师。
很多牛逼的软件工程师喜欢自称程序员，导致很多菜鸟认为会写程序就足够了，殊不知“programmer”、“coder”是牛人们的谦称————不懂软件工程之人不足与之论代码。

## Web前端脏乱差

Web前端长期以来很混乱，虽然不断的有人用各种框架，工具来改善前端开发过程，web前端依然让人感觉脏乱差。究其原因有三：
* javascript语言层面缺乏包机制。这是requirejs之类所试图解决的问题
* web前端包管理机制问题复杂，不仅需要考虑js，还要考虑css和html。这是bower试图解决的问题
* 有合并、压缩的需求，虽然有很多工具很好的完成了压缩的工作，但合并一直缺乏优雅的方案。

## 前端社区割裂

基于前面说到的一些问题，导致社区产生了大量风格迥异的js代码。这些代码也许可以一起很好的工作，但将错就错的行为让社区更加混乱。

这过程中产生了一些子社区，比如jquery，这导致了javascript社区的分裂。
Argular试图重新定义前端开发的整个流程，google一直在尝试让web前端的开发过程变得像传统软件开发一样清晰，比如GWT和Dart。
Argular取得了一定的成功，但依然有不少web工程师对Argular比较抵触。
所有试图以框架来解决web开发问题的，最终的结局要么是消亡，要么是割裂。

## 解决之道

正确的选择只有一条，就像其他编程语言一样：

* 统一社区风格, 利用社区的力量。
* 不应该让整个社区依赖某一个框架，我们只需要制定行业标准。

目前有些工具在解决这些问题：

* [Bower](http://bower.io/) 是包管理工具
* [grunt](http://gruntjs.com/)是构建工具
* CMD, AMD的一堆工具
* [component](https://github.com/component/component)则是既包含包管理，也包含简单的构建，同时component还是一个CMD工具。

我个人认为component是目前最好的解决方案。因为 component 包含了 bower + grunt + requirejs 的主要功能，而我们没空去学那么多乱七八糟的工具。

有人可能会问，component的存在是否也会造成前端社区的割裂？component要做的不是框架，而是社区标准，所以component的存在不会造成社区的割裂，只会让社区更加繁荣。

component 社区虽然也可以兼容jquery这样的框架，但这不是component所推荐的做法。component的风格是大量的小型的库，比如superagent, eacape-html, dom，每个库只做一件明确的事情。


## 后记

感谢TJ holowaychuk，给我们带来了太多美好的东西。不过自从TJ转投Go语言社区后，似乎是被Go社区"从语言层面解决软件工程问题"的哲学所感染，给component的发展带来了一些不确定性。目前component的官方网站[component.io](http://component.io)已经无法访问。TJ 在component的[一条issue](https://github.com/component/component/issues/587)中表达了自己的一些观点：“遗留的npm/browserify是最坏的东西，说实在的Go的方法好多了，只要ES6的module loaders可以玩了。Browserify最终会玩完，所有的都会哈哈，长期来看，他们都不管用，构建一点都不好玩”

原文

> The rest of npm/browserify is mostly bad stuff, a Go approach would be much better IMO, once ES6 module loaders are in play. Browserify will eventually die out too, they all will haha, long-term none of them make sense, builds are no fun
