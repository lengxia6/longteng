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

ASSERT_TYPE_CHOICE = (
    ('noselect','无'),
    ('in', '包含'),
    ('status_code', '状态码')

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
    assertType = models.CharField(max_length=20,  verbose_name="断言类型", default="noselect",choices=ASSERT_TYPE_CHOICE)
    assertContent = models.CharField(max_length=1024, verbose_name="断言内容", blank=True, null=True)

    def __str__(self):
        return self.name

class HttpRunResult(models.Model):
    """
    接口测试结果
    """
    httpapi = models.ForeignKey(HttpApi, on_delete=models.CASCADE, verbose_name="所属接口")
    response = models.TextField(verbose_name="响应结果")
    header = models.TextField(verbose_name="响应header")
    statusCode = models.IntegerField(verbose_name="状态码")
    assertResult = models.CharField(max_length=20, null=True, verbose_name="断言结果")





