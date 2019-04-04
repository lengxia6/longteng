from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('books/create', views.book_create, name='book_create'),
    path('book/<int:pk>/edit', views.book_edit, name='book_edit'),
]