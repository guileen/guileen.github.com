---
title: Promise模式在防止缓存雪崩中的应用
date: 2019-11-01 00:00:00
tags:
---
对大多数高并发架构而言，缓存是不可或缺的。在数据持久化层，其核心是保证数据一致性，而吞吐能力往往较弱。而在缓存层，因其逻辑简单，则具备较高的吞吐能力，但为了保证数据的时效性，则必须设置缓存的过期时间。在缓存过期后，程序会从持久化层读取数据，填充缓存。我们通常称这种缓存加载方式为懒加载（lazy load）。

在缓存失效的瞬间，如果突然爆发大量缓存请求，则会导致所有请求穿透至持久化层，给持久化层带来巨大压力，这种现象叫做缓存雪崩。

![缓存雪崩](http://upload-images.jianshu.io/upload_images/31319-843693e8c36814b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 解决缓存雪崩的几种方案

1. 在预加载时设置锁状态。后至的缓存请求，将获得锁状态，在一段时间后重试加载缓存。但这一方法不能保证第一时间返回数据。

![穿透锁](http://upload-images.jianshu.io/upload_images/31319-5138b17e9260eacb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
def lazyload(key):
    value = cache.get(key)
    if(!value):
        cache.set(key, '__lock__')
        value = db.get(key)
        cache.set(key, value)
    if(value == '__lock__'):
        sleep(100)
        return lazyload(key)
    return value
```

2. 这里重点介绍的Promise解决缓存穿透的思路，这种方法将使同一进程内对同一缓存的访问进行汇总，不仅减少对持久层的缓存穿透，而且也可以降低对缓存层的请求量。拥有极强的汇聚效果。

![Promise解决缓存雪崩](http://upload-images.jianshu.io/upload_images/31319-1443709321ad539e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
def _lazyload(key):
    value = cache.get(key)
    if(!value):
        value = db.get(key)
        cache.set(key, value)

promiseMap = {}
def lazyload(key):
    def clearPromiseMap:
        delete promiseMap[key]
    promise = promiseMap[key]
    if(!promise):
        promise = Promise(_lazyload, key)
        promise.then(clearPromiseMap)
        promiseMap[key] = promise
    return promise.resolve()
```

本文所有代码为伪代码！
