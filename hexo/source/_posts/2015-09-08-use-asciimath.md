---
title:  使用Asciimath来编辑数学公式
layout: post
published: true
categories:
tags: [mathematics]
---

## MathJax

```
When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
```

When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

## AsciiMath

```
`a * b = c   => a = c / b => b = c / a`
```

\` a * b = c   => a = c / b => b = c / a\`

\` a / b = c  => a = b * c\`

\` 1 / 2 = 0.5 =>  1/0.5 = 2 \`

\` 12 / 3 = 4 => 12 / 4 = 3 \`

\` 18 / 3 = 6 => 18 / 6 = 3 \`

\` 面积 = 长度 *  宽度 \`

\` 长度 = (面积) / (宽度) \`





[asciimath](http://asciimath.org) 在页面中加入下面这段代码

```html
<script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML"></script>
```

将公式用用\`包含起来

```
`sum_(i=1)^n i^3=((n(n+1))/2)^2`
```

\`sum_(i=1)^n i^3=((n(n+1))/2)^2\`


条件概率公式 `P(A|B) = (P(A nn B)) / (P(B))`

<p> `P(A|B) = (P(A nn B)) / (P(B))` </p>

全概率公式 `P(A) = sum_(i) P(A|B_i)*P(B_i)`

<p> `P(A) = sum_(i) P(A|B_i)*P(B_i)` </p>

微积分:

\`f(x)=x^2\`

\`d/dx(x^3)=((x+dx)^2 - x^2)/dx = (x^2 + 2xdx+dx^2 - x^2)/dx = 2x +dx = 2x\`

\`u'+v' = (du)/dx + (dv)/dx = (du+dv)/dx = (d(u+v)) / dx = (u+v)'\`

\`(cu)' = (dcu)/dx = c(du)/dx = cu'\`
