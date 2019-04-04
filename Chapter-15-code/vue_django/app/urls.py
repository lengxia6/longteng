from django.urls import path
from . import views
urlpatterns = [
    path('login', views.user_login, name="login"),
    path('project/list', views.project_list, name="project_list"),
    path('project/edit', views.project_edit, name="project_edit"),
    path('project/add', views.project_add, name="project_add"),
    path('project/delete', views.project_delete, name="project_delete"),
    path('project/batchdelete', views.project_batchdelete, name="project_batchdelete"),
]