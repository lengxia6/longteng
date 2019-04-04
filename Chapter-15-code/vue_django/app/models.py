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