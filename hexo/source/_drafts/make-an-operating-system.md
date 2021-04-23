---
title: 自制操作系统
tags:
---

我深刻的认识到，对操作系统内核的学习还不够深入。『想要知道梨子的滋味，就要亲口尝一尝』，要想搞懂操作系统，就要自己做一个。

参考书主要有3本[《操作系统设计与实现》](https://book.douban.com/subject/2044818/)、[《Orange'S:一个操作系统的实现》](https://book.douban.com/subject/3735649/)、[《30天自制操作系统》](https://book.douban.com/subject/11530329/)、[《一个64位操作系统的设计与实现》](https://book.douban.com/subject/30222325/)。《操作系统设计与实现》这本书是经典，Linus Torvalds就是读了这本书写出了Linux。《30天》代码可以在 [yourtion/30dayMakeOS](https://github.com/yourtion/30dayMakeOS) 找到。这里是[《一个64位操作系统的设计与实现》的代码](https://github.com/yifengyou/The-design-and-implementation-of-a-64-bit-os)

### day 1:

* 2进制编辑器 
  * [ImHex](https://github.com/WerWolv/ImHex) GUI界面，功能强大  
  * [PINCE](https://github.com/korcankaraokcu/PINCE) Linux 反汇编
  * VSCODE hex editor extension
* 汇编语言 NASM
  * brew install nasm
  * nasm boot.asm -o boot.bin
* 安装Bochs虚拟机及bximage
  * brew install bochs
  * bximage <kbd>↵</kbd> 1 <kbd>↵</kbd> fd <kbd>↵</kbd><kbd>↵</kbd> boot.img<kbd>↵</kbd>
  * bximage <kbd>↵</kbd> 5 <kbd>↵</kbd> boot.img
  * dd if=boot.bin of=boot.img bs=512 count=1 conv=notrunc
  * bochs -f bochsrc -q  <kbd>↵</kbd> c <kbd>↵</kbd>

写一个Bootloader，程序启动位置在0x7c00处。这个位置是1981年的IBM PC机5150上，确定下来的。0X7FFF(5150机器总内存空间32KB)-512B(堆栈/数据空间)-512B(MBR空间)=0X7C00。一旦计算机启动起来之后，MBR区、堆栈/数据区就不再需要了，因此我们完全还可以再次回收利用。引导扇区以0x55和0xaa字节作为结束。[[1]](https://zhuanlan.zhihu.com/p/99467926)

```asm
	org	0x7c00	

BaseOfStack	equ	0x7c00

Label_Start:
	mov	ax,	cs
	mov	ds,	ax
	mov	es,	ax
	mov	ss,	ax
	mov	sp,	BaseOfStack
;=======	clear screen
	mov	ax,	0600h
	mov	bx,	0700h
	mov	cx,	0
	mov	dx,	0184fh
	int	10h
;=======	set focus
	mov	ax,	0200h
	mov	bx,	0000h
	mov	dx,	0000h
	int	10h
;=======	display on screen : Start Booting......
	mov	ax,	1301h
	mov	bx,	000fh
	mov	dx,	0000h
	mov	cx,	10
	push	ax
	mov	ax,	ds
	mov	es,	ax
	pop	ax
	mov	bp,	StartBootMessage
	int	10h
;=======	reset floppy
	xor	ah,	ah
	xor	dl,	dl
	int	13h
	jmp	$
StartBootMessage:	db	"Start Boot"
;=======	fill zero until whole sector
	times	510 - ($ - $$)	db	0
	dw	0xaa55
```

> nasm boot.asm -o boot.bin

用hex editor打开boot.bin，可以看到以55AA结尾，并有Start Boot字符。

```
#bochsrc
display_library: sdl2
memory: host=32, guest=32
boot: floppy
floppy_bootsig_check: disabled=0
floppya: type=1_44, 1_44="boot.img", status=inserted, write_protected=0
log: bochs.out
megs: 148
```

> bochs -f bochsrc -q  <kbd>↵</kbd> c <kbd>↵</kbd>

至此，我们就可以看到一个虚拟机启动画面了

<img src="/img/make-os/boot.png" alt="image-20210423220327443" style="zoom:50%;" />