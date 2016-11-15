---
title: GameObject properties adapter ———— 游戏数值开发要点
layout: post
published: true
categories:
tags: [game-dev]
---

游戏数值是动态的，可叠加的，物品，天赋，被动技能，Buff，光环，都会改变一个GameObject的属性。

游戏数值开发的难点在于抽象。程序员必须将策划的语言抽象出来，否则物品、天赋、技能、Buff、等等会让你的代码千头万绪，错综复杂。

而如果能够很好的抽象出这些东西，将会一目了然，胸有成竹。

鄙人曾在一款塔防游戏中负责数值系统的开发。

数据抽象
----

* 静态数据 - 设定 - Settings - S

* 游戏对象 - 实例 - Instance - I

* 实例的设定 - 实例的静态数据 - Instance Settings - IS

* 实例当前的未叠加基本状态 - 实例裸体状态 - Instance Naked Data - IND

* 状态叠加器们 - Instance Adapters - IA

配置数据
----

将策划语言转变为可被程序识别的数据，做到技能、物品可配置。

* 物品 - 技能 - 天赋 - Adapters
  * \[选择器\] - \[Selector\] 定义作用对象，比如某天赋影响所有士兵，而另一技能只影响兽人士兵
    * \[修改器\] - \[Modifier\]
      * 属性
      * 操作符 + （增加x点） +% （增加x%）= （改变为x）
      * 值 x

