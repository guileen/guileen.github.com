---
title: Go语言的GC优化技巧
layout: post
published: true
categories: 
tags: [go]
---

GC只要不出问题，就不会有人关心GC的问题，但如果GC出了问题，想要优化它却不是一件容易的事情。我最近就遇到了Golang GC问题，经过一系列的尝试终于将应用性能优化了300%的。你一定会觉得性能优化300%，那之前的代码得写的多烂啊。坦白的说，之前的代码虽然未做优化，但并没有大的问题。

我们的IM服务器，使用golang开发，自定义的协议，运行在一台4核8G的云主机上，同时在线大约一万多人。一直以来，运行的还不错，但近期我们发现当在线人数达到2万人的时候，CPU占用就会达到100%，它就彻底的失去了响应。我的内心是奔溃的，因为根据我们曾经做过的压力测试推测，这点连接数完全不应该有问题的。

## 定位CPU问题

Golang定位CPU问题还是比较方便的，因为golang提供了非常便捷的profile工具。官方的文档看[这里](https://golang.org/pkg/net/http/pprof/)

首先需要在程序内部启动一个http服务，并引入`net/http/pprof`模块，就会自动增加 `/debug/pprof/*` 相关的Handler。其中 `/debug/pprof/profile`为CPU profile，`/debug/pprof/heap`为heap信息， 也是我们主要关注的两个信息。

```
import _ "net/http/pprof"
import "net/http"

go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

添加好上述代码，并部署执行后，即可使用如下`go tool pprof`命令进行监测

> go tool pprof http://localhost:6060/debug/pprof/profile

默认会搜集30s的profile，这里会等待30s。然后就可以查看profile的结果了。

> \> png > profile.png

我们发现最耗时的几个点 `runtime.scanobject`, `runtime.pcvalue`, `runtime.memclr`

> runtime.scanobject 7.82s(18.16%) of 10.64s(24.74%)<br>
> runtime.pcvalue 4.43s(10.29%) of 9.50s(22.07%)<br>
> runtime.memclr 3.18s(7.39%)<br>

而它们大部分都来自于 `runtime.gcDrain`
> runtime.gcDrain 0.02s of 23.66s(54.96%)

而这些都是和GC相关的操作，至此，我们可以得出一个初步结论，GC占用了大部分的CPU。


## 第一次实验

既然是GC问题，那么我们看一下heap吧
> go tool pprof http://localhost:6060/debug/pprof/heap
> \> png > heap.png

通过Heap我们可以发现内存占用最大的是Connection，每一个IM用户的连接都会有一个独立的Connection，而这个Connection上还会保存一些用户ID、昵称等基本信息。同时我们要把每个Connection放入一个map中，让我们称他cmap，cmap的key是用户ID，这样我们才能定位用户对应的Connection。

我们并不能确定问题在cmap上，或者是Connection结构上。但是我们完全没有其他的线索，既然它的heap占用最大，就先拿它开刀吧。

为了验证我们的假设，我们在测试环境中，不断的创建连接，关闭连接，同时运行profile。profile的结果显示，GC完全没问题，甚至GC都没出现在profile中。

其实这时测试实验已经可以基本确定GC问题和Connection和cmap无关了。但是我们依然希望对Connection的创建与销毁进行一个优化，然后再来对比GC是否有改善。

## 对象池模式

我们决定使用[对象池模式](https://zh.wikipedia.org/wiki/%E5%AF%B9%E8%B1%A1%E6%B1%A0%E6%A8%A1%E5%BC%8F)来优化Connection的创建销毁。所谓对象池模式，就是在对象创建时我们通过对象池进行获取而不是分配内存创建新对象，当我们要释放一个对象时也不是直接丢给GC而是放入对象池。

Golang已经提供了一个`sync.Pool`实现。｀sync.Pool`是线程安全的，你可以在多个goroutine中安全的使用它。`Pool`可能在任何时候回收`Pool`中的对象，所以你不用关心`Pool`的GC问题。

优化的调整也很简单：

优化前代码：

```
func NewConnection(conn net.Conn) *Connection{
    c := &Connection{conn: conn}
    // init stuffs...
}

func (c *Connection) Close() error{
    c.conn.Close()
}
```

优化后代码

```
// 对象池：全局对象池
var cPool = sync.Pool{
    // 当对象池中无对象时，如何创建新对象
    New:func() interface{}{return new(Connection)}
}

func NewConnection(conn net.Conn) *Connection{
    c := cPool.Get()  // 从对象池中获取
    c.conn = conn  //初始化
    // init stuffs...
}

func (c *Connection) Close() error{
    c.conn.Close()
    c.conn = nil  // Relaese
    // release stuffs ...
    cPool.Put(c) // 放回对象池
}
```

测试了没问题就发布了。事实再次证明，GC和Connection、connection map完全没有关系，GC的问题在生产环境上依然如常。而且还产生了一些bug，因为原本的释放由GC完成，所以不需要做临时属性的reset工作，但使用了对象池后，这些未释放的临时属性会一直存在，当你以为你是用的是一个`NewConnection`的时候，其他它并不是一个新的对象。

我的结论是，在与业务逻辑相关的地方，尽量不要使用对象池，以免引出新的bug。对象池应该用在那些边界明确、高内聚的模块上。

## slice, append 的妙用

GC更多还是与内存的分配与释放频次有关，我们把目光从内存占用量最大的模块上移开，关注了一下其他琐碎的小对象。通过profile与heap的对比往往能比较好的发现问题，profile与频率相关，heap与占用相关，如果两样都占了，那么就是很可疑的。

通过对比，我决定优化一下日志模块，这是自己写的一个小的日志模块，为了能更方便记录每个Connection上的基本信息、时间、行号等，但写的比较直接，基本靠 `Time.Format` `fmt.Sprintf` 完成了每行日志文本的拼接，这两个函数比较易用，但是性能并不是最佳。我参照了原生的`log`模块，对自己的日期格式化和日志文本的拼接进行了优化，值得一提的是一个原生`log`代码中对`append`的妙用。

优化前代码示意：

```
type Logger struct {
}

func (l *Logger) Log(str string) {
    ...
    fmt.Fprintln(writer, fmt.Sprintf("%s %s:%d %s %s",
        "[INFO]",filename, line, str
    ))
}
```

优化后代码示意：

```
type Logger struct {
    buf []byte
}

func (l *Logger) formatHeader(buf *[]byte) {
    ...
    *buf = append(*buf, "[INFO]"...)
    *buf = append(*buf, filename...)
    *buf = append(*buf, ':')
    *buf = append(*buf, itoa(line)...)
}

func (l *Logger) Log(str string) {
    l.buf = l.buf[:0]   // Reset slice
    l.formatHeader(&l.buf)
    l.buf = append(l.buf, str...)
    l.writer.Write(*buf)
}
```

以上的示例代码中，大家可以仔细体会一下。`Logger`对象有一个`buf`，`l.buf:=l.buf[:0]`这句本质上只是把`buf`这个slice的length修改了，但是capacity并没有改变，所以不会发生内存的分配。而`*buf=append(*buf, xxx)` 只有在length > capacity 时才会导致内存重新分配。而length > capacity 是很少发生的，也就意味着很少发生buf内存的分配，这也就是优化了GC。

受此启发，我们每次读取网络数据包的位置，也做了类似的优化，但这里无法使用append，只能直接make。

优化前的代码类似这样：

```
func (c *Connection) ReadBuffer(length) []byte{
    buff := make([]byte, length)
    io.ReadFull(c.reader, buff)
    return buff
}
```

我在Connection中增加了一个可重用的buf缓冲区，优化后的代码类似这样：

```
func (c *Connection) ReadBuffer(length int) []byte{
    if length > len(c.buf) {
        c.buf = make([]byte, length)
    }
    buff := c.buf[:length]
    io.ReadFull(reader, buff)
    return buff
}
```

这可以大大减少读数据时的内存分配。

这里我们可以总结出一条GC优化原则：
＊ 成员变量代替临时变量，减少内存分配。

注意：文中代码仅为示例，未考虑线程安全因素，实际使用中需要对成员变量的访问加锁。

## return还是传址

成员变量可以解决方法内部的GC问题，但是当需要与外部交互时，我们还需要其他的技巧。比如这个函数：

```
func (c *Connection) ReadPacket() *Packet {
    buff := c.ReadBuffer()
    packet := new(Packet)
    packet.Init(buff)
    return packet
}
```

这里我们不可避免的创建了一个`Packet`对象。而如果我们将函数进行如下改造，则可以为其他的代码创造出优化的空间。

```
func (c *Connection) ReadPacket() *Packet {
    packet := new(Packet)
    c.Read(packet)
    return packet
}

func (c *Connection) Read(packet *Packet) {
    buff := c.ReadBuffer()
    packet.Init(buff)
}
```

我们保留了`ReadPacket`方法以保持向下兼容，同时增加了一个新方法`Read`，它没有return，但是需要你传入一个Packet指针，这使它的消费者有条件重用这个Packet。

原消费者代码：

```
for {
    packet := connection.ReadPacket()
    handle(packet)
}
```

这里每次会创建一个新的packet。

优化后的消费者代码：

```
packet = new(Packet)
for {
    connection.Read(packet)
    handle(packet)
}
```

这里始终重用一个packet。

## 类型转换，[]byte to string

在网络应用中，不可避免的要使用[]byte，并且需要将[]byte转换为最终要使用的数据，因此我们经常需要做 []byte到string的转换。但是我们发现`string(bytes)` 这一转换将引起一次内存copy，这使得转换会产生一些重复数据。有一些黑科技可以让它不复制内存，但是这样获得的string没有imutable特性，会导致不可预料的后果以及一些内部优化也将失效。

```
func unsafeToString(bytes []byte) *string {
    hdr := &reflect.StringHeader{
        Data: uintptr(unsafe.Pointer(&bytes[0])),
        Len:  len(bytes),
    }
    return (*string)(unsafe.Pointer(hdr))
}
```

我尚不能确定是否有其他类型的相互转换也会有同样的问题。

## GOGC

使用GOGC环境变量或者[SetGCPercent](https://golang.org/pkg/runtime/debug/#SetGCPercent)，可以用来调整GC的触发频率，默认 GOGC=100，我们将这个数值调到了GOGC=200。对于这个参数，我还没有深入的研究，不过实验证明调高这个数值可以减少GC的CPU占用。

## GC日志

有时在做一些实验的时候我们可以通过观察GC日志来发现检验效果。你需要使用GODEBUG=gctrace=1 作为程序启动的环境变量，即可看到GC相关信息。

> GODEBUG=gctrace=1 yourprogram

## 禁术

Well，做了这么多，我们的CPU占用情况和GC情况到底改善了多少呢？18000连接左右时，CPU从80%占用降低到了50%占用。GC占比依然很高，仅从54%下降到了50%。这说明，我们并没有找到影响GC真正的原因。我必须寻找下一个优化点，否则一切好无头绪。于是我再次对比CPU profile和Heap dump的图，我想也许是业务逻辑处理模块的问题，但我还不能确定是哪个业务模块的问题，那就赌那个CPU占用最高的业务模块吧。

但已经花费了太多的时间优化GC，我不想再浪费时间不断的猜测，于是我只能使出我从不轻易使用的禁术（请勿模仿，使用不当可能会对你的职业生涯造成严重的伤害）————直接禁用了那个功能，并以最快的时间跑出了profile，然后立刻恢复了这个功能。

这次猜中了，当禁用了这个功能后，GC情况大大改善。这下心里有底了，顺藤摸瓜就发现了这么一段代码：

```
func Compress(p []byte) ([]byte, error) {
    buf := new(bytes.Buffer)
    zipWriter := zlib.NewWriter(buf)
    if _, err := zipWriter.Write(p); err != nil {
        return nil, err
    }
    if err := zipWriter.Close(); err != nil {
        return nil, err
    }
    return buf.Bytes(), nil
}
```

这就是照着golang[官方zlib Example](https://golang.org/pkg/compress/zlib/#pkg-overview)写的。看来Golang的zlib封装有很大的问题，导致了这个对象很重。

既然已经找到了问题的原因，就很好办了。解决的方法就是最开始提到的`对象池模式`。这次并没有使用`sync.Pool`，而是自己实现了一个简单的对象池。完整代码就不贴了

```
func (w *zlibWorker) compress(p []byte) ([]byte, error) {
    buf := new(bytes.Buffer)
    zipWriter := w.zipWriter  // 重用zipWriter
    zipWriter.Reset(buf)  // <- 主要在这里
    if _, err := zipWriter.Write(p); err != nil {
        return nil, err
    }
    if err := zipWriter.Close(); err != nil {
        return nil, err
    }
    return buf.Bytes(), nil
}
```

优化后的同时段的CPU占用率从50%下降到了20%，GC占用量可以忽略。而CPU占用最高的三个函数分别是 `runtime.memmove` 和 `compress/flate.(*compressor).reset` 还有 `syscall.Syscall`，前两个都源自`zlib.Writer.Reset`，看来还有进一步的优化空间，比如用CGO，不过这已经超出了本文的讨论范围。`syscall.Syscall`是网络应用不可避免的的部分，无法优化。可以将`syscall.Syscall`视为性能优化的参照标准，这一函数的CPU占比越大，通常程序是越健康的。

## 总结

这些技巧在其他有自动垃圾回收机制的语言中也同样适用

* Profile与Heap对照，往往能更有效的定位问题
* 通过实验来验证猜测
* 使用成员变量代替临时变量
* 使用传址代替返回
* 对比较重的对象应用`对象池模式`
* 利用语言特性进行优化
* 调整GC相关参数进行优化
