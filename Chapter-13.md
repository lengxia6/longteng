# 第十三天

## 调整下样式

1. 调整导航栏颜色

apiautotest/templates/base.html 将bg-dark 调整为bg-info

```
<nav class="navbar navbar-expand navbar-dark bg-info static-top">
```

2. 调整侧栏颜色和宽度

apiautotest/static/sb-admin.css

将133行附近的 background-color 调整为`#004085`
```
.sidebar {
  width: 90px !important;
  background-color: #004085;
  min-height: calc(100vh - 56px);
}
```

将186 行 附近的width从255 调整为150

```
 .sidebar {
    width: 150px !important;
  }
```

3. 调整表格样式

将 apiautotest/templates/project/project_list.html 21行附近调整为小表格样式

```
<table class="table  table-sm   table-hover" id="dataTables-example">
```

## 退出功能

### 添加url

logout

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/create', views.project_create, name='project_create')
]
```
### 添加views.py

```
# 修改顶部from import 语句导入logout函数
from django.contrib.auth import authenticate, login, logout

# 添加logut 函数
def user_logout(request):
    logout(request)
    return redirect('user_login')
```

###  更新base.html 页面

修改退出的url 为`% url 'user_logout'%}`

```
<div class="modal-footer">
    <button class="btn btn-secondary" type="button" data-dismiss="modal">取消</button>
    <a class="btn btn-primary" href={% url 'user_logout'%}>退出</a>
</div>

```


## 添加验证认证功能

现在大家不登录依然可以访问index页面，因为我们未进行登录验证
### 函数式视图

```
# 导入装饰器函数 login_required
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request,"index.html")

```


### 类视图
这个 上次课我们已经添加了

```
# 导入mixin类
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """
    项目详细视图
    """
    model = Project
    template_name = "project/project_base.html"
```

### 定义未登录时跳转到登录的url

settings.py  追加以下内容

```
LOGIN_URL='/apiautotest/login/'
```


## 更新项目详情页

创建project_base.html模板
```
{% extends "base.html" %}
{% block content %} 
<nav class="navbar navbar-expand  bg-light text-white static-top">
    <ul class="nav">
        <li class="nav-item">
          <a class="nav-link active" href={% url "project_detail" project.id %}>项目概况</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">api接口</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">测试报告</a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#">Disabled</a>
        </li>
      </ul>
</nav>
{% block project %}

{% endblock %}

{% endblock %}

```

更新project_detail.html
```
{% extends "project/project_base.html" %}
{% block project %}
<p></p>
<div class="row">
  <div class="col-xl-3 col-sm-6 mb-3">
    <div class="card text-white bg-primary o-hidden h-100">
      <div class="card-body">
        
        <div class="mr-5">{{ object.name }}</div>
      </div>
      <a class="card-footer text-white clearfix small z-1" href="#">
        <span class="float-left">项目名称</span>
        
      </a>
    </div>
  </div>
  <div class="col-xl-3 col-sm-6 mb-3">
    <div class="card text-white bg-warning o-hidden h-100">
      <div class="card-body">
       
        <div class="mr-5">{{ object.owner }}</div>
      </div>
      <a class="card-footer text-white clearfix small z-1" href="#">
        <span class="float-left">项目负责人</span>
       
      </a>
    </div>
  </div>
  <div class="col-xl-3 col-sm-6 mb-3">
    <div class="card text-white bg-success o-hidden h-100">
      <div class="card-body">
        
        <div class="mr-5">{{ object.createTime }}</div>
      </div>
      <a class="card-footer text-white clearfix small z-1" href="#">
        <span class="float-left">创建时间</span>
        
      </a>
    </div>
  </div>
  <div class="col-xl-3 col-sm-6 mb-3">
    <div class="card text-white bg-danger o-hidden h-100">
      <div class="card-body">
        
        <div class="mr-5">{{ object.createTime }}</div>
      </div>
      <a class="card-footer text-white clearfix small z-1" href="#">
        <span class="float-left">最近修改时间</span>
        
      </a>
    </div>
  </div>
</div>
{% endblock %}
```


## api 接口管理

新建api接口，编辑接口，接口列表

### 新建model

```
REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)


REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '原数据(raw)')
)

class HttpApi(models.Model):
    """
    接口信息
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiurl = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', blank=True, null=True,choices=REQUEST_PARAMETER_TYPE_CHOICE)
    requestHeader = models.TextField(max_length=2048, verbose_name="请求header",blank=True, null=True)
    requestBody = models.TextField(max_length=2048, verbose_name="请求体",blank=True, null=True)
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='更新人')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __str__(self):
        return self.name
```

### 新建接口

url配置
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/create', views.project_create, name='project_create'),
    path('project/<int:pk>/httpapi/create', views.httpapi_create, name='httpapi_create')
]
```

新建api视图

```
@login_required
def httpapi_create(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        return render(request,"project/httpapi_form.html", {"project": project })
    if request.method == "POST":
        httpapi_project = Project.objects.get(id=pk)
        httpapi_name = request.POST.get("httpapi_name")
        httpapi_description = request.POST.get("httpapi_description")
        httpapi_url = request.POST.get("httpapi_url")
        httpapi_requesttype = request.POST.get("httpapi_requesttype")
        httpapi_requestheader = request.POST.get("httpapi_requestheader")
        httpapi_requestparametertype = request.POST.get("httpapi_requestparametertype")
        httpapi_requestbody = request.POST.get("httpapi_requestbody")
        userupdate= request.user

        httpapi = HttpApi(project=httpapi_project,
                          name=httpapi_name,
                          requestType=httpapi_requesttype,
                          apiurl=httpapi_url,
                          requestParameterType=httpapi_requestparametertype,
                          requestHeader=httpapi_requestheader,
                          requestBody=httpapi_requestbody,
                          userUpdate=userupdate,
                          description=httpapi_description
                          )
        httpapi.save()

        return HttpResponse("ok")
```

新建api接口模板httpapi_form.html

```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">api接口</a>
                </li>
                {% if object %}
                <li class="breadcrumb-item active">接口编辑</li>
                {% else %}
                <li class="breadcrumb-item active">新建接口</li>
                {% endif %}
            </ol>
            <div class="panel-body">
                <div class="col-lg-6">
                    <form method="post">
                        {% csrf_token %} 

                        <div class="form-group">
                            <label for="httpapi_name">接口名称</label>
                            {% if object %}
                            <input class="form-control" name="httpapi_name" id="httpapi_name" required="required" value={{ object.name }}>
                            {% else %}
                            <input class="form-control" name="httpapi_name" id="httpapi_name" required="required">
                            {% endif %}
                        </div>
                        <div class="form-group">
                            
                            <label for="httpapi_description">接口描述</label>
                            {% if object %}
                            <input class="form-control" name="httpapi_description" id="httpapi_description" required="required" value={{ object.description }}>
                            {% else %}
                            <input class="form-control" name="httpapi_description" id="httpapi_description" required="required">
                            {% endif %}
                        </div>
                        <div class="form-group">
                            <label for="httpapi_url">接口url</label>
                            {% if object %}
                            <input class="form-control" name="httpapi_url" id="httpapi_url" required="required" value={{ object.apiurl }}>
                            {% else %}
                            <input class="form-control" name="httpapi_url" id="httpapi_url" required="required">
                            {% endif %}
                        </div>

                        <div class="form-group">
                            <label for="exampleFormControlSelect1">请求方法</label>
    
                            <select class="form-control" name="httpapi_requesttype" id="httpapi_requesttype">
                                <option>GET</option>
                                <option>POST</option>
                                <option>PUT</option>
                                <option>DELETE</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="httpapi_requestheader">请求Header</label>
                            {% if object %}
                            <textarea class="form-control" name="httpapi_requestheader" id="httpapi_requestheader" rows="5">{{ object.requestHeader }}</textarea>
                            {% else %}
                            <textarea class="form-control" name="httpapi_requestheader" id="httpapi_requestheader" rows="5"></textarea>
                            {% endif %}
                        </div>
                        <div class="form-group">
                            <legend class="col-form-label">请求参数类型</legend>

                            <div class="form-check  form-check-inline">
                                <input class="form-check-input" type="radio" name="httpapi_requestparametertype" id="httpapi_form-data" value="form-data">
                                <label class="form-check-label" for="httpapi_form">
                                    表单(form-data)
                                </label>
                            </div>
                            <div class="form-check  form-check-inline">
                                <input class="form-check-input" type="radio" name="httpapi_requestparametertype" id="httpapi_raw" value="raw">
                                <label class="form-check-label" for="httpapi_raw">
                                    原数据(raw)
                                </label>
                            </div>

                        </div>
                        <div class="form-group">
                            
                            <label for="httpapi_requestbody">请求数据</label>
                            {% if object %}
                            <textarea class="form-control" name="httpapi_requestbody" id="httpapi_requestbody" rows="5">{{ object.requestBody }}</textarea>
                            {% else %}
                            <textarea class="form-control" name="httpapi_requestbody" id="httpapi_requestbody" rows="5"></textarea>
                            {% endif %}
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
{% if object %}
<script>
    
    var e = document.getElementById("httpapi_requesttype")
    var optionsText="{{ object.requestType }}"
    for(var i=0;i<e.options.length;i++){
        if(e.options[i].text==optionsText){
            e.options[i].selected=true;
        }
    }

    var eid = "httpapi_" + "{{ object.requestParameterType }}"
   
    var e2 = document.getElementById(eid)
    e2.setAttribute("checked","checked")

    
    
    
</script>
{% endif %}
{% endblock %}
```

### api接口列表

url配置
```
urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/create', views.project_create, name='project_create'),
    path('project/<int:pk>/httpapi/create', views.httpapi_create, name='httpapi_create'),
    path('project/<int:pk>/httpapi/', views.httpapi_list, name='httpapi_list')
]
```

接口列表视图
```
@login_required
def httpapi_list(request, pk):
    project = Project.objects.get(id=pk)
    
    rs = HttpApi.objects.filter(project=project)
    paginator = Paginator(rs, 5)
    page = request.GET.get('page')
    httpapis = paginator.get_page(page)
    return render(request, "project/httpapi_list.html", {"project": project, "objects": httpapis})
```

接口列表模板 httpapi_list.html

```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">api接口</a>
                </li>

                <li class="breadcrumb-item active">接口列表</li>

            </ol>
            <div class="panel-heading">
                    <p>
                        <button onclick="location.href='{% url 'httpapi_create' project.id %}'" type="button" class="btn btn-primary btn-xs">新建接口</button>
                    </p>
               </div>
            <div class="panel-body">
                <div class="table">
                    <table class="table  table-sm   table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>接口名称</th>
                                <th>接口url</th>
                                <th>请求方式</th>
                                <th>更新时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for object in objects %}
                            <tr>
                                <td>{{object.name}}</td>
                                <td>{{object.description}}</td>
                                <td>{{object.requestType}}</td>
                                <td>{{object.lastUpdateTime }}</td>
                                <td>
                                    <a class="playitbtn tryitbtnsyntax" href="#">编辑</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <div class="pagination">
                            <span class="step-links">
                                {% if objects.has_previous %}
                                   
                                    <a href="?page={{ object.previous_page_number }}">上一页</a>
                                {% endif %}
                        
                                <span class="current">
                                    Page {{ objects.number }} of {{ objects.paginator.num_pages }}.
                                </span>
                        
                                {% if objects.has_next %}
                                    <a href="?page={{ objects.next_page_number }}">下一页</a>
                                    
                                {% endif %}
                            </span>
                        </div>
                </div>
                <!-- /.table-responsive -->
            </div>
            <!-- /.panel -->
        </div>
        <!-- /.col-lg-12 -->
    </div>

    {% endblock %}
```

更新project_base.html

```
        <li class="nav-item">
          <a class="nav-link active" href={% url "project_detail" project.id %}>项目概况</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href={% url "httpapi_list" project.id %}>api接口</a>
        </li>
```

### 编辑api接口

配置url
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('project/',views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/create', views.project_create, name='project_create'),
    path('project/<int:pk>/httpapi/create', views.httpapi_create, name='httpapi_create'),
    path('project/<int:pk>/httpapi/', views.httpapi_list, name='httpapi_list'),
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/edit', views.httpapi_edit, name='httpapi_edit')
]
```

编辑api接口视图

```
@login_required
def httpapi_edit(request, project_id, httpapi_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        return render(request,"project/httpapi_form.html", {"project": project, "object": httpapi })
    if request.method == "POST":

        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        httpapi.name = request.POST.get("httpapi_name")
        httpapi.description = request.POST.get("httpapi_description")
        httpapi.apiurl = request.POST.get("httpapi_url")
        httpapi.requestType = request.POST.get("httpapi_requesttype")
        httpapi.requestHeader = request.POST.get("httpapi_requestheader")
        httpapi.requestParameterType = request.POST.get("httpapi_requestparametertype")
        httpapi.requestBody = request.POST.get("httpapi_requestbody")
        httpapi.userUpdate= request.user
        httpapi.save()
        return redirect("httpapi_list",project.id)
```

更新httpapi_list.html

```
                                <td>
                                    <a class="playitbtn tryitbtnsyntax" href={% url "httpapi_edit" project.id object.id %}>编辑</a>
                                </td>
```


##作业

实现接口详情功能







