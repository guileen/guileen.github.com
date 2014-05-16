---
title: 修复mysql 1449 NO_SUCH_USER 错误
layout: post
published: true
categories: 
tags: mysql
---

权限一律正常。原来是trigger或view需要在分配好权限后，重新生成一遍，改DEFINER=username
