---
title: 遷移svn代碼到git
layout: post
published: false
categories:
tags: [git, svn]
---

很多時候我們需要將svn代碼遷移到git。比如從[visualsvn](http://www.visualsvn.com/server/)遷移到[gitlab](http://gitlab.org)，
在此過程中你通常需要刪除一些垃圾文件，修改你的committer名字。

克隆svn代碼：

```
git svn clone svn_url
```

刪除不需要的文件

```
git filter-branch --tree-filter 'rm -rf node_modules'
```

刪除空的提交

```
git filter-branch --commit-filter 'git_commit_non_empty_tree "$@"' HEAD
```

gc

```
git gc
```

如果你需要修改你的commiter或author名字

```bash
#!/bin/sh

git filter-branch --env-filter '

an="$GIT_AUTHOR_NAME"
am="$GIT_AUTHOR_EMAIL"
cn="$GIT_COMMITTER_NAME"
cm="$GIT_COMMITTER_EMAIL"

if [ "$GIT_COMMITTER_EMAIL" = "your@email.to.match" ]
then
    cn="Your New Committer Name"
    cm="Your New Committer Email"
fi
if [ "$GIT_AUTHOR_EMAIL" = "your@email.to.match" ]
then
    an="Your New Author Name"
    am="Your New Author Email"
fi

export GIT_AUTHOR_NAME="$an"
export GIT_AUTHOR_EMAIL="$am"
export GIT_COMMITTER_NAME="$cn"
export GIT_COMMITTER_EMAIL="$cm"
'
```

添加git remote庫並push

```
git remote add origin git_url
git push -u origin master
```

重新克隆一個乾淨的git庫

```
git clone git_url
```

完成。

