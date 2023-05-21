---
title: Python数据分析笔记
s: python-data-analysis-note
date: 2016-12-15 21:51:36
tags: [python, data, machine-learning]
---

# [可选]
install python

```
pip install -U pip

pip install <something>
pip uninstall <something>
```

pip support virtualenv

# [Anaconda]

[Install anaconda](https://www.continuum.io/downloads)

国内可从清华镜像下载，并设置镜像

[清华镜像源](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)

MacOS:

```
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda2-x.x.x-MacOSX-x86_64.sh`
bash Anaconda2-x.x.x-MacOS-x86_64.sh
```

会安装到~/anaconda2下，默认会将PATH设置在 bash_profile中，根据你自己的shell设置，加入
```
export PATH="/home/xx/anaconda2/bin:$PATH"
```

重新打开你的shell，执行`conda`命令测试。

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

Python环境管理:

```
conda create --name py27 python=2.7
activate py27
```

包管理:

```
conda list
conda install numpy
```

(conda install 会安装或更新依赖库，pip install则不会)

# [安装工具包]

conda install numpy scipy pandas matplotlib

# [IDE]

spyder, pycharm, sublime text, vim

# [Jupyter]
`ipython` 一个更好的python交互命令

`jupyter notebook` Web记事本，可以将交互过程记录并分享。

后续使用 jupyter 记录。
