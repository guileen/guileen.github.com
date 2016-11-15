---
title: functional programming and sprite system
layout: post
published: true
categories: 
tags: [game, web]
---

How to make a sprite system with functional programming.

function + data.

数据+实现，配置+接口，是一种编程模型。OO在某种形式上，也是一种数据+实现的编程模式，但他将2者耦合在一起。而模板+数据，则是一种更加解耦的模式。

```js
{
    img: img,
    rect:{x,y,w,h}
    screenRect: {x,y,w,h}
    children: [
        {
            rect:{x,y,w,h}
            img: img,
        }
        {
            rect:{x,y,w,h}
            screenRect:{x,y,w,h}
            frame: 0
            frames: [
                {img: img1},
                {img: img2},
            ]
        }
    ]
}
```

render

scale

animation

tween: 
    action:
        move
        rotate
        scale

