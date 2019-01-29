---
title: How to enable fenced code block in github pages
layout: post
published: true
categories:
tags: [generator]
---

[Github pages最近升级了jekyll 0.12.0](https://github.com/blog/1366-github-pages-updated-to-jekyll-0-12-0), 这一版本支持fenced code block.

in your \_config.yml

```yaml
markdown: redcarpet
```

    ```ruby
    def foo
      puts 'foo'
    end
    ```

```ruby
def foo
    puts 'foo'
end
```

```
{{ "{%" }} highlight ruby linenos=table %}
def foo
  puts 'foo'
end
{{ "{%" }} endhighlight %}
```
to:

{% raw %}
{% highlight ruby linenos=table %}
def foo
  puts 'foo'
end
{% endhighlight %}
{% endraw %}

如你所见，鄙人想增加行号，但是失败了。

非常遗憾的是，tag pages依然不被支持

