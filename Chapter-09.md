# 第九天

## 创建主页

我们现在可以添加代码来显示我们的第一个完整页面 -  LocalLibrary 网站的主页，显示每个模型类型有多少条记录，并提供我们其他页面的侧边栏导航链接。我们将编写基本URL映射和视图，从数据库获取记录以及使用模板展示

现在我们已经定义了我们的模型，并创建了一些数据，现在是编写代码以向用户呈现该信息的时候了。我们需要做的第一件事是确定我们希望能够在我们的页面中显示哪些信息，然后为返回这些资源定义适当的URL。那么我们将需要创建一个url映射器，视图和模板来显示这些页面。

以下图表提供了处理HTTP请求/响应时需要实现的数据和事情的主要流程。我们已经创建了这个模型，我们需要创建的主要内容是：

+ URL映射-根据匹配的URL转到相应的View功能。
+ View 函数从模型 获取请求的数据，创建一个显示数据的HTML页面，并将其返回给用户在浏览器查看。
+ 模板用来渲染view的数据

![img](./Chapter-09-code/basic-django.png)

### 定义资源URL
我们要为该网站提供一个登录页，以及显示书和作者的列表和详细视图的页面。
下面这些URL 是我们页面需要的
+ catalog/ — 主页
+ catalog/books/ — 书单页 列表视图
+ catalog/authors/ — 作者页 列表视图
+ catalog/book/<id> —详细视图。如下例子 ／catalog/book/3，id为3的书的详情
+ catalog/author/<id> — 详细视图。如下例子 /catalog/author/11，id为11的作者详情

### 创建主页
打开locallibrary/catalog/urls.py 修改以下内容

```
urlpatterns = [
    path('', views.index, name='index'),
]
```

path()函数定义了一个URL模式（在这种情况下是一个空字符串：''），在匹配到模式时将调用的视图函数（views.index - views.py中名为index()的函数）。

此path()函数还指定name参数，该参数唯一标识此特定URL映射。以使用此name“反转”映射器 - 动态创建指向映射器的资源的URL
例如，有了这个，我们现在可以通过在模板中创建以下链接从任何其他页面链接到我们的主页
```
<a href="{% url 'index' %}">Home</a>
```

我们可以对上面的链接进行硬编码（例如`<a href="/catalog/">主页</a>`），但如果我们更改了主页的模式（例如更改为/ catalog/index），模板将不再正确链接。使用反向url映射更加灵活和强大！

### View (基于函数)

视图是处理HTTP请求的功能，根据需要从数据库获取数据，通过使用HTML模板呈现此数据生成HTML页面，然后以HTTP响应返回HTML以显示给用户。索引视图遵循此模型 - 它提取有关数据库中有多少Book，BookInstance 可用 BookInstance 和 Author 记录的信息，并将其传递给模板以进行显示。

打开catalog/views.py，并注意该文件已经导入了 使用模板和数据生成HTML文件的 render() 快捷方式函数。

```
from django.shortcuts import render

# Create your views here.
```
复制以下代码。第一行导入我们将用于访问所有视图中数据的模型类
```
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    首页视图
    """
    # 统计图书的数目
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # 可接图书的数目 (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # 作者的数目
    
    # 渲染模板
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

```

视图函数的第一部分使用objects.all()模型类的属性来获取记录计数。它还会获取一个BookInstance状态字段值为“a”（可用）的对象列表。在函数结束时，我们将该函数称为render()创建和返回HTML页面作为响应。它将原始request对象，HTML模板以及context变量（Python字典）作为参数。

### Template（模板）

模版是定义一个文件（例如HTML页面）的结构与布局的文本文件，。Django将自动在应用程序“templates”目录查找模版。例如，在我们刚刚加的索引页，render() 函数会期望能够找到/locallibrary/catalog/templates/index.html这个文件，如何找不到该文件，则会引发错误。你可以看到访问 127.0.0.1:8000 现在将提供你一个相当直观的错误信息"TemplateDoesNotExist at /catalog/“以及其他详细信息

**扩展模版**

index模版将需要标准的HTML标记头部和正文，以及用于导航的部分（去我们尚为创建的网站其他的页面）以及一些介绍文本来展示我们图书数据。我们网站上的每一页，大部分文字（HTML和导航结构）都是一样的。Django模版语言不是强制开发人员在每个页面中复制这个“样板”，而是让你声明一个基本模版，然后再扩展它，仅替换每个特定页面不同的位置。

例如，基本模版 base.html 可能看起来像下面的文本。正如你所见的，它包含一些“常见“HTML”和标题，侧边栏和使用命名 block 和 endblock 模版标记（粗体显示）标记的内容部分。块可以是空的，或者包含将被派生页“默认使用”的内容。

 模版标签（{% %}）,你可以在模版中使用函数循环列表，基于变量的值执行条件操作等。除了模版标签，模版语法允许你引用模版变量（通过从视图进入模版），并使用模版过滤器重新格式化变量（例如，将字符串设置为小写）。

```
<!DOCTYPE html>
<html lang="en">
<head>
  {% block title %}<title>Local Library</title>{% endblock %}
</head>

<body>
  {% block sidebar %}<!-- insert default navigation text for every page -->{% endblock %}
  {% block content %}<!-- default content text (typically empty) -->{% endblock %}
</body>
</html>
```
当我们要为特定视图定义一个模版时，我们首先指定基本模版（使用 extends 模版标签）。如果我们想要在模版中替换的部分，会使用 block/endblock 在基本模版表明。

例如，下面我们使用 extends 模版标签，并覆盖 content 块。生成的最终HTML将包含在基本模板中定义的所有HTML和结构（包括在标题栏中定义的默认内容），但插入新内容块代替默认内容块

```
{% extends "base.html" %}

{% block content %}
<h1>Local Library Home</h1>
<p>Welcome to <em>LocalLibrary</em>, a very basic Django website developed as a tutorial example on the Mozilla Developer Network.</p>
{% endblock %}
```

**LocalLibrary基本模板**

下面就是我们的基本模版。正如所看到的，内容包括一些HTML和定义块 title ，sidebar 和 content。我们有默认的 title（当然我们可以改）和默认的所以图书和作者的链接列表 sidebar （我们可能并不会怎么改，但需要时，我们通过把想法放入块block中，比如想法是—允许范围）。创建一个新的文件 — locallibrary/catalog/templates/base_generic.html — 写入如下代码
```
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>SB Admin - Dashboard</title>

    <!-- Bootstrap core CSS-->
    <link href="/static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom fonts for this template-->
    <link href="/static/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">


    <!-- Custom styles for this template-->
    <link href="/static/css/sb-admin.css" rel="stylesheet">

</head>

<body id="page-top">

    <nav class="navbar navbar-expand navbar-dark  bg-dark static-top">

        <a class="navbar-brand mr-1" href="{% url "index" %}">图书管理平台</a>

        <button class="btn btn-link btn-sm text-white order-1 order-sm-0" id="sidebarToggle" href="#">
            <i class="fas fa-bars"></i>
        </button>


        <!-- Navbar -->
        <ul class="navbar-nav  ml-auto ml-md-6">
            <li class="nav-item dropdown no-arrow">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true"
                    aria-expanded="false">
                    <i class="fas fa-user-circle fa-fw"></i>
                </a>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
                    <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">Logout</a>
                </div>
            </li>
        </ul>

    </nav>

    <div id="wrapper">

        <!-- Sidebar -->
        <ul class="sidebar navbar-nav">
            <li class="nav-item active">
                <a class="nav-link" href="{% url "index" %}">
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>概览</span>
                </a>
            </li>

        </ul>

        <div id="content-wrapper">

            <div class="container-fluid">


                {% block content %}
                <!-- content-->

                {% endblock %}

            </div>
            <!-- /.container-fluid -->

            <!-- Sticky Footer -->
            <footer class="sticky-footer">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>Copyright © jiaminqiang 2018</span>
                    </div>
                </div>
            </footer>

        </div>
        <!-- /.content-wrapper -->

    </div>
    <!-- /#wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Logout Modal-->
    <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">退出</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">选择 "退出" 如果你确认退出.</div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">取消</button>
                    <a class="btn btn-primary" href=#>退出</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap core JavaScript-->
    <script src="/static/vendor/jquery/jquery.min.js"></script>
    <script src="/static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="/static/vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Page level plugin JavaScript-->

    <!-- Custom scripts for all pages-->
    <script src="/static/js/sb-admin.min.js"></script>
    <script src="/static/js/multiselect.min.js"></script>

 

</body>

</html>
```

该模版使用（并包含）JavaScript 和  Bootstrap  （css框架）来改进HTML页面的布局和显示，使用Bootstrap框架是创建一个可以在不同浏览器大小上很好地扩展的有吸引力的页面的快速方法，它还允许我们处理页面呈现而无需进入任何细节-我们只想关注服务器端代码.


**index模版**
新建HTML文件 locallibrary/catalog/templates/index.html 写入下面代码。第一行我们扩展了我们的基本模版, 使用 content替换默认块。
```
{% extends "base.html" %} {% block content %}
<ol class="breadcrumb">
    <li class="breadcrumb-item">
        <a href="#">概览</a>
    </li>
</ol>
<div class="row">
    <div class="col-xl-3 col-sm-6 mb-3">
      <div class="card text-white bg-primary o-hidden h-100">
        <div class="card-body">
          <div class="card-body-icon">
            <i class="fas fa-fw fa-comments"></i>
          </div>
          <div class="mr-5">图书种类: {{ num_books }}</div>
        </div>
      </div>
    </div>
    <div class="col-xl-3 col-sm-6 mb-3">
      <div class="card text-white bg-warning o-hidden h-100">
        <div class="card-body">
          <div class="card-body-icon">
            <i class="fas fa-fw fa-list"></i>
          </div>
          <div class="mr-5">图书数量: {{ num_instances }}</div>
        </div>
      </div>
    </div>
    <div class="col-xl-3 col-sm-6 mb-3">
      <div class="card text-white bg-success o-hidden h-100">
        <div class="card-body">
          <div class="card-body-icon">
            <i class="fas fa-fw fa-shopping-cart"></i>
          </div>
          <div class="mr-5">可接数量：{{ num_instances_available }}</div>
        </div>
      </div>
    </div>
    <div class="col-xl-3 col-sm-6 mb-3">
      <div class="card text-white bg-danger o-hidden h-100">
        <div class="card-body">
          <div class="card-body-icon">
            <i class="fas fa-fw fa-life-ring"></i>
          </div>
          <div class="mr-5">作者数量: {{ num_authors }}</div>
        </div>
     
      </div>
    </div>
  </div>
{% endblock %}
```

在动态内容部分，我们已经为视图中包含的信息声明了占位符（模板变量）。变量使用“{{ }}”语法标记
注意区别模板变量和模板标签

这里需要注意的重要一点是，这些变量是用我们在视图的render()函数中传递给context的字典的key命名的渲染模板时，这些将被其关联值替换
```
return render(
    request,
    'index.html',
     context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
)
```
**在模版中引用静态文件**

你的项目可能会使用静态资源，包括javascript，css 和图像。由于这些文件的位置可能不知道（或者可能会发生变化），则Django允许你指定你的模版相对于这些文件的url, STATIC_URL （默认基本网站设置的值为“／static／”）。



在settings.py中添加以下代码，
```
STATIC_ROOT = BASE_DIR + '/catalog/static/'
```
STATIC_ROOT 全局指定静态文件位置

## 通用列表和详细视图

### 书本清单页面
书本清单页面，将显示页面中所有可用图书记录的列表，使用url: catalog/books/进行访问。该页面将显示每条记录的标题和作者，标题是指向相关图书详细信息页面的超链接。

**URL映射**

打开/catalog/urls.py ，添加下面内容，这个path()函数，定义了一个与 URL 匹配的模式（'books/'），如果URL匹配，将调用视图函数（views.BookListView.as_view()）和一个对应这个特定映射的名称。

```
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
]
```

**View（基于类）**

我们可以很容易地，将书本列表视图编写为常规函数（就像我们之前的索引视图一样），它将查询数据库中的所有书本，然后调用render()，将列表传递给指定的模板。然而，我们用另一种方法取代，我们将使用基于类的通用列表视图（ListView） - 一个继承自现有视图的类。因为通用视图，已经实现了我们需要的大部分功能，并且遵循 Django 最佳实践，我们将能够创建更强大的列表视图，代码更少，重复次数更少

打开 catalog/views.py，并将以下代码复制到文件的底部：

```
from django.views import generic

class BookListView(generic.ListView):
    model = Book
```

通用视图将查询数据库，以获取指定模型（Book）的所有记录，然后呈现位于locallibrary/catalog/templates/catalog/book_list.html 的模板（我们将在下面创建）。在模板中，您可以使用名为object_list 或 book_list的模板变量（即通常为“the_model_name_list”），以访问书本列表

可以添加属性，以更改上面的默认行为。例如，如果需要使用同一模型的多个视图，则可以指定另一个模板文件，或者如果book_list对于特定模板用例不直观，则可能需要使用不同的模板变量名称。可能最有用的变更，是更改/过滤返回的结果子集 - 因此，您可能会列出其他用户阅读的前5本书，而不是列出所有书本。

```
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # book list 变量的名称
    queryset = Book.objects.all()
    #queryset = Book.objects.filter(title__icontains='python')[:5] # 书名包含python的5本书 
    template_name = 'book_list.html'  # 指定template名称
```
context_object_name 更改模板中引用对象的名称
queryset 更改默认的查询结果默认返回改modle的所有记录
template_name 更改默认的模板名称

**创建列表视图模板**

创建 HTML 文件 /locallibrary/catalog/templates/catalog/book_list.html，并复制到下面的文本中。如上所述，这是基于类的通用列表视图，所期望的默认模板文件（对于名为catalog的应用程序中，名为Book的模型）。

通用视图的模板就像任何其他模板一样（当然，传递给模板的上下文/信息可能不同）。与我们的index模板一样，我们在第一行扩展基本模板，然后替换名为content的区块。

 ```
{% extends "base.html" %}

{% block content %}
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="#">图书列表</a>
        </li>
    </ol>

    <div class="card mb-3">
        <div class="card-header">
          <i class="fas fa-table"></i>
          图书列表
          </div>
        <div class="card-body">
            {% if book_list %}
            <div class="table">
                    <table class="table  table-sm   table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>书名</th>
                                <th>作者</th>
                                <th>ISBN</th>
                                <th>列别</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for book in book_list %}
                            <tr>
                                <td>{{book.title}}</td>
                                <td>{{book.author}}</td>
                                <td>{{book.isbn}}</td>
                                <td>{{book.genre }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <p>There are no books in the library.</p>
                  {% endif %}
            </div>
        </div>
       
      </div>
           
{% endblock %}
 ```

 条件执行
 我们使用 if, else 和 endif模板标签，来检查 book_list是否已定义且不为空。如果 book_list为空，则 else子句显示文本，说明没有要列出的书本。如果 book_list不为空，那么我们遍历书本列表

 ```
{% if book_list %}
  <!-- code here to list the books -->
{% else %}
  <p>There are no books in the library.</p>
{% endif %}
 ```

 For 循环

 模板使用for 和 endfor模板标签，以循环遍历书本列表，如下所示。每次迭代都会使用当前列表项的信息，填充书本模板变量book

```
{% for book in book_list %}
  <li> <!-- code here get information from each book item --> </li>
{% endfor %}
```

访问变量

循环内的代码，为每本书创建一个列表项

```
<td>{{book.title}}</td>
```

我们使用“点符号”（例如 book.title 和 book.author）访问相关书本记录的字段，其中书本项目book后面的文本是字段名称（如同在模型中定义的）。

我们还可以在模板中，调用模型中的函数 - 在这里，我们调用Book.get_absolute_url()，来获取可用于显示关联详细记录的URL。这项工作提供的函数没有任何参数（没有办法传递参数！）

更新基本模板
打开基本模板（/locallibrary/catalog/templates/base.html）并将 {% url 'books' %} 插入所有书本 All books 的 URL 链接，如下所示。这将启用所有页面中的链接（由于我们已经创建了 “books” 的 url 映射器，我们可以成功地将其设置到位）


```
<li><a href="{% url 'books' %}">图书</a></li>
```

### 书本详细信息页面

书本详细信息页面，将显示有关特定书本的信息，使用 URL catalog/book/<id>（其中 <id> 是Book的主键）进行访问。除了Book模型中的字段（作者，摘要，ISBN，语言和种类）之外，我们还将列出可用副本（BookInstances）的详细信息，包括状态，预期返回日期，印记和 id。这将使我们的读者，不仅可以了解该书，还可以确认是否/何时可用

**URL 映射**

打开 /catalog/urls.py ，并添加下面粗体显示的 “book-detail” URL 映射器。这个 path() 函数定义了一个模式，关联到基于通用类的详细信息视图和名称。

```
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
```
对于书本详细信息路径，URL 模式使用特殊语法，来捕获我们想要查看的书本的特定 id。语法非常简单：尖括号定义要捕获的URL部分，包含视图可用于访问捕获数据的变量的名称。例如，<something> 将捕获标记的模式，并将值作为变量 “something” ，传递给视图。你可以选择在变量名称前，加上一个定义数据类型的转换器规范（int，str，slug，uuid，path）。

在这里，我们使用 '<int:pk>' 来捕获 book id，它必须是一个整数，并将其作为名为 pk 的参数（主键的缩写）传递给视图。

基于类的通用详细信息视图，需要传递一个名为 pk 的参数。如果您正在编写自己的函数视图，则可以使用您喜欢的任何参数名称，或者，确实也可以，在未命名的参数中传递信息

**View (基于类)**
打开 catalog/views.py，并将以下代码复制到文件的底部
 
```
class BookDetailView(generic.DetailView):
    model = Book
```

**创建详细信息视图模板**

创建 HTML 文件 /locallibrary/catalog/templates/catalog/book_detail.html

```
{% extends "base.html" %}

{% block content %}
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="#">图书详情</a>
        </li>
    </ol>

    <div class="card mb-3">
        <div class="card-header">
          <i class="fas fa-table"></i>
          图书详情
        </div>
        <div class="card-body">

                <h1>书名: {{ book.title }}</h1>

                <p><strong>作者:</strong> <a href="">{{ book.author }}</a></p> <!-- author detail link not yet defined -->
                <p><strong>摘要:</strong> {{ book.summary }}</p>
                <p><strong>ISBN:</strong> {{ book.isbn }}</p> 
                <p><strong>语言:</strong> {{ book.language }}</p>  
                <p><strong>类别:</strong> {% for genre in book.genre.all %} {{ genre }}{% if not forloop.last %}, {% endif %}{% endfor %}</p>  
              
                <div style="margin-left:20px;margin-top:20px">
                  <h4>副本</h4>
              
                  {% for copy in book.bookinstance_set.all %}
                  <hr>
                  <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">{{ copy.get_status_display }}</p>
                  {% if copy.status != 'a' %}<p><strong>预计可借日期:</strong> {{copy.due_back}}</p>{% endif %}
                  <p><strong>版次:</strong> {{copy.imprint}}</p>
                  <p class="text-muted"><strong>Id:</strong> {{copy.id}}</p>
                  {% endfor %}
                </div>
        </div>
       
      </div>
           
{% endblock %}
```
此模板中的几乎所有内容，都已在前面描述过
+ 我们扩展基本模板，并覆盖 “内容”区块 content。
+ 我们使用条件处理(if else endif)，来确定是否显示特定内容。
+ 我们使用 for 循环遍历对象列表
+ 我们使用 "点表示法" 访问context字段（因为我们使用了详细的通用视图，context被命名为book） 

函数book.bookinstance_set.all()返回与特定 Book 相关联的 BookInstance记录集合。

```
{% for copy in book.bookinstance_set.all %}
<!-- code to iterate across each copy/instance of a book -->
{% endfor %}
```

需要此方法，是因为仅在关系的 “一” 侧声明 ForeignKey（一对多）字段。由于没有做任何事情，来声明其他（“多”）模型中的关系，因此它没有任何字段，来获取相关记录集。为了解决这个问题，Django构造了一个适当命名的 “反向查找” 函数，您可以使用它。函数的名称，是通过对声明 ForeignKey 的模型名称，转化为小写来构造的，然后是_set（即，在 Book 中创建的函数是 bookinstance_set())

get_status_display函数 获取choices属性的值

修改book_list.html
```
<td><a href="{{ book.get_absolute_url }}">{{ book.title }}</a></td>
```

### 分页

记录少的时候，我们的图书清单页面看起来会很好。但是，当进入数十或数百条记录的页面时，页面将逐渐花费更长时间加载（并且有太多内容无法合理浏览）。此问题的解决方案，是为列表视图添加分页，减少每页上显示的项目数。

Django 在分页方面，拥有出色的内置支持。更好的是，它内置于基于类的通用列表视图中，因此您无需执行太多操作即可启用它！

打开 catalog/views.py，修改为以下内容

```
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
```

现在数据已经分页，我们需要添加对模板的支持，以滚动结果集合。因为我们可能希望在所有列表视图中，都执行此操作，所以我们将以可添加到基本模板的方式，执行此操作。

打开 /locallibrary/catalog/templates/base.html，修改为以下内容。代码首先检查当前页面上，是否启用了分页。如果是，则它会根据需要，添加下一个和上一个链接（以及当前页码）。

```
{% block content %}{% endblock %}
  
{% block pagination %}
  {% if is_paginated %}
      <div class="pagination">
          <span class="page-links">
              {% if page_obj.has_previous %}
                  <a href="{{ request.path }}?page={{ page_obj.previous_page_number }}">previous</a>
              {% endif %}
              <span class="page-current">
                  Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
              </span>
              {% if page_obj.has_next %}
                  <a href="{{ request.path }}?page={{ page_obj.next_page_number }}">next</a>
              {% endif %}
          </span>
      </div>
  {% endif %}
{% endblock %} 
```

page_obj 是一个 Paginator 对象，如果在当前页面上使用分页，它将存在。 它允许您获取有关当前页面，之前页面，有多少页面等的所有信息。

练习：
1. 实现Authour列表视图
2. 实现Authour详细视图
