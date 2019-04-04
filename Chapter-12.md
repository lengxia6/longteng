# 第十二天

## 实战项目 自动化测试平台
一个自动化接口测试平台，实现以下功能
* 项目管理
* 用例管理
* 测试报告
* 用户管理
* dashboard0p

### 创建项目框架

1. 使用django-admin 工具创建项目文件夹  autotest
2. 使用manager.py创建一个应用 apiautotest
3. 配置settings.py

```
# 注册app
INSTALLED_APPS = [
    'apiautotest.apps.ApiautotestConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 配置数据库，先启动mysql 并创建一个数据库 autotest
DATABASES = {
    'default': {
       # 'ENGINE': 'django.db.backends.sqlite3',
       # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'autotest',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# 配置语言和时区
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

# 配置静态文件目录，并在apiautotest目录下创建目录static 

STATIC_ROOT = BASE_DIR + '/apiautotest/static/'
```

4. 配置项目autotest/urls.py
```
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apiautotest/', include('apiautotest.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

5. 创建app apiautotest/urls.py
```
from django.urls import path
from . import views

urlpatterns = [
]
```

### 登录功能

配置登录url，登录view，登录template

#### 配置登录url
```
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
]
```

#### 登录view
```
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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

#### 登录template login.html

```
<!DOCTYPE html>
<html lang="zh-CN">

  <head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>登录</title>

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

### 创建base模板 base.html

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

    <!-- Page level plugin CSS-->
    <link href="/static/vendor/datatables/dataTables.bootstrap4.css" rel="stylesheet">

    <!-- Custom styles for this template-->
    <link href="/static/css/sb-admin.css" rel="stylesheet">

</head>

<body id="page-top">

    <nav class="navbar navbar-expand navbar-dark bg-dark static-top">

        <a class="navbar-brand mr-1" href="index.html">自动化测试平台</a>

        <button class="btn btn-link btn-sm text-white order-1 order-sm-0" id="sidebarToggle" href="#">
            <i class="fas fa-bars"></i>
        </button>


        <!-- Navbar -->
        <ul class="navbar-nav ml-auto ml-md-6">
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
                <a class="nav-link" href=#>
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href=#>
                    <i class="fas fa-fw fa-folder"></i>
                    <span>项目列表</span>
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
                    <a class="btn btn-primary" href="login.html">退出</a>
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
    <script src="/static/vendor/chart.js/Chart.min.js"></script>
    <script src="/static/vendor/datatables/jquery.dataTables.js"></script>
    <script src="/static/vendor/datatables/dataTables.bootstrap4.js"></script>

    <!-- Custom scripts for all pages-->
    <script src="/static/js/sb-admin.min.js"></script>

    <!-- Demo scripts for this page-->
    <script src="/static/js/demo/datatables-demo.js"></script>
    <script src="/static/js/demo/chart-area-demo.js"></script>

</body>

</html>
```

### 首页

#### inedex url配置
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
]
```

#### index view
```
def index(request):
    return render(request,"index.html")
```

#### index template index.html
```
{% extends "base.html" %} 
{% block content %}
<ol class="breadcrumb">
    <li class="breadcrumb-item">
        <a href="#">Dashboard</a>
    </li>
    <li class="breadcrumb-item active">Overview</li>
</ol>
{% endblock %}
```

更新base.html
```
            <li class="nav-item active">
                <a class="nav-link" href={% url "index" %}>
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </li>
```

### 项目管理
项目管理，新建项目，编辑项目

#### models apiautotest/models.py
```
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(max_length=50, verbose_name='项目名称')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')
    member = models.CharField(max_length=512, blank=True, null=True, verbose_name='项目成员')
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-createTime"]

```
#### 项目列表功能

url 配置
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
]
```

项目列表视图
```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

class ProjectListView(LoginRequiredMixin, generic.ListView):
    """
    项目列表视图 
    """
    model = Project
    template_name ='project/project_list.html'
    paginate_by = 10
```
项目列表模板  

```
{% extends "base.html" %} {% block content %} {% if object_list %}
<ol class="breadcrumb">
    <li class="breadcrumb-item">
        <a href="#">项目</a>
    </li>
    <li class="breadcrumb-item active">项目列表</li>
</ol>


<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <p>
                    <button onclick="location.href=# type="button" class="btn btn-primary btn-xs">新建项目</button>
                </p>
            </div>
            <!-- /.panel-heading -->
            <div class="panel-body">
                <div class="table">
                    <table class="table table-striped table-bordered table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>项目名称</th>
                                <th>描述</th>
                                <th>创建时间</th>
                                <th>最近修改时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for object in object_list %}
                            <tr>
                                <td>{{object.name}}</td>
                                <td>{{object.description}}</td>
                                <td>{{object.LastUpdateTime}}</td>
                                <td>{{object.createTime }}</td>
                                <td>
                                    <a class="playitbtn tryitbtnsyntax" href=#> 详情</a>
                                    <a class="playitbtn tryitbtnsyntax" href=#>编辑</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <!-- /.table-responsive -->
            </div>
            <!-- /.panel-body -->
        </div>
        <!-- /.panel -->
    </div>
    <!-- /.col-lg-12 -->
</div>
<!-- /.row -->

<!-- /.container-fluid -->

{% else %}
<p>There are no projects.</p>
{% endif %} {% endblock %}
```

更新base.html
```
            <li class="nav-item">
                <a class="nav-link" href={% url  "project_list" %}>
                    <i class="fas fa-fw fa-folder"></i>
                    <span>项目列表</span>
                </a>
            </li>
```

#### 项目详情功能

配置url
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
]
```

项目详情视图

```
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """
    项目详细视图
    """
    model = Project
    template_name = "project/project_detail.html"
```

项目详情模板

```
{% extends 'base.html' %} {% block content %}
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
    <h3 class="page-header">项目详情</h3>
    <div class="row">
        <div class="col-lg-3">
            <label>项目:</label>
        </div>
        <div class="col-lg-3">
            {{ object.name }}
        </div>
    </div>
    <div class='row'>
        <div class="col-lg-3">
            <label> 项目描述:</label>
        </div>
        <div class="col-lg-3">
            {{ object.description }}
        </div>
    </div>
    <div class='row'>
        <div class="col-lg-3">
            <label>创建时间:</label>
        </div>
        <div class="col-lg-6">
            {{ object.createTime }}
        </div>
    </div>
    <div class='row'>
        <div class="col-lg-3">
            <label>最近修改时间:</label>
        </div>
        <div class="col-lg-6">
            {{ object.LastUpdateTime }}
        </div>
    </div>
    <div class='row'>
        <div class="col-lg-3">
            <label>项目负责人:</label>
        </div>
        <div class="col-lg-3">
            {{ object.owner }}
        </div>
    </div>
    <div class='row'>
        <div class="col-lg-3">
            <label>项目成员:</label>
        </div>
        <div class="col-lg-3">
            {{ object.member }}
        </div>
    </div>
</div>
{% endblock %}
```

更新列表视图

```
<a class="playitbtn tryitbtnsyntax" href={% url "project_detail" object.id %}> 详情</a>
```

#### 项目编辑功能

url 配置

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
]
```

编辑视图
```
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def project_edit(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        if project.member is None:
            project.member=""
        else:
            project.member = project.member.replace(",","\n")
        return render(request, "project/project_form.html",{"project": project})
    if request.method == "POST":
        project = Project.objects.get(id=pk)
        project.name = request.POST.get("project_name")
        project_owner_str = request.POST.get("project_owner")
        try:
            project.owner = User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg = "指定的项目负责人不存在"
            if project.member is None:
                project.member=""
            return render(request, "project/project_form.html",{"project": project, "errmsg": errmsg})

        project.description = request.POST.get("project_description").strip()
        project_member_str = request.POST.get("project_member").strip()
        
        if project_member_str:
            member_list = project_member_str.strip().split("\n")
            for item in member_list:
                username = item.strip()
                try:
                   User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg = "项目成员%s不存在" % username
                    #return HttpResponse(len(project_member_str.strip()))
                    return render(request, "project/project_form.html",{"project": project, "errmsg": errmsg})
            project.member = ','.join(member_list)
        else:
            project.member="" 
        project.save()
        return redirect("project_detail",project.id)
```

项目表单模板

```
{% extends 'base.html' %} {% block content %}
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">
            
            <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="#">项目</a>
                    </li>
                    {% if project %}
                    <li class="breadcrumb-item active">项目编辑</li>
                    {% else %}
                    <li class="breadcrumb-item active">新建项目</li>
                    {% endif %}
            </ol>
            <div class="panel-body">
                <div class="col-lg-6">
                    <form method="post">
                        {% csrf_token %}
                        {% if errmsg %}
                        <div class="alert alert-warning">
                            <a href="#" class="close" data-dismiss="alert">
                                &times;
                            </a>
                            <strong>警告！</strong>{{ errmsg }}
                        </div>
                        {% endif %}
                        <div class="form-group">
                            <label for="Name">项目名称</label>
                            {% if project %}
                            <input class="form-control" name="project_name" required="required" value={{ project.name }}> {% else %}
                            <input class="form-control" name="project_name" required="required">  {% endif %}
                        </div>
                        <div class="form-group">
                            <label for="project_owner">项目负责人</label>
                            {% if project %}
                            <input class="form-control" name="project_owner" required="required" value={{ project.owner }}> {% else %}
                            <input class="form-control" name="project_owner" required="required" value={{ request.user }}> {% endif %}
                        </div>
                        <div class="form-group">
                            <label for="project_description">项目描述</label>
                            {% if project %}
                            <textarea class="form-control" rows="5" name="project_description" required="required">{{ project.description }} </textarea> {% else %}
                            <textarea class="form-control" rows="5" name="project_description" required="required"></textarea> {% endif %}
                        </div>
                        <div class="form-group">
                            <label for="project_member">项目成员</label>
                            {% if project %}
                            <textarea class="form-control" rows="5" name="project_member">{{ project.member }} </textarea> {% else %}
                            <textarea class="form-control" rows="5" name="project_member"></textarea> {% endif %}
                        </div>
                        <button type="submit" class="btn btn-default">提交</button>

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

更新列表模板
```
<a class="playitbtn tryitbtnsyntax" href={% url "project_edit" object.id %}>编辑</a>
```

#### 新建项目

url 配置

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/create', views.project_create, name='project_create')
]
```

新建项目view

```
def project_create(request):
    if request.method == "GET":
        return render(request, "project/project_form.html")
    if request.method == "POST":
        project_name = request.POST.get("project_name")
        project_owner_str = request.POST.get("project_owner")
        try:
            project_owner = User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg = "指定的项目负责人:%s不存在" % project_owner_str
            return render(request, "project/project_form.html",{"errmsg": errmsg})
        project_description = request.POST.get("project_description").strip()
        project_member_str = request.POST.get("project_member").strip()
        if project_member_str:
            member_list = project_member_str.strip().split("\n")
            for item in member_list:
                username = item.strip()
                try:
                   User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg = "项目成员%s不存在" % username
                    #return HttpResponse(len(project_member_str.strip()))
                    return render(request, "project/project_form.html",{"project": project, "errmsg": errmsg})
            project_member = ','.join(member_list)
        else:
            project_member=""

        project = Project(name=project_name,owner=project_owner,description=project_description,member=project_member)
        project.save()
        return redirect("project_detail",project.id)
```

更新项目列表模板

```
<button onclick="location.href='{% url 'project_create' %}'" type="button" class="btn btn-primary btn-xs">新建项目</button>
```

## 练习
项目列表添加分页功能