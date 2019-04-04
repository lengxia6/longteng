# 第十天

## django session

我们在之前的教程中创建的LocalLibrary网站，允许用户浏览目录中的书本和作者。虽然内容是从数据库动态生成的，但每个用户在使用站点时，基本上都可以访问相同的页面，和相同类型的信息。

在一个 “真实” 的图书馆中，您可能希望根据用户之前对站点的使用，首选项等，为个人用户提供自定义体验。例如，您可以在用户下次访问时，隐藏上次已经确认的警告消息。网站，或存储和尊重他们的偏好（例如，他们希望在每个页面上显示的搜索结果的数量）。

session允许实现此类行为，允许基于每个站点访问者，显示不同的内容

### 什么是session

Web浏览器和服务器之间的所有通信，都是通过HTTP协议进行的，该协议是无状态的。协议无状态的事实，意味着客户端和服务器之间的消息，完全相互独立 - 没有基于先前消息的“序列”或行为的概念。因此，如果想拥有一个追踪与客户的持续关系的网站，需要自己实现。

session用于跟踪站点和特定浏览器之间“状态”的机制。会话允许您为每个浏览器存储任意数据，并在浏览器连接时，将该数据提供给站点。然后，通过“kye”引用与会话相关联的各个数据项，“key”用于存储和检索数据。

Django使用包含特殊session ID的cookie，来识别每个浏览器，及其与该站点的关联会话。默认情况下，实际会话数据存储在站点数据库中，您可以将Django配置为，将会话数据存储在其他位置（缓存，文件）

### 启用session

django项目默认会启用session

配置在项目文件（locallibrary/locallibrary/settings.py）的INSTALLED_APPS 和 MIDDLEWARE 部分中设置，如下所示

```
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    ....

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ....
```

### 使用session
你可以从request请求参数访问视图中的session会话属性（作为视图的第一个参数传入的HttpRequest）。此会话属性，表示与当前用户的特定连接（或者更确切地说，是与当前浏览器的连接，由此站点的浏览器cookie中的会话ID标识）。

会话session属性是一个类似字典的对象，您可以在视图中多次读取和写入，并根据需要进行修改。您可以执行所有常规的字典操作，包括清除所有数据，测试是否存在密钥，循环数据等。大多数情况下，您只需使用标准 “字典” API，来获取和设置值。


API还提供了许多其他方法，主要用于管理关联的会话cookie。例如，有一些方法，可以测试客户端浏览器，是否支持cookie，设置和检查cookie过期日期，以及从数据存储中清除过期的会话。你可以在[如何使用会话](https://docs.djangoproject.com/en/2.0/topics/http/sessions/)中找到完整的API。


### 简单的例子 - 获取访问次数

作为一个简单的现实世界的例子，我们将更新我们的图书馆，告诉当前用户，他们访问 LocalLibrary 主页的次数。

打开/locallibrary/catalog/views.py，做以下更改
```
# Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)
```

这里，我们首先得到 session key  'num_visits'的值，如果之前没有设置，则将值设置为0。每次收到请求时，我们都会递增该值，并将其存回会话中（下次用户访问该页面时）。然后将num_visits变量，传递给上下文变量中的模板。


编辑locallibrary/catalog/templates/index.html 添加以下代码
```
<div class="row">
  <div class="col-xl-3 col-sm-6 mb-3">
    <div class="alert alert-warning">
      <a href="#" data-dismiss="alert"></a>
      {{ request.user }}-访问次数: <strong>{{ num_visits }}</strong>
    </div>
  </div>
</div>
```

在后台数据库的django_session表中可以看到session的记录：
session表包含3个字段 session_key、session_data、expire_date
session_key 字段session的唯一标志，关联cookie中的sessionid
seesion_data session信息,该字段使用了base64编码，要查看里面内容可使用base64解码
```
>>> import base64
>>> base64.b64decode('YmEzZWZmZDY2YzdjOTIxMzRkZTdlMTg5ZTE3MmM3YmZhNDM2NzdmNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4MGM0YjZhODU0ZjVkMmNjODgyYjkyNjBkYTM4MzUyZTMxMDBlNDc0IiwibnVtX3Zpc2l0cyI6NH0=')
b'ba3effd66c7c92134de7e189e172c7bfa43677f6:{"_auth_user_id":"1","_auth_user_backend":"django.contrib.auth.backends.ModelBackend","_auth_user_hash":"80c4b6a854f5d2cc882b9260da38352e3100e474","num_visits":4}'
```


## 身份验证
Django 提供了一个身份验证和授权（“权限”）系统，该系统构建在的session框架之上，允许你验证用户凭据，并定义每个用户可允许执行的操作。该框架包括用户Users和分组Groups的内置model（一次向多个用户应用权限的通用方法），用于登录用户的权限/标志，以指定用户是否可以执行任务，表单和视图，以及查看限制内容的工具。


下面演示如何在LocalLibrary网站中，启用用户身份验证，创建自己的登录和注销页面，为模型添加权限，以及控制对页面的访问。我们将使用身份验证/权限，来显示用户和图书馆员借用图书的列表。

### 启用身份验证

django 默认启用身份验证功能

配置在项目文件（locallibrary/locallibrary/settings.py）的INSTALLED_APPS和MIDDLEWARE部分中设置，如下所示

```
INSTALLED_APPS = [
    ...
    'django.contrib.auth',  #Core authentication framework and its default models.
    'django.contrib.contenttypes',  #Django content type system (allows permissions to be associated with models).
    ....

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',  #Manages sessions across requests
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',  #Associates users with requests using sessions.
    ....
```

### 设置登录url
```
path('login/',views.user_login, name='user_login'),
```

### 设置身份验证视图

```
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            msg = "账号或密码错误"
            return render(request,"login.html",{"msg": msg})
```



### 登录模板
创建一个名为 templates/login.html 的新HTML文件。为它加入以下内容：

```
<!DOCTYPE html>
<html lang="zh-CN">

  <head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>SB Admin - Login</title>

    <!-- Bootstrap core CSS-->
    <link href="/static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom fonts for this template-->
    <link href="/static/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">

    <!-- Custom styles for this template-->
    <link href="/static/css/sb-admin.css" rel="stylesheet">

  </head>

  <body class="bg-dark">

    <div class="container">
      <div class="card card-login mx-auto mt-5">
        <div class="card-header">登录</div>
        <div class="card-body">
          <form method="post" action="{% url 'user_login' %}">
            {% csrf_token %}
            <div class="form-group">
              <div class="form-label-group">
                <input type="text" name="username" id="inputUser" class="form-control" placeholder="Email address" required="required" autofocus="autofocus">
                <label for="inputUser">用户名</label>
              </div>
            </div>
            <div class="form-group">
              <div class="form-label-group">
                <input type="password" name="password" id="inputPassword" class="form-control" placeholder="Password" required="required">
                <label for="inputPassword">密码</label>
              </div>
            </div>
            {% if msg %}
                <div class="alert alert-warning">
                    <a href="#" class="close" data-dismiss="alert">
                        &times;
                    </a>
                    <strong>警告！</strong>{{ msg }}
                </div>
            {% endif %}
            <div class="form-group">
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="remember-me">
                  记住密码
                </label>
              </div>
            </div>
            
            <input class="btn btn-primary btn-block" type="submit" value="登录">
              
        </form>
          <div class="text-center">
            <a class="d-block small mt-3" href="#">注册</a>
            <a class="d-block small" href="#">忘记密码?</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap core JavaScript-->
    <script src="/static/vendor/jquery/jquery.min.js"></script>
    <script src="/static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="/static/vendor/jquery-easing/jquery.easing.min.js"></script>

  </body>

</html>
```
`<form method="post" action="{% url 'user_login' %}">`
表单的提交方法method、 action 指定提交的url
`{% csrf_token %}` 防止csrf攻击 
CSRF 攻击之所以能够成功，是因为黑客可以完全伪造用户的请求，该请求中所有的用户验证信息都是存在于 cookie 中，因此黑客可以在不知道这些验证信息的情况下直接利用用户自己的 cookie 来通过安全验证。要抵御 CSRF，关键在于在请求中放入黑客所不能伪造的信息，并且该信息不存在于 cookie 之中。可以在 HTTP 请求中以参数的形式加入一个随机产生的 token，并在服务器端建立一个拦截器来验证这个 token，如果请求中没有 token 或者 token 内容不正确，则认为可能是 CSRF 攻击而拒绝该请求。

### 退出url
```
path('logout/',views.user_logout, name='user_logout'),
```

### 退出view
```
def user_logout(request):
    logout(request)
    return redirect('user_login')
```

### 修改base.html
```
<div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">退出</h5>
            <button class="close" type="button" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body">退出当前用户</div>
          <div class="modal-footer">
            <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
            <a class="btn btn-primary" href="{% url "user_logout" %}">Logout</a>
          </div>
        </div>
      </div>
    </div>
```

设置退出url`<a class="btn btn-primary" href="{% url "user_logout" %}">Logout</a>`

### 添加检查是否登录
先导入要是的装饰器和类，在需要验证的地方添加
```
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def index(request):
...
...

class BookListView(LoginRequiredMixin, generic.ListView):
```

再次刷新http://127.0.0.1:8000/catalog/ 404默认重定向到

http://127.0.0.1:8000/accounts/login/?next=/catalog/

设置默认重定向配置
修改settings.py
```
LOGIN_URL='/catalog/login/'
```

### 权限控制

查看用户权限
```
>>> from django.contrib.auth.models import User
>>> user_obj = User.objects.get(username='test')
>>> user_obj.get_all_permissions()
{'catalog.view_book'}
```
添加用户权限认证
```
@login_required
def index(request):
    """
    首页视图
    """
    # 判断权限
    if not request.user.has_perm('catalog.view_book'):
        return HttpResponse("no permession")
```

## 新建book表单

新建表单功能
###

url配置
```
path('books/create', views.book_create, name='book_create'),
```


view视图
```
def book_create(request):
    if request.method == "GET":
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = {"authors": authors, "genres": genres}
        return render(request, "book_create.html",context)
    if request.method == "POST":
        book_title = request.POST.get("book_title")
        book_author_id = request.POST.get("book_author")
        book_summary = request.POST.get("book_summary")
        book_isbn = request.POST.get("book_isbn")
        book_genre_ids = request.POST.getlist("book_genre")
        book_author = Author.objects.get(id = book_author_id)
        book = Book(title=book_title, author=book_author, summary=book_summary, isbn=book_isbn)
        book.save()
        for book_genre_id in  book_genre_ids:
            book_genre = Genre.objects.get(id = book_genre_id)
            book.genre.add(book_genre)
        book.save()
        #return HttpResponse(book_genre_ids)
        return redirect('books')
```
book 表单模板

```
{% extends 'base.html' %} {% block content %}
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">图书</a>
                </li>
                <li class="breadcrumb-item active">新建图书</li>
            </ol>
            <div class="panel-body">
                <div class="col-lg-6">
                    <form method="post">
                        {% csrf_token %}
                        <div class="form-group">
                            <label>名称</label>
                            <input class="form-control" name="book_title" required="required">
                        </div>
                        <div class="form-group">
                            <label>作者</label>
                            <select class="form-control" name="book_author" id="id_book_author">
                                {% for author in authors %}
                                <option value="{{ author.id }}">{{ author }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>概述</label>
                            <textarea class="form-control" rows="5" name="book_summary" required="required"></textarea>
                        </div>

                        <div class="form-group">
                            <label>ISBN</label>
                            <input class="form-control" name="book_isbn" required="required">
                        </div>

                        <div class="form-group">
                            <label>类别</label>
                            <select class="form-control" name="book_genre" id="id_book_genre" multiple>
                                {% for genre in genres %}
                                <option value="{{ genre.id }}">{{ genre }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">提交</button>
                        </div>
                    </form>
                </div>
                <!-- /.col-lg-6 -->
            </div>
            <!-- /.panel-body -->
        </div>
        <!-- /.panel -->
    </div>
    <!-- /.col-lg-12 -->
</div>
{% endblock %}
```
添加新建book入口,修改book_list.html

```
{% extends "base.html" %}

{% block content %}
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="#">图书列表</a>
        </li>
    </ol>
    <div class="mb-2">
        <button onclick="location.href='{% url 'book_create'  %}'" type="button" class="btn btn-primary btn-xs">新建book</button>
    </div>
...
...
```

### 编辑book
修改已创建的图书内容

### url 设置
```
path('book/<int:pk>/edit', views.book_edit, name='book_edit'),
```

### 修改book_list 添加编辑选项
```
<td><a href="{% url 'book_edit' book.id %}">编辑</td>
```

### 修改view
```
def book_edit(request, pk):
    if request.method == "GET":
        return HttpResponse(pk)
```

### 编辑表单
```
{% extends 'base.html' %} {% block content %}
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">图书</a>
                </li>
                <li class="breadcrumb-item active">图书编辑</li>
            </ol>
            <div class="panel-body">
                <div class="col-lg-6">
                    <form method="post">
                        {% csrf_token %}
                        <div class="form-group">
                            <label>名称</label>
                            <input class="form-control" name="book_title" required="required" value="{{ book.title }}">
                        </div>
                        <div class="form-group">
                            <label>作者</label>
                            <select class="form-control" name="book_author" id="id_book_author">
                                {% for author in authors %}
                                <option value="{{ author.id }}">{{ author }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>概述</label>
                            <textarea class="form-control" rows="5" name="book_summary" required="required">{{ book.summary }}</textarea>
                        </div>

                        <div class="form-group">
                            <label>ISBN</label>
                            <input class="form-control" name="book_isbn" required="required" value="{{ book.isbn }}">
                        </div>

                        <div class="form-group">
                            <label>类别</label>
                            <select class="form-control" name="book_genre" id="id_book_genre" multiple>
                                {% for genre in genres %}
                                <option value="{{ genre.id }}">{{ genre }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">提交</button>
                        </div>
                    </form>
                </div>
                <!-- /.col-lg-6 -->
            </div>
            <!-- /.panel-body -->
        </div>
        <!-- /.panel -->
    </div>
    <!-- /.col-lg-12 -->
</div>

<script>
    
        var e = document.getElementById("id_book_author")
        var optionsText="{{ book.author }}"
        for(var i=0;i<e.options.length;i++){
            if(e.options[i].text==optionsText){
                e.options[i].selected=true;
            }
        }
        var e = document.getElementById("id_book_genre")
        var optionsText="{% for genre in book.genre.all %} {{ genre }}{% if not forloop.last %}, {% endif %}{% endfor %}"
        for(var i=0;i<e.options.length;i++){
            if(optionsText.includes(e.options[i].text)){
                e.options[i].selected=true;
            }
        }
             
    </script>
{% endblock %}
```

###再次编辑view
```
def book_edit(request, pk):
    if request.method == "GET":
        book = Book.objects.get(id = pk)
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = { "book": book, "authors": authors, "genres": genres }
        return render(request, "book_edit.html", context)
    if  request.method == "POST":
        book = Book.objects.get(id = pk)
        book.title = request.POST.get("book_title")
        book_author_id = request.POST.get("book_author")
        book.summary = request.POST.get("book_summary")
        book.isbn = request.POST.get("book_isbn")
        book_genre_ids = request.POST.getlist("book_genre")
        book.author = Author.objects.get(id = book_author_id)
        book.genre.clear()
        for book_genre_id in  book_genre_ids:
            book_genre = Genre.objects.get(id = book_genre_id)
            book.genre.add(book_genre)
        book.save()
        return redirect('books')
```

### 练习
1. 菜单栏添加类别，作者列表
2. 完成类别，作者的新建，与编辑