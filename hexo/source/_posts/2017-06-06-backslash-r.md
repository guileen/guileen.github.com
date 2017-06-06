---
title: backslash r
date: 2017-06-06 17:28:04
tags:
---

一直都知道Windows底下的换行符是 `\r\n`，Linux系统下是`\n`。
但并没有关心过 `\r`和`\n` 到底是什么意思。其实 `\r` 是将光标移至行首，而 `\n` 是将光标移至下一行。这么一看也理解了为什么Windows会将换行符设置为`\r\n`了。

下面这段代码，可以看出`\r`的作用。

```
var i = 0
function update() {
  i++
  process.stdout.write("\r" + i)
  if ((i % 10) == 0) {
    console.log("")
  }
}

setInterval(update, 100)
```
