---
title: Component 与 Bower 和 Grunt 的对比
layout: post
published: true
categories: 
tags: web, 前端, 软件工程
---


先吐槽一下，遇到许多所谓“软件工程师”，根本没有“软件工程”的概念，make，ant，gradle，持续集成，自动化测试，一概无视，这样的人只能称码农，不能叫软件工程师。
很多牛逼的软件工程师喜欢自称程序员，导致很多菜鸟认为会写程序就足够了，殊不知“programmer”、“coder”是牛人们的谦称————不懂软件工程之人不足与之论代码。

## Web前端脏乱差

Web前端长期以来很混乱，虽然不断的有人用各种框架，工具来改善前端开发过程，web前端依然让人感觉脏乱差。究其原因有三：
* javascript语言层面缺乏包机制。这是requirejs之类所试图解决的问题
* web前端包管理机制问题复杂，不仅需要考虑js，还要考虑css和html。这是bower试图解决的问题
* 有合并、压缩的需求，虽然有很多工具很好的完成了压缩的工作，但合并一直缺乏优雅的方案。

Bower 是包管理工具，grunt是构建工具，component则是既包含包管理，也包含构建的过程，同时component还具备requirejs的Common JS构建功能。

简言之 component 包含了 bower + grunt + requirejs 的主要功能。

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

component 社区不使用jquery这样的框架，只有一些小型的库，比如superagent, eacape-html, dom这样小型的库，每个库只做一件明确的事情。

感谢TJ holowaychuk，给我们带来了太多美好的东西。
