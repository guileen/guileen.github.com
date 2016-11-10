---
title: For each files in the Makefile
layout: post
published: true
categories: 
tags: make, build
---

在构建项目时，时常需要遍历某个文件夹下的文件，按特定的方式将其预处理，变为一个新文件。

我们可以为此写一个脚本，负责遍历文件夹，处理文件内容，输出文件内容。

可以看到stackoverflow上的这个[问题](http://stackoverflow.com/questions/2706064/compile-all-c-files-in-a-directory-into-separate-programs)很好的解释了这个问题的应用场景。

希望将某个目录下的每个c文件编译成一一对应的执行文件，x.c 编译成 x， y.c 编译成 y。

    SRCS = $(wildcard *.c)
    PROGS = $(patsubst %.c,%,$(SRCS))

    all: $(PROGS)

    %: %.c
            $(CC) $(CFLAGS)  -o $@ $<


如果没明白发生了什么，通过下面的例子大家应该可以明白。

Makefile:

    SRCS = $(wildcard a.txt)
    DESTS = $(patsubst %.txt, %.json, $(SRCS))

    all: $(DESTS)

    %: *.txt
        @echo $@
        @echo $<

在命令行下执行

    touch a.txt b.txt c.txt
    make

将会输出

    a.txt
    a.json
    b.txt
    b.json
    c.txt
    c.json


再举一个实际应用场景的例子，希望把某个目录下的 .csv 文件编译成 .json, 这一方法不仅能简化csv to json 脚本，还可以实现类似，仅当csv文件比json文件更新的情况下才需要编译。
