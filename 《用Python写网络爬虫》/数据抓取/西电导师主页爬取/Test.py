# coding: utf-8

import urllib2
import lxml.html
import re

url = 'http://ste.xidian.edu.cn/html/yanjiushengpeiyang/tongyuandaoshi/'
html = urllib2.urlopen(url).read()
# tree = lxml.html.fromstring(html)
# td = tree.cssselect('.txlist1')
# for tm in td:
#     print tm.text_content()


webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']')

print webpage_regex.findall(html)