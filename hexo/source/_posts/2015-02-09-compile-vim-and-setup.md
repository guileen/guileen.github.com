---
title: 编译vim
layout: post
published: true
categories: 
tags: 
---

lua, python, ruby, perl 都必须支持

```
git clone git@github.com:vim/vim.git --depth=1
./configure --with-features=huge --with-luajit --enable-rubyinterp=yes --enable-pythoninterp=yes --enable-python3interp=yes --enable-cscope --enable-luainterp=yes --enable-luainterp=yes --with-lua-prefix=/usr/local --enable-perlinterp=yes
make
make install
```

通用插件

```
pathogen
ack
greplace
neocomplete
nerdtree
tagbar
molokai
supertab
command-t
commentary
vim-multiple-cursors
vim-autoclose
```

其他每种语言还有各自的插件
