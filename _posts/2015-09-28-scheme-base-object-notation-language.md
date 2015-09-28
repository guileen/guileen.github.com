---
title: Scheme base notation language
layout: post
published: true
categories: 
tags: 
---

We use XML, JSON, BSON, MsgPack, Protobuf to transfer structured data. They have issues with effeciant or readability. I always think about that are there any better way to describe structured data clearly and effeciant.

We have primitive types: String, Number, Boolean, Date, Null. And combind types: Array, Object.

In real world, a class of object always have same fields, it's kind of waste.

For example, we have JSON of books

```
{
    books:[
        {"title":"hello world", "pages":100, "author":"Jack", published:1},
        {"title":"hello to programming 1", "pages":50, "author":"Tom", published:1},
        {"title":"hello to programming 2", "pages":50, "author":"Tom", published:1},
        {"title":"hello to programming 3", "pages":50, "author":"Tom", published:0},
    ]
}
```

So, protobuf need you define your scheme, and use you scheme code to compress field names.

In my vison, protobuf is effeciant, but it is not a dynamic describe language, it is an static describe language. Which means, in many times, you need compile your client and server with a shared scheme definition file.

Did you get it? Share scheme definition file, recompile client or server once scheme change, is lack of development effeciant.

So, I design a scheme language like below. It define the scheme first, and use it.

```
!book(title:s,pages:n,author:s,published:b);
{
    books:[
        book('hello world',100,'Jack',1),
        book('how to programming 1',50,'Tom',1),
        book('how to programming 2',50,'Tom',1),
        book('how to programming 3',50,'Tom',0)
    ]
}
```

The first line `!book(...);` define a scheme of book. Syntax is `!name(field:type, ...);`. 
The string after `;` is out data body. `book(...)` use described scheme to create a book object.

For a mobile app, you can seperate it to two part in communication.

The head:

```
!book(title:s,pages:n,author:s,published:b);
```

The body:

```
{
    books:[
        book('hello world',100,'Jack',1),
        book('how to programming 1',50,'Tom',1),
        book('how to programming 2',50,'Tom',1),
        book('how to programming 3',50,'Tom',0)
    ]
}
```

For a mobile app, first you can download scheme head only once, and then you only need receive the body part.
