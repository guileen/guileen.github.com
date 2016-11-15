---
title: 如何在Keynote中高亮代码
layout: post
published: true
categories: 
tags: [tools, slide]
---

要想在keynote中粘贴高亮的代码，你必须粘贴一个RTF的文本。Mac上有两种办法来复制一个高亮的RTF文本。

## 方法一：highlight

```
brew install highlight 

pbpaste | highlight -O rtf -S js | pbcopy
cat xxx.js | highlight -O rtf -S js | pbcopy
```

如果你了解Automator的话，你可以创建一个service，自动的完成这个过程。如下图，我选中一段文本，然后选择 services，然后选择我自己编写的highlight-rtf service，这段文本就会被高亮了。

![Highlight Service](http://guileen.github.io/upload/highlight-service.png)

如果有人对这个技术很感兴趣（转发量大）的话，我会贴出这个service的详细做法，以及我编写好的脚本。

##方法二：vim plugin CopyRTF

但是有些时候highlight不一定支持你的语言。这时你可以使用vim插件来完成，如果你使用vim编写代码的话，你一定已经支持了相应语言的高亮。

安装Vim 插件 [CopyRTF](https://github.com/zerowidth/vim-copy-as-rtf)。然后你只需要 `:CopyRTF` 即可复制当前文件或选中的文本到剪切板了。

另外推荐一个样式，[PaperColor](https://github.com/NLKNguyen/papercolor-theme)，你可以自定义背景色。

```
let g:PaperColor_Dark_Override = { 'background' : '#000000'}
let g:PaperColor_Light_Override = { 'background' : '#ffffff'}
```
