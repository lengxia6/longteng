from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class AutAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')    
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AutAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance)
