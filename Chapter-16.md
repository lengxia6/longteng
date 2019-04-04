# 第16天

## 报告

### url配置

```
path('project/<int:project_id>/report', views.report_list, name='report_list')
```

### 添加视图函数

```
@login_required
def report_list(request, project_id):
    project = Project.objects.get(id=project_id)
    try:
        testresult = HttpTestResult.objects.filter(httptest__project=project).order_by("-id")
    except Exception as e:
        return render(request,"project/report_list.html", {"project":project})
    
    return render(request,"project/report_list.html", {"project":project,  "objects": testresult })
```
### 添加模板
report_list.hml

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

                <li class="breadcrumb-item active">{{ testresult.httptest.name }}测试报告</li>

            </ol>
            
            <div class="panel-body">
                {% if objects %}
                <div class="table">
                    <table class="table  table-sm   table-hover" id="dataTables-example">
                        <thead>
                            <tr>
                                <th>接口名称</th>
                                <th>状态</th>
                                <th>时间</th>
                                <th>详情</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for object in objects %}
                            <tr>
                                <td>{{object.httptest.name}}</td>
                                <td>{{object.status}}</td>
                                <td>{{object.runTime}}</td>
                                <td>
                                    <a class="playitbtn tryitbtnsyntax" href="{% url 'test_result' project.id object.httptest_id %}">详情</a>
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

### 更新test_result.html

```
{% if objects %}
    <div class="col-md-4">
        <div class="card mb-3">
            <div class="card-body">
                <canvas id="myPieChart" width="100%" height="100"></canvas>
            </div>
        </div>
    </div>
    <div class="table">
```

### 更新test_result

```
    ok_count = 0
    failed_count = 0
    for httprunresult_id in httprunresult_ids :
        httprunresult = HttpRunResult.objects.get(id=httprunresult_id)
        httprunresults.append(httprunresult)
        if httprunresult.assertResult == "ok":
            ok_count += 1
        if httprunresult.assertResult == "failed":
            failed_count += 1

    return render(request,"project/test_result.html", {"project":project, "testresult":testresult, "objects": httprunresults, "ok": ok_count,"failed": failed_count })
```


### 更新base.html
```
<script>
    jQuery(document).ready(function($) {
  $('#multiselect').multiselect();
});
// 饼图
var ctx = document.getElementById("myPieChart");
if(ctx != null){
    var myPieChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ["ok", "failed"],
        datasets: [{
          data: [ {{ ok }}, {{ failed }}],
          backgroundColor: ['#007bff', '#dc3545'],
        }],
      },
    });
}
</script>
```

## dashboard

### 更新index.html
```
{% extends "base.html" %} {% block content %}
<ol class="breadcrumb">
    <li class="breadcrumb-item">
        <a href="#">Dashboard</a>
    </li>
    <li class="breadcrumb-item active">Overview</li>
</ol>
<div class="col-lg-8">
    <div class="card mb-3">
        <div class="card-body">
            <canvas id="myBarChart" width="100%" height="50"></canvas>
        </div>
        
    </div>
</div>
{% endblock %}
```

### 更新view
```
@login_required
def index(request):
    project_count = Project.objects.all().count()
    httpapi_count = HttpApi.objects.all().count()
    httptest_count = HttpTest.objects.all().count()
    httptestresult_count = HttpTestResult.objects.all().count()
    #return HttpResponse(project)
    return render(request,"index.html", {"project": project_count, "httpapi": httpapi_count,
    "httptest": httptest_count, "httptestresult": httptestresult_count})
```

### 更新base.html

```
// 柱状图
var ctx2 = document.getElementById("myBarChart");
if(ctx2 != null){
var myLineChart = new Chart(ctx2, {
  type: 'bar',
  data: {
    labels: ["项目数", "接口数", "测试数", "报告数"],
    datasets: [{
      label: "个数",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: [{{ project }}, {{ httpapi }}, {{ httptest }}, {{ httptestresult}}],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 20,
          maxTicksLimit: 1
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
}
```
## 配置依赖模块文件
requirements.txt

```
Django==2.0.5
requests==2.18.4
mysqlclient==1.3.12
gunicorn==19.9.0
```

## 线上环境部署

### 操作系统
centos 7

### 部署代码
将代码传送到linux环境下的

安装一个ssh 工具用来远程登录linux

在linux中安装lrzsz `yum install lrzsz`

执行rz 命令上传代码


### 安装mysql
数据库版本 django 2.0.*  mysql5.5
          django 2.1.*  mysql5.6

centos7
```
cd /etc/yum.repos.d/
rm -f ./*.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all
yum install mariadb
yum install mariadb-devel
#启动mysql-server
systemctl start mariadb
```

cetos6
```
cd /etc/yum.repos.d/
rm -f ./*.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
yum clean all
yum install mysql
yum install mysql-devel
# 启动
/etc/init.d/mysqld start
```

### anacoda 
一个python的发行版可快速在linux系统中配置python环境
https://repo.anaconda.com/archive/

安装anacod
```
sh ./Anaconda3-5.2.0-Linux-x86_64.sh

Welcome to Anaconda3 5.2.0

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>>

输入回车

Do you accept the license terms? [yes|no]

输入yes
Anaconda3 will now be installed into this location:
/root/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/root/anaconda3] >>>

输入/opt/anaconda3
回车

[/root/anaconda3] >>> /opt/anaconda3
PREFIX=/opt/anaconda3
installing: python-3.6.5-hc3d631a_2 ...

Do you wish to proceed with the installation of Microsoft VSCode? [yes|no]
>>> Please answer 'yes' or 'no':
no



```

### 配置虚拟环境

```
cd /opt/anaconda3/bin

./pip install virtualenv

cd /opt
/opt/anaconda3/bin/virtualenv env


source env/bin/activate
(env) [root@python-dev opt]#
```

### 查看项目依赖模块版本
`pip freeze`
### 安装依赖模块
```
# 在env环境下进入代码目录
cd /opt/autotest
# 安装依赖模块
(env) [root@python-dev autotest]# pip install -r requirements.txt  

```
### 初始化数据库
```
# 连接数据库
mysql -uroot -p
# 创建数据库
create database autotest /*!40100 DEFAULT CHARACTER SET utf8 */;
# 退出数据库
quit
```

初始化书库表

`python manage.py  migrate`

### 启动django应用

```
(env) [root@python-dev autotest]# nohup gunicorn autotest.wsgi >gunicorn.log 2>&1 &
[1] 14207
(env) [root@python-dev autotest]# tail gunicorn.log
nohup: ignoring input
[2018-09-08 11:09:45 +0000] [14207] [INFO] Starting gunicorn 19.9.0
[2018-09-08 11:09:45 +0000] [14207] [INFO] Listening at: http://127.0.0.1:8000 (14207)
[2018-09-08 11:09:45 +0000] [14207] [INFO] Using worker: sync
[2018-09-08 11:09:45 +0000] [14210] [INFO] Booting worker with pid: 14210
```


### 启动nginx前提
关闭iptables
```
# centos7
systemctl stop firewalld
# centos6
/etc/init.d/iptables stop

```
关闭selinux

`setenforce 0`

### 安装nginx

`vi  /etc/yum.repos.d/nginx.repo`

# 粘贴一下内容

```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
```

# 安装命令

```
yum install nginx
systemctl start nginx
```

### 配置nginx
vi /etc/nginx/conf.d/default.conf

```
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        #root   /usr/share/nginx/html;
        #index  index.html index.htm;
        proxy_pass http://localhost:8000;
    }

    location /static {
       alias  /opt/autotest/apiautotest/static;
    }



    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```


# reload
`nginx -s reload`

