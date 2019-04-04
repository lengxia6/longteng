from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    fields = ['last_name', 'first_name',  ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'display_genre')
    list_filter = ('title',)
    inlines = [BooksInstanceInline]
#admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
#admin.site.register(BookInstance)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('book','imprint', 'id')
        }),
        ('借书状态', {
            'fields': ('status', 'due_back')
        }),
    )


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


