from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

# Create your views here.

@login_required
def index(request):
    """
    首页视图
    """
    # 判断权限
    if not request.user.has_perm('catalog.view_book'):
        return HttpResponse("no permession")
    # 统计图书的数目
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # 可接图书的数目 (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # 作者的数目
    
    # 使用session统计访问次数
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # 渲染模板
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_visits': num_visits},
    )

from django.views import generic

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'   # book list 变量的名称
    queryset = Book.objects.all()
    #queryset = Book.objects.filter(title__icontains='python')[:5] # 书名包含python的5本书 
    template_name = 'book_list.html'  # 指定template名称

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            msg = "账号或密码错误"
            return render(request,"login.html",{"msg": msg})

def user_logout(request):
    logout(request)
    return redirect('user_login')

def book_create(request):
    if request.method == "GET":
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = {"authors": authors, "genres": genres}
        return render(request, "book_form.html",context)
    if request.method == "POST":
        book_title = request.POST.get("book_title")
        book_author_id = request.POST.get("book_author")
        book_summary = request.POST.get("book_summary")
        book_isbn = request.POST.get("book_isbn")
        book_genre_ids = request.POST.getlist("book_genre")
        book_author = Author.objects.get(id = book_author_id)
        book = Book(title=book_title, author=book_author, summary=book_summary, isbn=book_isbn)
        book.save()
        for book_genre_id in  book_genre_ids:
            book_genre = Genre.objects.get(id = book_genre_id)
            book.genre.add(book_genre)
        book.save()
        #return HttpResponse(book_genre_ids)
        return redirect('books')

def book_edit(request, pk):
    if request.method == "GET":
        book = Book.objects.get(id = pk)
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = { "book": book, "authors": authors, "genres": genres }
        return render(request, "book_edit.html", context)
    if  request.method == "POST":
        book = Book.objects.get(id = pk)
        book.title = request.POST.get("book_title")
        book_author_id = request.POST.get("book_author")
        book.summary = request.POST.get("book_summary")
        book.isbn = request.POST.get("book_isbn")
        book_genre_ids = request.POST.getlist("book_genre")
        book.author = Author.objects.get(id = book_author_id)
        book.genre.clear()
        for book_genre_id in  book_genre_ids:
            book_genre = Genre.objects.get(id = book_genre_id)
            book.genre.add(book_genre)
        book.save()
        return redirect('books')