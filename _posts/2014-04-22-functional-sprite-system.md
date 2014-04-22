---
title: functional programming and sprite system
layout: post
published: true
categories: 
tags: game,html5,
---

How to make a sprite system with functional programming.

function + data.

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

