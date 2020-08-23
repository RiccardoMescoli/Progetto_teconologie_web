from django.urls import path
from book_functionalities import views

app_name = 'book_functionalities'

urlpatterns = [
    path('author/create', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/detail', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/edit', views.AuthorEditView.as_view(), name='author-edit'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),

    path('book/create', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/detail', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/edit', views.BookEditView.as_view(), name='book-edit'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='book-delete'),

    path('book_genre/', views.BookGenreListView.as_view(), name='book-genre-list'),
    path('book_genre/create', views.BookGenreCreateView.as_view(), name='book-genre-create'),
    path('book_genre/list', views.BookGenreListView.as_view(), name='book-genre-list-explicit'),
    path('book_genre/<int:pk>/edit', views.BookGenreEditView.as_view(), name='book-genre-edit'),
    path('book_genre/<int:pk>/delete', views.BookGenreDeleteView.as_view(), name='book-genre-delete'),

    path('user/book_review/create', views.BookReviewCreateView.as_view(), name='book-review-create'),
    path('user/book_review/<int:pk>/edit', views.BookReviewEditView.as_view(), name='book-review-edit'),
    path('user/book_review/<int:pk>/delete', views.BookReviewDeleteView.as_view(), name='book-review-delete'),
]