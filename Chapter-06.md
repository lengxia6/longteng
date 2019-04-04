# 第六天 爬虫高级和html

## 爬虫高级

### 实例爬取整个网站
爬取整个完整并保存到本地
新建一个项目名称为website, 新建spider类

```
import scrapy
from scrapy import log
import os.path
from urllib.parse import urlparse


class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net']

    def parse(self, response):
        urlpath= urlparse(response.url).path
        dirpath = '/'.join(urlpath.split('/')[:-1]).strip('/')
        if dirpath == "":
            dirpath = "."
        filename = urlpath.split('/')[-1]
        if filename:
            filepath = os.path.join(dirpath, filename)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            with open(filepath,"wb") as f:
                f.write(response.body)
        for ele in response.css('a[href$=html]::attr(href)'):
            next_page = ele.extract()

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
```
allowed_domains 爬取的网站域名

以上代码只是爬取了html结尾的链接，不包括css和js和图片等

```
# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
import os.path
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor

class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net']

    def parse(self, response):
        urlpath= urlparse(response.url).path
        dirpath = '/'.join(urlpath.split('/')[:-1]).strip('/')
        if dirpath == "":
            dirpath = "."
        filename = urlpath.split('/')[-1]
        if filename:
            filepath = os.path.join(dirpath, filename)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            with open(filepath,"wb") as f:
                f.write(response.body)
        linkextractor = LinkExtractor()
        links = linkextractor.extract_links(response)
        for link in links:
            next_page = link.url

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

```
LinkExtractor  类为链接提取类可以提取html中的所有链接

### 动态网站爬取 Scrapy+selenium+chrome handless

**准备**
安装selenium
`pip install selenium`
在群文件现在chromedriver
新建项目web12306

**编写自定义下载类**

打开文件middlewares.py添加下面代码
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time
class PhantomjsMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "TrainSchedule":
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(executable_path=r'D:\chromedriver.exe',
            chrome_options=chrome_options) 
            # driver = webdriver.Firefox()
            driver.get(request.url)
            time.sleep(5)
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
                return
    def spider_closed(self, spider, reason):
        print ('close driver......')
        self.driver.close()
```
**加载新添加的类**
修改settings.py
```
DOWNLOADER_MIDDLEWARES = {
    'web12306.middlewares.PhantomjsMiddleware': 543,
}
```

**编写spider类**

在spiders下新建文件
TrainSchedule.py
```
# -*- coding: utf-8 -*-
import scrapy


class TrainscheduleSpider(scrapy.Spider):
    name = 'TrainSchedule'
    start_urls = ['http://www.12306.com/#/train/search/SZQ/SJP/2018-12-01/']

    def parse(self, response):
        print(response.css('p.ng-binding::text').extract())

```
**运行spider**
`scrapy.exe crawl TrainSchedule`


## html 基础

HTML 是一种相当简单的、由不同元素组成的标记语言，它可用于表示文本片段，使文本在文档中具有不同的含义（段落、项目列表、表格），将文档结构化为逻辑块（头部、主体、导航菜单），并且可以将图片，影像等内容嵌入到页面中。

HTML由一系列的元素组成, 可以使用它来封装，标记内容的不同部分

```
html入门
html介绍
```

在html中只有使用如下表示才是一个段落

```
<p> html入门</p>
<p> html介绍</p>
```

### html 元素

![img](./Chapter-06-code/pic/grumpy-cat-small.png)

1. 元素的构成

* 开始标签 `<p>` 表示一个段落的开始
* 结束标签 `</p>` 表示一个段落结束
* 内容 开始标签和结束标签之间的部分
* 元素  开始标签+内容+结束标签 

2. 嵌套元素

元素里可以嵌套另一个元素

`<p>我的<strong>html</strong></p>`

所有的元素都需要正确的打开和关闭

3. 块级元素和内联元素

* 块级元素在页面中以块的形式展现 —— 相对与其前面的内容它会出现在新的一行，其后的内容也会被挤到下一行展现。块级元素通常用于展示页面上结构化的内容，例如段落、列表、导航菜单、页脚等等。一个以block形式展现的块级元素不会被嵌套进内联元素中，但可以嵌套在其它块级元素中

* 内联元素通常出现在块级元素中并包裹文档内容的一小部分，而不是一整个段落或者一组内容。内联元素不会导致文本换行：它通常出现在一堆文字之间例如超链接元素`<a>`或者强调元素`<em>`和 `<strong>`

看下面例子
```
<em>一</em><em>二</em><em>三</em>

<p>四</p><p>五</p><p>六</p>
```

`<em>` 是一个内联元素，所以就像你在下方可以看到的，第一行代码中的三个元素都没有间隙的展示在了同一行。而<p>是一个块级元素，所以第二行代码中的每个元素分别都另起了新的一行展现，并且每个段落间都有空行

4. 空元素
不是所有元素都拥有开始标签，内容和结束标签. 一些元素只有一个标签，通常用来在此元素所在位置插入/嵌入一些东西 。例如：元素<img>是用来在元素<img>所在位置插入一张指定的图片。例子如下：
```
<img src="https://www.python.org/static/img/python-logo.png">
```

### 属性
元素可以有属性

![img](./Chapter-06-code/pic/grumpy-cat-attribute-small.png)

属性包含元素的额外信息，这些信息不会出现在实际的内容中。在上述例子中，这个class属性给元素赋了一个识别的名字，这个名字可以css所使用

一个属性必须包含如下内容：

* 在元素和属性之间有个空格 (如果有一个或多个已存在的属性，就与前一个属性之间有一个空格)
* 属性后面紧跟着一个=号
* 有一个属性值,由一对引号""引起来

例子

```
<a href="https://github.com/jiam/python-dev" title="python-dev" target="_blank">教程</a>
```

* href: 这个属性声明超链接的web地址，当这个链接被点击浏览器会跳转至href声明的web地址
* title: 标题title 属性为超链接声明额外的信息
* target: 目标target 属性指定将用于打开链接的方式,target="_blank" 将在新标签页中打开链接


布尔属性

有时你会看到没有值的属性，它是合法的。这些属性被称为布尔属性，他们只能有跟它的属性名一样的属性值。例如 disabled 属性，他们可以标记表单输入使之变为不可用(变灰色)，此时用户不能向他们输入任何数据
```
<input type="text" disabled="disabled">
<input type="text">
```

### html文档结构
```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>我的测试页</title>
  </head>
  <body>
    <p>这是我的一个页面</p>
  </body>
</html>
```

* `<!DOCTYPE html>`: 声明文档类型
* `<html></html>: <html>`元素。这个元素包裹了整个完整的页面，是一个根元素。  
* `<head></head>: <head>`元素. 这个元素是一个容器，它包含了所有你想包含在HTML页面中但不想在HTML页面中显示的内容。这些内容包括你想在搜索结果中出现的关键字和页面描述，CSS样式，字符集声明等等。
* `<meta charset="utf-8">`: 这个元素设置文档使用utf-8字符集编码

* `<title></title>`: 设置页面标题，出现在浏览器标签上，当你标记/收藏页面时它可用来描述页面。
* `<body></body>: <body>`元素。 包含了访问页面时所有显示在页面上的内容，文本，图片，音频，游戏等等

### HTML中的空白

无论你用了多少空白(包括空白字符，包括换行), 当渲染这些代码的时候，HTML解释器会将连续出现的空白字符减少为一个单独的空格符

```
<p>Dogs are silly.</p>

<p>Dogs        are
         silly.</p>
```
这面两个写法效果是相同的

### html中的特殊字符

常见特殊字符
![img](./Chapter-06-code/pic/timg.jpg)

### HTML注释
为了将一段HTML中的内容置为注释，你需要将其用特殊的记号`<!--和-->`包括起来， 比如：
```
<p>I'm not inside a comment</p>

<!-- <p>I am!</p> -->
```

### html 元数据


![img](./Chapter-06-code/pic/meta.jpg)
```
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="application-name" content="Python.org">
```

打开`www.jd.com `查看源代码

### 在HTML中应用CSS和JavaScript

如今，几乎你使用的所有网站都会使用 CSS 让网页更加炫酷, 使用JavaScript让网页有交互功能, 比如视频播放器，地图，游戏以及更多功能。这些应用在网页中很常见，它们分别使用 `<link> <style>`元素以及` <script> `元素

```
<!-- 本地新闻 -->
<script src="//www.163.com/special/00774J00/index_news_keys.js" charset="gbk"></script>
<!-- 第三方合作新闻推荐 -->
<link href="https://static.ws.126.net/f2e/www/index20170701/collect/head~DIhBY9NJYLhd.css" rel="stylesheet" />
```


### HTML 文字基础

标题、段落
```
<h1>The Crushing Bore</h1>

<p>By Chris Mills</p>

<h2>Chapter 1: The Dark Night</h2>

<p>It was a dark night. Somewhere, an owl hooted. The rain lashed down on the ...</p>

<h2>Chapter 2: The eternal silence</h2>

<p>Our protagonist could not so much as a whisper out of the shadowy figure ...</p>

<h3>The specter speaks</h3>

<p>Several more hours had passed, when all of a sudden the specter sat bolt upright and exclaimed, "Please have mercy on my soul!"</p>
```

无序列表

```
<ul>
  <li>牛奶</li>
  <li>鸡蛋</li>
  <li>面包</li>
  <li>鹰嘴豆泥</li>
</ul>

```
有序列表

```
<ol>
  <li>行驶到这条路的尽头</li>
  <li>向右转</li>
  <li>直行穿过第一个双环形交叉路</li>
  <li>在第三个环形交叉路左转</li>
  <li>学校就在你的右边，300米处</li>
</ol>
```

嵌套列表

```
<ol>
  <li>Remove the skin from the garlic, and chop coarsely.</li>
  <li>Remove all the seeds and stalk from the pepper, and chop coarsely.</li>
  <li>Add all the ingredients into a food processor.</li>
  <li>Process all the ingredients into a paste.
    <ul>
      <li>If you want a coarse "chunky" humous, process it for a short time.</li>
      <li>If you want a smooth humous, process it for a longer time.</li>
    </ul>
  </li>
</ol>
```

斜体字、粗体字、下划线
```
<!-- scientific names -->
<p>
  The Ruby-throated Hummingbird (<i>Archilocus colubris</i>)
  is the most common hummingbird in Eastern North America.
</p>

<!-- foreign words -->
<p>
  The menu was a sea of exotic words like <i lang="uk-latn">vatrushka</i>,
  <i lang="id">nasi goreng</i> and <i lang="fr">soupe à l'oignon</i>.
</p>

<!-- a known misspelling -->
<p>
  Someday I'll learn how to <u>spel</u> better.
</p>

<!-- Highlight keywords in a set of instructions -->
<ol>
  <li>
    <b>Slice</b> two pieces of bread off the loaf.
  </li>
  <li>
    <b>Insert</b> a tomato slice and a leaf of
    lettuce between the slices of bread.
  </li>
</ol>
```

### 表格

```
<table class="dataintable">
<tr>
<th>选择器</th>
<th>例子</th>
<th>例子描述</th>
<th style="width:5%;">CSS</th>
</tr>

<tr>
<td><a href="/cssref/selector_class.asp" title="CSS .class 选择器">.<i>class</i></a></td>
<td>.intro</td>
<td>选择 class=&quot;intro&quot; 的所有元素。</td>
<td>1</td>
</tr>

<tr>
<td><a href="/cssref/selector_id.asp" title="CSS #id 选择器">#<i>id</i></a></td>
<td>#firstname</td>
<td>选择 id=&quot;firstname&quot; 的所有元素。</td>
<td>1</td>
</tr>
</table>
```

### 表单

1. 用户提交数据

```
<form action="http://foo.com" method="get">
  <div>
    <label for="say">What greeting do you want to say?</label>
    <input name="say" id="say" value="Hi">
  </div>
  <div>
    <label for="to">Who do you want to say it to?</label>
    <input name="to" id="to" value="Mom">
  </div>
  <div>
    <button>Send my greetings</button>
  </div>
</form>
```
* action 属性: 数据要提交到额url，在本例中，数据被发送到 —— http://foo.com
* method属性:  提交数据使用的http方法 ，本例get
```
GET /?say=Hi&to=Mom HTTP/1.1
Host: foo.com

POST / HTTP/1.1
Host: foo.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```

发送文件
```
<form method="post" enctype="multipart/form-data">
  <div>
    <label for="file">Choose a file</label>
    <input type="file" id="file" name="myFile">
  </div>
  <div>
    <button>Send the file</button>
  </div>
</form>
```
* enctype 该属性允许指定在提交表单时所生成的请求中的Content-Type的HTTP数据头的值，默认值application/x-www-form-urlencoded。意思是为发送的数据指定编码格式

2. 校验数据

强制必填
```
<form>
  <label for="choose">Would you prefer a banana or cherry?</label>
  <input id="choose" name="i_like" required>
  <button>Submit</button>
</form
```

* required 属性 必填

限制长度
```
<form>
  <div>
    <label for="choose">Would you prefer a banana or a cherry?</label>
    <input id="choose" name="i_like" required minlength="6" maxlength="6">
  </div>
  <div>
    <label for="number">How many would you like?</label>
    <input type="number" id="number" name="amount" value="1" min="1" max="10">
  </div>
  <div>
    <button>Submit</button>
  </div>
</form>
```

### 表单组件

1. 文本输入
```
<input type="text" id="comment" name="comment" value="I'm a text field">
```

2. E-mail 地址
```
<input type="email" id="email" name="email" multiple>
```
通过包括multiple属性，可以让用户将多个电子邮件地址输入相同的输入(以逗号分隔)

3. 密码
```
<input type="password" id="pwd" name="pwd">
```

4. 搜索
```
<input type="search" id="search" name="search">
```
5. 多行文本
```
<textarea cols="30" rows="10"></textarea>
```

6. 下拉选择框
```
<select id="simple" name="simple">
  <option>Banana</option>
  <option>Cherry</option>
  <option>Lemon</option>
</select>
```

7. 多选框
```
<select multiple id="multi" name="multi">
  <option>Banana</option>
  <option>Cherry</option>
  <option>Lemon</option>
</select>
```

8. 复选框
```
<input type="checkbox" checked id="carrots" name="carrots" value="carrots">
```
9. 单选按钮
```
<input type="radio" checked id="soup" name="meal">
```
10. 按钮

提交
```
<button type="submit">
    This a <br><strong>submit button</strong>
</button>

<input type="submit" value="This is a submit button">
```

重置
```
<button type="reset">
    This a <br><strong>reset button</strong>
</button>

<input type="reset" value="This is a reset button">
```
