---
title: vim现代js设置
layout: post
published: true
categories: 
tags: [vim, editor]
---

Install vim plugin: yajs editorconfig-vim

```
let g:jsx_ext_required = 0 " Allow JSX in normal JS files
let g:syntastic_javascript_checkers = ['eslint']
```

安装相关工具

```
npm install -g eslint babel-eslint eslint-plugin-react
```

代码检查开关：

```
/* eslint-disable no-console */

//suppress all warnings between comments
console.log('foo');

/* eslint-enable */
```

