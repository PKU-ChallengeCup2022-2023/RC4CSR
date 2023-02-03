from django.contrib import admin
from .models import Book, SearchRecord, Book_Tag

# Register your models here.
admin.site.register(Book)
admin.site.register(SearchRecord)
admin.site.register(Book_Tag)