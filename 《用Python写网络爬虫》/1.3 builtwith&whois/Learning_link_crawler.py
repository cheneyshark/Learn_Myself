#coding:utf-8
#  正则能包
import re
# 相对链接转换为绝对链接模块    urlparse.urljoin
import urlparse
# 处理URL
import urllib2
import time
from datetime import datetime
# 解析robots.txt
import robotparser
# 提供队列操作的模块
import Queue


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1):
    """从给定的种子URL中抓去匹配正则能的链接
    """
    # 仍然需要爬取的URL队列
    # deque 双端队列，元素可以从两端弹出，其限定插入和删除操作在表的两端进行
    crawl_queue = Queue.deque([seed_url])
    # 构造一个字典序记录看过的URL和访问深度之间对应
    seen = {seed_url: 0}
    # 记录总共下载过的页面数量
    num_urls = 0

    # 解析 URL 的robots.txt文件
    rp = get_robots(seed_url)

    # 用Throttle(self,delay)构造期构造一个对象实例
    throttle = Throttle(delay)
    # 如果headers为True， 则返回headers的值，否则返回 {} 一个空的字典序
    headers = headers or {}
    # 用户代理赋值
    if user_agent:
        headers['User-agent'] = user_agent

    # 判断爬取的URL队列是否为空
    while crawl_queue:
        # pop方法从列表返回最后一个对象，并从列表中移除
        url = crawl_queue.pop()
        # 检查URL中的rebots.txt限制
        # can_fetch 函数为，用user_agent作为用户代理访问该URL，允许返回True，否则返回False
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                # 可以继续深入爬取
                if link_regex:
                    # 过滤是否匹配正则能表达式的链接   如本例中：/(index|view)   及匹配带有index获view的链接
                    # 对html中的所有链接进行遍历，看是否匹配正则能表达时 link_regex
                    # 把后面筛选出的list扩展到links 这个list的尾部  extend函数：使用一个序列扩展另一个list，参数是序列。
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    # 将link与seed_url形成绝对路径，重新赋值给link。
                    link = normalize(seed_url, link)
                    # 检查是否已经爬取过这个链接
                    if link not in seen:
                        seen[link] = depth + 1
                        # 对比是否与seed_url 域名相同   及URL和端口号字段
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url


class Throttle:
    """下载限速
        Throttle 类记录了每个域名上次访问的时间，如果当前时间距离上次访问时间小于指定演示，则执行睡眠操作。
        在每次下载之前调用Throttle对爬虫进行限速。
    """
    # __init__对象初始化函数，类似于Java中的构造器，可以有多种参数方式的重载
    def __init__(self, delay):
        # 每个域名多次下载之间的延迟时间
        self.delay = delay
        # 每个域名上次下载的时间戳
        self.domains = {}

    def wait(self, url):
        # urlparse模块的urlparse函数主要是把 url 拆分成6个部分，
        #   并返回元组(scheme——协议,netloc——域名和端口号,path——URI,parameters,query,fragment）。
        domain = urlparse.urlparse(url).netloc

        # 从字典序提取domain的对应时间戳。
        # 之所以用get函数不直接用 domains[domain],是因为如果直接调用时，字典序没有domain这个链接，则会报错，而get函数不会报错。
        last_accessed = self.domains.get(domain)


        if self.delay > 0 and last_accessed is not None:
            # datetime.now()  输出但前时间  时间格式为：2018-01-24 21:48:12.616524
            # 与上次的记录时间戳求差值后，在用.seconds 转化为秒
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # time.sleep(s)  程序休眠s秒
                time.sleep(sleep_secs)
        # 更新时间戳
        self.domains[domain] = datetime.now()



def download(url, headers, proxy, num_retries, data=None):
    """下载页面函数
    """
    print 'Downloading:', url
    # Request类是一个抽象的URL请求。
    # 参数说明： URL，data（请求包中的额外数据，缺省为None，及GET，如果有data参数，则请求为POST）、
    #          headers——字典类型
    request = urllib2.Request(url, data, headers)

    # urllib2.urlopen()函数不支持验证、cookies或者其他HTTP高级功能。
    # 要支持这些功能，必须使用build_opener（）函数创建自定义Opener对象。
    # build_opener()返回的对象具有open()方法，与urlopen（）函数的功能相同。
    opener = urllib2.build_opener()

    # 支持代理功能
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        # urllib2.urlopen(url)可以获取应答信息。
        # urlopen返回一个类文件对象，提供了如下方法：read(),readline(),readlines(),fileno(),close()
        response = opener.open(request)
        html = response.read()
        code = response.code  # code 返回的状态吗
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        # hasattr 判断一个对象 e 里面是否有 code 属性或者方法，有返回True，没有返回False
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html


def normalize(seed_url, link):
    """将link部分去掉fragment字段后，与seed_url形成绝对路径。返回一个新的URL。
    """
    # urldefrag(url) 将URL分解成去掉fragment的新URL和去掉的fragment的二元组
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    # 将处理后的link与 原URL形成绝对路径，并返回
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """解析robots.txt文件
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """返回html中链接的列表
    """
    # 匹配所有类似  <a...href="..." 格式的链接
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # 列出webpage中的所有链接，并返回此列表
    return webpage_regex.findall(html)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1, user_agent='GoodCrawler')
