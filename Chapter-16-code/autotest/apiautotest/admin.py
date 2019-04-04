from django.contrib import admin
from .models import Project,HttpApi,HttpRunResult,HttpTest,HttpTestResult

# Register your models here.

admin.site.register(Project)
admin.site.register(HttpApi)
admin.site.register(HttpRunResult)
admin.site.register(HttpTest)
admin.site.register(HttpTestResult)