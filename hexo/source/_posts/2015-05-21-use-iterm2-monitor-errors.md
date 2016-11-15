---
title: 使用iterm监控错误
layout: post
published: true
categories: 
tags: [tools, terminal]
---

Install terminal-notifier

`brew install terminal-notifier`

`Cmd+,` -> Prefrences -> Advanced -> Triggers

Add new trigger

Regular Expression: `.*ERRO.*`
Action: `Run Command`
Parameters: `/usr/local/bin/terminal-notifier -message "\0" -title Error`
