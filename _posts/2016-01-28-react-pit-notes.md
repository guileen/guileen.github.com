---
title: React相关坑记录
layout: post
published: true
categories: 
tags: 
---

1.  Warning: React.createElement: type should not be null, undefined, boolean, or number. It should be a string (for DOM elements) or a ReactClass (for composite components).

Invariant Violation: Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: object.

这个错误可以用最简单的方式重现

```
var Example = null
ReactDOM.render(<Example/>, document.getElementById('container'))
```

2. export default

babel使用了 presets `['es2015', 'react', 'stage-2']` 这个目前（2016.1.28) 不支持

```
export default Example
```

转换为了

```
exports.default = Example
```

以上两个问题结合起来后产生的问题，让我抓狂了数日。
