# 第15天

## 接口删除
删除已有的接口

### url配置

```
path('project/<int:project_id>/httpapi/<int:httpapi_id>/delete', views.httpapi_delete, name='httpapi_delete'),
```

### 添加视图函数 httpapi_delete

```
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def httpapi_delete(request, project_id, httpapi_id):
    project = Project.objects.get(id=project_id)
    httpapi = HttpApi.objects.get(project=project, id=httpapi_id)
    if request.method == "GET":
        return  render(request, "project/httpapi_delete.html", {"project": project, "object": httpapi})
    
    if request.method == "POST":
        httpapi.delete()
        return HttpResponse("delete ok")
```
### 添加删除确认模板 

新建模板 project/httpapi_delete.html

```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">
            <div class="panel-body">
                <div class="alert alert-danger" role="alert">
                    删除接口{{ object.name }}
                </div>
                <button type="button" class="btn btn-secondary" onclick="cancel()">取消</button>
                <button type="button" class="btn btn-primary" onclick="ok()">确认</button>
            </div>
            <!-- /.panel -->
        </div>
        <!-- /.col-lg-12 -->
    </div>
</div>
<script>
function cancel(){
    //window.location.href="{% url 'httpapi_list' project.id %}"
    window.history.back()
}

function ok(){
    var request = new XMLHttpRequest()
    
    request.open("POST", "{% url 'httpapi_delete' project.id object.id %}")
    request.onreadystatechange = function(){
        if (request.readyState === 4 && request.status === 200){
            window.location.href="{% url 'httpapi_list' project.id %}"
        }
    }
    request.send(null)
}
</script>
{% endblock %}
```

### 更新 httpapi_list.html

```
<a class="playitbtn tryitbtnsyntax" href={% url "httpapi_delete" project.id object.id %}>删除</a>
```

更新视图httpapi_delete
```

#return HttpResponse("delete ok")
return redirect("httpapi_list",project.id)
```

## 测试集合管理

创建包含多个接口的测试集合,运行测试集合,查看测试运行结果

### 添加moddel 

```
class HttpTest(models.Model):
    """
    接口测试
    """
    name = models.CharField(max_length=50, verbose_name='接口测试名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    httpapis = models.CharField(max_length=50, verbose_name='包含http接口id')

    def __str__(self):
        return self.name
```
更新数据库

### 新建测试集合

配置url
```
path('project/<int:project_id>/test/create', views.test_create, name='test_create'),
```

添加视图函数 test_create

```
from .models import Project, HttpApi, HttpRunResult, HttpTest

@login_required
def test_create(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "GET":
        httpapis = project.httpapi_set.all()
        return  render(request, "project/httpapi_test_form.html", {"project": project, "objects": httpapis})
    if request.method == "POST":
        httprunresults = []
        httpapi_name = request.POST.get("httpapi_name")
        to = request.POST.getlist("to")
        httpapis = ",".join(to)
        httptest = HttpTest(name=httpapi_name,httpapis=httpapis,project=project)
        httptest.save()
        return HttpResponse(httpapis)
```
添加模板 httpapi_test_form.html
```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">
            <form method="post">{% csrf_token %}
                <div class="row form-group">
                    <div class="col-lg-5">
                    <label for="httpapi_name">接口测试名称</label>
                    <input class="form-control" name="httpapi_name" id="httpapi_name" required="required">
                    </div>
                </div>
                <p>选择要测试的接口</p>
                <div class="row form-group">
                    <div class="col-lg-5">
                        <select name="from" class="form-control" id="multiselect" size="8" multiple="multiple">
                            {% for object in objects %}
                            <option value="{{ object.id }}">{{ object.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-lg-1">
                        <button type="button" id="multiselect_rightAll" class="btn btn-block"><i class="fa fa-angle-double-right"></i></button>
                        <button type="button" id="multiselect_rightSelected" class="btn btn-block"><i class="fa fa-angle-right"></i></button>
                        <button type="button" id="multiselect_leftSelected" class="btn btn-block"><i class="fa fa-angle-left"></i></button>
                        <button type="button" id="multiselect_leftAll" class="btn btn-block"><i class="fa fa-angle-double-left"></i></button>
                    </div>


                    <div class="col-lg-5">
                        <select name="to" id="multiselect_to" class="form-control" size="8" multiple="multiple">

                        </select>
                    </div>
                </div>
                <button type="submit" class="btn btn-default">提交</button>
            </form>
            <!-- /.panel -->
        </div>
        <!-- /.col-lg-12 -->
    </div>
</div>
<script>

</script> {% endblock %}
```

### 测试集合列表

配置url
```
path('project/<int:project_id>/test/', views.test_list, name='test_list'),
```

添加视图函数 test_list

```
@login_required
def test_list(request, project_id):
    project = Project.objects.get(id=project_id)
    rs = HttpTest.objects.filter(project_id=project_id).order_by("-id")
    paginator = Paginator(rs, 5)
    page = request.GET.get('page')
    tests = paginator.get_page(page)
    return render(request,"project/test_list.html", {"project": project, "objects": tests})
```

添加视图模板

project/test_list.html

```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">接口测试</a>
                </li>

                <li class="breadcrumb-item active">测试列表</li>

            </ol>
            <div class="panel-heading">
                    <p>
                        <button onclick="location.href='{% url 'test_create' project.id %}'" type="button" class="btn btn-primary btn-xs">新建测试</button>
                    </p>
                </div>
            <div class="panel-body">
                <div class="table">
                    <table class="table  table-sm   table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>测试名称</th>
    
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for object in objects %}
                            <tr>
                                <td>{{object.name}}</td>
                               
                                <td>
                                    
                                    <a class="playitbtn tryitbtnsyntax" href="#">运行</a>
                                    <a class="playitbtn tryitbtnsyntax" href="#">结果</a>
                                    
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

更新project/project_base.html
```
<li class="nav-item">
    <a class="nav-link" href={% url "test_list" project.id %}>api测试</a>
</li>
```

更新test_create函数
```
#return HttpResponse(httpapis)
        return redirect("test_list",project.id)
```

### 运行测试集合

添加model
```
class HttpTestResult(models.Model):
    """
    测试结果
    """
    httptest = models.ForeignKey(HttpTest, on_delete=models.CASCADE, verbose_name='测试')
    httprunresults = models.CharField(max_length=50, verbose_name='运行结果id')
    status = models.CharField(max_length=50, verbose_name='测试结果')

    def __str__(self):
        return self.httptest.name
```

添加lib/utils.py  封装接口运行功能
```
import  requests
from apiautotest.models import HttpApi, HttpRunResult
def test_run(httpapi):
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
    return httprunresult
```

配置url

```
path('project/<int:project_id>/test/<int:test_id>/run', views.test_run, name='test_run'),
```

添加视图函数

```
from .models import Project, HttpApi, HttpRunResult, HttpTest, HttpTestResult
from .lib import utils

@login_required
def test_run(request, project_id, test_id):
    project = Project.objects.get(id=project_id)
    test = HttpTest.objects.get(id=test_id)
    if request.method == "GET":
        httprunresults = []
        httprunresult_asserts = []
        httpapis = test.httpapis.split(",")
        for httpapi_id in httpapis:
            httpapi = HttpApi.objects.get(id=int(httpapi_id))
            httprunresult = utils.test_run(httpapi)
            httprunresults.append(str(httprunresult.id))
            httprunresult_asserts.append(httprunresult.assertResult)
        if "failed"  in httprunresult_asserts:
            status = "failed"
        else:
            status = "ok"
        httprunresults = ','.join(httprunresults)
        httptestresult = HttpTestResult(httptest=test, httprunresults=httprunresults,status=status)
        httptestresult.save()
        return HttpResponse(httprunresults)
```

更新test_list.html模板
```
<a class="playitbtn tryitbtnsyntax" href="{% url 'test_run' project.id object.id %}">运行</a>
```

### 显示运行结果

查看测试集合结果

配置url
```
path('project/<int:project_id>/test/<int:test_id>/result', views.test_result, name='test_result')
```

添加视图
```
@login_required            
def test_result(request, project_id, test_id):
    project = Project.objects.get(id=project_id)
    try:
        testresult = HttpTestResult.objects.filter(httptest_id=test_id).order_by("-id")[0]
    except:
        return render(request,"project/test_result.html", {"project":project})
    status = testresult.status
    httprunresult_ids = testresult.httprunresults.split(",")
    httprunresults = []
    for httprunresult_id in httprunresult_ids :
        httprunresult = HttpRunResult.objects.get(id=httprunresult_id)
        httprunresults.append(httprunresult)

    return render(request,"project/test_result.html", {"project":project, "testresult":testresult, "objects": httprunresults })
```

添加视图 project/test_result.html
```
{% extends "project/project_base.html" %} {% block project %}
<p></p>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">

            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="#">接口测试</a>
                </li>

                <li class="breadcrumb-item active">{{ testresult.httptest.name }}测试结果</li>

            </ol>
            
            <div class="panel-body">
                {% if objects %}
                <div class="table">
                    <table class="table  table-sm   table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>接口名称</th>
    
                                <th>状态</th>
                                <th>详情</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for object in objects %}
                            <tr>
                                <td>{{object.httpapi.name}}</td>
                                <td>{{object.assertResult}}</td>
                                <td>
                                    
                                    <a class="playitbtn tryitbtnsyntax" href="{% url 'httpapi_result' project.id object.httpapi_id %}">详情</a>
                                    
                                    
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
                {% else %}
                还没有运行，无测试结果
                {% endif %}
            </div>
            <!-- /.panel -->
        </div>
        <!-- /.col-lg-12 -->
    </div>

    {% endblock %}
```

更新test_list.html
```
<a class="playitbtn tryitbtnsyntax" href="{% url 'test_result' project.id object.id %}">结果</a>
```

更新test_run 函数
```
#return HttpResponse(httprunresults)
return redirect("test_result",project_id, test_id)
```