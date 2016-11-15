---
title: MurmurHash 算法
layout: post
published: true
categories: 
tags: [algorithm, hash]
---

发现一个不错的hash算法，可以用于我们的实际工作中，如sharding。

Hash可分为加密hash算法和非加密hash算法，Hash应用于加密、校验、查找、横向扩展等。

加密一般用MD5，SHA-1，校验一般CRC32。而服务器端的负载均衡方面，hash算法需要快速、分布均匀。

MurmurHash是一种非加密hash算法，特点是高运算性能，低碰撞率，分布均匀，由Austin Appleby创建于2008年，现已应用到Hadoop、libstdc++、nginx、libmemcached等开源系统。2011年Appleby被Google雇佣，随后Google推出其变种的CityHash算法。

* [python实现](http://code.google.com/p/pyfasthash/)
* [javascript实现](https://github.com/garycourt/murmurhash-js)
* [java实现](http://docs.guava-libraries.googlecode.com/git/javadoc/com/google/common/hash/Hashing.html)

参考：

* [http://en.wikipedia.org/wiki/List_of_hash_functions]
* [http://en.wikipedia.org/wiki/MurmurHash]
* [http://code.google.com/p/cityhash/source/browse/trunk/src/city.cc]
