# coding:utf-8

import lxml.html
broken_html = '<ul class = contry><li>Area<li>Population</ul/'
tree = lxml.html.fromstring(broken_html)
fixed_html = lxml.html.tostring(tree,pretty_print=True)
print fixed_html