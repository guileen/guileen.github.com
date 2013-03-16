---
title: Unix signals
layout: post
published: true
categories: 
tags: 
---
转载: http://blog.csdn.net/ljx0305/article/details/2904056

     SIGHUP    终止进程    终端线路挂断
     SIGINT    终止进程    中断进程
     SIGQUIT   建立CORE文件终止进程，并且生成core文件
     SIGILL   建立CORE文件      非法指令
     SIGTRAP  建立CORE文件      跟踪自陷
     SIGBUS   建立CORE文件      总线错误
     SIGSEGV  建立CORE文件      段非法错误
     SIGFPE   建立CORE文件      浮点异常
     SIGIOT   建立CORE文件      执行I/O自陷
     SIGKILL  终止进程    杀死进程
     SIGPIPE  终止进程    向一个没有读进程的管道写数据
     SIGALARM  终止进程    计时器到时
     SIGTERM  终止进程    软件终止信号
     SIGSTOP  停止进程    非终端来的停止信号
     SIGTSTP  停止进程    终端来的停止信号
     SIGCONT  忽略信号    继续执行一个停止的进程
     SIGURG   忽略信号    I/O紧急信号
     SIGIO    忽略信号    描述符上可以进行I/O
     SIGCHLD  忽略信号    当子进程停止或退出时通知父进程
     SIGTTOU  停止进程    后台进程写终端
     SIGTTIN  停止进程    后台进程读终端
     SIGXGPU  终止进程    CPU时限超时
     SIGXFSZ  终止进程    文件长度过长
     SIGWINCH  忽略信号    窗口大小发生变化
     SIGPROF  终止进程    统计分布图用计时器到时
     SIGUSR1  终止进程    用户定义信号1
     SIGUSR2  终止进程    用户定义信号2
     SIGVTALRM 终止进程    虚拟计时器到时

1) SIGHUP 本信号在用户终端连接(正常或非正常)结束时发出, 通常是在终端的控 
制进程结束时, 通知同一session内的各个作业, 这时它们与控制终端 
不再关联. 

2) SIGINT 程序终止(interrupt)信号, 在用户键入INTR字符(通常是Ctrl-C)时发出 

3) SIGQUIT 和SIGINT类似, 但由QUIT字符(通常是Ctrl-)来控制. 进程在因收到 
SIGQUIT退出时会产生core文件, 在这个意义上类似于一个程序错误信 
号. 

4) SIGILL 执行了非法指令. 通常是因为可执行文件本身出现错误, 或者试图执行 
数据段. 堆栈溢出时也有可能产生这个信号. 

5) SIGTRAP 由断点指令或其它trap指令产生. 由debugger使用. 

6) SIGABRT 程序自己发现错误并调用abort时产生. 

6) SIGIOT 在PDP-11上由iot指令产生, 在其它机器上和SIGABRT一样. 

7) SIGBUS 非法地址, 包括内存地址对齐(alignment)出错. eg: 访问一个四个字长 
的整数, 但其地址不是4的倍数. 

8) SIGFPE 在发生致命的算术运算错误时发出. 不仅包括浮点运算错误, 还包括溢 
出及除数为0等其它所有的算术的错误. 

9) SIGKILL 用来立即结束程序的运行. 本信号不能被阻塞, 处理和忽略. 

10) SIGUSR1 留给用户使用 

11) SIGSEGV 试图访问未分配给自己的内存, 或试图往没有写权限的内存地址写数据. 

12) SIGUSR2 留给用户使用 

13) SIGPIPE Broken pipe 

14) SIGALRM 时钟定时信号, 计算的是实际的时间或时钟时间. alarm函数使用该 
信号. 

15) SIGTERM 程序结束(terminate)信号, 与SIGKILL不同的是该信号可以被阻塞和 
处理. 通常用来要求程序自己正常退出. shell命令kill缺省产生这 
个信号. 

17) SIGCHLD 子进程结束时, 父进程会收到这个信号. 

18) SIGCONT 让一个停止(stopped)的进程继续执行. 本信号不能被阻塞. 可以用 
一个handler来让程序在由stopped状态变为继续执行时完成特定的 
工作. 例如, 重新显示提示符 

19) SIGSTOP 停止(stopped)进程的执行. 注意它和terminate以及interrupt的区别: 
该进程还未结束, 只是暂停执行. 本信号不能被阻塞, 处理或忽略. 

20) SIGTSTP 停止进程的运行, 但该信号可以被处理和忽略. 用户键入SUSP字符时 
(通常是Ctrl-Z)发出这个信号 

21) SIGTTIN 当后台作业要从用户终端读数据时, 该作业中的所有进程会收到SIGTTIN 
信号. 缺省时这些进程会停止执行. 

22) SIGTTOU 类似于SIGTTIN, 但在写终端(或修改终端模式)时收到. 

23) SIGURG 有"紧急"数据或out-of-band数据到达socket时产生. 

24) SIGXCPU 超过CPU时间资源限制. 这个限制可以由getrlimit/setrlimit来读取/ 
改变 

25) SIGXFSZ 超过文件大小资源限制. 

26) SIGVTALRM 虚拟时钟信号. 类似于SIGALRM, 但是计算的是该进程占用的CPU时间. 

27) SIGPROF 类似于SIGALRM/SIGVTALRM, 但包括该进程用的CPU时间以及系统调用的 
时间. 

28) SIGWINCH 窗口大小改变时发出. 

29) SIGIO 文件描述符准备就绪, 可以开始进行输入/输出操作. 

30) SIGPWR Power failure 

有两个信号可以停止进程:SIGTERM和SIGKILL。 SIGTERM比较友好，进程能捕捉这个信号，根据您的需要来关闭程序。在关闭程序之前，您可以结束打开的记录文件和完成正在做的任务。在某些情况下，假如进程正在进行作业而且不能中断，那么进程可以忽略这个SIGTERM信号。

对于SIGKILL信号，进程是不能忽略的。这是一个 “我不管您在做什么,立刻停止”的信号。假如您发送SIGKILL信号给进程，Linux就将进程停止在那里。
