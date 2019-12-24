#!/bin/sh
git push origin hexo && hexo generate && hexo deploy

# ssh ubuntu@leen.ipub.io -t 'cd /var/www/; chmod 755 -R ./leengui.com'
