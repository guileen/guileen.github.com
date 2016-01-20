---
title: 如何在Keynote中高亮代码
layout: post
published: true
categories: 
tags: 
---

要想在keynote中粘贴高亮的代码，你必须粘贴一个RTF的文本。Mac上有两种办法来复制一个高亮的RTF文本。

## 方法一：highlight

```
brew install highlight 

pbpaste | highlight -O rtf -S js | pbcopy
cat xxx.js | highlight -O rtf -S js | pbcopy
```

##方法二：vim plugin CopyRTF

但是有些时候highlight不一定支持你的语言。这时你可以使用vim插件来完成，如果你使用vim编写代码的话，你一定已经支持了相应语言的高亮。

安装Vim 插件 [CopyRTF](https://github.com/zerowidth/vim-copy-as-rtf)。然后你只需要 `:CopyRTF` 即可复制当前文件或选中的文本到剪切板了。

另外推荐一个样式，[PaperColor](https://github.com/NLKNguyen/papercolor-theme)，你可以自定义背景色。

```
let g:PaperColor_Dark_Override = { 'background' : '#000000'}
let g:PaperColor_Light_Override = { 'background' : '#ffffff'}
```
