---
title: 数据抽象层设计
layout: post
published: true
categories: 
tags: 
---

数据层的封装

Data Layer must be split by `User Space`, each `User Space` should be monitored.
Space is vertical split to `Data Type`. Each `Data Type` has it's own `Operations`.
Most `Operation` take `Id` as parameter or no parameter.
Some `Operation` take effect to `Rows` match some condition.

## DataTypes

* Object
* File
* User
* Message
* MQ
* Third-Service

## Object

### Goals

* Auto caching and persistent.
* Fast and advance query.
* Schemeless.
* Full-text search.
* Geo-Search.
* Safe lock-column?
* Programable configuration.
* Lazy ensure index.
* Multi IDC distributed.

Get/Set
Redis zset
Ardb
Mongodb
Hadoop MapReduce
Object {...}

## SQL Abstract Layer
Redis As SQL

## MapReduce Abstract Layer
Redis Lua As MapReduce

## Redis Abstract Layer
Massive Redis Storage and Cache

## Mongodb As Storage Layer
It's OK, mongodb it self is an Abstract Layer.
