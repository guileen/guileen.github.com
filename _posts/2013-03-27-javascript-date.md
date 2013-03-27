---
title: javascript 日期处理
layout: post
published: true
categories: 
tags: 
---

计算两日期间的天数之差


```js
function treatAsUTC(date) {
    var result = new Date(date);
    result.setMinutes(result.getMinutes() - result.getTimezoneOffset());
    return result;
}

var millisecondsPerDay = 24 * 60 * 60 * 1000;
function daysBetween(startDate, endDate) {
    return (treatAsUTC(endDate) - treatAsUTC(startDate)) / millisecondsPerDay;
}
```