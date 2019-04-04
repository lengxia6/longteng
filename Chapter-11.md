# 第十一天
mock就是模拟的意思，在开发和测试过程过，要使用某些功或者服务，但该功能和服务的代码还为开发或未开发完成，这是我们就需要用到mock

mock概念 [url](https://www.cnblogs.com/zjoch/p/6565956.html)


## 使用场景
* 单元测试
* 模拟外部依赖服务


### unittest.mock

使用python自带的unittest.mock模块，主要用来模拟python对象（函数/方法/模块）

example-1 模拟函数
```
from unittest import mock

def helloword():
   return "helloword"

def get_helloword():
    helloword = mock.Mock(return_value="helloword")
    r = helloword()
    print(r)

get_helloword()
```

example-2 模拟方法
```
from unittest import mock

class Person:
    def __init__(self):
        self.age = 10

    def get_age(self):
        return self.age

p = Person()
p.get_age = mock.Mock(return_value=20)
print(p.get_age())
```

exaple-3 模拟模块


创建python文件
mod1.py
```
def method1():
    pass
```

test.py
```
from unittest.mock import patch
import mod1
@patch('mod1.method1')
def test(mock_mod1):
    mock_mod1.return_value = "return mehthod1"
    print(mod1.method1())

test()
```

### 单元测试mock

被测代码
```
import requests

def send_request(url):
    r = requests.get(url)
    return r.status_code

def visit_ustack():
    return send_request('http://www.ustack.com')


```
单元测试

```
import unittest
from unittest import mock
import client

class TestClient(unittest.TestCase):
    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        client.send_request = success_send
        self.assertEqual(client.visit_ustack(), '200')

    def test_fail_request(self):
        fail_send = mock.Mock(return_value='404')
        client.send_request = fail_send
        self.assertEqual(client.visit_ustack(), '404')
```
执行单元测试

`python -m unittest test.py`

单元测试什么情况下使用mock
* 真实对象具有不可确定的行为(产生不可预测的结果，如股票的行情)
* 真实对象的某些行为很难触发(比如500错误)
* 真实情况令程序的运行速度很慢
* 被测试对象不存在

测试代码
```
import random

def get_tmp():
    return random.randint(-30, 40)

def alert():
    if get_tmp() > 30:
        return "tmp is  too high"
```

单元测试

```
import unittest
from unittest import mock
import client

class TestClient(unittest.TestCase):
    def test_success_request(self):
        success_send = mock.Mock(return_value=35)
        client.get_tmp = success_send
        self.assertEqual(client.alert(), 'tmp is  too high')
  
```

### mock service

a服务远程调用b服务 b服务还未开发完成

```
import requests
from unittest import mock

def request_a(url):
    r = requests.get(url)
    return r.status_code

def visit_ustack():
    return request_a('http://www.ustack.com')

request_a = mock.Mock(return_value="200")

print(visit_ustack())
```

### http mock service 工具

Turq是一个小型HTTP服务器，可以使用基于Python的语言编写脚本。使用它来设置模拟HTTP资源，以响应您选择的status，header和body
pip install turq

启动turq
`turq`

访问turq
http://127.0.0.1:13086

examle1
```
if path == '/hello':
    header('Content-Type', 'text/plain')
    body('Hello world!\r\n')
else:
    error(404)
```

以上代码填入编辑框,点击install 
访问以下地址
http://127.0.0.1:13085/hello


模拟restful接口
```
if route('/v1/products/:product_id'):
    if GET or HEAD:
        json({'id': int(product_id),
              'inStock': True})
    elif PUT:
        # Pretend that we saved it
        json(request.json)
    elif DELETE:
        status(204)   # No Content
if route('/v1/products'):
    if POST:
         json(request.json)
```
get
```
curl http://127.0.0.1:13085/v1/products/1
```

put
```
curl -X PUT  http://127.0.0.1:13085/v1/products/1 -d '
{
    "username": "jiminqiang",
    "age": 18
}
'
```
delete
```
curl -X DELETE -v http://127.0.0.1:13085/v1/products/2
```

模拟基本认证
```
basic_auth()
with html():
    H.h1('Super-secret page!')
```
`curl -u "test:password"  http://127.0.0.1:13085`

摘要认证
```
digest_auth()
```
`curl --digest -u  "test :password" http://127.0.0.1:13085`

Bearer token
```
bearer_auth()
```

`curl  -H 'authorization: Bearer sfsfasfdsf'  http://127.0.0.1:13085`

非编辑模式启动

 turq  --no-editor --rules  test.py

 ```
 if path == '/hello':
    header('Content-Type', 'text/plain')
    body('Hello world!\r\n')
else:
    error(404)
 ```
访问

`curl  http://127.0.0.1:13085/hello`

### 使用django开发一个rest mock
1. 创建项目和app
```
django-admin startproject simplemock
manage.py startapp mock
```
配置app

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mock.apps.MockConfig',
]
```

配置url
```
from django.contrib import admin
from django.urls import path
from mock import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

]
```

配置view
```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("index")
```
###练习实现 truq的rest 功能

