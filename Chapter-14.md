# 第14天

## 更新httpapi接口功能
httpapi添加断言字段

### 添加models 字段

```
ASSERT_TYPE_CHOICE = (
    ('noselect','无'),
    ('in', '包含'),
    ('status_code', '状态码')

)

class HttpApi(models.Model):
    """
    接口信息
    """
    ......
    assertType = models.CharField(max_length=20,  verbose_name="断言类型", default="noselect",choices=ASSERT_TYPE_CHOICE)
    assertContent = models.CharField(max_length=1024, verbose_name="断言内容", blank=True, null=True)

    def __str__(self):
        return self.name
```

### 更新httpapi表单内容
templates/project/httpapi_form.html
```
<div class="form-group">
    <label for="httpapi_asserttype">断言类型</label>

    <select class="form-control" name="httpapi_asserttype" id="httpapi_asserttype">
        <option vaule="noselect">无</option>
        <option value="in">包含</option>
        <option value="status_code">状态码</option>
    </select>
</div>
<div class="form-group">
    
    <label for="httpapi_assertcontent">断言内容</label>
    {% if object %}
    <textarea class="form-control" name="httpapi_assertcontent" id="httpapi_assertcontent" rows="5">{{ object.assertContent }}</textarea>
    {% else %}
    <textarea class="form-control" name="httpapi_assertcontent" id="httpapi_assertcontent" rows="5"></textarea>
    {% endif %}
</div>
```

###  更新view视图
```
@login_required
def httpapi_create(request, pk):
    ......
        httpapi_assertType = request.POST.get("httpapi_asserttype")
        httpapi_assertContent = request.POST.get("httpapi_assertcontent")
        userupdate= request.user

        .......
                          assertType=httpapi_assertType,
                          assertContent=httpapi_assertContent
                          )
        httpapi.save()

        #return HttpResponse("ok")
        return redirect("httpapi_list",httpapi_project.id)


@login_required
def httpapi_edit(request, project_id, httpapi_id):
   .....
        
        httpapi.assertType = request.POST.get("httpapi_asserttype")
        httpapi.assertContent = request.POST.get("httpapi_assertcontent")
        httpapi.userUpdate= request.user
        httpapi.save()
        return redirect("httpapi_list",project.id)
```


## 运行功能

运行httpapi接口

### 定义models 

```
class HttpRunResult(models.Model):
    """
    接口测试结果
    """
    httpapi = models.ForeignKey(HttpApi, on_delete=models.CASCADE, verbose_name="所属接口")
    response = models.TextField(verbose_name="响应结果")
    header = models.TextField(verbose_name="响应header")
    statusCode = models.IntegerField(verbose_name="状态码")
    assertResult = models.CharField(max_length=20, null=True, verbose_name="断言结果")
```
执行命令应用的数据库

### 将HttpRunResult 注册到django admin
```
from django.contrib import admin
from .models import Project,HttpApi,HttpRunResult

# Register your models here.

admin.site.register(Project)
admin.site.register(HttpApi)
admin.site.register(HttpRunResult)
```

### 设置url 
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
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/edit', views.httpapi_edit, name='httpapi_edit'),
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/run', views.httpapi_run, name='httpapi_run')
]
```

### 更新httpapi_list.html
```
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_edit" project.id object.id %}>编辑</a>
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_run" project.id object.id %}>运行</a>
```


### httpapi_run 视图
添加get测试
```
@login_required
def httpapi_run(request, project_id, httpapi_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        response_header = ""
        assertresult = ""
        if httpapi.requestType == "GET":
            data = {}
            if httpapi.requestBody != "":
                for line in httpapi.requestBody.strip().split("\n"):
                    key,value = line.split("=")
                    data[key] = value
                    
            r = requests.get(url=httpapi.apiurl,params=data)
            for item in r.headers:
                response_header += "%s: %s\n" % (item, r.headers.get(item))
            if httpapi.assertType == "noselect":
                assertresult = ""
            elif httpapi.assertType == "in":
                if httpai.assertContent.strip() in r.text:
                    assertresult = "ok"
                else:
                    assertresult = "failed"
            elif httpapi.assertType == "status_code":
                if httpapi.assertContent.strip() == str(r.status_code):
                    assertresult = "ok"
                else:
                    assertresult = "failed"
        httprunresult = HttpRunResult(httpapi=httpapi, 
                                      response=r.text, 
                                      header=response_header, 
                                      statusCode = r.status_code,
                                      assertResult = assertresult
                                      )
        httprunresult.save()
        return HttpResponse("result add ok")
```
完成后编辑httapi接口，点击运行
### 模板httpapi_result.html

```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

           

            <div class="panel-body">
            {% if object %}

                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <a class="nav-link active" href="#response" data-toggle="tab">响应内容</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#header" data-toggle="tab">响应Headers</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#status_code" data-toggle="tab">响应状态码</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#assert_result" data-toggle="tab">断言结果</a>
                    </li>

                </ul>


                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="response" role="textarea">
                        <textarea class="form-control" rows="10" readonly>{{ object.response }}</textarea>
                    </div>
                    <div class="tab-pane fade" id="header" role="tabpanel">
                        <textarea class="form-control" rows="10" readonly>{{ object.header }}</textarea>
                    </div>
                    <div class="tab-pane fade" id="status_code" role="tabpanel">
                        <textarea class="form-control" rows="10" readonly>{{ object.statusCode }}</textarea>
                    </div>
                    <div class="tab-pane fade" id="assert_result" role="tabpanel">
                            <textarea class="form-control" rows="10" readonly>{{ object.assertResult }}</textarea>
                        </div>

                </div>
            {% else %}
            还未执行
            {% endif %}

            </div>
            <!-- /.panel -->
        </div>
        <!-- /.col-lg-12 -->
    </div>

    {% endblock %}
```

### httpapi_result  url
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
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/edit', views.httpapi_edit, name='httpapi_edit'),
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/run', views.httpapi_run, name='httpapi_run'),
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/result', views.httpapi_result, name='httpapi_result')
]
```

### httpapi_result view
```
@login_required
def httpapi_result(request, project_id, httpapi_id):
    project = Project.objects.get(id=project_id)
    httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
    try:
        httpresult = HttpRunResult.objects.filter(httpapi=httpapi).order_by("-id")[0]
    except:
        return render(request,"project/httpapi_result.html", {"project": project})

    return render(request,"project/httpapi_result.html",{"project": project, "object": httpresult })
```

### 更新httpapi_list.html
```
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_edit" project.id object.id %}>编辑</a>
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_run" project.id object.id %}>运行</a>
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_result" project.id object.id %}>结果</a>
```

#### post 请求的测试 练习
正确运行post 表单请求

```
@login_required
def httpapi_run(request, project_id, httpapi_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
        response_header = ""
        assertresult = ""
        if httpapi.requestType == "GET":
            data = {}
            if httpapi.requestBody != "":
                for line in httpapi.requestBody.strip().split("\n"):
                    key,value = line.split("=")
                    data[key] = value
                    
            r = requests.get(url=httpapi.apiurl,params=data)
            for item in r.headers:
                response_header += "%s: %s\n" % (item, r.headers.get(item))
            if httpapi.assertType == "noselect":
                assertresult = ""
            elif httpapi.assertType == "in":
                if httpai.assertContent.strip() in r.text:
                    assertresult = "ok"
                else:
                    assertresult = "failed"
            elif httpapi.assertType == "status_code":
                if httpapi.assertContent.strip() == str(r.status_code):
                    assertresult = "ok"
                else:
                    assertresult = "failed"
        if httpapi.requestType == "POST":
            request_header = {}
            if httpapi.requestHeader != "":
                for line in httpapi.requestHeader.strip().split("\n"):
                    key,value = line.split("=")
                    request_header[key] = value
            if httpapi.requestParameterType == "form-data":
                request_body = {}
                for line in httpapi.requestBody.strip().split("\n"):
                    key,value = line.split("=")
                    request_body[key] = value
                r = requests.post(url=httpapi.apiurl,data=request_body,headers=request_header)
            elif httpapi.requestParameterType == "raw":
                request_body = httpapi.requestBody.strip()
                print(request_body)
                r = requests.post(url=httpapi.apiurl,data=request_body,headers=request_header)
            for item in r.headers:
                response_header += "%s: %s\n" % (item, r.headers.get(item))
            if httpapi.assertType == "noselect":
                assertresult = ""
            elif httpapi.assertType == "in":
                if httpai.assertContent.strip() in r.text:
                    assertresult = "ok"
                else:
                    assertresult = "failed"
            elif httpapi.assertType == "status_code":
                if httpapi.assertContent.strip() == str(r.status_code):
                    assertresult = "ok"
                else:
                    assertresult = "failed"
                      
        httprunresult = HttpRunResult(httpapi=httpapi, 
                                      response=r.text, 
                                      header=response_header, 
                                      statusCode = r.status_code,
                                      assertResult = assertresult
                                      )
        httprunresult.save()
        #return HttpResponse("result add ok")
        return redirect("httpapi_result",project.id, httpapi.id)
```

### 正确运行post raw请求
比如json


