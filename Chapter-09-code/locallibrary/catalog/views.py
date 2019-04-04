from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    首页视图
    """
    # 统计图书的数目
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # 可接图书的数目 (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # 作者的数目
    
    # 渲染模板
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # book list 变量的名称
    queryset = Book.objects.all()
    #queryset = Book.objects.filter(title__icontains='python')[:5] # 书名包含python的5本书 
    template_name = 'book_list.html'  # 指定template名称


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'