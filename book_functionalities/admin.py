from django.contrib import admin

# Register your models here.
from book_functionalities.models import Author, Book, BookGenre, BookReview

admin.site.register(Author)
admin.site.register(BookGenre)
admin.site.register(Book)
admin.site.register(BookReview)
