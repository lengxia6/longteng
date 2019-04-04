from django.contrib import admin
from .models import Project,HttpApi,HttpRunResult

# Register your models here.

admin.site.register(Project)
admin.site.register(HttpApi)
admin.site.register(HttpRunResult)