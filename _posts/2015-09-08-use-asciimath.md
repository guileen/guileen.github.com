---
title:  使用Asciimath来编辑数学公式
layout: post
published: true
categories: 
tags: 
---

[asciimath](http://asciimath.org) 在页面中加入下面这段代码

```html
<script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML"></script>
```

将公式用用\`\`包含起来

```
`sum_(i=1)^n i^3=((n(n+1))/2)^2`
```

\`sum_(i=1)^n i^3=((n(n+1))/2)^2\`


条件概率公式 `P(A|B) = (P(A nn B)) / (P(B))`

<p> `P(A|B) = (P(A nn B)) / (P(B))` </p>

全概率公式

<p> `P(A) = sum_(i) P(A|B_i)*P(B_i)` </p>
