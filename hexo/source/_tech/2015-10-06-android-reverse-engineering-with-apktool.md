---
title: Android反向工程
layout: post
published: true
categories:
tags: android
---

https://ibotpeaches.github.io/Apktool/

# 安装

## Linux:
1. Download Linux wrapper script (Right click, Save Link As apktool)
2. Download apktool-2 (find newest here)
3. Make sure you have the 32bit libraries (ia32-libs) downloaded and installed by your linux package manager, if you are on a 64bit unix system.
4. (This helps provide support for the 32bit native binary aapt, which is required by apktool)
5. Rename downloaded jar to apktool.jar
6. Move both files (apktool.jar & apktool) to /usr/local/bin (root needed)
7. Make sure both files are executable (chmod +x)
8. Try running apktool via cli

## Mac OS X:
1. Download Mac wrapper script (Right click, Save Link As apktool)
2. Download apktool-2 (find newest here)
3. Rename downloaded jar to apktool.jar
4. Move both files (apktool.jar & apktool) to /usr/local/bin (root needed)
5. Make sure both files are executable (chmod +x)
6. Try running apktool via cli

# 使用

apktool d test.apk

apktool b test


# 使用 dex2jar
unzip test.apk

wget https://github.com/pxb1988/dex2jar/releases/download/2.0/dex-tools-2.0.zip

# JD-GUI
可以搜索

# jad
../../jad -o -r -sjava -ddest tmp/**/*.class
