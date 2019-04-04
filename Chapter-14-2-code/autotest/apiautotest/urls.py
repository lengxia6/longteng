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
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/result', views.httpapi_result, name='httpapi_result'),
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/delete', views.httpapi_delete, name='httpapi_delete'),
    path('project/<int:project_id>/test/create', views.test_create, name='test_create'),
    path('project/<int:project_id>/test/', views.test_list, name='test_list'),
    path('project/<int:project_id>/test/<int:test_id>/run', views.test_run, name='test_run'),
    path('project/<int:project_id>/test/<int:test_id>/result', views.test_result, name='test_result')
]