---
title: Simple node mongodb driver design principle
layout: post
published: false
categories: 
tags: [node.js, mongodb]
---

    A db driver is used to maintain connections to db server, translate command and response from protocol, export usable API to make high level service. 
    For the API, driver takes connection config, and returns a client instance, we can execute db command from the client instance directly, that is clearly.

    When we design a node db driver, we must careful when we return the client instance. Because of the node asynchronous design pattern, someone maybe 
    allback a client instance but not return a client instance. When we callback the client instance, it is hard to inject client instance into the application context.

    [Node-redis] is a good example that just give port and host and return a RedisClient instance, and the client instance can execute any redis command.

    But the node-mongodb-native driver is not design like this, when we give a host port and database, it does not return an db instance, but callback an db instance.
    And more worth, we can't execute most command from the db instance, the most command is on the collection instance, but we have to retrival collection instance from db with callback.

    So I develop mongoskin, to wrap the node-mongodb-native driver, and make it works like a driver what I described above. But mongoskin is not a really driver, it is built upon node-mongodb-native.

    But why not develop a new driver instead of node-mongodb-native driver? But I personally have not enough time to maintain a db driver, I hope I can get a start, the community can contribute the other part of the driver.

    It is not very hard to develop a mongodb driver, the BSON is stable library.

    * Should get `db` `collection` as synchronized style.
    * Easy contribute, every command should be maintain and test standalone.
