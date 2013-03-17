---
title: How to enable fenced code block in github pages
layout: post
published: true
categories: 
tags: github
---

Github pages最近[升级][1]了jekyll 0.12.0, 这一版本支持fenced code block.

in your \_config.yml

```yaml
markdown: redcarpet
```

{% highlight ruby linenos=table %}
def foo
  puts 'foo'
end
{% endhighlight %}

非常遗憾的是，tag pages依然不被支持

[1] https://github.com/blog/1366-github-pages-updated-to-jekyll-0-12-0

