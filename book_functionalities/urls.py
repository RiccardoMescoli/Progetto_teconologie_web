from django.urls import path
from book_functionalities import views

app_name = 'book_functionalities'

urlpatterns = [
    path('author/create', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/detail', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/edit', views.AuthorEditView.as_view(), name='author-edit'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),

    path('book/top_list', views.book_top_list_view, name='book-top-list'),
    path('book/create', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/detail', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/edit', views.BookEditView.as_view(), name='book-edit'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='book-delete'),

    path('book_genre/', views.BookGenreListView.as_view(), name='book-genre-list'),
    path('book_genre/create', views.BookGenreCreateView.as_view(), name='book-genre-create'),
    path('book_genre/list', views.BookGenreListView.as_view(), name='book-genre-list-explicit'),
    path('book_genre/<int:pk>/edit', views.BookGenreEditView.as_view(), name='book-genre-edit'),
    path('book_genre/<int:pk>/delete', views.BookGenreDeleteView.as_view(), name='book-genre-delete'),

    path('book_review/search', views.book_review_search_view, name='book-review-search'),
    path('user/book_review/create', views.BookReviewCreateView.as_view(), name='book-review-create'),
    path('user/book_review/<int:pk>/edit', views.BookReviewEditView.as_view(), name='book-review-edit'),
    path('user/book_review/<int:pk>/delete', views.BookReviewDeleteView.as_view(), name='book-review-delete'),

    path('book_recommendation/search', views.book_recommendation_search_view, name='book-recommendation-search'),
    path(
        'user/book_recommendation/create',
        views.BookRecommendationCreateView.as_view(),
        name='book-recommendation-create'
    ),
    path(
        'user/book_recommendation/<int:pk>/delete',
        views.BookRecommendationDeleteView.as_view(),
        name='book-recommendation-delete'
    ),

    path('report/list', views.report_list_view, name='report-list'),
    path('book_review/<int:pk>/report/clear', views.review_report_clear, name='book-review-report-clear'),

    path('ajax/report', views.ajax_report_review, name='ajax-report'),
]