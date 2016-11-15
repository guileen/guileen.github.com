---
title: 开源语音识别引擎
layout: post
published: true
categories: 
tags: [machine-learning, editor]
---

大部分的语音识别引擎是收费的，或者是闭源的。google speech API不适合做语音控制系统，只适合识别日常语言。julius是一个日本人开发的语音识别引擎，GPL协议，看起来不错，决定研究一下。

今天花了很多时间折腾atom，是github推出的编辑器，可以方便灵活的编写插件。非常希望可以用说话来编程。折腾了一些，接触了如下东西。

* sox (with flac format) 一个CLI程序可以录音。
* node-speakable  录音并调用google speech API。
* node-julius  顾名思义，node调用julius API。还没有使用。
