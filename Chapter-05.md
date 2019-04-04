# 第五天 爬虫实战

## 并发抓取
将作业(抓取豆瓣电影 一周口碑榜，电影简介),改成并发模式，同时抓取多个网页

```
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_orders(url):
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    h = bs.select('#billboard > div.billboard-hd > h2')[0]
    t = h.contents[0]
    orders = bs.select('#billboard > div.billboard-bd > table')[0]
    urls = []
    for order in orders.find_all('a'):
        urls.append((order['href'],order.string))
    return t, urls


def get_contents(url):

    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    c = bs.select('#link-report')[0]

    return(c.text)


if __name__ == '__main__':

    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)
    with Pool(5) as p:
        contents =  p.map(get_contents, [url[0] for url in urls])
    for content in contents:
        print(content)
```
使用多进程的Pool.map  实现并发抓取

这里有个问题我们的电影名称和介绍没有关联了，改进下

```

def get_contents(url):
    url, name = url.split('|')
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    c = bs.select('#link-report')[0]

    return(name, c.text)

if __name__ == '__main__':

    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)
    with Pool(5) as p:
        contents =  p.map(get_contents, [url[0] + '|' + url[1]  for url in urls])
    for content in contents:
        print(content[0])
        print(content[1])
```

## 保存抓取结果

1. 保存为文本

```
if __name__ == '__main__':

    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)
    with Pool(5) as p:
        contents =  p.map(get_contents, [url[0] + '|' + url[1]  for url in urls])
    
    with open(r'd:\r.txt', 'a') as f:
        for content in contents:
            f.write(content[0] + '\n' +content[1])
```
2. 保存为csv

```
if __name__ == '__main__':
    import csv
    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)
    with Pool(5) as p:
        contents =  p.map(get_contents, [url[0] + '|' + url[1]  for url in urls])
    
    with open(r'd:\r.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['名称', '介绍'])
        for contents in contents:
            writer.writerow(contents)
```
3. 写入数据库

**准备工作**

安装mysqlclient

pip install --only-binary :all: mysqlclient

--only-binary 安装编译好的二进制

启动mysql server

**建表**

```
import MySQLdb

db = MySQLdb.connect(host='localhost',user="root",database="test")
cursor = db.cursor()
sql = '''create table if not exists moive(
    id int auto_increment, 
    name varchar(50), 
    content varchar(250),
    PRIMARY KEY (`id`))'''
cursor.execute(sql)
cursor.close()
db.close()

```

**写入数据**

```
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import MySQLdb

def get_orders(url):
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    h = bs.select('#billboard > div.billboard-hd > h2')[0]
    t = h.contents[0]
    orders = bs.select('#billboard > div.billboard-bd > table')[0]
    urls = []
    for order in orders.find_all('a'):
        urls.append((order['href'],order.string))
    return t, urls


def get_contents(url):
    url, name = url.split('|')
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    c = bs.select('#link-report')[0]

    return(name, c.text.strip())


if __name__ == '__main__':
    import csv
    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)

    with Pool(5) as p:
        contents =  p.map(get_contents, [url[0] + '|' + url[1]  for url in urls])
    
    db = MySQLdb.connect(host='localhost',user='root',database='test',charset='utf8')
    cursor = db.cursor()
    for content in contents:
        sql = 'insert into moive(name, content) values("%s", "%s")' % (content[0], content[1])
        print(sql)
        cursor.execute(sql)
        db.commit()
    cursor.close()
    db.close()
```

## scrapy 

### 准备
安装scrapy

pip install d:\Twisted-18.9.0-cp36-cp36m-win_amd64.whl
pip install scrapy
pip install pypiwin32


### scrapy架构

[文档](https://docs.scrapy.org/en/latest/topics/architecture.html)
scrapy 是一个基于twisted的异步处理框架，是纯ptyhon实现的爬虫框架，模块间耦合度低，可扩展性强，可以灵活的完成格中需求

Scrapy是用Twisted编写的，Twisted是一个流行的事件驱动的Python网络框架。因此，它使用非阻塞（也称为异步）代码实现并发。

![img](./Chapter-05-code/pics/scrapy_architecture_02.png)

上图显示了Scrapy体系结构及其组件的概述，以及系统内部发生的数据流的概述（由红色箭头显示）。

它可以分为如下几个部分：
* Engine 引擎负责控制系统所有组件之间的数据流，并在发生某些操作时触发事件
* Scheduler 调度程序接收来自引擎的请求，并在引擎请求它们时将它们排入队列
* Downloader 负责获取网页并将其提供给引擎，引擎又将它们提供给Spider
* Spider 蜘蛛是由Scrapy用户编写的自定义类，用于解析响应并从中提取items
* Item Pipeline 负责在Item被Spider提取后处理Item。典型的包括清理，验证和持久性（如将项目存储在数据库中）
* Downloader middlewares 是位于Engine和Downloader之间的特定钩子，当它们从Engine传递到Downloader时处理请求，以及从Downloader传递到Engine的响应。
* Spider middlewares 是位于Engine和Spider之间的特定钩子，能够处理Spider输入（响应）和输出（Item和请求）。

### 数据流
Scrapy中的数据流由执行Engine控制
1. Engine从Spider获取爬行的初始请求
2. Engine在Scheduler中调度请求并请求下一个要爬取的请求
3. Scheduler将下一个请求返回给Engine
4. Engine将请求发送到Donlaoder
5. 页面完成下载后，Downlaoder会生成一个响应并将其发送到Engine
6. Engine从Downloader接收响应并将其发送到Spider进行处理
7. Spider处理响应并将抓取到的Item和新的请求返回到Engine
8. Engine将已抓取的Item发送到Item Pipe，并将新的请求发送给scheduler
9. 重复1-8，只到没有可抓取的请求

### 第一个项目

通过一个项目，完成一边scrapy。通过这个过程，可以对scrapy的基本用法和原理有个答题的了解

* 创建一个Scrapy项目
* 写一个spider去爬取站点和提取数据
* 使用命令行导出已抓取的数据
* 跟随链接


1. 创建一个项目
```
scrapy startproject tutorial
```
项目结构

```
tutorial/
├── scrapy.cfg            # 部署时的配置文件
└── tutorial              # 项目模块目录  
    ├── __init__.py
    ├── __pycache__
    ├── items.py          # 项目Item 定义
    ├── middlewares.py    # midlewares 文件
    ├── pipelines.py      # pipline 文件
    ├── settings.py       # 项目配置文件
    └── spiders           # 放置Spider的目录
        ├── __init__.py
        └── __pycache__

```

2. 第一个Spider

Spider 是一个Class Scrapy用来从网站抓取信息，它必须是scarpy.Spider的子类，并且包含一个初始请求。递归抓取和提取数据是可选的

在tutorial/spiders目录下新建文件quotes_spider.py

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```
我们定义了个类继承scrapy.Spider
name 定义了spider的名字在整个项目中必须是唯一的
start_requests 必须返回一个可迭代的请求（可以返回请求列表或编写生成器函数），Spider将开始爬行。后续请求将从这些初始请求中连续生成。
parse  对请求的响应结果进行处理。通常会解析响应，将抽取的数据作为dicts提取，并查找要跟踪的新URL并从中创建新请求（Request）

运行spider
进入tutorial/tutorial内
`scrapy crawl quotes`
在当前目录下生产两个html文件
Scrapy Scheduler 调度由Spider的start_requests方法返回的scrapy.Request对象,收到请求后，实例化Reponse对象并调用callback方法(self.parse()),井Reponse做为参数传递

3. 提取数据

学习如何使用Scrapy提取数据的最佳方法是使用shell 

`scrapy shell 'http://quotes.toscrape.com/page/1/'`

你会看到以下内容
```
2018-11-24 20:30:56 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x000001D4F03E8EB8>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x000001D4F2B09898>
[s]   spider     <DefaultSpider 'default' at 0x1d4f2dab6a0>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
```

使用css选择器
```
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```
返回一个Selector对象的列表

提取数据
```
 response.css('title::text').extract()
```
注意我们在css查询中添加了`::text`,意思提取title元素中的文本
如果不添加
```
>>> response.css('title').extract()
['<title>Quotes to Scrape</title>']
```

注意结果是个列表如果我们想提取提一个
```
>>> response.css('title::text').extract_first()
'Quotes to Scrape'

>>> response.css('title::text')[0].extract()
'Quotes to Scrape'
```

还可以使用xpath
```
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').extract_first()
'Quotes to Scrape'
```

提取名言与作者

```
scrapy shell 'http://quotes.toscrape.com'

>>> quote = response.css("div.quote")[0]
>>> title = quote.css("span.text::text").extract_first()
>>> title
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
>>> author = quote.css("small.author::text").extract_first()
>>> author
'Albert Einstein'

>>> tags = quote.css("div.tags a.tag::text").extract()
>>> tags
['change', 'deep-thoughts', 'thinking', 'world']
```

改写我们的spider
```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```
注意 start_urls 是start_requests方法的快捷方式

运行spider
```
scrapy crawl quotes


{'text': '“I like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.”', 'author': 'Dr. Seuss
', 'tags': ['fantasy']}
2018-11-24 21:05:00 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': '“I may not have gone where I intended to go, but I think I have ended up where I needed to be.”', 'author': 'Dougla
s Adams', 'tags': ['life', 'navigation']}
```
4. 保存抓取的数据

```
scrapy crawl quotes -o quotes.json

```

在当前目录下生产quotes.json文件

4. 跟随链接

选择下一页
```
scrapy shell 'http://quotes.toscrape.com'
response.css('li.next a::attr(href)').extract_first()
'/page/2/'
```

修改spider
```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

5. 存入数据库

使用item
定义item 类
修改tutorial/items.py
```
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```

修改spider 使用item 类
 ```
import scrapy
from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = TutorialItem()
            item['text'] = quote.css('span.text::text').extract_first()
            item['author'] = quote.css('span small::text').extract_first()
            item['tags'] = quote.css('div.tags a.tag::text').extract()
            yield item

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
 ```

 使用pipelines

修改tutorial/piplines.py
 ```
 # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import MySQLdb

class TutorialPipeline(object):
    def __init__(self, host, database, user):
        self.host = host
        self.database = database
        self.user = user
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            settings.get('MYSQL_HOST'),
            settings.get('MYSQL_DATABASE'), 
            settings.get('MYSQL_USER')
            )
    def open_spider(self, spider):
        self.db = MySQLdb.connect(host=self.host,database=self.database,user=self.user, charset='utf8')
        self.cursor = self.db.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
    def process_item(self, item, spider):
        data = dict(item)
        sql = 'insert into qutoes(text, author, tags) values("%s", "%s", "%s")' % (data['text'],data['author'],data['tags'])
        self.cursor.execute(sql)
        self.db.commit()
        return item

 ```

 修改settings.py
 取消 ITEM_PIPELINES 注释
 ```
 ITEM_PIPELINES = {
    'tutorial.pipelines.TutorialPipeline': 300,
}
 ```

 添加数据库配置
 ```
MYSQL_HOST='localhost'
MYSQL_DATABASE='test'
MYSQL_USER='root'
 ```