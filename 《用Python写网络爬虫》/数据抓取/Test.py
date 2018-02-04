#coding:utf-8
import urllib2
import re
import lxml.html

def download(url, scrape_callback=None):
    # url = 'http://example.webscraping.com/places/default/view/American-Samoa-5'
    html = urllib2.urlopen(url).read()
    print 'url:', url
    # print 'html:', html

    if scrape_callback:
        scrape_callback(url, html)


import csv

# 构造一个 ScrapCallback类，来实现抓取行为。
class ScrapCallback:
    def __init__(self):
        # 'w'是写  'r'是读  reader = csv.reader(open(".csv", 'r'))
        self.writer =csv.writer(open('country_test.csv', 'w'))
        self.fields = ('area','population','country')
        self.writer.writerow(self.fields)

    # 构造 __call__方法。 call是一个特殊的方法，在对象作为函数被调用时会调用该方法。
    def __call__(self, url, html):
        # re.sarch() 函数将对整个字符串进行搜索，并返回第一个匹配的字符串的match对象。
        if re.search('/view/',url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())

            self.writer.writerow(row)



if __name__ == '__main__':
    download('http://example.webscraping.com/places/default/view/American-Samoa-5', scrape_callback=ScrapCallback())